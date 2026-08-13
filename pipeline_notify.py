#!/usr/bin/env python3
"""Send the published daily-news link to Feishu using an environment credential."""

from __future__ import annotations

import argparse
from datetime import date
from html import unescape
import json
import os
from pathlib import Path
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_DIR = Path(__file__).resolve().parent


def _valid_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc
    if parsed.isoformat() != value:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD")
    return value


def _clean_html_text(value: str) -> str:
    """Convert a short HTML fragment to the plain text accepted by card Markdown."""
    return re.sub(r"<[^>]+>", "", unescape(value)).strip()


def _summary_elements(report_date: str, base_dir: Path = BASE_DIR) -> list[dict]:
    """Build Feishu card blocks from the report's rendered briefing section."""
    html_path = base_dir / f"daily-ai-news-{report_date}.html"
    try:
        html_content = html_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return []

    summary_start = html_content.find('<div class="summary">')
    if summary_start < 0:
        return []

    summary_end_candidates = [
        position
        for marker in ('<div class="layout">', '<div class="content">')
        if (position := html_content.find(marker, summary_start)) >= 0
    ]
    if not summary_end_candidates:
        return []
    summary_html = html_content[summary_start : min(summary_end_candidates)]

    elements: list[dict] = []
    if "sum-cat-name" in summary_html:
        chunks = re.split(r'<div\s+class=["\']sum-cat["\']\s*>', summary_html)[1:]
        category_pattern = r'<span\s+class=["\']sum-cat-name["\']\s*>(.*?)</span>'
        title_pattern = r'<span\s+class=["\']sum-item["\']\s*>(.*?)</span>'
        expected_categories = summary_html.count("sum-cat-name")
        expected_titles = summary_html.count("sum-item")
    else:
        chunks = re.split(
            r'<div\s+class=["\']summary-item["\']\s*>', summary_html
        )[1:]
        category_pattern = r'<span\s+class=["\']cat-tag[^"\']*["\']\s*>(.*?)</span>'
        title_pattern = r'<span\s+class=["\']summary-title["\']\s*>(.*?)</span>'
        expected_categories = summary_html.count("cat-tag")
        expected_titles = summary_html.count("summary-title")

    parsed_titles = 0
    for chunk in chunks:
        category_match = re.search(category_pattern, chunk, flags=re.DOTALL)
        if not category_match:
            continue
        category = _clean_html_text(category_match.group(1))
        titles = [
            cleaned
            for title in re.findall(title_pattern, chunk, flags=re.DOTALL)
            if (cleaned := _clean_html_text(title))
        ]
        if not category or not titles:
            continue
        parsed_titles += len(titles)
        content = f"**{category}**\n" + "\n".join(f"• {title}" for title in titles)
        elements.append(
            {"tag": "div", "text": {"tag": "lark_md", "content": content}}
        )

    if (
        not elements
        or len(elements) != expected_categories
        or parsed_titles != expected_titles
    ):
        return []
    return elements


def _build_payload(report_date: str, report_url: str, base_dir: Path = BASE_DIR) -> dict:
    display_date = date.fromisoformat(report_date).strftime("%m月%d日")
    summary_elements = _summary_elements(report_date, base_dir)
    if summary_elements:
        elements = [*summary_elements, {"tag": "hr"}]
    else:
        elements = [
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "今日日报已发布，点击下方按钮查看完整内容。",
                },
            },
            {"tag": "hr"},
        ]
    elements.append(
        {
            "tag": "action",
            "actions": [
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "查看日报"},
                    "url": report_url,
                    "type": "primary",
                }
            ],
        }
    )

    return {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"📡 {display_date} AI 前沿动态",
                },
                "template": "blue",
            },
            "elements": elements,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, type=_valid_date)
    args = parser.parse_args()

    webhook = os.environ.get("FEISHU_WEBHOOK", "")
    if not webhook:
        print("ℹ️ FEISHU_WEBHOOK 未设置，跳过通知")
        return 0

    public_base_url = os.environ.get(
        "PUBLIC_BASE_URL",
        "https://LinkX-Capital.github.io/ai-daily-news",
    ).rstrip("/")
    report_url = f"{public_base_url}/daily-ai-news-{args.date}.html"
    payload = _build_payload(args.date, report_url)
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(
        webhook,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            status = response.status
            raw_response = response.read()
    except HTTPError as exc:
        print(f"❌ 飞书通知失败（HTTP {exc.code}）", file=sys.stderr)
        return 1
    except (URLError, TimeoutError, OSError) as exc:
        # Do not render exception details: some clients include the credential URL.
        print(f"❌ 飞书通知失败（{type(exc).__name__}）", file=sys.stderr)
        return 1

    if status != 200:
        print(f"❌ 飞书通知失败（HTTP {status}）", file=sys.stderr)
        return 1

    try:
        result = json.loads(raw_response)
    except (UnicodeError, json.JSONDecodeError):
        print("❌ 飞书通知响应不是有效 JSON", file=sys.stderr)
        return 1

    if "code" in result:
        success = result.get("code") == 0
    elif "StatusCode" in result:
        success = result.get("StatusCode") == 0
    else:
        success = result.get("msg") == "success"
    if not success:
        code = result.get("code", result.get("StatusCode", "unknown"))
        print(f"❌ 飞书通知被拒绝（code={code}）", file=sys.stderr)
        return 1

    summary_count = sum(
        element.get("tag") == "div" for element in payload["card"]["elements"]
    )
    print(f"✅ 飞书通知已发送（正文 {summary_count} 个区块）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
