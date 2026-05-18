#!/usr/bin/env python3
"""
Archive Searcher - 搜索历史日报档案

独立模块，可供 Knowledge Agent 使用
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

ARCHIVE_DIR = Path(__file__).parent / "archive"
SEARCH_LIMITS = {
    "archive_days": 90,
    "archive_results": 10,
}


class ArchiveSearcher:
    """搜索历史日报档案"""

    def __init__(self, archive_dir: Path = None):
        self.archive_dir = archive_dir or ARCHIVE_DIR
        self.cache = {}

    def _load_archive(self, date_str: str) -> List[Dict]:
        if date_str in self.cache:
            return self.cache[date_str]

        json_path = self.archive_dir / f"news_{date_str}.json"
        if json_path.exists():
            try:
                data = json.loads(json_path.read_text(encoding="utf-8"))
                articles = data.get("articles", [])
                self.cache[date_str] = articles
                return articles
            except (json.JSONDecodeError, KeyError):
                return []
        return []

    def search_by_keywords(self, keywords: List[str], days_back: int = 90) -> List[Dict]:
        """按关键词搜索历史动态"""
        results = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        current = start_date
        while current <= end_date:
            date_str = current.strftime("%Y-%m-%d")
            articles = self._load_archive(date_str)

            for article in articles:
                text_to_check = (
                    article.get("title", "") + " " +
                    article.get("body", "") + " " +
                    article.get("summary", "")
                ).lower()

                for kw in keywords:
                    if kw.lower() in text_to_check:
                        results.append({
                            "date": date_str,
                            "title": article.get("title", ""),
                            "body": article.get("body", ""),
                            "insight": article.get("insight", ""),
                            "link": article.get("link", ""),
                            "category": article.get("categories", [""])[0] if article.get("categories") else "",
                        })
                        break

            current += timedelta(days=1)

        results.sort(key=lambda x: x["date"], reverse=True)
        return results[:SEARCH_LIMITS["archive_results"]]


if __name__ == "__main__":
    # 测试
    searcher = ArchiveSearcher()
    results = searcher.search_by_keywords(["可灵", "Runway"], days_back=30)
    print(f"找到 {len(results)} 条结果")
    for r in results[:5]:
        print(f"- {r['date']}: {r['title'][:60]}...")
