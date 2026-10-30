#!/usr/bin/env python3
"""Send the published daily-news link to Feishu, WeChat (PushPlus) and/or email using environment credentials."""

from __future__ import annotations

import argparse
from datetime import date
from email.message import EmailMessage
from html import escape, unescape
import json
import os
from pathlib import Path
import re
import smtplib
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


def _summary_sections(report_date: str, base_dir: Path = BASE_DIR) -> list[tuple[str, list[str]]]:
    """Parse (category, titles) pairs from the report's rendered briefing section."""
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

    sections: list[tuple[str, list[str]]] = []
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
        sections.append((category, titles))

    if (
        not sections
        or len(sections) != expected_categories
        or parsed_titles != expected_titles
    ):
        return []
    return sections


def _summary_elements(report_date: str, base_dir: Path = BASE_DIR) -> list[dict]:
    """Build Feishu card blocks from the report's rendered briefing section."""
    return [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": f"**{category}**\n" + "\n".join(f"• {title}" for title in titles),
            },
        }
        for category, titles in _summary_sections(report_date, base_dir)
    ]


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


def _build_pushplus_payload(
    report_date: str, report_url: str, token: str, base_dir: Path = BASE_DIR
) -> dict:
    """PushPlus message (HTML template) shown in WeChat."""
    title, content = _build_html_message(report_date, report_url, base_dir)
    return {
        "token": token,
        "title": title,
        "content": content,
        "template": "html",
    }


def _build_html_message(
    report_date: str, report_url: str, base_dir: Path = BASE_DIR
) -> tuple[str, str]:
    """(title, HTML body) shared by the WeChat and email channels."""
    display_date = date.fromisoformat(report_date).strftime("%m月%d日")
    sections = _summary_sections(report_date, base_dir)
    if sections:
        parts = [
            f"<h4>{escape(category)}</h4><ul>"
            + "".join(f"<li>{escape(title)}</li>" for title in titles)
            + "</ul>"
            for category, titles in sections
        ]
    else:
        parts = ["<p>今日日报已发布，点击下方链接查看完整内容。</p>"]
    parts.append(f'<p><a href="{escape(report_url)}">👉 查看完整日报</a></p>')
    return f"📡 {display_date} AI 前沿动态", "".join(parts)


def _build_email(
    report_date: str, report_url: str, sender: str, recipients: list[str],
    base_dir: Path = BASE_DIR,
) -> EmailMessage:
    title, content = _build_html_message(report_date, report_url, base_dir)
    return _compose_email(
        title, content, f"{title}\n\n查看完整日报：{report_url}\n", sender, recipients
    )


def _compose_email(
    subject: str, html_content: str, text_content: str, sender: str, recipients: list[str]
) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message.set_content(text_content)
    message.add_alternative(f"<html><body>{html_content}</body></html>", subtype="html")
    return message


def _send_email(report_date: str, report_url: str) -> bool:
    title, content = _build_html_message(report_date, report_url)
    return send_html_email(title, content, f"{title}\n\n查看完整日报：{report_url}\n")


def send_html_email(subject: str, html_content: str, text_content: str) -> bool:
    """Send one HTML email to EMAIL_RECIPIENTS with the SMTP_* settings (also used by twitter_push)."""
    recipients = [
        address.strip()
        for address in os.environ.get("EMAIL_RECIPIENTS", "").split(",")
        if address.strip()
    ]
    user = os.environ.get("SMTP_USER", "")
    password = os.environ.get("SMTP_PASSWORD", "")
    if not user or not password:
        print("❌ 邮件通知缺少 SMTP_USER / SMTP_PASSWORD", file=sys.stderr)
        return False
    server = os.environ.get("SMTP_SERVER", "smtp.qq.com")
    port = int(os.environ.get("SMTP_PORT", "465"))
    use_ssl = os.environ.get("SMTP_SSL", "true").lower() != "false"
    message = _compose_email(subject, html_content, text_content, user, recipients)

    try:
        if use_ssl:
            client = smtplib.SMTP_SSL(server, port, timeout=20)
        else:
            client = smtplib.SMTP(server, port, timeout=20)
        with client:
            if not use_ssl:
                client.starttls()
            client.login(user, password)
            client.send_message(message)
    except smtplib.SMTPAuthenticationError:
        print("❌ 邮件通知失败：邮箱登录被拒绝（检查 SMTP_USER 和授权码）", file=sys.stderr)
        return False
    except (smtplib.SMTPException, OSError) as exc:
        # Do not render exception details: they may echo server responses with account info.
        print(f"❌ 邮件通知失败（{type(exc).__name__}）", file=sys.stderr)
        return False
    print(f"✅ 邮件通知已发送（{len(recipients)} 个收件人）")
    return True


