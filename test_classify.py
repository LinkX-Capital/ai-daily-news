#!/usr/bin/env python3
"""
快速测试脚本：验证去重逻辑
用法: python test_classify.py
"""

import sys
sys.path.insert(0, '/Users/shenyalan/ai-daily-news')

from improve_news import improve_news, title_similarity


def run_tests():
    test_articles = [
        {"title": "OpenAI releases GPT-5 with major reasoning improvements", "priority": 100, "categories": ["模型前沿"]},
        {"title": "GPT-5 released by OpenAI showing better reasoning", "priority": 90, "categories": ["模型前沿"]},
        {"title": "Anthropic Claude 4 launches with coding capabilities", "priority": 100, "categories": ["模型前沿"]},
        {"title": "Claude 4 released: Anthropic's new model excels at coding", "priority": 95, "categories": ["模型前沿"]},
        {"title": "NVIDIA announces next-gen GPU architecture", "priority": 100, "categories": ["算力追踪"]},
    ]

    print("=" * 50)
    print("去重测试")
    print("=" * 50)

    # 测试相似度计算
    sim = title_similarity(test_articles[0]["title"], test_articles[1]["title"])
    print(f"\n1. 相似度: '{test_articles[0]['title'][:30]}...' vs '{test_articles[1]['title'][:30]}...'")
    print(f"   结果: {sim:.2f} (期望 >= 0.4)")
    assert sim >= 0.4, f"相似度过低: {sim}"

    # 测试去重
    result = improve_news(test_articles)
    print(f"\n2. 去重: {len(test_articles)} -> {len(result)} 条")
    titles = [a['title'] for a in result]
    # GPT-5 重复应被合并
    gpt5_count = sum(1 for t in titles if 'GPT-5' in t or 'gpt-5' in t.lower())
    assert gpt5_count <= 1, f"GPT-5 重复未去除，剩余 {gpt5_count} 条"

    print("\n全部测试通过!")
    return True


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
