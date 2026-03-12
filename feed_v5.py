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
from improve_news import improve_news
from config_loader import (
    twitter_company_accounts, twitter_researcher_accounts,
    tier1_ai_companies, research_subfields, top_conferences,
    high_citation_authors, official_sources
)

# 导入研究者推文抓取
def fetch_researcher_tweets():
    """抓取前沿研究者推文"""
    try:
        from tweet_fetcher import get_tweets
        return get_tweets()
    except Exception as e:
        print(f"   ⚠️ 抓取研究者推文失败: {e}")
        return []

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========== 配置 ==========
API_KEY = os.environ.get("MINIMAX_API_KEY", "")  # 独立变量，不影响 GLM
API_URL = "https://api.minimaxi.com/anthropic/v1/messages"
OPML_FILE = "/Users/shenyalan/Desktop/Subscriptions-OnMyMac.opml"
ARCHIVE_DIR = "/Users/shenyalan/ai-daily-news/archive"
OUTPUT_FILE = "/Users/shenyalan/ai-daily-news/daily-ai-news.md"
SUMMARY_FILE = "/Users/shenyalan/ai-daily-news/daily-ai-news-summary.md"
CACHE_FILE = "/Users/shenyalan/ai-daily-news/cache_raw_news.json"

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

# 1. 来源权重
# 信息源金字塔
# Tier 1: 官方发布 (100分)
# Tier 2: 一手信源 (85分)
# Tier 3: 行业聚合 (70分)
# Tier 4: 其他 (50分)

SOURCE_WEIGHTS = {
    # Tier 1 - 官方发布
    "OpenAI News": 100, "Google DeepMind": 100, "Anthropic": 100,
    "NVIDIA Blog": 100, "Figure AI": 100, "Physical Intelligence": 100,
    "World Labs": 100, "Thinking Machines Lab": 100, "Meta AI": 100,
    "Microsoft Research": 100, "HuggingFace Blog": 100,
    "DeepSeek": 100, "Mistral AI": 100,
    "ByteDance": 100, "字节": 100, "阿里": 100, "百度": 100,
    "The Keyword": 100,  # Google 官方博客

    # Tier 2 - 一手信源 (记者/分析师直接报道)
    "The Information": 90, "Wired": 85, "TechCrunch": 85,
    "The Verge": 85, "Ars Technica": 85,
    "karpathy": 90, "Y Combinator Blog": 85, "a16z": 85, "Sequoia": 85,
    "36氪": 85,

    # Tier 3 - 行业聚合
    "量子位": 75, "新智元": 75, "机器之心": 75,
    "IT桔子": 70, "PaperWeekly": 70,
    "Sakana Blog": 80,
}

# 其他配置
HIGH_PRIORITY_KEYWORDS = [
    "gpt-5", "gpt-4.5", "o3", "o4", "o1", "claude 4", "gemini 2",
    "deepseek", "qwen3", "llama4", "mistral", "sora", "veo",
    "billion", "十亿", "亿美元", "acquire", "acquisition", "收购",
    "breakthrough", "state-of-the-art", "sota", "nature", "science",
    "launch", "unveil", "release", "announce", "发布", "开源",
    "embedding", "embedding2", "gemini embedding",
]

LOW_PRIORITY_KEYWORDS = [
    "advertisement", "sponsored", "招聘", "求职", "课程", "培训",
    "webinar", "抽奖", "活动", "meetup", "广告", "推广",
]

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

# ========== 计算研究文章优先级 ==========
def calculate_research_priority(article):
    """计算研究类文章优先级"""
    source = article.get("source", "")
    title = article.get("title", "").lower()
    summary = article.get("summary", "").lower()
    text = title + " " + summary

    # 1. 子领域基础分
    subfield = get_research_subfield(article.get("title", ""), summary)
    subfield_weight = RESEARCH_SUBFIELDS.get(subfield, {}).get("citation_weight", 15)

    # 2. 来源权重
    source_score = SOURCE_WEIGHTS.get(source, 50)

    # 3. 顶会加成
    conf_score = 0
    for conf, weight in TOP_CONFERENCES.items():
        if conf in text:
            conf_score = max(conf_score, weight)

    # 4. 学者/机构被引量
    author_score = 0
    for author, weight in HIGH_CITATION_AUTHORS.items():
        if author.lower() in text:
            author_score = max(author_score, weight)

    # 5. 热度关键词
    keyword_score = 0
    for kw in HIGH_PRIORITY_KEYWORDS:
        if kw.lower() in text:
            keyword_score += 5
    keyword_score = min(keyword_score, 20)

    # 综合分数
    total = source_score + subfield_weight + conf_score + author_score + keyword_score

    return total, subfield

