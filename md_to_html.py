#!/usr/bin/env python3
"""从 MD 文件生成 HTML - 委托给 html_generator 模块"""

from html_generator import md_to_html

if __name__ == "__main__":
    import os
    BASE_DIR = "/Users/shenyalan/ai-daily-news"
    MD_FILE = os.path.join(BASE_DIR, "daily-ai-news.md")
    OUTPUT_HTML = os.path.join(BASE_DIR, "daily-ai-news.html")

    from datetime import datetime
    date_str = datetime.now().strftime("%Y-%m-%d")
    DATED_HTML = os.path.join(BASE_DIR, f"daily-ai-news-{date_str}.html")

    articles = md_to_html(MD_FILE, OUTPUT_HTML, DATED_HTML)
    print(f"📖 解析到 {len(articles)} 条文章")
