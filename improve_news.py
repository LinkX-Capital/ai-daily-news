#!/usr/bin/env python3
"""
新闻规范化模块
功能：
1. 过滤非新闻内容（活动招募、招聘、播客、营销）
2. 同一公司多条消息去重（最多保留2条）
3. 同账号推文 thread 合并
4. 标题相似度去重
"""

import re
from typing import List, Dict
from collections import defaultdict
from config_loader import non_news_keywords, tier1_ai_companies


# ========== 1. 非新闻内容过滤 ==========

# 补充 config 中可能缺失的英文过滤词（代码层硬编码兜底）
_EXTRA_FILTER_KEYWORDS = [
    # 英文招聘
    "we're hiring", "we're looking for", "dm if interested", "we are hiring",
    "looking for people", "join our team", "open role",
    # 活动邀请
    "come meet us", "join us at", "register now", "sign up for",
    "rsvp", "tickets available",
    # 品牌营销
    "brand refresh", "品牌升级", "品牌焕新",
    # 纯自我回复/pinned
    "pinned tweet",
]


def is_non_news(title: str, summary: str = "") -> bool:
    """判断是否是非新闻内容（应被过滤）"""
    text = (title + " " + (summary or "")).lower()

    # 检查 config 中的非新闻关键词
    for kw in non_news_keywords():
        if kw.lower() in text:
            return True

    # 检查补充的硬编码关键词
    for kw in _EXTRA_FILTER_KEYWORDS:
        if kw.lower() in text:
            return True

    return False


# ========== 2. 同公司去重 ==========

def _extract_company(title: str, summary: str, source: str) -> str:
    """从标题/摘要/来源中提取公司名"""
    text = (title + " " + summary + " " + source).lower()

    # 公司名映射（小写 -> 标准名）
    company_patterns = {
        "openai": "OpenAI", "gpt": "OpenAI", "chatgpt": "OpenAI", "codex": "OpenAI",
        "anthropic": "Anthropic", "claude": "Anthropic",
        "google": "Google", "gemini": "Google", "deepmind": "Google",
        "nvidia": "NVIDIA",
        "meta": "Meta", "llama": "Meta",
        "deepseek": "DeepSeek",
        "xai": "xAI", "grok": "xAI", "spacex": "xAI",
        "vllm": "vLLM", "vllm_project": "vLLM",
        "semianalysis": "SemiAnalysis",
        "luma": "Luma Labs", "lumalabsai": "Luma Labs",
        "prismml": "PrismML",
        "boston dynamics": "Boston Dynamics", "bostondynamics": "Boston Dynamics",
    }

    for pattern, company in company_patterns.items():
        if pattern in text:
            return company

    # 回退：用 source 作为分组键
    return source.lower().strip() if source else "other"


def filter_company_duplicates(articles: List[Dict], max_per_company: int = 2) -> List[Dict]:
    """同一公司只保留优先级最高的 N 条"""
    grouped = defaultdict(list)

    for a in articles:
        company = _extract_company(
            a.get("title", ""),
            a.get("summary", ""),
            a.get("source", "")
        )
        grouped[company].append(a)

    result = []
    for company, arts in grouped.items():
        if company == "other":
            result.extend(arts)
        else:
            sorted_arts = sorted(arts, key=lambda x: x.get("priority", 0), reverse=True)
            kept = sorted_arts[:max_per_company]
            if len(arts) > max_per_company:
                dropped = [a.get("title", "")[:40] for a in sorted_arts[max_per_company:]]
                for d in dropped:
                    print(f"   [公司去重] {company}: 丢弃 '{d}...'")
            result.extend(kept)

    return result


# ========== 3. 推文 Thread 合并 ==========

