#!/bin/bash
# AI Daily News - 交互审核工作台启动脚本

cd /Users/shenyalan/ai-daily-news

# 检查 Streamlit 是否安装
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit 未安装，正在安装..."
    pip install streamlit
fi

# 启动 Streamlit
echo "🚀 启动 AI Daily News 审核工作台..."
echo "📱 浏览器访问: http://localhost:8501"
echo "⏹  按 Ctrl+C 停止"
echo ""

streamlit run review_dashboard.py --server.port 8501 --server.address localhost
