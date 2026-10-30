#!/usr/bin/env python3
"""Twitter 动态推送 - 抓取+生成预览+飞书推送"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

sys.path.insert(0, str(Path(__file__).parent))

from tweet_fetcher import get_tweets
from llm_config import API_KEY as LLM_API_KEY, API_URL as LLM_API_URL, light_model, light_extra, llm_headers


def is_questionable_tweet(tweet):
    """判断推文是否存疑"""
    title = tweet.get('title', '')
    source = tweet.get('source', '').replace('@', '').lower()

    if title.startswith('R to @'):
        if source in ['openai', 'googleai', 'meta', 'claudeai']:
            return True, "公司账号自我回复"
    if title.startswith('RT by @'):
        if source in ['openai', 'googleai', 'meta', 'claudeai']:
            return True, "公司账号自我转发"

    return False, None


def extract_highlights_llm(tweets: list):
    """用 LLM 提取今日重点（MiniMax 优先，GLM-4.7 备用）。

    返回 (highlights, selected)：selected 是实际送入 LLM 的推文列表，
    highlights 各项带 idx（selected 中的 1-based 序号），供回流日报候选池时精确映射。
    """
    import os
    import httpx
    import time

    # 预筛：跳过存疑项，取前 30 条送 LLM（此前只看前 10 条会漏掉大部分重点）
    selected = []
    for t in tweets:
        if is_questionable_tweet(t)[0]:
            continue
        selected.append(t)
        if len(selected) >= 30:
            break

    tweets_text = []
    for i, t in enumerate(selected, 1):
        title = t['title'].replace('\n', ' ')
        source = t['source'].replace('@', '')
        tweets_text.append(f"{i}. @{source}: {title[:300]}")

    prompt = f"""返回JSON：{{"highlights": [{{"idx": 序号, "title": "标题", "source": "来源"}}]}}

从下列推文中选出 6-8 条当日最重要的动态（官方发布、研究突破、重要数据优先），idx 填推文序号。title 用中文写一句话标题，公司名、人名、产品名保持英文。

推文：
{chr(10).join(tweets_text)}"""

    # 1. 尝试 MiniMax
    minimax_key = LLM_API_KEY
    if minimax_key:
        for attempt in range(3):
            try:
                response = httpx.post(
                    LLM_API_URL,
                    headers=llm_headers(minimax_key),
                    json={**light_extra(), "model": light_model("minimaxi-text-01"), "max_tokens": 1500, "messages": [{"role": "user", "content": prompt}]},
                    timeout=60
                )
                if response.status_code == 200:
                    result = response.json()
                    content_text = ""
                    for item in result.get("content", []):
                        if item.get("type") == "text":
                            content_text = item.get("text", "")
                            break
                    if not content_text:
                        for item in result.get("content", []):
                            if item.get("type") == "thinking":
                                content_text = item.get("thinking", "")
                                break
                    data = _extract_json(content_text)
                    if data:
                        return data.get("highlights", []), selected
            except Exception:
                if attempt < 2:
                    time.sleep(2)
                    continue
                break

    # 2. 备用 GLM-4.7
    glm_key = os.environ.get("ZHIPU_API_KEY", "")
    if not glm_key:
        return None, selected
    try:
        response = httpx.post(
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            headers={"Authorization": f"Bearer {glm_key}", "Content-Type": "application/json"},
            json={"model": "GLM-4.7", "max_tokens": 1500, "messages": [{"role": "user", "content": prompt}]},
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            content_text = result["choices"][0]["message"]["content"]
            data = _extract_json(content_text)
            if data:
                return data.get("highlights", []), selected
    except Exception:
        pass

    return None, selected


def build_highlight_records(highlights, selected):
    """把 LLM 重点（带 idx）映射回原始推文，生成可回流日报候选池的记录。"""
    by_idx = {i: t for i, t in enumerate(selected, 1)}
    records = []
    for h in highlights or []:
        rec = {
            "title": h.get('title', ''),
            "source": (h.get('source') or '').replace('@', ''),
        }
        t = by_idx.get(h.get('idx'))
        if t:
            rec["tweet_title"] = (t.get('title') or '')[:200]
            rec["link"] = t.get('link', '')
            rec["published"] = t.get('published', '')
        records.append(rec)
    return records




def _extract_json(text: str):
    """从文本中提取 JSON"""
    import re
    import json
    
    # 方法1：代码块
    m = re.search(r'\`\`\`json\s*([\s\S]*?)\s*\`\`\`', text, re.DOTALL)
    if m:
        raw = m.group(1).strip()
        try:
            return json.loads(raw)
        except:
            pass
    
    # 方法2：找 highlights 位置
    hl_idx = text.find('"highlights"')
    if hl_idx != -1:
        start = text.rfind('{', 0, hl_idx)
        end = text.rfind('}', hl_idx) + 1
        if start != -1 and end > start:
            raw = text[start:end]
            try:
                return json.loads(raw)
            except:
                pass
    
    return None


def extract_single_title_llm(title: str, source: str) -> str:
    """用 LLM 提取单条推文的精炼标题"""
    import os
    import httpx

    api_key = LLM_API_KEY
    if not api_key:
        return title[:50] + "..." if len(title) > 50 else title

    prompt = f"""从以下推文标题中提取核心信息，生成10-20字的简明标题。