def _post_json(url: str, payload: dict, label: str) -> dict | None:
    """POST JSON and return the parsed response, or None after printing a safe error."""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=10) as response:
            status = response.status
            raw_response = response.read()
    except HTTPError as exc:
        print(f"❌ {label}通知失败（HTTP {exc.code}）", file=sys.stderr)
        return None
    except (URLError, TimeoutError, OSError) as exc:
        # Do not render exception details: some clients include the credential URL.
        print(f"❌ {label}通知失败（{type(exc).__name__}）", file=sys.stderr)
        return None

    if status != 200:
        print(f"❌ {label}通知失败（HTTP {status}）", file=sys.stderr)
        return None

    try:
        return json.loads(raw_response)
    except (UnicodeError, json.JSONDecodeError):
        print(f"❌ {label}通知响应不是有效 JSON", file=sys.stderr)
        return None


def _send_pushplus(token: str, report_date: str, report_url: str) -> bool:
    url = os.environ.get("PUSHPLUS_URL", "https://www.pushplus.plus/send")
    payload = _build_pushplus_payload(report_date, report_url, token)
    result = _post_json(url, payload, "微信")
    if result is None:
        return False
    # PushPlus 用 code=200 表示已受理，之后异步投递到微信。
    if result.get("code") != 200:
        print(
            f"❌ 微信通知被拒绝（code={result.get('code', 'unknown')}，{result.get('msg', '')}）",
            file=sys.stderr,
        )
        return False
    print("✅ 微信通知已发送（PushPlus）")
    return True


def _send_feishu(webhook: str, report_date: str, report_url: str) -> bool:
    payload = _build_payload(report_date, report_url)
    result = _post_json(webhook, payload, "飞书")
    if result is None:
        return False

    if "code" in result:
        success = result.get("code") == 0
    elif "StatusCode" in result:
        success = result.get("StatusCode") == 0
    else:
        success = result.get("msg") == "success"
    if not success:
        code = result.get("code", result.get("StatusCode", "unknown"))
        print(f"❌ 飞书通知被拒绝（code={code}）", file=sys.stderr)
        return False

    summary_count = sum(
        element.get("tag") == "div" for element in payload["card"]["elements"]
    )
    print(f"✅ 飞书通知已发送（正文 {summary_count} 个区块）")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True, type=_valid_date)
    args = parser.parse_args()

    webhook = os.environ.get("FEISHU_WEBHOOK", "")
    pushplus_token = os.environ.get("PUSHPLUS_TOKEN", "")
    email_recipients = os.environ.get("EMAIL_RECIPIENTS", "").strip()
    if not webhook and not pushplus_token and not email_recipients:
        print("ℹ️ FEISHU_WEBHOOK / PUSHPLUS_TOKEN / EMAIL_RECIPIENTS 均未设置，跳过通知")
        return 0

    public_base_url = os.environ.get(
        "PUBLIC_BASE_URL",
        "https://linkx-capital.github.io/ai-daily-news",
    ).rstrip("/")
    report_url = f"{public_base_url}/daily-ai-news-{args.date}.html"

    # 每个已配置的渠道都必须成功；任一失败都阻断 published。
    ok = True
    if webhook:
        ok = _send_feishu(webhook, args.date, report_url) and ok
    if pushplus_token:
        ok = _send_pushplus(pushplus_token, args.date, report_url) and ok
    if email_recipients:
        ok = _send_email(args.date, report_url) and ok
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
