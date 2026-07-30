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
import hashlib
import subprocess

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
from release_gate import chinese_text_ok
from pipeline_core import (
    atomic_write_json,
    atomic_write_text,
    canonicalize_url,
    ensure_candidate_ids,
    parse_llm_array,
    reconcile_written_results,
    report_window,
    validate_rank_results,
)


class PipelineBlocked(RuntimeError):
    """Raised when a draft is unsafe or incomplete and must not be published."""


_CURRENT_REPORT_DATE = None
_CURRENT_RUN_ID = None


VALID_OUTPUT_CATEGORIES = {
    "模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"
}

# 导入研究者推文抓取
def fetch_researcher_tweets(start_time=None, end_time=None):
    """抓取前沿研究者推文：缓存超过30分钟则触发新抓取，否则用缓存"""
    import json
    import os
    from datetime import datetime
    from email.utils import parsedate_to_datetime

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

    def _in_requested_window(tweet):
        if not start_time or not end_time:
            return True
        try:
            published = parsedate_to_datetime(tweet.get("published", ""))
            return start_time <= published < end_time
        except Exception:
            return False

    def _windowed(tweets):
        return [tweet for tweet in (tweets or []) if _in_requested_window(tweet)]

    # 检查缓存新鲜度
    try:
        cached = _load_cache()
        if cached:
            tweets, cached_at = cached
            if cached_at:
                cache_time = datetime.fromisoformat(cached_at).replace(tzinfo=None)
                age_minutes = (datetime.now() - cache_time).total_seconds() / 60
                if age_minutes <= CACHE_MAX_AGE_MINUTES:
                    tweets = _windowed(tweets)
                    print(f"   📦 使用缓存: {len(tweets)} 条窗口内推文（{age_minutes:.0f} 分钟前抓取）")
                    return tweets
                else:
                    print(f"   ⚠️ 缓存已过期（{age_minutes:.0f} 分钟前），尝试重新抓取...")
    except Exception as e:
        print(f"   ⚠️ 缓存检查失败: {e}")

    # 缓存过期或不存在，尝试实时抓取
    try:
        from tweet_fetcher import fetch_all_tweets
        fresh_tweets = fetch_all_tweets(start_time=start_time, end_time=end_time)
        if fresh_tweets:
            print(f"   ✅ 实时抓取: {len(fresh_tweets)} 条推文")
            return fresh_tweets
    except Exception as e:
        print(f"   ⚠️ 实时抓取失败: {e}")

    # 抓取失败，回退到过期缓存
    try:
        cached = _load_cache()
        if cached and cached[0]:
            tweets = _windowed(cached[0])
            print(f"   📦 回退到过期缓存: {len(tweets)} 条窗口内推文")
            return tweets
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

RANK_TARGET_COUNT = 15       # 阶段1全局排序选出的目标条目数
RANK_RESERVE_COUNT = 10      # 额外保留候补顺序，仅用于审计/人工复核
RANK_POOL_COUNT = 35         # 初排扩大候选池，再做事件级复核
RANK_MAX_CANDIDATES = 200    # 正常单日全量送入排序，避免低分重要事件未被模型看见
WRITE_BATCH_SIZE = 5         # 缩小批次故障半径
REPORT_CUTOFF_HOUR = int(os.environ.get("REPORT_CUTOFF_HOUR", "6"))
REPORT_CUTOFF_MINUTE = int(os.environ.get("REPORT_CUTOFF_MINUTE", "40"))

def clean_text(t): return re.sub(r'<[^>]+>', '', t or "").strip() if t else ""
def normalize(t): return re.sub(r'\s+', '', (t or "").lower())

def parse_date(entry):
    parsed_value = (
        entry.get("published_parsed")
        if isinstance(entry, dict)
        else getattr(entry, "published_parsed", None)
    )
    if parsed_value:
        try:
            return datetime(*parsed_value[:6], tzinfo=timezone.utc)
        except Exception: pass
    import email.utils, calendar
    for f in ["published", "updated", "created"]:
        value = entry.get(f) if isinstance(entry, dict) else getattr(entry, f, None)
        if value:
            try:
                p = email.utils.parsedate_tz(value)
                if p:
                    timestamp = email.utils.mktime_tz(p)
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
    return False if d is None else START_UTC <= d < END_UTC


def _chinese_output_ok(title, body, insight=None):
    fields = [(title, 2), (body, 8)]
    if insight is not None:
        fields.append((insight, 4))
    return all(chinese_text_ok(text, min_cjk=min_cjk) for text, min_cjk in fields)


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


def _load_recent_tweet_links(days=3, report_date=None):
    """从近几天的 twitter preview 文件中提取 tweet URL，用于推文级去重"""
    seen = set()
    base = os.path.dirname(ARCHIVE_DIR)  # archive 的父目录
    anchor = datetime.strptime(report_date, "%Y-%m-%d") if report_date else datetime.now()
    for i in range(1, days + 1):
        date = (anchor - timedelta(days=i)).strftime("%Y-%m-%d")
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


def dedup_articles(articles, report_date=None):
    """跨天去重只做高置信 URL 匹配；语义相似项交给 rank 审核。

    旧实现会因为融资标题模板或跨语言标题相似而直接删除不同事件。召回
    优先阶段只允许 canonical URL 这种可解释、可复现的硬去重。
    """
    ensure_candidate_ids(articles)
    try:
        recent = load_recent_archives(days=3, report_date=report_date)
        seen_links = {
            canonicalize_url(a.get("link", "")) for a in recent if a.get("link")
        }
        recent_titles = [a.get("title", "") for a in recent if a.get("title")]
    except Exception:
        seen_links = set()
        recent_titles = []

    # 补充推文去重：从 twitter preview 文件中提取已抓取的 tweet URL
    seen_links.update(_load_recent_tweet_links(days=3, report_date=report_date))

    # 预计算近3天标题的实体对
    recent_entities = set()
    for rt in recent_titles:
        for pair in _extract_product_entities(rt):
            recent_entities.add(pair)

    filtered = []
    for a in articles:
        link = canonicalize_url(a.get("link", ""))
        title = a.get("title", "")

        # 1. URL 精确匹配
        if link and link in seen_links:
            print(f"   [跨天去重-URL] '{title[:40]}...' 已在前几天发布，跳过")
            continue

        # 2. 实体/标题相似只标记，不能在 rank 前销毁候选。
        entities = _extract_product_entities(title)
        possible_duplicate_reasons = []
        for company, product in entities:
            if product and (company, product) in recent_entities:
                possible_duplicate_reasons.append(f"entity:{company}+{product}")
                break
        for rt in recent_titles:
            if title_similarity(title, rt) >= 0.45:
                possible_duplicate_reasons.append(f"title:{rt[:80]}")
                break
        if possible_duplicate_reasons:
            a["_possible_recent_duplicate"] = possible_duplicate_reasons
            print(f"   [跨天待审] '{title[:40]}...' 可能与近期事件相关，不提前删除")

        filtered.append(a)
    return filtered

# ========== LLM ==========
def call_llm(prompt, system_prompt_file="news_processor.md", include_feedback=True):
    if not API_KEY:
        return None
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    # 写作/选稿可选择加载近期人工修正；不同任务使用独立 system prompt。
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
        # 只取最近 5 条有效示例，避免挤压严格 JSON 任务的上下文。
        _examples = [
            e for e in _examples
            if len(e.get("before", "")) > 5 and len(e.get("after", "")) > 5
        ][-5:]
        if include_feedback and _examples:
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
    _prompt_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "prompts", system_prompt_file
    )
    try:
        with open(_prompt_path, "r", encoding="utf-8") as f:
            system_prompt = f.read().strip() + _feedback_examples
    except FileNotFoundError:
        # fallback: 如果 prompt 文件不存在，使用空 prompt 避免崩溃
        print(f"   ⚠️ Prompt 文件不存在: {_prompt_path}")
        return None

    data = {
        "model": "MiniMax-M3", "temperature": 0.2,
        "max_tokens": 16000,
        "system": system_prompt,
        "messages": [{"role": "user", "content": prompt}]
    }
    for attempt in range(3):
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
            print(f"⚠️ LLM调用失败(第{attempt+1}/3次): {e}")
            if attempt < 2:
                import time; time.sleep(5)
            else:
                return None

