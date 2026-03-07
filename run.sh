#!/bin/bash
# AI 前沿动态 - 定时运行脚本

cd /Users/shenyalan/ai-daily-news

# 飞书通知
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/362a7cc7-5bce-4184-9ae3-7d6b6c0c429a"

# 1. 抓取内容
python feed_v5.py

# 2. 生成HTML
python generate_html.py

# 3. 发送通知
python notify.py

echo "✅ 任务完成: $(date)"
