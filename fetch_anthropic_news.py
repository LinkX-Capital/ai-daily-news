#!/usr/bin/env python3
"""抓取 Anthropic 官方新闻"""

from playwright.sync_api import sync_playwright
import json
from datetime import datetime, timezone
import re

ANTHROPIC_NEWS_URL = "https://www.anthropic.com/news"

def fetch_anthropic_news():
    """抓取 Anthropic 新闻"""
    articles = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print("  🌐 正在抓取 Anthropic News...")
            page.goto(ANTHROPIC_NEWS_URL, wait_until="networkidle", timeout=20000)
            page.wait_for_timeout(2000)

            # 获取新闻链接
            links = page.query_selector_all('a[href*="/news/"]')

            seen_titles = set()
            for link in links:
                try:
                    href = link.get_attribute('href')
                    if not href or href == '/news':
                        continue

                    text = link.inner_text().strip()

                    # 提取标题：取第一行或包含内容的行
                    lines = text.split('\n')
                    title = None
                    for line in lines:
                        line = line.strip()
                        # 跳过纯日期或纯分类
                        if re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+', line):
                            continue
                        if line in ['Announcements', 'Product', 'Policy']:
                            continue
                        if line:
                            title = line[:80]
                            break

                    if not title or title in seen_titles:
                        continue
                    seen_titles.add(title)

                    # 提取日期 - 使用 search 获取完整匹配
                    date_pattern = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}'
                    m = re.search(date_pattern, text)
                    if m:
                        from dateutil import parser
                        try:
                            pub_date = parser.parse(m.group())
                        except:
                            pub_date = datetime.now(timezone.utc)
                    else:
                        pub_date = datetime.now(timezone.utc)

                    # 清理摘要 - 移除日期和分类标签
                    clean_summary = text
                    # 移除日期
                    clean_summary = re.sub(r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+,\s+\d{4}', '', clean_summary)
                    # 移除分类标签
                    for tag in ['Announcements', 'Product', 'Policy']:
                        clean_summary = clean_summary.replace(tag, '')
                    clean_summary = ' '.join(clean_summary.split()).strip()[:200]

                    if title and len(title) > 5:
                        articles.append({
                            "title": title,
                            "link": "https://www.anthropic.com" + href if href.startswith('/') else href,
                            "summary": clean_summary,
                            "published": pub_date.isoformat(),
                            "published_parsed": pub_date.timetuple(),
                            "source": "Anthropic",
                        })
                except:
                    continue

            print(f"     ✅ 获取 {len(articles)} 条 Anthropic 新闻")

        except Exception as e:
            print(f"     ❌ 抓取失败: {e}")
        finally:
            browser.close()

    return articles


if __name__ == "__main__":
    articles = fetch_anthropic_news()
    print(f"\n共抓取 {len(articles)} 条")

    # 保存
    with open('/Users/shenyalan/ai-daily-news/anthropic_news.json', 'w') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print("已保存到 anthropic_news.json")
