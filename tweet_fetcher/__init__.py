"""Twitter/X 推文抓取器 - 统一账号配置"""

import feedparser
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
import httpx
import yaml
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

# ============ 配置加载 ============
CONFIG_FILE = Path(__file__).parent.parent / "accounts.yaml"
CACHE_FILE = Path(__file__).parent / "cache.json"
TIMEOUT = 15
MAX_HOURS = 24

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
    """从 accounts.yaml 加载配置"""
    if CONFIG_FILE.exists():
        return yaml.safe_load(CONFIG_FILE.read_text())
    return {}


def get_accounts() -> tuple[Dict[str, List[str]], Dict[str, str], List[str]]:
    """
    返回:
    - account_groups: {"Company": [...], "Researcher": [...]} 按分类分组的账号列表
    - account_info: {handle: {category, track, org}} 账号详情
    - all_handles: 所有账号 handle 列表（去重）
    """
    config = load_config()
    accounts = config.get("accounts", [])
    settings = config.get("settings", {})

    account_groups = {"Company": [], "Researcher": []}
    account_info = {}
    seen = set()

    for acc in accounts:
        handle = acc.get("handle", "").lower()  # 统一小写
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


# 加载账号配置
X_ACCOUNT_GROUPS, X_ACCOUNT_INFO, ALL_ACCOUNTS = get_accounts()


def is_recent(published: str, start_time: datetime = None, end_time: datetime = None) -> bool:
    """检查推文是否在时间窗口内"""
    try:
        pub_date = parsedate_to_datetime(published)

        # 自定义时间窗口
        if start_time and end_time:
            return start_time <= pub_date < end_time

        # 默认：现在往前 MAX_HOURS 小时
        now = datetime.now(timezone.utc)
        hours_ago = (now - pub_date).total_seconds() / 3600
        return hours_ago <= MAX_HOURS
    except:
        return False


def get_available_instance(username: str = "OpenAI") -> Optional[str]:
    for instance in NITTER_INSTANCES:
        try:
            with httpx.Client(timeout=5.0, headers=HEADERS, follow_redirects=True) as client:
                resp = client.get(f"{instance}/{username}/rss")
            if resp.status_code == 200 and len(resp.text) > 100 and resp.text.lstrip().startswith("<?xml"):
                return instance
        except Exception:
            continue
    return None


def fetch_user_tweets(username: str, instance: str, count: int = 10, start_time: datetime = None, end_time: datetime = None) -> List[Dict]:
    tweets = []
    url = f"{instance}/{username}/rss"

    try:
        client = httpx.Client(timeout=TIMEOUT, headers=HEADERS, follow_redirects=True)
        resp = client.get(url)
        if resp.status_code != 200 or not resp.text.lstrip().startswith("<?xml"):
            return []

        feed = feedparser.parse(resp.text)
        if feed.entries:
            for entry in feed.entries:
                title = entry.get("title", "")
                published = entry.get("published", "")

                if not is_recent(published, start_time, end_time):
                    continue

                # 解析格式：RT（转推）或 R to @（回复）
                is_retweet = title.startswith("RT ")
                is_reply = title.startswith("R to @")

                # 提取实际内容
                if is_retweet:
                    content = title.split(": ", 1)[1] if ": " in title else title[3:]
                elif is_reply:
                    content = title.split(": ", 1)[1] if ": " in title else title[4:]
                else:
                    content = title

                # 过滤：内容太短
                if len(content.strip()) < 30:
                    continue
                # 过滤：自己转自己/回复自己
                if is_retweet and f"@{username}" in title:
                    continue
                if is_reply and (f"R to @{username}" in title or f"R to @{username.lower()}" in title):
                    continue

                link = entry.get("link", "")
                for nitter_instance in NITTER_INSTANCES:
                    link = link.replace(f"{nitter_instance}/", "https://x.com/")

                tweets.append({
                    "title": title[:150] + "..." if len(title) > 150 else title,
                    "link": link,
                    "published": published,
                    "source": f"@{username}",
                    **X_ACCOUNT_INFO.get(username.lower(), {})
                })
                if len(tweets) >= count:
                    break
    except:
        pass

    return tweets


def fetch_all_tweets(max_per_account: int = 10, start_time: datetime = None, end_time: datetime = None) -> List[Dict]:
    all_tweets = []
    failed_accounts = []

    for account in ALL_ACCOUNTS:
        tweets = []
        last_error = "no instance tried"
        for instance in NITTER_INSTANCES:
            tweets = fetch_user_tweets(account, instance, max_per_account, start_time, end_time)
            if tweets:
                break
            last_error = f"{instance}: no recent tweets"
        if tweets:
            all_tweets.extend(tweets)
        else:
            failed_accounts.append((account, last_error))
        time.sleep(0.3)

    if failed_accounts:
        print(f"   ⚠️ {len(failed_accounts)} 个账号未抓到有效推文")
        for account, reason in failed_accounts[:10]:
            print(f"      @{account}: {reason}")

    if all_tweets:
        save_cache(all_tweets)
        print(f"   抓取到 {len(all_tweets)} 条新推文")
    else:
        print("   ⚠️ 本轮抓取为空，不覆盖缓存")

    return all_tweets


def save_cache(tweets: List[Dict]):
    """保存到缓存，包含缓存时间"""
    cache_data = {
        "tweets": tweets,
        "cached_at": datetime.now().isoformat()
    }
    CACHE_FILE.write_text(json.dumps(cache_data, ensure_ascii=False, indent=2))


def load_cache() -> List[Dict]:
    """加载缓存，并过滤过期推文"""
    if not CACHE_FILE.exists():
        return []

    try:
        cache_data = json.loads(CACHE_FILE.read_text())
        tweets = cache_data.get("tweets", [])

        valid_tweets = [t for t in tweets if is_recent(t.get("published", ""))]

        if valid_tweets:
            print(f"   缓存中有 {len(valid_tweets)} 条有效推文（过滤了 {len(tweets) - len(valid_tweets)} 条过期）")
        else:
            print(f"   缓存已过期，无有效推文")

        return valid_tweets
    except Exception as e:
        print(f"   加载缓存失败: {e}")
        return []


def get_tweets(start_time: datetime = None, end_time: datetime = None) -> List[Dict]:
    """获取推文，优先抓取新推文，失败时使用缓存"""
    try:
        tweets = fetch_all_tweets(start_time=start_time, end_time=end_time)
        if tweets:
            return tweets
        print("   抓取结果为空，尝试使用缓存...")
        return load_cache()
    except Exception as e:
        print(f"   抓取失败: {e}, 使用缓存")
        return load_cache()


if __name__ == "__main__":
    print("📡 抓取研究者动态...")
    print(f"   加载 {len(ALL_ACCOUNTS)} 个账号")

    from collections import Counter
    cats = Counter(X_ACCOUNT_INFO.get(acc, {}).get("category", "other") for acc in ALL_ACCOUNTS)
    print(f"   分类分布: {dict(cats)}")

    tweets = get_tweets()
    print(f"   获取 {len(tweets)} 条推文")
