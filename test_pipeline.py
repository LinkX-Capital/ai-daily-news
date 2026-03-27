#!/usr/bin/env python3
"""
日报管线测试脚本
输出到 test_output/ 目录，不影响正常管线
"""

import sys
sys.path.insert(0, '/Users/shenyalan/ai-daily-news')

from feed_v5 import (
    fetch_source, fetch_researcher_tweets, parse_opml, opml_file,
    improve_news, calculate_priority_v2, get_cat,
    merge_events, dedup_articles, load_recent_archives,
    process_with_llm_simple,
    SOURCES, START_UTC, END_UTC, START_BJ, END_BJ
)
from config_loader import tweet_cache, cache_file
import json
import os
from datetime import datetime

TEST_OUTPUT_DIR = "/Users/shenyalan/ai-daily-news/test_output"
os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

TEST_MD = os.path.join(TEST_OUTPUT_DIR, "test_daily-ai-news.md")
TEST_SUMMARY = os.path.join(TEST_OUTPUT_DIR, "test_daily-ai-news-summary.md")
TEST_CACHE = os.path.join(TEST_OUTPUT_DIR, "test_cache.json")

def generate_report(articles):
    """生成报告"""
    from collections import defaultdict

    month_day = END_BJ.strftime("%m月%d日")
    by_cat = defaultdict(list)
    for a in articles:
        for c in a["categories"]: by_cat[c].append(a)

    for cat in by_cat:
        by_cat[cat] = sorted(by_cat[cat], key=lambda x: x.get("priority", 0), reverse=True)[:8]

    lines = [f"## {month_day} AI前沿动态 [测试]", "",
             f"> 自动汇总 | 时间窗口: 24h | 每类 Top 5 | 测试环境", "",
             "---", "", "#要点汇总#", ""]

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        items = by_cat.get(cat, [])
        if items:
            def get_what(title):
                for sep in ['：', ':', '？', '?', '！', '!']:
                    if sep in title:
                        return title.split(sep)[0]
                return title
            titles = "; ".join([get_what(a['title']) for a in items[:5]])
            lines.append(f"- {cat}：{titles}")

    lines.extend(["", "---", "", "## 📖 详细参考", ""])

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        items = by_cat.get(cat, [])
        if not items: continue
        lines.append(f"### {cat}")
        for a in items:
            lines.append(f"**{a['title']}**")
            if a.get('body'):
                lines.append(f"- {a['body']}")
            if a.get('insight'):
                lines.append(f"  > 💡 {a['insight']}")
            link = a.get("link", "")
            if link:
                lines.append(f"   - 来源: [{a['source']}]({link})")
            else:
                lines.append(f"   - 来源: {a['source']}")
            lines.append("")

    lines.extend(["", "---", f"*测试生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*"])
    return "\n".join(lines)

def generate_summary(articles):
    """生成简洁报告"""
    from collections import defaultdict

    month_day = END_BJ.strftime("%m月%d日")
    by_cat = defaultdict(list)
    for a in articles:
        for c in a["categories"]: by_cat[c].append(a)

    for cat in by_cat:
        by_cat[cat] = sorted(by_cat[cat], key=lambda x: x.get("priority", 0), reverse=True)[:8]

    lines = [f"## {month_day} AI 前沿动态 [测试]", "",
             f"> 展开阐释 + 关键细节 + 为什么重要 + 来源链接 | 测试环境", "",
             "---", ""]

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        items = by_cat.get(cat, [])
        if not items: continue
        lines.append(f"### {cat}")
        for a in items:
            lines.append(f"**{a['title']}**")
            sentences = [s.strip() for s in a.get('body', '').split('。') if s.strip()]
            if len(sentences) > 1:
                for s in sentences[1:3]:
                    lines.append(f"- {s}。")
            if a.get('insight'):
                lines.append(f"- {a['insight']}")
            link = a.get('link', '')
            source = a.get('source', '')
            if link:
                lines.append(f"[来源: {source}]({link})")
            else:
                lines.append(f"[来源: {source}]")
            lines.append("")

    lines.extend(["---", f"*测试生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*"])
    return "\n".join(lines)

