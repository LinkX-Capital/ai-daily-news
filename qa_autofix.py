#!/usr/bin/env python3
"""
QA Autofix: 对 short_body 条目自动抓取原文并用 LLM 补充 body
在 qa.py 检测到问题后调用，复用 qa.py 的抓取能力

用法：
  python qa_autofix.py 2026-05-08
"""

import os
import re
import sys
import json
import httpx

sys.path.insert(0, os.path.dirname(__file__))
from html_generator import parse_md
from qa import fetch_source_content, search_alternative_sources, MCPWebReader

API_KEY = os.environ.get("MINIMAX_API_KEY", "")
API_URL = "https://api.minimaxi.com/anthropic/v1/messages"


def _count_sentences(text):
    if not text:
        return 0
    sentences = re.split(r'[。.!?！？]', text)
    return len([s for s in sentences if s.strip()])


def _search_arxiv(query):
    """用 arXiv API 按关键词搜索论文"""
    try:
        import urllib.request, urllib.parse
        en_words = re.findall(r'[A-Za-z][\w-]*(?:\s+[A-Za-z][\w-]*)*', query)
        search_q = ' '.join(en_words)[:100] if en_words else query[:50]
        if not search_q or len(search_q) < 3:
            return None
        encoded = urllib.parse.quote(search_q)
        url = f"http://export.arxiv.org/api/query?search_query=all:{encoded}&max_results=3&sortBy=submittedDate&sortOrder=descending"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml = resp.read().decode("utf-8")
        # 解析结果
        ids = re.findall(r'<id>http://arxiv.org/abs/(\d{4}\.\d{4,5})', xml)
        abstracts = re.findall(r'<summary>(.*?)</summary>', xml, re.DOTALL)
        if ids and abstracts:
            abstract = re.sub(r'\s+', ' ', abstracts[0]).strip()[:1200]
            return {"arxiv_id": ids[0], "abstract": abstract}
    except Exception:
        pass
    return None


def _fetch_arxiv_abstract(arxiv_id):
    """从 arXiv 获取论文 abstract"""
    try:
        import urllib.request
        url = f"https://arxiv.org/abs/{arxiv_id}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8")
        abstract = re.findall(
            r'<blockquote class="abstract mathjax">\s*<span class="descriptor">Abstract:</span>\s*(.*?)</blockquote>',
            html, re.DOTALL)
        if abstract:
            text = re.sub(r'<[^>]*>', '', abstract[0]).strip()
            return re.sub(r'\s+', ' ', text)[:1200]
    except Exception:
        pass
    return None


def _find_arxiv_id(link, body, title):
    """从文章字段中提取 arXiv 编号"""
    for field in [link, body, title]:
        if not field:
            continue
        m = re.search(r'(\d{4}\.\d{4,5})', field)
        if m:
            return m.group(1)
    return None


def _get_source_text(title, link, category):
    """获取原文内容，按优先级尝试多种方式。返回 (content, source_url) 元组"""
    # 1. arXiv 溯源（研究类优先）
    arxiv_id = _find_arxiv_id(link, "", title)

    if not arxiv_id and category in ["研究关注", "模型前沿"]:
        # 主动搜索 arXiv
        result = _search_arxiv(title)
        if result:
            print(f"      🔍 arXiv搜索命中: {result['arxiv_id']}")
            return result["abstract"], f"https://arxiv.org/abs/{result['arxiv_id']}"

    if arxiv_id:
        abstract = _fetch_arxiv_abstract(arxiv_id)
        if abstract and len(abstract) > 100:
            print(f"      📄 arXiv abstract: {arxiv_id}")
            return abstract, f"https://arxiv.org/abs/{arxiv_id}"

    # 2. 直接抓取链接
    if link:
        links = re.findall(r'https?://[^\s|)]+', link)
        if not links:
            links = [link]

        mcp_reader = MCPWebReader()
        for l in links:
            if "mp.weixin.qq.com" in l:
                continue
            # MCP 优先
            content = mcp_reader.fetch(l)
            if content and len(content) > 200:
                print(f"      🌐 MCP抓取成功: {l[:50]}")
                return content[:3000], None  # 原有链接，不需要追加
            # httpx 回退
            content = fetch_source_content(l)
            if content and len(content) > 200:
                print(f"      🌐 httpx抓取成功: {l[:50]}")
                return content[:3000], None

    # 3. Web search 替代来源
    print(f"      🔍 搜索替代来源...")
    content = search_alternative_sources(title)
    if content and len(content) > 200:
        return content[:3000], None

    return None, None


