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
MAX_HOURS = 24  # 只保留120小时内的推文


def is_recent(published: str) -> bool:
    """检查推文是否在时间窗口内"""
    try:
        pub_date = parsedate_to_datetime(published)
        now = datetime.now(timezone.utc)
        hours_ago = (now - pub_date).total_seconds() / 3600
        return hours_ago <= MAX_HOURS
    except:
        return False  # 无法解析时间则视为过期


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
        print("   ⚠️ 无法连接Nitter，使用缓存")
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

    if all_tweets:
        save_cache(all_tweets)
        print(f"   抓取到 {len(all_tweets)} 条新推文")
    
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
        cached_at = cache_data.get("cached_at", "")
        
        # 过滤掉过期的推文
        valid_tweets = []
        for t in tweets:
            published = t.get("published", "")
            if is_recent(published):
                valid_tweets.append(t)
        
        if valid_tweets:
            print(f"   缓存中有 {len(valid_tweets)} 条有效推文（过滤了 {len(tweets) - len(valid_tweets)} 条过期）")
        else:
            print(f"   缓存已过期，无有效推文")
            
        return valid_tweets
    except Exception as e:
        print(f"   加载缓存失败: {e}")
        return []


def get_tweets() -> List[Dict]:
    """获取推文，优先抓取新推文，失败时使用缓存"""
    try:
        tweets = fetch_all_tweets()
        if tweets:
            return tweets
        # 抓取为空时尝试使用缓存
        print("   抓取结果为空，尝试使用缓存...")
        return load_cache()
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