import re
def _report_date_from_output():
    match = re.search(r"daily-ai-news-(\d{4}-\d{2}-\d{2})", OUTPUT_FILE)
    return match.group(1) if match else END_BJ.strftime("%Y-%m-%d")


def _build_recent_context(recent_articles):
    if not recent_articles:
        return ""
    titles = [a.get("title", "")[:100] for a in recent_articles if a.get("title")]
    return "\n".join(f"- {title}" for title in titles[:50])


def _rank_candidate_text(article):
    evidence = article.get("content") or article.get("summary") or ""
    duplicate_hint = "; ".join(article.get("_possible_recent_duplicate", []))
    return (
        f"candidate_id: {article.get('_rank_ref') or article['candidate_id']}\n"
        f"标题: {article.get('raw_title') or article.get('title', '')}\n"
        f"来源: {article.get('source', '')}\n"
        f"启发式priority: {article.get('priority', 0)}\n"
        f"候选事实: {clean_text(evidence)[:450]}\n"
        f"近期重复提示: {duplicate_hint or '无'}"
    )


def _interleave_rank_candidates(articles):
    """Interleave categories and sources without dropping any candidate.

    The old priority-sorted prompt placed long runs from one outlet/category
    together, which created position bias in large daily pools. This ordering
    keeps priority inside each source while ensuring every editorial desk and
    source appears throughout the prompt.
    """
    category_order = [
        "模型前沿", "产业动态", "算力追踪",
        "初创&融资", "研究关注", "X讨论",
    ]
    by_category = defaultdict(lambda: defaultdict(list))
    for article in articles:
        categories = article.get("categories") or ["其他"]
        category = categories[0] if categories else "其他"
        source = article.get("source") or "<unknown>"
        by_category[category][source].append(article)

    ordered_by_category = {}
    for category, source_groups in by_category.items():
        for source_articles in source_groups.values():
            source_articles.sort(
                key=lambda item: item.get("priority", 0), reverse=True
            )
        source_order = sorted(
            source_groups,
            key=lambda source: source_groups[source][0].get("priority", 0),
            reverse=True,
        )
        category_items = []
        while any(source_groups[source] for source in source_order):
            for source in source_order:
                if source_groups[source]:
                    category_items.append(source_groups[source].pop(0))
        ordered_by_category[category] = category_items

    active_categories = [
        category for category in category_order if ordered_by_category.get(category)
    ]
    active_categories.extend(
        sorted(
            category for category in ordered_by_category
            if category not in category_order and ordered_by_category[category]
        )
    )
    result = []
    while any(ordered_by_category[category] for category in active_categories):
        for category in active_categories:
            if ordered_by_category[category]:
                result.append(ordered_by_category[category].pop(0))

    if len(result) != len(articles):
        raise PipelineBlocked("候选交错排序发生数量不一致")
    for index, article in enumerate(result, 1):
        article["_rank_input_position"] = index
    return result


def _call_ranker(prompt, valid_ids, expected_count, stage_label):
    last_error = "unknown"
    for attempt in range(3):
        raw = call_llm(
            prompt,
            system_prompt_file="news_ranker.md",
            include_feedback=False,
        )
        try:
            rows = parse_llm_array(raw or "")
            ranked_ids = validate_rank_results(rows, valid_ids, expected_count)
            return ranked_ids, rows
        except Exception as exc:
            last_error = str(exc)
            print(
                f"   ⚠️ {stage_label}响应无效（{attempt + 1}/3）: "
                f"{last_error[:120]}"
            )
            if attempt < 2:
                import time
                time.sleep(2)
    raise PipelineBlocked(f"{stage_label}连续失败: {last_error}")


_EVENT_ANCHOR_STOPWORDS = {
    "after", "announces", "announced", "begins", "build", "company",
    "first", "from", "here", "homegrown", "into", "launch", "launches",
    "makes", "model", "new", "next", "report", "reports", "says",
    "shares", "support", "system", "tool", "tools", "with",
}


def _event_title_anchors(title):
    return {
        token
        for token in re.findall(r"[a-z][a-z0-9-]{2,}", (title or "").lower())
        if token not in _EVENT_ANCHOR_STOPWORDS
    }


def _event_product_keys(article):
    title = article.get("raw_title") or article.get("title", "")
    return {
        f"{company.lower()}::{product.lower()}"
        for company, product in _extract_product_entities(title)
        if product
    }


def _same_ranked_event(left, right):
    """Conservative post-rank event identity check.

    This never removes a candidate before the model has seen it. It only
    prevents multiple reports or release-day integrations for the same named
    product from occupying several final slots.
    """
    if canonicalize_url(left.get("link", "")) == canonicalize_url(right.get("link", "")):
        return bool(left.get("link"))

    left_products = _event_product_keys(left)
    right_products = _event_product_keys(right)
    if left_products and left_products & right_products:
        return True

    left_title = left.get("raw_title") or left.get("title", "")
    right_title = right.get("raw_title") or right.get("title", "")
    shared = _event_title_anchors(left_title) & _event_title_anchors(right_title)
    left_acronyms = {
        token.lower() for token in re.findall(r"\b[A-Z][A-Z0-9-]{2,}\b", left_title)
        if token not in {"THE", "AND", "FOR", "WITH"}
    }
    right_acronyms = {
        token.lower() for token in re.findall(r"\b[A-Z][A-Z0-9-]{2,}\b", right_title)
        if token not in {"THE", "AND", "FOR", "WITH"}
    }
    shared_acronyms = left_acronyms & right_acronyms
    left_proper = {
        token.lower()
        for token in re.findall(r"\b[A-Z][A-Za-z0-9-]{2,}\b", left_title)
        if token.lower() not in _EVENT_ANCHOR_STOPWORDS
    }
    right_proper = {
        token.lower()
        for token in re.findall(r"\b[A-Z][A-Za-z0-9-]{2,}\b", right_title)
        if token.lower() not in _EVENT_ANCHOR_STOPWORDS
    }
    shared_named = shared_acronyms | (left_proper & right_proper)
    return bool(shared_named and len(shared) >= 2)


def _event_representative_score(article):
    """Prefer the underlying action over derivative market/reaction coverage."""
    title = (article.get("raw_title") or article.get("title", "")).lower()
    score = 0
    derivative_markers = (
        "shares slide", "stock falls", "stock drops", "market reacts",
        "after report", "回应", "股价下跌",
    )
    direct_action_markers = (
        "mass production", "begins production", "launches", "releases",
        "invests", "raises", "partners", "open-sourced", "量产", "发布",
        "融资", "投资",
    )
    score -= 50 * sum(marker in title for marker in derivative_markers)
    score += 15 * sum(marker in title for marker in direct_action_markers)
    evidence = article.get("content") or article.get("summary") or ""
    score += min(len(str(evidence)), 1200) / 200
    return score


def _collapse_ranked_events(ordered_ids, article_by_id, expected_count):
    kept = []
    for candidate_id in ordered_ids:
        article = article_by_id[candidate_id]
        duplicate_of = next((
            kept_id for kept_id in kept
            if _same_ranked_event(article, article_by_id[kept_id])
        ), None)
        if duplicate_of:
            existing = article_by_id[duplicate_of]
            if _event_representative_score(article) > _event_representative_score(existing):
                kept[kept.index(duplicate_of)] = candidate_id
                existing["_event_duplicate_of"] = candidate_id
                article.pop("_event_duplicate_of", None)
            else:
                article["_event_duplicate_of"] = duplicate_of
            continue
        kept.append(candidate_id)
        if len(kept) == expected_count:
            break
    minimum_publishable = min(RANK_TARGET_COUNT, expected_count)
    if len(kept) < minimum_publishable:
        raise PipelineBlocked(
            f"事件去重后仅剩 {len(kept)} 条，无法满足 "
            f"{minimum_publishable} 条成稿需求"
        )
    return kept


