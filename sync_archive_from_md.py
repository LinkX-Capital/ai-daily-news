#!/usr/bin/env python3
"""把人工返工后的日报 md 条目回流进 archive/news_<date>.json。

背景：跨天去重（feed_v5.dedup_articles）读的是 archive 存档，而存档只在自动
管线跑完后写入、只包含自动版条目。人工补充/修改的条目若不回流，次日的
二手延迟报道（如 IT桔子隔天转载海外融资）会被当成新事件重复收录。

用法：
    python3 sync_archive_from_md.py 2026-10-21

行为：
    - 解析 daily-ai-news-<date>.md 的详细参考条目（**标题** + 来源链接）
    - 与 archive/news_<date>.json 现有 articles 按标题匹配
    - archive 缺失的条目追加（source 标记 "manual-sync"，供追溯）
    - 幂等：重复执行不会产生重复条目
"""

import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent


def parse_md_entries(md_text: str) -> list[dict]:
    """解析详细参考区的 (标题, [来源URL]) 列表。"""
    entries = []
    title_re = re.compile(r"^\*\*(.+?)\*\*\s*$", re.MULTILINE)
    link_re = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
    for m in title_re.finditer(md_text):
        title = m.group(1).strip()
        # 该标题之后到下一个标题之间的来源行
        next_m = title_re.search(md_text, m.end())
        block = md_text[m.end():next_m.start() if next_m else len(md_text)]
        links = [url for _, url in link_re.findall(block)]
        entries.append({"title": title, "links": links})
    return entries


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(64)
    date = sys.argv[1]
    md_file = BASE_DIR / f"daily-ai-news-{date}.md"
    archive_file = BASE_DIR / "archive" / f"news_{date}.json"
    if not md_file.exists():
        print(f"❌ 找不到 {md_file.name}")
        sys.exit(1)
    if not archive_file.exists():
        print(f"❌ 找不到 {archive_file}（需先跑一次自动管线生成存档）")
        sys.exit(1)

    md_entries = parse_md_entries(md_file.read_text(encoding="utf-8"))
    data = json.loads(archive_file.read_text(encoding="utf-8"))
    existing = {a.get("title", "").strip() for a in data.get("articles", [])}

    added = 0
    for e in md_entries:
        if e["title"] in existing:
            continue
        data["articles"].append({
            "title": e["title"],
            "link": e["links"][0] if e["links"] else "",
            "links": e["links"],
            "categories": ["manual-sync"],
            "source": "manual-sync",
        })
        existing.add(e["title"])
        added += 1
        print(f"  + {e['title'][:50]}")

    if added:
        archive_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    print(f"✅ {date}: md 共 {len(md_entries)} 条，archive 原有 "
          f"{len(data['articles']) - added} 条，回流 {added} 条")


if __name__ == "__main__":
    main()
