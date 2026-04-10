#!/usr/bin/env python3
"""管线测试：跑完整流程，输出到 test_output.md，不覆盖任何现有文件"""

import sys, os, json, re
sys.path.insert(0, '/Users/shenyalan/ai-daily-news')

import feed_v5 as fv
from datetime import datetime, timezone, timedelta

# ========== 动态时间窗口：近24小时 ==========
# 结束时间：当前北京时间（向下取整到整点）
# 开始时间：结束时间 - 24小时
beijing_offset = 8
bj_tz = timezone(timedelta(hours=beijing_offset))
now_bj = datetime.now(bj_tz)
# 向下取整到整点
end_bj = now_bj.replace(minute=0, second=0, microsecond=0)
# 如果当前是整点，则从当前时刻开始；否则从上一整点开始
if now_bj.minute == 0 and now_bj.second == 0:
    end_bj = now_bj
start_bj = end_bj - timedelta(hours=24)

fv.START_UTC = start_bj - timedelta(hours=8)
fv.END_UTC = end_bj - timedelta(hours=8)
fv.START_BJ = start_bj
fv.END_BJ = end_bj

print(f"时间窗口: {start_bj.strftime('%m/%d %H:%M')} ~ {end_bj.strftime('%m/%d %H:%M')} 北京时间（近24小时）")

COMPANY_ACCOUNTS = fv.twitter_company_accounts()
RESEARCHER_ACCOUNTS = fv.twitter_researcher_accounts()

all_arts, errors = [], []

# 抓取 RSS
for name, (url, tz) in fv.SOURCES.items():
    if fv.is_podcast_source(name):
        continue
    print(f"  {name}...", end=" ", flush=True)
    arts, err = fv.fetch_source(name, url)
    if err:
        print(f"ERR")
        errors.append(f"{name}: {err}")
    else:
        print(f"{len(arts)}")
        all_arts.extend(arts)

# 抓取推文
print("抓取推文...")
researcher_tweets = fv.fetch_researcher_tweets()
if researcher_tweets:
    print(f"  {len(researcher_tweets)} 条推文")
    for t in researcher_tweets:
        source = t.get("source", "")
        title = t.get("title", "")
        priority = fv.calculate_priority_v2({
            "source": source, "title": title, "summary": title, "categories": ["X讨论"]
        })
        priority += 15
        all_arts.append({
            "title": title[:80], "summary": title, "content": title,
            "link": t.get("link", ""), "categories": ["X讨论"],
            "is_tweet": True, "source": t.get("source", ""),
            "published_parsed": fv.parse_tweet_time(t.get("published", "")),
            "priority": priority,
        })

print(f"\n抓取总计: {len(all_arts)} 条")

# 去重和合并
unique = fv.dedup_articles(all_arts)
print(f"去重后: {len(unique)}")
merged = fv.merge_events(unique)
print(f"合并后: {len(merged)}")

# 同公司多事件合并：同公司多条合并为一条（保留最高优先级）
def merge_company_duplicates(articles):
    """将同一公司的多条新闻合并为一条"""
    company_groups = {}
    # 公司/品牌关键词映射（优先级低的先匹配）
    company_aliases = [
        ("面壁", ["面壁", "ModelForce"]),
        ("DeepSeek", ["deepseek", "deepseekr1"]),
        ("Qwen", ["qwen", "通义", "alibaba qwen"]),
        ("GLM", ["glm", "智谱", "zhipu"]),
        ("OpenAI", ["openai", "chatgpt", "gpt-"]),
        ("Anthropic", ["anthropic", "claude"]),
        ("Google", ["google", "gemini", "deepmind", "deep think"]),
        ("Meta", ["meta", "llama", "muse"]),
        ("NVIDIA", ["nvidia", "cuda", "tensorrt"]),
        ("Canva", ["canva"]),
        ("World Labs", ["world labs", "marble", "haven"]),
        ("Tubi", ["tubi"]),
    ]

    def get_company(article):
        # 检查标题、来源、body、summary（body为空时检查summary）
        text = (
            article.get("title", "") + " " +
            article.get("source", "") + " " +
            (article.get("body") or "") + " " +
            (article.get("summary") or "")
        ).lower()
        for company, aliases in company_aliases:
            if any(alias in text for alias in aliases):
                return company
        return None

    for a in articles:
        company = get_company(a)
        if company:
            company_groups.setdefault(company, []).append(a)
        else:
            # 非公司新闻，保持原样
            company_groups.setdefault(f"__{a.get('title', '')[:20]}__", []).append(a)

    result = []
    for key, arts in company_groups.items():
        if key.startswith("__"):
            # 非公司新闻，直接保留
            result.extend(arts)
        elif len(arts) > 1:
            # 保留最高优先级，合并body
            best = max(arts, key=lambda x: x.get("priority", 0))
            bodies = []
            for a in arts:
                body = a.get("body", "") or a.get("summary", "")
                if body and len(body) > 20:
                    bodies.append(body[:100])
            if bodies:
                best["body"] = " | ".join(bodies[:3])  # 最多3条body
            print(f"  合并 {key}: {len(arts)} → 1 条")
            result.append(best)
        else:
            result.append(arts[0])

    return result