def merge_tweet_threads(articles: List[Dict]) -> List[Dict]:
    """同一账号的连续推文（reply chain）合并为一条

    判断条件：同一 source + link 中含 reply 标记（R to @）或连续 status ID
    """
    # 按 source 分组推文
    tweet_groups = defaultdict(list)
    non_tweets = []

    for a in articles:
        if a.get("is_tweet"):
            source = a.get("source", "").lower()
            tweet_groups[source].append(a)
        else:
            non_tweets.append(a)

    merged_tweets = []
    for source, tweets in tweet_groups.items():
        if len(tweets) <= 1:
            merged_tweets.extend(tweets)
            continue

        # 按 link 中的 status ID 排序
        def _get_status_id(t):
            link = t.get("link", "")
            m = re.search(r'/status/(\d+)', link)
            return int(m.group(1)) if m else 0

        tweets_sorted = sorted(tweets, key=_get_status_id)

        # 检测 thread：连续的 status ID 差距小（reply chain）
        # 或者标题以 "R to @" 开头（nitter/x.com reply 格式）
        clusters = []
        current_cluster = [tweets_sorted[0]]

        for i in range(1, len(tweets_sorted)):
            prev = tweets_sorted[i - 1]
            curr = tweets_sorted[i]

            prev_id = _get_status_id(prev)
            curr_id = _get_status_id(curr)

            title = curr.get("title", "")
            is_reply = title.startswith("R to @") or title.startswith("RT by @")

            # 同一 thread：ID 差距 < 10 或是 reply
            if prev_id and curr_id and (curr_id - prev_id < 10) or is_reply:
                current_cluster.append(curr)
            else:
                clusters.append(current_cluster)
                current_cluster = [curr]

        clusters.append(current_cluster)

        # 合并每个 cluster
        for cluster in clusters:
            if len(cluster) == 1:
                merged_tweets.append(cluster[0])
            else:
                # 取优先级最高的作为主条目，合并内容
                cluster_sorted = sorted(cluster, key=lambda x: x.get("priority", 0), reverse=True)
                main = dict(cluster_sorted[0])  # 复制

                # 合并所有推文内容到 summary
                all_texts = []
                for t in cluster_sorted:
                    text = t.get("title", "") or t.get("summary", "")
                    if text and text not in all_texts:
                        all_texts.append(text)

                main["summary"] = " | ".join(all_texts)[:600]
                main["content"] = main["summary"]
                main["thread_count"] = len(cluster)

                print(f"   [Thread合并] @{source}: {len(cluster)}条 → 1条")
                merged_tweets.append(main)

    return non_tweets + merged_tweets


# ========== 4. 标题相似度去重 ==========

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
    """规范化新闻：过滤 + thread合并 + 公司去重 + 相似度去重

    Args:
        articles: 新闻列表
        do_filter: True=预规范化（LLM前，执行过滤+thread合并+公司去重）
                   False=后规范化（LLM后，只做相似度去重）
    """
    improved = list(articles)

    if do_filter:
        # 1. 过滤非新闻内容
        before = len(improved)
        filtered = []
        for a in improved:
            title = a.get("title", "")
            summary = a.get("summary", "")
            if is_non_news(title, summary):
                print(f"   过滤: {title[:50]}...")
            else:
                filtered.append(a)
        improved = filtered
        print(f"   过滤后: {len(improved)} 条")

        # 2. 推文 thread 合并
        improved = merge_tweet_threads(improved)

        # 3. 同公司去重（最多保留2条）
        improved = filter_company_duplicates(improved, max_per_company=2)

    # 4. 标题相似度去重（前后规范化都执行）
    improved = filter_similar_duplicates(improved, threshold=0.35, debug=True)
    print(f"   去重后: {len(improved)} 条")

    return improved


if __name__ == "__main__":
    test_articles = [
        {"title": "OpenAI releases GPT-5 with major reasoning improvements", "priority": 100, "categories": ["模型前沿"]},
        {"title": "GPT-5 released by OpenAI showing better reasoning", "priority": 90, "categories": ["模型前沿"]},
        {"title": "Anthropic Claude 4 launches with coding capabilities", "priority": 100, "categories": ["模型前沿"]},
        {"title": "PrismML招聘大规模LLM训练经验工程师", "priority": 50, "categories": ["X讨论"]},
        {"title": "Come meet us at AI on the Lot in Culver City", "priority": 30, "categories": ["产业动态"]},
    ]
    result = improve_news(test_articles)
    print("\n结果:")
    for a in result:
        print(f"  - {a['title'][:50]}... -> {a.get('categories', [])}")
