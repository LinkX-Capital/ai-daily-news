#!/usr/bin/env bash
# AI 前沿动态：生成、校验并发布指定日期的日报。
#
# 成功的唯一判据是 archive/manifests/<date>.json 中 status=published。
# feed_v5.py 只负责产出 status=ready；本脚本完成截图、Git 推送和可选通知后，
# 才会原子地把 manifest 推进到 published。

set -Eeuo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${AI_DAILY_NEWS_DIR:-$SCRIPT_DIR}"

load_pipeline_environment() {
    local env_file=""
    if [ -n "${PIPELINE_ENV_FILE:-}" ]; then
        env_file="$PIPELINE_ENV_FILE"
        if [ ! -r "$env_file" ]; then
            echo "❌ PIPELINE_ENV_FILE 不可读：$env_file" >&2
            exit 78
        fi
    elif [ -r "$PROJECT_DIR/.env" ]; then
        env_file="$PROJECT_DIR/.env"
    elif [ -n "${HOME:-}" ] && [ -r "$HOME/.zshrc" ]; then
        env_file="$HOME/.zshrc"
    fi

    if [ -n "$env_file" ]; then
        # allexport 让 .env 中普通 KEY=value 也成为子进程环境变量。
        # 临时关闭 nounset，以兼容交互式 shell 配置中对可选变量的引用。
        set +u
        set -a
        if source "$env_file" >/dev/null; then
            :
        else
            rc=$?
            set +a
            set -u
            echo "❌ 管线环境文件加载失败（退出码 ${rc}）" >&2
            exit "$rc"
        fi
        set +a
        set -u
    fi
}

load_pipeline_environment
set -Eeuo pipefail

PYTHON_BIN="${PYTHON_BIN:-python3}"
GIT_BIN="${GIT_BIN:-git}"
MANIFEST_TOOL="$PROJECT_DIR/pipeline_manifest.py"
MANIFEST_DIR="${MANIFEST_DIR:-$PROJECT_DIR/archive/manifests}"
LOCK_DIR="${PIPELINE_LOCK_DIR:-/tmp/ai-daily-news.pipeline.lock}"

log() {
    printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

usage() {
    echo "用法: $0 [YYYY-MM-DD]" >&2
}

if [ "$#" -gt 1 ]; then
    usage
    exit 64
fi

# REPORT_DATE 在脚本入口只计算一次，随后显式传给每个日期敏感步骤。
# 未显式指定时使用“最近一个已经走完截止时间的日报日期”；这样机器若在
# 06:40 前启动，不会提前发布一个尚未闭窗的当日版本。
if [ "$#" -eq 1 ]; then
    REPORT_DATE="$1"
elif [ -n "${REPORT_DATE:-}" ]; then
    REPORT_DATE="$REPORT_DATE"
else
    REPORT_DATE="$(
        "$PYTHON_BIN" "$MANIFEST_TOOL" resolve-date \
            --timezone "${REPORT_TIMEZONE:-Asia/Shanghai}" \
            --cutoff-hour "${REPORT_CUTOFF_HOUR:-6}" \
            --cutoff-minute "${REPORT_CUTOFF_MINUTE:-40}"
    )"
fi
if ! "$PYTHON_BIN" -c \
    'from datetime import date; import sys; value=sys.argv[1]; parsed=date.fromisoformat(value); raise SystemExit(0 if parsed.isoformat() == value else 1)' \
    "$REPORT_DATE" >/dev/null 2>&1; then
    echo "❌ 无效 REPORT_DATE：应为 YYYY-MM-DD" >&2
    exit 64
fi

export REPORT_DATE
export NEWS_DATE="$REPORT_DATE"

MANIFEST_FILE="$MANIFEST_DIR/$REPORT_DATE.json"
MD_FILE="$PROJECT_DIR/daily-ai-news-$REPORT_DATE.md"
HTML_FILE="$PROJECT_DIR/daily-ai-news-$REPORT_DATE.html"
SCREENSHOT_FILE="$PROJECT_DIR/daily-ai-news-$REPORT_DATE-mobile.png"
INDEX_FILE="$PROJECT_DIR/index.html"
ARCHIVE_FILE="$PROJECT_DIR/archive/news_$REPORT_DATE.json"

mkdir -p "$MANIFEST_DIR"
cd "$PROJECT_DIR"

LOCK_ACQUIRED=0
release_lock() {
    if [ "$LOCK_ACQUIRED" -eq 1 ]; then
        rm -f -- "$LOCK_DIR/pid" "$LOCK_DIR/report_date"
        rmdir -- "$LOCK_DIR" 2>/dev/null || true
    fi
}
trap release_lock EXIT

acquire_lock() {
    if mkdir -- "$LOCK_DIR" 2>/dev/null; then
        LOCK_ACQUIRED=1
    else
        local owner_pid=""
        if [ -r "$LOCK_DIR/pid" ]; then
            owner_pid="$(sed -n '1p' "$LOCK_DIR/pid" 2>/dev/null || true)"
        fi

        # mkdir 锁可能因机器重启或进程被强杀而遗留；只清理格式正确且已死亡的 PID。
        if [[ "$owner_pid" =~ ^[0-9]+$ ]] && ! kill -0 "$owner_pid" 2>/dev/null; then
            rm -f -- "$LOCK_DIR/pid" "$LOCK_DIR/report_date"
            if rmdir -- "$LOCK_DIR" 2>/dev/null && mkdir -- "$LOCK_DIR" 2>/dev/null; then
                LOCK_ACQUIRED=1
                log "⚠️ 已清理失效的共享锁（原 PID ${owner_pid}）"
            fi
        fi
    fi

    if [ "$LOCK_ACQUIRED" -ne 1 ]; then
        log "⏳ 另一实例正在运行，未启动 $REPORT_DATE 管线"
        exit 75
    fi

    printf '%s\n' "$$" >"$LOCK_DIR/pid"
    printf '%s\n' "$REPORT_DATE" >"$LOCK_DIR/report_date"
}