def _selection_desks(article):
    title = article.get("raw_title") or article.get("title", "")
    source = article.get("source", "")
    categories = article.get("categories") or []
    text = f"{title} {source}".lower()
    desks = set()

    if (
        source.lower().startswith("arxiv")
        or "huggingface daily papers" in source.lower()
        or "研究关注" in categories
    ):
        desks.add("research")
    if any(
        keyword in text
        for keyword in (
            "nuclear", "reactor", "fusion", "stellarator",
            "核能", "核反应堆", "聚变",
        )
    ):
        desks.add("frontier_energy")
    if any(
        keyword in text
        for keyword in (
            "robot", "robotics", "humanoid", "embodied", "physical ai",
            "具身", "机器人", "机械臂", "数据手套",
        )
    ):
        desks.add("robotics")
    capital_action = re.search(
        r"\b(?:invest(?:s|ed|ment)?|raises?|funding|financing|acquir(?:e|es|ed|ing))\b"
        r"|投资|融资|募资|收购",
        text,
    )
    material_scale = re.search(
        r"\$\s*\d|(?:multi)?billion|(?:hundred\s+)?million|"
        r"\d+(?:\.\d+)?\s*[亿万]元?|数十亿|数百亿",
        text,
    )
    if capital_action and material_scale:
        desks.add("strategic_capital")
    return desks


def _selection_entity(article):
    text = " ".join(
        str(article.get(field, ""))
        for field in ("raw_title", "title", "source")
    ).lower()
    patterns = (
        ("Moonshot", ("moonshot", "kimi", "moon_ep", "moonep", "agentenv", "perceptionbench")),
        ("NVIDIA", ("nvidia",)),
        ("Microsoft", ("microsoft",)),
        ("OpenAI", ("openai", "chatgpt")),
        ("Anthropic", ("anthropic", "claude")),
        ("Google", ("google", "deepmind", "gemini")),
        ("Meta", ("meta", "llama")),
    )
    for entity, aliases in patterns:
        if any(alias in text for alias in aliases):
            return entity
    return None


def _rank_research_shortlist(articles):
    research_articles = [
        article for article in articles
        if "research" in _selection_desks(article)
    ]
    expected_count = min(6, len(research_articles))
    if expected_count == 0:
        return []

    prompt = f"""请从以下研究候选中选出 {expected_count} 项最值得进入综合日报复核池的独立研究，并按重要性排序。

优先标准：
- 明确的新方法、训练/推理框架、重要实证结果或可复用的开源研究基础设施；
- 对 Agent、模型能力、MLSys、具身智能或 AI4S 有广泛影响，而不是只靠热门关键词；
- 有具体贡献、实验或系统设计信息。排除普通增量论文、活动、综述和缺乏新增事实的宣传。

只能原样返回输入里的短 candidate_id；输出恰好 {expected_count} 项，rank 为连续整数。
只输出 JSON 数组：
[{{"candidate_id":"R017","rank":1}}, ...]

研究候选：

""" + "\n\n---\n\n".join(
        _rank_candidate_text(article) for article in research_articles
    )

    valid_refs = [article["_rank_ref"] for article in research_articles]
    ranked_refs, _ = _call_ranker(
        prompt, valid_refs, expected_count, "研究桌复核"
    )
    ref_to_id = {
        article["_rank_ref"]: article["candidate_id"]
        for article in research_articles
    }
    ranked_ids = [ref_to_id[ranked_ref] for ranked_ref in ranked_refs]
    for rank, candidate_id in enumerate(ranked_ids, 1):
        next(
            article for article in research_articles
            if article["candidate_id"] == candidate_id
        )["_research_rank"] = rank
    return ranked_ids


def _build_editorial_portfolio(
    global_ids,
    preliminary_ids,
    all_candidate_ids,
    research_ids,
    article_by_id,
    selected_count,
    final_count,
):
    """Protect desk coverage while retaining global importance ordering."""
    required = []

    def require_from_order(desk, ordered_ids, floor):
        chosen = [
            candidate_id for candidate_id in ordered_ids
            if desk in _selection_desks(article_by_id[candidate_id])
        ][:floor]
        for candidate_id in chosen:
            article = article_by_id[candidate_id]
            reasons = article.setdefault("_portfolio_required", [])
            if desk not in reasons:
                reasons.append(desk)
            if candidate_id not in required:
                required.append(candidate_id)

    require_from_order("research", research_ids, 3)
    require_from_order("frontier_energy", all_candidate_ids, 2)
    require_from_order("robotics", all_candidate_ids, 2)
    # Capital events are ordered by the global editor first. This protects
    # material investments in frontier labs and compute infrastructure without
    # turning every funding announcement into a quota item.
    capital_order = list(dict.fromkeys(preliminary_ids + all_candidate_ids))
    require_from_order("strategic_capital", capital_order, 2)

    selected = list(global_ids[:selected_count])
    for candidate_id in required:
        if candidate_id not in selected:
            selected.append(candidate_id)

    global_position = {
        candidate_id: rank for rank, candidate_id in enumerate(preliminary_ids, 1)
    }
    # Keep the strongest global judgement, while allowing a run of small
    # updates from the same company below the top three to yield to independent
    # strategic events.
    protected = set(required) | set(global_ids[:3])
    while len(selected) > selected_count:
        entity_counts = defaultdict(int)
        for candidate_id in selected:
            entity = _selection_entity(article_by_id[candidate_id])
            if entity:
                entity_counts[entity] += 1

        removable = [
            candidate_id for candidate_id in selected
            if candidate_id not in protected
        ]
        if not removable:
            removable = [
                candidate_id for candidate_id in selected
                if candidate_id not in set(required)
            ]
        if not removable:
            raise PipelineBlocked("编辑组合约束冲突，无法形成 Top 15")

        def removal_score(candidate_id):
            entity = _selection_entity(article_by_id[candidate_id])
            concentration = entity_counts.get(entity, 1) if entity else 1
            return (
                concentration,
                global_position.get(candidate_id, 10**6),
            )

        selected.remove(max(removable, key=removal_score))

    selected_set = set(selected)
    selected_order = [
        candidate_id for candidate_id in global_ids
        if candidate_id in selected_set
    ]
    selected_order.extend(
        candidate_id for candidate_id in required
        if candidate_id in selected_set and candidate_id not in selected_order
    )
    if len(selected_order) != selected_count:
        raise PipelineBlocked("编辑组合后的入选数量不一致")

    reserve_sources = global_ids + preliminary_ids + research_ids
    final_ids = list(selected_order)
    for candidate_id in reserve_sources:
        if len(final_ids) >= final_count:
            break
        if candidate_id in final_ids:
            continue
        if any(
            _same_ranked_event(
                article_by_id[candidate_id],
                article_by_id[kept_id],
            )
            for kept_id in final_ids
        ):
            continue
        final_ids.append(candidate_id)

    if len(final_ids) != final_count:
        raise PipelineBlocked(
            f"编辑组合仅形成 {len(final_ids)} 个唯一事件，预期 {final_count}"
        )
    return final_ids


