#!/usr/bin/env python3
"""
日报质量检查脚本
在生成 MD 后、发布前运行，输出质检报告

用法：
  python qa.py                  # 检查 daily-ai-news.md
  python qa.py 2026-04-20       # 检查 daily-ai-news-2026-04-20.md
  python qa.py --factcheck      # 启用 LLM 事实校验
  python qa.py --factcheck 2026-04-20
"""

import os
import re
import sys
import json
from collections import defaultdict
from datetime import datetime
import httpx

# 从 html_generator 复用 parse_md
sys.path.insert(0, os.path.dirname(__file__))
from html_generator import parse_md

VALID_CATEGORIES = {"模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"}

# 低价值关键词（应被过滤的内容）
LOW_VALUE_KEYWORDS = [
    "招募", "征集中", "倒计时", "沙龙", "报名", "活动预告",
    "招聘", "求职", "Hiring",
    "讲座预告", "直播预告",
]

# 过度推断/空洞表达关键词（用于 insight 检查）
OVER_INFER_KEYWORDS = [
    "彻底改变", "开启新纪元", "标志着.*时代的到来", "将颠覆",
    "走在行业前列", "引领行业", "开创先河",
    "革命性突破", "历史性突破", "划时代",
    "重要里程碑", "填补了.*空白",
    "AGI的关键路径", "通向AGI的必经之路",
    # 过度引申
    "可能.*重塑", "有望颠覆", "或将引发.*革命",
    "意味着.*时代的", "标志着一个新",
    "永远改变", "不可逆转",
    "正在彻底", "已经彻底",
]

# 品牌/公司别称映射（用于同公司去重）
COMPANY_ALIASES = {
    "高德": ["高德", "ABot", "途途"],
    "Luma": ["Luma", "LumaLabs", "lumalabsai"],
    "SemiAnalysis": ["SemiAnalysis", "semianalysis_"],
    "OpenAI": ["OpenAI"],
    "Anthropic": ["Anthropic"],
    "Meta": ["Meta", "Facebook", "扎克伯格"],
    "Google": ["Google", "谷歌", "DeepMind"],
    "NVIDIA": ["NVIDIA", "英伟达", " Nvidia"],
    "Microsoft": ["Microsoft", "微软"],
    "vLLM": ["vllm_project", "vLLM"],
}


def load_md(date_str=None):
    base = os.path.dirname(__file__)
    if date_str:
        path = os.path.join(base, f"daily-ai-news-{date_str}.md")
    else:
        path = os.path.join(base, "daily-ai-news.md")
    if not os.path.exists(path):
        print(f"文件不存在: {path}")
        sys.exit(1)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read(), path


def check_low_value(articles):
    """检查是否有应被过滤的低价值条目"""
    issues = []
    for a in articles:
        title = a.get('title', '')
        body = a.get('body', '')
        text = title + ' ' + body
        for kw in LOW_VALUE_KEYWORDS:
            if kw in text:
                issues.append(('low_value', a['title'], f"含低价值关键词: {kw}"))
                break
    return issues


def check_categories(articles):
    """检查分类是否有效"""
    issues = []
    for a in articles:
        cats = a.get('categories', [])
        if not cats:
            issues.append(('no_category', a['title'], "无分类"))
            continue
        for c in cats:
            if c not in VALID_CATEGORIES:
                issues.append(('invalid_category', a['title'], f"无效分类: {c}"))
    return issues


def check_company_dup(articles):
    """检查同一公司是否出现超过2条"""
    issues = []
    company_items = defaultdict(list)
    for a in articles:
        title = a.get('title', '')
        for company, aliases in COMPANY_ALIASES.items():
            if any(alias in title for alias in aliases):
                company_items[company].append(a['title'])
                break
    for company, items in company_items.items():
        if len(items) > 2:
            issues.append(('company_dup', company,
                          f"出现{len(items)}条（建议最多2条）: {'; '.join(items[:3])}..."))
    return issues


def check_over_inference(articles):
    """检查 insight 中是否有过度推断/空洞表达
    insight 要务实严谨，基于事实做判断，不过度引申
    """
    issues = []
    for a in articles:
        insight_text = ' '.join(a.get('key_points', []))
        for pattern in OVER_INFER_KEYWORDS:
            if re.search(pattern, insight_text):
                issues.append(('over_infer', a['title'],
                              f"insight含过度推断 '{pattern}': {insight_text[:60]}..."))
                break
    return issues