# ========== 计算普通优先级 ==========
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

# 改进的分类关键词
CATEGORIES = {
    # 模型前沿：模型本身的发布、能力更新、评测
    "模型前沿": ["gpt", "claude", "gemini", "llama", "qwen", "deepseek", "minimax", "kimi",
                "模型", "发布", "开源", "能力", "benchmark", "评测", "sota", "参数",
                "多模态", "视频生成", "图像生成", "文生图", "文生视频",
                "具身智能", "机器人", "world model", "reasoning", "推理",
                "moe", "transformer", "vla", "agent", "embedding", "embedding2", "gemini embedding"],
    
    # 算力追踪：硬件、芯片、云服务
    "embedding": "模型前沿",
    "nvidia model": "产业动态",
    "nvidia发布": "产业动态",
    "算力追踪": ["gpu", "npu", "tpu", "h100", "h200", "b100", "blackwell",
                "芯片", "算力", "nvidia", "amd", "intel",
                "云计算", "aws", "azure", "gcp", "inference", "训练", "推理"],
    
    # 产业动态：公司战略、产品发布、合作、高管动态
    "产业动态": ["产品", "发布", "上线", "更新", "合作", "战略", "部署",
                "高管", "ceo", "融资", "投资", "收购", "并购", "上市",
                "苹果", "apple", "meta", "google", "microsoft", "amazon",
                "阿里", "字节", "百度", "腾讯", "华为", "字节跳动"],
    
    # 初创&融资：融资事件、投资动态
    "初创&融资": ["融资", "投资", "funding", "round", "估值", "ipo",
                "a轮", "b轮", "c轮", "d轮", "独角兽", "上市",
                "收购", "并购", "acquire"],
    
    # 研究关注：论文、学术研究
    "研究关注": ["论文", "研究", "nature", "science", "icml", "neurips",
                "cvpr", "acl", "arxiv", "学者", "教授", "paper",
                "算法", "突破", "实验室"],
}
CATEGORY_PRIORITY = {"模型前沿": 1, "产业动态": 2, "算力追踪": 3, "初创&融资": 4, "研究关注": 5, "X讨论": 6, "其他": 7}

# 研究子领域优先级
SUBFIELD_ORDER = {
    "LLM/大语言模型": 1,
    "推理/思考": 2,
    "AI安全/对齐": 3,
    "多模态": 4,
    "世界模型/具身智能": 5,
    "AI4S/科学智能": 6,
    "MLSys/系统": 7,
    "传统ML": 8,
    "其他研究": 9,
}

MAX_PER_CATEGORY = 8
MIN_ARTICLES = 30

def clean_text(t): return re.sub(r'<[^>]+>', '', t or "").strip() if t else ""
def normalize(t): return re.sub(r'\s+', '', (t or "").lower())

def parse_date(entry):
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        try:
            return datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        except: pass
    import email.utils, calendar
    for f in ["published", "updated", "created"]:
        if hasattr(entry, f):
            try:
                p = email.utils.parsedate_tz(getattr(entry, f))
                if p:
                    timestamp = calendar.timegm(p[:9])
                    return datetime.fromtimestamp(timestamp, tz=timezone.utc)
            except: continue
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
    except:
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