def _rank_candidates(rank_candidates, recent_articles):
    final_count = min(
        len(rank_candidates), RANK_TARGET_COUNT + RANK_RESERVE_COUNT
    )
    if final_count == 0:
        raise PipelineBlocked("没有可供排序的候选")
    pool_count = min(len(rank_candidates), max(final_count, RANK_POOL_COUNT))
    prompt_candidates = _interleave_rank_candidates(rank_candidates)
    for index, article in enumerate(prompt_candidates, 1):
        article["_rank_ref"] = f"R{index:03d}"

    prompt = f"""请从今日候选中严格选出 {pool_count} 个事件进入复核池并排序。

硬性要求：
1. 输出必须恰好 {pool_count} 项，rank 必须是 1 到 {pool_count} 的连续整数。
2. 只能原样返回输入里的短 candidate_id（例如 R017）；禁止返回标题或自行编造长 ID。
3. 排的是“事件”而不是媒体文章：同一事件多来源只选信息最完整的一条。
4. priority 仅供参考，不能替代编辑判断。低分但重大的芯片、供应链、头部公司动作、关键研究不可因来源靠后而漏掉。
5. 排除招聘、普通 CFO 等例行人事任命、活动宣传、纯祝贺、生活感想、无新增事实的转发以及与本刊范围无关的消费/娱乐内容。
6. 若候选被标为“近期可能重复”，只有确属同一主体、同一动作时才排除；模板相似不等于重复。
7. 必须先扫描全部候选再排序；机器人、先进制造、光刻、数据中心、核能/聚变等前沿基础设施属于范围，不能仅因标题不含 AI 而忽略。
8. 不设机械分类配额，但同质论文或同一公司的小更新不能淹没独立的资本、产能、供应链、合作和技术里程碑。
9. 有明确系统贡献的训练/推理框架和重要开源研究工具属于高价值研究；具体融资、产能落地、物理基础设施与机器人进展，通常高于泛泛评论、立场声明或未落地的政策猜测。

只输出 JSON 数组：
[{{"candidate_id":"R017","rank":1}}, ...]

近期已发布事件：
{_build_recent_context(recent_articles) or "无"}

今日候选：

""" + "\n\n---\n\n".join(_rank_candidate_text(a) for a in prompt_candidates)

    valid_refs = [article["_rank_ref"] for article in prompt_candidates]
    preliminary_refs, _ = _call_ranker(
        prompt, valid_refs, pool_count, "初排"
    )
    ref_to_candidate_id = {
        article["_rank_ref"]: article["candidate_id"]
        for article in prompt_candidates
    }
    preliminary_ids = [
        ref_to_candidate_id[candidate_ref]
        for candidate_ref in preliminary_refs
    ]
    article_by_id = {
        article["candidate_id"]: article for article in rank_candidates
    }
    for rank, candidate_id in enumerate(preliminary_ids, 1):
        article_by_id[candidate_id]["_preliminary_rank"] = rank

    collapsed = _collapse_ranked_events(
        preliminary_ids,
        article_by_id,
        final_count,
    )
    duplicate_count = sum(
        bool(article_by_id[candidate_id].get("_event_duplicate_of"))
        for candidate_id in preliminary_ids
    )
    if duplicate_count:
        print(
            f"   🧹 事件级复核: 初排 {len(preliminary_ids)} 条，"
            f"跳过 {duplicate_count} 个重复报道或发布日伴生项，"
            f"保留 {len(collapsed)} 个唯一事件"
        )
    research_ids = _rank_research_shortlist(prompt_candidates)
    portfolio_ids = _build_editorial_portfolio(
        collapsed,
        preliminary_ids,
        [article["candidate_id"] for article in rank_candidates],
        research_ids,
        article_by_id,
        min(RANK_TARGET_COUNT, final_count),
        final_count,
    )
    protected_count = sum(
        bool(article_by_id[candidate_id].get("_portfolio_required"))
        for candidate_id in portfolio_ids[:RANK_TARGET_COUNT]
    )
    print(
        f"   🗂️ 编辑组合: Top {min(RANK_TARGET_COUNT, final_count)} "
        f"中 {protected_count} 条承担研究/机器人/前沿能源/战略资本覆盖"
    )
    return portfolio_ids


def _prepare_writer_evidence(article):
    """Collect source evidence before writing; never append it to final body."""
    base = clean_text(article.get("content") or article.get("summary") or "")
    parts = [base] if base else []
    fetched = ""
    link = article.get("link", "")
    if link and len(base) < 900:
        fetched = _deep_fetch(link) or ""
        fetched = clean_text(fetched)
        if fetched and fetched not in base:
            parts.append(fetched)
    evidence = "\n\n".join(part for part in parts if part).strip()
    article["_evidence_length"] = len(evidence)
    article["_deep_fetch_used"] = bool(fetched)
    return evidence[:2400]


def _writer_item_text(article):
    evidence = article.get("_writer_evidence") or _prepare_writer_evidence(article)
    article["_writer_evidence"] = evidence
    retry_feedback = article.get("_writer_retry_feedback", "")
    return (
        f"candidate_id: {article.get('_writer_ref') or article['candidate_id']}\n"
        f"原始标题: {article.get('raw_title') or article.get('title', '')}\n"
        f"来源: {article.get('source', '')}\n"
        f"原文链接: {article.get('link', '')}\n"
        f"重试纠错: {retry_feedback or '无'}\n"
        f"可用事实证据:\n{evidence or '来源仅提供标题；不得扩写未经证实的事实。'}"
    )


def _writer_prompt(batch, recent_articles):
    return f"""请为输入中的每一个 candidate_id 撰写日报条目，不得选稿或省略。

输出必须是 JSON 数组，每个输入 ID 恰好对应一项：
[
  {{
    "candidate_id": "cand_xxx",
    "title": "中文标题",
    "body": "中文事实正文",
    "insight": "中文务实判断",
    "category": "模型前沿|产业动态|算力追踪|初创&融资|研究关注|X讨论"
  }}
]

硬性要求：
- title、body、insight 使用中文完整表达；公司、产品、模型、论文与 benchmark 专名可保留英文。
- 不得复制英文原句，不得出现抓取标记、Image Credits、Abstract、关键词或作者元数据。
- 只使用“可用事实证据”里的信息。body 必须至少两个以中文标点结束的完整句子；证据不足时也要把已知动作和适用范围拆成两句，但不得猜测或用常识补齐。
- body 只写事实；判断放 insight。category 必须严格取六个合法值之一。
- 不得改变、遗漏、重复或臆造 candidate_id。

近期已发布事件（只用于说明延续关系，不可作为新增事实来源）：
{_build_recent_context(recent_articles) or "无"}

待写条目：

""" + "\n\n---\n\n".join(_writer_item_text(a) for a in batch)


def _valid_writer_row(row):
    title = (row.get("title") or "").strip()
    body = (row.get("body") or "").strip()
    insight = (row.get("insight") or "").strip()
    category = (row.get("category") or "").strip()
    if category not in VALID_OUTPUT_CATEGORIES:
        return False, f"无效分类: {category or '<missing>'}"
    if not _chinese_output_ok(title, body, insight):
        return False, "中文/残留门禁失败"
    if _count_sentences(body) < 2:
        return False, "body 少于 2 句"
    return True, ""


def _call_writer(batch, recent_articles, attempts=2):
    article_by_ref = {
        article["_writer_ref"]: article for article in batch
    }
    pending_refs = list(article_by_ref)
    accepted = {}

    for attempt in range(attempts):
        pending_batch = [article_by_ref[writer_ref] for writer_ref in pending_refs]
        prompt = _writer_prompt(pending_batch, recent_articles)
        raw = call_llm(prompt, system_prompt_file="news_writer.md", include_feedback=True)
        try:
            rows = parse_llm_array(raw or "")
            by_ref, missing_refs = reconcile_written_results(rows, pending_refs)
            for writer_ref, row in list(by_ref.items()):
                ok, reason = _valid_writer_row(row)
                if not ok:
                    article_by_ref[writer_ref]["_writer_retry_feedback"] = (
                        f"上一版未通过：{reason}。必须修正后重新输出。"
                    )
                    missing_refs.append(writer_ref)
                    del by_ref[writer_ref]
                    print(f"   ⚠️ 写作门禁拒绝 {writer_ref}: {reason}")
            for writer_ref, row in by_ref.items():
                actual_id = article_by_ref[writer_ref]["candidate_id"]
                normalized_row = dict(row)
                normalized_row["candidate_id"] = actual_id
                accepted[actual_id] = normalized_row
            pending_refs = list(dict.fromkeys(missing_refs))
            if not pending_refs:
                return accepted, []
            print(
                f"   ⚠️ 写作响应不完整（{attempt + 1}/{attempts}），"
                f"剩余 {len(pending_refs)} 条"
            )
        except Exception as exc:
            print(
                f"   ⚠️ 写作响应无效（{attempt + 1}/{attempts}）: "
                f"{str(exc)[:120]}"
            )

        if attempt + 1 < attempts:
            import time
            time.sleep(2)

    missing_ids = [
        article_by_ref[writer_ref]["candidate_id"]
        for writer_ref in pending_refs
    ]
    return accepted, missing_ids


def _write_selected_articles(selected_articles, recent_articles):
    for index, article in enumerate(selected_articles, 1):
        article["_writer_ref"] = f"W{index:02d}"
    written = {}
    missing_ids = []
    total_batches = (len(selected_articles) + WRITE_BATCH_SIZE - 1) // WRITE_BATCH_SIZE
    for batch_index in range(total_batches):
        batch = selected_articles[
            batch_index * WRITE_BATCH_SIZE:(batch_index + 1) * WRITE_BATCH_SIZE
        ]
        print(f"   📝 写作批次 {batch_index + 1}/{total_batches}（{len(batch)} 条）")
        batch_written, batch_missing = _call_writer(batch, recent_articles, attempts=2)
        written.update(batch_written)
        missing_ids.extend(batch_missing)

    # Retry every missing/invalid item independently so one malformed item
    # cannot erase a whole batch.
    by_id = {a["candidate_id"]: a for a in selected_articles}
    still_missing = []
    for candidate_id in dict.fromkeys(missing_ids):
        article = by_id[candidate_id]
        print(f"   🔁 单条恢复: {article.get('raw_title', '')[:60]}")
        single_written, single_missing = _call_writer([article], recent_articles, attempts=2)
        written.update(single_written)
        if single_missing:
            still_missing.append(candidate_id)

    if still_missing:
        titles = [by_id[cid].get("raw_title", "")[:80] for cid in still_missing]
        raise PipelineBlocked(
            "选中条目写作失败，已隔离且禁止原文回填: " + "; ".join(titles)
        )
    return written


