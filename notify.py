#!/usr/bin/env python3
"""AI 前沿动态 - 通知工具

飞书推送内容要求（与 feed_v5.py LLM prompt 一致）：
- 标题：是什么+为什么重要（不用媒体口吻，如"彻底告别XX"）
- body：2句话完整摘要
- key_points：从body提取新信息，不重复body
- 要点速览：只显示"是什么"（取冒号之前的部分）
- 分类：模型前沿/产业动态/算力追踪/初创&融资/研究关注
"""

import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# ========== 配置 ==========
NOTIFY_METHOD = os.environ.get("NOTIFY_METHOD", "feishu")

SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
EMAIL_FROM = os.environ.get("EMAIL_FROM", "")
EMAIL_TO = os.environ.get("EMAIL_TO", "")

SLACK_WEBHOOK = os.environ.get("SLACK_WEBHOOK", "")
DINGTALK_WEBHOOK = os.environ.get("DINGTALK_WEBHOOK", "")
FEISHU_WEBHOOK = os.environ.get("FEISHU_WEBHOOK", "")

BASE_DIR = "/Users/shenyalan/ai-daily-news"
_NEWS_DATE = os.environ.get("NEWS_DATE") or datetime.now().strftime('%Y-%m-%d')
REPORT_FILE = os.path.join(BASE_DIR, f"daily-ai-news-{_NEWS_DATE}.md")


def read_report():
    if not os.path.exists(REPORT_FILE):
        return None

    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    summary = []
    in_summary = False
    for line in lines:
        if "要点汇总" in line and line.strip().startswith('#'):
            in_summary = True
            continue
        if in_summary and line.startswith("---"):
            break
        if in_summary and line.strip():
            summary.append(line.strip())

    return {
        "date": content.split("\n")[0] if content else "",
        "summary": "\n".join(summary[:6]),
        "full": content
    }


def send_email(report):
    if not SMTP_USER or not SMTP_PASS:
        print("⚠️ 邮件配置未设置")
        return False

    subject = f"AI前沿动态 {datetime.now().strftime('%m月%d日')}"
    body = f"{report['date']}\n\n## 要点汇总\n\n{report['summary']}\n\n---\n详细内容见本地文件"

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
        server.quit()
        print("✅ 邮件已发送")
        return True
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False


def send_slack(report):
    if not SLACK_WEBHOOK:
        print("⚠️ Slack 配置未设置")
        return False

    import httpx

    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": "📡 AI 前沿动态"}},
        {"type": "section", "text": {"type": "mrkdwn", "text": report['summary'][:500]}},
        {"type": "actions", "elements": [{"type": "button", "text": {"type": "plain_text", "text": "查看详情"}, "url": f"https://yl0223-ai.github.io/ai-daily-news/daily-ai-news-{datetime.now().strftime("%Y-%m-%d")}.html"}]}
    ]

    try:
        r = httpx.post(SLACK_WEBHOOK, json={"blocks": blocks}, timeout=10)
        print("✅ Slack 通知已发送" if r.status_code == 200 else f"❌ Slack 发送失败: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Slack 发送失败: {e}")
        return False


def send_dingtalk(report):
    if not DINGTALK_WEBHOOK:
        print("⚠️ 钉钉配置未设置")
        return False

    import httpx

    text = f"# AI 前沿动态\n\n{report['summary']}\n\n---\n详细报告见本地文件"

    try:
        r = httpx.post(DINGTALK_WEBHOOK, json={"msgtype": "markdown", "markdown": {"title": "AI前沿动态", "text": text}}, timeout=10)
        print("✅ 钉钉通知已发送" if r.status_code == 200 else f"❌ 钉钉发送失败: {r.status_code}")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ 钉钉发送失败: {e}")
        return False


