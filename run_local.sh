#!/bin/bash
# AI新闻管线 - 本地定时运行脚本

cd /Users/shenyalan/ai-daily-news

# 设置环境变量
export MINIMAX_API_KEY="${MINIMAX_API_KEY}"
export NOTIFY_METHOD="feishu"
export FEISHU_WEBHOOK="${FEISHU_WEBHOOK}"

echo "=========================================="
echo "🤖 AI前沿动态 - $(date '+%Y-%m-%d %H:%M')"
echo "=========================================="

# 运行抓取脚本 (v5.0 - 研究按领域+被引量排序)
python feed_v5.py

# 发送通知
if [ -f "notify.py" ]; then
    echo ""
    echo "📨 发送通知..."
    python notify.py
fi

echo ""
echo "✅ 完成! $(date '+%Y-%m-%d %H:%M:%S')"
