"""Twitter/X 推文抓取器 - 统一账号配置（twitterapi.io API）

公共 Nitter 实例已于 2026-08 全线失效（403/人机验证/白名单），改用
twitterapi.io REST API。API key 存放于本目录 api.key（已被 .gitignore
的 *.key 规则忽略），也可通过环境变量 TWITTERAPI_KEY 提供。
"""

import json
import os
import time
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timezone

import httpx
import yaml

# ============ 配置加载 ============
CONFIG_FILE = Path(__file__).parent.parent / "accounts.yaml"
CACHE_FILE = Path(__file__).parent / "cache.json"
KEY_FILE = Path(__file__).parent / "api.key"
API_URL = "https://api.twitterapi.io/twitter/user/last_tweets"
TIMEOUT = 20
MAX_HOURS = 24
TITLE_MAX = 400


def get_api_key() -> str:
    if KEY_FILE.exists():
        key = KEY_FILE.read_text().strip()
        if key:
            return key
    return os.environ.get("TWITTERAPI_KEY", "")


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


def parse_pub_date(published: str) -> Optional[datetime]:
    """解析推文时间：兼容 twitterapi.io 格式与 RFC822（旧缓存）"""
    if not published:
        return None
    try:
        # twitterapi.io: "Sun Aug 02 03:00:09 +0000 2026"
        return datetime.strptime(published, "%a %b %d %H:%M:%S %z %Y")
    except ValueError:
        pass
    try:
        return parsedate_to_datetime(published)
    except Exception:
        return None


def is_recent(published: str, start_time: datetime = None, end_time: datetime = None) -> bool:
    """检查推文是否在时间窗口内"""
    pub_date = parse_pub_date(published)
    if pub_date is None:
        return False

    # 自定义时间窗口
    if start_time and end_time:
        return start_time <= pub_date < end_time

    # 默认：现在往前 MAX_HOURS 小时
    now = datetime.now(timezone.utc)
    hours_ago = (now - pub_date).total_seconds() / 3600
    return hours_ago <= MAX_HOURS


def fetch_user_tweets(username: str, count: int = 10, start_time: datetime = None, end_time: datetime = None) -> List[Dict]:
    api_key = get_api_key()
    if not api_key:
        print("   ⚠️ 未配置 twitterapi.io API key（tweet_fetcher/api.key 或 TWITTERAPI_KEY）")
        return []

    try:
        resp = httpx.get(
            API_URL,
            params={"userName": username, "count": count},
            headers={"x-api-key": api_key},
            timeout=TIMEOUT,
        )
        if resp.status_code != 200:
            return []
        raw_tweets = resp.json().get("data", {}).get("tweets", [])
    except Exception:
        return []

    tweets = []
    for tw in raw_tweets:
        published = tw.get("createdAt", "")
        if not is_recent(published, start_time, end_time):
            continue

        text = (tw.get("text") or "").strip()
        if len(text) < 30:
            continue
        # 过滤：回复自己 / 回复他人（回复多为碎片噪声）
        if tw.get("isReply"):
            continue

        tweets.append({
            "title": text[:TITLE_MAX] + "..." if len(text) > TITLE_MAX else text,
            "link": tw.get("url", ""),
            "published": published,
            "source": f"@{username}",
            **X_ACCOUNT_INFO.get(username.lower(), {})
        })
        if len(tweets) >= count:
            break

    return tweets


def fetch_all_tweets(max_per_account: int = 10, start_time: datetime = None, end_time: datetime = None) -> List[Dict]:
    all_tweets = []
    failed_accounts = []

    for account in ALL_ACCOUNTS:
        try:
            tweets = fetch_user_tweets(account, max_per_account, start_time, end_time)
        except Exception as e:
            tweets = []
            print(f"      @{account}: 请求异常 {e}")
        if tweets:
            all_tweets.extend(tweets)
        else:
            failed_accounts.append(account)
        time.sleep(0.5)

    if failed_accounts:
        print(f"   ℹ️ {len(failed_accounts)} 个账号窗口内无有效推文")
        for account in failed_accounts[:10]:
            print(f"      @{account}: no recent tweets")

    if all_tweets:
        save_cache(all_tweets)
        print(f"   抓取到 {len(all_tweets)} 条新推文")
    else:
        print("   ⚠️ 本轮抓取为空")

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
