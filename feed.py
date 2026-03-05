#!/usr/bin/env python3
"""
AI Daily News - RSS Aggregator
每天自动抓取AI前沿动态，输出为Markdown
"""

import feedparser
import httpx
from datetime import datetime
from collections import defaultdict
import re
import os

# RSS 订阅源列表
RSS_SOURCES = {
    # 国际大厂
    "Google AI": "https://blog.google/technology/google-deepmind/rss/",
    "OpenAI": "https://openai.com/news/rss.xml",
    "NVIDIA": "https://blogs.nvidia.com/feed/",
    "Microsoft Research": "https://www.microsoft.com/en-us/research/feed/",

    # AI 研究 & 博客
    "Karpathy": "https://karpathy.bearblog.dev/feed/",
    "Lilian Weng": "https://lilianweng.github.io/index.xml",
    "The Latent Space": "https://www.latent.space/feed",
    "Thinking Machines": "https://thinkingmachines.ai/blog/index.xml",
    "Sakana AI": "https://sakana.ai/feed.xml",

    # 科技媒体
    "TechCrunch": "https://techcrunch.com/feed/",
    "The Information": "https://www.theinformation.com/feed",
    "Crunchbase News": "https://news.crunchbase.com/feed/",

    # 开发者社区
    "Hacker News": "https://news.ycombinator.com/rss",
    "Y Combinator Blog": "https://www.ycombinator.com/blog/feed",

    # 中文源
    "QbitAI": "https://www.qbitai.com/feed",
    "36氪": "http://36kr.com/feed",
    "微信读书(AI)": "https://raw.githubusercontent.com/osnsyc/Wechat-Scholar/main/channels/gh_dbc0a5474692.xml",
    "机器之心": "https://wechat2rss.xlab.app/feed/ede30346413ea70dbef5d485ea5cbb95cca446e7.xml",
    "AI寒舍": "https://wechat2rss.xlab.app/feed/3be891c2f4e526629ab055a297cc2cd6c1f0a563.xml",
}

# 输出文件路径
OUTPUT_FILE = os.environ.get("OUTPUT_FILE", "daily-ai-news.md")


def clean_text(text: str) -> str:
    """清理HTML标签和多余空白"""
    # 移除HTML标签
    text = re.sub(r'<[^>]+>', '', text)
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def normalize_title(title: str) -> str:
    """标准化标题用于去重比较"""
    # 转小写，移除标点和空格
    title = title.lower().strip()
    title = re.sub(r'[^\w\s]', '', title)
    title = re.sub(r'\s+', '', title)
    return title


def fetch_feed(source_name: str, url: str, limit: int = 10):
    """抓取单个RSS源"""
    try:
        # 使用 User-Agent 避免被拦截
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = httpx.get(url, headers=headers, timeout=15, follow_redirects=True)
        response.raise_for_status()

        feed = feedparser.parse(response.text)

        articles = []
        for entry in feed.entries[:limit]:
            title = clean_text(entry.get("title", ""))
            link = entry.get("link", "")

            # 尝试获取摘要
            summary = ""
            if hasattr(entry, "summary"):
                summary = clean_text(entry.summary)
            elif hasattr(entry, "description"):
                summary = clean_text(entry.description)

            # 截断过长的摘要
            if len(summary) > 300:
                summary = summary[:300] + "..."

            articles.append({
                "title": title,
                "link": link,
                "summary": summary,
                "source": source_name
            })

        return articles, None
    except Exception as e:
        return [], f"{source_name}: {str(e)}"


def remove_duplicates(articles: list) -> list:
    """基于标题相似度去重"""
    seen = {}
    unique_articles = []

    for article in articles:
        normalized = normalize_title(article["title"])

        # 检查是否已存在相似标题
        is_duplicate = False
        for existing_normalized in seen:
            # 简单相似度检查：如果normalized是existing的子串或反之
            if normalized in existing_normalized or existing_normalized in normalized:
                is_duplicate = True
                break

        if not is_duplicate:
            seen[normalized] = True
            unique_articles.append(article)

    return unique_articles


def generate_markdown(articles: list) -> str:
    """生成Markdown格式输出"""
    today = datetime.now().strftime("%Y-%m-%d")

    md_lines = [
        f"# AI前沿动态 · {today}",
        "",
        f"> 自动汇总 · 来源: {len(RSS_SOURCES)} 个RSS源",
        "",
        "---",
        ""
    ]

    # 按来源分组
    by_source = defaultdict(list)
    for article in articles:
        by_source[article["source"]].append(article)

    # 输出
    for source, source_articles in sorted(by_source.items()):
        md_lines.append(f"## {source}")
        md_lines.append("")

        for article in source_articles:
            if article["link"]:
                md_lines.append(f"- [{article['title']}]({article['link']})")
            else:
                md_lines.append(f"- {article['title']}")

            if article["summary"]:
                md_lines.append(f"  - {article['summary']}")

        md_lines.append("")

    # 统计信息
    md_lines.extend([
        "---",
        "",
        f"**统计**: 共 {len(articles)} 条内容",
        "",
        f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    ])

    return "\n".join(md_lines)


def main():
    """主函数"""
    print(f"🤖 开始抓取AI资讯... ({len(RSS_SOURCES)} 个源)")

    all_articles = []
    errors = []

    # 抓取所有源
    for source_name, url in RSS_SOURCES.items():
        print(f"  📡 抓取: {source_name}...", end=" ")
        articles, error = fetch_feed(source_name, url)

        if error:
            print(f"❌ {error}")
            errors.append(error)
        else:
            print(f"✅ {len(articles)} 条")
            all_articles.extend(articles)

    # 去重
    unique_articles = remove_duplicates(all_articles)
    print(f"\n📊 抓取: {len(all_articles)} 条 → 去重后: {len(unique_articles)} 条")

    # 生成Markdown
    markdown = generate_markdown(unique_articles)

    # 写入文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"✅ 已输出到: {OUTPUT_FILE}")

    if errors:
        print(f"\n⚠️ 部分源抓取失败:")
        for e in errors:
            print(f"  - {e}")

    return len(unique_articles)


if __name__ == "__main__":
    main()
