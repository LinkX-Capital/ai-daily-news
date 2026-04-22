#!/usr/bin/env python3
"""
新闻去重模块（精简版）
分类、过滤等已由 LLM 完成，本模块仅保留去重逻辑
"""

import re
from typing import List, Dict
from collections import defaultdict


# ========== 标题相似度去重 ==========
def normalize_for_comparison(text: str) -> set:
    """将标题标准化为用于比较的词集合"""
    text = text.lower()
    stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
                 "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
                 "being", "have", "has", "had", "do", "does", "did", "will", "would",
                 "could", "should", "may", "might", "can", "this", "that", "these",
                 "those", "it", "its", "2026", "2025", "2024", "2023", "-", ":", "|",
                 "now", "new", "pro", "3", "2", "1", "ai", "llm", "model", "google",
                 "openai", "meta", "microsoft", "anthropic", "deepmind"}
    english_words = set(w for w in re.findall(r'[a-z]+', text) if w not in stopwords and len(w) > 1)
    chinese_text = re.sub(r'[a-z0-9\s]', '', text)
    chinese_bigrams = set(chinese_text[i:i+2] for i in range(len(chinese_text)-1))
    return english_words | chinese_bigrams

def title_similarity(t1: str, t2: str) -> float:
    """计算两个标题的相似度 (Jaccard)"""
    set1 = normalize_for_comparison(t1)
    set2 = normalize_for_comparison(t2)
    if not set1 or not set2:
        return 0.0
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    return intersection / union if union > 0 else 0.0

def filter_similar_duplicates(articles: List[Dict], threshold: float = 0.4, debug: bool = False) -> List[Dict]:
    """基于标题相似度去重，保留优先级高的"""
    if len(articles) <= 1:
        return articles

    result = []
    for a in articles:
        title = a.get("title", "")
        is_duplicate = False
        for existing in result:
            sim = title_similarity(title, existing.get("title", ""))
            if sim >= threshold:
                if debug:
                    print(f"   [相似去重] '{title[:30]}...' ~= '{existing.get('title', '')[:30]}...' ({sim:.2f})")
                if a.get("priority", 0) > existing.get("priority", 0):
                    result.remove(existing)
                    result.append(a)
                is_duplicate = True
                break
            if not is_duplicate and sim >= threshold * 0.7:
                t1_words = normalize_for_comparison(title)
                t2_words = normalize_for_comparison(existing.get("title", ""))
                core_overlap = len(t1_words & t2_words) / max(len(t1_words | t2_words), 1)
                if core_overlap >= 0.5:
                    if debug:
                        print(f"   [核心词去重] '{title[:30]}...' ~= '{existing.get('title', '')[:30]}...' (core:{core_overlap:.2f})")
                    if a.get("priority", 0) > existing.get("priority", 0):
                        result.remove(existing)
                        result.append(a)
                    is_duplicate = True
                    break
        if not is_duplicate:
            result.append(a)
    return result


# ========== 主函数 ==========
def improve_news(articles: List[Dict], do_filter: bool = True) -> List[Dict]:
    """去重（分类和过滤已由 LLM 完成）

    Args:
        articles: 新闻列表
        do_filter: 保留参数兼容 feed_v5.py，实际不再过滤
    """
    improved = list(articles)

    # 标题相似度去重
    improved = filter_similar_duplicates(improved, threshold=0.35, debug=True)
    print(f"   去重后: {len(improved)} 条")

    return improved


if __name__ == "__main__":
    test_articles = [
        {"title": "OpenAI releases GPT-5 with major reasoning improvements", "priority": 100, "categories": ["模型前沿"]},
        {"title": "GPT-5 released by OpenAI showing better reasoning", "priority": 90, "categories": ["模型前沿"]},
        {"title": "Anthropic Claude 4 launches with coding capabilities", "priority": 100, "categories": ["模型前沿"]},
    ]
    result = improve_news(test_articles)
    for a in result:
        print(f"  - {a['title'][:50]}... -> {a['categories']}")
