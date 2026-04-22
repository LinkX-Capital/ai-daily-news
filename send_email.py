#!/usr/bin/env python3
"""通过阿里企业邮箱发送日报截图给LP"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
from pathlib import Path


def load_env():
    """加载 .env 文件"""
    env_path = Path(__file__).parent / ".env"
    config = {}
    if not env_path.exists():
        print("❌ 缺少 .env 文件，请复制 .env.example 为 .env 并填写配置")
        raise SystemExit(1)
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, _, value = line.partition("=")
            config[key.strip()] = value.strip()
    return config


def send_daily_email(image_path=None):
    config = load_env()
    today = datetime.now().strftime("%Y-%m-%d")
    month_day = datetime.now().strftime("%m月%d日")

    # 默认今天的截图
    if image_path is None:
        base = Path(__file__).parent
        image_path = base / "daily-ai-news-mobile.png"

    if not Path(image_path).exists():
        print(f"❌ 截图不存在: {image_path}")
        raise SystemExit(1)

    # 构建邮件
    subject = f"全球AI前沿动态 {today}｜星连资本"
    recipients = [r.strip() for r in config["EMAIL_RECIPIENTS"].split(",")]

    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = config["SMTP_USER"]
    msg["To"] = ", ".join(recipients)

    # HTML 正文
    html_body = f"""
    <div style="font-family: -apple-system, sans-serif; max-width: 600px; margin: 0 auto;">
        <p>各位好，</p>
        <p>以下是{month_day}的全球AI前沿动态，请查收。</p>
        <p><img src="cid:daily_image" style="width: 100%; max-width: 375px; border-radius: 8px;"></p>
        <p style="color: #999; font-size: 12px;">此邮件由系统自动发送，如有问题请联系 shenyalan@linkxcap.com</p>
    </div>
    """
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    # 附件图片（内嵌）
    with open(image_path, "rb") as f:
        img = MIMEImage(f.read())
        img.add_header("Content-ID", "<daily_image>")
        img.add_header("Content-Disposition", "inline",
                       filename=f"daily-ai-news-{today}.png")
        msg.attach(img)

    # 发送
    print(f"📧 正在发送邮件至 {len(recipients)} 位收件人...")
    try:
        server = smtplib.SMTP_SSL(config["SMTP_SERVER"], int(config["SMTP_PORT"]))
        server.login(config["SMTP_USER"], config["SMTP_PASSWORD"])
        server.sendmail(config["SMTP_USER"], recipients, msg.as_string())
        server.quit()
        print(f"✅ 邮件已发送: {subject}")
    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP 认证失败，请检查邮箱和授权码")
        raise SystemExit(1)
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    send_daily_email()