require_nonempty_file() {
    local path="$1"
    if [ ! -s "$path" ]; then
        echo "❌ 缺少发布产物：$path" >&2
        return 1
    fi
}

manifest_has_status() {
    local expected="$1"
    "$PYTHON_BIN" "$MANIFEST_TOOL" check \
        --path "$MANIFEST_FILE" \
        --date "$REPORT_DATE" \
        --status "$expected" >/dev/null 2>&1
}

ready_artifacts_are_valid() {
    "$PYTHON_BIN" "$MANIFEST_TOOL" verify-ready \
        --path "$MANIFEST_FILE" \
        --date "$REPORT_DATE" >/dev/null 2>&1
}

acquire_lock

# 只有日期匹配的 published manifest 才能幂等跳过。archive count 不再代表成功。
if manifest_has_status published; then
    log "⏭️ $REPORT_DATE 已发布，跳过"
    exit 0
fi

# ready 表示 canonical 产物已经通过 QA。发布中途失败时从这里断点续发，
# 不重新抓取、改写或覆盖日报。
if manifest_has_status ready && ready_artifacts_are_valid; then
    log "▶️ $REPORT_DATE 已通过 QA，从 ready 状态继续发布"
else
    if manifest_has_status ready; then
        log "⚠️ ready 产物缺失、损坏或内容哈希不一致，禁止直接发布"
    fi
    if [ -z "${MINIMAX_API_KEY:-}" ]; then
        echo "❌ MINIMAX_API_KEY 未设置，无法执行强制排序与中文写作，已安全终止" >&2
        exit 78
    fi

    log "▶️ 生成 $REPORT_DATE 日报"
    "$PYTHON_BIN" "$MANIFEST_TOOL" mark-running \
        --path "$MANIFEST_FILE" \
        --date "$REPORT_DATE"

    if "$PYTHON_BIN" feed_v5.py --cache --date "$REPORT_DATE"; then
        :
    else
        rc=$?
        log "❌ 主生成失败（退出码 ${rc}），终止所有发布步骤"
        exit "$rc"
    fi

    if ! manifest_has_status ready; then
        log "❌ 主生成未产出日期匹配的 ready manifest，终止发布"
        exit 1
    fi
    if ! ready_artifacts_are_valid; then
        log "❌ 主生成的 ready 产物未通过内容哈希校验，终止发布"
        exit 1
    fi
fi

require_nonempty_file "$MD_FILE"
require_nonempty_file "$HTML_FILE"
require_nonempty_file "$ARCHIVE_FILE"

# feed_v5.py 已生成一次 HTML；这里不再重复调用 html_generator.py。
# 截图阶段显式移除 webhook，确保 GitHub 页面完成推送后才发送通知。
log "▶️ 生成移动端截图"
(
    unset FEISHU_WEBHOOK
    "$PYTHON_BIN" screenshot_and_push.py "$REPORT_DATE"
)
require_nonempty_file "$SCREENSHOT_FILE"
require_nonempty_file "$INDEX_FILE"

log "▶️ 推送网页产物"
publish_files=(
    "daily-ai-news-$REPORT_DATE.html"
    "daily-ai-news-$REPORT_DATE-mobile.png"
    "index.html"
)
"$GIT_BIN" add -- "${publish_files[0]}" "${publish_files[2]}"
"$GIT_BIN" add -f -- "${publish_files[1]}"

if "$GIT_BIN" diff --cached --quiet -- "${publish_files[@]}"; then
    log "ℹ️ 网页产物与当前版本一致，无需新建提交"
else
    "$GIT_BIN" commit -m "Update: $REPORT_DATE" -- "${publish_files[@]}"
fi
"$GIT_BIN" push

# 通知是可选集成：未配置凭据时明确跳过；一旦配置，发送失败必须阻断 published。
if [ -n "${FEISHU_WEBHOOK:-}" ]; then
    log "▶️ 发送飞书通知"
    "$PYTHON_BIN" pipeline_notify.py --date "$REPORT_DATE"
else
    log "ℹ️ 未设置 FEISHU_WEBHOOK，跳过飞书通知"
fi

"$PYTHON_BIN" "$MANIFEST_TOOL" mark-published \
    --path "$MANIFEST_FILE" \
    --date "$REPORT_DATE"

# Twitter 预览是日报的伴生产物：twitter_push.py 负责抓推文 → LLM 提炼 →
# 生成 twitter-preview-<date>.md → 推送重点卡片到飞书 → git push preview。
# 故意放在 mark-published 之后、且非阻断：twitter 抓取/推送失败不得回滚已发布的日报，
# 也不影响 feed_v5.py 读取的推文缓存刷新（见 8a2f762 "needed for cache refresh"）。
log "▶️ 生成 Twitter 预览并推送"
if ! "$PYTHON_BIN" twitter_push.py "$REPORT_DATE"; then
    log "⚠️ Twitter 预览生成/推送失败，不影响日报发布"
fi

log "✅ $REPORT_DATE 已发布"