def _write_selection_audit(all_articles, ranked_ids, selected_ids, ready_ids):
    ranked_position = {candidate_id: index + 1 for index, candidate_id in enumerate(ranked_ids)}
    rows = []
    for article in all_articles:
        candidate_id = article["candidate_id"]
        if candidate_id in ready_ids:
            fate = "ready_candidate"
        elif candidate_id in selected_ids:
            fate = "selected_write_failed"
        elif candidate_id in ranked_position:
            fate = "reserve"
        else:
            fate = "rank_not_selected"
        rows.append({
            "candidate_id": candidate_id,
            "fate": fate,
            "rank": ranked_position.get(candidate_id),
            "rank_ref": article.get("_rank_ref"),
            "rank_input_position": article.get("_rank_input_position"),
            "preliminary_rank": article.get("_preliminary_rank"),
            "research_rank": article.get("_research_rank"),
            "portfolio_required": article.get("_portfolio_required"),
            "event_duplicate_of": article.get("_event_duplicate_of"),
            "source": article.get("source", ""),
            "title": article.get("raw_title") or article.get("title", ""),
            "priority": article.get("priority", 0),
            "link": article.get("link", ""),
        })
    date_str = _report_date_from_output()
    audit_path = os.path.join(ARCHIVE_DIR, f"dropped_{date_str}.json")
    atomic_write_json(audit_path, {
        "date": date_str,
        "input": len(all_articles),
        "ranked": len(ranked_ids),
        "selected": len(selected_ids),
        "ready": len(ready_ids),
        "candidates": rows,
    })
    print(f"   💾 选稿审计: {audit_path}")


def process_with_llm(articles, recent_articles=None):
    """Rank all eligible candidates, then write and validate exactly Top N."""
    recent_articles = recent_articles or []
    if not API_KEY:
        raise PipelineBlocked("MINIMAX_API_KEY 缺失，禁止发布原始候选")
    if not articles:
        raise PipelineBlocked("候选为空，禁止生成空日报")

    ensure_candidate_ids(articles)
    sorted_articles = sorted(
        articles, key=lambda item: item.get("priority", 0), reverse=True
    )
    if len(sorted_articles) > RANK_MAX_CANDIDATES:
        raise PipelineBlocked(
            f"候选数 {len(sorted_articles)} 超过可审计上限 {RANK_MAX_CANDIDATES}，禁止静默截断"
        )

    print(f"   🔍 全量排序 {len(sorted_articles)} 条候选（无公司/来源硬删除）")
    ranked_ids = _rank_candidates(sorted_articles, recent_articles)
    article_by_id = {article["candidate_id"]: article for article in sorted_articles}
    for index, candidate_id in enumerate(ranked_ids, 1):
        article_by_id[candidate_id]["_editorial_rank"] = index

    selected_ids = ranked_ids[: min(RANK_TARGET_COUNT, len(ranked_ids))]
    selected_articles = [article_by_id[candidate_id] for candidate_id in selected_ids]
    # Persist the editorial decision before writing starts. If a later model
    # call fails, the selected/reserve/not-selected split remains inspectable.
    _write_selection_audit(
        sorted_articles, ranked_ids, selected_ids, set()
    )
    written = _write_selected_articles(selected_articles, recent_articles)

    ready = []
    for candidate_id in selected_ids:
        article = article_by_id[candidate_id]
        row = written[candidate_id]
        article["title"] = row["title"].strip()
        article["body"] = row["body"].strip()
        article["insight"] = row["insight"].strip()
        article["categories"] = [row["category"].strip()]
        article["provenance"] = {
            "selection": "llm_ranked",
            "writing": "llm_writer",
            "status": "validated",
        }
        article["_provenance"] = "llm_written_validated"
        article["_selection_status"] = "selected"
        # Evidence is an internal transient and must not enter the archive.
        article.pop("_writer_evidence", None)
        article.pop("_writer_retry_feedback", None)
        article.pop("_writer_ref", None)
        ready.append(article)

    expected_ready = min(RANK_TARGET_COUNT, len(sorted_articles))
    if len(ready) != expected_ready:
        raise PipelineBlocked(f"成稿数量 {len(ready)} != 预期 {expected_ready}")

    _write_selection_audit(
        sorted_articles, ranked_ids, selected_ids, {a["candidate_id"] for a in ready}
    )
    print(f"✅ 全量候选{len(sorted_articles)} → 排序{len(ranked_ids)} → 成稿{len(ready)}")
    return ready

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

def _count_sentences(text):
    """计算中英文句数"""
    if not text:
        return 0
    sentences = re.split(r'[。.!?！？]', text)
    return len([s for s in sentences if s.strip()])

def post_validate_and_enrich(articles):
    """Final read-only validation.

    Source enrichment now happens before the writer.  Post-writing raw append
    was the second major English/residue leak, so this stage must never mutate
    body text or call a generative web-search fallback.
    """
    warnings = []
    for a in articles:
        body = a.get("body", "")
        sent_count = _count_sentences(body)
        title = a.get("title", "")
        insight = a.get("insight", "")
        if not _chinese_output_ok(title, body, insight):
            warnings.append(f"[{title[:40]}] 中文/残留门禁失败")
        elif sent_count < 2:
            warnings.append(f"[{title[:40]}] body仅{sent_count}句")

    if warnings:
        for w in warnings:
            print(f"   ⚠️ {w}")
        raise PipelineBlocked(f"最终正文校验失败 {len(warnings)} 条")
    return articles

# ========== 研究关注关键词 ==========
_HF_RESEARCH_KEYWORDS = {
    "LLM": ["llm", "large language model", "gpt", "claude", "gemini", "transformer", "attention",
             "prefill", "decode", "context length", "kv cache", "reasoning", "chain of thought",
             "rlhf", "dpo", "grpo", "fine-tun", "instruction follow", "agent"],
    "多模态": ["multimodal", "vision language", "vlm", "image generation", "video generation",
              "diffusion", "text-to-image", "text-to-video", "speech", "audio languag"],
    "世界模型": ["world model", "video prediction", "visual foresight", "scene generation",
               "dynamics model", "generative simulator", "interactive simulation"],
    "认知模型": ["cognitive", "causal reason", "theory of mind", "mental model",
               "grounded language", "concept learning", "neurosymbolic"],
    "具身智能": ["robot", "embodied", "manipulation", "locomotion", "navigation",
               "sim-to-real", "dexterous", "grasp", "physical ai", "autonomous driv"],
    "agent": ["agent", "tool use", "tool-augment", "agentic", "autonomous",
             "multi-agent", "web agent", "code agent", "gui agent",
             "function call", "api call", "workflow"],
    "推理": ["reasoning", "math", "code", "programming", "search", "planning",
            "tool use", "agentic", "self-improv", "process reward", "verif"],
    "MLSys": ["mlsys", "inference", "training", "distributed", "gpu", "serving", "compiler",
              "quantiz", "prun", "distill", "efficient", "optimiz",
              "kv cache", "speculativ", "offload"],
    "benchmark": ["benchmark", "evaluat", "leaderboard", "dataset",
                  "human prefer", "arena"],
    "AI安全": ["alignment", "safety", "interpretab", "red team", "jailbreak", "bias",
              "fairness", "robust", "guardrail", "constitutional", "scalable oversight"],
    "AI4S": ["ai for science", "protein", "drug", "molecule", "material", "physics",
             "climate", "biology", "alphafold"],
}


