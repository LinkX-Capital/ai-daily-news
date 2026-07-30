#!/usr/bin/env bash
# launchd 兜底：仅 published manifest 代表当天日报已经完成。
# 并发控制统一由 run.sh 的共享锁负责，本脚本原样透传它的退出码。

set -Eeuo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${AI_DAILY_NEWS_DIR:-$SCRIPT_DIR}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
MANIFEST_TOOL="$PROJECT_DIR/pipeline_manifest.py"
MANIFEST_DIR="${MANIFEST_DIR:-$PROJECT_DIR/archive/manifests}"
RUN_SCRIPT="${AI_DAILY_RUN_SCRIPT:-$PROJECT_DIR/run.sh}"
HISTORY_LOG="${CATCHUP_HISTORY_LOG:-$PROJECT_DIR/logs/catchup-history.log}"

if [ "$#" -gt 1 ]; then
    echo "用法: $0 [YYYY-MM-DD]" >&2
    exit 64
fi

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
# 所有 cron/launchd/catch-up 入口共用同一把锁。
export PIPELINE_LOCK_DIR="${PIPELINE_LOCK_DIR:-/tmp/ai-daily-news.pipeline.lock}"

MANIFEST_FILE="$MANIFEST_DIR/$REPORT_DATE.json"
mkdir -p "$(dirname -- "$HISTORY_LOG")" "$MANIFEST_DIR"
cd "$PROJECT_DIR"

log_history() {
    printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" | tee -a "$HISTORY_LOG"
}

if "$PYTHON_BIN" "$MANIFEST_TOOL" check \
    --path "$MANIFEST_FILE" \
    --date "$REPORT_DATE" \
    --status published >/dev/null 2>&1; then
    log_history "⏭️ $REPORT_DATE 已发布，兜底无需运行"
    exit 0
fi

log_history "▶️ $REPORT_DATE 尚未发布，触发主管线"
if "$RUN_SCRIPT" "$REPORT_DATE"; then
    :
else
    rc=$?
    if [ "$rc" -eq 75 ]; then
        log_history "⏳ 主管线正在由另一实例执行，本次兜底延后（退出码 ${rc}）"
    else
        log_history "❌ 兜底主管线失败（退出码 ${rc}）"
    fi
    exit "$rc"
fi

# 防止下游脚本返回 0 却没有真正完成发布。
if ! "$PYTHON_BIN" "$MANIFEST_TOOL" check \
    --path "$MANIFEST_FILE" \
    --date "$REPORT_DATE" \
    --status published >/dev/null 2>&1; then
    log_history "❌ 主管线返回成功，但 published manifest 缺失或日期不匹配"
    exit 1
fi

log_history "✅ $REPORT_DATE 兜底发布完成"
