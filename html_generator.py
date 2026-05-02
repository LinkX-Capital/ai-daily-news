#!/usr/bin/env python3
"""HTML 生成模块 V2 — Sequoia editorial × smol.ai layout"""

import re
import os
import sys
from datetime import datetime, timedelta
from collections import defaultdict

# 尝试导入路径配置
try:
    sys.path.insert(0, '/Users/shenyalan/ai-daily-news')
    from config_loader import base_dir, output_md, output_html
    HAS_CONFIG = True
except ImportError:
    HAS_CONFIG = False

# 分类顺序
CAT_ORDER = ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]

# 分类名称标准化
CAT_ALIASES = {
    '算力追踪': '算力追踪',
    '算力跟踪': '算力追踪',
    '算力': '算力追踪',
}


def normalize_category(cat):
    return CAT_ALIASES.get(cat, cat)


def parse_md(md_content):
    """解析 MD 字符串"""
    articles = []
    current_cat = None
    current_body_lines = []
    summary_items = {}
    in_summary = False

    lines = md_content.split('\n')
    for line in lines:
        original_stripped = line.strip()

        if ('要点汇总' in original_stripped or '要点速览' in original_stripped) and original_stripped.startswith('#'):
            in_summary = True
            continue
        if in_summary and original_stripped.startswith('---'):
            in_summary = False
            continue
        if in_summary and original_stripped.startswith('- '):
            parts = original_stripped[2:].split('：', 1)
            if len(parts) == 2:
                cat = re.sub(r'\*\*', '', parts[0].strip())
                cat = normalize_category(cat)
                items = [i.strip() for i in parts[1].split(';') if i.strip()]
                summary_items[cat] = items
            continue

        if original_stripped.startswith('### ') or (original_stripped.startswith('## ') and not original_stripped.startswith('### ')):
            cat_text = original_stripped.lstrip('#').strip()
            if cat_text not in ['📖 详细参考', '详细参考', '要点汇总', '要点速览', 'AI 前沿动态', '04月05日 AI 前沿动态']:
                current_cat = normalize_category(cat_text)
            continue

        if original_stripped.startswith('**') and original_stripped.endswith('**') and len(original_stripped) > 4:
            if articles and current_body_lines:
                articles[-1]['body'] = ' '.join(current_body_lines)
            current_body_lines = []
            title = original_stripped[2:-2].strip()
            if title:
                articles.append({
                    'title': title,
                    'categories': [current_cat] if current_cat else [],
                    'body': '',
                    'source': '',
                    'link': '',
                    'key_points': [],
                    'priority': 100
                })
            continue

        if articles and (original_stripped.startswith('> ') or original_stripped.startswith('>')):
            if '> 💡' in original_stripped:
                insight = original_stripped.split('💡', 1)[1].strip()
            else:
                insight = original_stripped.lstrip('> ').strip()
            if insight:
                articles[-1]['key_points'].append(insight)
            continue

        if '来源:' in original_stripped and articles:
            if current_body_lines:
                articles[-1]['body'] = ' '.join(current_body_lines)
                current_body_lines = []
            source_pairs = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', original_stripped)
            if source_pairs:
                articles[-1]['sources'] = [list(pair) for pair in source_pairs]
                articles[-1]['source'] = source_pairs[0][0]
                articles[-1]['link'] = source_pairs[0][1]
            else:
                source_match = re.search(r'\[([^\]]+)\]', original_stripped)
                if source_match:
                    articles[-1]['source'] = source_match.group(1).strip()
            continue

        if original_stripped and not original_stripped.startswith('#') and '💡' not in original_stripped and '来源:' not in original_stripped and articles:
            if original_stripped.startswith('---') or original_stripped.startswith('*更新时间'):
                continue
            body_text = re.sub(r'^[\-\*•]\s+', '', original_stripped)
            if body_text:
                current_body_lines.append(body_text)
            continue

    if articles and current_body_lines:
        articles[-1]['body'] = ' '.join(current_body_lines)

    return articles, summary_items


# 公司/产品名自动高亮
ENTITY_NAMES = [
    "GlobalFoundries", "Anthropic", "OpenAI", "Google", "Microsoft", "Apple",
    "Amazon", "NVIDIA", "AMD", "Intel", "Qualcomm", "Meta", "ByteDance", "Alibaba",
    "DeepSeek", "Moonshot AI", "Moonshot", "Ant Group", "inclusionAI",
    "SpaceX", "xAI", "Cursor", "Replit", "Perplexity", "Cloudflare", "Vercel", "Modal",
    "PrismML", "NeoCognition",
    "Claude Opus", "Claude Sonnet", "Claude Code", "ChatGPT",
    "Codex", "Claude", "Gemini",
    "GPT-5.4", "GPT-5", "GPT-4",
    "Kimi K2.6", "Kimi",
    "Qwen",
    "SWE-bench", "Claw-Eval", "TerminalBench",
]
ENTITY_NAMES.sort(key=len, reverse=True)
ENTITY_PATTERN = re.compile('(' + '|'.join(re.escape(n) for n in ENTITY_NAMES) + ')')


def highlight_entities(text):
    """高亮公司/产品名，跳过已在 HTML 标签属性内的"""
    parts = re.split(r'(<[^>]+>)', text)
    for i, part in enumerate(parts):
        if not part.startswith('<'):
            parts[i] = ENTITY_PATTERN.sub(r'<span class="ent">\1</span>', part)
    return ''.join(parts)


def convert_bold(text):
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return text


def _truncate(text, max_len=36):
    """截断标题用于侧边栏"""
    if len(text) <= max_len:
        return text
    return text[:max_len].rstrip('，。、；：') + '…'