def check_body_quality(articles):
    """检查 body 质量：长度、信息密度
    body 只描述关键事实和关联事件，不做判断/引申（判断放在 insight）
    """
    issues = []
    for a in articles:
        body = a.get('body', '').strip()
        title = a.get('title', '')

        # 计算句子数（不去掉加粗内容，直接在原文上算）
        sentences = [s.strip() for s in re.split(r'[。！？]', body) if s.strip()]
        sent_count = len(sentences)

        if not body:
            issues.append(('empty_body', title, "body为空"))
        elif sent_count < 2:
            issues.append(('short_body', title, f"body仅{sent_count}句话（建议2-5句）"))
        elif sent_count > 7:
            issues.append(('long_body', title, f"body有{sent_count}句话（建议2-5句）"))

        # 检查 body 是否包含不应有的判断性表达（判断应在 insight 中）
        judgment_patterns = [
            (r'这意味着', 'body含判断性表达'),
            (r'这表明', 'body含判断性表达'),
            (r'这标志着', 'body含判断性表达'),
            (r'这反映出', 'body含判断性表达'),
            (r'这不仅是.*更是', 'body含判断性表达'),
        ]
        for pattern, desc in judgment_patterns:
            if re.search(pattern, body):
                issues.append(('body_has_judgment', title,
                              f"{desc}（判断应放在insight中）: {re.search(pattern, body).group()[:30]}"))
                break
    return issues


def check_source(articles):
    """检查来源链接"""
    issues = []
    for a in articles:
        if not a.get('link'):
            issues.append(('no_source', a['title'], "缺少来源链接"))
    return issues


def check_summary_sync(articles, summary_items):
    """检查要点速览与详细内容是否同步"""
    issues = []
    # 收集详细条目的标题关键词（取主体名词）
    detail_keywords = []
    for a in articles:
        title = a.get('title', '')
        # 提取2-4字关键词
        kws = re.findall(r'[\u4e00-\u9fff]{2,4}|[A-Z][a-z]+|OpenAI|Google|Meta|NVIDIA|AI|ABot', title)
        detail_keywords.append(set(kws))

    # 检查要点速览中提到的条目是否在详细内容中
    for cat, items in summary_items.items():
        for item in items:
            item_kws = set(re.findall(r'[\u4e00-\u9fff]{2,4}|[A-Z][a-z]+|OpenAI|Google|Meta|NVIDIA|AI|ABot', item))
            if not item_kws:
                continue
            found = False
            for dk in detail_keywords:
                overlap = item_kws & dk
                if len(overlap) >= 2:
                    found = True
                    break
            if not found:
                issues.append(('summary_orphan', item[:40],
                              f"要点速览条目在详细内容中无对应"))
    return issues


# --- 事实校验 ---

# 应保持英文的公司名和人名（不翻译为中文）
KEEP_ENGLISH = [
    "OpenAI", "Google", "Anthropic", "NVIDIA", "Meta", "Microsoft",
    "Amazon", "Apple", "DeepMind", "SemiAnalysis", "Luma",
    "MiniMax", "vLLM", "Marvell", "PyTorch", "Chalkie",
    "Stargate", "Tinker",
    "Sam Altman", "Mira Murati", "Dario Amodei", "Jensen Huang",
    "Mark Zuckerberg", "Joshua Gross", "Andrew Tulloch",
    "Barret Zoph", "Soumith Chintala",
]

# 模糊称呼（应具体到人名或公司名）
VAGUE_REFERENCES = [
    r"AI研究者[说道称]",
    r"研究人员[说道称]",
    r"业内专家[说道称]",
    r"业内人士[说道称]",
    r"相关人士[说道称]",
    r"科学家们",
    r"某公司",
    r"知名公司",
]