print("同公司合并...")
merged = merge_company_duplicates(merged)

merged = sorted(merged, key=lambda x: x.get("priority", 0), reverse=True)

# 预规范化
print("预规范化...")
merged = fv.improve_news(merged, do_filter=True)

# URL 硬去重（只对比前天的archive，避免重复）
recent_urls = set()
today_str = end_bj.strftime("%Y-%m-%d")
yesterday_str = (end_bj - timedelta(days=1)).strftime("%Y-%m-%d")
skip_dates = {today_str, yesterday_str}  # 跳过今天和昨天
for i in range(2, 5):  # 从前天开始
    date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
    if date in skip_dates:
        print(f"URL去重: 跳过 {date}")
        continue
    archive_file = os.path.join(fv.ARCHIVE_DIR, f"news_{date}.json")
    if os.path.exists(archive_file):
        try:
            with open(archive_file, 'r', encoding='utf-8') as f:
                for a in json.load(f).get("articles", []):
                    link = a.get("link", "").rstrip("/")
                    if link:
                        recent_urls.add(link)
        except Exception:
            pass
if recent_urls:
    before = len(merged)
    merged = [a for a in merged if a.get("link", "").rstrip("/") not in recent_urls]
    removed = before - len(merged)
    if removed > 0:
        print(f"URL去重: 移除 {removed} 条近期已收录链接")

# LLM 处理
if fv.API_KEY and len(merged) > 5:
    print("读取近期存档...")
    recent_articles = fv.load_recent_archives(days=3)
    print(f"调用LLM处理 {len(merged)} 条...")
    merged = fv.process_with_llm(merged, recent_articles)
else:
    print("跳过 LLM（无API KEY或条数不足）")

# 后规范化
print("后规范化...")
merged = fv.improve_news(merged, do_filter=False)

# 后规范化后再做一次同公司合并（LLM处理后body有了，可能检测到更多）
print("后规范化同公司合并...")
merged = merge_company_duplicates(merged)

# 输出测试 md
print(f"\n最终: {len(merged)} 条")
output_path = "/Users/shenyalan/ai-daily-news/test_output.md"

month_day = fv.END_BJ.strftime("%m月%d日")
by_cat = {}
for a in merged:
    for c in a.get("categories", ["未分类"]):
        by_cat.setdefault(c, []).append(a)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(f"## {month_day} 管线测试输出\n\n")
    f.write(f"> 时间窗口: {start_bj.strftime('%m/%d %H:%M')} ~ {end_bj.strftime('%m/%d %H:%M')} 北京时间（近24小时）\n\n")
    f.write("---\n\n")

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        arts = by_cat.get(cat, [])
        if not arts:
            continue
        f.write(f"### {cat} ({len(arts)}条)\n")
        for a in arts:
            title = a.get("title", "")
            body = a.get("body", "") or a.get("summary", "")
            link = a.get("link", "")
            source = a.get("source", "")
            priority = a.get("priority", 0)
            insight = a.get("insight", "")
            low_q = " [低质量]" if a.get("low_quality") else ""

            f.write(f"**{title}**{low_q}\n")
            f.write(f"- [{source}] P{priority:.0f} | {body[:200]}\n")
            if insight:
                f.write(f"  > {insight}\n")
            if link:
                f.write(f"  - {link}\n")
            f.write("\n")
        f.write("\n")

print(f"已输出: {output_path}")
