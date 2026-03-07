#!/usr/bin/env python3
"""AI 前沿动态 - 内容质量改进工具"""

import httpx
import os

# 配置
API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")
if not API_KEY:
    print("❌ 错误: 未设置 ANTHROPIC_AUTH_TOKEN 环境变量")
    exit(1)

API_URL = "https://api.minimaxi.com/anthropic/v1/messages"
INPUT_FILE = "/Users/shenyalan/ai-daily-news/daily-ai-news.md"
OUTPUT_FILE = "/Users/shenyalan/ai-daily-news/daily-ai-news-improved.md"

SYSTEM_PROMPT = """你是一位资深AI行业研究员，负责改进AI新闻日报的内容质量。

## 任务
改进 /Users/shenyalan/ai-daily-news/daily-ai-news.md 的内容

## 格式要求
直接输出Markdown内容，不要有任何分析、说明、注释。

## 内容质量标准
- 每条新闻：标题、1句话摘要、2-3句话正文
- 关键数据用中文加粗：$110B→**1100亿美元**，50x→**50倍**
- 删除无实质内容条目（图片描述、空话）
- 删除低价值新闻

## 输出
直接输出完整Markdown文件内容。"""


def call_api(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "MiniMax-M2.5",
        "max_tokens": 8000,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        r = httpx.post(API_URL, headers=headers, json=data, timeout=120, verify=False)
        r.raise_for_status()
        result = r.json()
        # Claude API 返回 content 是数组，找到 text 类型的元素
        if result.get("content"):
            for item in result["content"]:
                if item.get("type") == "text":
                    return item.get("text", "")
        return ""
    except Exception as e:
        print(f"❌ API调用失败: {e}")
        return None


def clean_output(text):
    """清理输出，移除分析内容"""
    lines = text.split('\n')

    # 找到第一个 ## 标题行
    start_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('## 20') or line.strip().startswith('## 03'):
            start_idx = i
            break

    if start_idx >= 0:
        text = '\n'.join(lines[start_idx:])

    # 移除可能的引号包裹
    text = text.strip()
    if text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    text = text.strip()

    return text


def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ 找不到 {INPUT_FILE}，请先运行 python feed.py")
        return

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    print(f"📖 读取原始日报: {len(content)} 字符")

    prompt = f"改进以下AI日报：\n\n{content}"
    result = call_api(prompt)

    if result:
        result = clean_output(result)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(result)

        print(f"✅ 已输出: {OUTPUT_FILE}")
        print(f"   改进后: {len(result)} 字符")
    else:
        print("❌ 改进失败")


if __name__ == "__main__": main()
