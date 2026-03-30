#!/usr/bin/env python3
"""从存档生成 Markdown 格式日报"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timedelta

ARCHIVE_DIR = Path("/Users/shenyalan/ai-daily-news/archive")


def get_what(title):
    """要点速览只显示'是什么'（取冒号之前的部分）"""
    for sep in ['：', ':', '？', '?', '！', '!']:
        if sep in title:
            return title.split(sep)[0][:50]
    return title[:50]


def generate_md(articles, date_str):
    """生成 Markdown 格式日报
    date_str: 存档文件名中的日期（对应时间窗口开始，即START_BJ）
    日报标题应该是 date_str + 1天（因为日报对应的是"今天9点"的窗口，
    START_BJ是昨天9点，所以标题应该是"今天"）
    """
    # date_str 是存档对应的"时间窗口开始"日期（START_BJ）
    # 日报标题应该是 date_str 的后一天（因为日报是 昨天9点→今天9点 的内容）
    date_obj = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)
    month_day = date_obj.strftime("%m月%d日")

    by_cat = defaultdict(list)
    for a in articles:
        for c in a.get("categories", []):
            by_cat[c].append(a)

    lines = []
    lines.append(f"# 📡 {month_day} AI前沿动态")
    lines.append("")
    lines.append(f"**自动汇总** | 24h | 共 {len(articles)} 条")
    lines.append("")

    # 要点速览
    lines.append("## 📌 要点速览")
    lines.append("")

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        items = by_cat.get(cat, [])
        if not items:
            continue
        items_text = "；".join([get_what(a["title"]) for a in items[:5]])
        lines.append(f"- **{cat}**：{items_text}")
    lines.append("")

    # 正文分类
    lines.append("---")
    lines.append("")

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        items = by_cat.get(cat, [])
        if not items:
            continue
        lines.append(f"## {cat}")
        lines.append("")

        for a in items:
            # 标题
            lines.append(f"### {a['title']}")
            lines.append("")

            # 正文（body）
            body = a.get("body", "").strip()
            if body:
                lines.append(body)
                lines.append("")

            # 关键点（key_points）
            key_points = a.get("key_points", [])
            if key_points:
                lines.append("**要点**：")
                for point in key_points[:3]:
                    lines.append(f"- {point}")
                lines.append("")

            # 洞察（insight）
            insight = a.get("insight", "").strip()
            if insight:
                lines.append(f"> 💡 {insight}")
                lines.append("")

            # 来源
            source = a.get("source", "")
            link = a.get("link", "")
            if link:
                lines.append(f"📌 来源：[{source}]({link})")
            else:
                lines.append(f"📌 来源：{source}")
            lines.append("")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: python gen_md.py <日期>")
        print("例如: python gen_md.py 2026-03-27")
        return

    date_str = sys.argv[1]
    archive_file = ARCHIVE_DIR / f"news_{date_str}.json"

    if not archive_file.exists():
        print(f"❌ 存档不存在: {archive_file}")
        return

    with open(archive_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    articles = data.get("articles", [])
    print(f"📖 读取存档 {archive_file}: {len(articles)} 条文章")

    md = generate_md(articles, date_str)

    # 保存 md 文件
    output_file = Path("/Users/shenyalan/ai-daily-news") / f"daily-ai-news-{date_str}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"✅ 已生成: {output_file}")


if __name__ == "__main__":
    main()