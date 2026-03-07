#!/usr/bin/env python3
"""
AI 前沿动态 - 改进版管线
- 更详细的优先级排序机制
- LLM 提取要点
- 历史存档
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

# 确保archive目录存在
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

# ========== 优先级排序机制 ==========
# 1. 来源权重 (1-100, 越高越重要)
SOURCE_WEIGHTS = {
    # 顶级AI实验室/公司
    "OpenAI News": 95, "Google DeepMind": 95, "Anthropic": 95,
    "NVIDIA Blog": 90, "Microsoft Research": 90,
    # 顶级科技媒体
    "TechCrunch": 70, "The Information": 75, "Wired": 65,
    "The Verge": 65, "Ars Technica": 60,
    # 顶级风投
    "Y Combinator Blog": 80, "a16z": 80, "Sequoia": 75,
    # AI研究者
    "karpathy": 85, "Sakana Blog": 80, "Thinking Machines Lab": 80,
    "Latent Space": 75, "Lilian Weng": 75,
    # 中文科技媒体
    "量子位": 60, "新智元": 60, "机器之心": 60, "36氪": 55,
    "IT桔子": 50, "PaperWeekly": 50,
}

# 2. 内容热度关键词 (影响分数)
HIGH_PRIORITY_KEYWORDS = [
    # 模型发布/突破
    "gpt-5", "gpt-4.5", "o3", "o4", "claude 4", "gemini 2",
    "deepseek", "qwen3", "llama4", "mistral", "sora", "veo",
    # 大额融资
    "billion", "十亿", "亿美元", "100", "1000", "funding round",
    # 收购/并购
    "acquire", "acquisition", "收购", "并购",
    # 突破性研究
    "breakthrough", "state-of-the-art", "sota", "benchmark",
    "nature", "science", "icml", "neurips", "cvpr",
    # 重大产品发布
    "launch", "unveil", "release", "announce", "发布", "开源",
]

# 3. 低优先级关键词 (过滤)
LOW_PRIORITY_KEYWORDS = [
    "advertisement", "sponsored", "招聘", "求职", "课程", "培训",
    "webinar", "抽奖", "活动", "meetup", "conference agenda",
]

# 4. 时效性权重 (小时内的新闻权重更高)
def get_freshness_weight(published_parsed):
    """根据发布时间计算时效性权重"""
    if not published_parsed:
        return 1.0
    try:
        pub_time = datetime(*published_parsed[:6], tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        hours_ago = (now - pub_time).total_seconds() / 3600
        if hours_ago < 2: return 2.0
        if hours_ago < 6: return 1.5
        if hours_ago < 12: return 1.2
        return 1.0
    except:
        return 1.0

# 5. 计算综合优先级
def calculate_priority(article):
    """综合计算文章优先级分数"""
    source = article.get("source", "")
    title = article.get("title", "").lower()
    summary = article.get("summary", "").lower()

    # 来源基础分
    source_score = SOURCE_WEIGHTS.get(source, 50)

    # 热度关键词加分
    keyword_score = 0
    text = title + " " + summary
    for kw in HIGH_PRIORITY_KEYWORDS:
        if kw.lower() in text:
            keyword_score += 10
    keyword_score = min(keyword_score, 30)  # 最多加30分

    # 低优先级关键词减分
    penalty = 0
    for kw in LOW_PRIORITY_KEYWORDS:
        if kw.lower() in text:
            penalty -= 20
    penalty = max(penalty, -30)  # 最多减30分

    # 时效性权重
    freshness = get_freshness_weight(article.get("published_parsed"))

    # 综合分数
    total = (source_score + keyword_score + penalty) * freshness
    return total

# ========== 时间窗口 ==========
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

# ========== 分类 ==========
CATEGORIES = {
    "模型前沿": ["LLM", "大模型", "GPT", "Claude", "Gemini", "Qwen", "DeepSeek", "MoE", "Transformer", "VLA", "R1", "o1", "图像生成", "视频生成", "Sora", "Veo", "世界模型", "具身智能", "benchmark", "评测", "模型", "Agent", "multimodal", "reasoning", "world model", "frontier model", "thinking model", "model"],
    "算力追踪": ["GPU", "NPU", "TPU", "H100", "H200", "B100", "Blackwell", "芯片", "算力", "定价", "价格", "token", "成本", "云计算", "AWS", "Azure", "inference", "training", "compute", "NVIDIA", "AMD", "data center", "cluster"],
    "产业动态": ["产品", "发布", "上线", "更新", "合作", "战略", "部署", "硬件", "机器人", "自动驾驶", "智驾", "Apple", "Meta", "Microsoft", "字节", "阿里", "百度", "腾讯", "华为", "Amazon", "launch", "release", "update", "product", "partner", "announce", "partnership"],
    "初创&融资": ["融资", "投资", "Funding", "Round", "估值", "IPO", "收购", "并购", "亿元", "亿美元", "A轮", "B轮", "C轮", "独角兽", "funding", "raise", "acquire", "valuation", "unicorn", "series", "seed", "startup"],
    "研究关注": ["论文", "研究", "Nature", "ICML", "NeurIPS", "CVPR", "ACL", "arXiv", "学者", "教授", "实验室", "paper", "research", "algorithm", "preprint", "academic"],
}
CATEGORY_PRIORITY = {"模型前沿": 1, "产业动态": 2, "算力追踪": 3, "初创&融资": 4, "研究关注": 5, "其他": 6}

MAX_PER_CATEGORY = 8
MIN_ARTICLES = 30  # 最少保留文章数

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

# ========== 相似度去重 ==========
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
    """去重：相似度>0.6视为重复"""
    unique = []
    for a in articles:
        is_dup = False
        for i, u in enumerate(unique):
            if a["source"] == u["source"]:
                continue
            sim = calc_similarity(a["title"], u["title"])
            title_a, title_u = normalize(a["title"]), normalize(u["title"])
            if sim > 0.6 or title_a in title_u or title_u in title_a:
                # 保留分数高的
                if a["priority"] > u["priority"]:
                    unique[i] = a
                is_dup = True
                break
        if not is_dup:
            unique.append(a)
    return unique

# ========== LLM 摘要生成 ==========
def call_llm(prompt):
    """调用 MiniMax API"""
    if not API_KEY:
        print("⚠️ 未配置 LLM API Key，跳过LLM处理")
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
    """使用LLM处理文章"""
    if not API_KEY or len(articles) < 5:
        return articles

    # 准备输入
    news_list = []
    for i, a in enumerate(articles[:20]):  # 每次最多处理20条
        news_list.append(f"{i+1}. 标题: {a['title']}\n   来源: {a['source']}\n   摘要: {a.get('summary', '')[:200]}")

    prompt = f"处理以下AI新闻，提取关键信息：\n\n" + "\n".join(news_list)

    result = call_llm(prompt)
    if not result:
        return articles

    # 解析JSON结果
    try:
        # 尝试提取JSON数组
        import json as json_module
        json_match = re.search(r'\[[\s\S]*\]', result)
        if json_match:
            llm_results = json_module.loads(json_match.group())
            # 合并LLM结果
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
            article = {
                "title": title,
                "summary": summary[:150] if summary else "",
                "content": summary,
                "link": link,
                "categories": cats,
                "source": name,
                "published_parsed": e.get("published_parsed"),
            }
            article["priority"] = calculate_priority(article)
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

    # 要点汇总
    lines.extend(["# 📌 要点速览", ""])
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注"]:
        items = by_cat.get(cat, [])
        if items:
            # 取前3条的核心一句话
            highlights = []
            for a in items[:3]:
                title = a['title'][:35] + "..." if len(a['title']) > 35 else a['title']
                highlights.append(title)
            lines.append(f"**{cat}**: {' | '.join(highlights)}")

    # 详情
    lines.extend(["", "---", "", "# 📖 详细参考", ""])
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "其他"]:
        items = by_cat.get(cat, [])
        if not items: continue
        lines.append(f"## 🔹 {cat}")
        for a in items:
            priority_emoji = "🔥" if a.get("priority", 0) > 100 else "📰"
            lines.append(f"{priority_emoji} **{a['title']}**")
            if a.get('impact'):
                lines.append(f"   > {a['impact']}")
            lines.append(f"   - 来源: {a['source']} | [原文]({a['link']})")
            lines.append("")

    lines.extend(["", "---", f"*更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*"])

    return "\n".join(lines)

# ========== 保存历史 ==========
def save_archive(articles):
    """保存到历史存档"""
    date_str = END_BJ.strftime("%Y-%m-%d")
    archive_file = os.path.join(ARCHIVE_DIR, f"news_{date_str}.json")

    data = {
        "date": date_str,
        "count": len(articles),
        "articles": articles
    }

    with open(archive_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ 已存档: {archive_file}")

# ========== 主函数 ==========
def main():
    print(f"🤖 AI前沿动态 v2.0")
    print(f"   时间窗口: {START_BJ.strftime('%Y-%m-%d %H:%M')} - {END_BJ.strftime('%Y-%m-%d %H:%M')} 北京时间")
    print(f"   RSS源: {len(SOURCES)} 个")
    print(f"   优先级: 来源权重 + 热度关键词 + 时效性")
    if API_KEY:
        print(f"   LLM: MiniMax-M2.5 ✓")
    else:
        print(f"   LLM: 未配置 ✗")

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

    # 去重
    unique = dedup_articles(all_arts)
    # 按优先级排序
    unique = sorted(unique, key=lambda x: x.get("priority", 0), reverse=True)

    # 保留足够文章
    if len(unique) < MIN_ARTICLES:
        print(f"📊 文章不足 {MIN_ARTICLES} 篇，保留全部 {len(unique)} 篇")

    print(f"\n📊 {len(all_arts)} → {len(unique)} 条")

    # LLM 处理 (可选)
    if API_KEY and len(unique) > 5:
        print("🤖 调用LLM提取要点...")
        unique = process_with_llm(unique)

    # 分类统计
    by_cat = defaultdict(int)
    for a in unique:
        for c in a["categories"]: by_cat[c] += 1
    print(f"📂 分类: ", end="")
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注"]:
        print(f"{cat}{by_cat.get(cat,0)} ", end="")
    print("")

    if errors:
        print(f"⚠️ 失败: {errors[:3]}")

    # 生成报告
    report = generate_report(unique)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    # 存档
    save_archive(unique)

    print(f"✅ 已输出: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
