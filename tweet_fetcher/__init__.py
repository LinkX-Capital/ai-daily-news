"""Twitter/X 推文抓取器 - 支持多实例自动切换"""

import feedparser
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
import httpx
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone

# 账号配置
X_ACCOUNTS = {
    "OpenAI": ["OpenAI", "sama", "_jasonwei", "ShunyuYao12"],
    "Google DeepMind": ["GoogleDeepMind", "denny_zhou", "NeelNanda5", "YiTayML"],
    "Meta": ["AIatMeta", "jaseweston"],
    "Anthropic": ["AnthropicAI", "thesephist"],
    "xAI": ["xai","TheGregYang", "tingchenai"],
    "World Labs": ["theworldlabs"],
    "Physical Intelligence": ["physical_int"],
    "DeepSeek": ["deepseek_ai"],
    "Qwen": ["Alibaba_Qwen"],
    "Stanford": ["drfeifei", "chelseabfinn", "percyliang"],
    "UCB": ["pabbeel", "svlevine"],
    "NYU": ["ylecun"],
    "karpathy": ["karpathy"],
    "AndrewYNg": ["AndrewYNg"],
    "AI社区": ["swyx"],
    "vLLM": ["vllm_project"],
}

NITTER_INSTANCES = [
    "https://nitter.net",
    "https://nitter.poast.org",
    "https://nitter.privacydev.net",
    "https://nitter.hu",
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/rss+xml, application/xml, text/xml',
}

CACHE_FILE = Path(__file__).parent / "cache.json"
TIMEOUT = 15
MAX_PER_ACCOUNT = 3
MAX_HOURS = 120


def is_recent(published: str) -> bool:
    try:
        pub_date = parsedate_to_datetime(published)
        now = datetime.now(timezone.utc)
        hours_ago = (now - pub_date).total_seconds() / 3600
        return hours_ago <= MAX_HOURS
    except:
        return True


def get_available_instance() -> Optional[str]:
    for instance in NITTER_INSTANCES:
        try:
            client = httpx.Client(timeout=5.0, headers=HEADERS)
            resp = client.get(f"{instance}/OpenAI/rss")
            if resp.status_code == 200 and len(resp.text) > 100:
                return instance
        except:
            continue
    return None


def fetch_user_tweets(username: str, instance: str, count: int = 3) -> List[Dict]:
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

                if not is_recent(published):
                    continue
                if title and len(title) > 30 and not title.startswith("RT @"):
                    link = entry.get("link", "")
                    if "nitter" in link:
                        link = link.replace("nitter.net/", "x.com/").replace("nitter.", "x.com/")

                    tweets.append({
                        "title": title[:150] + "..." if len(title) > 150 else title,
                        "link": link,
                        "published": published,
                        "source": f"@{username}",
                    })
    except:
        pass

    return tweets


def fetch_all_tweets(max_per_account: int = MAX_PER_ACCOUNT) -> List[Dict]:
    instance = get_available_instance()
    if not instance:
        return load_cache()

    print(f"   使用实例: {instance}")

    all_tweets = []
    for company, accounts in X_ACCOUNTS.items():
        for account in accounts:
            tweets = fetch_user_tweets(account, instance, max_per_account)
            for t in tweets:
                t["company"] = company
            all_tweets.extend(tweets)
            time.sleep(0.3)

    save_cache(all_tweets)
    return all_tweets


def save_cache(tweets: List[Dict]):
    CACHE_FILE.write_text(json.dumps(tweets, ensure_ascii=False, indent=2))


def load_cache() -> List[Dict]:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except:
            pass
    return []


def get_tweets() -> List[Dict]:
    try:
        return fetch_all_tweets()
    except Exception as e:
        print(f"   抓取失败: {e}, 使用缓存")
        return load_cache()


if __name__ == "__main__":
    print("📡 抓取研究者动态...")
    tweets = get_tweets()
    print(f"   获取 {len(tweets)} 条推文")

    from collections import Counter
    companies = Counter(t.get("company", "other") for t in tweets)
    for c, n in companies.most_common(5):
        print(f"      {c}: {n}")