要求：
- 保留核心事件主体
- 用中文
- 去掉"RT by"、"R to"等前缀
- 直接返回标题

推文：{title}"""

    try:
        response = httpx.post(
            LLM_API_URL,
            headers=llm_headers(api_key),
            json={
                **light_extra(), "model": light_model("minimaxi-text-01"),
                "max_tokens": 50,
                "messages": [{"role": "user", "content": prompt}]
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            content = ""
            for item in result.get("content", []):
                if item.get("type") == "text":
                    content = item.get("text", "")
                    break
            if not content:
                for item in result.get("content", []):
                    if item.get("type") == "thinking":
                        content = item.get("thinking", "")
                        break
            if content:
                # 清理并返回
                return content.strip()[:50]
    except:
        pass

    return title[:50] + "..." if len(title) > 50 else title


def generate_preview_md(cache, output_path, highlights=None, date_str=None):
    """生成 twitter_preview.md"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    total = len(cache)

    # 统计存疑内容
    questionable = []
    for t in cache:
        is_q, reason = is_questionable_tweet(t)
        if is_q:
            questionable.append((t, reason))

    lines = []
    lines.append(f"# Twitter 动态预览")
    lines.append(f"**日期**：{date_str} 07:15")
    lines.append(f"**总计**：{total} 条推文")
    lines.append("")

    # 过滤说明
    lines.append("---")
    lines.append("")
    lines.append("## 📋 过滤说明")
    lines.append("")
    lines.append("**抓取规则**：24小时内、去除重复账号、内容 >30字符")
    if questionable:
        lines.append(f"**存疑过滤**：{len( questionable)}条（公司账号自我回复/转发，标注⚠️）")
    else:
        lines.append("**存疑过滤**：无")
    lines.append("")

    # 今日重点（LLM 提炼）
    if highlights:
        lines.append("---")
        lines.append("")
        lines.append("## ⭐ 今日重点（LLM 提炼）")
        lines.append("")
        for i, h in enumerate(highlights, 1):
            hl_title = h.get('title', '')
            hl_source = h.get('source', '').replace('@', '')
            lines.append(f"{i}. **{hl_title}**")
            lines.append(f"   @{hl_source}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # 按 category 分组
    by_cat = defaultdict(list)
    for t in cache:
        cat = t.get('category', '其他')
        by_cat[cat].append(t)

    by_source = defaultdict(list)
    for t in cache:
        by_source[t['source']].append(t)

    # 分类顺序
    cat_order = ['Company', 'Researcher']
    cat_emoji = {'Company': '🏢', 'Researcher': '👤'}
    cat_names = {'Company': '公司发布', 'Researcher': '研究者动态'}

    for cat in cat_order:
        if cat not in by_cat:
            continue
        tweets = by_cat[cat]
        lines.append(f"## {cat_emoji[cat]} {cat_names[cat]}（{len(tweets)}条）")
        lines.append("")

        for source, src_tweets in sorted(by_source.items()):
            if src_tweets[0].get('category') != cat:
                continue

            info = src_tweets[0]
            org = info.get('org', '')
            track = info.get('track', '')

            header = f"### {source}"
            if org:
                header += f" [{org}]"
            if track:
                header += f" | {track}"
            lines.append(header)
            lines.append("")

            for t in src_tweets:
                title = t['title'].replace('\n', ' ')
                url = t['link']
                is_q, reason = is_questionable_tweet(t)
                marker = "⚠️ " if is_q else ""
                lines.append(f"- {marker}{title}")
                lines.append(f"  [查看]({url})")
            lines.append("")

    Path(output_path).write_text('\n'.join(lines))
    return total


def build_twitter_email(cache, highlight_records, date_str):
    """(subject, html, text) for the Twitter preview email; highlights link back to each tweet."""
    from html import escape

    display_date = datetime.strptime(date_str, "%Y-%m-%d").strftime("%m月%d日")
    cats = Counter(t.get('category', '?') for t in cache)
    preview_url = f'https://linkx-capital.github.io/ai-daily-news/twitter-preview-{date_str}.md'
    subject = f"🐦 {display_date} Twitter 动态"

    parts = [
        f"<p>共 {len(cache)} 条推文：公司发布 {cats.get('Company', 0)} 条，"
        f"研究者动态 {cats.get('Researcher', 0)} 条</p>",
        "<h4>⭐ 今日重点</h4>",
    ]
    text_lines = [subject, "", "今日重点："]
    if highlight_records:
        items = []
        for record in highlight_records:
            title = escape(record.get('title', ''))
            source = escape(record.get('source', ''))
            link = record.get('link', '')
            label = f'<a href="{escape(link)}">{title}</a>' if link else title
            items.append(f"<li>{label}<br><small>@{source}</small></li>")
            text_lines.append(f"- {record.get('title', '')}（@{record.get('source', '')}）{link}")
        parts.append("<ol>" + "".join(items) + "</ol>")
    else:
        parts.append("<p>今日未能提取重点，请查看全部推文。</p>")
        text_lines.append("今日未能提取重点，请查看全部推文。")
    parts.append(f'<p><a href="{preview_url}">👉 查看全部推文</a></p>')
    text_lines += ["", f"查看全部推文：{preview_url}"]
    return subject, "".join(parts), "\n".join(text_lines) + "\n"


def push_to_feishu(cache, webhook_url, highlights=None, date_str=None):
    """推送到飞书"""
    import httpx

    if date_str is None:
        date_str = datetime.now().strftime("%m月%d日")
    total = len(cache)

    cats = Counter(t.get('category', '?') for t in cache)

    overview = f"📊 概览：{total}条推文"
    if 'Company' in cats:
        overview += f"\n- 🏢 公司发布：{cats.get('Company', 0)}条"
    if 'Researcher' in cats:
        overview += f"\n- 👤 研究者动态：{cats.get('Researcher', 0)}条"

    # LLM 提取重点（优先使用已提取的结果）
    if highlights is None:
        print("   🔄 调用 LLM 提取今日重点...")
        highlights, _ = extract_highlights_llm(cache)

    if highlights:
        print(f"   ✅ LLM 提取到 {len(highlights)} 条重点")
        highlights_lines = []
        for i, h in enumerate(highlights, 1):
            hl_title = h.get('title', '')[:40]
            hl_source = h.get('source', '').replace('@', '')
            highlights_lines.append(f"{i}. **{hl_title}**\n   {hl_source}")
        highlights_text = '\n'.join(highlights_lines)
    else:
        print("   ⚠️ LLM 不可用，使用简单截取")
        sorted_tweets = sorted(cache, key=lambda t: (
            t['title'].startswith('RT '),
            t['title'].startswith('R to @'),
            is_questionable_tweet(t)[0]
        ))
        highlights_lines = []
        for i, t in enumerate(sorted_tweets[:6], 1):
            title = t['title'].replace('\n', ' ')[:40]
            source = t['source'].replace('@', '')
            highlights_lines.append(f"{i}. **{title}**\n   {source}")
        highlights_text = '\n'.join(highlights_lines)

    card_content = f"""**📡 Twitter 动态预览**

{overview}

**⭐ 今日重点**

{highlights_text}

---
👀 查看全部 {total} 条"""

    payload = {
        'msg_type': 'interactive',
        'card': {
            'header': {
                'title': {'tag': 'plain_text', 'content': f'Twitter预览 {date_str}'},
                'template': 'blue'
            },
            'elements': [
                {'tag': 'div', 'text': {'tag': 'lark_md', 'content': card_content}},
                {'tag': 'hr'},
                {
                    'tag': 'action',
                    'actions': [{
                        'tag': 'button',
                        'text': {'tag': 'plain_text', 'content': '📖 查看详情'},
                        'url': f'https://linkx-capital.github.io/ai-daily-news/twitter-preview-{date_str}.md',
                        'type': 'primary'
                    }]
                }
            ]
        }
    }

    r = httpx.post(webhook_url, json=payload, timeout=10)
    return r.json()


def main():
    import sys
    import os
    webhook = (
        os.environ.get("FEISHU_TWITTER_WEBHOOK")
        or os.environ.get("FEISHU_WEBHOOK")
        or ""
    ).strip()
    # 支持命令行指定日期：python twitter_push.py 2026-06-19
    date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y-%m-%d")
    preview_path = Path(__file__).parent / f'twitter-preview-{date_str}.md'

    # 1. 抓取
    print('📡 抓取 Twitter...')
    tweets = get_tweets()
    print(f'   抓取到 {len(tweets)} 条推文')

    # 2. LLM 提取重点（用于飞书推送 + 次日日报候选池回流）
    print('🔄 调用 LLM 提取...')
    highlights, selected = extract_highlights_llm(tweets)

    # 2.5 重点落盘：feed_v5 次日运行时读取，给命中候选加排序权重
    hl_path = Path(__file__).parent / 'cache' / f'twitter_highlights_{date_str}.json'
    try:
        hl_path.parent.mkdir(exist_ok=True)
        hl_path.write_text(json.dumps({
            "date": date_str,
            "generated_at": datetime.now().isoformat(),
            "highlights": build_highlight_records(highlights, selected),
        }, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'   ⭐ 重点已回流: cache/twitter_highlights_{date_str}.json')
    except Exception as e:
        print(f'   ⚠️ 重点回流落盘失败: {e}')

    # 3. 生成预览
    print('📝 生成 preview...')
    generate_preview_md(tweets, preview_path, highlights, date_str=date_str)
    print(f'   已保存到 {preview_path}')

    # 4. 推送飞书
    print('📨 推送飞书...')
    if not webhook:
        print('   ℹ️ 未配置 FEISHU_TWITTER_WEBHOOK/FEISHU_WEBHOOK，跳过')
    else:
        result = push_to_feishu(tweets, webhook, highlights, date_str=date_str)
        if result.get('msg') == 'success':
            print('   ✅ 飞书推送成功')
        else:
            print(f'   ❌ 飞书推送失败: {result}')

    # 5. 推送到 GitHub
    print('🔄 推送到 GitHub...')
    import subprocess
    date_str_for_git = date_str  # 使用与 preview 一致的日期
    try:
        subprocess.run(['git', 'add', f'twitter-preview-{date_str_for_git}.md'], check=True, capture_output=True, cwd=Path(__file__).resolve().parent)
        subprocess.run(['git', 'commit', '-m', f'twitter preview {date_str_for_git}'], check=True, capture_output=True, cwd=Path(__file__).resolve().parent)
        subprocess.run(['git', 'push'], check=True, capture_output=True, cwd=Path(__file__).resolve().parent)
        print('   ✅ GitHub push 成功')
    except subprocess.CalledProcessError:
        print('   ⚠️ GitHub push 失败')

    # 6. 邮件推送（放在 GitHub 推送之后，邮件里的"查看全部"链接才能打开）
    if os.environ.get("EMAIL_RECIPIENTS", "").strip():
        print('📧 发送 Twitter 邮件...')
        from pipeline_notify import send_html_email
        subject, html_content, text_content = build_twitter_email(
            tweets, build_highlight_records(highlights, selected), date_str
        )
        if not send_html_email(subject, html_content, text_content):
            print('   ⚠️ Twitter 邮件发送失败，不影响日报')

    print(f'\n✅ 完成: {datetime.now().strftime("%H:%M:%S")}')


if __name__ == '__main__':
    main()
