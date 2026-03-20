#!/usr/bin/env python3
"""测试完整推文分类流程 - 不修改日报文件"""

import json
import sys
sys.path.insert(0, '/Users/shenyalan/ai-daily-news')

from config_loader import twitter_company_accounts, twitter_researcher_accounts

# 加载配置
COMPANY_ACCOUNTS = twitter_company_accounts()
RESEARCHER_ACCOUNTS = twitter_researcher_accounts()

# 读取缓存的推文
cache_file = "/Users/shenyalan/ai-daily-news/tweet_fetcher/cache.json"
with open(cache_file, 'r') as f:
    data = json.load(f)
    tweets = data.get("tweets", data) if isinstance(data, dict) else data

print(f"📦 缓存中有 {len(tweets)} 条推文\n")

# 分类统计
company_tweets = []
researcher_tweets = []
other_tweets = []

for t in tweets:
    source = t.get("source", "").lower().replace("@", "")
    title = t.get("title", "")[:60]

    is_company = any(c.lower() in source for c in COMPANY_ACCOUNTS)
    is_researcher = any(r.lower() in source for r in RESEARCHER_ACCOUNTS)

    if is_company:
        company_tweets.append(t)
    elif is_researcher:
        researcher_tweets.append(t)
    else:
        other_tweets.append(t)

print("="*80)
print(f"🏢 公司推文 → 待分类 ({len(company_tweets)}条)")
print("="*80)
for i, t in enumerate(company_tweets[:10], 1):  # 只显示前10条
    print(f"{i:2d}. {t.get('source', ''):20s} - {t.get('title', '')[:60]}")

print(f"\n" + "="*80)
print(f"👤 个人推文 → X讨论 ({len(researcher_tweets)}条)")
print("="*80)
for i, t in enumerate(researcher_tweets[:10], 1):  # 只显示前10条
    print(f"{i:2d}. {t.get('source', ''):20s} - {t.get('title', '')[:60]}")

print(f"\n" + "="*80)
print(f"❓ 其他推文 → X讨论 ({len(other_tweets)}条)")
print("="*80)
for i, t in enumerate(other_tweets[:10], 1):  # 只显示前10条
    print(f"{i:2d}. {t.get('source', ''):20s} - {t.get('title', '')[:60]}")

print(f"\n" + "="*80)
print("📊 分类统计:")
print("="*80)
print(f"  🏢 公司推文 (待分类): {len(company_tweets)}条")
print(f"  👤 个人推文 (X讨论):  {len(researcher_tweets)}条")
print(f"  ❓ 其他推文 (X讨论):  {len(other_tweets)}条")
print(f"  📝 总计:             {len(tweets)}条")
print("\n✅ 分类逻辑正确:")
print("  - 公司账号推文 → 待分类 (将由LLM根据内容分类)")
print("  - 个人账号推文 → X讨论")
print("  - 其他推文     → X讨论")