def _enrich_body_with_llm(title, current_body, source_text, category):
    """用 LLM 基于原文重写 body"""
    if not API_KEY:
        return None

    cat_hint = {
        "研究关注": "方法创新点、实验结果数据、与现有方法对比",
        "模型前沿": "能力突破点、关键benchmark数据、成本/速度",
        "算力追踪": "规模数据、产能、成本变化",
        "产业动态": "具体事件、涉及人/产品、影响范围",
        "初创&融资": "金额、投资方、商业逻辑",
        "X讨论": "观点核心、论据、具体数据",
    }.get(category, "关键事实和数据")

    prompt = f"""基于原文补充这条新闻的body。

## 当前标题
{title}

## 当前body（信息不足，需要补充）
{current_body}

## 原文内容
{source_text[:2500]}

## 要求
- 保留当前body中已有的有价值信息（事实、数据、人名等），在此基础上补充
- 最终输出3-5句话的中文body，只写关键事实
- 重点补充：{cat_hint}
- 关键数据加粗（用**包裹）
- 禁止AI判断/引申，只写原文支撑的事实
- 海外公司/人名保持英文
- 直接输出body文本，不要任何前缀说明"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "MiniMax-M2.5", "temperature": 0.1,
        "max_tokens": 500,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        r = httpx.post(API_URL, headers=headers, json=data, timeout=30, verify=False)
        if r.status_code == 200:
            result = r.json()
            if result.get("content"):
                for item in result["content"]:
                    if item.get("type") == "text":
                        text = item.get("text", "").strip()
                        if len(text) > 50 and not text.startswith("抱歉"):
                            return text[:400]
    except Exception as e:
        print(f"      ⚠️ LLM调用失败: {e}")
    return None


def autofix_short_body(date_str):
    """读取 md，找到 short_body 条目，抓原文补充，回写 md"""
    base = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(base, f"daily-ai-news-{date_str}.md")

    if not os.path.exists(md_path):
        print(f"   文件不存在: {md_path}")
        return 0

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    articles, _ = parse_md(md_content)
    fixed_count = 0

    for a in articles:
        title = a.get("title", "")
        body = a.get("body", "")
        sent_count = _count_sentences(body)

        if sent_count >= 3:
            continue

        # 获取分类
        category = a.get("categories", [""])[0] if a.get("categories") else ""
        link = a.get("link", "")

        print(f"   [{title[:35]}...] body仅{sent_count}句，尝试补充...")

        # 抓取原文
        source_text, new_source_url = _get_source_text(title, link, category)
        if not source_text:
            print(f"      ❌ 无法获取原文")
            continue

        # LLM 补充
        new_body = _enrich_body_with_llm(title, body, source_text, category)
        if not new_body:
            print(f"      ❌ LLM补充失败")
            continue

        # 回写 md：替换原 body
        # md 格式: "- {body}" 在 "**{title}**" 之后
        # 用正则定位并替换
        escaped_title = re.escape(title)
        pattern = rf'(\*\*{escaped_title}\*\*\n)- .+?(\n  > 💡)'
        replacement = rf'\g<1>- {new_body}\g<2>'
        new_md, count = re.subn(pattern, replacement, md_content, count=1, flags=re.DOTALL)

        if count > 0:
            md_content = new_md
            # 追加新来源链接（不替换原有链接）
            if new_source_url:
                source_pattern = rf'(\*\*{escaped_title}\*\*.*?- 来源: .+?)(\n)'
                source_match = re.search(source_pattern, md_content, re.DOTALL)
                if source_match:
                    existing_line = source_match.group(1)
                    # 避免重复追加
                    if new_source_url not in existing_line:
                        domain = "arXiv" if "arxiv.org" in new_source_url else "补充来源"
                        appended = f"{existing_line} | [{domain}]({new_source_url}){source_match.group(2)}"
                        md_content = md_content[:source_match.start()] + appended + md_content[source_match.end():]
                        print(f"      📎 追加来源: {new_source_url[:50]}")
            fixed_count += 1
            print(f"      ✅ 已补充")
        else:
            print(f"      ⚠️ md替换失败（格式不匹配）")

    # 回写文件
    if fixed_count > 0:
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"\n   📝 已回写 {md_path}，补充了 {fixed_count} 条")

    return fixed_count


if __name__ == "__main__":
    date_str = sys.argv[1] if len(sys.argv) > 1 else None
    if not date_str:
        from datetime import datetime
        date_str = datetime.now().strftime("%Y-%m-%d")
    print(f"=== QA Autofix: {date_str} ===\n")
    fixed = autofix_short_body(date_str)
    print(f"\n完成: 补充了 {fixed} 条")