def _fetch_hf_daily_papers(max_papers=10):
    """从 HuggingFace Daily Papers API 抓取当天热门论文，按领域关键词过滤。
    返回与 feed_v5 文章格式兼容的列表，不设特殊标记，进入 LLM 正常处理流程。
    """
    try:
        r = httpx.get("https://huggingface.co/api/daily_papers", timeout=20)
        r.raise_for_status()
        all_papers = r.json()
    except Exception as e:
        print(f"   ⚠️ HF Daily Papers 抓取失败: {str(e)[:60]}")
        return []

    all_papers.sort(key=lambda x: x.get("paper", {}).get("upvotes", 0), reverse=True)

    matched = []
    for entry in all_papers:
        paper = entry.get("paper", {})
        title = paper.get("title", "")
        summary = paper.get("summary", "")
        upvotes = paper.get("upvotes", 0)
        pid = paper.get("id", "")
        authors = [a.get("name", "") for a in (paper.get("authors") or [])[:3]]

        text_lower = (title + " " + summary).lower()
        subfield = None
        for sf, keywords in _HF_RESEARCH_KEYWORDS.items():
            if any(kw.lower() in text_lower for kw in keywords):
                subfield = sf
                break

        if not subfield:
            continue

        author_str = ", ".join(authors)

        matched.append({
            "title": title[:80],
            "summary": f"{title}. Authors: {author_str}. Upvotes: {upvotes}",
            "content": summary or title,
            "link": f"https://huggingface.co/papers/{pid}",
            "source_item_id": pid,
            "categories": ["研究关注"],
            "source": "HuggingFace Daily Papers",
            "is_tweet": False,
            "published_parsed": None,
            "priority": 15 + min(upvotes, 20),
            "_subfield": subfield,
            "_upvotes": upvotes,
        })

    # 每个领域最多取 top 2，总共不超过 max_papers
    by_field = {}
    for a in matched:
        sf = a.get("_subfield", "")
        if sf not in by_field:
            by_field[sf] = []
        by_field[sf].append(a)

    result = []
    for sf in ["LLM", "推理", "agent", "世界模型", "认知模型", "多模态", "具身智能", "MLSys", "benchmark", "AI安全", "AI4S"]:
        if sf in by_field and len(result) < max_papers:
            for paper in by_field[sf][:2]:
                if len(result) < max_papers:
                    result.append(paper)

    return result


def _deep_fetch(url):
    """根据域名路由到对应提取器，返回纯文本片段或 None。"""
    if not url or not url.startswith("http"):
        return None
    try:
        if "arxiv.org/abs/" in url:
            m = re.search(r'arxiv\.org/abs/(\d{4}\.\d{4,5})', url)
            if m:
                r = _fetch_arxiv(m.group(1))
                if r and r.get("abstract"):
                    title = r.get("title", "")
                    return (f"[arXiv {title}]\n" if title else "") + r["abstract"]
        if any(d in url for d in PAYWALL_DOMAINS):
            return _extract_meta_summary(url)
        if "newsletter.semianalysis.com" in url or "substack.com" in url:
            return _extract_substack(url)
        if any(d in url for d in ("vllm.ai/blog/", "stepfun.com/blog/", "blog.together.ai", "together.ai/blog")):
            return _extract_html_main(url, max_chars=1500)
        if "techcrunch.com" in url:
            return _extract_html_main(url, max_chars=1800, marker_re=r'(In\s+Brief|Posted:|Image\s+Credits)')
        if "huggingface.co" in url and ("/papers/" in url or "/datasets/" in url or re.search(r'/[^/]+/[^/]+$', url)):
            return _extract_html_main(url, max_chars=1500)
    except Exception as e:
        print(f"   ⚠️ 深抓失败 {url[:50]}: {str(e)[:60]}")
    return None


def _extract_meta_summary(url):
    """从付费墙文章 HTML 中提取 og:description / JSON-LD keywords / authors。"""
    try:
        html = _fetch_via_curl(url)  # 自动用 Googlebot UA
    except Exception:
        return None
    parts = []
    og = re.search(r'<meta[^>]*property=["\']og:description["\'][^>]*content=["\']([^"\']+)', html)
    if og:
        parts.append(og.group(1).strip()[:600])
    # JSON-LD NewsArticle 提取 keywords / authors
    jsonld_blocks = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.+?)</script>', html, re.DOTALL)
    for block in jsonld_blocks[:3]:
        try:
            import json as _json
            data = _json.loads(block)
        except Exception:
            continue
        if isinstance(data, dict) and data.get("@type") in ("NewsArticle", "Article"):
            kw = data.get("keywords")
            if kw:
                kw_str = ", ".join(kw) if isinstance(kw, list) else str(kw)
                parts.append(f"关键词: {kw_str[:300]}")
            authors = data.get("author")
            if authors:
                auth_names = [a.get("name") for a in authors if isinstance(a, dict)] if isinstance(authors, list) else [authors.get("name")] if isinstance(authors, dict) else []
                if auth_names:
                    parts.append(f"作者: {', '.join(filter(None, auth_names))}")
            break
    return "\n".join(parts) if parts else None


def _extract_substack(url):
    """Substack 文章正文提取。"""
    try:
        html = _fetch_via_curl(url)
    except Exception:
        return None
    # Substack 把正文放在 "body_html":"..." 字段中
    m = re.search(r'"body_html"\s*:\s*"((?:[^"\\]|\\.)+?)"', html)
    if m:
        raw = m.group(1).encode().decode("unicode_escape", errors="ignore")
        text = re.sub(r'<[^>]+>', ' ', raw)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 200:
            return text[:1800]
    # 回退到 og:description
    return _extract_meta_summary(url)


def _extract_html_main(url, max_chars=1500, marker_re=None):
    """通用 HTML 正文提取：去脚本/样式后取主体文字。"""
    try:
        html = _fetch_via_curl(url)
    except Exception:
        return None
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    if marker_re:
        m = re.search(marker_re, text)
        if m:
            text = text[m.start():]
    if len(text) < 200:
        return None
    return text[:max_chars]


# ========== 抓取 ==========

# 付费墙站点用 Googlebot UA 绕过（The Information / WSJ / FT / NYT 等）
PAYWALL_DOMAINS = ("theinformation.com", "wsj.com", "ft.com", "nytimes.com",
                   "bloomberg.com", "economist.com")
GOOGLEBOT_UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"


def _ua_for_url(url):
    """根据 URL 域名决定 User-Agent。付费墙用 Googlebot，其他用 Mozilla。"""
    if any(d in url for d in PAYWALL_DOMAINS):
        return GOOGLEBOT_UA
    return "Mozilla/5.0"