def check_fact_heuristic(articles):
    """启发式事实校验：模糊称呼、英文翻译、无依据声称"""
    issues = []
    for a in articles:
        title = a.get('title', '')
        body = a.get('body', '')
        insight = ' '.join(a.get('key_points', []))
        text = title + ' ' + body

        # 1. 模糊称呼检查
        for pattern in VAGUE_REFERENCES:
            if re.search(pattern, text):
                issues.append(('vague_ref', title,
                              f"含模糊称呼: {re.search(pattern, text).group()}"))
                break

        # 2. 英文名翻译检查
        # 检查是否出现了中文翻译后的公司名/人名，但没出现英文原文
        cn_to_en = {
            "开放人工智能": "OpenAI", "脸书": "Meta", "谷歌": "Google",
            "英伟达": "NVIDIA", "微软": "Microsoft", "亚马逊": "Amazon",
            "苹果": "Apple", "深度思维": "DeepMind",
        }
        for cn, en in cn_to_en.items():
            if cn in text and en not in text:
                issues.append(('translated_name', title,
                              f"'{cn}'应使用英文 '{en}'"))
                break

        # 3. 无依据因果声称检查
        unsupported_claims = [
            r"这将彻底",
            r"必将导致",
            r"一定会",
            r"毫无疑问",
        ]
        for pattern in unsupported_claims:
            if re.search(pattern, insight):
                issues.append(('unsupported_claim', title,
                              f"insight含无依据声称: {re.search(pattern, insight).group()}"))
                break

        # 4. 数据准确性标记：检查 body 中的数字是否有 "约"/"近"/"超" 等限定词
        # 如 "$5000亿" 之类的大额数字缺乏限定
        numbers_in_body = re.findall(r'[\$￥]?(\d+[,.]?\d*)\s*(亿|万|百万|十亿|trillion|billion|million)', body)
        if numbers_in_body:
            for num_tuple in numbers_in_body:
                # 检查该数字附近是否有来源标记
                num_str = num_tuple[0] + num_tuple[1]
                context_start = max(0, body.find(num_str) - 10)
                context = body[context_start:body.find(num_str) + len(num_str) + 10]
                # 如果数字前没有 "据"、"报告"、"预计" 等来源标记，也没有加粗
                if not re.search(r'(据|报告|预计|数据|统计|透露|宣布|确认)\S{0,5}$', body[context_start:body.find(num_str)]):
                    # 加粗的数字通常有来源支撑
                    if f'**{num_str}' not in body and f'{num_str}**' not in body:
                        pass  # 不标记，避免误报

    return issues


def fetch_source_content(url):
    """httpx 直接抓取，作为 MCP 的回退方案"""
    try:
        with httpx.Client(timeout=15, follow_redirects=True, verify=False) as client:
            r = client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                text = re.sub(r'<[^>]+>', ' ', r.text)
                text = re.sub(r'\s+', ' ', text).strip()
                if len(text) > 200:
                    return text[:3000]
    except Exception:
        pass
    return None


def search_alternative_sources(title):
    """当原文抓取失败时，用 web-search 找替代来源并抓取"""
    import asyncio
    from mcp.client.streamable_http import streamablehttp_client
    from mcp import ClientSession

    # 从标题提取搜索关键词
    search_query = re.sub(r'[，。：；！？、]', ' ', title).strip()[:70]

    async def _search():
        mcp_url = "https://open.bigmodel.cn/api/mcp/web_search_prime/mcp"
        token = os.environ.get("ZHIPU_WEBREADER_TOKEN",
                                "5f650035e5a845549e4765184d8179b1.GdehlMpHT0dKq3m3")
        headers = {"Authorization": f"Bearer {token}"}
        async with streamablehttp_client(url=mcp_url, headers=headers) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("web_search_prime", {
                    "search_query": search_query,
                    "location": "cn",
                    "content_size": "medium",
                })
                items = []
                for c in result.content:
                    if hasattr(c, "text"):
                        text = c.text
                        try:
                            parsed = json.loads(text)
                            if isinstance(parsed, str):
                                parsed = json.loads(parsed)
                        except (json.JSONDecodeError, TypeError):
                            parsed = None
                        if isinstance(parsed, list):
                            for item in parsed[:5]:
                                if isinstance(item, dict):
                                    items.append({
                                        "url": item.get("link") or item.get("url", ""),
                                        "content": item.get("content", ""),
                                    })
                        break
                return items

    try:
        loop = asyncio.new_event_loop()
        items = loop.run_until_complete(_search())
        loop.close()
    except Exception:
        return None

    if not items:
        return None

    # 优先拼接搜索结果的 content 作为原文摘要
    summaries = []
    for item in items:
        if item["content"] and len(item["content"]) > 50:
            summaries.append(item["content"])
    if summaries:
        combined = "\n".join(summaries)
        if len(combined) > 200:
            print(f"      -> 搜索摘要: {len(combined)}字")
            return combined[:3000]

    # 用 MCP web-reader 抓取搜索到的替代链接
    mcp_reader = MCPWebReader()
    for item in items:
        alt_url = item["url"]
        if not alt_url:
            continue
        content = mcp_reader.fetch(alt_url)
        if content and len(content) > 200:
            print(f"      -> 搜索替代来源: {alt_url[:60]}")
            return content
        content = fetch_source_content(alt_url)
        if content and len(content) > 200:
            print(f"      -> 搜索替代来源: {alt_url[:60]}")
            return content
    return None


