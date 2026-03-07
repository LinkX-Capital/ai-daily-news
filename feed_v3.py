#!/usr/bin/env python3
"""
AI 前沿动态 - v3.1
重点优化：统一顶尖AI公司优先级
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
# 优先级排序机制 v3.1
# 核心原则：顶尖AI公司优先级一致
# ============================================================

# 顶尖AI公司列表 (统一最高优先级)
TIER1_AI_COMPANIES = [
    "openai", "anthropic", "google", "nvidia",
    "deepmind", "figure ai", "physical intelligence", "π",
    "z.ai", "智谱", "glm", "qwen", "minimax", "kimi",
    "deepseek", "worldlabs", "thinking machines",
    "字节", "腾讯", "阿里", "百度", "meta", "microsoft",
    "apple", "amazon", "xai", "mistral"
]

# 1. 来源权重 (1-100)
SOURCE_WEIGHTS = {
    # ===== 第一梯队: 顶尖AI公司/实验室 =====
    # 这些公司优先级一致
    "OpenAI News": 100,
    "Google DeepMind": 100,
    "Anthropic": 100,
    "NVIDIA Blog": 100,
    "Figure AI": 100,
    "Physical Intelligence": 100,
    "World Labs": 100,
    "Thinking Machines Lab": 100,
    "Meta AI": 100,
    "Microsoft Research": 100,

    # ===== 第二梯队: 顶级风投 ===== (关注AI投资动态)
    "Y Combinator Blog": 90, "a16z": 90, "Sequoia": 85,

    # ===== 第三梯队: AI研究者/评论者 =====
    "karpathy": 90,
    "Latent Space": 85, "Lilian Weng": 85,
    "Sakana Blog": 85,

    # ===== 第四梯队: 顶级科技媒体 =====
    "The Information": 80, "TechCrunch": 75, "Wired": 70,
    "The Verge": 70, "Ars Technica": 65,

    # ===== 第五梯队: 中文科技媒体 =====
    "量子位": 70, "新智元": 70, "机器之心": 70, "36氪": 65,
    "IT桔子": 60, "PaperWeekly": 60,
}

# 2. 分类内重要公司权重 (同一分类内再细分)
# 核心：顶尖AI公司权重一致
COMPANY_WEIGHTS = {
    # 模型类 - 所有顶尖AI公司权重相同
    "模型前沿": {
        # 顶尖AI公司 (权重相同)
        "openai": 25, "gpt": 25, "chatgpt": 25,
        "anthropic": 25, "claude": 25,
        "google": 25, "gemini": 25, "deepmind": 25,
        "nvidia": 25,
        "meta": 25, "llama": 25,
        "microsoft": 25,
        "deepseek": 25, "qwen": 25, "minimax": 25, "kimi": 25,
        "字节": 25, "阿里": 25, "百度": 25, "腾讯": 25,
        "figure": 25, "physical intelligence": 25, "π": 25,
        "worldlabs": 25, "thinking machines": 25,
        # 产品/技术
        "sora": 20, "veo": 20, "视频生成": 18,
    },
    # 产业类
    "产业动态": {
        # 顶尖AI公司 (权重相同)
        "openai": 25, "google": 25, "microsoft": 25, "nvidia": 25,
        "meta": 25, "apple": 25, "amazon": 25,
        "字节": 25, "腾讯": 25, "阿里": 25, "百度": 25, "华为": 25,
        "anthropic": 25, "figure": 20, "physical intelligence": 20,
        "deepseek": 25, "minimax": 25, "kimi": 25, "qwen": 25,
        # 重要领域
        "机器人": 20, "自动驾驶": 20, "特斯拉": 20,
    },
    # 算力类 - NVIDIA为主
    "算力追踪": {
        "nvidia": 30, "h100": 28, "h200": 28, "blackwell": 28,
        "amd": 20, "intel": 15, "google": 15, "tpu": 15,
        "aws": 15, "azure": 15, "云计算": 15,
    },
    # 融资类
    "初创&融资": {
        # 顶尖AI公司融资
        "openai": 25, "anthropic": 25, "xai": 25,
        "deepseek": 25, "minimax": 25, "kimi": 25,
        "figure": 25, "physical intelligence": 25,
        "worldlabs": 25, "thinking machines": 25,
        # 融资相关
        "独角兽": 20, "估值": 20, "ipo": 20,
        "a轮": 15, "b轮": 15, "c轮": 18, "d轮": 18,
    },
    # 研究类
    "研究关注": {
        "nature": 20, "science": 20,
        "icml": 18, "neurips": 18, "cvpr": 18, "acl": 18,
        "arXiv": 15, "论文": 12,
    }
}

# 3. 热度关键词 (同类内加分)
HIGH_PRIORITY_KEYWORDS = [
    # 重大模型发布
    "gpt-5", "gpt-4.5", "o3", "o4", "o1", "claude 4", "gemini 2",
    "deepseek", "qwen3", "llama4", "mistral", "sora", "veo",
    "world model", "reasoning model", "thinking model",
    # 大额融资
    "billion", "十亿", "亿美元", "100亿", "1000亿", "funding round",
    # 收购/并购
    "acquire", "acquisition", "收购", "并购",
    # 突破性成果
    "breakthrough", "state-of-the-art", "sota", "benchmark",
    "nature", "science", "首次", "第一", "最强",
    # 重大产品发布
    "launch", "unveil", "release", "announce", "发布", "开源",
    # 中文热门
    "秒杀", "超越", "突破",
]

# 4. 低优先级关键词 (过滤/降权)
LOW_PRIORITY_KEYWORDS = [
    "advertisement", "sponsored", "招聘", "求职", "课程", "培训",
    "webinar", "抽奖", "活动", "meetup", "conference agenda",
    "广告", "推广", "招商", "报名", "参会",
]

# 5. 时效性权重
def get_freshness_weight(published_parsed):
    if not published_parsed:
        return 1.0
    try:
        pub_time = datetime(*published_parsed[:6], tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        hours_ago = (now - pub_time).total_seconds() / 3600
        if hours_ago < 2: return 2.0
        if hours_ago < 6: return 1.5
        if hours_ago < 12: return 1.2
        if hours_ago < 24: return 1.0
        return 0.8
    except:
        return 1.0

# 6. 内容质量评估
def get_content_quality_score(article):
    title = article.get("title", "")
    summary = article.get("summary", "")

    score = 0
    if len(title) > 10: score += 1
    if len(title) < 80: score += 1
    if len(summary) > 50: score += 2
    if len(summary) > 150: score += 1
    if re.search(r'\d+[亿万亿]|\d+%|[Bb]\d+|[Mm]\d+', summary):
        score += 3
    companies = ["openai", "google", "nvidia", "microsoft", "meta", "apple", "amazon"]
    if any(c in summary.lower() for c in companies):
        score += 2

    return score

# ============================================================
# 计算综合优先级分数
# ============================================================
def calculate_priority(article, category=None):
    source = article.get("source", "")
    title = article.get("title", "").lower()
    summary = article.get("summary", "").lower()
    text = title + " " + summary

    # 1. 来源基础分 (0-100)
    source_score = SOURCE_WEIGHTS.get(source, 50)

    # 2. 分类内公司权重 (0-30)
    company_score = 0
    if category and category in COMPANY_WEIGHTS:
        for kw, weight in COMPANY_WEIGHTS[category].items():
            if kw in text:
                company_score = max(company_score, weight)
    else:
        for kw, weight in [(c, 20) for c in TIER1_AI_COMPANIES]:
            if kw in text:
                company_score = max(company_score, weight)

    # 3. 热度关键词加分 (0-30)
    keyword_score = 0
    for kw in HIGH_PRIORITY_KEYWORDS:
        if kw.lower() in text:
            keyword_score += 10
    keyword_score = min(keyword_score, 30)

    # 4. 低优先级惩罚 (-30-0)
    penalty = 0
    for kw in LOW_PRIORITY_KEYWORDS:
        if kw.lower() in text:
            penalty -= 20
    penalty = max(penalty, -30)

    # 5. 时效性权重 (0.8-2.0)
    freshness = get_freshness_weight(article.get("published_parsed"))

    # 6. 内容质量 (0-10)
    quality = get_content_quality_score(article)

    # 综合分数
    total = (source_score + company_score + keyword_score + penalty + quality) * freshness
    return total

# ============================================================
# 其他配置
# ============================================================
CATEGORIES = {
    "模型前沿": ["LLM", "大模型", "GPT", "Claude", "Gemini", "Qwen", "DeepSeek", "MoE", "Transformer", "VLA", "R1", "o1", "图像生成", "视频生成", "Sora", "Veo", "世界模型", "具身智能", "benchmark", "评测", "模型", "Agent", "multimodal", "reasoning", "world model", "frontier model", "thinking model", "model"],
    "算力追踪": ["GPU", "NPU", "TPU", "H100", "H200", "B100", "Blackwell", "芯片", "算力", "定价", "价格", "token", "成本", "云计算", "AWS", "Azure", "inference", "training", "compute", "NVIDIA", "AMD", "data center", "cluster"],
    "产业动态": ["产品", "发布", "上线", "更新", "合作", "战略", "部署", "硬件", "机器人", "自动驾驶", "智驾", "Apple", "Meta", "Microsoft", "字节", "阿里", "百度", "腾讯", "华为", "Amazon", "launch", "release", "update", "product", "partner", "announce", "partnership"],
    "初创&融资": ["融资", "投资", "Funding", "Round", "估值", "IPO", "收购", "并购", "亿元", "亿美元", "A轮", "B轮", "C轮", "独角兽", "funding", "raise", "acquire", "valuation", "unicorn", "series", "seed", "startup"],
    "研究关注": ["论文", "研究", "Nature", "ICML", "NeurIPS", "CVPR", "ACL", "arXiv", "学者", "教授", "实验室", "paper", "research", "algorithm", "preprint", "academic"],
}
CATEGORY_PRIORITY = {"模型前沿": 1, "产业动态": 2, "算力追踪": 3, "初创&融资": 4, "研究关注": 5, "其他": 6}

MAX_PER_CATEGORY = 8
MIN_ARTICLES = 30

# ========== 工具函数 ==========
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
        "system": """你是一位资深AI行业分析师，负责从AI新闻中提取关键信息。