def generate_html(articles, summary_items, month_day=None, is_latest=True,
                   file_date=None, prev_file=None, next_file=None, raw_md=None):
    """Header + Briefing above, sidebar + content below

    file_date: ISO date string like '2026-03-07' or '2026-03-28+29'
    prev_file: filename stem of previous issue, e.g. '2026-03-06'
    next_file: filename stem of next issue, e.g. '2026-03-08'
    """
    if file_date:
        today_iso = file_date
        # parse display month_day from file_date
        dm = re.match(r'(\d{4})-(\d{2})-(\d{2})', file_date)
        if dm:
            month_day = f"{dm.group(2)}月{dm.group(3)}日"
        elif month_day is None:
            month_day = datetime.now().strftime("%m月%d日")
    else:
        today_iso = datetime.now().strftime("%Y-%m-%d")
        if month_day is None:
            month_day = datetime.now().strftime("%m月%d日")

    today_time = today_iso  # for batch conversion, no time needed

    by_cat = defaultdict(list)
    for a in articles:
        for c in a.get("categories", []):
            by_cat[c].append(a)

    total = len(articles)

    # Top headline (support <!-- headline: ... --> override in md)
    top_headline = "较平静的一天"
    headline_override = None
    if raw_md:
        for line in raw_md.split('\n'):
            if line.strip().startswith('<!-- headline:'):
                headline_override = line.strip()
                headline_override = headline_override.replace('<!-- headline:', '').replace('-->', '').strip()
                break
    if headline_override:
        top_headline = headline_override
    else:
        for cat in CAT_ORDER:
            cat_articles = by_cat.get(cat, [])
            if cat_articles:
                top_headline = cat_articles[0]['title']
                break

    # Prev/next dates — search for actual existing files
    if prev_file is not None or next_file is not None:
        prev_date = prev_file
        next_date = next_file
    else:
        prev_date = next_date = None
        try:
            dt = datetime.strptime(today_iso, "%Y-%m-%d")
            # Search backwards for prev
            for delta in range(1, 11):
                p = (dt - timedelta(days=delta)).strftime("%Y-%m-%d")
                if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                               f"daily-ai-news-{p}.html")):
                    prev_date = p
                    break
            # Search forwards for next
            for delta in range(1, 11):
                n = (dt + timedelta(days=delta)).strftime("%Y-%m-%d")
                if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                               f"daily-ai-news-{n}.html")):
                    next_date = n
                    break
        except ValueError:
            pass

    # Build sidebar nav HTML
    nav_items = ""
    for cat in CAT_ORDER:
        cat_articles = by_cat.get(cat, [])
        if not cat_articles:
            continue
        cls = cat.replace("&", "and").replace(" ", "-")
        nav_items += f"""
        <details class="nav-details" open>
            <summary class="nav-section">
                <span>{cat}</span>
                <span class="nav-count">{len(cat_articles)}</span>
            </summary>
            <div class="nav-articles">"""
        for i, a in enumerate(cat_articles):
            short = _truncate(a['title'])
            nav_items += f"""
                <a href="#c-{cls}-{i}" class="nav-item">{short}</a>"""
        nav_items += """
            </div>
        </details>"""

    # Build mobile TOC
    mobile_toc = ""
    for cat in CAT_ORDER:
        cat_articles = by_cat.get(cat, [])
        if not cat_articles:
            continue
        cls = cat.replace("&", "and").replace(" ", "-")
        mobile_toc += f'<a href="#s-{cls}">{cat}</a>'

    # Build summary — pill/tag style like V1
    summary_html = ""
    if summary_items:
        summary_html = """
            <div class="summary">
                <div class="sum-label">Briefing</div>"""
        for cat in CAT_ORDER:
            items = summary_items.get(cat, [])
            if not items:
                continue
            summary_html += f"""
                <div class="sum-cat">
                    <span class="sum-cat-name">{cat}</span>"""
            for item in items:
                summary_html += f"""
                    <span class="sum-item">{item}</span>"""
            summary_html += """
                </div>"""
        summary_html += """
            </div>"""

    # Build content sections
    sections_html = ""
    for cat in CAT_ORDER:
        cat_articles = by_cat.get(cat, [])
        if not cat_articles:
            continue

        cls = cat.replace("&", "and").replace(" ", "-")

        sections_html += f"""
        <section class="sec" id="s-{cls}">
            <h2 class="sec-h">{cat}</h2>"""

        for i, a in enumerate(cat_articles):
            card_id = f"c-{cls}-{i}"
            title_html = highlight_entities(a['title'])
            body_text = a.get('body', '')
            has_insight = bool(a.get('key_points'))

            sources = a.get('sources', [])
            if sources:
                src_html = ' / '.join(
                    f'<a href="{url}" target="_blank">{name}</a>' for name, url in sources
                )
            elif a.get('link'):
                src_html = f'<a href="{a["link"]}" target="_blank">{a.get("source", "来源")}</a>'
            elif a.get('source'):
                src_html = a["source"]
            else:
                src_html = ''

            sections_html += f"""
        <article class="card" id="{card_id}">
            <h3 class="card-h">{title_html}</h3>"""

            if body_text:
                sections_html += f"""
            <p class="card-body">{highlight_entities(convert_bold(body_text))}</p>"""

            if has_insight:
                for point in a['key_points']:
                    sections_html += f"""
            <div class="card-note"><span class="note-label">Insight by AI</span> {highlight_entities(convert_bold(point))}</div>"""

            if src_html:
                sections_html += f"""
            <div class="card-src">{src_html}</div>"""

            sections_html += """
        </article>"""

        sections_html += """
        </section>"""

    # Bottom nav: prev/next
    issue_nav_html = ""
    if prev_date:
        issue_nav_html += f'<a href="daily-ai-news-{prev_date}.html" class="issue-prev">&larr; 上一期</a>'
    else:
        issue_nav_html += '<span></span>'
    if not is_latest and next_date:
        issue_nav_html += f'\n            <a href="daily-ai-news-{next_date}.html" class="issue-next">下一期 &rarr;</a>'
    else:
        issue_nav_html += '<span></span>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="color-scheme" content="light dark">
    <title>{month_day} AI前沿动态</title>
    <style>
        html {{ scroll-behavior: smooth; }}

        :root {{
            --bg: #ffffff;
            --bg-page: #FAF9F6;
            --text: #1a1a1a;
            --text-2: #444444;
            --text-3: #888888;
            --border: #D9D8D6;
            --note-bg: #f4eff5;
            --pill-bg: #EFEDEA;
            --purple: #660874;
            --purple-80: #843990;
            --purple-60: #a36bac;
            --purple-40: #c29cc8;
            --purple-20: #e8dce9;
            --sidebar-w: 220px;
            --max-w: 740px;
        }}
        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg: #0a0a0a;
                --bg-page: #0a0a0a;
                --text: #e5e5e5;
                --text-2: #aaaaaa;
                --text-3: #666666;
                --border: #1e1e1e;
                --note-bg: #1a111b;
                --pill-bg: #161412;
                --purple: #b87cc4;
                --purple-80: #a06aad;
                --purple-60: #8a5d96;
                --purple-40: #6e3f7a;
                --purple-20: #3d1e45;
            }}
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", "Noto Sans SC", sans-serif;
            background: var(--bg-page);
            color: var(--text);
            line-height: 1.7;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        /* ========== Particle BG ========== */
        #particle-bg {{
            position: fixed; top: 0; left: 0;
            pointer-events: none;
            z-index: 0;
            -webkit-mask-image:
                linear-gradient(to right, black 5%, transparent 25%, transparent 75%, black 95%),
                linear-gradient(to bottom, black 8%, transparent 30%, transparent 70%, black 92%);
            -webkit-mask-composite: source-over;
            mask-image:
                linear-gradient(to right, black 5%, transparent 25%, transparent 75%, black 95%),
                linear-gradient(to bottom, black 8%, transparent 30%, transparent 70%, black 92%);
            mask-composite: add;
        }}

        /* ========== Top Bar ========== */
        .topbar {{
            position: sticky; top: 0; z-index: 100;
            background: var(--bg);
            border-bottom: 1px solid var(--border);
            padding: 0 24px;
            height: 48px;
            display: flex; align-items: center; justify-content: space-between;
        }}
        .topbar-left {{
            display: flex;
            align-items: baseline;
            gap: 10px;
        }}
        .topbar-brand {{
            font-size: 14px;
            font-weight: 700;
            color: var(--purple);
            letter-spacing: -0.3px;
        }}
        .topbar-tagline {{
            font-size: 11px;
            color: var(--text-3);
            letter-spacing: 0.2px;
        }}
        .topbar-right {{
            display: flex;
            gap: 8px;
        }}
        .topbar-btn {{
            font-size: 12px;
            padding: 4px 12px;
            border: 1px solid var(--border);
            border-radius: 3px;
            color: var(--text-3);
            text-decoration: none;
            transition: all 0.15s ease;
        }}
        .topbar-btn:hover {{
            color: var(--text);
            border-color: var(--text-3);
        }}
        .topbar-search {{
            display: flex;
            align-items: center;
            border: 1px solid var(--border);
            border-radius: 3px;
            padding: 0 8px;
            height: 28px;
            margin-right: 4px;
        }}
        .topbar-search input {{
            border: none;
            outline: none;
            background: transparent;
            font-size: 12px;
            color: var(--text);
            width: 100px;
            font-family: inherit;
        }}
        .topbar-search input::placeholder {{
            color: var(--text-3);
        }}
        .topbar-search .search-icon {{
            font-size: 11px;
            color: var(--text-3);
            margin-right: 4px;
        }}

        /* ========== Search Dropdown ========== */
        .search-dropdown {{
            position: fixed;
            top: 52px;
            right: 32px;
            width: 440px;
            max-height: 60vh;
            overflow-y: auto;
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 4px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            display: none;
            z-index: 200;
        }}
        .search-dropdown.active {{ display: block; }}
        .search-empty {{
            padding: 20px 16px;
            font-size: 13px;
            color: var(--text-3);
            text-align: center;
        }}
        .search-result {{
            display: flex;
            align-items: baseline;
            gap: 8px;
            padding: 10px 14px;
            border-bottom: 1px solid var(--border);
            text-decoration: none;
            color: var(--text);
            font-size: 13px;
            line-height: 1.4;
        }}
        .search-result:last-child {{ border-bottom: none; }}
        .search-result:hover {{ background: var(--purple-20); }}
        .search-result-date {{
            font-size: 11px;
            color: var(--text-3);
            flex-shrink: 0;
            font-variant-numeric: tabular-nums;
        }}
        .search-result-title {{
            flex: 1;
            min-width: 0;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .search-result-cat {{
            font-size: 11px;
            color: var(--purple-80);
            flex-shrink: 0;
        }}

        /* ========== Page wrapper ========== */
        .page {{
            max-width: calc(var(--max-w) + var(--sidebar-w) + 80px);
            margin: 0 auto;
            padding: 0 32px;
        }}

        /* --- Header (above layout) --- */
        .header {{
            padding: 28px 0 24px;
            border-bottom: 1px solid var(--border);
        }}
        .header-date {{
            font-size: 12px;
            color: var(--text-3);
            font-variant-numeric: tabular-nums;
            margin-bottom: 8px;
        }}
        .header h1 {{
            font-size: 24px;
            font-weight: 700;
            letter-spacing: -0.3px;
            line-height: 1.4;
            color: var(--text);
        }}
        .header-sub {{
            margin-top: 8px;
            font-size: 13px;
            color: var(--text-3);
        }}

        /* --- Summary / Briefing (above layout) --- */
        .summary {{
            padding: 20px 0 24px;
            border-bottom: 1px solid var(--border);
        }}
        .sum-label {{
            font-size: 11px;
            font-weight: 600;
            color: var(--purple);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 14px;
        }}
        .sum-cat {{
            display: flex;
            flex-wrap: wrap;
            align-items: flex-start;
            gap: 6px;
            margin-bottom: 10px;
        }}
        .sum-cat:last-child {{
            margin-bottom: 0;
        }}
        .sum-cat-name {{
            display: inline-block;
            background: var(--purple-20);
            color: var(--purple);
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 12px;
            font-weight: 600;
            flex-shrink: 0;
        }}
        .sum-item {{
            background: var(--pill-bg);
            padding: 3px 10px;
            border-radius: 3px;
            font-size: 13px;
            color: var(--text-2);
            line-height: 1.5;
        }}

        /* ========== Layout (sidebar + content) ========== */
        .layout {{
            display: flex;
        }}

        /* ========== Sidebar ========== */
        .sidebar {{
            width: var(--sidebar-w);
            flex-shrink: 0;
            padding: 20px 16px 20px 0;
            position: sticky;
            top: 48px;
            height: calc(100vh - 48px);
            overflow-y: auto;
            border-right: 1px solid var(--border);
        }}
        .sidebar::-webkit-scrollbar {{ width: 0; }}

        .nav-label {{
            font-size: 10px;
            font-weight: 600;
            color: var(--text-3);
            text-transform: uppercase;
            letter-spacing: 1px;
            padding-bottom: 16px;
        }}

        .nav-details {{
            margin-bottom: 2px;
        }}
        .nav-details summary {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 6px 0;
            font-size: 11px;
            font-weight: 600;
            color: var(--text);
            cursor: pointer;
            list-style: none;
            user-select: none;
        }}
        .nav-details summary::-webkit-details-marker {{ display: none; }}
        .nav-details summary::before {{
            content: "\\25BE";
            font-size: 9px;
            color: var(--text-3);
            margin-right: 5px;
            display: inline-block;
            transition: transform 0.15s ease;
        }}
        .nav-details:not([open]) summary::before {{
            transform: rotate(-90deg);
        }}
        .nav-count {{
            font-size: 10px;
            color: var(--text-3);
            font-variant-numeric: tabular-nums;
            margin-left: auto;
            padding-left: 4px;
        }}

        .nav-articles {{
            padding-left: 14px;
            border-left: 1px solid var(--border);
            margin: 2px 0 12px;
        }}
        .nav-item {{
            display: block;
            padding: 3px 8px;
            font-size: 12px;
            color: var(--text-3);
            text-decoration: none;
            line-height: 1.45;
            transition: color 0.15s ease;
        }}
        .nav-item:hover {{
            color: var(--text-2);
        }}
        .nav-item.active {{
            color: var(--purple);
            font-weight: 500;
        }}

        /* ========== Main ========== */
        .main {{
            flex: 1;
            max-width: var(--max-w);
            padding: 20px 0 0 24px;
            min-width: 0;
        }}

        /* --- Section --- */
        .sec {{
            margin-bottom: 32px;
            scroll-margin-top: 64px;
        }}
        .sec-h {{
            font-size: 11px;
            font-weight: 600;
            color: var(--purple);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 16px;
        }}

        /* --- Card --- */
        .card {{
            padding: 16px 0;
            border-bottom: 1px solid var(--border);
            scroll-margin-top: 64px;
            cursor: default;
        }}
        .card:last-child {{ border-bottom: none; }}
        .card-h {{
            font-size: 16px;
            font-weight: 600;
            line-height: 1.5;
            color: var(--text);
            letter-spacing: -0.2px;
            margin-bottom: 8px;
        }}

        .ent {{
            font-weight: 500;
        }}

        .card-body {{
            font-size: 14px;
            line-height: 1.75;
            color: var(--text-2);
        }}
        .card-body strong {{
            color: var(--text);
            font-weight: 600;
        }}

        .card-note {{
            margin-top: 10px;
            padding: 10px 14px;
            background: var(--note-bg);
            font-size: 13px;
            line-height: 1.75;
            color: var(--text-2);
            border-radius: 2px;
        }}
        .note-label {{
            font-size: 10px;
            font-weight: 600;
            color: var(--purple-80);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-right: 6px;
        }}

        .card-src {{
            margin-top: 10px;
            font-size: 12px;
            color: var(--text-3);
        }}
        .card-src a {{
            color: var(--text-3);
            text-decoration: none;
        }}
        .card-src a:hover {{
            color: var(--text);
        }}

        /* ========== Bottom (independent) ========== */
        .bottom {{
            border-top: 1px solid var(--border);
            margin-top: 16px;
            padding: 20px 0 32px;
        }}

        /* --- Issue Navigation --- */
        .issue-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
        }}
        .issue-nav a {{
            font-size: 13px;
            padding: 6px 16px;
            border: 1px solid var(--border);
            border-radius: 3px;
            color: var(--text-3);
            text-decoration: none;
            transition: all 0.15s ease;
        }}
        .issue-nav a:hover {{
            color: var(--text);
            border-color: var(--text-3);
        }}

        /* --- Footer --- */
        .footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid var(--border);
            padding-top: 16px;
        }}
        .footer-copy {{
            font-size: 12px;
            color: var(--text-3);
        }}
        .footer-top {{
            font-size: 12px;
            color: var(--text-3);
            text-decoration: none;
            padding: 4px 12px;
            border: 1px solid var(--border);
            border-radius: 3px;
            transition: all 0.15s ease;
        }}
        .footer-top:hover {{
            color: var(--text);
            border-color: var(--text-3);
        }}

        /* ========== Mobile TOC ========== */
        .mob-toc {{
            display: none;
            overflow-x: auto;
            gap: 0;
            padding: 0 16px;
            background: var(--bg);
            border-bottom: 1px solid var(--border);
            position: sticky; top: 48px; z-index: 50;
            height: 40px;
            align-items: center;
        }}
        .mob-toc::-webkit-scrollbar {{ display: none; }}
        .mob-toc a {{
            flex-shrink: 0;
            padding: 8px 12px;
            font-size: 12px;
            font-weight: 500;
            text-decoration: none;
            color: var(--text-3);
            white-space: nowrap;
        }}
        .mob-toc a:hover {{ color: var(--text); }}

        /* ========== Responsive ========== */
        @media (max-width: 768px) {{
            .sidebar {{ display: none; }}
            .mob-toc {{ display: flex !important; }}
            .main {{
                max-width: 100%;
                padding: 24px 20px 48px;
            }}
            .header {{ padding: 20px 0 16px; }}
            .header h1 {{ font-size: 20px; }}
        }}
        @media (max-width: 480px) {{
            .main {{ padding: 20px 16px 40px; }}
            .header {{ padding: 16px 0 12px; }}
            .header h1 {{ font-size: 18px; }}
            .card-h {{ font-size: 15px; }}
            .topbar-tagline {{ display: none; }}
            .topbar-search {{ display: none; }}
            .search-dropdown {{ display: none !important; }}
        }}
    </style>
