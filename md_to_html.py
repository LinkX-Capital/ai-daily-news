#!/usr/bin/env python3
"""从 MD 文件生成 HTML"""

import re
from datetime import datetime
from collections import defaultdict

MD_FILE = "/Users/shenyalan/ai-daily-news/daily-ai-news.md"
OUTPUT_HTML = "/Users/shenyalan/ai-daily-news/daily-ai-news.html"

def parse_md(md_content):
    """解析 MD 文件，提取文章和要点汇总"""
    articles = []
    current_cat = None
    current_body_lines = []
    summary_items = {}  # 分类 -> 要点列表
    in_summary = False

    lines = md_content.split('\n')
    for i, line in enumerate(lines):
        stripped = line.strip()

        # 检测要点汇总部分
        if '#要点汇总#' in stripped:
            in_summary = True
            continue
        if in_summary and stripped.startswith('---'):
            in_summary = False
            continue
        if in_summary and stripped.startswith('- '):
            # 解析要点汇总行: - 分类：要点1; 要点2; ... (使用中文冒号)
            parts = stripped[2:].split('：', 1)
            if len(parts) == 2:
                cat = parts[0].strip()
                items_str = parts[1].strip()
                items = [i.strip() for i in items_str.split(';') if i.strip()]
                summary_items[cat] = items
            continue

        # 检测分类标题 (### 开头)
        if stripped.startswith('### '):
            current_cat = stripped[4:].strip()
            continue

        # 检测文章标题 (**title**)
        if stripped.startswith('**') and stripped.endswith('**'):
            # 保存之前的文章
            if articles and current_body_lines:
                body_text = ' '.join(current_body_lines)
                articles[-1]['body'] = body_text
            current_body_lines = []

            title = stripped[2:-2]
            articles.append({
                'title': title,
                'categories': [current_cat] if current_cat else [],
                'body': '',
                'source': '',
                'link': '',
                'key_points': [],
                'priority': 100
            })
            continue

        # 检测 insight (> 💡)
        if '> 💡' in stripped and articles:
            insight = stripped.split('💡')[1].strip() if '💡' in stripped else ''
            if insight:
                articles[-1]['key_points'].append(insight)
            continue

        # 检测来源 (- 来源:)
        if stripped.startswith('- 来源:') and articles:
            # 先保存body
            if current_body_lines:
                body_text = ' '.join(current_body_lines)
                articles[-1]['body'] = body_text
                current_body_lines = []

            source_match = re.search(r'\[([^\]]+)\]', stripped)
            if source_match:
                articles[-1]['source'] = source_match.group(1).strip()
                link_match = re.search(r'\(([^)]+)\)', stripped)
                if link_match:
                    articles[-1]['link'] = link_match.group(1)
            continue

        # 检测 body (以 - 开头，但不是来源)
        if stripped.startswith('- ') and not stripped.startswith('- 来源:') and articles:
            current_body_lines.append(stripped[2:].strip())
            continue

    # 保存最后一个文章的body
    if articles and current_body_lines:
        body_text = ' '.join(current_body_lines)
        articles[-1]['body'] = body_text

    return articles, summary_items


def generate_html(articles, summary_items):
    """生成 HTML"""
    month_day = datetime.now().strftime("%m月%d日")

    by_cat = defaultdict(list)
    for a in articles:
        for c in a.get("categories", []):
            by_cat[c].append(a)

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

    # 要点速览 - 使用 summary_items 而不是从文章标题提取
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        items = summary_items.get(cat, [])
        if items:
            html += f'<div class="summary-item"><span class="cat-tag">{cat}</span>'
            for item in items[:4]:
                html += f'<span class="summary-title">{item}</span>'
            html += '</div>'

    html += """
    </div>
    <div class="content">"""

    # 详细内容
    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        items = by_cat.get(cat, [])
        if not items:
            continue
        html += f'<div class="section-title">{cat}</div>'
        for a in items:
            html += f'''
        <div class="card">
            <div class="card-header">
                <span class="priority medium">📰</span>
                <span class="title">{a['title']}</span>
            </div>'''

            if a.get('body'):
                html += f'<div class="body">{a["body"]}</div>'

            if a.get('key_points'):
                html += '<ul class="key-points">'
                for point in a['key_points'][:3]:
                    html += f'<li>{point}</li>'
                html += '</ul>'

            source = a.get('source', '')
            link = a.get('link', '')
            if link:
                html += f'<div class="source">📌 来源: <a href="{link}" target="_blank">{source}</a></div>'
            elif source:
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
    with open(MD_FILE, 'r') as f:
        md_content = f.read()

    articles, summary_items = parse_md(md_content)
    print(f"📖 解析到 {len(articles)} 条文章")
    print(f"📋 要点汇总: {len(summary_items)} 个分类")
    for cat, items in summary_items.items():
        print(f"  {cat}: {items[:3]}...")

    html = generate_html(articles, summary_items)

    # 保存 HTML
    with open(OUTPUT_HTML, 'w') as f:
        f.write(html)
    print(f"✅ 已生成: {OUTPUT_HTML}")

    # 同时保存带日期的版本
    date_str = datetime.now().strftime("%Y-%m-%d")
    dated_html = f"/Users/shenyalan/ai-daily-news/daily-ai-news-{date_str}.html"
    with open(dated_html, 'w') as f:
        f.write(html)
    print(f"✅ 已生成: {dated_html}")


if __name__ == "__main__":
    main()
