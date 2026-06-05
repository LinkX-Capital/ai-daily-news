#!/usr/bin/env python3
"""
bilingual_html.py — 从中文 HTML 生成双语版本（MiniMax 翻译 + 中英切换按钮）

用法:
    python bilingual_html.py 2026-06-03
    python bilingual_html.py              # 自动取今天日期

流程:
    读取中文 HTML → 提取文本 → MiniMax 翻译 → 注入切换按钮 + JS → 覆写 HTML
"""

import os, sys, re, json, time, glob, httpx, asyncio
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
API_KEY = os.environ.get("MINIMAX_API_KEY", "")
API_URL = "https://api.minimaxi.com/anthropic/v1/messages"
CACHE_PATH = os.path.join(BASE, '.bilingual_cache.json')

# ── Helpers ───────────────────────────────────────────────

def strip_html(s):
    return re.sub(r'<[^>]+>', '', s).strip()

def has_chinese(s):
    return any('\u4e00' <= c <= '\u9fff' for c in s)

# ── MiniMax API ───────────────────────────────────────────

def _build_prompt(chunk):
    return (
        'Translate the following Chinese texts to English.\n'
        'Return ONLY a JSON object mapping each Chinese text to its English translation.\n'
        'Example format: {"模型前沿": "Model Frontier", "OpenAI发布": "OpenAI Releases"}\n'
        'Rules: Keep company/product/person names, technical terms, numbers, and units unchanged. '
        'Be concise and professional.\n\n'
        + json.dumps(chunk, ensure_ascii=False)
    )

SYSTEM_PROMPT = (
    "You are a professional Chinese-to-English translator specializing in AI and tech news. "
    "Translate accurately and concisely. Preserve all company names, product names, person names, "
    "technical terms, numbers, and units unchanged. Do not add explanations."
)

def call_minimax_sync(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01"
    }
    data = {
        "model": "MiniMax-M2.7",
        "temperature": 0.2,
        "max_tokens": 16000,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}]
    }
    for attempt in range(3):
        try:
            r = httpx.post(API_URL, headers=headers, json=data, timeout=180, verify=False)
            r.raise_for_status()
            result = r.json()
            for item in result.get("content", []):
                if item.get("type") == "text":
                    return item["text"]
        except Exception as e:
            if attempt < 2: time.sleep(2 ** attempt)
    return None

async def call_minimax_async(client, prompt, sem, chunk_id=None):
    async with sem:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        data = {
            "model": "MiniMax-M2.7",
            "temperature": 0.2,
            "max_tokens": 16000,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": prompt}]
        }
        for attempt in range(3):
            try:
                r = await client.post(API_URL, headers=headers, json=data, timeout=180)
                r.raise_for_status()
                result = r.json()
                for item in result.get("content", []):
                    if item.get("type") == "text":
                        return item["text"]
            except Exception as e:
                print(f"  ⚠️ {chunk_id} attempt {attempt+1}/3: {type(e).__name__}: {str(e)[:100]}", flush=True)
                if attempt < 2: await asyncio.sleep(2 ** attempt)
        return None

def _parse_response(resp):
    """Parse API response. Handles both array and dict formats, strips markdown fences."""
    if not resp: return {}
    # Strip markdown code fences
    cleaned = re.sub(r'```(?:json)?\s*', '', resp).strip()
    # Try array format first
    am = re.search(r'\[.*\]', cleaned, re.DOTALL)
    if am:
        try:
            pairs = json.loads(am.group(0))
            return {p['zh']: p['en'] for p in pairs if 'zh' in p and 'en' in p}
        except (json.JSONDecodeError, TypeError):
            pass
    # Try dict format {"zh1": "en1", "zh2": "en2"}
    dm = re.search(r'\{.*\}', cleaned, re.DOTALL)
    if dm:
        try:
            d = json.loads(dm.group(0))
            return d
        except (json.JSONDecodeError, TypeError):
            pass
    return {}

# ── Extraction (order must match JS selectors) ────────────

