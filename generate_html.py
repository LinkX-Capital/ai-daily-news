#!/usr/bin/env python3
"""生成HTML格式的AI日报"""

import json
import os
from datetime import datetime
from collections import defaultdict

ARCHIVE_DIR = "/Users/shenyalan/ai-daily-news/archive"
OUTPUT_HTML = "/Users/shenyalan/ai-daily-news/daily-ai-news.html"

def generate_html(articles):
    month_day = datetime.now().strftime("%m月%d日")

    by_cat = defaultdict(list)
    for a in articles:
        for c in a.get("categories", []):
            by_cat[c].append(a)

    for c in by_cat:
        by_cat[c] = sorted(by_cat[c], key=lambda x: x.get("priority", 0), reverse=True)[:8]

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{month_day} AI前沿动态</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
            line-height: 1.6;
            padding: 16px;
            max-width: 800px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 16px;
        }}
        .header h1 {{ font-size: 20px; margin-bottom: 8px; }}
        .meta {{ font-size: 12px; opacity: 0.8; }}
        .summary {{
            background: white;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 16px;
        }}
        .summary h2 {{ font-size: 16px; margin-bottom: 12px; color: #1a1a2e; }}
        .cat-tag {{
            display: inline-block;
            background: #e8f4fd;
            color: #0066cc;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-right: 8px;
            flex-shrink: 0;
        }}
        .summary-item {{
            display: flex;
            flex-wrap: wrap;
            align-items: flex-start;
            margin-bottom: 10px;
            gap: 6px;
        }}
        .summary-title {{
            display: block;
            background: #f5f5f5;
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 13px;
            color: #333;
            margin-right: 6px;
            margin-bottom: 4px;
        }}
        .card {{
            background: white;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }}
        .card-header {{
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }}
        .priority {{
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 4px;
            margin-right: 8px;
            font-weight: bold;
        }}
        .priority.high {{ background: #ff4d4f; color: white; }}
        .priority.medium {{ background: #faad14; color: white; }}
        .priority.low {{ background: #d9d9d9; color: #666; }}
        .title {{ font-size: 16px; font-weight: 600; color: #1a1a2e; flex: 1; }}
        .body {{ font-size: 14px; color: #666; margin-bottom: 12px; }}
        .key-points {{
            background: #f9f9f9;
            padding: 12px;
            border-radius: 8px;
            margin-bottom: 12px;
        }}
        .key-points li {{
            font-size: 13px;
            color: #333;
            margin-bottom: 4px;
            list-style: none;
            padding-left: 12px;
            position: relative;
        }}
        .key-points li:before {{
            content: "•";
            position: absolute;
            left: 0;
            color: #0066cc;
        }}
        .related {{
            background: #fff7e6;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 12px;
            color: #d46b08;
            margin-bottom: 8px;
        }}
        .source {{ font-size: 12px; color: #999; }}
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            color: #1a1a2e;
            margin: 20px 0 12px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #0066cc;
        }}
        .footer {{
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 12px;
        }}
        @media (max-width: 480px) {{
            body {{ padding: 12px; }}
            .header h1 {{ font-size: 18px; }}
            .title {{ font-size: 15px; }}
            .body {{ font-size: 13px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📡 {month_day} AI前沿动态</h1>
        <div class="meta">自动汇总 | 24h | 共 {len(articles)} 条</div>
    </div>

    <div class="summary">
        <h2>📌 要点速览</h2>"""

    # 要点速览只显示"是什么"（取冒号之前的部分）
    def get_what(title):
        for sep in ['：', ':', '？', '?', '！', '!']:
            if sep in title:
                return title.split(sep)[0][:30]
        return title[:30]
    
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注"]:
        items = by_cat.get(cat, [])
        if items:
            titles = " | ".join([get_what(a['title']) for a in items[:3]])
            # 每个要点单独一行，更清晰
            html += f'<div class="summary-item"><span class="cat-tag">{cat}</span>'
            for a in items[:3]:
                html += f'<span class="summary-title">{get_what(a["title"])}</span>'
            html += '</div>'

    html += """
    </div>
    <div class="content">"""

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注"]:
        items = by_cat.get(cat, [])
        if not items: continue
        html += f'<div class="section-title">{cat}</div>'
        for a in items:
            priority = a.get("priority", 0)
            if priority > 150:
                priority_class = "high"
                emoji = "🔥"
            elif priority > 100:
                priority_class = "medium"
                emoji = "📰"
            else:
                priority_class = "low"
                emoji = "📄"

            html += f'''
        <div class="card">
            <div class="card-header">
                <span class="priority {priority_class}">{emoji}</span>
                <span class="title">{a['title']}</span>
            </div>'''

            if a.get('body'):
                html += f'<div class="body">{a["body"]}</div>'

            if a.get('key_points'):
                html += '<ul class="key-points">'
                for point in a['key_points'][:3]:
                    html += f'<li>{point}</li>'
                html += '</ul>'

            if a.get('related'):
                html += f'<div class="related">🔗 关联: {a["related"]}</div>'

            source = a.get('source', '')
            link = a.get('link', '')
            if link:
                html += f'<div class="source">📌 来源: <a href="{link}" target="_blank">{source}</a></div>'
            else:
                html += f'<div class="source">📌 来源: {source}</div>'
            html += '</div>'

    html += f"""
    </div>
    <div class="footer">
        更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}
    </div>
</body>
</html>"""

    return html


def main():
    # 读取最新存档
    files = sorted(os.listdir(ARCHIVE_DIR))
    if not files:
        print("❌ 没有找到存档文件")
        return

    latest = files[-1]
    with open(os.path.join(ARCHIVE_DIR, latest), 'r') as f:
        data = json.load(f)

    articles = data.get("articles", [])
    print(f"📖 读取到 {len(articles)} 条文章")

    html = generate_html(articles)
    with open(OUTPUT_HTML, 'w') as f:
        f.write(html)

    print(f"✅ 已生成HTML: {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