</head>
<body>
    <canvas id="particle-bg"></canvas>
    <!-- Top bar -->
    <div class="topbar">
        <div class="topbar-left">
            <span class="topbar-brand">AI Daily News</span>
            <span class="topbar-tagline">Keep Informed with Link-X Capital</span>
        </div>
        <div class="topbar-right">
            <div class="topbar-search">
                <span class="search-icon">&#128269;</span>
                <input type="text" id="search" placeholder="搜索新闻..." autocomplete="off">
            </div>
            <a href="index.html" class="topbar-btn">往期动态</a>
            <a href="topics.html" class="topbar-btn">专题报告</a>
        </div>
    </div>

    <div class="search-dropdown" id="search-dropdown"></div>

    <!-- Mobile TOC -->
    <div class="mob-toc" id="mob-toc">
        {mobile_toc}
    </div>

    <!-- Page wrapper: header + briefing above, sidebar + content below -->
    <div class="page">
        <header class="header">
            <div class="header-date">{today_iso}</div>
            <h1>{top_headline}</h1>
            <div class="header-sub">{total} stories, 24h window</div>
        </header>

        {summary_html}

        <div class="layout">
            <!-- Sidebar -->
            <nav class="sidebar">
                <div class="nav-label">Contents</div>
                {nav_items}
            </nav>

            <!-- Main content -->
            <div class="main">
                {sections_html}
            </div>
        </div>

        <!-- Bottom: independent of layout -->
        <div class="bottom">
            <div class="issue-nav">
                {issue_nav_html}
            </div>
            <div class="footer">
                <span class="footer-copy">&copy; 2026 &middot; AI Daily News by Link-X Capital</span>
                <a href="#" class="footer-top">Back to top &uarr;</a>
            </div>
        </div>
    </div>

    <!-- Scroll spy -->
    <script>
    (function() {{
        const cards = document.querySelectorAll('.card[id]');
        const navs = document.querySelectorAll('.nav-item[href^="#c-"]');
        if (!cards.length || !navs.length) return;
        const obs = new IntersectionObserver(entries => {{
            entries.forEach(e => {{
                if (e.isIntersecting) {{
                    navs.forEach(n => n.classList.remove('active'));
                    const hit = document.querySelector('.nav-item[href="#' + e.target.id + '"]');
                    if (hit) hit.classList.add('active');
                }}
            }});
        }}, {{ rootMargin: '-80px 0px -65% 0px' }});
        cards.forEach(c => obs.observe(c));
    }})();

    // Search — real-time, fetches HTML pages in browser
    (function() {{
        const input = document.getElementById('search');
        const dropdown = document.getElementById('search-dropdown');
        if (!input || !dropdown) return;

        const cards = document.querySelectorAll('.card');
        const sections = document.querySelectorAll('.sec[id]');
        const details = document.querySelectorAll('.nav-details');

        let searchData = [];
        let totalFiles = 0, loadedCount = 0, started = false;

        function stripTag(s) {{ return s.replace(/<[^>]+>/g, ''); }}

        function parseHtml(html, url) {{
            const dm = url.match(/(\d{{4}})-(\d{{2}})-(\d{{2}})/);
            const date = dm ? dm[2] + '-' + dm[3] : '';
            let articles = [], currentCat = '';
            const parts = html.split(/<h2 class="sec-h"[^>]*>(.*?)<\/h2>/);
            for (let i = 0; i < parts.length; i++) {{
                if (i % 2 === 1) currentCat = stripTag(parts[i]).trim();
                else if (i > 0 && currentCat) {{
                    const tRe = /<h3 class="card-h"[^>]*>(.*?)<\/h3>/g, bRe = /<p class="card-body">(.*?)<\/p>/g;
                    const ts = [], bs = [];
                    let m;
                    while ((m = tRe.exec(parts[i])) !== null) ts.push(m[1]);
                    while ((m = bRe.exec(parts[i])) !== null) bs.push(m[1]);
                    for (let j = 0; j < ts.length; j++) {{
                        const t = stripTag(ts[j]).trim();
                        const b = j < bs.length ? stripTag(bs[j]).trim().slice(0, 120) : '';
                        if (t) articles.push({{ d: date, t, b, c: currentCat, f: url }});
                    }}
                }}
            }}
            return articles;
        }}

        function startLoad() {{
            if (started) return;
            started = true;
            // Fetch index.html to get the file list
            fetch('index.html').then(r => r.text()).then(html => {{
                const re = /href="(daily-ai-news-20\d{{2}}-[^"]+\.html)"/g;
                const files = []; let m;
                while ((m = re.exec(html)) !== null) files.push(m[1]);
                totalFiles = files.length;
                files.forEach(url => {{
                    fetch(url).then(r => r.text()).then(h => {{
                        searchData = searchData.concat(parseHtml(h, url));
                        loadedCount++;
                    }}).catch(() => {{ loadedCount++; }});
                }});
            }}).catch(() => {{}});
        }}

        input.addEventListener('focus', startLoad);

        input.addEventListener('input', function() {{
            const q = this.value.toLowerCase().trim();

            if (!q) {{
                cards.forEach(c => c.style.display = '');
                sections.forEach(s => s.style.display = '');
                details.forEach(d => d.style.display = '');
                dropdown.classList.remove('active');
                return;
            }}

            // In-page filter
            cards.forEach(card => {{
                card.style.display = card.textContent.toLowerCase().includes(q) ? '' : 'none';
            }});
            sections.forEach(sec => {{
                const vis = sec.querySelectorAll('.card:not([style*="none"])');
                sec.style.display = vis.length ? '' : 'none';
            }});
            details.forEach(det => {{
                const link = det.querySelector('.nav-item');
                if (!link) return;
                const sec = document.querySelector(link.getAttribute('href'));
                det.style.display = (sec && sec.style.display !== 'none') ? '' : 'none';
            }});

            // Cross-archive dropdown
            if (!searchData.length) {{
                if (started) {{
                    dropdown.innerHTML = '<div class="search-empty">正在加载 (' + loadedCount + '/' + totalFiles + ')...</div>';
                    dropdown.classList.add('active');
                }}
                return;
            }}
            const results = searchData.filter(item =>
                item.t.toLowerCase().includes(q) || item.b.toLowerCase().includes(q)
            ).slice(0, 15);

            if (!results.length) {{
                dropdown.innerHTML = '<div class="search-empty">无匹配结果</div>';
            }} else {{
                dropdown.innerHTML = results.map(r =>
                    '<a href="' + r.f + '" class="search-result">' +
                    '<span class="search-result-date">' + r.d + '</span>' +
                    '<span class="search-result-title">' + r.t + '</span>' +
                    '<span class="search-result-cat">' + r.c + '</span>' +
                    '</a>'
                ).join('');
            }}
            dropdown.classList.add('active');
        }});

        document.addEventListener('click', function(e) {{
            if (!e.target.closest('.topbar-search') && !e.target.closest('.search-dropdown')) {{
                dropdown.classList.remove('active');
            }}
        }});
        input.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape') {{ dropdown.classList.remove('active'); input.blur(); }}
        }});
    }})();

    // Diamond-frame particle network with ripple energy
    (function() {{
        const canvas = document.getElementById('particle-bg');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

        const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const rgb = isDark ? '184,124,196' : '102,8,116';

        let W, H;
        const MAX_D = 160, RIPPLE_SPEED = 80, RIPPLE_LIFE = 3.5;
        let nodes = [], ripples = [];

        function resize() {{
            W = canvas.width = window.innerWidth;
            H = canvas.height = window.innerHeight;
            // Diamond frame distribution
            const cx = W / 2, cy = H / 2;
            const dw = W * 0.42, dh = H * 0.42;
            const dEdges = [
                [cx, cy - dh, cx + dw, cy],
                [cx + dw, cy, cx, cy + dh],
                [cx, cy + dh, cx - dw, cy],
                [cx - dw, cy, cx, cy - dh]
            ];
            const count = Math.max(20, Math.round(50 * (W * H) / (1600 * 900)));
            nodes = [];
            for (let i = 0; i < count; i++) {{
                let x, y;
                if (Math.random() < 0.80) {{
                    const ei = Math.random() * 4 | 0;
                    const t = Math.random();
                    const e = dEdges[ei];
                    x = e[0] + (e[2] - e[0]) * t + (Math.random() - 0.5) * 20;
                    y = e[1] + (e[3] - e[1]) * t + (Math.random() - 0.5) * 20;
                }} else {{
                    x = Math.random() * W;
                    y = Math.random() * H;
                }}
                nodes.push({{
                    x, y,
                    vx: (Math.random() - 0.5) * 0.25,
                    vy: (Math.random() - 0.5) * 0.20,
                    r: 1.2 + Math.random() * 1.8,
                    energy: 0
                }});
            }}
            ripples = [];
        }}

        let t0 = performance.now(), lastF = 0, fc = 0;

        function loop(now) {{
            requestAnimationFrame(loop);
            if (now - lastF < 16.67) return;
            lastF = now;
            const t = (now - t0) / 1000;
            fc++;

            // Spawn ripple every ~2s
            if (fc % 120 === 0 && nodes.length) {{
                const s = nodes[Math.random() * nodes.length | 0];
                ripples.push({{ x: s.x, y: s.y, born: t }});
            }}
            for (let i = ripples.length - 1; i >= 0; i--) {{
                if (t - ripples[i].born > RIPPLE_LIFE) ripples.splice(i, 1);
            }}

            // Move & energy
            for (const n of nodes) {{
                n.x += n.vx; n.y += n.vy;
                if (n.x < 0 || n.x > W) n.vx *= -1;
                if (n.y < 0 || n.y > H) n.vy *= -1;
                n.energy *= 0.94;
                for (const r of ripples) {{
                    const dx = n.x - r.x, dy = n.y - r.y;
                    const dist = Math.sqrt(dx*dx + dy*dy);
                    const ringR = RIPPLE_SPEED * (t - r.born);
                    if (Math.abs(dist - ringR) < 18) n.energy = Math.min(1, n.energy + 0.5);
                }}
            }}

            ctx.clearRect(0, 0, W, H);

            // Ripple rings
            for (const r of ripples) {{
                const age = t - r.born;
                const radius = RIPPLE_SPEED * age;
                const alpha = 0.12 * Math.max(0, 1 - age / RIPPLE_LIFE);
                ctx.strokeStyle = 'rgba(' + rgb + ',' + alpha + ')';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.arc(r.x, r.y, radius, 0, Math.PI * 2);
                ctx.stroke();
            }}

            // Connections
            for (let i = 0; i < nodes.length; i++) {{
                for (let j = i + 1; j < nodes.length; j++) {{
                    const a = nodes[i], b = nodes[j];
                    const dx = a.x - b.x, dy = a.y - b.y;
                    const d = Math.sqrt(dx*dx + dy*dy);
                    if (d > MAX_D) continue;
                    const distA = 1 - d / MAX_D;
                    const maxE = Math.max(a.energy, b.energy);
                    const alpha = distA * (0.08 + 0.22 * maxE);
                    ctx.strokeStyle = 'rgba(' + rgb + ',' + alpha + ')';
                    ctx.lineWidth = 0.6;
                    ctx.beginPath();
                    ctx.moveTo(a.x, a.y);
                    ctx.lineTo(b.x, b.y);
                    ctx.stroke();
                }}
            }}

            // Nodes (dots)
            for (const n of nodes) {{
                const alpha = 0.22 + 0.40 * n.energy;
                const r = n.r + n.energy * 1.5;
                ctx.fillStyle = 'rgba(' + rgb + ',' + alpha + ')';
                ctx.beginPath();
                ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
                ctx.fill();
            }}
        }}

        resize();
        window.addEventListener('resize', resize);
        requestAnimationFrame(loop);
    }})();
    </script>
