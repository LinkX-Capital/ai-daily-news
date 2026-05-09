#!/usr/bin/env python3
"""
AI 前沿动态 - v5.0
重点优化：研究关注按具体领域和学者被引量排序
"""

import feedparser
import httpx
import os
import json
import argparse
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import re
import urllib3

# 导入规范化模块
import sys
sys.path.insert(0, '/Users/shenyalan/ai-daily-news')
from improve_news import improve_news, title_similarity
from config_loader import (
    twitter_company_accounts, twitter_researcher_accounts,
    tier1_ai_companies, research_subfields, top_conferences,
    high_citation_authors, official_sources,
    base_dir, archive_dir, output_md, output_html, output_html_path, cache_file, tweet_cache, opml_file
)
from html_generator import md_to_html

# 导入研究者推文抓取
def fetch_researcher_tweets():
    """抓取前沿研究者推文：缓存超过30分钟则触发新抓取，否则用缓存"""
    import json
    import os
    from datetime import datetime, timezone

    cache_path = tweet_cache()
    CACHE_MAX_AGE_MINUTES = 30

    def _load_cache():
        if not os.path.exists(cache_path):
            return None
        with open(cache_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        tweets = data.get("tweets", data) if isinstance(data, dict) else data
        cached_at = data.get("cached_at", "") if isinstance(data, dict) else ""
        return tweets, cached_at

    # 检查缓存新鲜度
    try:
        cached = _load_cache()
        if cached:
            tweets, cached_at = cached
            if cached_at:
                cache_time = datetime.fromisoformat(cached_at).replace(tzinfo=None)
                age_minutes = (datetime.now() - cache_time).total_seconds() / 60
                if age_minutes <= CACHE_MAX_AGE_MINUTES:
                    print(f"   📦 使用缓存: {len(tweets)} 条推文（{age_minutes:.0f} 分钟前抓取）")
                    return tweets
                else:
                    print(f"   ⚠️ 缓存已过期（{age_minutes:.0f} 分钟前），尝试重新抓取...")
    except Exception as e:
        print(f"   ⚠️ 缓存检查失败: {e}")

    # 缓存过期或不存在，尝试实时抓取
    try:
        from tweet_fetcher import fetch_all_tweets
        fresh_tweets = fetch_all_tweets()
        if fresh_tweets:
            print(f"   ✅ 实时抓取: {len(fresh_tweets)} 条推文")
            return fresh_tweets
    except Exception as e:
        print(f"   ⚠️ 实时抓取失败: {e}")

    # 抓取失败，回退到过期缓存
    try:
        cached = _load_cache()
        if cached and cached[0]:
            print(f"   📦 回退到过期缓存: {len(cached[0])} 条推文")
            return cached[0]
    except Exception:
        pass

    print(f"   ⚠️ 无可用推文数据")
    return []

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========== 配置 ==========
API_KEY = os.environ.get("MINIMAX_API_KEY", "")  # 独立变量，不影响 GLM
API_URL = "https://api.minimaxi.com/anthropic/v1/messages"
OPML_FILE = opml_file()
ARCHIVE_DIR = archive_dir()
OUTPUT_FILE = output_md()
CACHE_FILE = cache_file()

os.makedirs(ARCHIVE_DIR, exist_ok=True)

# ========== RSS 源读取 ==========
def parse_opml(opml_file):
    sources = {}
    try:
        with open(opml_file, 'r', encoding='utf-8') as f:
            content = f.read()
        lines = content.split('\n')
        for line in lines:
            url_match = re.search(r'xmlUrl="([^"]+)"', line)
            title_match = re.search(r'title="([^"]+)"', line)
            if url_match and title_match:
                url = url_match.group(1)
                title = title_match.group(1)
                cn_keywords = ["36kr", "wechat", "qbitai", "xlab", "itjuzi", "juzi", "github"]
                is_cn = any(kw in url.lower() for kw in cn_keywords)
                sources[title] = (url, "CN" if is_cn else "US")
        return sources
    except Exception as e:
        print(f"❌ 读取OPML失败: {e}")
        return {}

SOURCES = parse_opml(OPML_FILE)
EXTRA_SOURCES = {
    # 添加官方 RSS 源（确认有效的）
    "HuggingFace Blog": ("https://huggingface.co/blog/feed.xml", "US"),
    "The Keyword": ("https://blog.google/rss/", "US"),
    # 其他需要手动确认 RSS 地址
}
SOURCES.update(EXTRA_SOURCES)

# ============================================================
# v5.0 研究领域细分 + 学者被引量 (从配置加载)
# ============================================================

# 顶尖AI公司列表
TIER1_AI_COMPANIES = tier1_ai_companies()

# 研究领域细分
RESEARCH_SUBFIELDS = research_subfields()

# 学术顶会权重
TOP_CONFERENCES = top_conferences()

# 学者/机构被引量
HIGH_CITATION_AUTHORS = high_citation_authors()

# 公司官方来源映射
OFFICIAL_SOURCES = official_sources()

def is_official_source(company, source_name):
    official_list = OFFICIAL_SOURCES.get(company.lower(), [])
    return source_name in official_list

# 海外AI公司官方来源
OFFICIAL_COMPANY_SOURCES = [
    "OpenAI News", "Anthropic", "Google DeepMind", "NVIDIA Blog",
    "Meta AI", "Microsoft Research", "HuggingFace Blog", "karpathy",
    "TechCrunch", "The Information", "X",
    "@AnthropicAI", "OpenAI", "Google AI"
]

# ============================================================
# 优先级计算 v2.0 - 按「事件量级 × 来源权威性」
# ============================================================

# ===== 来源权威性 (1-10) =====
SOURCE_AUTHORITY = {
    # Tier 1 - 官方发布 (10)
    "OpenAI News": 10, "Google DeepMind": 10, "Anthropic": 10,
    "NVIDIA Blog": 10, "Meta AI": 10, "Microsoft Research": 10,
    "HuggingFace Blog": 10, "DeepSeek": 10, "Mistral AI": 10,
    "Figure AI": 10, "Physical Intelligence": 10, "World Labs": 10,
    "Thinking Machines Lab": 10, "The Keyword": 10,
    # Tier 1.5 - 顶级分析 (9)
    "SemiAnalysis": 9, "The Information": 9, "Epoch AI": 9,
    # Tier 2 - 一手信源 (7-8)
    "TechCrunch": 8, "Wired": 8, "The Verge": 8, "Ars Technica": 8,
    "36氪": 8,
    # Tier 2.5 - Twitter 官方账号 (7)
    "@openai": 7, "@anthropicai": 7, "@openrouter": 7,
    "@alibaba_qwen": 7, "@kimi_moonshot": 7, "@vllm_project": 7,
    "@googledeepmind": 7, "@googleai": 7, "karpathy": 8,
    # Tier 3 - 行业聚合 (5-6)
    "量子位": 6, "新智元": 6, "机器之心": 6,
    "PaperWeekly": 6, "IT桔子": 5, "Sakana Blog": 6,
    # 默认
    "_default": 5,
}

def get_source_authority(source):
    """获取来源权威性分数 (1-10)"""
    return SOURCE_AUTHORITY.get(source, SOURCE_AUTHORITY["_default"])


# ===== 事件量级判断模式 =====

# 模型前沿 - 事件量级
MODEL_FRONTIER_HIGH = [
    "gpt-5", "o3", "o4", "claude 4", "gemini 3",
    "breakthrough", "首次", "首创", "全新架构", "新范式",
    "state-of-the-art", "sota", "超越", "beat",
]
MODEL_FRONTIER_MEDIUM = [
    "gpt-4.5", "gemini 2", "llama 4", "qwen3", "deepseek v4",
    "发布", "开源", "release", "launch", "unveil",
    "multimodal", "多模态", "reasoning", "推理", "agent",
]

# 算力追踪 - 事件量级
INFRA_HIGH = [
    "gb300", "gb200", "b300", "b200", "blackwell",
    "euv", "high-na", "光刻机", "asml",
    "hbm4", "hbm3e", "hbm3", "存储突破",
    "cowos", "封装产能", "产能突破",
    "capex", "数据中心", "data center",
    "trainium", "inferentia",
]
INFRA_MEDIUM = [
    "h200", "h100", "b100", "gpu", "npu", "tpu",
    "nvidia", "amd", "intel", "tsmc", "台积电",
    "算力", "云计算", "芯片", "chip",
    "三星", "sk海力士", "美光", "micron", "dram",
]

# 研究关注 - 事件量级
RESEARCH_HIGH = [
    "首次提出", "开创性", "全新方法", "新范式", "颠覆性",
    "paradigm shift", "first", "novel", "breakthrough",
]
RESEARCH_MEDIUM = [
    "nature", "science", "neurips", "icml", "cvpr", "iclr", "acl",
    "改进", "优化", "提升", "新方法", "提出",
]

# 产业动态 - 事件量级
INDUSTRY_HIGH = [
    "pmf", "product-market fit",
    "重磅发布", "major release", "flagship",
    "arr", "annual recurring revenue", "月活", "mau", "dau",
    "付费用户", "订阅用户", "revenue",
]
INDUSTRY_MEDIUM = [
    "发布", "上线", "推出", "launch", "release",
    "合作", "战略", "partnership",
    "用户增长", "增长", "growth",
]

# 初创&融资 - 事件量级
FUNDING_HIGH = [
    "agi", "通用人工智能", "具身智能", "embodied", "人形机器人",
    "ai agent", "world model", "世界模型",
    "收购", "acquire", "merger", "并购",
    "十亿", "百亿", "$10b", "$100b",
]
FUNDING_MEDIUM = [
    "融资", "funding", "round",
    "sequoia", "a16z", "红杉", "软银",
    "亿美元", "$100m", "估值",
]

# X讨论 - 事件量级
DISCUSSION_HIGH = [
    "深度分析", "深度", "insight", "analysis",
    "预测", "predict", "判断", "观点",
    "cognition", "cursor", "devin",  # AI编程公司
    "anthropic", "openai", "deepmind", "google ai",  # 头部AI公司
    "x.ai", "sakana",  # 新兴AI公司
]
DISCUSSION_MEDIUM = [
    "paper", "论文", "research", "研究",
    "技术", "technical", "模型", "model",
]


def calculate_event_magnitude(title, summary, category):
    """计算事件量级 (1-10)"""
    text = (title + " " + (summary or "")).lower()

    # 根据分类选择模式
    patterns = {
        "模型前沿": (MODEL_FRONTIER_HIGH, MODEL_FRONTIER_MEDIUM),
        "算力追踪": (INFRA_HIGH, INFRA_MEDIUM),
        "研究关注": (RESEARCH_HIGH, RESEARCH_MEDIUM),
        "产业动态": (INDUSTRY_HIGH, INDUSTRY_MEDIUM),
        "初创&融资": (FUNDING_HIGH, FUNDING_MEDIUM),
        "X讨论": (DISCUSSION_HIGH, DISCUSSION_MEDIUM),
    }

    high_patterns, medium_patterns = patterns.get(category, ([], []))

    if not high_patterns:
        return 5  # 默认中等

    # 匹配高量级模式
    high_count = sum(1 for p in high_patterns if p in text)
    if high_count >= 2:
        return 10
    elif high_count == 1:
        return 8

    # 匹配中量级模式
    medium_count = sum(1 for p in medium_patterns if p in text)
    if medium_count >= 3:
        return 7
    elif medium_count >= 1:
        return 6

    return 4  # 低量级


# ========== 判断研究子领域 ==========
def get_research_subfield(title, summary):
    """判断文章属于哪个研究子领域"""
    text = (title + " " + summary).lower()
    scores = {}

    for field, config in RESEARCH_SUBFIELDS.items():
        score = 0
        # 关键词匹配
        for kw in config["keywords"]:
            if kw.lower() in text:
                score += 3
        # 顶级作者/机构匹配
        for author in config["top_authors"]:
            if author.lower() in text:
                score += 5
        if score > 0:
            scores[field] = score

    if not scores:
        return "其他研究"
    return max(scores.items(), key=lambda x: x[1])[0]

# ============================================================
# 优先级计算 v2.0 - 按「事件量级 × 来源权威性」
# ============================================================

# ===== 来源权威性 (1-10) =====
SOURCE_AUTHORITY = {
    # Tier 1 - 官方发布 (9-10)
    "OpenAI News": 10, "Google DeepMind": 10, "Anthropic": 10,
    "NVIDIA Blog": 10, "Meta AI": 10, "Microsoft Research": 10,
    "HuggingFace Blog": 10, "DeepSeek": 10, "Mistral AI": 10,
    # Tier 1.5 - 顶级分析 (9)
    "SemiAnalysis": 9, "The Information": 9, "Epoch AI": 9,
    # Tier 2 - 一手信源 (7-8)
    "TechCrunch": 8, "Wired": 8, "The Verge": 8, "Ars Technica": 8,
    "36氪": 8,
    # Tier 2.5 - Twitter 官方账号 (7)
    "@openai": 7, "@anthropicai": 7, "@openrouter": 7,
    "@alibaba_qwen": 7, "@kimi_moonshot": 7, "@vllm_project": 7,
    "@googledeepmind": 7, "@googleai": 7,
    # Tier 3 - 行业聚合 (5-6)
    "量子位": 6, "新智元": 6, "机器之心": 6,
    "PaperWeekly": 6, "IT桔子": 5,
    # 默认
    "_default": 5,
}

def get_source_authority(source):
    """获取来源权威性分数 (1-10)"""
    return SOURCE_AUTHORITY.get(source, SOURCE_AUTHORITY["_default"])


# ===== 事件量级判断模式 =====

# 模型前沿 - 事件量级
MODEL_FRONTIER_HIGH = [
    # 下一代模型
    "gpt-5", "o3", "o4", "claude 4", "gemini 3",
    # 重大突破
    "breakthrough", "首次", "首创", "全新架构", "新范式",
    "state-of-the-art", "sota", "超越",
]
MODEL_FRONTIER_MEDIUM = [
    # 重要更新
    "gpt-4.5", "gemini 2", "llama 4", "qwen3", "deepseek v4",
    "发布", "开源", "release", "launch", "unveil",
]

# 算力追踪 - 事件量级
INFRA_HIGH = [
    # 新一代芯片
    "gb300", "gb200", "b300", "b200", "blackwell",
    # 光刻机
    "euv", "high-na euv", "光刻机", "asml",
    # 存储
    "hbm4", "hbm3e", "hbm3", "内存", "memory", "dram",
    "三星存储", "sk海力士", "美光", "micron",
    # 供应链
    "cowos", "封装", "产能", "tsmc", "台积电",
    # 重大 Capex / 芯片工厂
    "capex", "$10b", "$100b", "chip factory", "芯片工厂", "terafab", "fab",
]
INFRA_MEDIUM = [
    # 芯片相关
    "h200", "h100", "b100", "gpu", "npu", "tpu",
    "nvidia", "amd", "intel", "groq",
    # 算力相关
    "算力", "云计算", "数据中心", "data center",
]

# 研究关注 - 事件量级
RESEARCH_HIGH = [
    # 开创性工作
    "首次提出", "开创性", "全新方法", "新范式", "颠覆性",
    "paradigm shift", "first", "novel", "breakthrough",
]
RESEARCH_MEDIUM = [
    # 顶会论文
    "nature", "science", "neurips", "icml", "cvpr", "iclr", "acl",
    # 重要改进
    "改进", "优化", "提升", "新方法", "提出",
]

# 产业动态 - 事件量级
INDUSTRY_HIGH = [
    # PMF 验证
    "pmf", "product-market fit", "找到产品市场匹配",
    # 重要产品
    "重磅发布", "major release", "flagship",
    # 运营数据
    "arr", "annual recurring revenue", "月活", "mau", "dau",
    "付费用户", "订阅用户", "revenue",
]
INDUSTRY_MEDIUM = [
    # 产品发布
    "发布", "上线", "推出", "launch", "release",
    # 合作
    "合作", "战略", "partnership",
    # 用户数据
    "用户增长", "增长", "growth",
]

# 初创&融资 - 事件量级
FUNDING_HIGH = [
    # 前沿领域
    "agi", "通用人工智能", "具身智能", "embodied", "人形机器人",
    "ai agent", "agent", "世界模型", "world model",
    # 重点收购
    "收购", "acquire", "merger", "并购",
    # 大金额
    "十亿", "百亿", "$10b", "$100b", "$1b",
]
FUNDING_MEDIUM = [
    # 融资相关
    "融资", "funding", "round",
    # 投资方
    "sequoia", "a16z", "红杉", "软银",
    # 金额
    "亿美元", "$100m", "估值",
]

# X讨论 - 事件量级
DISCUSSION_HIGH = [
    # 顶级账号关键词
    "深度分析", "深度", "insight", "analysis",
    # 重要观点
    "预测", "predict", "判断", "观点",
]
DISCUSSION_MEDIUM = [
    # 研究相关
    "paper", "论文", "research", "研究",
    # 技术相关
    "技术", "technical", "模型", "model",
]


def calculate_event_magnitude(title, summary, category):
    """计算事件量级 (1-10)"""
    text = (title + " " + (summary or "")).lower()

    # 根据分类选择模式
    if category == "模型前沿":
        high_patterns = MODEL_FRONTIER_HIGH
        medium_patterns = MODEL_FRONTIER_MEDIUM
    elif category == "算力追踪":
        high_patterns = INFRA_HIGH
        medium_patterns = INFRA_MEDIUM
    elif category == "研究关注":
        high_patterns = RESEARCH_HIGH
        medium_patterns = RESEARCH_MEDIUM
    elif category == "产业动态":
        high_patterns = INDUSTRY_HIGH
        medium_patterns = INDUSTRY_MEDIUM
    elif category == "初创&融资":
        high_patterns = FUNDING_HIGH
        medium_patterns = FUNDING_MEDIUM
    elif category == "X讨论":
        high_patterns = DISCUSSION_HIGH
        medium_patterns = DISCUSSION_MEDIUM
    else:
        return 5  # 默认中等

    # 匹配高量级模式
    high_count = sum(1 for p in high_patterns if p in text)
    if high_count >= 2:
        return 9 + min(high_count, 1)  # 9-10
    elif high_count == 1:
        return 8
    # 匹配中量级模式
    medium_count = sum(1 for p in medium_patterns if p in text)
    if medium_count >= 3:
        return 7
    elif medium_count >= 1:
        return 6
    # 默认低量级
    return 4


def calculate_priority_v2(article):
    """计算优先级 v2.0 - 事件量级 × 来源权威性"""
    source = article.get("source", "")
    title = article.get("title", "")
    summary = article.get("summary", "")
    category = article.get("categories", [""])[0] if article.get("categories") else ""
    # 计算两个维度
    source_score = get_source_authority(source)
    event_score = calculate_event_magnitude(title, summary, category)
    # 综合分数 = 事件量级 × 来源权威性
    total = event_score * source_score
    return total


# ============================================================
# 优先级计算 v2.0 - 统一框架
# ============================================================

# 研究关注 - 来源权威性
RESEARCH_SOURCE_AUTHORITY = {
    "Nature": 10, "Science": 10, "Nature Machine Intelligence": 10,
    "NeurIPS": 9, "ICML": 9, "CVPR": 9, "ICLR": 9,
    "PaperWeekly": 7, "机器之心": 7, "量子位": 7,
    "_default": 6,
}

import re


def get_conference_tier(text):
    """识别顶会等级 - 使用模式匹配"""
    text_lower = text.lower()

    # Tier 0 - 顶刊
    if re.search(r'\b(nature|science)\b', text_lower):
        return 1.5

    # Tier 1 - 顶级AI会议（使用简单包含匹配，兼容各种格式如 CVPR26, CVPR'26）
    top_conf = ['neurips', 'nips', 'icml', 'iclr', 'cvpr', 'iccv']
    for conf in top_conf:
        if conf in text_lower:
            return 1.4

    # Tier 2 - 重要会议
    important_conf = ['acl', 'emnlp', 'aaai', 'ijcai', 'conll']
    for conf in important_conf:
        if conf in text_lower:
            return 1.3

    return 1.0


def get_institution_tier(text):
    """识别机构等级 - 使用模式匹配"""
    # Tier 0 - 高被引学者
    high_citation = [
        r'(Hinton|LeCun|Bengio|Goodfellow)',
        r'(Karpathy|Jeff Dean|Demis Hassabis)',
        r'(孙剑|汤晓鸥|朱松纯|唐杰)',
    ]
    for p in high_citation:
        if re.search(p, text, re.I):
            return 1.5

    # Tier 1 - 顶尖机构
    top_institutions = [
        r'\b(Stanford|MIT|Berkeley|CMU|Caltech|Harvard)\b',
        r'\b(Oxford|Cambridge|ETH Zurich|EPFL|Princeton)\b',
        r'(清华|北大|北京大学|清华大学)',
        r'(复旦|浙大|浙江大学|上交|上海交大|中科大)',
        r'(中科院|国科大|中国科学院)',
        r'(Google DeepMind|DeepMind)',
        r'(OpenAI|Anthropic|Meta AI|Microsoft Research)',
    ]
    for p in top_institutions:
        if re.search(p, text):
            return 1.3

    # Tier 2 - 一般学术机构
    if re.search(r'(大学|学院|研究院|实验室|Institute|Lab)', text):
        return 1.1

    return 1.0


def calculate_research_priority_v2(article):
    """计算研究关注优先级 v2.0 - 事件量级 × 来源权威性 × 影响力加成"""
    source = article.get("source", "")
    title = article.get("title", "").lower()
    summary = article.get("summary", "").lower()
    text = title + " " + summary

    # 1. 事件量级
    magnitude = 5  # 默认

    # 量级=10：开创性工作
    paradigm_shift = ["首次提出", "开创性", "全新方法", "新范式", "颠覆性",
                      "paradigm shift", "groundbreaking", "breakthrough"]
    if any(p in text for p in paradigm_shift):
        magnitude = 10
    # 量级=9：顶刊
    elif re.search(r'\b(nature|science|cell|pnas)\b', text):
        magnitude = 9
    # 量级=8：顶会（使用简单匹配，兼容各种格式）
    elif any(c in text for c in ['neurips', 'nips', 'icml', 'iclr', 'cvpr', 'iccv']):
        magnitude = 8
    # 量级=7：重要成果
    elif any(p in text for p in ["best paper", "最佳论文", "sota", "state-of-the-art"]):
        magnitude = 7

    # 2. 来源权威性
    source_score = RESEARCH_SOURCE_AUTHORITY.get(source, RESEARCH_SOURCE_AUTHORITY["_default"])

    # 3. 影响力加成 = 顶会等级 × 机构等级
    conf_tier = get_conference_tier(text)
    inst_tier = get_institution_tier(text)
    bonus = conf_tier * inst_tier

    # 4. 最终分数
    total = magnitude * source_score * bonus
    return total


def calculate_priority_v2(article):
    """计算优先级 v2.0 - 事件量级 × 来源权威性"""
    category = article.get("categories", [""])[0] if article.get("categories") else ""

    # 研究关注使用专门的计算
    if category == "研究关注":
        return calculate_research_priority_v2(article)

    source = article.get("source", "")
    title = article.get("title", "")
    summary = article.get("summary", "")

    source_score = get_source_authority(source)
    event_score = calculate_event_magnitude(title, summary, category)

    return event_score * source_score


# ========== 计算普通优先级 (已废弃，使用 calculate_priority_v2) ==========
def calculate_priority(article, category=None):
    source = article.get("source", "")
    title = article.get("title", "").lower()
    summary = article.get("summary", "").lower()
    text = title + " " + summary

    source_score = SOURCE_WEIGHTS.get(source, 50)

    # 公司权重
    company_score = 0
    for company in TIER1_AI_COMPANIES:
        if company in text:
            if is_official_source(company, source):
                company_score = max(company_score, 55)  # 官方+30
            else:
                company_score = max(company_score, 25)

    keyword_score = 0
    for kw in HIGH_PRIORITY_KEYWORDS:
        if kw.lower() in text:
            keyword_score += 10
    keyword_score = min(keyword_score, 30)

    # 顶尖模型公司发布新模型 -> 额外加分
    top_model_companies = ["openai", "google", "anthropic", "deepmind", "meta", "nvidia"]
    is_top_company = any(c in text for c in top_model_companies)
    is_new_model = any(kw in text for kw in ["embedding", "gemini", "gpt", "claude", "llama", "model", "release", "launch", "发布"])
    if is_top_company and is_new_model:
        keyword_score += 30  # 额外加成

    penalty = 0
    for kw in LOW_PRIORITY_KEYWORDS:
        if kw.lower() in text:
            penalty -= 20

    quality = 0
    if len(summary) > 50: quality += 2
    if re.search(r'\d+[亿万亿]|\d+%', summary): quality += 3

    total = source_score + company_score + keyword_score + penalty + quality
    return total, []

# ========== 事件合并 ==========
# 注意：事件合并已禁用，因为关键词匹配容易导致数据错乱

def merge_events(articles):
    """事件合并 - 禁用状态
    
    原因：关键词匹配会把不相关的新闻错误合并，导致：
    1. link 指向错误来源
    2. body 内容与来源不匹配
    3. LLM 基于错误内容编造事实
    
    如需恢复，使用 URL 精确匹配：
    - 同一 URL 的多来源报道可以合并
    - 不同 URL 即使标题相似也不合并
    """
    # 暂时不做任何合并，直接返回
    return articles

# ============================================================
# 分类和工具函数
# ============================================================
# AI无关内容过滤关键词
NON_AI_KEYWORDS = [
    # 汽车/出行（纯汽车新闻，不含智驾）
    "汽车", "新车", "车型", "车企", "车市", "销量", "奔驰", "宝马", "奥迪", "丰田", "本田", "大众",
    "购车", "4S店",
    # 房地产
    "房价", "房地产", "买房", "卖房", "楼盘", "开发商", "土地", "学区房",
    # 食品/餐饮
    "食品安全", "餐饮", "美食", "餐厅", "外卖", "食品", "饮料",
    # 医疗健康 (非AI医疗)
    "养生", "保健", "药品", "疫苗",
    # 金融投资（纯金融，非AI投资）
    "股市", "基金", "理财", "币圈", "加密货币",
    # 社会新闻/娱乐
    "出轨", "离婚", "明星", "网红", "娱乐", "直播", "翻车", "骨折",
    # 比赛/活动 (非行业会议)
    "世界杯", "比赛", "竞技", "斗蛐蛐", "冠军", "奖金",
    # 36氪日常新闻
    "氪星晚报", "8点1氪", "晚报",
    # 纯硬件/消费电子（和AI无关的）
    "pc shipments", "个人电脑", "笔记本电脑", "手机销量", "智能手表",
    # 纯安全事故（和AI无关）
    "仓库", "fatality",
]

# ============================================================
# 分类系统 v2.0 - 按「主体 + 事件性质」划分
# ============================================================

# ===== 学术实体 =====
ACADEMIC_ENTITIES = [
    # 中文大学
    "大学", "学院", "研究院", "实验室", "中科院", "清华", "北大", "复旦", "浙大",
    "上交", "中科大", "哈工", "北航", "北理", "国科大", "南大", "武大", "华科", "西交",
    # 英文大学
    "stanford", "mit", "berkeley", "cmu", "uiuc", "caltech", "oxford", "cambridge",
]

# ===== 顶会/期刊 =====
TOP_VENUES = [
    "nature", "science", "icml", "neurips", "cvpr", "iclr", "acl", "emnlp", "aaai",
    "arxiv", "论文", "paper",
]

# ===== 模型前沿：模型能力本身 =====
MODEL_PATTERNS = [
    # 具体模型名
    "gpt-4", "gpt-5", "gpt-4o", "gpt-4.5", "o1", "o3", "o4",
    "claude 3", "claude 4", "claude-3", "claude-4",
    "gemini 2", "gemini-2", "gemini 1.5",
    "llama 3", "llama 4", "llama-3", "llama-4",
    "qwen", "deepseek", "mistral", "minimax", "kimi", "grok",
    # 模型架构/技术
    "benchmark", "评测", "sota", "参数", "推理能力",
    "多模态", "视频生成", "图像生成", "文生图", "文生视频",
    "world model", "reasoning", "vla", "agent", "embedding",
    "moe", "transformer", "attention", "diffusion",
    # 模型动作
    "发布模型", "开源模型", "新模型", "模型更新",
    # 编程模型
    "coding model", "编程模型", "代码模型",
    # 语言模型
    "语言模型", "大模型", "llm", "diffusion llm", "扩散语言模型",
]

# ===== 算力追踪：算力硬件 + 基础设施 + Capex + 算力需求 =====
INFRA_PATTERNS = [
    # 算力芯片（chip 要结合上下文，消费电子会被 CONSUMER_ELECTRONICS 排除）
    "gpu", "npu", "tpu", "h100", "h200", "b100", "b200", "blackwell", "gb200", "gb300",
    "算力芯片", "ai芯片", "训练芯片", "推理芯片", "chip",
    # 算力厂商
    "nvidia", "amd", "intel", "groq", "cerebras", "tenstorrent",
    # 云服务/数据中心
    "云计算", "云服务", "云厂商", "数据中心", "data center", "datacenter", "算力中心", "算力工厂",
    "aws", "azure", "gcp", "oracle cloud", "coreweave",
    # SemiAnalysis / Capex
    "semianalysis", "capex", "capital expenditure", "ai capex",
    # 算力需求（注意：不含单独的 token，避免匹配 "AI tokens" 薪酬话题）
    "算力需求", "计算需求", "compute demand",
    "算力缺口", "算力短缺", "gpu shortage", "算力供给", "算力供应",
    "训练算力", "推理算力", "eflops", "exaflops", "petaflops",
    "算力租赁", "gpu rental", "gpu cloud",
    # 供应链
    "tsmc", "台积电", "cowos", "hbm", "封装产能", "芯片产能",
    # 数据中心能源
    "数据中心电力", "数据中心能耗",
]

# ===== 产业动态：商业/产品/合作/政策 =====
INDUSTRY_PATTERNS = [
    # 商业数据
    "用户增长", "营收", "付费用户", "订阅", "dau", "mau",
    # 合作/战略
    "战略合作", "合作伙伴",
    # 高管
    "高管", "ceo", "cto", "离职", "加入", "人事变动",
    # 安全/合规
    "安全事件", "漏洞", "数据泄露", "封禁", "监管", "合规",
    # 产品（非模型类）
    "产品上线", "产品更新", "功能更新",
    # 公司动态
    "裁员", "组织架构", "业务调整",
]

# ===== 初创&融资：融资/收购/IPO =====
FUNDING_PATTERNS = [
    "融资", "funding", "round", "a轮", "b轮", "c轮", "d轮", "pre-ipo",
    "估值", "ipo", "上市", "独角兽",
    "收购", "并购", "acquire", "acquisition", "merger",
]

# ===== X讨论：个人动态 =====
PERSONAL_PATTERNS = [
    "我认为", "我觉得", "interesting", "个人观点",
]

# 消费电子排除（不算算力追踪）
CONSUMER_ELECTRONICS = [
    "手机", "智能手机", "pc出货", "笔记本电脑", "智能手表", "耳机", "平板",
    "phone", "laptop", "smartwatch", "earbuds", "tablet", "consumer electronics",
]

# 兼容旧代码（保留 CATEGORIES 变量名）
CATEGORIES = {
    "模型前沿": MODEL_PATTERNS,
    "算力追踪": INFRA_PATTERNS,
    "产业动态": INDUSTRY_PATTERNS,
    "初创&融资": FUNDING_PATTERNS,
    "研究关注": TOP_VENUES,
}
CATEGORY_PRIORITY = {"模型前沿": 1, "产业动态": 2, "算力追踪": 3, "初创&融资": 4, "研究关注": 5, "X讨论": 6, "其他": 7}

# 研究子领域优先级
SUBFIELD_ORDER = {
    "LLM/大语言模型": 1,
    "推理/思考": 2,
    "多模态": 3,
    "世界模型/具身智能": 4,
    "MLSys/系统": 5,
    "AI4S/科学智能": 6,
    "评测": 7,
    "AI安全/对齐": 8,
    "传统ML": 9,
    "其他研究": 10,
}

MAX_PER_CATEGORY = 8
MIN_ARTICLES = 30

def clean_text(t): return re.sub(r'<[^>]+>', '', t or "").strip() if t else ""
def normalize(t): return re.sub(r'\s+', '', (t or "").lower())

def parse_date(entry):
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        try:
            return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        except Exception: pass
    import email.utils, calendar
    for f in ["published", "updated", "created"]:
        if hasattr(entry, f):
            try:
                p = email.utils.parsedate_tz(getattr(entry, f))
                if p:
                    timestamp = calendar.timegm(p[:9])
                    return datetime.fromtimestamp(timestamp, tz=timezone.utc)
            except Exception: continue
    return None


# 解析推文时间
def parse_tweet_time(published_str):
    """解析推文的 published 字段为 published_parsed 格式"""
    if not published_str:
        return None
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(published_str)
        return [
            dt.year, dt.month, dt.day,
            dt.hour, dt.minute, dt.second,
            dt.weekday(), dt.timetuple().tm_yday, 0
        ]
    except Exception:
        return None
# 播客源（需要过滤）
PODCAST_SOURCES = ["a16z", "simplecast", "podcast", "播客"]

def is_podcast_source(name):
    """判断是否是播客源"""
    name_lower = name.lower()
    return any(p in name_lower for p in PODCAST_SOURCES)

def is_in_window(entry):
    d = parse_date(entry)
    return False if d is None else START_UTC <= d <= END_UTC

def is_ai_related(title, summary, source=""):
    """判断是否与AI相关（包含前沿科技 + 来源判断）"""
    text = (title + " " + (summary or "")).lower()
    source_lower = source.lower().replace("@", "")

    # 如果来源是 AI 公司官方账号，直接认为是 AI 相关
    company_accounts = twitter_company_accounts()
    if any(c in source_lower for c in company_accounts):
        return True

    # AI 相关关键词
    ai_keywords = ["ai", "人工智能", "大模型", "llm", "gpt", "claude", "gemini",
                   "模型", "机器学习", "深度学习", "神经网络", "transformer",
                   "nlp", "cv", "计算机视觉", "语音", "自然语言", "自动驾驶",
                   "agent", "agents", "多模态", "视频生成", "图像生成", "文生图"]

    # 前沿科技（和AI一样属于科技前沿，应保留）
    frontier_keywords = ["quantum", "量子", "brain-computer", "脑机", "bci",
                        "fusion", "核聚变", "核融合", "可控核聚变",
                        "nuclear", "半导体", "芯片", "chip", "gpu", "nvidia",
                        "算力", "数据中心", "data center", "terafab"]

    has_ai = any(kw in text for kw in ai_keywords)
    has_frontier = any(kw in text for kw in frontier_keywords)

    # 检查是否包含非AI关键词
    has_non_ai = any(kw in text for kw in NON_AI_KEYWORDS)

    # 如果有AI关键词或前沿科技，且没有非AI关键词
    if (has_ai or has_frontier) and not has_non_ai:
        return True
    if (has_ai or has_frontier) and has_non_ai:
        ai_count = sum(1 for kw in ai_keywords if kw in text)
        frontier_count = sum(1 for kw in frontier_keywords if kw in text)
        non_ai_count = sum(1 for kw in NON_AI_KEYWORDS if kw in text)
        return (ai_count + frontier_count) > non_ai_count
    return False

def get_cat(title, summary, source=""):
    """分类判断 v2.0 - 按「主体 + 事件性质」划分"""
    text = (title + " " + (summary or "")).lower()

    # ===== 0. 先判断是否AI相关（内容 + 来源）=====
    if not is_ai_related(title, summary, source):
        return ["其他"]

    # ===== 1. 初创&融资：融资事件优先判断 =====
    if any(p in text for p in FUNDING_PATTERNS):
        return ["初创&融资"]

    # ===== 2. 研究关注：学术实体 + 研究内容 =====
    has_academic = any(e in text for e in ACADEMIC_ENTITIES)
    has_venue = any(v in text for v in TOP_VENUES)
    has_research = any(p in text for p in ["论文", "paper", "研究", "提出", "发现", "算法"])

    # 学术机构 + 研究内容 → 研究关注
    if has_academic and (has_venue or has_research):
        return ["研究关注"]

    # ===== 3. 算力追踪：先排除消费电子 =====
    is_consumer_electronics = any(c in text for c in CONSUMER_ELECTRONICS)

    if not is_consumer_electronics:
        has_infra = any(p in text for p in INFRA_PATTERNS)
        if has_infra:
            return ["算力追踪"]

    # ===== 4. 模型前沿：模型能力 =====
    has_model = any(p in text for p in MODEL_PATTERNS)
    if has_model:
        return ["模型前沿"]

    # ===== 5. 产业动态：商业/合作/产品 =====
    has_industry = any(p in text for p in INDUSTRY_PATTERNS)
    if has_industry:
        return ["产业动态"]

    # ===== 6. 默认：产业动态 =====
    return ["产业动态"]

def extract_keywords(title):
    t = clean_text(title).lower()
    stop_words = ["announces", "launches", "introduces", "releases", "updates", "new", "the", "a", "an", "and", "or", "for", "with", "from"]
    words = re.findall(r'\w+', t)
    return set(w for w in words if w not in stop_words and len(w) > 2)

def calc_similarity(title1, title2):
    kw1, kw2 = extract_keywords(title1), extract_keywords(title2)
    if not kw1 or not kw2: return 0
    intersection = len(kw1 & kw2)
    union = len(kw1 | kw2)
    return intersection / union if union > 0 else 0

def _extract_product_entities(title):
    """从标题中提取「公司+产品」实体对，用于跨天去重。"""
    # 公司名映射（英文→标准名）
    company_map = {
        "OpenAI": "OpenAI", "GPT": "OpenAI", "Codex": "OpenAI", "ChatGPT": "OpenAI",
        "Google": "Google", "Gemini": "Google", "TPU": "Google", "Gemma": "Google",
        "Anthropic": "Anthropic", "Claude": "Anthropic",
        "NVIDIA": "NVIDIA",
        "Meta": "Meta", "Llama": "Meta",
        "DeepSeek": "DeepSeek",
        "xAI": "xAI", "Grok": "xAI",
        "Apple": "Apple",
        "阿里": "阿里", "Qwen": "阿里", "通义": "阿里",
        "腾讯": "腾讯", "混元": "腾讯", "Hunyuan": "腾讯", "Hy3": "腾讯",
        "字节": "字节", "ByteDance": "字节",
        "月之暗面": "月之暗面", "Kimi": "月之暗面", "Moonshot": "月之暗面",
        "复旦": "复旦",
        "SemiAnalysis": "SemiAnalysis",
    }
    # 产品名模式：版本号（GPT-5.5, Qwen3.6, V4）
    product_pattern = re.compile(
        r'(GPT[\s\-]?\d+(?:\.\d+)?)'
        r'|(Claude[\s\-]?\w*)'
        r'|(Gemini[\s\-]?\d+(?:\.\d+)?)'
        r'|(Qwen[\s\-]?\d+(?:\.\d+)?)'
        r'|(DeepSeek[\s\-]?\w*(?:\d+)?)'
        r'|(Hy[\d][\-\w]*)'
        r'|(Kimi[\s\-]?\w*(?:\d+(?:\.\d+)?)?)'
        r'|(TPU[\s\-]?\w*\d+)'
        r'|(Grok[\s\-]?\w*)',
        re.IGNORECASE
    )
    companies = set()
    for name, standard in company_map.items():
        if name in title:
            companies.add(standard)

    products = set()
    for m in product_pattern.finditer(title):
        products.add(m.group(0).replace(" ", "").replace("－", "-"))

    # 返回 (company, product) 组合列表
    result = []
    for c in companies:
        for p in products:
            result.append((c, p))
    # 如果只有公司没有产品，也返回
    if not products and companies:
        for c in companies:
            result.append((c, ""))
    return result


def _load_recent_tweet_links(days=3):
    """从近几天的 twitter preview 文件中提取 tweet URL，用于推文级去重"""
    seen = set()
    base = os.path.dirname(ARCHIVE_DIR)  # archive 的父目录
    for i in range(1, days + 1):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        tp_file = os.path.join(base, f"twitter-preview-{date}.md")
        if os.path.exists(tp_file):
            try:
                with open(tp_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        for m in re.finditer(r'https://x\.com/\S+/status/(\d+)', line):
                            url = m.group(0).rstrip("/").split("#")[0]
                            seen.add(url)
            except Exception:
                pass
    return seen


def dedup_articles(articles):
    """跨天去重：URL 精确匹配 + 推文去重 + 实体匹配 + 标题语义去重"""
    try:
        recent = load_recent_archives(days=3)
        seen_links = {a.get("link", "").rstrip("/").split("#")[0] for a in recent if a.get("link")}
        recent_titles = [a.get("title", "") for a in recent if a.get("title")]
    except Exception:
        seen_links = set()
        recent_titles = []

    # 补充推文去重：从 twitter preview 文件中提取已抓取的 tweet URL
    seen_links.update(_load_recent_tweet_links(days=3))

    # 预计算近3天标题的实体对
    recent_entities = set()
    for rt in recent_titles:
        for pair in _extract_product_entities(rt):
            recent_entities.add(pair)

    filtered = []
    for a in articles:
        link = a.get("link", "").rstrip("/").split("#")[0]
        title = a.get("title", "")

        # 1. URL 精确匹配
        if link and link in seen_links:
            print(f"   [跨天去重-URL] '{title[:40]}...' 已在前几天发布，跳过")
            continue

        # 2. 实体匹配：同公司+同产品 → 重复
        entities = _extract_product_entities(title)
        entity_dup = False
        for company, product in entities:
            if product and (company, product) in recent_entities:
                print(f"   [跨天去重-实体] '{title[:40]}...' ({company}+{product}) 已报过，跳过")
                entity_dup = True
                break
        if entity_dup:
            continue

        # 3. 标题语义去重
        is_dup = False
        for rt in recent_titles:
            if title_similarity(title, rt) >= 0.45:
                print(f"   [跨天去重-语义] '{title[:40]}...' ~ '{rt[:40]}...', 跳过")
                is_dup = True
                break
        if is_dup:
            continue

        filtered.append(a)
    return filtered

# ========== LLM ==========
def call_llm(prompt):
    if not API_KEY:
        return None
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    # 从 feedback.md 加载最近的修正作为 few-shot 示例
    _fb_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback.md")
    _feedback_examples = ""
    try:
        _examples = []
        _entry = {}
        for _line in open(_fb_path, encoding="utf-8"):
            _line = _line.strip()
            if _line.startswith("### ["):
                if _entry.get("before") and _entry.get("after"):
                    _examples.append(_entry)
                _entry = {}
            elif _line.startswith("- **field**:"):
                _entry["field"] = _line.replace("- **field**:", "").strip()
            elif _line.startswith("- **before**:"):
                _entry["before"] = _line.replace("- **before**:", "").strip()
            elif _line.startswith("- **after**:"):
                _entry["after"] = _line.replace("- **after**:", "").strip()
            elif _line.startswith("- **reason**:"):
                _entry["reason"] = _line.replace("- **reason**:", "").strip()
        if _entry.get("before") and _entry.get("after"):
            _examples.append(_entry)
        # 只取最近5条有效示例
        _examples = [e for e in _examples if len(e.get("before", "")) > 5 and len(e.get("after", "")) > 5][-5:]
        if _examples:
            _lines = ["\n## 过往修正示例（不要犯同样的错）"]
            for _i, _e in enumerate(_examples, 1):
                _lines.append(f"\n### 示例{_i}（{_e.get('field', 'unknown')}）")
                _lines.append(f"- 错误: {_e['before'][:200]}")
                _lines.append(f"- 正确: {_e['after'][:200]}")
                if _e.get("reason"):
                    _lines.append(f"- 原因: {_e['reason'][:100]}")
            _feedback_examples = "\n".join(_lines)
    except FileNotFoundError:
        pass

    # 从外部文件加载 system prompt（自进化：修改 prompts/news_processor.md 即可）
    _prompt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts", "news_processor.md")
    try:
        with open(_prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read().strip() + _feedback_examples
    except FileNotFoundError:
        # fallback: 如果 prompt 文件不存在，使用空 prompt 避免崩溃
        print(f"   ⚠️ Prompt 文件不存在: {_prompt_path}")
        return None

    data = {
        "model": "MiniMax-M2.5", "temperature": 0.2,
        "max_tokens": 8000,
        "system": system_prompt,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        r = httpx.post(API_URL, headers=headers, json=data, timeout=120, verify=False)
        r.raise_for_status()
        result = r.json()
        if result.get("content"):
            for item in result["content"]:
                if item.get("type") == "text":
                    return item.get("text", "")
        return None
    except Exception as e:
        print(f"⚠️ LLM调用失败: {e}")
        return None

import re
def process_with_llm(articles, recent_articles=None):
    import re
    if recent_articles is None:
        recent_articles = []
    if not API_KEY or len(articles) < 5:
        return articles

    # 构建历史动态摘要
    recent_summary = ""
    if recent_articles:
        recent_titles = [a["title"][:40] for a in recent_articles[-15:]]
        recent_summary = f"\
\
## 近期动态(供参考关联)\
" + "\
".join([f"- {t}" for t in recent_titles])

    # 按优先级排序，确保重要新闻优先处理
    sorted_articles = sorted(articles, key=lambda x: x.get('priority', 0), reverse=True)

    # 预过滤：排除明显非AI内容（Tesla财报、NASA、Rivian等）
    NON_AI_TITLE_KEYWORDS = [
        "tesla q", "rivian", "nasa ", "apple watch", "iphone case",
        "linkedin's ceo", "threads is adding", "startup battlefield",
        "cosmetics giant", "data breach", "rituals confirms",
        "养虾", "招聘", "内推",
    ]
    def is_likely_non_ai(a):
        title_lower = a.get('title', '').lower()
        return any(kw in title_lower for kw in NON_AI_TITLE_KEYWORDS)

    ai_filtered = [a for a in sorted_articles if not is_likely_non_ai(a)]

    # 每个来源最多保留N条，避免单一源占满名额
    from collections import Counter
    src_count = Counter()
    diversified = []
    for a in ai_filtered:
        src = a.get('source', '')
        limit = 6 if src == "TechCrunch" else 3
        if src_count[src] < limit:
            diversified.append(a)
            src_count[src] += 1

    # 构建清晰的新闻列表，每条独立
    news_list = []
    for i, a in enumerate(diversified[:40]):  # 取前40条AI相关新闻
        summary = a.get('summary', '') or a.get('content', '')
        news_list.append(f"""【新闻{i+1}】
标题：{a['title']}
来源：{a['source']}
摘要：{summary[:300]}""")
    
    prompt = """请严格按照下方新闻进行处理。

## 输出格式要求
只返回is_ai_related=true的新闻，JSON数组格式：
[
  {
    "original_title": "原始标题（必须和输入完全一致）",
    "title": "中文标题，事件主体+做什么+为什么重要，禁止感叹号/问号结尾",
    "body": "建议3-6句话，只写关键事实：是什么、关键数据、突破/创新、关联事件、事实性影响（市场反应/行业变化/专家评价）。信息不足时宁可2句也不编造。禁止AI自己的判断和引申（判断放insight）",
    "insight": "一句话务实判断：具体趋势、竞争动态或实际影响。禁止空洞宏大叙事",
    "category": "分类"
  }
]

## body分类侧重点
- 模型前沿：能力突破点、关键数据（成本、benchmark）、适用场景
- 算力追踪：规模（芯片型号、数量）、产能、成本变化、供应链影响
- 研究关注：方法创新点、实验结果、局限性
- 产业动态：具体发生了什么、涉及哪些人/产品、影响范围
- 初创&融资：领域、商业逻辑、金额，投资方背书
- X讨论：观点核心、论据

## insight分类侧重点
- 模型前沿：技术代差、具体商业影响
- 算力追踪：供需关系、格局变化
- 研究关注：创新性、对后续研究/应用的实际影响
- 产业动态：市场影响、竞争定位
- 初创&融资：商业逻辑、团队或项目亮点
- X讨论：观点质量、值得关注程度

## 串联要求
- 如果多条新闻属于同一故事的不同面（如：同一公司的多个动作、同一赛道的多个玩家），在body中简要关联
- 参考下方"近期动态"，如果今天的事件是某条近期的延续/升级，简要说明变化
- insight不要重复body已说的事实，而是给出独立的判断
""" + ("\n\n" + recent_summary if recent_summary else "") + "\n\n## 今日新闻\n\n" + "\n\n".join(news_list)
    result = call_llm(prompt)
    if not result:
        return articles
    try:
        import json as json_module
        import re as re_module

        def clean_json_string(s):
            """清理 JSON 字符串中的问题字符"""
            # 移除控制字符（除了 \n \r \t）
            s = re_module.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', s)
            # 修复未转义的引号（在字符串值内）
            # 修复未转义的反斜杠
            s = s.replace('\\', '\\\\').replace('\\\\\\\\', '\\\\')
            # 移除 markdown 代码块
            s = re_module.sub(r'^```json\s*', '', s)
            s = re_module.sub(r'^```\s*', '', s)
            s = re_module.sub(r'\s*```$', '', s)
            return s.strip()

        # 尝试多种方式解析JSON
        json_match = re_module.search(r'\[[\s\S]*\]', result)
        llm_results = None
        if json_match:
            raw = json_match.group()
            raw = clean_json_string(raw)

            # 尝试直接解析
            try:
                llm_results = json_module.loads(raw)
            except Exception as e1:
                # 尝试修复常见问题
                try:
                    # 移除多余逗号
                    raw_fixed = re_module.sub(r',(\s*[\]\}])', r'\1', raw)
                    llm_results = json_module.loads(raw_fixed)
                except Exception as e2:
                    # 尝试逐个对象解析
                    try:
                        objects = re_module.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', raw)
                        llm_results = []
                        for obj in objects:
                            try:
                                llm_results.append(json_module.loads(obj))
                            except Exception:
                                pass
                        if not llm_results:
                            print(f"   ⚠️ JSON解析失败: {e1}")
                            return articles
                    except Exception as e3:
                        print(f"   ⚠️ JSON解析失败: {e1}, {e3}")
                        return articles
            # 建立原始标题到文章的映射
            title_to_article = {}
            for a in articles:
                orig_title = a.get('title', '')
                if orig_title:
                    title_to_article[orig_title] = a

            filtered_articles = []
            for lr in llm_results:
                # 通过原始标题匹配文章
                original_title = lr.get('original_title', '')
                article = title_to_article.get(original_title)

                if not article:
                    # 尝试模糊匹配
                    for t, a in title_to_article.items():
                        if original_title[:30] in t or t[:30] in original_title:
                            article = a
                            break

                if not article:
                    continue

                orig_summary = article.get('summary', '')

                # 使用 LLM 生成的标题
                llm_title = lr.get('title', '')
                if llm_title and len(llm_title) > 5:
                    article['title'] = llm_title[:80]

                # 使用 LLM 判断的分类
                llm_cat = lr.get('category', '')
                if llm_cat:
                    article['categories'] = [llm_cat]

                # 使用 LLM 生成的 body
                llm_body = lr.get('body', '')
                if llm_body and len(llm_body) > 10:
                    article['body'] = llm_body[:400]
                else:
                    article['body'] = orig_summary[:150] if orig_summary else article['title']

                # 使用 LLM 生成的 insight（一句话点评）
                llm_insight = lr.get('insight', '')
                if llm_insight:
                    article['insight'] = llm_insight[:150]

                filtered_articles.append(article)
            
            articles = filtered_articles
            print(f"✅ LLM处理了 {len(llm_results)} 条新闻，过滤后 {len(articles)} 条")
    except Exception as e:
        print(f"⚠️ 解析LLM结果失败: {e}")
    return articles

# ========== 论文自动溯源 + Body 校验 ==========
_ARXIV_CACHE = {}

def _fetch_arxiv(arxiv_id):
    """从 arXiv 获取论文 abstract"""
    if arxiv_id in _ARXIV_CACHE:
        return _ARXIV_CACHE[arxiv_id]
    try:
        import urllib.request
        url = f"https://arxiv.org/abs/{arxiv_id}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode("utf-8")
        title = re.findall(r'<meta name="citation_title" content="([^"]+)"', html)
        abstract = re.findall(r'<blockquote class="abstract mathjax">\s*<span class="descriptor">Abstract:</span>\s*(.*?)</blockquote>', html, re.DOTALL)
        result = {}
        if title: result["title"] = title[0]
        if abstract:
            text = re.sub(r'<[^>]*>', '', abstract[0]).strip()
            result["abstract"] = re.sub(r'\s+', ' ', text)[:1200]
        _ARXIV_CACHE[arxiv_id] = result
        return result
    except Exception:
        return None

def _find_arxiv_id(article):
    """从文章 link/body/title 中提取 arXiv 编号"""
    for field in [article.get("link", ""), article.get("body", ""), article.get("title", "")]:
        m = re.search(r'(\d{4}\.\d{4,5})', field)
        if m and "arxiv" in field.lower():
            return m.group(1)
    return None

def _count_sentences(text):
    """计算中英文句数"""
    if not text:
        return 0
    sentences = re.split(r'[。.!?！？]', text)
    return len([s for s in sentences if s.strip()])

def _has_quantifiable_data(text):
    """检查是否有可量化数据"""
    if not text:
        return False
    return bool(re.search(r'\d+\.?\d*%|\$\d+|\d+x|\d+倍|\d+亿|\d+万|\d{2,}B|\d{2,}M', text))

def post_validate_and_enrich(articles):
    """后处理：轻量校验，主要补充逻辑由 QA autofix 完成"""
    warnings = []
    for a in articles:
        title_short = a.get("title", "")[:40]
        body = a.get("body", "")
        sent_count = _count_sentences(body)
        if sent_count < 3:
            warnings.append(f"[{title_short}] body仅{sent_count}句")
    if warnings:
        for w in warnings:
            print(f"   ⚠️ {w}")
        print(f"   📋 后处理校验: {len(warnings)} 个待补充（将由QA autofix处理）")
    else:
        print(f"   ✅ 后处理校验: 全部通过")
    return articles

# ========== 抓取 ==========
def fetch_source(name, url, limit=15, max_retries=5):
    """抓取 RSS 源，支持重试"""
    for attempt in range(max_retries):
        try:
            client = httpx.Client(timeout=15, verify=False, follow_redirects=True)
            r = client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            feed = feedparser.parse(r.text)
            articles = []
            for e in feed.entries:
                if not is_in_window(e): continue
                title = clean_text(e.get("title", ""))
                link = e.get("link", "")
                summary = clean_text(e.get("summary") or e.get("description") or "")
                if not title or len(title) < 5: continue
                cats = get_cat(title, summary)
                primary_cat = cats[0]

                article = {
                    "title": title,
                    "summary": summary[:150] if summary else "",
                    "content": summary,
                    "link": link,
                    "categories": cats,
                    "source": name,
                    "published_parsed": list(e.get("published_parsed"))[:6] if e.get("published_parsed") else None,
                }

                # 使用新的优先级计算 v2.0
                article["priority"] = calculate_priority_v2(article)

                articles.append(article)
                if len(articles) >= limit: break
            client.close()
            return articles, None
        except Exception as e:
            if attempt < max_retries - 1:
                import time
                time.sleep(2)  # 重试前等待2秒
                continue
            return [], str(e)[:60]

# ========== 生成报告 ==========
def generate_report(articles):
    month_day = END_BJ.strftime("%m月%d日")
    by_cat = defaultdict(list)
    for a in articles:
        for c in a["categories"]: by_cat[c].append(a)

    # 分类内排序
    for cat in by_cat:
        # 全部按优先级排序
        by_cat[cat] = sorted(by_cat[cat], key=lambda x: x.get("priority", 0), reverse=True)[:MAX_PER_CATEGORY]

    merged_count = sum(1 for a in articles if a.get("is_merged"))

    # 计算时间窗口
    time_diff = END_BJ - START_BJ
    hours = int(time_diff.total_seconds() / 3600)

    # 简洁头部
    lines = [f"## {month_day} AI 前沿动态", "",
             f"> 自动汇总 | 时间窗口: {hours}h | 每类 Top 5", "",
             "---", "",
             "## 要点汇总", ""]

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        items = by_cat.get(cat, [])
        if items:
            # 要点速览：使用完整标题，不截断
            titles = "; ".join([a['title'] for a in items[:5]])
            lines.append(f"- {cat}：{titles}")

    lines.extend(["", "---", "", "## 📖 详细参考", ""])

    # 模型前沿
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资"]:
        items = by_cat.get(cat, [])
        if not items: continue
        lines.append(f"### {cat}")
        for a in items:
            priority = a.get("priority", 0)
            priority_emoji = "🔥" if priority > 150 else "📰" if priority > 100 else "📄"

            if a.get("is_merged"):
                sources_str = " | ".join(a.get("merged_sources", []))
                link = a.get("link", "")
                if link:
                    source_line = f"   - 来源: [{sources_str}]({link}) ({a.get('source_count')}源合并)"
                else:
                    source_line = f"   - 来源: {sources_str} ({a.get('source_count')}源合并)"
            else:
                link = a.get("link", "")
                if link:
                    source_line = f"   - 来源: [{a['source']}]({link})"
                else:
                    source_line = f"   - 来源: {a['source']}"

            lines.append(f"**{a['title']}**")
            # 正文
            if a.get('body'):
                lines.append(f"- {a['body']}")
            # 一句话点评
            if a.get('insight'):
                lines.append(f"  > 💡 {a['insight']}")
            lines.append(source_line)
            lines.append("")

    # 研究关注 (按优先级排序，不分组)
    research_items = by_cat.get("研究关注", [])
    if research_items:
        lines.append("### 研究关注")
        for a in research_items:
            priority = a.get("priority", 0)
            priority_emoji = "🔥" if priority > 150 else "📰" if priority > 100 else "📄"
            link = a.get("link", "")
            if link:
                source_line = f"   - 来源: [{a['source']}]({link})"
            else:
                source_line = f"   - 来源: {a['source']}"
            lines.append(f"**{a['title']}**")
            # 正文
            if a.get('body'):
                lines.append(f"- {a['body']}")
            # 一句话点评
            if a.get('insight'):
                lines.append(f"  > 💡 {a['insight']}")
            lines.append(source_line)
            lines.append("")

    # X讨论 (按优先级排序)
    x_items = by_cat.get("X讨论", [])
    if x_items:
        lines.append("### X讨论")
        for a in x_items:
            link = a.get("link", "")
            if link:
                source_line = f"   - 来源: [{a['source']}]({link})"
            else:
                source_line = f"   - 来源: {a['source']}"

            lines.append(f"**{a['title']}**")
            if a.get('body'):
                lines.append(f"- {a['body']}")
            if a.get('insight'):
                lines.append(f"  > 💡 {a['insight']}")
            lines.append(source_line)
            lines.append("")

    lines.extend(["", "---", f"*更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*"])
    return "\n".join(lines)


def _log_quality(articles):
    """每次运行后记录质量元数据到 quality_log.jsonl（自进化数据源）"""
    from collections import Counter
    log_path = os.path.join(ARCHIVE_DIR, "..", "quality_log.jsonl")
    log_path = os.path.normpath(log_path)

    cat_counts = Counter()
    body_lens = []
    insight_count = 0
    for a in articles:
        cats = a.get("categories", [])
        if cats:
            cat_counts[cats[0]] += 1
        body = a.get("body", "") or a.get("summary", "")
        if body:
            body_lens.append(len(body))
        if a.get("insight"):
            insight_count += 1

    entry = {
        "date": END_BJ.strftime("%Y-%m-%d"),
        "total": len(articles),
        "categories": dict(cat_counts),
        "body_avg_len": round(sum(body_lens) / len(body_lens), 1) if body_lens else 0,
        "insight_count": insight_count,
        "insight_ratio": round(insight_count / len(articles), 2) if articles else 0,
        "prompt_hash": _prompt_hash(),
    }

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _prompt_hash():
    """记录当前 prompt 文件的哈希，用于追踪哪版 prompt 产出了什么质量"""
    import hashlib
    prompt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts", "news_processor.md")
    try:
        content = open(prompt_path, "r", encoding="utf-8").read()
        return hashlib.md5(content.encode()).hexdigest()[:8]
    except FileNotFoundError:
        return "missing"


def _check_feedback():
    """管线启动时检查 feedback.md 是否有未处理的新修正，打印提醒。"""
    feedback_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback.md")
    state_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".feedback_state.json")

    if not os.path.exists(feedback_path):
        return

    # 解析 feedback.md 中所有 ### 条目
    entries = []
    current = {}
    for line in open(feedback_path, "r", encoding="utf-8"):
        m = re.match(r'^### \[([\d-]+)\] #(\d+)', line)
        if m:
            if current:
                entries.append(current)
            current = {"date": m.group(1), "num": int(m.group(2)), "hints": []}
        hm = re.match(r'^- \*\*rule_hint\*\*: (.+)', line)
        if hm and current:
            current["hints"].append(hm.group(1).strip())
    if current:
        entries.append(current)

    if not entries:
        return

    # 读取上次已处理的条目数
    last_seen = 0
    if os.path.exists(state_path):
        try:
            with open(state_path, "r") as f:
                last_seen = json.load(f).get("last_seen_count", 0)
        except (json.JSONDecodeError, OSError):
            pass

    new_count = len(entries) - last_seen
    if new_count <= 0:
        return

    # 有新修正，打印提醒
    print(f"📋 feedback.md 有 {new_count} 条新修正（总计 {len(entries)} 条）:")
    for entry in entries[last_seen:]:
        label = f"  #{entry['num']} [{entry['date']}]"
        for h in entry["hints"]:
            print(f"{label} → {h}")
            label = "            "
    print(f"   提示: 审视 rule_hint 是否需要反映到 prompts/news_processor.md")
    print()


def _mark_feedback_seen():
    """管线成功完成后标记所有 feedback 条目为已处理。"""
    feedback_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "feedback.md")
    state_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".feedback_state.json")
    if not os.path.exists(feedback_path):
        return
    count = sum(1 for line in open(feedback_path, "r", encoding="utf-8")
                if re.match(r'^### \[', line))
    with open(state_path, "w") as f:
        json.dump({"last_seen_count": count}, f)


def save_archive(articles):
    # 使用 END_BJ（窗口结束日期）命名存档，与 run.sh skip 检查一致
    date_str = END_BJ.strftime("%Y-%m-%d")
    archive_file = os.path.join(ARCHIVE_DIR, f"news_{date_str}.json")
    data = {"date": date_str, "count": len(articles), "articles": articles}
    with open(archive_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 已存档: {archive_file}")

def get_time_window(target_date=None):
    """获取时间窗口：固定 24 小时（昨天9点 → 今天9点）

    Args:
        target_date: 指定日期，格式 YYYY-MM-DD。默认为今天。
    """
    beijing_offset = 8

    if target_date:
        # 使用指定日期（带时区）
        end_beijing = datetime.strptime(target_date, "%Y-%m-%d").replace(
            hour=9, minute=0, second=0, microsecond=0, tzinfo=timezone(timedelta(hours=beijing_offset))
        )
    else:
        # 使用当前时间
        now_utc = datetime.now(timezone.utc)
        now_beijing = now_utc + timedelta(hours=beijing_offset)
        # end_beijing = 今天9点（如果还没到9点）或昨天9点（如果已过9点）
        end_beijing = now_beijing.replace(hour=9, minute=0, second=0, microsecond=0)
        if now_beijing.hour >= 9:
            end_beijing = end_beijing + timedelta(days=1)

    # 固定：24小时窗口
    start_beijing = end_beijing - timedelta(days=1)

    return start_beijing - timedelta(hours=8), end_beijing - timedelta(hours=8), start_beijing, end_beijing

# 默认时间窗口（今天）
START_UTC, END_UTC, START_BJ, END_BJ = get_time_window()

# ========== MD to HTML (委托给 html_generator 模块) ==========
def md_to_html_from_file(md_file=None, output_html=None):
    """从 MD 文件生成 HTML"""
    if md_file is None:
        md_file = output_md()
    if output_html is None:
        output_html = output_html_path()

    if not os.path.exists(md_file):
        print(f"❌ MD 文件不存在: {md_file}")
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    dated_html = f"{base_dir()}/daily-ai-news-{date_str}.html"
    md_to_html(md_file, output_html, dated_html=dated_html)

# ========== 主函数 ==========
def load_recent_archives(days=3):
    """读取近期存档用于关联分析和跨天去重"""
    recent_news = []
    for i in range(1, days+1):
        date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        archive_file = os.path.join(ARCHIVE_DIR, f"news_{date}.json")
        if os.path.exists(archive_file):
            try:
                with open(archive_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for a in data.get("articles", []):
                        recent_news.append({
                            "title": a.get("title", ""),
                            "link": a.get("link", ""),
                            "category": a.get("categories", [""])[0] if a.get("categories") else ""
                        })
            except Exception as e:
                print(f"   ⚠️ 读取存档失败: {e}")
    return recent_news

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='AI 前沿动态日报')
    parser.add_argument('--cache', action='store_true', help='抓取后保存到缓存文件')
    parser.add_argument('--from-cache', action='store_true', help='从缓存文件读取，跳过抓取')
    parser.add_argument('--skip-llm', action='store_true', help='跳过 LLM 处理')
    parser.add_argument('--limit', type=int, default=0, help='限制处理条数（用于快速测试）')
    parser.add_argument('--date', type=str, default=None, help='指定日期 YYYY-MM-DD')
    parser.add_argument('--md', action='store_true', help='从 MD 文件生成 HTML（用于手动编辑后的发布）')
    parser.add_argument('--no-overwrite', action='store_true', help='不覆盖已存在的 daily-ai-news.md（保留手动编辑）')
    args = parser.parse_args()

    # 从 MD 生成 HTML（独立模式）
    if args.md:
        md_to_html_from_file()
        return

    # 使用指定日期重新计算时间窗口
    global START_UTC, END_UTC, START_BJ, END_BJ, OUTPUT_FILE
    if args.date:
        START_UTC, END_UTC, START_BJ, END_BJ = get_time_window(args.date)
        OUTPUT_FILE = output_md(args.date)

    print(f"🤖 AI前沿动态 v5.1")
    print(f"   时间窗口: {START_BJ.strftime('%Y-%m-%d %H:%M')} - {END_BJ.strftime('%Y-%m-%d %H:%M')} 北京时间")

    # 检查是否有未处理的 feedback 修正
    _check_feedback()

    if args.from_cache:
        print(f"   模式: 从缓存读取")
    elif args.cache:
        print(f"   模式: 抓取并缓存")

    # 从配置加载账号列表
    COMPANY_ACCOUNTS = twitter_company_accounts()
    RESEARCHER_ACCOUNTS = twitter_researcher_accounts()

    all_arts, errors = [], []

    # 从缓存读取 或 重新抓取
    if args.from_cache:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cached = json.load(f)
                all_arts = cached.get('articles', [])
                errors = cached.get('errors', [])
            print(f"📦 从缓存读取: {len(all_arts)} 条")
            # 过滤超出时间窗口的文章
            before_count = len(all_arts)
            all_arts = [a for a in all_arts if is_in_window(a)]
            if len(all_arts) < before_count:
                print(f"   ⏰ 时间窗口过滤: {before_count} → {len(all_arts)} 条（移除 {before_count - len(all_arts)} 条过期）")
        else:
            print(f"❌ 缓存文件不存在: {CACHE_FILE}")
            return
    else:
        # 抓取 RSS
        for name, (url, tz) in SOURCES.items():
            if is_podcast_source(name):
                continue
            print(f"  📡 {name}...", end=" ", flush=True)
            arts, err = fetch_source(name, url)
            if err:
                print("❌")
                errors.append(f"{name}: {err}")
            else:
                print(f"✅ {len(arts)}")
                all_arts.extend(arts)

        # 抓取研究者推文
        print("📡 抓取研究者动态...")
        researcher_tweets = fetch_researcher_tweets()
        if researcher_tweets:
            print(f"   获取 {len(researcher_tweets)} 条推文")

            # 预分类关键词
            MODEL_KW = ["model", "发布", "release", "launch", "benchmark", "sota",
                        "gpt", "claude", "gemini", "llama", "qwen", "mistral",
                        "开源", "open source", "open-weight", "参数", "parameter",
                        "性能", "performance", "outperform", "超越",
                        "multimodal", "多模态", "vision", "image", "video",
                        "reasoning", "推理", "coding", "agent"]
            COMPUTE_KW = ["gpu", "tpu", "chip", "芯片", "trainium", "inferentia",
                         "inference", "推理加速", "serving", "vllm",
                         "datacenter", "数据中心", "capex", "算力"]
            RESEARCH_KW = ["paper", "论文", "arxiv", "iclr", "neurips", "icml",
                          "method", "方法", "propose", "提出", "improve", "改进"]
            FUNDING_KW = ["funding", "融资", "round", "raise", "valuation", "估值",
                         "acquire", "收购", "$"]

            company_accounts_lower = {c.lower() for c in COMPANY_ACCOUNTS}

            for t in researcher_tweets:
                source = t.get("source", "")
                title = t.get("title", "")
                source_lower = source.lower().replace("@", "")

                # 公司账号和研究账号：根据内容预分类
                text_lower = title.lower()
                if sum(1 for kw in COMPUTE_KW if kw.lower() in text_lower) >= 1:
                    cat = "算力追踪"
                elif sum(1 for kw in MODEL_KW if kw.lower() in text_lower) >= 2:
                    cat = "模型前沿"
                elif sum(1 for kw in FUNDING_KW if kw.lower() in text_lower) >= 1:
                    cat = "初创&融资"
                elif sum(1 for kw in RESEARCH_KW if kw.lower() in text_lower) >= 1:
                    cat = "研究关注"
                elif source_lower in company_accounts_lower:
                    cat = "产业动态"
                else:
                    cat = "X讨论"

                # 使用匹配的分类计算优先级
                priority = calculate_priority_v2({
                    "source": source,
                    "title": title,
                    "summary": title,
                    "categories": [cat]
                })
                # 推文优先级 boost，确保进入 LLM 处理
                priority += 15

                all_arts.append({
                    "title": title[:80],
                    "summary": title,
                    "content": title,
                    "link": t.get("link", ""),
                    "categories": [cat],
                    "is_tweet": True,
                    "source": t.get("source", ""),
                    "published_parsed": parse_tweet_time(t.get("published", "")),
                    "priority": priority,
                })

        # 保存缓存
        if args.cache:
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump({'articles': all_arts, 'errors': errors, 'time': datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
            print(f"💾 已缓存到: {CACHE_FILE}")

    # 去重和合并
    unique = dedup_articles(all_arts)
    print(f"📊 去重后: {len(unique)} 条")

    merged = merge_events(unique)
    print(f"📊 合并后: {len(merged)} 条")

    # 限制条数（用于快速测试）
    if args.limit > 0:
        merged = merged[:args.limit]
        print(f"🔬 限制测试: {len(merged)} 条")

    merged = sorted(merged, key=lambda x: x.get("priority", 0), reverse=True)

    # 预规范化
    print("🔧 预规范化...")
    merged = improve_news(merged, do_filter=True)

    # LLM 处理
    if not args.skip_llm and API_KEY and len(merged) > 5:
        print("📚 读取近期存档...")
        recent_articles = load_recent_archives(days=3)
        print(f"🤖 调用LLM处理...")
        merged = process_with_llm(merged, recent_articles)
    elif args.skip_llm:
        print("⏭️ 跳过 LLM 处理")

    # 后规范化
    print("🔧 后规范化...")
    merged = improve_news(merged, do_filter=False)

    # 论文溯源 + Body 校验
    if not args.skip_llm:
        print("🔍 论文溯源 + Body 校验...")
        merged = post_validate_and_enrich(merged)

    # 如果跳过了 LLM，用新分类逻辑重新分类
    if args.skip_llm:
        for a in merged:
            new_cat = get_cat(a.get('title', ''), a.get('summary', ''), a.get('source', ''))
            a['categories'] = new_cat
            # 同时重新计算优先级
            a['priority'] = calculate_priority_v2(a)

    # 重新排序
    merged = sorted(merged, key=lambda x: x.get("priority", 0), reverse=True)

    for a in merged:
        if a.get("is_tweet"):
            source = a.get("source", "").lower().replace("@", "")
            title = a.get("title", "").lower()
            if any(r in source for r in RESEARCHER_ACCOUNTS):
                if any(k in title for k in ['paper', 'arxiv', 'research', 'study', 'experiment', 'method', 'model', 'agi', 'agent', 'oracles', 'activation', 'red team', '对齐', '研究', '论文', '模型']):
                    a['categories'] = ['研究关注']
                else:
                    a['categories'] = ['X讨论']
            elif any(c in source for c in COMPANY_ACCOUNTS):
                pass
            else:
                a['categories'] = ['X讨论']

    # 统计
    by_cat = defaultdict(int)
    for a in merged:
        for c in a["categories"]: by_cat[c] += 1
    print(f"📂 分类: ", end="")
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        print(f"{cat}{by_cat.get(cat,0)} ", end="")
    print("")

    if errors:
        print(f"⚠️ 失败: {errors[:3]}")

    # Overflow 标记：超过上限时用 LLM 标记低价值条目（不自动删除）
    from qa import MAX_ARTICLES, check_article_overflow
    if len(merged) > MAX_ARTICLES and not args.skip_llm:
        print(f"\n⚠️ 条目过多（{len(merged)}>{MAX_ARTICLES}），LLM 建议删除：")
        overflow_issues = check_article_overflow(merged)
        if overflow_issues:
            for _, title, msg in overflow_issues:
                reason = msg.split('：')[-1] if '：' in msg else msg
                print(f"   ⚠️ {title[:45]} — {reason}")

    # 生成报告
    if args.no_overwrite and os.path.exists(OUTPUT_FILE):
        print(f"⚠️ {OUTPUT_FILE} 已存在且 --no-overwrite，跳过覆盖")
    else:
        report = generate_report(merged)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(report)


    # 保存归档
    save_archive(merged)
    print(f"✅ 已输出: {OUTPUT_FILE}")

    # 质量日志（自进化数据源）
    _log_quality(merged)

    # 自动 QA 检查 + autofix
    try:
        from qa import run_checks
        print("\n📋 自动 QA 检查...")
        date_str = args.date if args.date else datetime.now().strftime("%Y-%m-%d")
        issue_count = run_checks(date_str)

        # QA 发现 short_body 问题 → 自动补充
        if issue_count > 0 and not args.skip_llm:
            from qa_autofix import autofix_short_body
            print("\n🔧 自动补充 body...")
            fixed = autofix_short_body(date_str)
            if fixed > 0:
                print(f"   ✅ 已补充 {fixed} 条")
    except ImportError as e:
        print(f"   ⚠️ QA/autofix模块缺失: {e}")
    except Exception as e:
        print(f"   ⚠️ QA检查失败: {e}")

    # 标记 feedback 已处理（本轮已看过这些提醒）
    _mark_feedback_seen()

    # 生成HTML
    try:
        import subprocess
        env = os.environ.copy()
        news_date = args.date if args.date else datetime.now().strftime("%Y-%m-%d")
        env["NEWS_DATE"] = news_date
        subprocess.run(['python', 'html_generator.py'], check=True, capture_output=True, env=env)
    except Exception as e:
        print(f"   ⚠️ HTML生成失败: {e}")

if __name__ == "__main__":
    main()
