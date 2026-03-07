#!/usr/bin/env python3
"""抓取 Anthropic 新闻页面的脚本"""

from playwright.sync_api import sync_playwright
import json
from datetime import datetime, timezone, timedelta
import re

def fetch_anthropic_news():
    """抓取 Anthropic News 页面"""
    anthropic_articles = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print("  🌐 正在抓取 Anthropic News...")
            page.goto("https://www.anthropic.com/news", wait_until="networkidle", timeout=30000)

            # 等待页面加载
            page.wait_for_timeout(3000)

            # 获取文章列表
            # Anthropic News 页面结构
            articles = page.query_selector_all('article, [class*="news"], [class*="card"]')

            print(f"     找到 {len(articles)} 个元素")

            # 尝试不同的选择器
            news_items = page.query_selector_all('a[href*="/news/"]')

            for item in news_items[:10]:  # 最多取10条
                try:
                    # 获取链接和标题
                    href = item.get_attribute('href')
                    title_elem = item.query_selector('h1, h2, h3, [class*="title"]')

                    if not href or '/news/' not in href:
                        continue

                    title = title_elem.inner_text() if title_elem else ""

                    # 获取摘要
                    desc_elem = item.query_selector('p, [class*="description"], [class*="summary"]')
                    summary = desc_elem.inner_text() if desc_elem else ""

                    # 获取日期
                    time_elem = item.query_selector('time')
                    date_str = time_elem.get_attribute('datetime') if time_elem else ""

                    if title and len(title) > 10:
                        anthropic_articles.append({
                            "title": title.strip(),
                            "link": "https://www.anthropic.com" + href if href.startswith('/') else href,
                            "summary": summary.strip()[:200] if summary else "",
                            "published": date_str,
                            "source": "Anthropic"
                        })
                except Exception as e:
                    continue

            # 如果上述方法失败，尝试直接获取所有链接
            if not anthropic_articles:
                all_links = page.query_selector_all('a[href]')
                for link in all_links:
                    try:
                        href = link.get_attribute('href') or ""
                        if '/news/' in href and href != '/news':
                            text = link.inner_text().strip()
                            if text and len(text) > 20:
                                anthropic_articles.append({
                                    "title": text[:100],
                                    "link": "https://www.anthropic.com" + href if href.startswith('/') else href,
                                    "summary": "",
                                    "published": "",
                                    "source": "Anthropic"
                                })
                    except:
                        continue

            # 去重
            seen = set()
            unique_articles = []
            for a in anthropic_articles:
                if a['link'] not in seen:
                    seen.add(a['link'])
                    unique_articles.append(a)

            anthropic_articles = unique_articles[:10]

        except Exception as e:
            print(f"     ❌ 抓取失败: {e}")
        finally:
            browser.close()

    return anthropic_articles


def main():
    articles = fetch_anthropic_news()
    print(f"  ✅ 抓取到 {len(articles)} 条 Anthropic 新闻")

    # 保存到文件供主程序使用
    with open('/Users/shenyalan/ai-daily-news/anthropic_news.json', 'w') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    return articles


if __name__ == "__main__":
    main()