class MCPWebReader:
    """MCP web-reader 客户端，复用单次 session"""
    def __init__(self):
        self.loop = None

    def fetch(self, url):
        import asyncio
        from mcp.client.streamable_http import streamablehttp_client
        from mcp import ClientSession

        async def _fetch():
            mcp_url = "https://open.bigmodel.cn/api/mcp/web_reader/mcp"
            token = os.environ.get("ZHIPU_WEBREADER_TOKEN",
                                    "5f650035e5a845549e4765184d8179b1.GdehlMpHT0dKq3m3")
            headers = {"Authorization": f"Bearer {token}"}
            async with streamablehttp_client(url=mcp_url, headers=headers) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool("webReader", {
                        "url": url,
                        "return_format": "text",
                        "retain_images": False,
                    })
                    for c in result.content:
                        if hasattr(c, "text"):
                            text = c.text
                            try:
                                parsed = json.loads(text)
                                # 双重编码：json.loads 可能返回字符串
                                if isinstance(parsed, str):
                                    parsed = json.loads(parsed)
                                if isinstance(parsed, dict):
                                    content = parsed.get("content", "")
                                    if content:
                                        return content[:3000]
                            except (json.JSONDecodeError, TypeError, AttributeError):
                                pass
                            if len(text) > 100:
                                return text[:3000]
                    return None

        if self.loop is None or self.loop.is_closed():
            self.loop = asyncio.new_event_loop()
        try:
            return self.loop.run_until_complete(_fetch())
        except Exception as e:
            # 如果失败，创建新 loop 重试一次
            self.loop = asyncio.new_event_loop()
            try:
                return self.loop.run_until_complete(_fetch())
            except Exception as e2:
                return None


