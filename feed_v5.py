#!/usr/bin/env python3
"""
AI 前沿动态 - v5.0
重点优化：研究关注按具体领域和学者被引量排序
"""

import feedparser
import httpx
import os
import json
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import re
import urllib3

# 导入规范化模块
import sys
sys.path.insert(0, '/Users/shenyalan/ai-daily-news')
from improve_news import improve_news

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ========== 配置 ==========
API_KEY = os.environ.get("ANTHROPIC_AUTH_TOKEN", "")
API_URL = "https://api.minimaxi.com/anthropic/v1/messages"
OPML_FILE = "/Users/shenyalan/Desktop/Subscriptions-OnMyMac.opml"
ARCHIVE_DIR = "/Users/shenyalan/ai-daily-news/archive"
OUTPUT_FILE = "/Users/shenyalan/ai-daily-news/daily-ai-news.md"

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
    # OPML 中已有：TechCrunch, 量子位, 新智元, Google DeepMind, OpenAI, Sakana 等
    # 仅添加 OPML 中没有的源
    "HuggingFace Blog": ("https://huggingface.co/blog/feed.xml", "US"),
}
SOURCES.update(EXTRA_SOURCES)

# ============================================================
# v5.0 研究领域细分 + 学者被引量
# ============================================================

# 顶尖AI公司列表
TIER1_AI_COMPANIES = [
    "openai", "anthropic", "google", "nvidia",
    "deepmind", "figure ai", "physical intelligence", "π",
    "z.ai", "智谱", "glm", "qwen", "minimax", "kimi",
    "deepseek", "worldlabs", "thinking machines",
    "字节", "腾讯", "阿里", "百度", "meta", "microsoft",
    "apple", "amazon", "xai", "mistral", "huggingface"
]

# ===== 研究领域细分 =====
RESEARCH_SUBFIELDS = {
    "LLM/大语言模型": {
        "keywords": ["llm", "large language model", "gpt", "chatgpt", "claude", "gemini",
                    "大模型", "语言模型", "transformer", "注意力机制", "预训练", "微调",
                    "rlhf", "dpo", "ppo", "prompt", "上下文", "token"],
        "top_authors": ["openai", "anthropic", "google deepmind", "meta ai", "stanford", "berkeley"],
        "citation_weight": 30,
    },
    "多模态": {
        "keywords": ["multimodal", "vision language", "vlm", "image generation", "video generation",
                    "图像生成", "视频生成", "文生图", "文生视频", "diffusion", "stable diffusion",
                    "sora", "dalle", "midjourney", "video", "image"],
        "top_authors": ["openai", "google deepmind", "stability ai", "midjourney", "runway"],
        "citation_weight": 28,
    },
    "世界模型/具身智能": {
        "keywords": ["world model", "embodied ai", "robotics", "robot", "autonomous",
                    "世界模型", "具身智能", "机器人", "自动驾驶", "simulation",
                    "physical intelligence", "figure", "boston dynamics"],
        "top_authors": ["physical intelligence", "figure ai", "deepmind", "boston dynamics", "tesla"],
        "citation_weight": 28,
    },
    "AI4S/科学智能": {
        "keywords": ["ai for science", "scientific ai", "biology", "protein", "drug discovery",
                    "ai4s", "科学智能", "生物", "蛋白质", "药物发现", "alphaFold",
                    "分子", "材料", "physics", "climate"],
        "top_authors": ["deepmind", "isomorphic", "alphaFold", "darpa"],
        "citation_weight": 27,
    },
    "MLSys/系统": {
        "keywords": ["mlsys", "machine learning system", "distributed training", "inference",
                    "系统", "分布式", "训练", "推理", "芯片", "gpu", "tpu", "npu",
                    "efficient", "optimization", "compiler"],
        "top_authors": ["nvidia", "google", "microsoft", "meta", "stanford", "berkeley"],
        "citation_weight": 25,
    },
    "AI安全/对齐": {
        "keywords": ["ai safety", "alignment", "interpretability", "rlhf", "capability",
                    "ai安全", "对齐", "可解释", "red team", "alignment",
                    "risks", "governance", "policy"],
        "top_authors": ["anthropic", "openai", "deepmind", "center ai safety"],
        "citation_weight": 26,
    },
    "推理/思考": {
        "keywords": ["reasoning", "thinking", "chain of thought", "o1", "o3",
                    "推理", "思考", "思维链", "数学", "code", "programming"],
        "top_authors": ["openai", "deepmind", "anthropic", "numina"],
        "citation_weight": 27,
    },
    "传统ML": {
        "keywords": ["cnn", "rnn", "reinforcement learning", "gan", "supervised",
                    "监督学习", "强化学习", "对抗", "分类", "检测", "分割"],
        "top_authors": ["stanford", "mit", "berkeley", "cmu"],
        "citation_weight": 20,
    },
}

