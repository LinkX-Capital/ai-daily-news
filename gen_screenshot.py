#!/usr/bin/env python3
"""使用playwright生成手机端长图 - 深色正式风格（用于分享给LP）"""

import asyncio
import re
from datetime import datetime
from collections import defaultdict
from playwright.async_api import async_playwright
from html_generator import parse_md, convert_bold, get_priority_display, CAT_ORDER


def parse_md_screenshot(md_content):
    """解析 MD，修复 insight 被混入 body 的问题"""
    articles, summary_items = parse_md(md_content)
    for a in articles:
        if not a.get('body'):
            continue
        # 从 body 中提取 `> insight文字` 部分
        # MD 里 insight 格式: "  > insight内容" 被 body 收集后变成 " > insight内容"
        body = a['body']
        # 匹配末尾的 `> ` 开头的 insight 文本
        # 可能有多个以 `. ` 结尾的句子，最后跟着 `> xxx`
        insight_parts = []
        body_parts = []

        for segment in re.split(r'(?=\s+>\s)', body):
            stripped = segment.strip()
            if stripped.startswith('> ') and not stripped.startswith('> 💡'):
                insight_text = stripped[2:].strip()
                if insight_text:
                    insight_parts.append(insight_text)
            else:
                body_parts.append(segment)

        if insight_parts:
            a['body'] = ' '.join(b.strip() for b in body_parts).strip()
            # 追加到 key_points（insight 区域）
            for ip in insight_parts:
                if ip not in a.get('key_points', []):
                    a.setdefault('key_points', []).insert(0, ip)
    return articles, summary_items


def build_screenshot_html(md_content):
    """从 MD 内容生成深色正式风格的截图 HTML"""
    articles, summary_items = parse_md_screenshot(md_content)
    month_day = datetime.now().strftime("%m月%d日")
    today = datetime.now().strftime("%Y-%m-%d")

    by_cat = defaultdict(list)
    for a in articles:
        for c in a.get("categories", []):
            by_cat[c].append(a)

    # 分类配色
    cat_colors = {
        "模型前沿": "#60a5fa", "产业动态": "#34d399", "算力追踪": "#a78bfa",
        "初创&融资": "#fbbf24", "研究关注": "#22d3ee", "X讨论": "#9ca3af",
    }
    cat_bg = {
        "模型前沿": "rgba(59,130,246,0.12)", "产业动态": "rgba(16,185,129,0.12)",
        "算力追踪": "rgba(139,92,246,0.12)", "初创&融资": "rgba(245,158,11,0.12)",
        "研究关注": "rgba(6,182,212,0.12)", "X讨论": "rgba(107,114,128,0.12)",
    }

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif;
    background: #0c0f1a;
    color: #e2e8f0;
    line-height: 1.6;
    width: 375px;
    -webkit-font-smoothing: antialiased;
}}
.header {{
    background: linear-gradient(135deg, #0f172a 0%, #1a1f3a 40%, #1e2a4a 100%);
    padding: 32px 20px 24px;
    position: relative;
    overflow: hidden;
}}
.header::after {{
    content: '';
    position: absolute;
    bottom: 0; left: 20px; right: 20px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(100,140,255,0.35), rgba(160,100,255,0.25), transparent);
}}
.header-label {{
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 10px;
}}
.header h1 {{
    font-size: 20px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 4px;
    letter-spacing: -0.3px;
}}
.header-meta {{
    font-size: 11px;
    color: #475569;
}}
.summary {{
    padding: 18px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}}