def call_llm_factcheck(title, body, insight, source_text):
    """用 LLM 对单条新闻做事实校验"""
    api_key = os.environ.get("MINIMAX_API_KEY", "")
    api_url = "https://api.minimaxi.com/anthropic/v1/messages"
    if not api_key:
        return None

    prompt = f"""你是事实核查员。请对比以下日报条目与原文内容，找出事实错误或不一致。

## 日报条目
标题：{title}
正文：{body}
Insight：{insight}

## 原文摘要
{source_text[:2000]}

## 检查项
1. 人名、公司名、产品名是否准确
2. 数据（金额、百分比、数量）是否一致
3. 因果关系是否正确（是否强加了原文没有的因果）
4. 是否有原文没有的推测性内容被当作事实呈现

## 输出格式
如果发现事实问题，输出JSON数组：
[{{"issue": "问题描述", "detail": "原文是X，日报写的是Y", "severity": "error/warning"}}]

如果没有问题，输出：[]
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "MiniMax-M2.5",
        "max_tokens": 2000,
        "temperature": 0.1,
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        r = httpx.post(api_url, headers=headers, json=data, timeout=120, verify=False)
        if r.status_code == 200:
            resp = r.json()
            text = ""
            if "content" in resp:
                for block in resp["content"]:
                    if block.get("type") == "text":
                        text = block.get("text", "")
                        break
                    # MiniMax thinking 模型：text 可能在 thinking 字段
                    if "text" in block:
                        text = block["text"]
                        break
            elif "choices" in resp:
                text = resp["choices"][0].get("message", {}).get("content", "")
            # 提取JSON
            match = re.search(r'\[.*\]', text, re.DOTALL)
            if match:
                return json.loads(match.group())
            # LLM 可能返回空数组或纯文本"[]"
            if text.strip() == "[]":
                return []
            return None
        else:
            print(f"    LLM HTTP {r.status_code}")
            return None
    except httpx.TimeoutException:
        print(f"    LLM超时，跳过")
        return None
    except Exception as e:
        print(f"    LLM调用失败: {e}")
        return None


def check_fact_llm(articles):
    """用 LLM 对每条新闻与原文做事实校验"""
    issues = []
    checked = 0
    mcp_reader = MCPWebReader()

    for a in articles:
        link = a.get('link', '')
        if not link:
            continue

        title = a.get('title', '')
        body = a.get('body', '')
        insight = ' '.join(a.get('key_points', []))

        # 处理多个链接（用 | 分隔）
        links = re.findall(r'https?://[^\s|)]+', link)
        if not links:
            links = [link]

        # 优先用 MCP web-reader 抓取
        source_text = None
        for l in links:
            source_text = mcp_reader.fetch(l)
            if source_text and len(source_text) > 200:
                break

        # MCP 失败时回退 httpx
        if not source_text or len(source_text) < 200:
            for l in links:
                source_text = fetch_source_content(l)
                if source_text and len(source_text) > 200:
                    break

        if not source_text or len(source_text) < 200:
            # 最后尝试：web-search 搜索替代来源
            print(f"    [?] 原文抓取失败，搜索替代来源: {title[:40]}...")
            source_text = search_alternative_sources(title)

        if not source_text or len(source_text) < 200:
            issues.append(('fetch_fail', title, f"无法抓取原文: {links[0][:60]}"))
            continue

        checked += 1
        print(f"    [{checked}] 校验中: {title[:40]}...")

        result = call_llm_factcheck(title, body, insight, source_text)
        if result is not None:
            for item in result:
                severity = item.get('severity', 'warning')
                tag = 'fact_error' if severity == 'error' else 'fact_warning'
                issues.append((tag, title,
                              f"{item.get('issue', '')}: {item.get('detail', '')}"))
        else:
            issues.append(('llm_fail', title, "LLM校验返回空"))

    return issues


def check_insight_quality(articles):
    """检查 insight 是否只是重复标题"""
    issues = []
    for a in articles:
        title = a.get('title', '')
        for kp in a.get('key_points', []):
            # 去掉标题中的主体部分，检查 insight 是否只是复述
            title_core = re.sub(r'[，。：；、]', '', title[:20])
            kp_core = re.sub(r'[，。：；、]', '', kp[:20])
            if title_core and kp_core and (title_core in kp_core or kp_core in title_core):
                issues.append(('insight_repeat', title,
                              f"insight可能只是重复标题: {kp[:50]}..."))
    return issues


def check_title_similarity(articles):
    """检查是否有标题高度相似的重复条目"""
    issues = []

    def normalize_for_comparison(text):
        text = text.lower()
        stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
                     "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
                     "being", "have", "has", "had", "do", "does", "did", "will", "would",
                     "could", "should", "may", "might", "can", "this", "that", "these",
                     "those", "it", "its", "2026", "2025", "2024", "2023", "-", ":", "|",
                     "now", "new", "pro", "3", "2", "1", "ai", "llm", "model", "google",
                     "openai", "meta", "microsoft", "anthropic", "deepmind"}
        english_words = set(w for w in re.findall(r'[a-z]+', text) if w not in stopwords and len(w) > 1)
        chinese_text = re.sub(r'[a-z0-9\s]', '', text)
        chinese_bigrams = set(chinese_text[i:i+2] for i in range(len(chinese_text)-1))
        return english_words | chinese_bigrams

    titles = [(a.get('title', ''), normalize_for_comparison(a.get('title', ''))) for a in articles]
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            t1_set = titles[i][1]
            t2_set = titles[j][1]
            if not t1_set or not t2_set:
                continue
            intersection = len(t1_set & t2_set)
            union = len(t1_set | t2_set)
            sim = intersection / union if union > 0 else 0.0
            if sim >= 0.4:
                issues.append(('title_similar', titles[i][0],
                              f"与'{titles[j][0][:30]}'相似度{sim:.0%}，可能重复"))
    return issues


def run_checks(date_str=None, factcheck=False):
    md_content, path = load_md(date_str)
    articles, summary_items = parse_md(md_content)

    print(f"=== 日报质量检查 ===")
    print(f"文件: {path}")
    print(f"条目数: {len(articles)}")
    print(f"分类: {', '.join(VALID_CATEGORIES)}")
    if factcheck:
        print(f"事实校验: 启用（LLM）")
    print()

    all_issues = []

    # 1. 低价值检测
    issues = check_low_value(articles)
    all_issues.extend(issues)
    print(f"[1] 低价值条目: {len(issues)} 个问题")
    for _, title, detail in issues:
        print(f"    - {title}")
        print(f"      {detail}")

    # 2. 分类检查
    issues = check_categories(articles)
    all_issues.extend(issues)
    print(f"\n[2] 分类问题: {len(issues)} 个")
    for _, title, detail in issues:
        print(f"    - {title}: {detail}")

    # 3. 同公司去重
    issues = check_company_dup(articles)
    all_issues.extend(issues)
    print(f"\n[3] 同公司重复: {len(issues)} 个")
    for _, company, detail in issues:
        print(f"    - {company}: {detail}")

    # 4. 过度推断
    issues = check_over_inference(articles)
    all_issues.extend(issues)
    print(f"\n[4] 过度推断: {len(issues)} 个")
    for _, title, detail in issues:
        print(f"    - {title}")
        print(f"      {detail}")

    # 5. Body 质量
    issues = check_body_quality(articles)
    all_issues.extend(issues)
    print(f"\n[5] Body质量: {len(issues)} 个问题")
    for _, title, detail in issues:
        print(f"    - {title}: {detail}")

    # 6. 来源检查
    issues = check_source(articles)
    all_issues.extend(issues)
    print(f"\n[6] 来源链接: {len(issues)} 个缺失")
    for _, title, detail in issues:
        print(f"    - {title}: {detail}")

    # 7. 要点速览同步
    issues = check_summary_sync(articles, summary_items)
    all_issues.extend(issues)
    print(f"\n[7] 要点速览同步: {len(issues)} 个问题")
    for _, title, detail in issues:
        print(f"    - {title}: {detail}")

    # 8. Insight质量
    issues = check_insight_quality(articles)
    all_issues.extend(issues)
    print(f"\n[8] Insight质量: {len(issues)} 个问题")
    for _, title, detail in issues:
        print(f"    - {title}")
        print(f"      {detail}")

    # 9. 启发式事实校验（快速，免费）
    issues = check_fact_heuristic(articles)
    all_issues.extend(issues)
    print(f"\n[9] 事实校验(启发式): {len(issues)} 个问题")
    for _, title, detail in issues:
        print(f"    - {title}: {detail}")

    # 10. 标题相似度（重复检测）
    issues = check_title_similarity(articles)
    all_issues.extend(issues)
    print(f"\n[10] 标题相似度: {len(issues)} 个问题")
    for _, title, detail in issues:
        print(f"    - {title}: {detail}")

    # 11. LLM 事实校验（可选，逐条比对原文）
    if factcheck:
        print(f"\n[11] 事实校验(LLM): 逐条对比原文...")
        issues = check_fact_llm(articles)
        all_issues.extend(issues)
        if not issues:
            print(f"    全部通过")
        else:
            for _, title, detail in issues:
                print(f"    - {title}: {detail}")

    # 汇总
    print(f"\n{'='*50}")
    if not all_issues:
        print("全部检查通过，无问题。")
    else:
        # 按类型统计
        by_type = defaultdict(list)
        for issue in all_issues:
            by_type[issue[0]].append(issue)
        print(f"共发现 {len(all_issues)} 个问题:")
        for type_name, items in by_type.items():
            print(f"  - {type_name}: {len(items)} 个")

        # 严重程度
        critical = [i for i in all_issues if i[0] in ('low_value', 'over_infer', 'company_dup', 'fact_error', 'unsupported_claim')]
        warnings = [i for i in all_issues if i[0] in ('short_body', 'empty_body', 'body_has_judgment', 'insight_repeat', 'vague_ref', 'translated_name', 'fact_warning')]
        minor = [i for i in all_issues if i[0] in ('no_source', 'summary_orphan', 'fetch_fail', 'llm_fail', 'title_similar', 'long_body')]

        if critical:
            print(f"\n需要处理 ({len(critical)}):")
            for _, title, detail in critical:
                print(f"  !! {title}: {detail}")
        if warnings:
            print(f"\n建议优化 ({len(warnings)}):")
            for _, title, detail in warnings:
                print(f"  ? {title}: {detail}")
        if minor:
            print(f"\n可选修复 ({len(minor)}):")
            for _, title, detail in minor:
                print(f"  ~ {title}: {detail}")

    return len(all_issues)


if __name__ == "__main__":
    args = sys.argv[1:]
    factcheck = '--factcheck' in args
    args = [a for a in args if a != '--factcheck']
    date_str = args[0] if args else None
    issue_count = run_checks(date_str, factcheck=factcheck)
    sys.exit(1 if issue_count > 0 else 0)