def is_ai_related(title, summary):
    """判断是否与AI相关（包含前沿科技）"""
    text = (title + " " + (summary or "")).lower()
    
    # AI 相关关键词
    ai_keywords = ["ai", "人工智能", "大模型", "llm", "gpt", "claude", "gemini",
                   "模型", "机器学习", "深度学习", "神经网络", "transformer",
                   "nlp", "cv", "计算机视觉", "语音", "自然语言", "自动驾驶",
                   "agent", "agents", "多模态", "视频生成", "图像生成", "文生图"]
    
    # 前沿科技（和AI一样属于科技前沿，应保留）
    frontier_keywords = ["quantum", "量子", "brain-computer", "脑机", "bci",
                        "fusion", "核聚变", "核融合", "可控核聚变",
                        "nuclear", "半导体", "芯片", "gpu", "nvidia"]
    
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

def get_cat(title, summary):
    text = (title + " " + (summary or "")).lower()
    
    # 先判断是否AI相关
    if not is_ai_related(title, summary):
        return ["其他"]  # 非AI内容归为"其他"
    
    scores = {}
    for cat, keywords in CATEGORIES.items():
        score = sum(1 for k in keywords if k.lower() in text)
        if score > 0:
            scores[cat] = score
    
    if not scores:
        return ["产业动态"]  # 默认为产业动态
    
    # 优先级排序
    sorted_cats = sorted(scores.items(), key=lambda x: (-x[1], CATEGORY_PRIORITY.get(x[0], 6)))
    return [sorted_cats[0][0]]

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

def dedup_articles(articles):
    """去重：已禁用
    
    原因：相似度判断会把不相关的新闻错误合并，导致：
    1. link 指向错误来源
    2. 不同新闻被当作同一事件
    
    如需恢复，使用 URL 精确匹配或提高相似度阈值
    """
    return articles

# ========== LLM ==========
def call_llm(prompt):
    if not API_KEY:
        return None
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "MiniMax-M2.5", "temperature": 0.2,
        "max_tokens": 8000,
        "system": """你是一个AI新闻处理器。

## 任务
处理下方的新闻列表，严格按【新闻1】、【新闻2】的顺序输出结果。

## 判断规则
### 保留条件（is_ai_related=true）
- AI/大模型、模型发布
- 量子、脑机接口、核聚变、半导体
- AI+行业、智慧城市、机器人研究
- AI相关产业链的科技融资

### 过滤条件（is_ai_related=false）
- 纯汽车、PC销量、纯安全事故
- 娱乐圈、房地产、招聘
- 纯活动预告、会议邀请（除非有实质性发布内容）
- 个人动态、日常讨论、无实质内容的转发
- 客户采用XX技术/模型的案例（除非是重大合作）
- 非核心厂商的产品/功能更新（非Google/OpenAI/NVIDIA等核心厂商）
- 已发布很久的技术新介绍（炒冷饭）
- 顶尖大学/研究机构的重要研究应该保留（UIUC、清华、斯坦福、MIT等）
- 非重大、非突破性的政策/路线图/安全指南

### 分类规则
- 模型前沿：模型发布、benchmark、多模态、视频生成、模型开源、模型评测
- 产业动态：商业、合作、用户增长、政策
- 算力追踪：芯片、硬件、半导体设备
- 初创&融资：融资、投资
- 研究关注：论文、学术、CVPR/ICML、可解释性、AI安全
- X讨论：个人动态、观点分享、日常讨论

## 输出格式
JSON数组，只返回is_ai_related=true的新闻：
[
  {
    "original_title": "原始标题（必须和输入完全一致）",
    "title": "中文标题",
    "body": "3-6句话，还原事件本身和关键细节",
    "insight": "一句话点评：趋势洞察、竞争分析、或与其他事件的关联",
    "category": "分类"
  }
]

## 重要
- title格式：关键特征+产品名/公司名
  - 把"是什么"放在前面（多模态嵌入、Agent运行时、自研芯片），产品名放在后面
  - 示例：「多模态统一嵌入模型Gemini Embedding 2」而非「Gemini Embedding 2多模态嵌入」
  - 禁止感叹号、问号结尾
  - 禁止模糊称呼，必须具体到人名或公司名
- body规则（专注事件还原）：
  - 3-6句话，只描述事件本身、关键细节和数据
  - 不包含判断和评价，判断放在insight里
  - 信息密度高，不重复标题
  - 海外公司/人名保持英文
- insight规则（负责判断）：
  - 一句话点评，作为顶尖AI分析师的洞察
  - 可以是：趋势判断、竞争格局分析、或与其他事件的关联
  - 要有观点，不要套话
- 只返回is_ai_related=true的新闻
- 所有输出必须用中文""",
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

    # 构建清晰的新闻列表，每条独立
    news_list = []
    for i, a in enumerate(sorted_articles[:25]):  # 取前25条高优先级新闻
        summary = a.get('summary', '') or a.get('content', '')
        news_list.append(f"""【新闻{i+1}】
标题：{a['title']}
来源：{a['source']}
摘要：{summary[:300]}""")
    
    prompt = """你是一个AI新闻处理器。请严格按照下方新闻进行处理。

## 输出格式要求
只返回is_ai_related=true的新闻，JSON数组格式：
[
  {
    "original_title": "原始标题（必须和输入完全一致）",
    "title": "中文标题（事件主体+做什么+为什么重要）",
    "body": "3-6句话摘要，必须有so what（为什么重要）",
    "category": "分类"
  }
]

""" + "\n\n".join(news_list)
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
                            except:
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
                    article['body'] = llm_body[:200]
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