# 学术顶会权重
TOP_CONFERENCES = {
    # 机器学习顶会
    "neurips": 25, "icml": 25, "iclr": 25,
    # 计算机视觉
    "cvpr": 24, "iccv": 24, "eccv": 22,
    # NLP/AI
    "acl": 23, "emnlp": 22, "naacl": 21,
    # 机器人/AI4S
    "iros": 20, "corl": 22, "rss": 20,
    # Science/Nature
    "nature": 30, "science": 30,
    # ArXiv
    "arxiv": 15,
}

# 学者/机构被引量 (简化版，实际可用Semantic Scholar API)
HIGH_CITATION_AUTHORS = {
    # 高被引学者/机构
    "hinton": 30, "bengio": 30, "lecun": 30,  # 图灵奖得主
    "deepmind": 28, "openai": 28, "stanford": 25,
    "berkeley": 25, "mit": 25, "cmu": 25,
    "google": 22, "meta": 22, "microsoft": 22,
    "andrew ng": 25, "karpathy": 22,
    "jeff dean": 25, "samy bengio": 24,
    "ilya": 25, "dario": 24,
    "yoshua bengio": 28, "geoffrey hinton": 28,
    "yann lecun": 28,
    # 中国学者/机构
    "清华": 20, "北大": 20, "中科院": 18,
    "浙大": 18, "上交": 18, "复旦": 18,
}

# 公司官方来源映射
OFFICIAL_SOURCES = {
    "openai": ["OpenAI News"],
    "google": ["Google DeepMind", "The Keyword", "Google Blog"],
    "deepmind": ["Google DeepMind"],
    "anthropic": ["Anthropic"],
    "nvidia": ["NVIDIA Blog"],
    "microsoft": ["Microsoft Research", "Microsoft News"],
    "meta": ["Meta AI"],
    "huggingface": ["HuggingFace Blog"],
    "karpathy": ["karpathy"],
    "sakana": ["Sakana Blog"],
}

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
SOURCE_WEIGHTS = {
    "OpenAI News": 100, "Google DeepMind": 100, "Anthropic": 100,
    "NVIDIA Blog": 100, "Figure AI": 100, "Physical Intelligence": 100,
    "World Labs": 100, "Thinking Machines Lab": 100, "Meta AI": 100,
    "Microsoft Research": 100, "HuggingFace Blog": 100,
    "karpathy": 95, "Sakana Blog": 90,
    "Y Combinator Blog": 85, "a16z": 85, "Sequoia": 80,
    "The Information": 80, "TechCrunch": 70, "Wired": 70,
    "The Verge": 70, "Ars Technica": 65,
    "量子位": 70, "新智元": 70, "机器之心": 70, "36氪": 65,
    "IT桔子": 60, "PaperWeekly": 60,
}

