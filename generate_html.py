#!/usr/bin/env python3
"""生成HTML格式的AI日报"""

import json
import os
import re
from datetime import datetime
from collections import defaultdict

ARCHIVE_DIR = "/Users/shenyalan/ai-daily-news/archive"
OUTPUT_HTML = "/Users/shenyalan/ai-daily-news/daily-ai-news.html"


def md_to_html(text):
    """将 Markdown **加粗** 转换为 HTML <strong>"""
    if not text:
        return text
    # **xxx** -> <strong>xxx</strong>
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)


def generate_html(articles, date_str=None, summary_raw_text=None):
    if date_str:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        month_day = date_obj.strftime("%m月%d日")
    else:
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
        .body {{ font-size: 14px; color: #666; margin-bottom: 8px; }}
        .insight {{ font-size: 13px; color: #555; background: #f0f7ff; padding: 10px 12px; border-radius: 6px; margin-bottom: 8px; border-left: 3px solid #0066cc; }}
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
                return title.split(sep)[0][:50]
        return title[:50]

    # 如果有原始要点汇总文本，解析并使用正确格式
    if summary_raw_text:
        # 原始文本格式：- 分类：内容1; 内容2; 内容3
        for line in summary_raw_text.strip().split('\n'):
            line = line.strip()
            if not line or not line.startswith('-'):
                continue
            # 去掉开头的 "- "
            line = line[1:].strip()
            # 找到分类和内容
            for sep in ['：', ':']:
                if sep in line:
                    cat_part, content_part = line.split(sep, 1)
                    cat = cat_part.strip()
                    titles = [t.strip() for t in content_part.split(';') if t.strip()]
                    if titles:
                        html += f'<div class="summary-item"><span class="cat-tag">{cat}</span>'
                        for t in titles:
                            html += f'<span class="summary-title">{get_what(t)}</span>'
                        html += '</div>'
                    break
    else:
        # 从文章数据重建
        for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
            items = by_cat.get(cat, [])
            if items:
                html += f'<div class="summary-item"><span class="cat-tag">{cat}</span>'
                for a in items:
                    html += f'<span class="summary-title">{get_what(a["title"])}</span>'
                html += '</div>'

    html += """
    </div>
    <div class="content">"""

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
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
                <span class="title">{md_to_html(a['title'])}</span>
            </div>'''

            if a.get('body'):
                html += f'<div class="body">{md_to_html(a["body"])}</div>'

            if a.get('insight'):
                html += f'<div class="insight">💡 {md_to_html(a["insight"])}</div>'

            if a.get('key_points'):
                html += '<ul class="key-points">'
                for point in a['key_points'][:3]:
                    html += f'<li>{md_to_html(point)}</li>'
                html += '</ul>'

            if a.get('related'):
                html += f'<div class="related">🔗 关联: {md_to_html(a["related"])}</div>'

            source = a.get('source', '')
            link = a.get('link', '')
            if link:
                html += f'<div class="source">📌 来源: <a href="{link}" target="_blank">{md_to_html(source)}</a></div>'
            else:
                html += f'<div class="source">📌 来源: {md_to_html(source)}</div>'

            # 显示合并的来源（Twitter账号等）
            merged = a.get('merged_sources', [])
            if merged and len(merged) > 1:
                other = [s for s in merged if s != source]
                if other:
                    html += f'<div class="source" style="margin-top:4px;color:#888">📎 同时参考: {", ".join(other)}</div>'

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
    from datetime import datetime, timedelta
    import re

    # 从 md 文件读取日期，确定应该读取哪个存档
    md_file = "/Users/shenyalan/ai-daily-news/daily-ai-news.md"
    date_str = None
    if os.path.exists(md_file):
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        # 解析 md 文件中的日期，如 "03月27日"
        date_match = re.search(r'(\d{2})月(\d{2})日', md_content)
        if date_match:
            month, day = date_match.groups()
            date_str = f"2026-{month}-{day}"  # 如 "2026-03-27"
            # 查找对应的存档文件
            expected_archive = f"news_{date_str}.json"
            archive_path = os.path.join(ARCHIVE_DIR, expected_archive)
            if os.path.exists(archive_path):
                with open(archive_path, 'r') as f:
                    data = json.load(f)
                articles = data.get("articles", [])
                print(f"📖 读取存档 {expected_archive}: {len(articles)} 条文章")
            else:
                print(f"⚠️ 存档不存在: {expected_archive}，尝试读取最新存档")
                files = sorted(os.listdir(ARCHIVE_DIR))
                if files:
                    latest = files[-1]
                    date_str = latest.replace("news_", "").replace(".json", "")
                    with open(os.path.join(ARCHIVE_DIR, latest), 'r') as f:
                        data = json.load(f)
                    articles = data.get("articles", [])
                    print(f"📖 读取最新存档 {latest}: {len(articles)} 条文章")
                else:
                    print("❌ 没有找到存档文件")
                    return
        else:
            print("⚠️ 无法从 md 文件解析日期，使用最新存档")
            files = sorted(os.listdir(ARCHIVE_DIR))
            if files:
                latest = files[-1]
                date_str = latest.replace("news_", "").replace(".json", "")
                with open(os.path.join(ARCHIVE_DIR, latest), 'r') as f:
                    data = json.load(f)
                articles = data.get("articles", [])
                print(f"📖 读取最新存档 {latest}: {len(articles)} 条文章")
            else:
                print("❌ 没有找到存档文件")
                return
    else:
        print("❌ md 文件不存在")
        return

    # 生成带日期的HTML文件
    dated_html_file = f"/Users/shenyalan/ai-daily-news/daily-ai-news-{date_str}.html"
    html = generate_html(articles)
    
    # 保存带日期的版本
    with open(dated_html_file, 'w') as f:
        f.write(html)
    print(f"✅ 已生成HTML: {dated_html_file}")
    
    # 同时保存为 daily-ai-news.html
    with open(OUTPUT_HTML, 'w') as f:
        f.write(html)
    print(f"✅ 已更新: {OUTPUT_HTML}")
    
    # 更新 index.html
    update_index(date_str)

def update_index(latest_date):
    """更新 index.html，添加最新日期的链接"""
    import re
    
    index_file = "/Users/shenyalan/ai-daily-news/index.html"
    
    # 读取现有 index.html
    if os.path.exists(index_file):
        with open(index_file, 'r') as f:
            index_content = f.read()
    else:
        # 创建新的 index.html
        index_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI前沿动态</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }
        h1 { color: #1a1a2e; }
        .archive-list { list-style: none; padding: 0; }
        .archive-list li { padding: 10px 0; border-bottom: 1px solid #eee; }
        .archive-list a { color: #0066cc; text-decoration: none; font-size: 16px; }
        .archive-list a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>📡 AI前沿动态</h1>
    <ul class="archive-list">
    </ul>
</body>
</html>"""
    
    # 解析现有日期列表
    dates = re.findall(r'href="daily-ai-news-(\d{4}-\d{2}-\d{2})\.html"', index_content)
    dates = list(set(dates))
    
    # 添加新日期
    if latest_date not in dates:
        dates.append(latest_date)
    
    # 按日期排序（最新的在前）
    dates.sort(reverse=True)
    
    # 生成新的列表
    links_html = '\n'.join([f'        <li><a href="daily-ai-news-{d}.html">{d} AI前沿动态</a></li>' for d in dates])

    # 精确替换日报存档的 ul（使用 id="daily-archive"）
    index_content = re.sub(r'<ul class="archive-list" id="daily-archive">.*?</ul>', f'<ul class="archive-list" id="daily-archive">\n{links_html}\n    </ul>', index_content, flags=re.DOTALL)
    
    with open(index_file, 'w') as f:
        f.write(index_content)
    
    print(f"✅ 已更新index.html")


if __name__ == "__main__":
    main()
