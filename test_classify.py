#!/usr/bin/env python3
"""
快速测试脚本：验证分类和过滤逻辑
用法: python test_classify.py
"""

import json
import sys
sys.path.insert(0, '/Users/shenyalan/ai-daily-news')

from improve_news import is_non_news, fix_category

def run_tests():
    with open('/Users/shenyalan/ai-daily-news/test_cases.json', 'r') as f:
        data = json.load(f)

    cases = data['cases']
    passed = 0
    failed = 0

    print("=" * 50)
    print("🧪 分类与过滤测试")
    print("=" * 50)

    for i, c in enumerate(cases, 1):
        title = c['title']
        summary = c.get('summary', '')
        expected_cat = c['expected_category']
        expected_keep = c['expected_keep']

        # 测试过滤
        should_filter = is_non_news(title, summary)
        actual_keep = not should_filter

        # 测试分类
        actual_cat = fix_category(title, summary, "")

        # 判断结果
        keep_ok = actual_keep == expected_keep
        cat_ok = actual_cat == expected_cat or expected_cat == "其他"
        ok = keep_ok and cat_ok

        if ok:
            passed += 1
            status = "✅"
        else:
            failed += 1
            status = "❌"

        print(f"\n{status} [{i}/{len(cases)}] {title[:40]}...")
        if not keep_ok:
            print(f"   过滤: 期望{'保留' if expected_keep else '过滤'}, 实际{'保留' if actual_keep else '过滤'}")
        if not cat_ok:
            print(f"   分类: 期望{expected_cat}, 实际{actual_cat}")
        if not ok and c.get('reason'):
            print(f"   原因: {c['reason']}")

    print("\n" + "=" * 50)
    print(f"结果: {passed} 通过, {failed} 失败")
    print("=" * 50)

    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