def extract_texts(html):
    """Extract all translatable Chinese texts in document order."""
    texts = []

    # 1. h1 — page title
    for m in re.finditer(r'<h1>(.*?)</h1>', html, re.DOTALL):
        texts.append(strip_html(m.group(1)))

    # 2. .sec-h — section headers
    for m in re.finditer(r'<h2 class="sec-h">(.*?)</h2>', html):
        texts.append(m.group(1).strip())

    # 3. .card-h — article titles
    for m in re.finditer(r'<h3 class="card-h"[^>]*>(.*?)</h3>', html, re.DOTALL):
        texts.append(strip_html(m.group(1)))

    # 4. .card-body — article bodies
    for m in re.finditer(r'<p class="card-body">(.*?)</p>', html, re.DOTALL):
        texts.append(strip_html(m.group(1)))

    # 5. .card-note — insights (strip note-label span)
    for m in re.finditer(r'<div class="card-note">(.*?)</div>', html, re.DOTALL):
        inner = re.sub(r'<span class="note-label">.*?</span>', '', m.group(1))
        t = strip_html(inner).strip()
        if t:
            texts.append(t)

    # 6. .sum-cat-name
    for m in re.finditer(r'<span class="sum-cat-name">(.*?)</span>', html):
        texts.append(m.group(1).strip())

    # 7. .sum-item
    for m in re.finditer(r'<span class="sum-item">(.*?)</span>', html):
        texts.append(strip_html(m.group(1)))

    # 8. sidebar section names (first span inside summary.nav-section)
    for m in re.finditer(r'<summary class="nav-section">\s*<span>(.*?)</span>', html):
        texts.append(m.group(1).strip())

    # 9. .nav-item
    for m in re.finditer(r'<a[^>]*class="nav-item"[^>]*>(.*?)</a>', html):
        texts.append(strip_html(m.group(1)))

    # 10. .mob-toc a
    toc = re.search(r'<div class="mob-toc"[^>]*>(.*?)</div>', html, re.DOTALL)
    if toc:
        for m in re.finditer(r'<a[^>]*>(.*?)</a>', toc.group(1)):
            texts.append(m.group(1).strip())

    # 11. .issue-prev
    for m in re.finditer(r'<a[^>]*class="issue-prev"[^>]*>(.*?)</a>', html):
        texts.append(strip_html(m.group(1)))

    # 12. .topbar-btn
    for m in re.finditer(r'<a[^>]*class="topbar-btn"[^>]*>(.*?)</a>', html):
        texts.append(strip_html(m.group(1)))

    return texts

# ── Generic extraction for non-daily pages ────────────────
# Selectors for text elements common across all pages.
# NOTE: the JS in build_toggle_js_generic() must use a matching list.
GENERIC_SELECTORS = [
    # Plain tags
    'h1', 'h2', 'h3', 'h4', 'p', 'li',
    # Topbar
    'a.topbar-btn', 'a.topbar-nav', 'span.topbar-brand', 'span.topbar-tagline',
    # Hero
    'div.hero-eyebrow', 'h1.hero-title', 'p.hero-sub', 'div.hero-meta', 'div.hero-date',
    'div.hero-stat-num', 'div.hero-stat-label',
    # Section headers
    'div.section-label', 'div.sec-title', 'span.sec-title', 'span.sec-num',
    # Edition cards (topic-frontier-models.html)
    'div.edition-title', 'div.edition-sub',
    'div.edition-date-label', 'div.edition-date-val', 'div.edition-date-month',
    'span.model-chip', 'span.edition-tag',
    # Topic cards (topics.html)
    'div.topic-title', 'div.topic-desc',
    'span.topic-meta-item', 'span.topic-badge', 'span.edition-chip',
    # Special list (index.html)
    'div.sp-title', 'div.sp-desc',
    # Timeline (index.html)
    'div.te-date', 'div.te-summary', 'div.te-count',
    # Cards (frontier-models-2026-05-26.html)
    'div.card-title', 'div.card-sub', 'div.card-body', 'div.card-tag',
    'div.mini-stat-val', 'div.mini-stat-label',
    # Stats / sub-sections (Google-IO-2026-Deep-Research.html)
    'div.sub-title',
    'div.stat-item', 'div.stat-val', 'div.stat-label',
    'div.info-card',
    # Summary cards (summary.html)
    'span.cat-tag', 'div.source',
    # TOC
    'div.toc-title', 'div.toc-sub',
    'span.nav-item', 'a.nav-item',
]

# Compound CSS selectors the JS evaluates (no corresponding regex extractor;
# the JS uses textContent-based lookup, so no extraction is needed).
GENERIC_SELECTORS_JS_ONLY = [
    'details.nav-details > summary > span:not(.nav-count)',
]