def _fetch_via_curl(url):
    """curl fallback: 用系统 curl 抓取（绕过 Python OpenSSL 兼容性问题）"""
    import subprocess
    ua = _ua_for_url(url)
    result = subprocess.run(
        ["curl", "-sL", "--max-time", "15", "-H", f"User-Agent: {ua}", url],
        capture_output=True, text=True, timeout=20
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise RuntimeError(f"curl failed: rc={result.returncode}")
    return result.stdout

def fetch_source(name, url, limit=15, max_retries=5):
    """抓取 RSS 源，支持重试，httpx 失败时自动 fallback 到 curl"""
    for attempt in range(max_retries):
        try:
            client = httpx.Client(timeout=15, verify=False, follow_redirects=True)
            r = client.get(url, headers={"User-Agent": _ua_for_url(url)})
            r.raise_for_status()
            feed = feedparser.parse(r.text)
            client.close()
        except Exception as e:
            # httpx 失败，尝试 curl fallback（仅最后两次重试时）
            if attempt >= max_retries - 2:
                try:
                    raw = _fetch_via_curl(url)
                    feed = feedparser.parse(raw)
                except Exception as e2:
                    if attempt < max_retries - 1:
                        import time; time.sleep(2)
                        continue
                    return [], str(e)[:60]
            else:
                if attempt < max_retries - 1:
                    import time; time.sleep(2)
                    continue
                return [], str(e)[:60]

        try:
            articles = []
            for e in feed.entries:
                if not is_in_window(e): continue
                title = clean_text(e.get("title", ""))
                link = e.get("link", "")
                summary = clean_text(e.get("summary") or e.get("description") or "")
                if not title or len(title) < 5: continue
                cats = get_cat(title, summary, name)
                primary_cat = cats[0]

                article = {
                    "title": title,
                    "summary": summary[:150] if summary else "",
                    "content": summary,
                    "link": link,
                    "source_item_id": e.get("id") or e.get("guid") or link,
                    "categories": cats,
                    "source": name,
                    "published_parsed": list(e.get("published_parsed"))[:6] if e.get("published_parsed") else None,
                }

                # 使用新的优先级计算 v2.0
                article["priority"] = calculate_priority_v2(article)

                articles.append(article)
                if len(articles) >= limit: break
            return articles, None
        except Exception as e:
            if attempt < max_retries - 1:
                import time; time.sleep(2)
                continue
            return [], str(e)[:60]

# ========== 生成报告 ==========
def generate_report(articles):
    # 从 OUTPUT_FILE 文件名提取日期，确保与文件名一致
    import re as _re
    _m = _re.search(r'daily-ai-news-(\d{4})-(\d{2})-(\d{2})', OUTPUT_FILE)
    if _m:
        month_day = f"{_m.group(2)}月{_m.group(3)}日"
    else:
        month_day = START_BJ.strftime("%m月%d日")
    by_cat = defaultdict(list)
    for a in articles:
        for c in a["categories"]: by_cat[c].append(a)

    # 分类内排序
    for cat in by_cat:
        # 全量成稿已经通过 Top-N 门禁；渲染层不得再次静默截断。
        by_cat[cat] = sorted(
            by_cat[cat], key=lambda x: x.get("_editorial_rank", 10**9)
        )

    merged_count = sum(1 for a in articles if a.get("is_merged"))

    # 计算时间窗口
    time_diff = END_BJ - START_BJ
    hours = int(time_diff.total_seconds() / 3600)

    # 简洁头部
    lines = [f"## {month_day} AI 前沿动态", "",
             f"> 自动汇总 | 时间窗口: {hours}h | 全局精选 {len(articles)} 条", "",
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


def _log_quality(articles, report_date, gate_result=None):
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
        "date": report_date,
        "run_id": _CURRENT_RUN_ID,
        "total": len(articles),
        "categories": dict(cat_counts),
        "body_avg_len": round(sum(body_lens) / len(body_lens), 1) if body_lens else 0,
        "insight_count": insight_count,
        "insight_ratio": round(insight_count / len(articles), 2) if articles else 0,
        "prompt_hash": _prompt_hash(),
        "release_gate": gate_result.as_dict() if gate_result else None,
    }

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _prompt_hash():
    """Hash every prompt that can affect selection or publication writing."""
    root = os.path.dirname(os.path.abspath(__file__))
    digest = hashlib.sha256()
    prompt_paths = [
        os.path.join(root, "prompts", "news_ranker.md"),
        os.path.join(root, "prompts", "news_writer.md"),
        os.path.join(root, "feedback.md"),
    ]
    found = False
    for path in prompt_paths:
        try:
            with open(path, "rb") as prompt_file:
                digest.update(os.path.basename(path).encode("utf-8"))
                digest.update(b"\0")
                digest.update(prompt_file.read())
                found = True
        except FileNotFoundError:
            digest.update(f"missing:{path}".encode("utf-8"))
    return digest.hexdigest()[:12] if found else "missing"


def _pipeline_version_hash():
    """Hash code, prompts and editorial config for reproducible manifests."""
    root = os.path.dirname(os.path.abspath(__file__))
    digest = hashlib.sha256()
    relative_paths = [
        "feed_v5.py",
        "improve_news.py",
        "pipeline_core.py",
        "release_gate.py",
        "config.json",
        "accounts.yaml",
        "prompts/news_ranker.md",
        "prompts/news_writer.md",
    ]
    for relative_path in relative_paths:
        path = os.path.join(root, relative_path)
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        try:
            with open(path, "rb") as source_file:
                digest.update(source_file.read())
        except FileNotFoundError:
            digest.update(b"<missing>")
    return digest.hexdigest()[:16]


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
    atomic_write_json(state_path, {"last_seen_count": count})


def _canonical_archive_article(article):
    """Keep publication fields only; raw source prose stays in audit/cache."""
    allowed = (
        "candidate_id",
        "title",
        "body",
        "insight",
        "categories",
        "source",
        "link",
        "priority",
        "provenance",
        "_editorial_rank",
        "_selection_status",
        "_evidence_length",
        "_deep_fetch_used",
    )
    return {key: article[key] for key in allowed if key in article}


def build_archive_data(articles, report_date):
    return {
        "date": report_date,
        "count": len(articles),
        "articles": [_canonical_archive_article(article) for article in articles],
    }


def save_archive(articles, report_date):
    archive_file = os.path.join(ARCHIVE_DIR, f"news_{report_date}.json")
    data = build_archive_data(articles, report_date)
    atomic_write_json(archive_file, data)
    print(f"✅ 已存档: {archive_file}")
    return archive_file, data


def _manifest_path(report_date):
    return os.path.join(ARCHIVE_DIR, "manifests", f"{report_date}.json")


def _read_manifest(report_date):
    path = _manifest_path(report_date)
    try:
        with open(path, "r", encoding="utf-8") as manifest_file:
            data = json.load(manifest_file)
        if isinstance(data, dict) and data.get("date") == report_date:
            return data
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        pass
    return {}


def _write_manifest(report_date, status, **fields):
    data = _read_manifest(report_date)
    data.update({
        "date": report_date,
        "status": status,
        "run_id": _CURRENT_RUN_ID,
        "pipeline_version": _pipeline_version_hash(),
        "prompt_hash": _prompt_hash(),
    })
    data.update(fields)
    atomic_write_json(_manifest_path(report_date), data)
    return data


def _mark_pipeline_failed(report_date, exc):
    if not report_date:
        return
    try:
        _write_manifest(
            report_date,
            "qa_failed",
            failed_at=datetime.now(timezone.utc).isoformat(),
            failure={
                "type": type(exc).__name__,
                "detail": str(exc)[:1000],
            },
        )
    except Exception as manifest_exc:
        print(f"⚠️ 无法写入失败 manifest: {manifest_exc}", file=sys.stderr)


def _new_run_id(report_date):
    seed = (
        f"{report_date}|{datetime.now(timezone.utc).isoformat()}|"
        f"{os.getpid()}|{_pipeline_version_hash()}"
    )
    return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:20]


