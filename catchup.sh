#!/bin/bash
# launchd 兜底：检查今天日报 archive 是否已生成，没有就跑主管线
# 设计：cron 6:40 是主力；本脚本由 launchd 在多个时间点 + 开机/唤醒后触发，
#       只要当天某一次 catch-up 时 archive 还缺，就自动补跑。
cd /Users/shenyalan/ai-daily-news || exit 1

# mkdir 原子锁，防 cron 与 launchd / 多次触发并发
LOCKDIR=/tmp/ai-daily-news.catchup.lock
mkdir "$LOCKDIR" 2>/dev/null || { echo "$(date): 已有实例在跑，跳过" ; exit 0; }
trap 'rmdir "$LOCKDIR" 2>/dev/null' EXIT

DATE=$(date +%Y-%m-%d)
ARCHIVE="archive/news_${DATE}.json"
HISTORY_LOG=logs/catchup-history.log

mkdir -p logs

if [ -f "$ARCHIVE" ]; then
    COUNT=$(python3 -c "import json;d=json.load(open('$ARCHIVE'));print(d.get('count',len(d.get('articles',[]))))" 2>/dev/null || echo "0")
    if [ "$COUNT" -gt 0 ] 2>/dev/null; then
        echo "$(date): 今日($DATE) archive 已存在($COUNT 条)，跳过兜底" | tee -a "$HISTORY_LOG"
        exit 0
    fi
fi

echo "$(date): 今日($DATE) archive 缺失，兜底触发主管线" | tee -a "$HISTORY_LOG"
bash run.sh
echo "$(date): 兜底主管线完成" | tee -a "$HISTORY_LOG"
