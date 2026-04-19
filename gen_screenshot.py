#!/usr/bin/env python3
"""使用playwright生成手机端长图（用于分享给LP）"""

import asyncio
import re
import os
import base64
from datetime import datetime
from collections import defaultdict
from playwright.async_api import async_playwright
from html_generator import parse_md, convert_bold, CAT_ORDER


def parse_md_screenshot(md_content):
    """解析 MD，修复 insight 被混入 body 的问题"""
    articles, summary_items = parse_md(md_content)
    for a in articles:
        if not a.get('body'):
            continue
        body = a['body']
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
            for ip in insight_parts:
                if ip not in a.get('key_points', []):
                    a.setdefault('key_points', []).insert(0, ip)
    return articles, summary_items


def build_screenshot_html(md_content):
    """渐变背景 + 白色卡片布局"""
    articles, summary_items = parse_md_screenshot(md_content)
    # Try to extract date from md title (e.g. "## 04月18-19日")
    m = re.match(r'##\s*(\d{2})月(\d+)(?:[-+](\d+))?日', md_content.lstrip())
    if m:
        month = int(m.group(1))
        day1 = int(m.group(2))
        day2 = m.group(3)
        if day2:
            today_str = f"2026年{month}月{day1}日-{month}月{int(day2)}日"
        else:
            today_str = f"2026年{month}月{day1}日"
    else:
        today_str = datetime.now().strftime("%Y年%m月%d日")
    today_iso = datetime.now().strftime("%Y-%m-%d")

    item_num = [0]

    cat_icons = {
        "模型前沿": "🧠", "产业动态": "🏭", "算力追踪": "⚡",
        "初创&融资": "💰", "研究关注": "🔬", "X讨论": "💬",
    }

    by_cat = defaultdict(list)
    for a in articles:
        for c in a.get("categories", []):
            by_cat[c].append(a)

    # logos base64
    logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets-logo.png"))
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    logo_url = f"data:image/png;base64,{logo_b64}"

    inc_logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "assets-incubator-logo.png"))
    with open(inc_logo_path, "rb") as f:
        inc_b64 = base64.b64encode(f.read()).decode()
    inc_logo_url = f"data:image/png;base64,{inc_b64}"

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", sans-serif;
    background: #764ba2;
    color: #1a1a1a;
    line-height: 1.6;
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
    text-align: justify;
}}

