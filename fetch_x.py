#!/usr/bin/env python3
"""抓取 X/Twitter 用户推文 - 使用 Nitter RSS"""

import feedparser
import json
from datetime import datetime

# Nitter RSS 源
NITTER_RSS = "https://nitter.net/AnthropicAI/rss"

def fetch_x_tweets(username="AnthropicAI", count=10):
    """通过 Nitter RSS 抓取 X 用户推文"""
    tweets = []

    try:
        print(f"  🌐 正在抓取 @{username} via Nitter RSS...")

        # 尝试多个 Nitter 实例
        nitter_instances = [
            f"https://nitter.net/{username}/rss",
            f"https://nitter.privacydev.net/{username}/rss",
            f"https://nitter.poast.org/{username}/rss",
        ]

        for rss_url in nitter_instances:
            try:
                feed = feedparser.parse(rss_url)
                if feed.entries:
                    print(f"     使用: {rss_url}")
                    break
            except:
                continue

        if not feed.entries:
            print(f"     ⚠️ 无法获取 RSS")
            return []

        for entry in feed.entries[:count]:
            title = entry.get("title", "")

            # 过滤转推和太短的推文
            if title and len(title) > 30 and not title.startswith("RT @"):
                tweets.append({
                    "title": title[:100] + "..." if len(title) > 100 else title,
                    "link": entry.get("link", ""),
                    "summary": title,
                    "published": entry.get("published", ""),
                    "source": f"@{username}"
                })

        print(f"     ✅ 获取 {len(tweets)} 条推文")

    except Exception as e:
        print(f"     ❌ 抓取失败: {e}")

    return tweets


def main():
    tweets = fetch_x_tweets("AnthropicAI", 10)

    # 保存
    with open('/Users/shenyalan/ai-daily-news/x_tweets.json', 'w') as f:
        json.dump(tweets, f, ensure_ascii=False, indent=2)

    return tweets


if __name__ == "__main__":
    main()