.summary-label {{
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 12px;
}}
.summary-item {{
    margin-bottom: 10px;
}}
.summary-item:last-child {{ margin-bottom: 0; }}
.cat-tag {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 3px;
    font-size: 9px;
    font-weight: 600;
    letter-spacing: 0.5px;
    margin-bottom: 5px;
}}
.summary-titles {{
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
}}
.summary-title {{
    display: inline-block;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 11px;
    color: #94a3b8;
    line-height: 1.35;
}}
.section-title {{
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    padding: 14px 20px 6px;
}}
.card {{
    padding: 14px 20px 12px;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    border-left: 2.5px solid transparent;
}}
.card-header {{
    display: flex;
    align-items: flex-start;
    gap: 7px;
    margin-bottom: 6px;
}}
.priority {{
    font-size: 11px;
    line-height: 1;
    margin-top: 4px;
    flex-shrink: 0;
}}
.title {{
    font-size: 14px;
    font-weight: 600;
    color: #f1f5f9;
    flex: 1;
    line-height: 1.4;
}}
.body {{
    font-size: 12px;
    color: #94a3b8;
    margin-bottom: 8px;
    line-height: 1.7;
}}
.body strong {{ color: #e2e8f0; font-weight: 600; }}
.body code {{
    background: rgba(139,92,246,0.15);
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 11px;
    color: #c4b5fd;
}}
.insight {{
    background: rgba(245,158,11,0.05);
    border-left: 2px solid rgba(245,158,11,0.25);
    padding: 6px 10px;
    border-radius: 0 4px 4px 0;
    font-size: 11px;
    color: #fbbf24;
    margin-bottom: 8px;
    line-height: 1.45;
}}
.source {{
    font-size: 10px;
    color: #334155;
}}
.source a {{
    color: #475569;
    text-decoration: none;
}}
.footer {{
    text-align: center;
    padding: 16px 20px;
    color: #1e293b;
    font-size: 9px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    border-top: 1px solid rgba(255,255,255,0.02);
}}
</style>
</head>
<body>
<div class="header">
    <div class="header-label">AI Daily Intelligence</div>
    <h1>{month_day} AI前沿动态</h1>
    <div class="header-meta">{len(articles)} 条动态 &middot; 过去24小时</div>
</div>
<div class="summary">
    <div class="summary-label">要点速览</div>"""

    # 要点速览
    for cat in CAT_ORDER:
        items = summary_items.get(cat, [])
        if not items:
            continue
        color = cat_colors.get(cat, "#94a3b8")
        bg = cat_bg.get(cat, "rgba(255,255,255,0.05)")
        html += f'<div class="summary-item"><span class="cat-tag" style="background:{bg};color:{color}">{cat}</span><div class="summary-titles">'
        for item in items:
            html += f'<span class="summary-title">{convert_bold(item)}</span>'
        html += '</div></div>'

    html += '</div>'

    # 详细内容
    for cat in CAT_ORDER:
        items = by_cat.get(cat, [])
        if not items:
            continue
        color = cat_colors.get(cat, "#94a3b8")
        html += f'<div class="section-title" style="color:{color}">{cat}</div>'
        border_color = cat_colors.get(cat, "#475569")
        for a in items:
            priority = a.get("priority", 0)
            _, emoji = get_priority_display(priority, a.get("categories"), a.get("title", ""), a.get("body", ""))
            html += f'''<div class="card" style="border-left-color:{border_color}">
    <div class="card-header">
        <span class="priority">{emoji}</span>
        <span class="title">{a["title"]}</span>
    </div>'''
            if a.get("body"):
                html += f'<div class="body">{convert_bold(a["body"])}</div>'
            if a.get("key_points"):
                for point in a["key_points"]:
                    html += f'<div class="insight">💡 {convert_bold(point)}</div>'
            source = a.get("source", "")
            link = a.get("link", "")
            if link:
                html += f'<div class="source">📌 来源: <a href="{link}">{source}</a></div>'
            elif source:
                html += f'<div class="source">📌 来源: {source}</div>'
            html += '</div>'

    html += f"""<div class="footer">AI Daily Intelligence &middot; {today}</div>
</body>
</html>"""
    return html


async def generate_screenshot():
    today = datetime.now().strftime('%Y-%m-%d')
    # 优先用带日期的 MD，fallback 到 daily-ai-news.md
    md_dated = f"/Users/shenyalan/ai-daily-news/daily-ai-news-{today}.md"
    md_default = "/Users/shenyalan/ai-daily-news/daily-ai-news.md"
    import os
    md_file = md_dated if os.path.exists(md_dated) else md_default
    output_file = "/Users/shenyalan/ai-daily-news/daily-ai-news-mobile.png"

    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    screenshot_html = build_screenshot_html(md_content)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": 375, "height": 1200},
            device_scale_factor=2
        )
        await page.set_content(screenshot_html)
        await page.wait_for_timeout(2000)
        height = await page.evaluate("document.body.scrollHeight")
        await page.set_viewport_size({"width": 375, "height": height})
        await page.screenshot(path=output_file, full_page=True)
        await browser.close()
        print(f"✅ 已生成手机端长图: {output_file}")


if __name__ == "__main__":
    asyncio.run(generate_screenshot())
