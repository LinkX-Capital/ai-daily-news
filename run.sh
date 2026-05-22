#!/bin/bash
# AI 前沿动态 - 定时运行脚本（每天6:00）

cd /Users/shenyalan/ai-daily-news

# 如果当天 archive 已存在且内容非空，跳过管线
DATE_STR=$(date +%Y-%m-%d)
ARCHIVE_FILE="archive/news_${DATE_STR}.json"
if [ -f "$ARCHIVE_FILE" ]; then
    ARTICLE_COUNT=$(python3 -c "import json; d=json.load(open('$ARCHIVE_FILE')); print(d.get('count', len(d.get('articles', []))))" 2>/dev/null || echo "0")
    if [ "$ARTICLE_COUNT" -gt 0 ] 2>/dev/null; then
        echo "⏭️ 当天 archive 已存在 (${DATE_STR}, ${ARTICLE_COUNT} 条)，跳过管线: $(date)"
        exit 0
    else
        echo "⚠️ 当天 archive 存在但为空 (${DATE_STR})，重新运行管线"
        rm "$ARCHIVE_FILE"
    fi
fi

# 加载环境变量
source ~/.zshrc

# 飞书通知
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/362a7cc7-5bce-4184-9ae3-7d6b6c0c429a"

# 0. 先抓取 Twitter，刷新缓存
python3 twitter_push.py

# 1. 抓取 + LLM处理 → 生成 md + archive
python3 feed_v5.py --cache

# 2. 从 md 生成 HTML（含 dated HTML + index.html）
python3 html_generator.py

# 3. 生成手机端截图
python3 gen_screenshot.py

# 4. 发送飞书通知
python3 notify.py

# 5. Git push HTML 文件到 GitHub
git add daily-ai-news-${DATE_STR}.html index.html daily-ai-news-mobile.png
git diff --cached --quiet || git commit -m "Update: ${DATE_STR}" && git push

echo "✅ 任务完成: $(date)"