def _content_hash(report, archive_data, html_path):
    digest = hashlib.sha256()
    digest.update(report.encode("utf-8"))
    digest.update(
        json.dumps(
            archive_data, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    )
    with open(html_path, "rb") as html_file:
        digest.update(html_file.read())
    return digest.hexdigest()


def _print_gate_result(label, gate):
    print(
        f"   {label}: blocker={len(gate.blockers)}, "
        f"warning={len(gate.warnings)}"
    )
    for issue in gate.issues:
        marker = "❌" if issue.severity == "blocker" else "⚠️"
        print(f"   {marker} [{issue.code}] {issue.title}: {issue.detail}")

def get_time_window(target_date=None):
    """Return one explicit 24-hour report window.

    The default cutoff matches the actual 06:40 cron.  Unlike the old
    implementation, running after the cutoff never advances the end boundary
    into tomorrow.  Backfills and catch-up runs therefore remain deterministic.
    """
    if target_date is None:
        local_tz = timezone(timedelta(hours=8))
        now_local = datetime.now(timezone.utc).astimezone(local_tz)
        cutoff = now_local.replace(
            hour=REPORT_CUTOFF_HOUR,
            minute=REPORT_CUTOFF_MINUTE,
            second=0,
            microsecond=0,
        )
        report_day = now_local.date() if now_local >= cutoff else (now_local - timedelta(days=1)).date()
        target_date = report_day.strftime("%Y-%m-%d")
    return report_window(
        target_date,
        cutoff_hour=REPORT_CUTOFF_HOUR,
        cutoff_minute=REPORT_CUTOFF_MINUTE,
        utc_offset_hours=8,
    )

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
def load_recent_archives(days=3, report_date=None):
    """读取近期存档用于关联分析和跨天去重"""
    recent_news = []
    anchor = datetime.strptime(report_date, "%Y-%m-%d") if report_date else datetime.now()
    for i in range(1, days+1):
        date = (anchor - timedelta(days=i)).strftime("%Y-%m-%d")
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

    # 使用显式日报日期计算固定窗口；默认日期也由 cutoff 决定。
    global START_UTC, END_UTC, START_BJ, END_BJ, OUTPUT_FILE
    global _CURRENT_REPORT_DATE, _CURRENT_RUN_ID
    if args.date:
        try:
            parsed_report_date = datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError as exc:
            raise PipelineBlocked("--date 必须使用 YYYY-MM-DD") from exc
        if parsed_report_date.strftime("%Y-%m-%d") != args.date:
            raise PipelineBlocked("--date 必须使用 YYYY-MM-DD")
        START_UTC, END_UTC, START_BJ, END_BJ = get_time_window(args.date)
    report_date = args.date or END_BJ.strftime("%Y-%m-%d")
    _CURRENT_REPORT_DATE = report_date
    _CURRENT_RUN_ID = _new_run_id(report_date)
    OUTPUT_FILE = output_md(report_date)
    run_cache_file = os.path.join(
        os.path.dirname(CACHE_FILE), "cache", f"raw_news_{report_date}.json"
    )

    print(f"🤖 AI前沿动态 v5.1")
    print(f"   Run ID: {_CURRENT_RUN_ID}")
    print(f"   日报日期: {report_date}")
    print(f"   时间窗口: {START_BJ.strftime('%Y-%m-%d %H:%M')} - {END_BJ.strftime('%Y-%m-%d %H:%M')} 北京时间")

    # 检查是否有未处理的 feedback 修正
    _check_feedback()

    if args.from_cache:
        print(f"   模式: 从缓存读取")
    elif args.cache:
        print(f"   模式: 抓取并缓存")

    if args.no_overwrite and os.path.exists(OUTPUT_FILE):
        raise PipelineBlocked(
            f"{OUTPUT_FILE} 已存在；--no-overwrite 模式禁止生成不一致的归档或 HTML"
        )

    # 从配置加载账号列表
    COMPANY_ACCOUNTS = twitter_company_accounts()
    RESEARCHER_ACCOUNTS = twitter_researcher_accounts()

    all_arts, errors = [], []

    # 从缓存读取 或 重新抓取
    if args.from_cache:
        selected_cache = run_cache_file if os.path.exists(run_cache_file) else CACHE_FILE
        if os.path.exists(selected_cache):
            with open(selected_cache, 'r', encoding='utf-8') as f:
                cached = json.load(f)
            cached_report_date = cached.get("report_date")
            if cached_report_date and cached_report_date != report_date:
                raise PipelineBlocked(
                    f"缓存日期 {cached_report_date} 与日报日期 {report_date} 不一致"
                )
            all_arts = cached.get('articles', [])
            errors = cached.get('errors', [])
            print(f"📦 从缓存读取: {len(all_arts)} 条 ({selected_cache})")
            # 过滤超出时间窗口的文章
            before_count = len(all_arts)
            all_arts = [a for a in all_arts if is_in_window(a)]
            if len(all_arts) < before_count:
                print(f"   ⏰ 时间窗口过滤: {before_count} → {len(all_arts)} 条（移除 {before_count - len(all_arts)} 条过期）")
        else:
            raise PipelineBlocked(f"缓存文件不存在: {run_cache_file}")
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
        researcher_tweets = fetch_researcher_tweets(START_UTC, END_UTC)
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
                    "tweet_id": (
                        re.search(r"/status/(\d+)", t.get("link", "") or "").group(1)
                        if re.search(r"/status/(\d+)", t.get("link", "") or "")
                        else ""
                    ),
                    "categories": [cat],
                    "is_tweet": True,
                    "source": t.get("source", ""),
                    "published_parsed": parse_tweet_time(t.get("published", "")),
                    "priority": priority,
                })

        # 抓取 HuggingFace Daily Papers（进入 LLM 正常处理流程）
        print("📡 抓取 HuggingFace Daily Papers...")
        hf_papers = _fetch_hf_daily_papers(max_papers=10)
        if hf_papers:
            for p in hf_papers:
                print(f"   [{p.get('_subfield')}] [{p.get('_upvotes', 0)}👍] {p.get('title', '')[:60]}")
                all_arts.append(p)
            print(f"   获取 {len(hf_papers)} 篇热门论文")
        else:
            print("   无匹配论文")

        ensure_candidate_ids(all_arts)

        # 保存按日报日期分区的可回放缓存
        if args.cache:
            cache_payload = {
                'report_date': report_date,
                'window_start_utc': START_UTC.isoformat(),
                'window_end_utc': END_UTC.isoformat(),
                'articles': all_arts,
                'errors': errors,
                'time': datetime.now(timezone.utc).isoformat(),
            }
            atomic_write_json(run_cache_file, cache_payload)
            print(f"💾 已缓存到: {run_cache_file}")

    # 去重和合并
    ensure_candidate_ids(all_arts)
    unique = dedup_articles(all_arts, report_date=report_date)
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
    if not args.skip_llm:
        print("📚 读取近期存档...")
        recent_articles = load_recent_archives(days=3, report_date=report_date)
        print(f"🤖 调用LLM处理...")
        merged = process_with_llm(merged, recent_articles)
    elif args.skip_llm:
        raise PipelineBlocked("--skip-llm 仅供诊断，禁止生成可发布日报")

    # 一手源已在写作前注入；此处只做不变更内容的最终校验。
    print("🔍 最终正文校验...")
    merged = post_validate_and_enrich(merged)

    # 保留编辑排序，不再被旧 priority 覆盖。
    merged = sorted(merged, key=lambda x: x.get("_editorial_rank", 10**9))

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

    # Canonical gate is the publication decision. There is no raw/safety-net
    # fallback and no post-gate autofix that can mutate approved content.
    from qa import run_release_gate
    print("\n📋 发布硬门禁...")
    canonical_gate = run_release_gate(merged, strict=True)
    _print_gate_result("canonical", canonical_gate)
    if not canonical_gate.passed:
        _write_manifest(
            report_date,
            "qa_failed",
            failed_at=datetime.now(timezone.utc).isoformat(),
            qa={"canonical": canonical_gate.as_dict()},
        )
        raise PipelineBlocked(
            f"发布硬门禁未通过：{len(canonical_gate.blockers)} 个 blocker"
        )

    report = generate_report(merged)

    # Verify the rendered representation before it can become canonical.
    from html_generator import parse_md
    rendered_articles, _ = parse_md(report)
    rendered_gate = run_release_gate(rendered_articles, strict=False)
    _print_gate_result("rendered-md", rendered_gate)
    if len(rendered_articles) != len(merged):
        raise PipelineBlocked(
            f"渲染条目数 {len(rendered_articles)} != canonical 条目数 {len(merged)}"
        )
    if not rendered_gate.passed:
        raise PipelineBlocked(
            f"Markdown 渲染门禁未通过：{len(rendered_gate.blockers)} 个 blocker"
        )

    atomic_write_text(OUTPUT_FILE, report)
    archive_file, archive_data = save_archive(merged, report_date)
    print(f"✅ 已输出: {OUTPUT_FILE}")

    env = os.environ.copy()
    env["NEWS_DATE"] = report_date
    html_process = subprocess.run(
        [sys.executable, "html_generator.py"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
        cwd=os.path.dirname(os.path.abspath(__file__)),
    )
    if html_process.stdout.strip():
        print(html_process.stdout.strip())
    html_file = os.path.join(base_dir(), f"daily-ai-news-{report_date}.html")
    if not os.path.exists(html_file) or os.path.getsize(html_file) == 0:
        raise PipelineBlocked(f"HTML 产物缺失或为空: {html_file}")

    content_hash = _content_hash(report, archive_data, html_file)
    _write_manifest(
        report_date,
        "ready",
        ready_at=datetime.now(timezone.utc).isoformat(),
        content_hash=content_hash,
        article_count=len(merged),
        window={
            "start_utc": START_UTC.isoformat(),
            "end_utc": END_UTC.isoformat(),
            "start_bj": START_BJ.isoformat(),
            "end_bj": END_BJ.isoformat(),
        },
        artifacts={
            "markdown": OUTPUT_FILE,
            "archive": archive_file,
            "html": html_file,
        },
        qa={
            "canonical": canonical_gate.as_dict(),
            "rendered_md": rendered_gate.as_dict(),
        },
        fetch_errors=errors,
    )

    # Diagnostics and feedback state only advance after ready was written.
    try:
        _log_quality(merged, report_date, canonical_gate)
        _mark_feedback_seen()
    except Exception as diagnostic_exc:
        print(f"⚠️ 质量日志写入失败（不改变 ready 状态）: {diagnostic_exc}")

    print(f"✅ {report_date} 已通过发布门禁，manifest=ready")

if __name__ == "__main__":
    try:
        main()
    except PipelineBlocked as exc:
        _mark_pipeline_failed(_CURRENT_REPORT_DATE, exc)
        print(f"❌ 管线已阻断: {exc}", file=sys.stderr)
        raise SystemExit(2)
    except Exception as exc:
        _mark_pipeline_failed(_CURRENT_REPORT_DATE, exc)
        print(f"❌ 管线失败: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