def send_feishu(report):
    if not FEISHU_WEBHOOK:
        print("⚠️ 飞书配置未设置")
        return False

    import httpx
    from datetime import datetime
    import re
    from html import unescape

    # 日期
    from datetime import datetime as _dt
    _date_obj = _dt.strptime(_NEWS_DATE, '%Y-%m-%d')
    date_str = _date_obj.strftime("%m月%d日")

    # 直接从 HTML 文件读取要点速览
    html_file = f"/Users/shenyalan/ai-daily-news/daily-ai-news-{_NEWS_DATE}.html"
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except:
        # 失败则用旧的 report
        html_content = ""

    # 构建元素
    elements = []

    # 如果成功读取 HTML，解析要点速览
    if html_content and ("要点速览" in html_content or "Briefing" in html_content or "sum-cat-name" in html_content):
        # 提取摘要部分 - 从 <div class="summary"> 到下一个主要区块
        start = html_content.find('<div class="summary">')
        # V2 用 <div class="layout">，V1 用 <div class="content">
        content_start = html_content.find('<div class="layout">', start)
        if content_start < 0:
            content_start = html_content.find('<div class="content">', start)
        if start >= 0 and content_start >= 0:
            summary_html = html_content[start:content_start]

            # 按sum-cat分割（兼容 V2 和 V1）
            # V2: <div class="sum-cat"> ... <span class="sum-cat-name"> ... <span class="sum-item">
            # V1: <div class="summary-item"> ... <span class="cat-tag"> ... <span class="summary-title">
            if 'sum-cat-name' in summary_html:
                # V2 format
                items_html = re.split(r'<div class="sum-cat">', summary_html)
                for item_html in items_html[1:]:
                    cat_match = re.search(r'<span class="sum-cat-name">([^<]+)</span>', item_html)
                    if not cat_match:
                        continue
                    cat = unescape(cat_match.group(1))

                    titles = re.findall(r'<span class="sum-item">(.*?)</span>', item_html)
                    titles = [re.sub(r'<[^>]+>', '', unescape(t)).strip() for t in titles if re.sub(r'<[^>]+>', '', t).strip()]

                    if titles:
                        lines = f"**{cat}**\n" + "\n".join(f"• {t}" for t in titles)
                        elements.append({
                            "tag": "div",
                            "text": {"tag": "lark_md", "content": lines}
                        })
            else:
                # V1 format
                items_html = re.split(r'<div class="summary-item">', summary_html)
                for item_html in items_html[1:]:
                    cat_match = re.search(r'<span class="cat-tag[^"]*">([^<]+)</span>', item_html)
                    if not cat_match:
                        continue
                    cat = unescape(cat_match.group(1))

                    titles = re.findall(r'<span class="summary-title">(.*?)</span>', item_html)
                    titles = [re.sub(r'<[^>]+>', '', unescape(t)).strip() for t in titles if re.sub(r'<[^>]+>', '', t).strip()]

                    if titles:
                        lines = f"**{cat}**\n" + "\n".join(f"• {t}" for t in titles)
                        elements.append({
                            "tag": "div",
                            "text": {"tag": "lark_md", "content": lines}
                        })
    else:
        # 备用：从 report 解析
        summary_lines = report.get('summary', '').split('\n')
        for line in summary_lines:
            if line.strip() and '：' in line:
                parts = line.split('：', 1)
                cat = parts[0].replace('- ', '').strip()
                content = parts[1] if len(parts) > 1 else ''
                elements.append({
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": f"**{cat}**：{content}"}
                })

    # 添加分隔和查看详情按钮
    elements.append({"tag": "hr"})
    elements.append({
        "tag": "action",
        "actions": [
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "📖 查看详情"},
                "url": f"https://yl0223-ai.github.io/ai-daily-news/daily-ai-news-{_NEWS_DATE}.html",
                "type": "primary"
            }
        ]
    })

    payload = {
        "msg_type": "interactive",
        "card": {
            "header": {"title": {"tag": "plain_text", "content": "📡 " + date_str + " AI 前沿动态"}, "template": "blue"},
            "elements": elements
        }
    }

    try:
        r = httpx.post(FEISHU_WEBHOOK, json=payload, timeout=10)
        print("✅ 飞书通知已发送" if r.status_code == 200 else f"❌ 飞书发送失败: {r.status_code} - {r.text}")
        return r.status_code == 200
    except Exception as e:
        print(f"❌ 飞书发送失败: {e}")
        return False


def notify():
    report = read_report()
    if not report:
        print("❌ 未找到报告文件")
        return False

    if NOTIFY_METHOD == "email":
        return send_email(report)
    elif NOTIFY_METHOD == "slack":
        return send_slack(report)
    elif NOTIFY_METHOD == "dingtalk":
        return send_dingtalk(report)
    elif NOTIFY_METHOD == "feishu":
        return send_feishu(report)
    else:
        print(f"⚠️ 未知的通知方式: {NOTIFY_METHOD}")
        return False


if __name__ == "__main__":
    notify()