## 输出格式要求
直接输出JSON数组，不要有任何解释。每个元素格式：
{"title": "简化后的标题", "summary": "1句话要点", "impact": "影响/意义", "category": "分类"}

## 质量标准
- 标题简洁，不超过30字
- summary 必须包含关键数据（金额、比例等）
- impact 描述对行业的影响
- 只输出有效新闻，过滤广告/招聘/无效内容""",
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

def process_with_llm(articles):
    if not API_KEY or len(articles) < 5:
        return articles
    news_list = []
    for i, a in enumerate(articles[:20]):
        news_list.append(f"{i+1}. 标题: {a['title']}\n   来源: {a['source']}\n   摘要: {a.get('summary', '')[:200]}")
    prompt = f"处理以下AI新闻，提取关键信息：\n\n" + "\n".join(news_list)
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
                    articles[i]['summary'] = lr.get('summary', articles[i].get('summary', ''))
                    articles[i]['impact'] = lr.get('impact', '')
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
            article["priority"] = calculate_priority(article, primary_cat)
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

    for c in by_cat:
        by_cat[c] = sorted(by_cat[c], key=lambda x: x.get("priority", 0), reverse=True)[:MAX_PER_CATEGORY]

    lines = [f"## {month_day} AI 前沿动态", "", f"> 自动汇总 | 时间窗口: 24h | 来源: {len(SOURCES)}个RSS", "", "---", ""]

    lines.extend(["# 📌 要点速览", ""])
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注"]:
        items = by_cat.get(cat, [])
        if items:
            highlights = []
            for a in items[:3]:
                title = a['title'][:35] + "..." if len(a['title']) > 35 else a['title']
                highlights.append(title)
            lines.append(f"**{cat}**: {' | '.join(highlights)}")

    lines.extend(["", "---", "", "# 📖 详细参考", ""])
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "其他"]:
        items = by_cat.get(cat, [])
        if not items: continue
        lines.append(f"## 🔹 {cat}")
        for a in items:
            priority = a.get("priority", 0)
            priority_emoji = "🔥" if priority > 150 else "📰" if priority > 100 else "📄"
            lines.append(f"{priority_emoji} **{a['title']}** (优先级:{int(priority)})")
            if a.get('impact'):
                lines.append(f"   > {a['impact']}")
            lines.append(f"   - 来源: {a['source']} | [原文]({a['link']})")
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
def main():
    print(f"🤖 AI前沿动态 v3.1")
    print(f"   优先级: 顶尖AI公司(OpenAI/Anthropic/Google/NVIDIA等)权重一致")
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
    unique = sorted(unique, key=lambda x: x.get("priority", 0), reverse=True)

    if len(unique) < MIN_ARTICLES:
        print(f"📊 文章不足 {MIN_ARTICLES} 篇，保留全部 {len(unique)} 篇")

    print(f"\n📊 {len(all_arts)} → {len(unique)} 条")

    if API_KEY and len(unique) > 5:
        print("🤖 调用LLM提取要点...")
        unique = process_with_llm(unique)

    by_cat = defaultdict(int)
    for a in unique:
        for c in a["categories"]: by_cat[c] += 1
    print(f"📂 分类: ", end="")
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注"]:
        print(f"{cat}{by_cat.get(cat,0)} ", end="")
    print("")

    if errors:
        print(f"⚠️ 失败: {errors[:3]}")

    report = generate_report(unique)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    save_archive(unique)
    print(f"✅ 已输出: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
