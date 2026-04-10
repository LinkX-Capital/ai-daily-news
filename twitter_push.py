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


def extract_highlights_llm(tweets: list) -> list:
    """用 LLM 提取今日重点（MiniMax 优先，GLM-4.7 备用）"""
    import os
    import httpx
    import time

    tweets_text = []
    for i, t in enumerate(tweets[:10], 1):
        title = t['title'].replace('\n', ' ')
        source = t['source'].replace('@', '')
        tweets_text.append(f"{i}. @{source}: {title}")

    prompt = f"""返回JSON：{{"highlights": [{{"title": "标题", "source": "来源"}}]}}

推文：
{chr(10).join(tweets_text)}"""

    # 1. 尝试 MiniMax
    minimax_key = os.environ.get("MINIMAX_API_KEY", "")
    if minimax_key:
        for attempt in range(3):
            try:
                response = httpx.post(
                    "https://api.minimaxi.com/anthropic/v1/messages",
                    headers={"Authorization": f"Bearer {minimax_key}", "Content-Type": "application/json"},
                    json={"model": "minimaxi-text-01", "max_tokens": 1000, "messages": [{"role": "user", "content": prompt}]},
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
                        return data.get("highlights", [])
            except Exception:
                if attempt < 2:
                    time.sleep(2)
                    continue
                break

    # 2. 备用 GLM-4.7
    glm_key = os.environ.get("ZHIPU_API_KEY", "")
    if not glm_key:
        glm_key = "5f650035e5a845549e4765184d8179b1.GdehlMpHT0dKq3m3"
    try:
        response = httpx.post(
            "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            headers={"Authorization": f"Bearer {glm_key}", "Content-Type": "application/json"},
            json={"model": "GLM-4.7", "max_tokens": 1000, "messages": [{"role": "user", "content": prompt}]},
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            content_text = result["choices"][0]["message"]["content"]
            data = _extract_json(content_text)
            if data:
                return data.get("highlights", [])
    except Exception:
        pass

    return None




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

    api_key = os.environ.get("MINIMAX_API_KEY", "")
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
            "https://api.minimaxi.com/anthropic/v1/messages",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "minimaxi-text-01",
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


def generate_preview_md(cache, output_path, highlights=None):
    """生成 twitter_preview.md"""
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


def push_to_feishu(cache, webhook_url, highlights=None):
    """推送到飞书"""
    import httpx

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
        highlights = extract_highlights_llm(cache)

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
                        'url': 'https://yl0223-ai.github.io/ai-daily-news/twitter_preview.md',
                        'type': 'primary'
                    }]
                }
            ]
        }
    }

    r = httpx.post(webhook_url, json=payload, timeout=10)
    return r.json()


def main():
    webhook = 'https://open.feishu.cn/open-apis/bot/v2/hook/362a7cc7-5bce-4184-9ae3-7d6b6c0c429a'
    preview_path = Path(__file__).parent / 'twitter_preview.md'

    # 1. 抓取
    print('📡 抓取 Twitter...')
    tweets = get_tweets()
    print(f'   抓取到 {len(tweets)} 条推文')

    # 2. LLM 提取重点（用于飞书推送）
    print('🔄 调用 LLM 提取...')
    highlights = extract_highlights_llm(tweets)

    # 3. 生成预览
    print('📝 生成 preview...')
    generate_preview_md(tweets, preview_path, highlights)
    print(f'   已保存到 {preview_path}')

    # 4. 推送飞书
    print('📨 推送飞书...')
    result = push_to_feishu(tweets, webhook, highlights)
    if result.get('msg') == 'success':
        print('   ✅ 飞书推送成功')
    else:
        print(f'   ❌ 飞书推送失败: {result}')

    # 5. 推送到 GitHub
    print('🔄 推送到 GitHub...')
    import subprocess
    date_str_for_git = datetime.now().strftime("%Y-%m-%d")
    try:
        subprocess.run(['git', 'add', 'twitter_preview.md'], check=True, capture_output=True, cwd='/Users/shenyalan/ai-daily-news')
        subprocess.run(['git', 'commit', '-m', f'twitter preview {date_str_for_git}'], check=True, capture_output=True, cwd='/Users/shenyalan/ai-daily-news')
        subprocess.run(['git', 'push'], check=True, capture_output=True, cwd='/Users/shenyalan/ai-daily-news')
        print('   ✅ GitHub push 成功')
    except subprocess.CalledProcessError:
        print('   ⚠️ GitHub push 失败')

    print(f'\n✅ 完成: {datetime.now().strftime("%H:%M:%S")}')


if __name__ == '__main__':
    main()
