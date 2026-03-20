#!/usr/bin/env python3
"""测试推文分类逻辑"""

import sys
sys.path.insert(0, '/Users/shenyalan/ai-daily-news')

from config_loader import twitter_company_accounts, twitter_researcher_accounts

# 加载配置
COMPANY_ACCOUNTS = twitter_company_accounts()
RESEARCHER_ACCOUNTS = twitter_researcher_accounts()

print(f"📋 公司账号 ({len(COMPANY_ACCOUNTS)}): {sorted(COMPANY_ACCOUNTS)}")
print(f"\n📋 研究者账号 ({len(RESEARCHER_ACCOUNTS)}): {sorted(RESEARCHER_ACCOUNTS)}")

# 测试用例
test_tweets = [
    {"source": "@GoogleDeepMind", "expected": "待分类", "type": "公司"},
    {"source": "@GoogleAI", "expected": "待分类", "type": "公司"},
    {"source": "@OpenAI", "expected": "待分类", "type": "公司"},
    {"source": "@AnthropicAI", "expected": "待分类", "type": "公司"},
    {"source": "@AIatMeta", "expected": "待分类", "type": "公司"},
    {"source": "@MiniMax_AI", "expected": "待分类", "type": "公司"},
    {"source": "@perplexity_ai", "expected": "待分类", "type": "公司"},
    {"source": "@sama", "expected": "X讨论", "type": "个人"},
    {"source": "@jeffdean", "expected": "X讨论", "type": "个人"},
    {"source": "@karpathy", "expected": "X讨论", "type": "个人"},
    {"source": "@denny_zhou", "expected": "X讨论", "type": "个人"},
]

print("\n" + "="*80)
print("分类测试:")
print("="*80)

errors = []
for tweet in test_tweets:
    source = tweet["source"].lower().replace("@", "")
    expected = tweet["expected"]

    is_company = any(c.lower() in source for c in COMPANY_ACCOUNTS)
    is_researcher = any(r.lower() in source for r in RESEARCHER_ACCOUNTS)

    if is_company:
        actual = "待分类"
    elif is_researcher:
        actual = "X讨论"
    else:
        actual = "X讨论"  # 其他账号

    status = "✅" if actual == expected else "❌"
    print(f"{status} {tweet['source']:20s} → {actual:8s} (期望: {expected}, 类型: {tweet['type']})")

    if actual != expected:
        errors.append(f"{tweet['source']} - 实际: {actual}, 期望: {expected}")

print("\n" + "="*80)
if errors:
    print("❌ 测试失败:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✅ 所有测试通过!")