# ========== 抓取 ==========
def fetch_source(name, url, limit=15):
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

            # 研究类用专门计算方法
            if primary_cat == "研究关注":
                priority, subfield = calculate_research_priority(article)
                article["priority"] = priority
                article["subfield"] = subfield
            else:
                priority, companies = calculate_priority(article, primary_cat)
                article["priority"] = priority
                article["subfield"] = None

            articles.append(article)
            if len(articles) >= limit: break
        client.close()
        return articles, None
    except Exception as e: return [], str(e)[:60]

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
             "#要点汇总#", ""]

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        items = by_cat.get(cat, [])
        if items:
            # 要点速览：精简说明是什么，不截断
            def get_what(title):
                # 有冒号/分隔符：取前面核心部分，不截断
                for sep in ['：', ':', '？', '?', '！', '!']:
                    if sep in title:
                        return title.split(sep)[0]
                # 无分隔符：直接返回完整标题
                return title
            titles = "; ".join([get_what(a['title']) for a in items[:5]])
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
            lines.append(f"**{a['title']}**")
            # 正文
            if a.get('body'):
                lines.append(f"- {a['body']}")
            # 一句话点评
            if a.get('insight'):
                lines.append(f"  > 💡 {a['insight']}")
            lines.append(f"   - 来源: {a['source']}")
            lines.append("")

    lines.extend(["", "---", f"*更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*"])
    return "\n".join(lines)

def generate_summary_report(articles):
    """生成简洁版报告：标题 + 展开阐释 + 关键细节 + 为什么重要 + 来源链接"""
    month_day = END_BJ.strftime("%m月%d日")
    by_cat = defaultdict(list)
    for a in articles:
        for c in a["categories"]: by_cat[c].append(a)

    for cat in by_cat:
        by_cat[cat] = sorted(by_cat[cat], key=lambda x: x.get("priority", 0), reverse=True)[:MAX_PER_CATEGORY]

    lines = [f"## {month_day} AI 前沿动态", "",
             f"> 展开阐释 + 关键细节 + 为什么重要 + 来源链接", "",
             "---", ""]

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        items = by_cat.get(cat, [])
        if not items: continue
        lines.append(f"### {cat}")

        for a in items:
            lines.append(f"**{a['title']}**")

            # 获取 body 的句子
            sentences = [s.strip() for s in a.get('body', '').split('。') if s.strip()] if a.get('body') else []

            # 细节 - key_points 或 body 第二句起
            if a.get('key_points'):
                for point in a['key_points'][:3]:
                    lines.append(f"- {point}")
            elif len(sentences) > 1:
                for s in sentences[1:3]:
                    lines.append(f"- {s}。")

            # 重要性 - insight 或 body 最后
            if a.get('insight'):
                lines.append(f"- {a['insight']}")
            elif len(sentences) > 3:
                lines.append(f"- {sentences[-1]}。")

            # 来源链接
            link = a.get('link', '')
            source = a.get('source', '')
            if link:
                lines.append(f"[来源: {source}]({link})")
            else:
                lines.append(f"[来源: {source}]")
            lines.append("")

    lines.extend(["---", f"*更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*"])
    return "\n".join(lines)

