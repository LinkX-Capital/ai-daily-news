#!/usr/bin/env python3
"""截图指定日期的日报并推送飞书

用法:
  python3 screenshot_and_push.py                     # 默认今天
  python3 screenshot_and_push.py 2026-04-25          # 指定一天
  python3 screenshot_and_push.py 2026-04-25 2026-04-26  # 指定多天
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

from playwright.async_api import async_playwright

# 复用 gen_screenshot 的构建逻辑
from gen_screenshot import build_screenshot_html

BASE_DIR = Path(__file__).parent
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")

DATES = sys.argv[1:] if len(sys.argv) > 1 else [datetime.now().strftime("%Y-%m-%d")]


async def take_screenshot(date: str) -> Path | None:
    md_file = BASE_DIR / f"daily-ai-news-{date}.md"
    output_file = BASE_DIR / f"daily-ai-news-{date}-mobile.png"

    if not md_file.exists():
        print(f"  skip {md_file.name} not found")
        return None

    md_content = md_file.read_text(encoding="utf-8")
    screenshot_html = build_screenshot_html(md_content)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": 375, "height": 1200},
            device_scale_factor=2,
        )
        await page.set_content(screenshot_html)
        await page.wait_for_timeout(2000)
        height = await page.evaluate("document.documentElement.scrollHeight")
        await page.set_viewport_size({"width": 375, "height": height})
        await page.screenshot(
            path=str(output_file),
            full_page=True,
            clip={"x": 0, "y": 0, "width": 375, "height": height},
        )
        await browser.close()

    print(f"  ok {output_file.name}")
    return output_file


def _parse_summary_from_html(date: str) -> list[dict]:
    """从 HTML 文件解析要点速览，返回飞书 card elements"""
    import re
    from html import unescape

    html_file = BASE_DIR / f"daily-ai-news-{date}.html"
    if not html_file.exists():
        return []

    html_content = html_file.read_text(encoding="utf-8")
    if "要点速览" not in html_content and "sum-cat-name" not in html_content:
        return []

    elements = []
    start = html_content.find('<div class="summary">')
    content_start = html_content.find('<div class="layout">', start)
    if content_start < 0:
        content_start = html_content.find('<div class="content">', start)
    if start < 0 or content_start < 0:
        return []

    summary_html = html_content[start:content_start]

    if "sum-cat-name" in summary_html:
        # V2 format
        for chunk in re.split(r'<div class="sum-cat">', summary_html)[1:]:
            cat_m = re.search(r'<span class="sum-cat-name">([^<]+)</span>', chunk)
            if not cat_m:
                continue
            cat = unescape(cat_m.group(1))
            titles = re.findall(r'<span class="sum-item">(.*?)</span>', chunk)
            titles = [re.sub(r"<[^>]+>", "", unescape(t)).strip() for t in titles if re.sub(r"<[^>]+>", "", t).strip()]
            if titles:
                lines = f"**{cat}**\n" + "\n".join(f"• {t}" for t in titles)
                elements.append({"tag": "div", "text": {"tag": "lark_md", "content": lines}})
    else:
        # V1 format
        for chunk in re.split(r'<div class="summary-item">', summary_html)[1:]:
            cat_m = re.search(r'<span class="cat-tag[^"]*">([^<]+)</span>', chunk)
            if not cat_m:
                continue
            cat = unescape(cat_m.group(1))
            titles = re.findall(r'<span class="summary-title">(.*?)</span>', chunk)
            titles = [re.sub(r"<[^>]+>", "", unescape(t)).strip() for t in titles if re.sub(r"<[^>]+>", "", t).strip()]
            if titles:
                lines = f"**{cat}**\n" + "\n".join(f"• {t}" for t in titles)
                elements.append({"tag": "div", "text": {"tag": "lark_md", "content": lines}})

    return elements


def push_feishu(dates: list[str]):
    import httpx

    if not FEISHU_WEBHOOK:
        print("  skip FEISHU_WEBHOOK not set")
        return

    for date in dates:
        gh_url = f"https://LinkX-Capital.github.io/ai-daily-news/daily-ai-news-{date}.html"

        # 要点速览内容
        summary_elements = _parse_summary_from_html(date)

        elements = []
        if summary_elements:
            elements.extend(summary_elements)
            elements.append({"tag": "hr"})
        elements.append({
            "tag": "action",
            "actions": [
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "查看日报"},
                    "url": gh_url,
                    "type": "primary",
                }
            ],
        })

        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": f"{date} AI 前沿动态"},
                    "template": "blue",
                },
                "elements": elements,
            },
        }

        r = httpx.post(FEISHU_WEBHOOK, json=payload, timeout=10)
        if r.status_code == 200:
            print(f"  feishu ok {date}")
        else:
            print(f"  feishu fail {date} {r.status_code} {r.text}")


async def main():
    print("screenshot")
    for date in DATES:
        await take_screenshot(date)

    print("feishu")
    push_feishu(DATES)


if __name__ == "__main__":
    asyncio.run(main())