def main():
    print(f"🧪 日报管线测试")
    print(f"   输出目录: {TEST_OUTPUT_DIR}")
    print(f"   时间窗口: {START_BJ.strftime('%Y-%m-%d %H:%M')} - {END_BJ.strftime('%Y-%m-%d %H:%M')} 北京时间")

    # 抓取RSS
    all_arts = []
    for name, (url, tz) in SOURCES.items():
        from feed_v5 import is_podcast_source
        if is_podcast_source(name):
            continue
        print(f"  📡 {name}...", end=" ", flush=True)
        arts, err = fetch_source(name, url)
        if err:
            print("❌")
        else:
            print(f"✅ {len(arts)}")
            all_arts.extend(arts)

    # 推文
    print("📡 抓取研究者动态...")
    researcher_tweets = fetch_researcher_tweets()
    if researcher_tweets:
        print(f"   使用缓存: {len(researcher_tweets)} 条")
        for t in researcher_tweets:
            all_arts.append({
                "title": t.get("title", "")[:80],
                "summary": t.get("title", ""),
                "content": t.get("title", ""),
                "link": t.get("link", ""),
                "categories": ["X讨论"],
                "is_tweet": True,
                "source": t.get("source", ""),
                "published_parsed": None,
                "priority": calculate_priority_v2({
                    "source": t.get("source", ""),
                    "title": t.get("title", ""),
                    "summary": t.get("title", ""),
                    "categories": ["X讨论"]
                }) + 15
            })

    print(f"📊 抓取总数: {len(all_arts)} 条")

    # 去重、合并
    unique = dedup_articles(all_arts)
    print(f"📊 去重后: {len(unique)} 条")
    merged = merge_events(unique)
    merged = sorted(merged, key=lambda x: x.get("priority", 0), reverse=True)

    # 预规范化
    print("🔧 预规范化...")
    merged = improve_news(merged, do_filter=True)

    # 先用规则系统分类（这样 LLM 就不需要做分类判断了）
    print("📂 规则系统预分类...")
    for a in merged:
        new_cat = get_cat(a.get('title', ''), a.get('summary', ''), a.get('source', ''))
        a['categories'] = new_cat

    # LLM 处理（只做标题重写和 body/insight 生成，不做分类）
    print("📚 读取近期存档...")
    recent_articles = load_recent_archives(days=3)
    print(f"🤖 调用LLM处理（简化模式）...")
    merged = process_with_llm_simple(merged, recent_articles)

    # 后规范化（只做去重，不做分类过滤）
    print("🔧 后规范化...")
    merged = improve_news(merged, do_filter=False)

    # 重新分类（确保分类正确）
    for a in merged:
        new_cat = get_cat(a.get('title', ''), a.get('summary', ''), a.get('source', ''))
        a['categories'] = new_cat
        a['priority'] = calculate_priority_v2(a)

    # 重新分类
    for a in merged:
        new_cat = get_cat(a.get('title', ''), a.get('summary', ''), a.get('source', ''))
        a['categories'] = new_cat
        a['priority'] = calculate_priority_v2(a)

    merged = sorted(merged, key=lambda x: x.get("priority", 0), reverse=True)

    # 统计
    from collections import defaultdict
    by_cat = defaultdict(int)
    for a in merged:
        for c in a["categories"]: by_cat[c] += 1
    print(f"📂 分类: ", end="")
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        print(f"{cat}{by_cat.get(cat,0)} ", end="")
    print("")

    # 生成报告
    report = generate_report(merged)
    with open(TEST_MD, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"✅ 测试报告: {TEST_MD}")

    summary = generate_summary(merged)
    with open(TEST_SUMMARY, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"✅ 测试摘要: {TEST_SUMMARY}")

    # 保存测试缓存
    with open(TEST_CACHE, "w", encoding="utf-8") as f:
        json.dump({'articles': merged, 'time': datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)
    print(f"✅ 测试缓存: {TEST_CACHE}")

if __name__ == "__main__":
    main()