# 其他配置
HIGH_PRIORITY_KEYWORDS = [
    "gpt-5", "gpt-4.5", "o3", "o4", "o1", "claude 4", "gemini 2",
    "deepseek", "qwen3", "llama4", "mistral", "sora", "veo",
    "billion", "十亿", "亿美元", "acquire", "acquisition", "收购",
    "breakthrough", "state-of-the-art", "sota", "nature", "science",
    "launch", "unveil", "release", "announce", "发布", "开源",
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

    # 6. 时效性
    freshness = 1.0
    if article.get("published_parsed"):
        try:
            pub_time = datetime(*article["published_parsed"][:6], tzinfo=timezone.utc)
            hours_ago = (datetime.now(timezone.utc) - pub_time).total_seconds() / 3600
            if hours_ago < 2: freshness = 1.8
            elif hours_ago < 6: freshness = 1.5
            elif hours_ago < 12: freshness = 1.2
        except: pass

    # 综合分数
    total = (source_score + subfield_weight + conf_score + author_score + keyword_score) * freshness

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

    penalty = 0
    for kw in LOW_PRIORITY_KEYWORDS:
        if kw.lower() in text:
            penalty -= 20

    freshness = 1.0
    if article.get("published_parsed"):
        try:
            pub_time = datetime(*article["published_parsed"][:6], tzinfo=timezone.utc)
            hours_ago = (datetime.now(timezone.utc) - pub_time).total_seconds() / 3600
            if hours_ago < 2: freshness = 2.0
            elif hours_ago < 6: freshness = 1.5
            elif hours_ago < 12: freshness = 1.2
        except: pass

    quality = 0
    if len(summary) > 50: quality += 2
    if re.search(r'\d+[亿万亿]|\d+%', summary): quality += 3

    total = (source_score + company_score + keyword_score + penalty + quality) * freshness
    return total, []

# ========== 事件合并 ==========
def extract_event_key(article):
    title = article.get("title", "").lower()
    summary = article.get("summary", "").lower()
    text = title + " " + summary
    event_keywords = []
    for company in TIER1_AI_COMPANIES:
        if company in text:
            event_keywords.append(company)
    actions = ["发布", "融资", "收购", "发布", "上线", "开源", "launch", "release", "funding"]
    for action in actions:
        if action in text:
            event_keywords.append(action)
    products = ["gpt", "claude", "gemini", "llama", "sora", "deepseek"]
    for p in products:
        if p in text:
            event_keywords.append(p)
    return frozenset(event_keywords) if event_keywords else None

def merge_events(articles):
    events = defaultdict(list)
    for a in articles:
        key = extract_event_key(a)
        if key:
            events[key].append(a)
        else:
            events[frozenset([a.get("title", "")[:20]])].append(a)

    merged = []
    for key, arts in events.items():
        if len(arts) == 1:
            merged.append(arts[0])
        else:
            arts = sorted(arts, key=lambda x: x.get("priority", 0), reverse=True)
            primary = arts[0]
            sources = list(set(a.get("source", "") for a in arts))
            summaries = [a.get("summary", "") for a in arts if a.get("summary")]
            best_summary = max(summaries, key=len) if summaries else ""
            primary["merged_sources"] = sources
            primary["summary"] = best_summary
            primary["is_merged"] = True
            primary["source_count"] = len(arts)
            merged.append(primary)
    return merged

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
                "moe", "transformer", "vla", "agent"],
    
    # 算力追踪：硬件、芯片、云服务
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
CATEGORY_PRIORITY = {"模型前沿": 1, "产业动态": 2, "算力追踪": 3, "初创&融资": 4, "研究关注": 5, "其他": 6}

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
    unique = []
    for a in articles:
        is_dup = False
        for i, u in enumerate(unique):
            if a["source"] == u["source"]:
                continue
            sim = calc_similarity(a["title"], u["title"])
            title_a, title_u = normalize(a["title"]), normalize(u["title"])
            if sim > 0.6 or title_a in title_u or title_u in title_a:
                if a["priority"] > u["priority"]:
                    unique[i] = a
                is_dup = True
                break
        if not is_dup:
            unique.append(a)
    return unique

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
        "model": "MiniMax-M2.5",
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

### 分类规则
- 模型前沿：模型发布、benchmark、多模态、视频生成
- 产业动态：商业、合作、用户增长、政策
- 算力追踪：芯片、硬件、半导体设备
- 初创&融资：融资、投资
- 研究关注：论文、学术、CVPR/ICML

