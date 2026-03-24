#!/usr/bin/env python3
"""HTML 生成模块 - 统一管理日报 HTML 输出"""

import re
import os
import sys
from datetime import datetime
from collections import defaultdict

# 尝试导入路径配置（可选，失败时使用默认值）
try:
    sys.path.insert(0, '/Users/shenyalan/ai-daily-news')
    from config_loader import base_dir, output_md, output_html
    HAS_CONFIG = True
except ImportError:
    HAS_CONFIG = False

# 分类顺序
CAT_ORDER = ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]

# 分类名称标准化映射
CAT_ALIASES = {
    '算力追踪': '算力追踪',
    '算力跟踪': '算力追踪',
    '算力': '算力追踪',
}

def normalize_category(cat):
    """标准化分类名称"""
    return CAT_ALIASES.get(cat, cat)


def parse_md(md_content):
    """解析 MD 字符串，提取文章和要点汇总"""
    articles = []
    current_cat = None
    current_body_lines = []
    summary_items = {}
    in_summary = False

    lines = md_content.split('\n')
    for line in lines:
        original_stripped = line.strip()

        # 检测要点汇总
        if '#要点汇总#' in original_stripped:
            in_summary = True
            continue
        if in_summary and original_stripped.startswith('---'):
            in_summary = False
            continue
        if in_summary and original_stripped.startswith('- '):
            parts = original_stripped[2:].split('：', 1)
            if len(parts) == 2:
                cat = normalize_category(parts[0].strip())
                items = [i.strip() for i in parts[1].split(';') if i.strip()]
                summary_items[cat] = items
            continue

        # 检测分类标题
        for prefix in ['### ', '## ']:
            if original_stripped.startswith(prefix):
                cat_text = original_stripped[len(prefix):].strip()
                if cat_text not in ['详细参考', '要点汇总', 'AI 前沿动态']:
                    current_cat = normalize_category(cat_text)
                break

        # 检测文章标题
        if original_stripped.startswith('**') and original_stripped.endswith('**') and not original_stripped.startswith('##'):
            if articles and current_body_lines:
                articles[-1]['body'] = ' '.join(current_body_lines)
            current_body_lines = []
            title = original_stripped[2:-2].strip()
            if title:
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

        # 检测 insight
        if '> 💡' in original_stripped and articles:
            insight = original_stripped.split('💡')[1].strip() if '💡' in original_stripped else ''
            if insight:
                articles[-1]['key_points'].append(insight)
            continue

        # 检测来源
        if '来源:' in original_stripped and articles:
            if current_body_lines:
                articles[-1]['body'] = ' '.join(current_body_lines)
                current_body_lines = []
            source_match = re.search(r'\[([^\]]+)\]', original_stripped)
            if source_match:
                articles[-1]['source'] = source_match.group(1).strip()
                link_match = re.search(r'\(([^)]+)\)', original_stripped)
                if link_match:
                    articles[-1]['link'] = link_match.group(1)
            continue

        # 检测 body
        if original_stripped.startswith('-') and '来源:' not in original_stripped and articles:
            body_text = original_stripped.lstrip('-').strip()
            if body_text:
                current_body_lines.append(body_text)
            continue

    # 保存最后一个 body
    if articles and current_body_lines:
        articles[-1]['body'] = ' '.join(current_body_lines)

    return articles, summary_items


def convert_bold(text):
    """将 **text** 转换为 <strong>text</strong>"""
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)


def get_priority_display(priority):
    """根据优先级返回样式和图标"""
    if priority > 150:
        return "high", "🔥"
    elif priority > 100:
        return "medium", "📰"
    else:
        return "low", "📄"


def generate_html(articles, summary_items, month_day=None):
    """生成 HTML"""
    if month_day is None:
        month_day = datetime.now().strftime("%m月%d日")

    # 按分类分组
    by_cat = defaultdict(list)
    for a in articles:
        for c in a.get("categories", []):
            by_cat[c].append(a)

    # 构建 HTML
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
        .body {{ font-size: 14px; color: #666; margin-bottom: 12px; line-height: 1.7; }}
        .body strong {{ color: #1a1a2e; font-weight: 600; }}
        .insight {{
            background: #fff7e6;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 13px;
            color: #d46b08;
            margin-bottom: 12px;
        }}
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
        .source a {{ color: #666; text-decoration: none; }}
        .source a:hover {{ text-decoration: underline; }}
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

    # 要点速览
    for cat in CAT_ORDER:
        items = summary_items.get(cat, [])
        if items:
            html += f'<div class="summary-item"><span class="cat-tag">{cat}</span>'
            for item in items[:4]:
                html += f'<span class="summary-title">{convert_bold(item)}</span>'
            html += '</div>'

    html += """
    </div>
    <div class="content">"""

    # 详细内容
    for cat in CAT_ORDER:
        items = by_cat.get(cat, [])
        if not items:
            continue
        html += f'<div class="section-title">{cat}</div>'
        for a in items:
            priority = a.get("priority", 0)
            priority_class, emoji = get_priority_display(priority)

            html += f'''
        <div class="card">
            <div class="card-header">
                <span class="priority {priority_class}">{emoji}</span>
                <span class="title">{a['title']}</span>
            </div>'''

            if a.get('body'):
                html += f'<div class="body">{convert_bold(a["body"])}</div>'

            # insight 显示
            if a.get('key_points'):
                for point in a['key_points']:
                    html += f'<div class="insight">💡 {convert_bold(point)}</div>'

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


def md_to_html(md_file, output_html=None, dated_html=None):
    """从 MD 文件生成 HTML"""
    import os

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    articles, summary_items = parse_md(md_content)
    html = generate_html(articles, summary_items)

    # 保存 HTML
    if output_html is None:
        output_html = md_file.replace('.md', '.html')

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 已生成: {output_html}")

    # 保存带日期的版本
    if dated_html:
        with open(dated_html, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✅ 已生成: {dated_html}")

    return articles


if __name__ == "__main__":
    if HAS_CONFIG:
        MD_FILE = output_md()
        OUTPUT_HTML = output_html()
        BASE_DIR = base_dir()
    else:
        BASE_DIR = "/Users/shenyalan/ai-daily-news"
        MD_FILE = os.path.join(BASE_DIR, "daily-ai-news.md")
        OUTPUT_HTML = os.path.join(BASE_DIR, "daily-ai-news.html")

    DATE_STR = datetime.now().strftime("%Y-%m-%d")
    DATED_HTML = os.path.join(BASE_DIR, f"daily-ai-news-{DATE_STR}.html")

    articles = md_to_html(MD_FILE, OUTPUT_HTML, DATED_HTML)
    print(f"📖 解析到 {len(articles)} 条文章")
