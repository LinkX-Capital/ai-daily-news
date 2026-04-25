#!/usr/bin/env python3
"""
自动补充 MD 条目的关键事实信息。

对 body 关键事实少的条目：
1. 从来源链接抓取原文
2. 用 LLM 重写 body，补充 benchmark/定价/数据等关键事实
3. 写回 MD 文件

用法：
  python enrich.py                    # 补充今天的日报
  python enrich.py 2026-04-24         # 补充指定日期
  python enrich.py --dry-run          # 只打印需要补充的条目，不修改
"""

import os
import re
import sys
import httpx
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from html_generator import parse_md

# ========== 配置 ==========
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
API_URL = "https://api.minimaxi.com/anthropic/v1/messages"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# body 最小字符数阈值（低于此值视为信息不足）
MIN_BODY_LEN = 120

# 关键事实信号词（有这些说明 body 不算太薄）
FACT_SIGNALS = [
    r'\d+\.?\d*%',     # 百分比
    r'\$[\d.]+[BMK]?',  # 美元金额
    r'\d+[BbMm万]$',    # 参数规模
    r'\d+[KM]上下文',   # 上下文长度
    r'Terminal-Bench|SWE-Bench|GPQA|MMLU|HumanEval',  # benchmark
]


def is_body_thin(body):
    """判断 body 是否信息量不足"""
    if not body or len(body) < MIN_BODY_LEN:
        return True
    # 如果包含关键事实信号，不算薄
    for pattern in FACT_SIGNALS:
        if re.search(pattern, body):
            return False
    # 超过 300 字符的 body 通常已经比较完整
    if len(body) > 300:
        return False
    return True


def fetch_source(url, timeout=10):
    """抓取来源页面文本"""
    if not url or not url.startswith('http'):
        return ""
    try:
        r = httpx.get(url, follow_redirects=True, timeout=timeout,
                      headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return ""
        text = r.text
        # 简单提取：去 HTML 标签，取前 3000 字符
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:3000]
    except Exception:
        return ""


def call_llm(system_prompt, user_prompt):
    """调用 MiniMax API（Anthropic 兼容格式）"""
    if not API_KEY:
        print("  WARNING: MINIMAX_API_KEY 未设置，跳过 LLM 补充")
        return None

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "MiniMax-M2.5",
        "max_tokens": 2000,
        "temperature": 0.2,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}]
    }

    try:
        r = httpx.post(API_URL, json=data, headers=headers, timeout=60)
        r.raise_for_status()
        resp = r.json()
        return resp["content"][0]["text"]
    except Exception as e:
        print(f"  LLM 调用失败: {e}")
        return None


def enrich_article(article):
    """对单条文章进行信息补充"""
    title = article.get("title", "")
    body = article.get("body", "")
    sources = article.get("sources", [])

    # 抓取来源原文
    source_texts = []
    for name, url in sources[:2]:  # 最多抓 2 个来源
        print(f"  抓取来源: {name}...")
        text = fetch_source(url)
        if text:
            source_texts.append(f"【来源: {name}】\n{text}")

    if not source_texts:
        print(f"  无法抓取来源，跳过")
        return None

    source_context = "\n\n".join(source_texts)

    system_prompt = """你是一个AI新闻分析师。任务：根据来源原文，补充新闻条目中缺失的关键事实。

## 核心原则：只补充事实，不做推断
- 只从来源原文中提取可验证的具体事实
- 禁止推测、猜测或延伸解读（如"可能意味着"、"或将引发"）
- 如果来源中没有某个信息，就不要写

## 应该补充的（原文中有的事实）
- 具体数字：benchmark分数、定价、参数量、融资金额、估值、员工数
- 关键技术细节：架构、方法名称、训练方式
- 关键时间点：发布日期、预计上线时间
- 关键人物/机构：具体谁做的、谁投资的
- 已确认的关联影响：原文明确提到的因果或竞争关系

## 不应该写的
- 对未来的预测或猜测
- 模糊的宏观判断（如"标志着新时代"、"行业洗牌"）
- 来源中没有提到的公司或技术
- 任何"可能"、"有望"、"或将"、"意味着"等推测性表述

## 格式
- 3-6句话，信息密度高，每句话都有一个可验证的事实
- 关键事实加粗（**...**）
- 海外公司/人名保持英文（OpenAI、Anthropic、NVIDIA等）
- 不用感叹号、不用媒体夸张口吻
- 输出纯文本，不要 markdown 格式（加粗除外）
- 只输出 body 内容，不要输出标题、key_points 或来源"""

    user_prompt = f"""## 当前标题
{title}

## 当前 body（信息不足，需补充）
{body}

## 来源原文
{source_context}

请输出补充后的 body："""

    result = call_llm(system_prompt, user_prompt)
    if result:
        # 清理可能的 markdown 包裹
        result = result.strip()
        if result.startswith("```"):
            result = re.sub(r'^```\w*\n?', '', result)
            result = re.sub(r'\n?```$', '', result)
        return result.strip()
    return None


def update_md_content(md_content, title, new_body):
    """在 MD 内容中替换指定条目的 body"""
    # 找到标题位置
    title_pattern = re.escape(f"**{title}**")
    match = re.search(title_pattern, md_content)
    if not match:
        return md_content

    # 从标题后开始，找到下一个 > 💡 或 📌 来源 或 **标题** 或 ## 分类
    start = match.end()
    # 跳过标题后的空行
    rest = md_content[start:]

    # body 区域：从标题后到第一个 insight/来源/下一个标题
    end_patterns = [
        r'\n> 💡',
        r'\n📌 来源',
        r'\n\*\*',
        r'\n## ',
    ]
    body_end = len(rest)
    for pat in end_patterns:
        m = re.search(pat, rest)
        if m and m.start() < body_end:
            body_end = m.start()

    old_body_section = rest[:body_end]
    new_body_section = f"\n\n{new_body}\n"

    return md_content[:start] + new_body_section + rest[body_end:]


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    if args:
        date_str = args[0]
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    md_file = os.path.join(BASE_DIR, f"daily-ai-news-{date_str}.md")
    if not os.path.exists(md_file):
        print(f"文件不存在: {md_file}")
        sys.exit(1)

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    articles, _ = parse_md(md_content)

    # 找出需要补充的条目
    thin_articles = []
    for a in articles:
        if is_body_thin(a.get("body", "")):
            thin_articles.append(a)

    if not thin_articles:
        print("所有条目信息量充足，无需补充。")
        return

    print(f"发现 {len(thin_articles)}/{len(articles)} 条信息不足的条目：")
    for a in thin_articles:
        body_len = len(a.get("body", ""))
        print(f"  - {a['title']} (body: {body_len}字)")

    if dry_run:
        print("\n[dry-run] 不修改文件。")
        return

    # 逐条补充
    enriched = 0
    for a in thin_articles:
        print(f"\n补充: {a['title']}")
        new_body = enrich_article(a)
        if new_body and len(new_body) > len(a.get("body", "")):
            md_content = update_md_content(md_content, a["title"], new_body)
            enriched += 1
            print(f"  OK body: {len(a.get('body', ''))}字 -> {len(new_body)}字")
        else:
            print(f"  SKIP 未获得更好的内容")

    if enriched > 0:
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"\n已补充 {enriched} 条，保存到 {md_file}")
    else:
        print("\n未能补充任何条目。")


if __name__ == "__main__":
    main()