/* ===== Header ===== */
.header {{
    background: #ffffff;
    margin: 12px 12px 0;
    border-radius: 16px;
    padding: 16px 20px 22px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}
.header-logos {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
    padding-bottom: 14px;
    border-bottom: 1px solid #f0f0f0;
}}
.header-logo-fund {{
    height: 24px;
    width: auto;
}}
.header-logo-inc {{
    height: 14px;
    width: auto;
}}
.header-text {{
    text-align: center;
    text-align-last: center;
}}
.header h1 {{
    font-size: 20px;
    font-weight: 700;
    color: #1a1a2e;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}}
.header-sub {{
    font-size: 10px;
    color: #333333;
    letter-spacing: 0.2px;
    margin-bottom: 10px;
    white-space: nowrap;
    margin-left: -20px;
    margin-right: -20px;
}}
.header-date {{
    display: inline-block;
    font-size: 12px;
    font-weight: 600;
    color: #764ba2;
    background: #f5f0ff;
    padding: 3px 14px;
    border-radius: 20px;
}}

/* ===== Content Cards ===== */
.card {{
    background: #ffffff;
    margin: 12px;
    border-radius: 16px;
    padding: 0 20px 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}
.section-label {{
    font-size: 14px;
    font-weight: 700;
    color: #1a1a2e;
    padding: 16px 0 10px;
    margin-bottom: 10px;
}}
/* 要点速览 */
.summary-item {{
    margin-bottom: 8px;
}}
.summary-item:last-child {{
    margin-bottom: 0;
}}
.summary-cat {{
    display: inline-block;
    font-size: 11px;
    font-weight: 600;
    color: #764ba2;
    background: #f5f0ff;
    padding: 2px 8px;
    border-radius: 3px;
    margin-bottom: 4px;
}}
.summary-titles {{
    display: flex;
    flex-direction: column;
    gap: 2px;
}}
.summary-title {{
    font-size: 12px;
    color: #333333;
    line-height: 1.4;
    padding-left: 12px;
    position: relative;
}}
.summary-title::before {{
    content: "•";
    position: absolute;
    left: 0;
    color: #764ba2;
    font-size: 12px;
}}

/* ===== Category ===== */
.cat-section {{
    margin-bottom: 20px;
}}
.cat-section:last-child {{
    margin-bottom: 0;
}}
.cat-header {{
    font-size: 13px;
    font-weight: 700;
    color: #764ba2;
    letter-spacing: 1px;
    padding: 10px 0 8px;
    border-bottom: 1px solid #f0e6f6;
    margin-bottom: 12px;
}}

/* ===== News Item ===== */
.news-item {{
    margin-bottom: 18px;
}}
.news-item:last-child {{
    margin-bottom: 0;
}}
.news-header {{
    display: flex;
    align-items: flex-start;
    gap: 8px;
    margin-bottom: 6px;
}}
.news-num {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 20px;
    height: 20px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #ffffff;
    font-size: 11px;
    font-weight: 700;
    border-radius: 4px;
    flex-shrink: 0;
    margin-top: 1px;
}}
.news-title {{
    font-size: 14px;
    font-weight: 600;
    color: #1a1a2e;
    line-height: 1.45;
    flex: 1;
}}
.news-body {{
    font-size: 13px;
    color: #333333;
    line-height: 1.75;
    padding-left: 24px;
    margin-bottom: 6px;
}}
.news-body strong {{
    color: #1a1a1a;
    font-weight: 600;
}}
.news-body code {{
    background: #f3eeff;
    padding: 1px 4px;
    border-radius: 3px;
    font-size: 11.5px;
    color: #764ba2;
}}
.news-insight {{
    background: #faf6ff;
    border-left: 2.5px solid #a78bfa;
    padding: 6px 10px;
    border-radius: 0 4px 4px 0;
    font-size: 13px;
    color: #6d28d9;
    line-height: 1.5;
    margin-left: 24px;
    margin-bottom: 4px;
}}
.news-source {{
    font-size: 11px;
    color: #999999;
    padding-left: 24px;
}}

/* ===== Footer ===== */
.footer {{
    background: #ffffff;
    margin: 0 12px 12px;
    border-radius: 16px;
    text-align: center;
    padding: 16px 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}
.footer-inner {{
    display: flex;
    align-items: flex-start;
    gap: 10px;
    text-align: left;
}}
.footer-logo {{
    width: 80px;
    height: auto;
    flex-shrink: 0;
    margin-top: 1px;
}}
.footer-desc {{
    font-size: 11px;
    color: #999999;
    line-height: 1.6;
    flex: 1;
}}
.footer-date {{
    font-size: 9px;
    color: #cccccc;
    text-align: center;
    margin-top: 10px;
    letter-spacing: 0.5px;
}}
</style>
</head>
<body>

<div class="header">
    <div class="header-logos">
        <img src="{logo_url}" class="header-logo-fund" alt="星连资本">
        <img src="{inc_logo_url}" class="header-logo-inc" alt="奇绩创坛">
    </div>
    <div class="header-text">
        <h1>全球AI前沿动态</h1>
        <div class="header-sub">每日追踪AI领域前沿进展，捕捉模型演进、研究突破与产业动态等关键信号</div>
        <div class="header-date">{today_str}</div>
    </div>
</div>

<div class="card">
    <div class="section-label">📌 要点速览</div>"""

    # 要点速览
    for cat in CAT_ORDER:
        items = summary_items.get(cat, [])
        if not items:
            continue
        html += f'<div class="summary-item"><span class="summary-cat">{cat}</span><div class="summary-titles">'
        for item in items:
            html += f'<span class="summary-title">{convert_bold(item)}</span>'
        html += '</div></div>'

    html += '</div>'

    # 详细解读
    html += '<div class="card"><div class="section-label">📖 详细解读</div>'

    for cat in CAT_ORDER:
        cat_items = by_cat.get(cat, [])
        if not cat_items:
            continue
        html += f'<div class="cat-section"><div class="cat-header">{cat}</div>'

        for a in cat_items:
            item_num[0] += 1
            num = item_num[0]
            title = a.get("title", "")
            body = a.get("body", "")
            key_points = a.get("key_points", [])
            source = a.get("source", "")
            link = a.get("link", "")

            html += '<div class="news-item">'
            html += f'<div class="news-header"><span class="news-num">{num}</span><span class="news-title">{title}</span></div>'

            if body:
                html += f'<div class="news-body">{convert_bold(body)}</div>'

            for point in key_points:
                html += f'<div class="news-insight">💡 {convert_bold(point)}</div>'

            html += '</div>'

        html += '</div>'

    html += '</div>'

    html += f"""
<div class="footer">
    <div class="footer-inner">
        <img src="{logo_url}" class="footer-logo" alt="星连资本">
        <div class="footer-desc">每日追踪AI领域前沿进展。信号源覆盖全球顶尖科技企业、重点实验室与核心人才，为关键机会识别与趋势判断提供支持。</div>
    </div>
    <div class="footer-date">{today_iso}</div>
</div>
</body>
</html>"""
    return html


async def generate_screenshot():
    today = datetime.now().strftime('%Y-%m-%d')
    md_dated = f"/Users/shenyalan/ai-daily-news/daily-ai-news-{today}.md"
    md_default = "/Users/shenyalan/ai-daily-news/daily-ai-news.md"
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
        height = await page.evaluate("document.documentElement.scrollHeight")
        await page.set_viewport_size({"width": 375, "height": height})
        await page.screenshot(path=output_file, full_page=True, clip={"x": 0, "y": 0, "width": 375, "height": height})
        await browser.close()
        print(f"✅ 已生成手机端长图: {output_file}")


if __name__ == "__main__":
    asyncio.run(generate_screenshot())
