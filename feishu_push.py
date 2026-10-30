#!/usr/bin/env python3
from __future__ import annotations

"""飞书机器人推送日报卡片（私发，替代旧的截图+群webhook流程）

用法:
  python3 feishu_push.py                     # 默认今天
  python3 feishu_push.py 2026-10-29          # 指定一天
  python3 feishu_push.py 2026-10-29 2026-10-30  # 指定多天
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from html import unescape
from pathlib import Path

BASE_DIR = Path(__file__).parent
# Sheryl 的 open_id（2026-10-29 账号切换后）
RECIPIENT = "ou_77de8ed7a11a5f7f0f6bd47d0e36d0da"

DATES = sys.argv[1:] if len(sys.argv) > 1 else [datetime.now().strftime("%Y-%m-%d")]


def _parse_summary_from_html(date: str) -> list[dict]:
    """从 HTML 文件解析要点速览，返回飞书 card elements"""
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
            titles = [re.sub(r"<[^>]+>", "", unescape(t)).strip() for t in titles if re.sub(r"<[^>]+>", "", unescape(t)).strip()]
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
            titles = [re.sub(r"<[^>]+>", "", unescape(t)).strip() for t in titles if re.sub(r"<[^>]+>", "", unescape(t)).strip()]
            if titles:
                lines = f"**{cat}**\n" + "\n".join(f"• {t}" for t in titles)
                elements.append({"tag": "div", "text": {"tag": "lark_md", "content": lines}})

    return elements


def build_card(date: str) -> dict:
    gh_url = f"https://linkx-capital.github.io/ai-daily-news/daily-ai-news-{date}.html"

    elements = []
    summary_elements = _parse_summary_from_html(date)
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

    return {
        "header": {
            "title": {"tag": "plain_text", "content": f"{date} AI 前沿动态"},
            "template": "blue",
        },
        "elements": elements,
    }


def send_card(card: dict) -> bool:
    """通过 lark-cli 机器人私发 interactive 卡片，带重试（lark-cli 网络偶发超时）"""
    for attempt in range(3):
        proc = subprocess.run(
            [
                "lark-cli", "im", "+messages-send",
                "--as", "bot",
                "--user-id", RECIPIENT,
                "--msg-type", "interactive",
                "--content", json.dumps(card, ensure_ascii=False),
            ],
            capture_output=True, text=True,
        )
        if proc.returncode == 0 and '"ok": true' in proc.stdout:
            return True
        print(f"  attempt {attempt + 1} failed: {proc.stdout.strip()[:200]} {proc.stderr.strip()[:200]}")
    return False


def main():
    for date in DATES:
        card = build_card(date)
        if send_card(card):
            print(f"  feishu ok {date}")
        else:
            print(f"  feishu fail {date}")
            sys.exit(1)


if __name__ == "__main__":
    main()