## 输出格式
JSON数组，按顺序输出：
[
  {
    "title": "【新闻1】是什么+为什么重要（不用媒体口吻）",
    "body": "【新闻1】2句话的完整摘要，说明发生了什么",
    "key_points": ["【新闻1】要点1（从body提取，不要重复body内容）", "【新闻1】要点2"],
    "is_ai_related": true/false,
    "category": "分类"
  },
  ...
]

## 重要
- title格式：事件主体+做什么/发布什么+为什么重要（不用感叹号、不用媒体夸张口吻）
  - 错误示例：「彻底告别VE与VAE！商汤硬核重构多模态」「GPU时代落幕？硅谷巨头集体叛逃」
  - 正确示例：「商汤发布新多模态架构：砍掉中间编码器，2B参数超越传统范式」「英伟达投入1500亿自研芯片：应对巨头叛逃，GPU时代或终结」
- body必须是一段完整的2句话摘要，不能只是关键词
- key_points从body中提取新信息，不要重复body已说的内容
- 必须按新闻顺序输出，不要跳序
- 标题用原文标题""",
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
        recent_summary = f"\n\n## 近期动态(供参考关联)\n" + "\n".join([f"- {t}" for t in recent_titles])

    # 构建清晰的新闻列表，每条独立
    news_list = []
    for i, a in enumerate(articles[:15]):  # 减少到15条，避免混淆
        summary = a.get('summary', '') or a.get('content', '')
        news_list.append(f"""【新闻{i+1}】
