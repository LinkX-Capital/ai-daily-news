#!/usr/bin/env python3
"""Twitter 动态推送 - 抓取、生成预览并通过新飞书机器人私发。"""

import sys
import json
import re
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent))

from tweet_fetcher import get_tweets
from llm_config import API_KEY as LLM_API_KEY, API_URL as LLM_API_URL, MODEL_MAIN, light_model, light_extra, llm_headers

PRIMARY_LIMIT = 5
SECONDARY_LIMIT = 3
BEIJING = ZoneInfo("Asia/Shanghai")
DAILY_WISHES = (
    "愿今天有件小事，让你偷偷开心。",
    "愿你的好奇心，今天也有收获。",
    "愿你走的每一步，都更靠近喜欢的生活。",
    "把今天过成一杯刚好合口的咖啡。",
    "愿忙碌的间隙，也有一阵轻松的风。",
    "今天，也请给自己留一点温柔。",
    "愿你的认真，被生活轻轻接住。",
    "愿你今天遇见一个值得记住的小瞬间。",
    "愿手里的事情顺利，心里的事情有着落。",
    "慢慢来，沿途也有值得看的风景。",
    "愿今天的你，有灵感，也有好心情。",
    "给自己一点时间，好事正在慢慢发生。",
    "愿今天的阳光，刚好落在你的肩上。",
    "愿你在自己的节奏里，过一个舒服的今天。",
    "愿所有小小的期待，都有温柔的回音。",
    "今天也许会有一份意料之外的喜欢。",
    "愿你有开始的勇气，也有停下来歇歇的自在。",
    "愿你的日常里，多一点轻盈的时刻。",
    "愿今天的努力，长成明天的小惊喜。",
    "祝你今天，心里有光，手边有暖。",
    "愿你抬头的时候，刚好看见喜欢的天空。",
    "愿灵感在路上，也在你放松的那一刻。",
    "愿今天的相遇，带来一点新鲜和欢喜。",
    "愿你把日子过得有滋味，也有余地。",
    "今天，愿你对世界的好奇得到一点回应。",
    "愿你拥有一小段，完全属于自己的好时光。",
    "愿今天有好消息，也有好好吃饭的时间。",
    "愿你喜欢的小事，恰好也在今天发生。",
    "愿每个平常的今天，都藏着一点可爱。",
    "愿你带着轻松的心情，遇见今天的新鲜事。",
)


def daily_blessing(date_str):
    """每天随机选一句原创赠言；同一天的所有展示保持一致。"""
    day = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
    index = int.from_bytes(hashlib.sha256(day.encode()).digest()[:8], "big")
    return DAILY_WISHES[index % len(DAILY_WISHES)]


def split_highlights(highlights):
    """兼容旧缓存，并在每个展示出口执行 5 + 3 的硬上限。"""
    primary, secondary = [], []
    for i, item in enumerate(highlights or []):
        tier = item.get('tier') or ('primary' if i < PRIMARY_LIMIT else 'secondary')
        if tier == 'primary' and len(primary) < PRIMARY_LIMIT:
            primary.append(item)
        elif tier == 'secondary' and len(secondary) < SECONDARY_LIMIT:
            secondary.append(item)
    return primary, secondary


def _require_summaries(items):
    for item in items:
        summary = item.get('summary')
        if not isinstance(summary, str) or not summary.strip():
            raise ValueError(f"动态缺少一句话说明，补全后才能发布：{item.get('title', '')}")


