#!/bin/bash
# Twitter 动态推送 - 每天早上7:15

cd /Users/shenyalan/ai-daily-news

# 加载环境变量（proxy等）
source ~/.zshrc

# 运行推送脚本
python3 twitter_push.py

echo "✅ Twitter 推送完成: $(date)"