标题：{a['title']}
来源：{a['source']}
摘要：{summary[:300]}""")
    
    prompt = "你是一个AI新闻处理器。请严格按照下方每条新闻的顺序处理，不要混淆。\n\n" + "\n\n".join(news_list)
    result = call_llm(prompt)
    if not result:
        return articles
    try:
        import json as json_module
        import re as re_module
        # 尝试多种方式解析JSON
        json_match = re_module.search(r'\[[\s\S]*\]', result)
        if json_match:
            try:
                llm_results = json_module.loads(json_match.group())
            except:
                # 尝试修复常见的JSON问题
                import json
                raw = json_match.group()
                # 移除可能的markdown代码块
                raw = raw.strip().strip('`').strip()
                llm_results = json_module.loads(raw)
            filtered_articles = []
            for i, lr in enumerate(llm_results):
                if i >= len(articles):
                    break
                
                # 保存原始标题
                orig_title = articles[i].get('title', '')
                orig_summary = articles[i].get('summary', '')
                    
                # LLM 判断是否AI相关
                is_ai = lr.get('is_ai_related', True)
                if is_ai is False:
                    print(f"   LLM过滤: {articles[i]['title'][:30]}...")
                    continue
                    
                llm_title = lr.get('title', '')
                
                # 使用 LLM 生成的标题（如果有效的话）
                llm_title = lr.get('title', '')
                if llm_title and len(llm_title) > 5:
                    articles[i]['title'] = llm_title[:80]
                else:
                    articles[i]['title'] = orig_title[:80]
                
                # 使用 LLM 判断的分类
                llm_cat = lr.get('category', '')
                if llm_cat:
                    articles[i]['categories'] = [llm_cat]
                
                # 使用 LLM 生成的 body（精简版）
                llm_body = lr.get('body', '')
                if llm_body and len(llm_body) > 10:
                    articles[i]['body'] = llm_body[:150]
                else:
                    # 用原文摘要但截断
                    articles[i]['body'] = orig_summary[:150] if orig_summary else orig_title[:150]
                
                # 使用 LLM 的 key_points
                articles[i]['key_points'] = lr.get('key_points', [])[:3]
                articles[i]['related'] = lr.get('related', '')
                filtered_articles.append(articles[i])
            
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
                "published_parsed": e.get("published_parsed"),
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

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注"]:
        items = by_cat.get(cat, [])
        if items:
            # 要点速览只显示"是什么"（取冒号之前的部分）
            def get_what(title):
                # 取冒号、问号、感叹号之前的部分作为"是什么"
                for sep in ['：', ':', '？', '?', '！', '!']:
                    if sep in title:
                        return title.split(sep)[0][:35]
                return title[:35]
            titles = "; ".join([get_what(a['title']) for a in items[:3]])
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
            # 关键点 - 至少2处加粗
            if a.get('key_points'):
                for point in a['key_points'][:4]:
                    lines.append(f"   - **{point}**")
            # 关联解读
            if a.get('related'):
                lines.append(f"   > 关联: {a['related']}")
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
            # 关键点 - 至少2处加粗
            if a.get('key_points'):
                for point in a['key_points'][:4]:
                    lines.append(f"   - **{point}**")
            lines.append(f"   - 来源: {a['source']}")
            lines.append("")

    lines.extend(["", "---", f"*更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*"])
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
    # Anthropic 和 X/Twitter 抓取已禁用，改为从 TechCrunch RSS 追踪
    print(f"🤖 AI前沿动态 v5.0")

    print(f"🤖 AI前沿动态 v5.0")
    print(f"   特性: 研究关注按领域+被引量排序")
    print(f"   时间窗口: {START_BJ.strftime('%Y-%m-%d %H:%M')} - {END_BJ.strftime('%Y-%m-%d %H:%M')} 北京时间")

    all_arts, errors = [], []
    for name, (url, tz) in SOURCES.items():
        # 跳过播客源
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

    unique = dedup_articles(all_arts)
    print(f"\n📊 去重后: {len(unique)} 条")

    print("🔗 合并多源事件...")
    merged = merge_events(unique)
    print(f"📊 合并后: {len(merged)} 条")

    merged = sorted(merged, key=lambda x: x.get("priority", 0), reverse=True)

    # 第一次规范化（在LLM之前），主要过滤明显的非新闻
    print("🔧 预规范化...")
    merged = improve_news(merged, do_filter=True)

    if len(merged) < MIN_ARTICLES:
        print(f"📊 文章不足 {MIN_ARTICLES} 篇，保留全部 {len(merged)} 篇")

    # 读取历史存档用于关联分析
    recent_articles = []
    if API_KEY and len(merged) > 5:
        print("📚 读取近期存档用于关联分析...")
        recent_articles = load_recent_archives(days=3)
        print(f"   读取到 {len(recent_articles)} 条历史文章")

    if API_KEY and len(merged) > 5:
        print("🤖 调用LLM提取要点(含关联分析)...")
        merged = process_with_llm(merged, recent_articles)
    
    # LLM处理后不再过滤（LLM已判断is_ai_related），只做分类修正和去重
    print("🔧 LLM后规范化（分类修正）...")
    merged = improve_news(merged, do_filter=False)

    by_cat = defaultdict(int)
    for a in merged:
        for c in a["categories"]: by_cat[c] += 1
    print(f"📂 分类: ", end="")
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注"]:
        print(f"{cat}{by_cat.get(cat,0)} ", end="")
    print("")

    # 研究子领域统计
    research_arts = [a for a in merged if "研究关注" in a.get("categories", [])]
    subfield_count = defaultdict(int)
    for a in research_arts:
        subfield_count[a.get("subfield", "其他研究")] += 1
    if subfield_count:
        print(f"📚 研究子领域: ", end="")
        for sf, cnt in sorted(subfield_count.items(), key=lambda x: SUBFIELD_ORDER.get(x[0], 9)):
            print(f"{sf}{cnt} ", end="")
        print("")

    if errors:
        print(f"⚠️ 失败: {errors[:3]}")

    report = generate_report(merged)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    save_archive(merged)
    print(f"✅ 已输出: {OUTPUT_FILE}")

    # 生成HTML版本
    try:
        import subprocess
        subprocess.run(['python', 'generate_html.py'], check=True, capture_output=True)
    except:
        pass

if __name__ == "__main__":
    main()
