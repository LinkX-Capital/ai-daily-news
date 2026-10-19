#!/usr/bin/env bash
# 手动一键运行（桌面快捷方式调用）：和定时任务走同一条流程，但把进度显示在窗口里。
# 当天已发布时只会提示并退出，不会重复发布。

set -Euo pipefail

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
mkdir -p logs

if [ -r .env ]; then
    set -a
    # shellcheck disable=SC1091
    source .env
    set +a
fi

echo "=============================================="
echo "  AI 前沿动态日报 · 手动运行"
echo "  $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================================="
echo

bash catchup.sh "$@" 2>&1 | tee -a logs/catchup.log
rc=${PIPESTATUS[0]}

echo
echo "=============================================="
case "$rc" in
    0)  echo "  ✅ 完成：今天的日报已发布"
        echo "  网站：https://linkxcapital.github.io/ai-daily-news/" ;;
    75) echo "  ⏳ 已有另一个实例在运行（可能是定时任务），稍后再试" ;;
    78) echo "  ❌ 缺少配置（检查 .env 里的 key）" ;;
    *)  echo "  ❌ 失败（退出码 $rc），上面的输出和 logs/catchup.log 里有原因" ;;
esac
echo "=============================================="
echo
read -r -p "按回车键关闭窗口..." _ || true
exit "$rc"
