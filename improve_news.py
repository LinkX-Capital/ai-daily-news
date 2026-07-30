#!/usr/bin/env python3
"""
新闻规范化模块
功能：
1. 过滤非新闻内容（活动招募、招聘、播客、营销）
2. 仅在存在明确父子关系时合并同账号推文 thread
3. 仅对高置信同事件做去重

公司/来源多样性属于最终选稿约束，不应在 rank 前硬删除候选。
"""

import re
from typing import List, Dict, Optional
from collections import defaultdict
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from config_loader import non_news_keywords


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

    # Routine hiring/personnel announcements are not daily frontier events.
    # Keep this narrow so founder/CEO departures or material reorganizations
    # can still reach editorial ranking.
    routine_hire_patterns = (
        r"\b(?:joins?|joining|appoints?|appointed|hires?|hired)\b.{0,80}"
        r"\b(?:chief financial officer|cfo)\b",
        r"\b(?:chief financial officer|cfo)\b.{0,80}"
        r"\b(?:joins?|joining|appointed|hired)\b",
        r"(?:任命|加入).{0,30}(?:首席财务官|CFO)",
    )
    if any(re.search(pattern, text, re.IGNORECASE) for pattern in routine_hire_patterns):
        return True

    return False


# ========== 2. 公司识别（仅供兼容调用，不参与预排序删除） ==========

def _extract_company(title: str, summary: str, source: str) -> Optional[str]:
    """从标题/摘要/来源中提取已知公司名。

    无法识别时必须返回 ``None``。媒体来源（如 TechCrunch、The
    Information、arXiv）不是新闻主体，不能作为公司分组键。
    """
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

    return None


def filter_company_duplicates(articles: List[Dict], max_per_company: int = 2) -> List[Dict]:
    """兼容旧调用：同一已识别公司只保留优先级最高的 N 条。

    该函数不再由 :func:`improve_news` 的预排序流程调用。未知主体逐条
    保留，不能因共享同一媒体来源而被分组删除。
    """
    grouped = defaultdict(list)
    unknown = []

    for a in articles:
        company = _extract_company(
            a.get("title", ""),
            a.get("summary", ""),
            a.get("source", "")
        )
        if company is None:
            unknown.append(a)
        else:
            grouped[company].append(a)

    result = list(unknown)
    for company, arts in grouped.items():
        sorted_arts = sorted(arts, key=lambda x: x.get("priority", 0), reverse=True)
        kept = sorted_arts[:max_per_company]
        if len(arts) > max_per_company:
            dropped = [a.get("title", "")[:40] for a in sorted_arts[max_per_company:]]
            for d in dropped:
                print(f"   [公司去重] {company}: 丢弃 '{d}...'")
        result.extend(kept)

    return result


# ========== 3. 推文 Thread 合并 ==========

def _coerce_tweet_id(value) -> Optional[str]:
    """把显式 tweet/status id 或 URL 规范化为数字字符串。"""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, int):
        return str(value) if value > 0 else None

    text = str(value).strip()
    if text.isdigit():
        return text
    match = re.search(r"/status/(\d+)", text)
    return match.group(1) if match else None


def _tweet_status_id(article: Dict) -> Optional[str]:
    for key in ("tweet_id", "status_id", "id_str"):
        status_id = _coerce_tweet_id(article.get(key))
        if status_id:
            return status_id
    return _coerce_tweet_id(article.get("link"))


def _tweet_parent_id(article: Dict) -> Optional[str]:
    for key in (
        "in_reply_to_status_id",
        "in_reply_to_status_id_str",
        "in_reply_to_tweet_id",
        "reply_to_status_id",
        "parent_tweet_id",
    ):
        parent_id = _coerce_tweet_id(article.get(key))
        if parent_id:
            return parent_id
    return None


def _tweet_conversation_id(article: Dict) -> Optional[str]:
    for key in ("conversation_id", "conversation_id_str"):
        conversation_id = _coerce_tweet_id(article.get(key))
        if conversation_id:
            return conversation_id
    return None


def merge_tweet_threads(articles: List[Dict]) -> List[Dict]:
    """仅在存在明确关系元数据时合并同一账号的推文 thread。

    X/Twitter 的 snowflake status id 不是 thread id；标题以 ``R to @``
    开头也只说明它回复了某人，无法说明它回复的是列表中的相邻推文。
    因此只有以下证据可以触发合并：

    - ``in_reply_to_*``/``parent_tweet_id`` 精确指向同账号候选；或
    - 多条候选带有相同的显式 ``conversation_id``。

    缺少这些字段时宁可不合并。
    """
    indexed_articles = list(enumerate(articles))
    tweet_groups = defaultdict(list)
    for index, a in indexed_articles:
        if a.get("is_tweet"):
            source = a.get("source", "").lower()
            tweet_groups[source].append((index, a))

    replacements = {}
    consumed = set()

    for source, indexed_tweets in tweet_groups.items():
        if len(indexed_tweets) <= 1:
            continue

        parent = {index: index for index, _ in indexed_tweets}

        def find(index):
            while parent[index] != index:
                parent[index] = parent[parent[index]]
                index = parent[index]
            return index

        def union(left, right):
            left_root = find(left)
            right_root = find(right)
            if left_root != right_root:
                parent[right_root] = left_root

        # 只有唯一 status id 才能作为精确父节点，避免脏数据误连。
        status_members = defaultdict(list)
        for index, tweet in indexed_tweets:
            status_id = _tweet_status_id(tweet)
            if status_id:
                status_members[status_id].append(index)
        unique_status_index = {
            status_id: members[0]
            for status_id, members in status_members.items()
            if len(members) == 1
        }

        for index, tweet in indexed_tweets:
            parent_id = _tweet_parent_id(tweet)
            if parent_id and parent_id in unique_status_index:
                union(index, unique_status_index[parent_id])

        conversation_groups = defaultdict(list)
        for index, tweet in indexed_tweets:
            conversation_id = _tweet_conversation_id(tweet)
            if conversation_id:
                conversation_groups[conversation_id].append(index)
        for members in conversation_groups.values():
            if len(members) > 1:
                first = members[0]
                for member in members[1:]:
                    union(first, member)

        components = defaultdict(list)
        tweet_by_index = dict(indexed_tweets)
        for index, _ in indexed_tweets:
            components[find(index)].append(index)

        for component in components.values():
            if len(component) <= 1:
                continue

            component.sort()
            cluster = [tweet_by_index[index] for index in component]
            main = dict(max(cluster, key=lambda x: x.get("priority", 0)))

            all_texts = []
            for tweet in cluster:
                text = tweet.get("title", "") or tweet.get("summary", "")
                if text and text not in all_texts:
                    all_texts.append(text)

            main["summary"] = " | ".join(all_texts)[:600]
            main["content"] = main["summary"]
            main["thread_count"] = len(cluster)

            first_index = component[0]
            replacements[first_index] = main
            consumed.update(component[1:])
            account = source.lstrip("@")
            print(f"   [Thread合并] @{account}: {len(cluster)}条 → 1条")

    result = []
    for index, article in indexed_articles:
        if index in consumed:
            continue
        result.append(replacements.get(index, article))
    return result