def save_archive(articles):
    date_str = END_BJ.strftime("%Y-%m-%d")
    archive_file = os.path.join(ARCHIVE_DIR, f"news_{date_str}.json")
    data = {"date": date_str, "count": len(articles), "articles": articles}
    with open(archive_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 已存档: {archive_file}")

def get_time_window():
    """获取时间窗口
    - 周一：上周五9点 -> 本周一9点（3天，覆盖周末）
    - 其他日期：昨天9点 -> 今天9点（24小时）
    """
    beijing_offset = 8
    now_utc = datetime.now(timezone.utc)
    now_beijing = now_utc + timedelta(hours=beijing_offset)

    # 判断今天是周几（0=周一，6=周日）
    weekday = now_beijing.weekday()

    end_beijing = now_beijing.replace(hour=9, minute=0, second=0, microsecond=0)
    if now_beijing.hour < 9:
        end_beijing = end_beijing - timedelta(days=1)

    # 周一：回溯到上周五（3天）
    if weekday == 0:
        start_beijing = end_beijing - timedelta(days=3)
        window_desc = "72h"
    else:
        start_beijing = end_beijing - timedelta(days=1)
        window_desc = "24h"

    return start_beijing - timedelta(hours=8), end_beijing - timedelta(hours=8), start_beijing, end_beijing

START_UTC, END_UTC, START_BJ, END_BJ = get_time_window()

# ========== 主函数 ==========
def load_recent_archives(days=3):
    """读取近期存档用于关联分析"""
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
                            "category": a.get("categories", [""])[0] if a.get("categories") else ""
                        })
            except:
                pass
    return recent_news

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='AI 前沿动态日报')
    parser.add_argument('--cache', action='store_true', help='抓取后保存到缓存文件')
    parser.add_argument('--from-cache', action='store_true', help='从缓存文件读取，跳过抓取')
    parser.add_argument('--skip-llm', action='store_true', help='跳过 LLM 处理')
    parser.add_argument('--limit', type=int, default=0, help='限制处理条数（用于快速测试）')
    args = parser.parse_args()

    print(f"🤖 AI前沿动态 v5.1")
    print(f"   时间窗口: {START_BJ.strftime('%Y-%m-%d %H:%M')} - {END_BJ.strftime('%Y-%m-%d %H:%M')} 北京时间")
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
            for t in researcher_tweets:
                source = t.get("source", "").lower().replace("@", "")
                title = t.get("title", "")
                # 根据账号类型计算优先级
                if any(c in source for c in COMPANY_ACCOUNTS):
                    # 公司账号：用普通优先级规则（来源权重）
                    priority, _ = calculate_priority({"source": t.get("source", ""), "title": title, "summary": title})
                elif any(r in source for r in RESEARCHER_ACCOUNTS):
                    # 研究者账号：用研究者优先级规则
                    priority, _ = calculate_research_priority({"source": t.get("source", ""), "title": title, "summary": title})
                else:
                    # 其他推文：用普通优先级规则（按内容重要性）
                    priority, _ = calculate_priority({"source": "TechCrunch", "title": title, "summary": title})

                all_arts.append({
                    "title": title[:80],
                    "summary": title,
                    "content": title,
                    "link": t.get("link", ""),
                    "categories": ["研究者动态"],
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

    # 生成报告
    report = generate_report(merged)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    # 生成简洁版报告
    SUMMARY_FILE = "/Users/shenyalan/ai-daily-news/daily-ai-news-summary.md"
    summary_report = generate_summary_report(merged)
    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write(summary_report)
    print(f"✅ 简洁版: {SUMMARY_FILE}")

    save_archive(merged)
    print(f"✅ 已输出: {OUTPUT_FILE}")

    # 生成HTML
    try:
        import subprocess
        subprocess.run(['python', 'generate_html.py'], check=True, capture_output=True)
    except:
        pass

if __name__ == "__main__":
    main()
