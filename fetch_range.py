#!/usr/bin/env python3
"""Twitter 动态抓取 - 指定日期范围"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict, Counter

sys.path.insert(0, str(Path(__file__).parent))

import httpx
import feedparser
import yaml
from email.utils import parsedate_to_datetime

# ============ 配置加载 ============
CONFIG_FILE = Path(__file__).parent / "accounts.yaml"
CACHE_FILE = Path(__file__).parent / "tweet_fetcher" / "cache.json"
TIMEOUT = 15

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/rss+xml, application/xml, text/xml',
}

NITTER_INSTANCES = [
    "https://nitter.net",
    "https://nitter.poast.org",
    "https://nitter.privacydev.net",
    "https://nitter.hu",
]


def load_config() -> dict:
    if CONFIG_FILE.exists():
        return yaml.safe_load(CONFIG_FILE.read_text())
    return {}


def get_accounts():
    config = load_config()
    accounts = config.get("accounts", [])
    settings = config.get("settings", {})

    account_groups = {"Company": [], "Researcher": []}
    account_info = {}
    seen = set()

    for acc in accounts:
        handle = acc.get("handle", "").lower()
        if not handle or handle in seen:
            continue
        seen.add(handle)

        category = acc.get("category", "other")
        if category not in account_groups:
            account_groups[category] = []
        account_groups[category].append(handle)

        account_info[handle] = {
            "category": category,
            "track": acc.get("track", ""),
            "org": acc.get("org", ""),
        }

    all_handles = list(seen)
    return account_groups, account_info, all_handles


X_ACCOUNT_GROUPS, X_ACCOUNT_INFO, ALL_ACCOUNTS = get_accounts()


def get_available_instance():
    for instance in NITTER_INSTANCES:
        try:
            client = httpx.Client(timeout=5.0, headers=HEADERS)
            resp = client.get(f"{instance}/OpenAI/rss")
            if resp.status_code == 200 and len(resp.text) > 100:
                return instance
        except:
            continue
    return None


def is_in_range(published: str, start_date: datetime, end_date: datetime) -> bool:
    """检查推文是否在指定日期范围内"""
    try:
        pub_date = parsedate_to_datetime(published)
        # 统一为UTC时间比较
        pub_date_utc = pub_date.astimezone(timezone.utc)
        return start_date <= pub_date_utc <= end_date
    except:
        return False


def fetch_user_tweets_range(username: str, instance: str, start_date: datetime, end_date: datetime, count: int = 20) -> list:
    tweets = []
    url = f"{instance}/{username}/rss"

    try:
        client = httpx.Client(timeout=TIMEOUT, headers=HEADERS)
        resp = client.get(url)
        if resp.status_code != 200:
            return []

        feed = feedparser.parse(resp.text)
        if feed.entries:
            for entry in feed.entries[:count]:
                title = entry.get("title", "")
                published = entry.get("published", "")

                if not is_in_range(published, start_date, end_date):
                    continue

                is_retweet = title.startswith("RT ")
                is_reply = title.startswith("R to @")

                if is_retweet:
                    content = title.split(": ", 1)[1] if ": " in title else title[3:]
                elif is_reply:
                    content = title.split(": ", 1)[1] if ": " in title else title[4:]
                else:
                    content = title

                if len(content.strip()) < 30:
                    continue

                link = entry.get("link", "")
                if "nitter" in link:
                    link = link.replace("nitter.net/", "x.com/").replace("nitter.", "x.com/")

                tweets.append({
                    "title": title[:150] + "..." if len(title) > 150 else title,
                    "link": link,
                    "published": published,
                    "source": f"@{username}",
                    **X_ACCOUNT_INFO.get(username.lower(), {})
                })
    except:
        pass

    return tweets


def main():
    # 昨天 8:00 到今天 8:00 (北京时间 UTC+8)
    tz_cn = timezone(timedelta(hours=8))
    now_cn = datetime.now(tz_cn)
    start = datetime(now_cn.year, now_cn.month, now_cn.day - 1, 8, 0, 0, tzinfo=tz_cn)
    end = datetime(now_cn.year, now_cn.month, now_cn.day, 8, 0, 0, tzinfo=tz_cn)
    range_label = f"{start.month}_{start.day}-{end.month}_{end.day}"
    ranges = [
        (range_label, start, end),
    ]

    instance = get_available_instance()
    if not instance:
        print("❌ 无法连接Nitter实例")
        return

    print(f"📡 使用实例: {instance}")
    print(f"👥 账号数量: {len(ALL_ACCOUNTS)}")

    for range_name, start_date, end_date in ranges:
        print(f"\n{'='*50}")
        print(f"📅 抓取范围: {range_name}")
        print(f"   开始: {start_date}")
        print(f"   结束: {end_date}")

        all_tweets = []
        for account in ALL_ACCOUNTS:
            tweets = fetch_user_tweets_range(account, instance, start_date, end_date, count=20)
            all_tweets.extend(tweets)
            time.sleep(0.3)
            if len(all_tweets) % 20 == 0:
                print(f"   已抓取 {len(all_tweets)} 条...")

        print(f"   共抓取到 {len(all_tweets)} 条推文")

        # 按 category 分组
        by_cat = defaultdict(list)
        for t in all_tweets:
            cat = t.get('category', '其他')
            by_cat[cat].append(t)

        # 输出统计
        cats = Counter(t.get('category', '?') for t in all_tweets)
        print(f"   分类: {dict(cats)}")

        # 保存到文件
        output_file = Path(__file__).parent / f"twitter_range_{range_name.replace('.', '_')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "range": range_name,
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
                "total": len(all_tweets),
                "tweets": all_tweets
            }, f, ensure_ascii=False, indent=2)
        print(f"   ✅ 已保存到 {output_file}")

        # 生成 Markdown 预览
        md_file = Path(__file__).parent / f"twitter_range_{range_name.replace('.', '_')}.md"
        generate_md(all_tweets, md_file, range_name)
        print(f"   ✅ Markdown预览已保存到 {md_file}")


def generate_md(tweets, output_path, range_name):
    """生成Markdown预览"""
    lines = []
    lines.append(f"# Twitter 动态 - {range_name}")
    lines.append(f"**总计**: {len(tweets)} 条推文")
    lines.append("")

    # 按 category 分组
    by_cat = defaultdict(list)
    for t in tweets:
        cat = t.get('category', '其他')
        by_cat[cat].append(t)

    by_source = defaultdict(list)
    for t in tweets:
        by_source[t['source']].append(t)

    cat_order = ['Company', 'Researcher']
    cat_emoji = {'Company': '🏢', 'Researcher': '👤'}
    cat_names = {'Company': '公司发布', 'Researcher': '研究者动态'}

    for cat in cat_order:
        if cat not in by_cat:
            continue
        lines.append(f"## {cat_emoji[cat]} {cat_names[cat]}（{len(by_cat[cat])}条）")
        lines.append("")

        for source, src_tweets in sorted(by_source.items()):
            if src_tweets[0].get('category') != cat:
                continue

            info = src_tweets[0]
            org = info.get('org', '')
            track = info.get('track', '')

            header = f"### {source}"
            if org:
                header += f" [{org}]"
            if track:
                header += f" | {track}"
            lines.append(header)
            lines.append("")

            for t in src_tweets:
                title = t['title'].replace('\n', ' ')
                url = t['link']
                lines.append(f"- {title}")
                lines.append(f"  [查看]({url})")
            lines.append("")

    Path(output_path).write_text('\n'.join(lines))


if __name__ == "__main__":
    main()