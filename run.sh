#!/bin/bash
# AI 前沿动态 - 定时运行脚本（每天8:00）

cd /Users/shenyalan/ai-daily-news

# 如果当天 archive 已存在，跳过管线
DATE_STR=$(date +%Y-%m-%d)
if [ -f "archive/news_${DATE_STR}.json" ]; then
    echo "⏭️ 当天 archive 已存在 (${DATE_STR})，跳过管线: $(date)"
    exit 0
fi

# 加载环境变量
source ~/.zshrc

# 飞书通知
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/362a7cc7-5bce-4184-9ae3-7d6b6c0c429a"

# 1. 抓取 + LLM处理 → 生成 md + archive
python3 feed_v5.py --cache

# 2. 从 md 生成 HTML（含 dated HTML + index.html）
python3 html_generator.py

# 3. 生成手机端截图
python3 gen_screenshot.py

# 4. 发送飞书通知
python3 notify.py

# 5. Git push HTML 文件到 GitHub
git add daily-ai-news.html daily-ai-news-${DATE_STR}.html index.html daily-ai-news-mobile.png
git diff --cached --quiet || git commit -m "Update: ${DATE_STR}" && git push

echo "✅ 任务完成: $(date)"
