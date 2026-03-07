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
    "HuggingFace Blog": ("https://huggingface.co/blog/feed.xml", "US"),
    "Microsoft News": ("https://news.microsoft.com/source/feed/", "US"),
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
CATEGORIES = {
    "模型前沿": ["LLM", "大模型", "GPT", "Claude", "Gemini", "Qwen", "DeepSeek", "MoE", "Transformer", "VLA", "R1", "o1", "图像生成", "视频生成", "Sora", "Veo", "世界模型", "具身智能", "benchmark", "评测", "模型", "Agent", "multimodal", "reasoning", "world model", "frontier model", "thinking model", "model"],
    "算力追踪": ["GPU", "NPU", "TPU", "H100", "H200", "B100", "Blackwell", "芯片", "算力", "定价", "价格", "token", "成本", "云计算", "AWS", "Azure", "inference", "training", "compute", "NVIDIA", "AMD", "data center", "cluster"],
    "产业动态": ["产品", "发布", "上线", "更新", "合作", "战略", "部署", "硬件", "机器人", "自动驾驶", "智驾", "Apple", "Meta", "Microsoft", "字节", "阿里", "百度", "腾讯", "华为", "Amazon", "launch", "release", "update", "product", "partner", "announce", "partnership"],
    "初创&融资": ["融资", "投资", "Funding", "Round", "估值", "IPO", "收购", "并购", "亿元", "亿美元", "A轮", "B轮", "C轮", "独角兽", "funding", "raise", "acquire", "valuation", "unicorn", "series", "seed", "startup"],
    "研究关注": ["论文", "研究", "Nature", "ICML", "NeurIPS", "CVPR", "ACL", "arXiv", "学者", "教授", "实验室", "paper", "research", "algorithm", "preprint", "academic"],
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

def is_in_window(entry):
    d = parse_date(entry)
    return False if d is None else START_UTC <= d <= END_UTC

def get_cat(title, summary):
    text = (title + " " + (summary or "")).lower()
    scores = {}
    for cat, keywords in CATEGORIES.items():
        score = sum(1 for k in keywords if k.lower() in text)
        if score > 0:
            scores[cat] = score
    if not scores:
        return ["其他"]
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
        "system": """你是一位顶尖AI行业研究员，负责提炼前沿动态。

## 输出格式
直接输出JSON数组，不要有任何解释。每个元素格式：
{
  "title": "事件核心一句话概括",
  "body": "2-3句简短说明，包含：是什么+为什么重要+影响",
  "key_points": ["关键判断1", "关键判断2", "关键数据"],
  "related": "与近期动态的关联解读(如有)",
  "category": "分类"
}

## 严格标准
1. body控制在2-3句话，简短有力
2. key_points 2-3个，一句话一条，供扫读
3. related：如有关联写一句，否则空
4. 过滤广告/招聘/无效内容""",
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

def process_with_llm(articles, recent_articles=None):
    if recent_articles is None:
        recent_articles = []
    if not API_KEY or len(articles) < 5:
        return articles

    # 构建历史动态摘要
    recent_summary = ""
    if recent_articles:
        recent_titles = [a["title"][:40] for a in recent_articles[-15:]]
        recent_summary = f"\n\n## 近期动态(供参考关联)\n" + "\n".join([f"- {t}" for t in recent_titles])

    news_list = []
    for i, a in enumerate(articles[:20]):
        source_info = ""
        if a.get("is_merged"):
            source_info = f" (综合{a.get('source_count', 1)}个来源)"
        news_list.append(f"{i+1}. 标题: {a['title']}\n   来源: {a['source']}{source_info}\n   摘要: {a.get('summary', '')[:200]}")
    # 构建prompt，加入历史信息
    prompt = f"处理以下AI新闻，提取关键信息：\n\n" + "\n".join(news_list) + recent_summary
    result = call_llm(prompt)
    if not result:
        return articles
    try:
        import json as json_module
        json_match = re.search(r'\[[\s\S]*\]', result)
        if json_match:
            llm_results = json_module.loads(json_match.group())
            for i, lr in enumerate(llm_results):
                if i < len(articles):
                    articles[i]['title'] = lr.get('title', articles[i]['title'])
                    articles[i]['body'] = lr.get('body', '')  # 正文：是什么+为什么+影响
                    articles[i]['key_points'] = lr.get('key_points', [])  # 关键点
                    articles[i]['related'] = lr.get('related', '')  # 关联解读
                    articles[i]['category'] = lr.get('category', '')
            print(f"✅ LLM处理了 {len(llm_results)} 条新闻")
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

    lines = [f"## {month_day} AI 前沿动态", "", f"> 自动汇总 | 时间窗口: 24h | 来源: {len(SOURCES)}个RSS", "", "---", ""]
    lines.extend([f"# 📌 要点速览", "", f"📊 共 {len(articles)} 条新闻 (含 {merged_count} 条多源合并)", ""])

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注"]:
        items = by_cat.get(cat, [])
        if items:
            highlights = []
            for a in items[:3]:
                title = a['title'][:35] + "..." if len(a['title']) > 35 else a['title']
                if a.get("is_merged"):
                    title = f"🔗{title}"
                highlights.append(title)
            lines.append(f"**{cat}**: {' | '.join(highlights)}")

    lines.extend(["", "---", "", "# 📖 详细参考", ""])

    # 模型前沿
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资"]:
        items = by_cat.get(cat, [])
        if not items: continue
        lines.append(f"## 🔹 {cat}")
        for a in items:
            priority = a.get("priority", 0)
            priority_emoji = "🔥" if priority > 150 else "📰" if priority > 100 else "📄"

            if a.get("is_merged"):
                sources_str = " | ".join(a.get("merged_sources", []))
                source_line = f"   - 来源: {sources_str} ({a.get('source_count')}源合并)"
            else:
                source_line = f"   - 来源: {a['source']}"

            lines.append(f"{priority_emoji} **{a['title']}**")
            # 正文
            if a.get('body'):
                lines.append(f"   {a['body']}")
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
        lines.append("## 🔹 研究关注")
        for a in research_items:
            priority = a.get("priority", 0)
            priority_emoji = "🔥" if priority > 150 else "📰" if priority > 100 else "📄"
            lines.append(f"{priority_emoji} **{a['title']}**")
            # 正文
            if a.get('body'):
                lines.append(f"   {a['body']}")
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
    beijing_offset = 8
    now_utc = datetime.now(timezone.utc)
    now_beijing = now_utc + timedelta(hours=beijing_offset)
    end_beijing = now_beijing.replace(hour=9, minute=0, second=0, microsecond=0)
    if now_beijing.hour < 9:
        end_beijing = end_beijing - timedelta(days=1)
    start_beijing = end_beijing - timedelta(days=1)
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
    print(f"🤖 AI前沿动态 v5.0")
    print(f"   特性: 研究关注按领域+被引量排序")
    print(f"   时间窗口: {START_BJ.strftime('%Y-%m-%d %H:%M')} - {END_BJ.strftime('%Y-%m-%d %H:%M')} 北京时间")

    all_arts, errors = [], []
    for name, (url, tz) in SOURCES.items():
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

if __name__ == "__main__":
    main()