def extract_texts_generic(html):
    """For non-daily pages: extract Chinese text from common text elements."""
    import re as _re
    texts = []

    for sel in GENERIC_SELECTORS:
        if '.' in sel:
            tag, cls = sel.split('.', 1)
            pat = rf'<{tag}\s+class="{cls}"[^>]*>(.*?)</{tag}>'
        else:
            pat = rf'<{sel}[^>]*>(.*?)</{sel}>'

        for m in _re.finditer(pat, html, _re.DOTALL):
            text = strip_html(m.group(1))
            if has_chinese(text):
                texts.append(text)

    # Special: <details><summary><span>专题报告</span><span class="nav-count">3</span></summary>
    # — extract the first span text inside summary (for index.html nav).
    for m in _re.finditer(
        r'<details[^>]*>\s*<summary>\s*<span>([^<]+)</span>',
        html):
        text = m.group(1).strip()
        if has_chinese(text):
            texts.append(text)

    return texts

# ── Generic injection for non-daily pages ──────────────────

def build_toggle_js_generic(en_map, ph_en):
    """JS that iterates all [data-i18n] elements and swaps text."""
    # Combine the regex-derived selectors with the JS-only compound selectors
    sel_list = list(GENERIC_SELECTORS) + list(GENERIC_SELECTORS_JS_ONLY)
    return f"""
// ── Bilingual toggle (generic) ──
(function() {{
    const EN = {json.dumps(en_map, ensure_ascii=False)};
    const PH_EN = {json.dumps(ph_en)};

    const SEL = {json.dumps(sel_list)};

    let isEn = localStorage.getItem('lang-pref') === 'en';
    const cache = new Map();

    // Get text from direct text nodes only (excludes nested span/strong/em children).
    // Useful for elements like <div class="te-date">May 31 <span>最新</span></div>
    // where the visible date should match the extracted date text, not the badge text.
    function getDirectText(el) {{
        var result = '';
        for (var i = 0; i < el.childNodes.length; i++) {{
            var node = el.childNodes[i];
            if (node.nodeType === 3) {{  // TEXT_NODE
                result += node.textContent;
            }}
        }}
        return result.trim();
    }}

    function applyLang() {{
        SEL.forEach(function(sel) {{
            document.querySelectorAll(sel).forEach(function(el) {{
                // Skip elements with disallowed nested children
                if (el.children.length > 0) {{
                    var hasNested = false;
                    for (var c of el.children) {{
                        if (c.tagName !== 'BR' && c.tagName !== 'SPAN' && c.tagName !== 'STRONG' && c.tagName !== 'EM' && c.tagName !== 'A') {{
                            hasNested = true; break;
                        }}
                    }}
                    if (hasNested) return;
                }}

                // Try direct text first (excludes nested span/strong children),
                // then fall back to the full textContent (covers div.te-summary with <strong>).
                var zh = getDirectText(el);
                if (!EN[zh]) zh = el.textContent.trim();
                if (!zh || !EN[zh]) return;

                if (isEn) {{
                    if (!cache.has(el)) cache.set(el, el.innerHTML);
                    el.textContent = EN[zh];
                }} else {{
                    var saved = cache.get(el);
                    if (saved) el.innerHTML = saved;
                }}
            }});
        }});

        var search = document.getElementById('search');
        if (search) {{
            if (isEn) {{
                if (!cache.has('_ph')) cache.set('_ph', search.placeholder);
                search.placeholder = PH_EN;
            }} else {{
                var saved = cache.get('_ph');
                if (saved) search.placeholder = saved;
            }}
        }}

        var btn = document.getElementById('lang-toggle');
        if (btn) btn.textContent = isEn ? '中文' : 'EN';
        localStorage.setItem('lang-pref', isEn ? 'en' : 'zh');
    }}

    var btn = document.getElementById('lang-toggle');
    if (btn) btn.addEventListener('click', function() {{ isEn = !isEn; applyLang(); }});
    if (isEn) applyLang();
}})();
"""

def inject_bilingual_generic(html, en_map, ph_en):
    """Add toggle to a non-daily page. Falls back to floating button if no topbar."""
    # 1. Toggle button — try topbar-right first, then floating fallback
    btn = '\n            <button class="lang-toggle" id="lang-toggle">EN</button>'
    float_btn = '\n<button class="lang-toggle lang-toggle-float" id="lang-toggle">EN</button>'

    if 'class="topbar-right"' in html:
        html = re.sub(
            r'(<div class="topbar-right">)',
            r'\1' + btn,
            html, count=1)
    elif '<div class="topbar">' in html:
        # Has topbar but no topbar-right
        html = html.replace('<div class="topbar">', '<div class="topbar">' + btn, 1)
    else:
        # No topbar — use floating
        html = html.replace('<body>', '<body>' + float_btn, 1)

    # 2. CSS before </style>
    html = html.replace('</style>', TOGGLE_CSS + '    </style>')

    # 3. JS before </body>
    html = html.replace('</body>', '<script>\n' + build_toggle_js_generic(en_map, ph_en) + '\n    </script>\n</body>')

    return html