def _normalize_highlights(data, selected):
    if not isinstance(data, dict) or not isinstance(data.get('highlights'), list):
        raise ValueError('重点提炼缺少 highlights 数组')
    normalized, seen_indices, seen_events = [], set(), set()
    for row in data['highlights']:
        if not isinstance(row, dict):
            raise ValueError('重点条目必须是对象')
        idx = row.get('idx')
        related = row.get('related_idxs', [idx])
        if not isinstance(related, list):
            raise ValueError('related_idxs 必须是数组')
        evidence = [idx, *related]
        if any(type(value) is not int or not 1 <= value <= len(selected) for value in evidence):
            raise ValueError('重点引用了不存在的推文')
        tier = row.get('tier')
        title, summary, event_key = (row.get(key) for key in ('title', 'summary', 'event_key'))
        if tier not in {'primary', 'secondary'} or not all(isinstance(v, str) and v.strip() for v in (title, summary, event_key)):
            raise ValueError('重点缺少分层、标题、事实摘要或事件标识')
        event_key = event_key.strip().casefold()
        if event_key in seen_events or seen_indices.intersection(evidence):
            continue
        seen_events.add(event_key)
        seen_indices.update(evidence)
        normalized.append({
            'idx': idx, 'related_idxs': list(dict.fromkeys(evidence)),
            'tier': tier, 'title': title.strip(), 'summary': summary.strip(),
            'event_key': event_key,
            'source': selected[idx - 1].get('source', '').lstrip('@'),
        })
    primary, secondary = split_highlights(normalized)
    return [*primary, *secondary]


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

    # 全量候选参与比较；只去掉确定重复的原帖和已知存疑内容。
    selected = []
    seen_links = set()
    for t in tweets:
        if is_questionable_tweet(t)[0]:
            continue
        link = t.get('link', '')
        if link and link in seen_links:
            continue
        if not t.get('title', '').strip():
            continue
        if link:
            seen_links.add(link)
        selected.append(t)
    if not selected:
        return [], selected

    tweets_text = []
    for i, t in enumerate(selected, 1):
        title = t['title'].replace('\n', ' ')
        source = t['source'].replace('@', '')
        tweets_text.append(f"{i}. @{source}: {title}")

    prompt = f"""你为一位希望快速掌握当天 AI 大事的个人读者编辑动态。
完整读完全部 {len(selected)} 条候选，先按同一具体事件合并多条来源，再按行业影响、新增事实、证据强度排序。
只返回 JSON：{{"highlights": [{{"idx": 代表原帖序号, "related_idxs": [同事件的其他候选序号], "event_key": "该具体事件的唯一标识", "tier": "primary或secondary", "title": "中文短标题", "summary": "一句关键事实"}}]}}

规则：
- primary 为先看，最多 {PRIMARY_LIMIT} 条；secondary 为按需看，最多 {SECONDARY_LIMIT} 条。条数是上限，宁缺毋滥，不凑数。
- primary 优先改变模型能力、产品可用性或行业格局的关键发布、突破、融资和收购；secondary 放重要评测、论文或配套进展。
- 头部全新一代模型发布、重大融资收购的行业影响通常高于开发框架的小版本更新。同一事件的转发和配套支持数量不增加它的重要性。
- 一个具体事件只出现一次；官方公告、转发、第三方评测和部署支持归入同一事件。不同产品的不同事件保持独立。
- 有原作者时优先引用原作者。转发只有新增重要信息或其原帖不在候选时才作为代表；宣传、祝贺和空泛预告放弃。
- 原作者不在候选时，可信转发中明确的重大公告也正常参与排序，不因转发形式漏掉大事。
- title 通常不超过 28 个中文字；每条必须有一句非空的 summary，通常不超过 60 个中文字，具体交代主体在做什么、产品作用或发布范围。不重复标题，不写泛泛意义或建议，不用“未披露”等说明填充。给定原文不足以写出一句具体说明时，该条不入选，不能只留标题。
- 用日常中文，融资写“首期交割”等清楚的说法，不用“初关”等行话；赠言由程序单独生成，此处只返回新闻内容。
- 只能使用候选原文中明确给出的事实、数字、时间和因果关系；原文被截断时不补猜。融资目标不写成已到账，厂商自评注明主体。
- 公司名、人名、产品名保持英文。idx 和 related_idxs 只能引用真实候选序号。event_key 对同一事件必须一致。

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
                    json={**light_extra(), "model": light_model(MODEL_MAIN), "max_tokens": 4000, "messages": [{"role": "user", "content": prompt}]},
                    timeout=60
                )
                if response.status_code == 200:
                    result = response.json()
                    content_text = ""
                    for item in result.get("content", []):
                        if item.get("type") == "text":
                            content_text = item.get("text", "")
                            break
                    data = _extract_json(content_text)
                    if data is not None:
                        return _normalize_highlights(data, selected), selected
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
            json={"model": "GLM-4.7", "max_tokens": 4000, "messages": [{"role": "user", "content": prompt}]},
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            content_text = result["choices"][0]["message"]["content"]
            data = _extract_json(content_text)
            if data is not None:
                return _normalize_highlights(data, selected), selected
    except Exception:
        pass

    return None, selected


def build_highlight_records(highlights, selected):
    """把 LLM 重点（带 idx）映射回原始推文，生成可回流日报候选池的记录。"""
    by_idx = {i: t for i, t in enumerate(selected, 1)}
    records = []
    for i, h in enumerate(highlights or []):
        rec = {
            "title": h.get('title', ''),
            "source": (h.get('source') or '').replace('@', ''),
            "summary": h.get('summary', ''),
            "tier": h.get('tier') or ('primary' if i < PRIMARY_LIMIT else 'secondary'),
            "event_key": h.get('event_key', ''),
        }
        t = by_idx.get(h.get('idx'))
        if t:
            rec["source"] = t.get('source', '').lstrip('@')
            rec["tweet_title"] = (t.get('title') or '')[:200]
            rec["link"] = t.get('link', '')
            rec["published"] = t.get('published', '')
            rec["related_links"] = list(dict.fromkeys(
                by_idx[idx].get('link', '') for idx in h.get('related_idxs', []) if idx in by_idx
            ))
        records.append(rec)
    primary, secondary = split_highlights(records)
    return [*primary, *secondary]




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
    lines.append(f"# {daily_blessing(date_str)}")
    lines.append(f"**日期**：{date_str} · AI 动态")
    lines.append(f"**更新**：{datetime.now(BEIJING).strftime('%Y-%m-%d %H:%M')} 北京时间")
    lines.append("")

    primary, secondary = split_highlights(highlights)
    _require_summaries([*primary, *secondary])
    lines.extend([f"## 先看 · {len(primary)} 条", ""])

    def append_items(items):
        for i, item in enumerate(items, 1):
            lines.append(f"{i}. **{item.get('title', '')}**")
            if item.get('summary'):
                lines.append(f"   {item['summary']}")
            source = item.get('source', '').lstrip('@')
            link = item.get('link', '')
            attribution = f"[@{source}]({link})" if link else f"@{source}"
            if item.get('context_url'):
                attribution += f" · [公告]({item['context_url']})"
            lines.append(f"   {attribution}")
            lines.append("")

    if primary:
        append_items(primary)
    else:
        lines.extend(['重点提炼暂不可用，原始推文已保留。' if highlights is None else '今天暂无需要优先阅读的新动态。', ''])
    if secondary:
        lines.extend(['<details>', f'<summary>按需看 · {len(secondary)} 条</summary>', ''])
        append_items(secondary)
        lines.extend(['</details>', ''])

    lines.append("---")
    lines.append("")
    lines.append(f"## 完整推文 · {total} 条")
    lines.append("")
    lines.append("抓取范围：最近 24 小时；来源按账号分组。")
    if questionable:
        lines.append(f"其中 {len(questionable)} 条存疑内容已标注。")
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
        f"<h3>{escape(daily_blessing(date_str))}</h3>",
        f"<p>共 {len(cache)} 条推文：公司发布 {cats.get('Company', 0)} 条，"
        f"研究者动态 {cats.get('Researcher', 0)} 条</p>",
    ]
    text_lines = [subject, daily_blessing(date_str), ""]
    primary, secondary = split_highlights(highlight_records)
    for heading, group in [('先看', primary), ('按需看', secondary)]:
        if not group:
            continue
        parts.append(f'<h4>{heading}</h4>')
        text_lines.append(f'{heading}：')
        items = []
        for record in group:
            title = escape(record.get('title', ''))
            source = escape(record.get('source', ''))
            link = record.get('link', '')
            label = f'<a href="{escape(link)}">{title}</a>' if link else title
            items.append(f"<li>{label}<br><small>@{source}</small></li>")
            text_lines.append(f"- {record.get('title', '')}（@{record.get('source', '')}）{link}")
        parts.append("<ol>" + "".join(items) + "</ol>")
    if not primary and not secondary:
        parts.append("<p>今日未能提取重点，请查看全部推文。</p>")
        text_lines.append("今日未能提取重点，请查看全部推文。")
    parts.append(f'<p><a href="{preview_url}">👉 查看全部推文</a></p>')
    text_lines += ["", f"查看全部推文：{preview_url}"]
    return subject, "".join(parts), "\n".join(text_lines) + "\n"


def push_to_feishu(cache, webhook_url, highlights=None, date_str=None):
    """旧版群 webhook 发送器；自动管线改用 push_twitter_to_feishu。"""
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


def build_twitter_card(cache, highlights, date_str):
    """个人阅览：每日赠言、最多五条直读、最多三条默认折叠。"""
    from html import escape

    primary, secondary = split_highlights(highlights)
    _require_summaries([*primary, *secondary])

    def item_elements(items):
        elements = []
        for i, item in enumerate(items, 1):
            title = escape(item.get('title', ''))
            source = escape(item.get('source', '').lstrip('@'))
            link = item.get('link', '')
            attribution = f"[@{source}]({link})" if link else f"@{source}"
            if item.get('context_url'):
                attribution += f" · [公告]({item['context_url']})"
            elements.append({'tag': 'markdown', 'content': f"**{i:02d}  {title}**"})
            if item.get('summary'):
                elements.append({'tag': 'markdown', 'content': escape(item['summary'])})
            elements.append({'tag': 'markdown', 'content': attribution, 'text_size': 'notation'})
        return elements

    items = item_elements(primary)
    if not items:
        message = '重点提炼暂不可用，原始推文已保留。' if highlights is None else '今天暂无需要优先阅读的新动态。'
        items = [{'tag': 'markdown', 'content': message}]

    elements = [{
        'tag': 'column_set', 'flex_mode': 'none',
        'columns': [{
            'tag': 'column', 'width': 'weighted', 'weight': 1,
            'vertical_spacing': '8px',
            'elements': [{'tag': 'markdown', 'content': '**先看**'}, *items],
        }],
    }]
    if secondary:
        elements.append({
            'tag': 'collapsible_panel', 'expanded': False,
            'header': {'title': {'tag': 'plain_text', 'content': f'按需看 · {len(secondary)} 条'}},
            'vertical_spacing': '8px', 'elements': item_elements(secondary),
        })
    elements.extend([
        {'tag': 'markdown', 'content': f"<font color='grey'>筛自 {len(cache)} 条推文 · {date_str}</font>", 'text_size': 'notation'},
        {
            'tag': 'button', 'type': 'primary_filled', 'width': 'fill',
            'text': {'tag': 'plain_text', 'content': '查看全部 Twitter 动态'},
            'behaviors': [{'type': 'open_url', 'default_url': f'https://linkx-capital.github.io/ai-daily-news/twitter-preview-{date_str}.md'}],
        },
    ])

    return {
        'schema': '2.0',
        'config': {'width_mode': 'default'},
        'header': {
            'title': {'tag': 'plain_text', 'content': daily_blessing(date_str)},
            'subtitle': {'tag': 'plain_text', 'content': f'{date_str} · AI 前沿动态 · Twitter'},
            'template': 'blue',
            'icon': {'tag': 'standard_icon', 'token': 'ai-common_colorful'},
        },
        'body': {
            'padding': '12px 12px 20px 12px',
            'vertical_spacing': '12px',
            'elements': elements,
        },
    }


def push_twitter_to_feishu(cache, highlights, date_str):
    """与日报共用新飞书应用和收件人，避免继续投递到旧群 webhook。"""
    from feishu_push import send_card

    return send_card(build_twitter_card(cache, highlights, date_str))


def main():
    import sys
    import os
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
    records = build_highlight_records(highlights, selected) if highlights is not None else None

    # 2.5 重点落盘：feed_v5 次日运行时读取，给命中候选加排序权重
    hl_path = Path(__file__).parent / 'cache' / f'twitter_highlights_{date_str}.json'
    try:
        hl_path.parent.mkdir(exist_ok=True)
        hl_path.write_text(json.dumps({
            "date": date_str,
            "generated_at": datetime.now(BEIJING).isoformat(),
            "blessing": daily_blessing(date_str),
            "highlights": records or [],
        }, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'   ⭐ 重点已回流: cache/twitter_highlights_{date_str}.json')
    except Exception as e:
        print(f'   ⚠️ 重点回流落盘失败: {e}')

    # 3. 生成预览
    print('📝 生成 preview...')
    generate_preview_md(tweets, preview_path, records, date_str=date_str)
    print(f'   已保存到 {preview_path}')

    # 4. 推送飞书
    print('📨 通过新飞书机器人私发 Twitter 动态...')
    feishu_ok = push_twitter_to_feishu(
        tweets, records, date_str
    )
    if feishu_ok:
        print('   ✅ 飞书私信推送成功')
    else:
        print('   ❌ 飞书私信推送失败')

    # 5. 推送到 GitHub
    print('🔄 推送到 GitHub...')
    import subprocess
    date_str_for_git = date_str  # 使用与 preview 一致的日期
    try:
        subprocess.run(['git', 'add', f'twitter-preview-{date_str_for_git}.md'], check=True, capture_output=True, cwd=Path(__file__).resolve().parent)
        subprocess.run(['git', 'commit', '-m', f'twitter preview {date_str_for_git}', '--', f'twitter-preview-{date_str_for_git}.md'], check=True, capture_output=True, cwd=Path(__file__).resolve().parent)
        subprocess.run(['git', 'push'], check=True, capture_output=True, cwd=Path(__file__).resolve().parent)
        print('   ✅ GitHub push 成功')
    except subprocess.CalledProcessError:
        print('   ⚠️ GitHub push 失败')

    # 6. 邮件推送（放在 GitHub 推送之后，邮件里的"查看全部"链接才能打开）
    if os.environ.get("EMAIL_RECIPIENTS", "").strip():
        print('📧 发送 Twitter 邮件...')
        from pipeline_notify import send_html_email
        subject, html_content, text_content = build_twitter_email(
            tweets, records, date_str
        )
        if not send_html_email(subject, html_content, text_content):
            print('   ⚠️ Twitter 邮件发送失败，不影响日报')

    print(f'\n✅ 完成: {datetime.now().strftime("%H:%M:%S")}')
    if not feishu_ok:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
