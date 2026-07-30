#!/usr/bin/env python3
"""Send the published daily-news link to Feishu using an environment credential."""

from __future__ import annotations

import argparse
from datetime import date
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def _valid_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc
    if parsed.isoformat() != value:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD")
    return value


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
    display_date = date.fromisoformat(args.date).strftime("%m月%d日")
    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": f"📡 {display_date} AI 前沿动态",
                },
                "template": "blue",
            },
            "elements": [
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
            ],
        },
    }
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

    print("✅ 飞书通知已发送")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