# ── Translation (with global cache + concurrent) ─────────

def _load_cache():
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_cache(cache):
    with open(CACHE_PATH, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

async def translate_unique_async(unique_texts, concurrency=3):
    """Translate a set of unique texts concurrently. Returns dict zh->en.
    Uses and updates the global cache."""
    cache = _load_cache()

    # Split into cached vs needs-translation
    todo = [t for t in unique_texts if t not in cache or not cache[t]]
    print(f"  📚 Cache: {len(unique_texts) - len(todo)} hits, {len(todo)} to translate")

    if not todo:
        return cache

    CHUNK = 10
    chunks = [todo[i:i+CHUNK] for i in range(0, len(todo), CHUNK)]
    sem = asyncio.Semaphore(concurrency)

    async with httpx.AsyncClient() as client:
        async def run_chunk(chunk, idx):
            prompt = _build_prompt(chunk)
            resp = await call_minimax_async(client, prompt, sem, chunk_id=f"#{idx}")
            return chunk, _parse_response(resp)

        # Throttle: fire at most `concurrency` at a time
        results = []
        for i in range(0, len(chunks), concurrency):
            batch = chunks[i:i+concurrency]
            print(f"  📡 Translating chunks {i+1}-{min(i+concurrency, len(chunks))} of {len(chunks)}", flush=True)
            batch_results = await asyncio.gather(*[run_chunk(c, i+j+1) for j, c in enumerate(batch)])
            results.extend(batch_results)
            for chunk, parsed in batch_results:
                cache.update(parsed)
            ok_count = sum(1 for _, p in batch_results if p)
            print(f"     → {ok_count}/{len(batch)} succeeded, cache size: {len(cache)}", flush=True)
            _save_cache(cache)  # persist after each batch

    return cache

def translate_texts_cached(texts):
    """Sync wrapper for single-file mode (uses async internally)."""
    unique = list(dict.fromkeys(texts))
    cache = asyncio.run(translate_unique_async(unique))
    result = [cache.get(t, t) for t in texts]
    found = sum(1 for t in texts if t in cache)
    print(f"  ✅ {found}/{len(texts)} translated (cache)")
    return result

def translate_texts(texts):
    """Legacy sync translate (for compatibility)."""
    unique = list(dict.fromkeys(texts))
    translations = {}
    CHUNK = 25

    for i in range(0, len(unique), CHUNK):
        chunk = unique[i:i+CHUNK]
        n_batch = i // CHUNK + 1
        n_total = (len(unique) - 1) // CHUNK + 1
        print(f"  📡 Batch {n_batch}/{n_total} ({len(chunk)} segments)...")
        resp = call_minimax_sync(_build_prompt(chunk))
        if not resp:
            print("  ❌ No response"); continue
        translations.update(_parse_response(resp))
        if i + CHUNK < len(unique):
            time.sleep(0.5)

    result = [translations.get(t, t) for t in texts]
    found = sum(1 for t in texts if t in translations)
    print(f"  ✅ {found}/{len(texts)} translated")
    return result

# ── HTML Injection ────────────────────────────────────────

TOGGLE_CSS = """
/* ── Lang toggle ── */
.lang-toggle {
    background: var(--purple-20);
    color: var(--purple);
    border: none;
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    letter-spacing: 0.5px;
    transition: background 0.2s, color 0.2s;
    white-space: nowrap;
}
.lang-toggle:hover {
    background: var(--purple);
    color: #fff;
}
/* Floating variant for pages without topbar */
.lang-toggle-float {
    position: fixed;
    top: 12px;
    right: 12px;
    z-index: 9999;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
"""

def build_toggle_js(en_texts, ph_en):
    return f"""
// ── Bilingual toggle ──
(function() {{
    const EN = {json.dumps(en_texts, ensure_ascii=False)};
    const PH_EN = {json.dumps(ph_en)};

    // Selectors in the SAME ORDER as Python extract_texts()
    const SEL = [
        'h1',
        '.sec-h',
        '.card-h',
        '.card-body',
        '.card-note',
        '.sum-cat-name',
        '.sum-item',
        'summary.nav-section > span:not(.nav-count)',
        '.nav-item',
        '.mob-toc a',
        '.issue-prev',
        '.topbar-btn',
    ];

    let isEn = localStorage.getItem('lang-pref') === 'en';
    const cache = new Map();

    function applyLang() {{
        let idx = 0;
        SEL.forEach(function(sel) {{
            document.querySelectorAll(sel).forEach(function(el) {{
                if (idx >= EN.length) return;
                var en = EN[idx];
                if (!en) {{ idx++; return; }}

                if (isEn) {{
                    if (!cache.has(idx)) cache.set(idx, el.innerHTML);
                    if (sel === '.card-note') {{
                        var label = el.querySelector('.note-label');
                        if (label) {{
                            el.textContent = '';
                            el.appendChild(label);
                            el.append(' ' + en);
                        }} else {{
                            el.textContent = en;
                        }}
                    }} else {{
                        el.textContent = en;
                    }}
                }} else {{
                    var saved = cache.get(idx);
                    if (saved) el.innerHTML = saved;
                }}
                idx++;
            }});
        }});

        var search = document.getElementById('search');
        if (search) {{
            if (isEn) {{
                if (!cache.has('_ph')) cache.set('_ph', search.placeholder);
                search.placeholder = PH_EN;
            }} else {{
                var saved = cache.get('_ph');
                if (saved) search.placeholder = saved;
            }}
        }}

        var btn = document.getElementById('lang-toggle');
        if (btn) btn.textContent = isEn ? '中文' : 'EN';
        localStorage.setItem('lang-pref', isEn ? 'en' : 'zh');
    }}

    var btn = document.getElementById('lang-toggle');
    if (btn) btn.addEventListener('click', function() {{ isEn = !isEn; applyLang(); }});

    if (isEn) applyLang();
}})();
"""

def inject_bilingual(html, en_texts, ph_en):
    # 1. Toggle button in topbar (before archive link)
    btn = '\n            <button class="lang-toggle" id="lang-toggle">EN</button>'
    html = html.replace(
        '<a href="index.html" class="topbar-btn">',
        btn + '\n            <a href="index.html" class="topbar-btn">'
    )

    # 2. CSS before </style>
    html = html.replace('</style>', TOGGLE_CSS + '    </style>')

    # 3. JS before </body>
    html = html.replace('</body>', '<script>\n' + build_toggle_js(en_texts, ph_en) + '\n    </script>\n</body>')

    return html

# ── Main ──────────────────────────────────────────────────

def process_one(html_path, force=False, generic=False):
    """Process a single HTML file with cache-backed sync translation.
    generic=True: use generic selectors (for non-daily pages).
    generic=False (default): use daily news selectors."""
    if not os.path.exists(html_path):
        print(f"❌ Not found: {html_path}")
        return False

    with open(html_path, encoding='utf-8') as f:
        html = f.read()

    if 'id="lang-toggle"' in html:
        if force:
            print(f"🔄 Force: {os.path.basename(html_path)}")
            html = re.sub(r'\n*\s*<button class="lang-toggle[^"]*"[^>]*>.*?</button>', '', html, flags=re.DOTALL)
            html = re.sub(r'\n*\s*/\* ── Lang toggle ── \*/.*?\}\s*\n', '\n', html, flags=re.DOTALL)
            html = re.sub(r'\s*\.lang-toggle:hover\s*\{[^}]*\}\s*', '\n', html, flags=re.DOTALL)
            html = re.sub(r'\s*\.lang-toggle-float\s*\{[^}]*\}\s*', '\n', html, flags=re.DOTALL)
            html = re.sub(r'\s*\.lang-toggle\s*\{[^}]*\}\s*', '\n', html, flags=re.DOTALL)
            html = re.sub(r'\s*/\* Floating variant.*?\*/\s*', '\n', html, flags=re.DOTALL)
            html = re.sub(r'\n*\s*<script>\s*// ── Bilingual toggle.*?</script>', '', html, flags=re.DOTALL)
            html = re.sub(r'\n*\s*// ── Bilingual toggle.*?\}\)\(\);\s*\n', '\n', html, flags=re.DOTALL)
        else:
            print(f"⏭️  Already bilingual: {os.path.basename(html_path)}")
            return False

    if generic:
        texts = extract_texts_generic(html)
    else:
        texts = extract_texts(html)

    if not texts:
        print(f"⏭️  No content: {os.path.basename(html_path)}")
        return False

    # Deduplicate while preserving order
    texts = list(dict.fromkeys(texts))

    # Check cache for already-translated texts
    cache = _load_cache()
    todo = list(dict.fromkeys(t for t in texts if t not in cache))
    cached = len(texts) - len([t for t in texts if t not in cache])

    if todo:
        print(f"📖 {os.path.basename(html_path)} ({cached} cached, {len(todo)} new)")
        translations = translate_texts(todo)
        # Only cache successful translations (skip where zh==en, i.e. API failed)
        for orig, trans in zip(todo, translations):
            if orig != trans:
                cache[orig] = trans
        _save_cache(cache)
    else:
        print(f"📖 {os.path.basename(html_path)} (all cached)")

    en_map = {t: cache.get(t, t) for t in texts}

    ph_m = re.search(r'placeholder="([^"]*)"', html)
    ph_zh = ph_m.group(1) if ph_m else '搜索新闻...'
    ph_en = 'Search news...' if has_chinese(ph_zh) else ph_zh

    if generic:
        html = inject_bilingual_generic(html, en_map, ph_en)
    else:
        en_texts = [cache.get(t, t) for t in texts]
        html = inject_bilingual(html, en_texts, ph_en)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"   ✅ Done")
    return True

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Add bilingual toggle to AI Daily News HTML')
    parser.add_argument('target', nargs='?', help='Date, "all", "all-daily", or filename. Use "all" for all pages')
    parser.add_argument('--force', action='store_true', help='Re-translate even if already bilingual')
    parser.add_argument('--generic', action='store_true', help='Use generic selectors (for index/topics/etc.)')
    parser.add_argument('--concurrency', type=int, default=3, help='Concurrent API requests (default 3)')
    args = parser.parse_args()

    if not args.target:
        args.target = datetime.now().strftime('%Y-%m-%d')

    if args.target == 'all':
        # Process all page types: daily + index + topics + reports
        files = sorted(set(
            glob.glob(os.path.join(BASE, 'daily-ai-news-20*.html')) +
            glob.glob(os.path.join(BASE, 'index.html')) +
            glob.glob(os.path.join(BASE, 'topics.html')) +
            glob.glob(os.path.join(BASE, 'topic-*.html')) +
            glob.glob(os.path.join(BASE, 'summary.html')) +
            glob.glob(os.path.join(BASE, 'frontier-models-*.html')) +
            glob.glob(os.path.join(BASE, 'Google-IO-*.html')) +
            glob.glob(os.path.join(BASE, 'GTC-*.html'))
        ))
        if not files:
            print("❌ No HTML files found"); sys.exit(1)

        print(f"🚀 Processing {len(files)} files (file-by-file, using cache)...")
        ok = skip = fail = 0
        for i, fp in enumerate(files, 1):
            print(f"\n[{i}/{len(files)}]", end=' ', flush=True)
            # Determine mode based on filename
            is_daily = 'daily-ai-news-' in os.path.basename(fp)
            try:
                result = process_one(fp, force=args.force, generic=not is_daily)
                if result:
                    ok += 1
                else:
                    skip += 1
            except Exception as e:
                print(f"❌ {e}")
                fail += 1

        cache = _load_cache()
        print(f"\n{'='*40}")
        print(f"✅ Translated: {ok}  ⏭️ Skipped: {skip}  ❌ Failed: {fail}")
        print(f"📚 Cache: {len(cache)} translations")
    elif args.target == 'all-daily':
        # Just daily news files
        files = sorted(glob.glob(os.path.join(BASE, 'daily-ai-news-20*.html')))
        ok = skip = fail = 0
        for i, fp in enumerate(files, 1):
            print(f"\n[{i}/{len(files)}]", end=' ', flush=True)
            try:
                result = process_one(fp, force=args.force, generic=False)
                if result:
                    ok += 1
                else:
                    skip += 1
            except Exception as e:
                print(f"❌ {e}")
                fail += 1

        cache = _load_cache()
        print(f"\n{'='*40}")
        print(f"✅ Translated: {ok}  ⏭️ Skipped: {skip}  ❌ Failed: {fail}")
        print(f"📚 Cache: {len(cache)} translations")
    else:
        # Single file: check if daily or not
        if not args.target.endswith('.html'):
            target_path = os.path.join(BASE, f"daily-ai-news-{args.target}.html")
        else:
            target_path = os.path.join(BASE, args.target)
        is_daily = 'daily-ai-news-' in os.path.basename(target_path)
        process_one(target_path, force=args.force, generic=args.generic or not is_daily)

if __name__ == '__main__':
    main()