# ========== 4. 高置信同事件去重 ==========

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
    word_aliases = {
        "release": "release", "releases": "release", "released": "release", "releasing": "release",
        "launch": "release", "launches": "release", "launched": "release", "launching": "release",
    }
    english_words = set()
    for word in re.findall(r'[a-z]+', text):
        word = word_aliases.get(word, word)
        if word not in stopwords and len(word) > 1:
            english_words.add(word)
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


_TRACKING_QUERY_KEYS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "utm_id", "gclid", "fbclid",
}

_GENERIC_EVENT_ANCHORS = {
    "about", "after", "again", "against", "available", "build", "company",
    "complete", "completed", "day", "excited", "funding", "happy", "have",
    "lands", "latest", "launch", "live", "million", "news", "now", "our",
    "partner", "partners", "partnership", "raises", "raised", "release",
    "report", "startup", "their", "this", "today", "update", "with", "your",
}


def _canonical_link(link: str) -> str:
    """移除 fragment 和常见跟踪参数，保留可证明同源的 URL。"""
    if not link:
        return ""
    try:
        parts = urlsplit(link.strip())
        query = urlencode([
            (key, value)
            for key, value in parse_qsl(parts.query, keep_blank_values=True)
            if key.lower() not in _TRACKING_QUERY_KEYS
        ])
        path = parts.path.rstrip("/") or "/"
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, query, ""))
    except ValueError:
        return link.strip().rstrip("/").split("#", 1)[0]


def _canonical_title(title: str) -> str:
    return re.sub(r"[\W_]+", "", title.lower(), flags=re.UNICODE)


def _distinctive_english_anchors(title: str) -> set:
    """提取英文专名/产品锚点；通用新闻动作不算事件身份。"""
    anchors = set()
    for token in re.findall(r"(?<!\w)@?[a-z][a-z0-9]*(?:[-_.][a-z0-9]+)*(?!\w)", title.lower()):
        token = token.lstrip("@")
        if len(token) < 3 or token in _GENERIC_EVENT_ANCHORS:
            continue
        anchors.add(token)
    return anchors


def _is_high_confidence_duplicate(article: Dict, existing: Dict, threshold: float) -> bool:
    link = _canonical_link(article.get("link", ""))
    existing_link = _canonical_link(existing.get("link", ""))
    if link and existing_link and link == existing_link:
        return True

    title = article.get("title", "")
    existing_title = existing.get("title", "")
    if title and existing_title and _canonical_title(title) == _canonical_title(existing_title):
        return True

    similarity = title_similarity(title, existing_title)
    shared_anchors = (
        _distinctive_english_anchors(title)
        & _distinctive_english_anchors(existing_title)
    )
    # 低于 0.4 时，类似“Kimi K3 已在 A/B 平台上线”或不同合作伙伴
    # 的模板化公告仍可能共享许多词，但并不是同一条可互换的新闻。
    return similarity >= max(threshold, 0.4) and len(shared_anchors) >= 3


def filter_similar_duplicates(articles: List[Dict], threshold: float = 0.4, debug: bool = False) -> List[Dict]:
    """仅对高置信同事件去重，保留优先级高的候选。

    通用模板相似（如“某公司获得种子轮融资”）不足以证明是同一事件。
    除精确链接/标题外，模糊匹配还必须共享至少三个英文专名或产品锚点。
    """
    if len(articles) <= 1:
        return articles

    result = []
    for a in articles:
        title = a.get("title", "")
        is_duplicate = False
        for existing in result:
            sim = title_similarity(title, existing.get("title", ""))
            if _is_high_confidence_duplicate(a, existing, threshold):
                if debug:
                    print(f"   [高置信去重] '{title[:30]}...' ~= '{existing.get('title', '')[:30]}...' ({sim:.2f})")
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
    """规范化新闻：过滤 + 保守 thread 合并 + 高置信事件去重。

    Args:
        articles: 新闻列表
        do_filter: True=预规范化（LLM前，执行过滤+保守 thread 合并）
                   False=后规范化（LLM后，只做高置信事件去重）
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

    # 3. 高置信同事件去重（前后规范化都执行）
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