</body>
</html>"""

    return html


def _update_index_html(today_date_str, articles):
    """在 index.html 中插入今天的条目（如果不存在），并移动'最新'标签。
    同时更新侧边栏导航链接和 nav-count。"""
    import re
    from datetime import datetime

    index_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    if not os.path.exists(index_path):
        return

    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 从日期算月份和日
    dt = datetime.strptime(today_date_str, "%Y-%m-%d")
    month_key = dt.strftime("%b").lower()  # apr
    day_num = dt.day
    month_label = dt.strftime("%b")       # Apr
    month_body_id = f"month-{month_key}"

    # 构建摘要：从 articles 取前5条标题，格式：<strong>主体</strong>做了什么
    summary_parts = []
    for a in articles[:5]:
        title = a.get('title', '')
        # 尝试在标题中找到冒号或逗号作为主体/描述的分界
        sep_pos = len(title)
        for sep_char in ['：', ':', '，']:
            pos = title.find(sep_char)
            if pos > 0 and pos < sep_pos:
                sep_pos = pos
        if sep_pos < len(title):
            entity = title[:sep_pos]
            desc = title[sep_pos+1:].strip()[:40]
            summary_parts.append(f"<strong>{entity}</strong>{desc}")
        else:
            summary_parts.append(f"<strong>{title[:15]}</strong>{title[15:40]}")
    summary_text = "；".join(summary_parts)
    count = len(articles)

    # 新条目 HTML
    new_entry = (
        f'        <a href="daily-ai-news-{today_date_str}.html" class="timeline-entry" id="{month_key}-{day_num}">\n'
        f'            <div class="te-date">{month_label} {day_num} <span class="te-badge">最新</span></div>\n'
        f'            <div class="te-summary">{summary_text}</div>\n'
        f'            <div class="te-count">{count} 条动态</div>\n'
        f'        </a>\n'
    )

    # 移除旧的"最新"标签
    html = html.replace(' <span class="te-badge">最新</span>', '')

    # 检查今天的条目是否已存在：存在则替换，不存在则插入
    entry_id = f'{month_key}-{day_num}'
    existing_pattern = rf'        <a href="daily-ai-news-{today_date_str}\.html" class="timeline-entry" id="{entry_id}">.*?</a>\n'
    match = re.search(existing_pattern, html, re.DOTALL)

    if match:
        # 替换已有条目
        html = html[:match.start()] + new_entry + html[match.end():]
        print(f"Replaced existing entry for {today_date_str}")
    else:
        # 在对应月份的 month-body 开头插入
        month_start = html.find(f'id="{month_body_id}"')
        if month_start == -1:
            print(f"Warning: month body '{month_body_id}' not found in index.html")
            return

        # 找到 month-body div 后面的 >
        insert_pos = html.find('>', month_start) + 1
        html = html[:insert_pos] + '\n' + new_entry + html[insert_pos:]

    # --- 更新侧边栏导航链接 ---
    nav_link_id = f'#{month_key}-{day_num}'
    nav_link_text = f'{month_label} {day_num:02d}'
    new_nav_link = f'                    <a href="{nav_link_id}" class="nav-item">{nav_link_text}</a>'

    if f'href="{nav_link_id}"' not in html:
        # 找到对应月份的 nav-details 中的 nav-articles div
        month_cn = f"{dt.year} 年 {dt.month} 月"
        nav_section_pattern = rf'<summary><span>{month_cn}</span><span class="nav-count">\d+</span></summary>\s*<div class="nav-articles">'
        nav_match = re.search(nav_section_pattern, html)
        if nav_match:
            # 找到正确的插入位置（按日期降序）
            nav_start = nav_match.end()
            # 找到该 nav-articles 的结束 </div>
            nav_end = html.find('</div>', nav_start)
            nav_block = html[nav_start:nav_end]
            # 提取已有的日期链接
            existing_days = re.findall(rf'href="#{month_key}-(\d+)"', nav_block)
            existing_days_int = [int(d) for d in existing_days]

            # 找到第一个比当前日期小的位置，在其前面插入
            insert_pos = nav_start  # 默认插入到开头
            for i, existing_day in enumerate(existing_days_int):
                if existing_day < day_num:
                    # 找到这个链接在 html 中的位置
                    link_pattern = rf'<a href="#{month_key}-{existing_day}" class="nav-item">'
                    link_match = re.search(link_pattern, html[nav_start:nav_end])
                    if link_match:
                        insert_pos = nav_start + link_match.start()
                    break
            else:
                # 所有已有日期都比当前大，插入到末尾
                insert_pos = nav_end

            # 插入时确保换行
            if insert_pos == nav_start or insert_pos == nav_end:
                html = html[:insert_pos] + '\n' + new_nav_link + html[insert_pos:]
            else:
                html = html[:insert_pos] + new_nav_link + '\n' + html[insert_pos:]
            print(f"Added sidebar nav link for {nav_link_text}")

    # --- 更新 nav-count ---
    # 统计该月份实际的 timeline-entry 数量
    month_entries = re.findall(rf'id="{month_key}-\d+"', html)
    actual_count = len(month_entries)
    month_cn = f"{dt.year} 年 {dt.month} 月"
    count_pattern = rf'(<summary><span>{month_cn}</span><span class="nav-count">)\d+(</span></summary>)'
    html = re.sub(count_pattern, rf'\g<1>{actual_count}\g<2>', html)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated index.html with {today_date_str} (nav-count: {actual_count})")



def _find_prev_file(today_date_str):
    """Find the actual previous daily HTML file (handles gaps and combined dates)."""
    base = os.path.dirname(os.path.abspath(__file__))
    try:
        dt = datetime.strptime(today_date_str, "%Y-%m-%d")
    except ValueError:
        return None, None

    # Search backwards up to 10 days for the previous file
    for delta in range(1, 11):
        prev_dt = dt - timedelta(days=delta)
        prev_date = prev_dt.strftime("%Y-%m-%d")
        prev_path = os.path.join(base, f"daily-ai-news-{prev_date}.html")
        if os.path.exists(prev_path):
            return prev_date, prev_path
        # Check combined date format (e.g., 2026-03-28+29, 2026-04-05+06)
        import glob
        combined = glob.glob(os.path.join(base, f"daily-ai-news-{prev_date}+*.html"))
        if combined:
            basename = os.path.basename(combined[0])
            date_part = basename.replace('daily-ai-news-', '').replace('.html', '')
            return date_part, combined[0]
    return None, None


def _patch_prev_day_next_link(today_date_str):
    """Patch previous file's HTML to add 'next' link pointing to today.
    Handles non-consecutive dates by searching for the actual previous file."""
    import re as _re

    prev_date, prev_path = _find_prev_file(today_date_str)
    if not prev_path:
        return

    with open(prev_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace empty <span></span> after 上一期 with next link
    next_link = f'<a href="daily-ai-news-{today_date_str}.html" class="issue-next">下一期 &rarr;</a>'
    # Match any 上一期 link followed by empty <span></span>
    old_pattern = r'class="issue-prev">&larr; 上一期</a>\s*<span></span>'
    new_pattern = f'class="issue-prev">&larr; 上一期</a>\\n                {next_link}'
    if _re.search(old_pattern, html):
        html = _re.sub(old_pattern, new_pattern, html)
        with open(prev_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Patched prev-next in: daily-ai-news-{prev_date}.html")


def md_to_html(md_file, output_html=None, dated_html=None):
    """从 MD 文件生成 HTML

    Args:
        md_file: 输入 MD 文件路径
        output_html: 主 HTML 输出路径 (如 daily-ai-news.html)
        dated_html: 日期归档 HTML 输出路径 (如 daily-ai-news-2026-04-24.html)
    """
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    articles, summary_items = parse_md(md_content)
    date_str = datetime.now().strftime("%Y-%m-%d")
    html = generate_html(articles, summary_items, is_latest=True, file_date=date_str, raw_md=md_content)

    if output_html is None:
        output_html = md_file.replace('.md', '-v2.html')

    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"V2 generated: {output_html}")

    # Generate dated archive HTML
    if dated_html:
        with open(dated_html, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Dated HTML generated: {dated_html}")
        _patch_prev_day_next_link(date_str)

    return articles


if __name__ == "__main__":
    BASE_DIR = "/Users/shenyalan/ai-daily-news"
    today = os.environ.get("NEWS_DATE") or datetime.now().strftime('%Y-%m-%d')
    MD_FILE = os.path.join(BASE_DIR, f"daily-ai-news-{today}.md")
    DATED = os.path.join(BASE_DIR, f"daily-ai-news-{today}.html")

    articles = md_to_html(MD_FILE, output_html=DATED, dated_html=DATED)
    _update_index_html(today, articles)
    print(f"Parsed {len(articles)} articles")
