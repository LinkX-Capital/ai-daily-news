#!/usr/bin/env python3
"""
Research Agent - 从日报动态生成深度研究报告和投资分析

两阶段设计：
1. Stage 1: 深度研究 - 搞清楚事实（是什么、为什么重要、关键数据、竞争格局）
2. Stage 2: 投资分析 - 对被投企业的影响和行动建议

数据来源：
- 复用日报 JSON（body, insight, link）
- Archive 历史动态搜索
- 外部搜索（Semantic Scholar 论文、Web 搜索）

Usage:
    python research_agent.py --list-today              # 列出今日条目
    python research_agent.py --date 2026-05-12 --index 0  # 研究指定条目
    python research_agent.py --topic "Interaction Model"  # 直接研究主题
    python research_agent.py --company "可灵AI" --full     # 完整研究
"""

import argparse
import asyncio
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

import httpx

# ============ 配置 ============

SCRIPT_DIR = Path(__file__).parent
REPORTS_DIR = SCRIPT_DIR / "reports"
ARCHIVE_DIR = SCRIPT_DIR / "archive"
DAILY_NEWS_PATTERN = "daily-ai-news-{}.md"

# LINK-X 被投企业（按赛道）
LINKX_PORTFOLIO = {
    "模型": ["智谱AI", "面壁智能", "生数科技"],
    "Infra": ["基流科技", "谦和益邦", "AGICmicro", "无问芯穹", "趋境科技"],
    "应用": ["珀乐科技", "AIPPT"],
    "AI4S": ["百奥几何"],
    "安全": ["瑞莱智慧"],
    "具身": ["动易科技", "阿米奥"],
    "Agent": ["紫荆智康"]
}

# 赛道关键词映射
TRACK_KEYWORDS = {
    "L1-计算范式": ["芯片", "量子", "核聚变", "semiconductor", "quantum", "hardware"],
    "L2-模型架构": ["大模型", "LLM", "多模态", "transformer", "MoE", "架构", "训练"],
    "L3-AI Infra": ["推理", "部署", "框架", "推理优化", "serverless", "算力"],
    "L4-应用Agent": ["Agent", "应用", "产品", "商业化", "具身", "机器人", "视频生成"]
}

# 搜索限制
SEARCH_LIMITS = {
    "archive_days": 90,   # Archive 回溯天数
    "archive_results": 10, # 最多返回的历史条目数
    "papers": 5,          # 论文数量
}

# ============ 复用 qa.py 的组件 ============

class MCPWebReader:
    """MCP web-reader 客户端（复用自 qa.py）"""
    def __init__(self):
        self.loop = None

    def fetch(self, url):
        async def _fetch():
            from mcp.client.streamable_http import streamablehttp_client
            from mcp import ClientSession

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
                                if isinstance(parsed, str):
                                    parsed = json.loads(parsed)
                                if isinstance(parsed, dict):
                                    content = parsed.get("content", "")
                                    if content:
                                        return content[:3000]
                            except (json.JSONDecodeError, TypeError):
                                pass
                            if len(text) > 100:
                                return text[:3000]
                    return None

        if self.loop is None or self.loop.is_closed():
            self.loop = asyncio.new_event_loop()
        try:
            return self.loop.run_until_complete(_fetch())
        except Exception:
            self.loop = asyncio.new_event_loop()
            try:
                return self.loop.run_until_complete(_fetch())
            except Exception:
                return None

    def search_alternative(self, query: str) -> List[Dict]:
        """搜索替代来源（复用自 qa.py）"""
        async def _search():
            from mcp.client.streamable_http import streamablehttp_client
            from mcp import ClientSession

            mcp_url = "https://open.bigmodel.cn/api/mcp/web_search_prime/mcp"
            token = os.environ.get("ZHIPU_WEBREADER_TOKEN",
                                    "5f650035e5a845549e4765184d8179b1.GdehlMpHT0dKq3m3")
            headers = {"Authorization": f"Bearer {token}"}
            async with streamablehttp_client(url=mcp_url, headers=headers) as (read, write, _):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool("web_search_prime", {
                        "search_query": query[:70],
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
            if self.loop is None or self.loop.is_closed():
                self.loop = asyncio.new_event_loop()
            return self.loop.run_until_complete(_search())
        except Exception:
            return []

    def close(self):
        if self.loop and not self.loop.is_closed():
            self.loop.close()


# ============ Archive 搜索 ============

class ArchiveSearcher:
    """搜索历史日报档案"""

    def __init__(self):
        self.cache = {}

    def _load_archive(self, date_str: str) -> List[Dict]:
        if date_str in self.cache:
            return self.cache[date_str]

        json_path = ARCHIVE_DIR / f"news_{date_str}.json"
        if json_path.exists():
            try:
                data = json.loads(json_path.read_text(encoding="utf-8"))
                articles = data.get("articles", [])
                self.cache[date_str] = articles
                return articles
            except (json.JSONDecodeError, KeyError):
                return []
        return []

    def search_by_keywords(self, keywords: List[str], days_back: int = 90) -> List[Dict]:
        """按关键词搜索历史动态"""
        results = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        current = start_date
        while current <= end_date:
            date_str = current.strftime("%Y-%m-%d")
            articles = self._load_archive(date_str)

            for article in articles:
                text_to_check = (
                    article.get("title", "") + " " +
                    article.get("body", "") + " " +
                    article.get("summary", "")
                ).lower()

                for kw in keywords:
                    if kw.lower() in text_to_check:
                        results.append({
                            "date": date_str,
                            "title": article.get("title", ""),
                            "body": article.get("body", ""),
                            "insight": article.get("insight", ""),
                            "link": article.get("link", ""),
                            "category": article.get("categories", [""])[0] if article.get("categories") else "",
                        })
                        break

            current += timedelta(days=1)

        results.sort(key=lambda x: x["date"], reverse=True)
        return results[:SEARCH_LIMITS["archive_results"]]


# ============ 外部搜索 ============

class ExternalSearcher:
    """外部搜索（论文、Web）"""

    def __init__(self):
        self.web_reader = MCPWebReader()
        self.timeout = 30

    def search_papers(self, query: str, limit: int = 5) -> List[Dict]:
        """搜索 Semantic Scholar 论文"""
        results = []
        try:
            url = "https://api.semanticscholar.org/graph/v1/paper/search"
            params = {
                "query": query,
                "limit": limit,
                "fields": "paperId,title,abstract,authors,year,url,citationCount"
            }
            response = httpx.get(url, params=params, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                for paper in data.get("data", []):
                    results.append({
                        "paperId": paper.get("paperId"),
                        "title": paper.get("title"),
                        "abstract": paper.get("abstract", ""),
                        "authors": [a.get("name") for a in paper.get("authors", [])],
                        "year": paper.get("year"),
                        "url": paper.get("url"),
                        "citationCount": paper.get("citationCount", 0),
                        "source": "Semantic Scholar"
                    })
        except Exception as e:
            results.append({"source": "Semantic Scholar", "error": str(e)})
        return results

    def search_web(self, query: str) -> List[Dict]:
        """Web 搜索（通过 MCP）"""
        return self.web_reader.search_alternative(query)

    def fetch_url(self, url: str) -> Optional[str]:
        """抓取 URL 内容"""
        # 优先用 MCP
        content = self.web_reader.fetch(url)
        if content:
            return content
        # 回退到 httpx
        try:
            r = httpx.get(url, timeout=15, follow_redirects=True,
                         headers={"User-Agent": "Mozilla/5.0"})
            if r.status_code == 200:
                text = re.sub(r'<[^>]+>', ' ', r.text)
                text = re.sub(r'\s+', ' ', text).strip()
                return text[:3000] if len(text) > 200 else None
        except Exception:
            pass
        return None

    def close(self):
        self.web_reader.close()


# ============ Planner 集成 ============

# 导入 Planner
try:
    from planner import Planner as QuestionPlanner, ResearchPlan, TopicType
except ImportError:
    # 如果 planner.py 不存在，使用简化版本
    QuestionPlanner = None
    ResearchPlan = None
    TopicType = None

# 导入 Knowledge
try:
    from knowledge import Knowledge
    KNOWLEDGE_AVAILABLE = True
except ImportError:
    Knowledge = None
    KNOWLEDGE_AVAILABLE = False


# ============ 联邦搜索主类 ============

class FederatedSearch:
    """联邦搜索：协调多数据源"""

    def __init__(self):
        self.archive = ArchiveSearcher()
        self.external = ExternalSearcher()
        self.planner = QuestionPlanner() if QuestionPlanner else None

    def research(self, topic: str, category: str, context: str,
                 entities: Dict, source_url: str = "",
                 show_plan: bool = False) -> Dict[str, Any]:
        """执行联邦搜索研究"""

        # 1. 使用 Planner 生成研究计划
        if self.planner:
            plan = self.planner.plan(topic, context, category, entities)
            if show_plan:
                print("\n" + plan.to_summary())
                print()
            questions = [q.to_dict() for q in plan.questions]
        else:
            # 回退到简单问题生成
            questions = self._simple_questions(topic, category, entities)

        # 2. 收集搜索关键词
        keywords = []
        keywords.extend(entities.get("companies", [])[:2])
        keywords.extend(entities.get("products", [])[:2])
        topic_words = re.findall(r'[\w\u4e00-\u9fff]{2,}', topic)
        keywords.extend(topic_words[:3])
        keywords = list(set(kw for kw in keywords if len(kw) > 1))

        # 3. 执行搜索
        results = {
            "archive": [],
            "papers": [],
            "web": [],
            "source_content": None
        }

        # 根据问题确定需要的搜索源
        needed_sources = set()
        for q in questions:
            needed_sources.update(q.get("sources", []))

        # Archive 搜索
        if "archive" in needed_sources:
            print("  → 搜索历史档案...")
            archive_results = self.archive.search_by_keywords(
                keywords, days_back=SEARCH_LIMITS["archive_days"]
            )
            results["archive"] = archive_results
            if archive_results:
                print(f"    找到 {len(archive_results)} 条相关历史动态")

        # 抓取来源原文
        if source_url:
            print("  → 抓取来源原文...")
            content = self.external.fetch_url(source_url)
            if content:
                results["source_content"] = content
                print(f"    抓取成功: {len(content)} 字符")

        # 论文搜索
        if "papers" in needed_sources:
            print("  → 搜索论文...")
            paper_results = self.external.search_papers(" ".join(keywords[:3]))
            results["papers"] = paper_results
            if paper_results and not paper_results[0].get("error"):
                print(f"    找到 {len(paper_results)} 篇论文")

        # Web 搜索
        if "web" in needed_sources:
            print("  → Web 搜索...")
            web_results = self.external.search_web(" ".join(keywords[:3]))
            results["web"] = web_results
            if web_results:
                print(f"    找到 {len(web_results)} 条结果")

        # 4. 生成摘要
        summary = self._summarize(results, context)

        return {
            "plan": plan.to_dict() if self.planner and show_plan else None,
            "questions": questions,
            "results": results,
            "summary": summary
        }

    def _simple_questions(self, topic: str, category: str, entities: Dict) -> List[Dict]:
        """简单问题生成（Planner 不可用时的回退）"""
        questions = []

        if category in ["模型前沿", "研究关注"]:
            questions.append({
                "question": f"{topic} 的技术原理是什么？核心创新点？",
                "type": "technical",
                "sources": ["papers", "web", "source"]
            })

        companies = entities.get("companies", [])
        if companies:
            questions.append({
                "question": f"{companies[0]} 相关的历史动态？",
                "type": "company",
                "sources": ["archive", "web"]
            })

        if category in ["模型前沿", "应用", "初创&融资"]:
            questions.append({
                "question": f"这个赛道的主要玩家和竞品是什么？",
                "type": "market",
                "sources": ["archive", "web"]
            })

        return questions

    def _summarize(self, results: Dict, context: str) -> str:
        """生成搜索结果摘要"""
        parts = []

        # 已有信息
        if context:
            parts.append(f"## 已有信息\n{context[:300]}...")

        # 历史动态
        if results["archive"]:
            parts.append(f"\n## 历史动态（过去{SEARCH_LIMITS['archive_days']}天）")
            for item in results["archive"][:5]:
                parts.append(f"- **{item['date']}**: {item['title'][:60]}...")

        # 论文
        if results["papers"] and not results["papers"][0].get("error"):
            parts.append(f"\n## 相关论文")
            for p in results["papers"][:3]:
                parts.append(f"- {p.get('title', 'N/A')} ({p.get('year', 'N/A')})")

        # Web
        if results["web"]:
            parts.append(f"\n## Web 资源")
            for w in results["web"][:3]:
                url = w.get("url", "")[:60]
                content = w.get("content", "")[:100]
                parts.append(f"- {url}: {content}...")

        return "\n".join(parts)

    def close(self):
        self.external.close()


# ============ 研究代理 ============

class ResearchAgent:
    def __init__(self):
        self.reports_dir = REPORTS_DIR
        self.reports_dir.mkdir(exist_ok=True)

        # LLM 配置
        self.api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("MINIMAX_API_KEY", "")
        # 优先使用 Anthropic
        if os.getenv("ANTHROPIC_API_KEY"):
            self.api_url = "https://api.anthropic.com/v1/messages"
            self.model = "claude-sonnet-4-20250514"
            self.use_anthropic = True
        else:
            self.api_url = "https://api.minimaxi.com/anthropic/v1/messages"
            self.model = "MiniMax-M2.5"
            self.use_anthropic = False

        # Knowledge Graph
        self.knowledge = Knowledge() if KNOWLEDGE_AVAILABLE else None

        # Token 追踪
        self.token_usage = {
            "stage1": {"input": 0, "output": 0},
            "stage2": {"input": 0, "output": 0},
            "total": {"input": 0, "output": 0}
        }

    def _call_llm(self, prompt: str, system: str = "",
                  max_tokens: int = 4000, stage: str = "total") -> Optional[str]:
        """调用 LLM"""
        if not self.api_key:
            return None

        if self.use_anthropic:
            # Anthropic API
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            try:
                response = client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=0.2,
                    system=system,
                    messages=[{"role": "user", "content": prompt}]
                )
                # 追踪 token
                if hasattr(response, "usage"):
                    input_tokens = response.usage.input_tokens
                    output_tokens = response.usage.output_tokens
                    self.token_usage[stage]["input"] += input_tokens
                    self.token_usage[stage]["output"] += output_tokens
                    self.token_usage["total"]["input"] += input_tokens
                    self.token_usage["total"]["output"] += output_tokens
                return response.content[0].text
            except Exception as e:
                print(f"    Anthropic API Error: {e}")
                return None
        else:
            # MiniMax API (Anthropic 兼容格式)
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            data = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": 0.2,
                "system": system,
                "messages": [{"role": "user", "content": prompt}]
            }

            try:
                r = httpx.post(self.api_url, json=data, headers=headers,
                              timeout=120, verify=False)
                if r.status_code == 200:
                    resp = r.json()
                    # 追踪 token (如果响应中包含)
                    if "usage" in resp:
                        input_tokens = resp["usage"].get("input_tokens", 0)
                        output_tokens = resp["usage"].get("output_tokens", 0)
                        self.token_usage[stage]["input"] += input_tokens
                        self.token_usage[stage]["output"] += output_tokens
                        self.token_usage["total"]["input"] += input_tokens
                        self.token_usage["total"]["output"] += output_tokens
                    
                    if "content" in resp:
                        for block in resp["content"]:
                            if block.get("type") == "text":
                                text = block.get("text", "")
                                # 跳过工具调用
                                if "<tool_call" not in text and "<invoke" not in text:
                                    return text
                    elif "choices" in resp:
                        return resp["choices"][0].get("message", {}).get("content", "")
            except Exception as e:
                print(f"    MiniMax API Error: {e}")
            return None

    def print_token_summary(self):
        """打印 token 消耗摘要"""
        total_input = self.token_usage["total"]["input"]
        total_output = self.token_usage["total"]["output"]
        total = total_input + total_output
        
        print(f"\n▶ Token 消耗统计:")
        print(f"  Stage 1: {self.token_usage['stage1']['input']:,} in + {self.token_usage['stage1']['output']:,} out = {self.token_usage['stage1']['input'] + self.token_usage['stage1']['output']:,}")
        print(f"  Stage 2: {self.token_usage['stage2']['input']:,} in + {self.token_usage['stage2']['output']:,} out = {self.token_usage['stage2']['input'] + self.token_usage['stage2']['output']:,}")
        print(f"  总计: {total_input:,} in + {total_output:,} out = {total:,} tokens")
        
        # 估算成本 (Anthropic Sonnet 4 定价: $3/M input, $15/M output)
        cost_input = total_input * 3 / 1_000_000
        cost_output = total_output * 15 / 1_000_000
        total_cost = cost_input + cost_output
        print(f"  预估成本: ${total_cost:.4f} (输入 ${cost_input:.4f} + 输出 ${cost_output:.4f})")

    def _extract_entities(self, topic: str, context: str) -> Dict[str, List[str]]:
        """提取关键实体"""
        prompt = f"""从以下文本中提取关键实体（JSON格式）：

主题：{topic}
背景：{context[:500]}

输出格式：
{{"companies": ["公司1"], "products": ["产品1"], "people": ["人名1"]}}
只返回JSON，不要其他内容。"""

        result = self._call_llm(prompt)
        if result:
            try:
                result = result.strip()
                if result.startswith("```"):
                    result = result.split("```")[1]
                    if result.startswith("json"):
                        result = result[4:]
                return json.loads(result.strip())
            except:
                pass
        return {"companies": [], "products": [], "people": []}

    def _classify_track(self, topic: str, context: str) -> str:
        """判断赛道"""
        for track, keywords in TRACK_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in topic.lower() or kw.lower() in context.lower():
                    return track
        return "未分类"

    def _query_knowledge_graph(self, entities: Dict[str, List[str]]) -> str:
        """查询知识图谱获取竞品信息"""
        if not self.knowledge:
            return ""

        parts = []
        all_names = (entities.get("companies", []) +
                    entities.get("products", []) +
                    entities.get("people", []))

        for name in all_names[:3]:  # 最多查3个实体
            try:
                # 查询竞品
                competitors = self.knowledge.get_competitors(name)
                if competitors:
                    parts.append(f"\n### {name} 竞品图谱")
                    for comp in competitors[:5]:
                        track = comp.get("track", "未知赛道")
                        parts.append(f"- **{comp['name']}** ({track})")
                        if comp.get("relation_desc"):
                            parts.append(f"  - {comp['relation_desc']}")
            except Exception:
                pass

        return "\n".join(parts) if parts else ""

    def _get_portfolio_competitors(self, entities: Dict[str, List[str]]) -> str:
        """查询知识图谱中与被投企业相关的竞品"""
        if not self.knowledge:
            return ""

        parts = []
        all_entities = (entities.get("companies", []) +
                       entities.get("products", []))

        for track, companies in LINKX_PORTFOLIO.items():
            for portfolio_company in companies:
                for entity in all_entities:
                    # 检查是否有竞争关系
                    try:
                        competitors = self.knowledge.get_competitors(entity)
                        for comp in competitors:
                            if portfolio_company.lower() in comp["name"].lower():
                                parts.append(f"- **{portfolio_company}** 与 {entity} 存在竞争关系")
                    except Exception:
                        pass

        return "\n".join(parts) if parts else ""

    def stage1_deep_research(self, topic: str, context: str = "",
                            category: str = "", source_url: str = "") -> Dict[str, Any]:
        """Stage 1: 深度研究"""

        print("▶ Stage 1: 深度研究")

        # 1. 提取实体
        entities = self._extract_entities(topic, context)

        # 2. 判断赛道
        track = self._classify_track(topic, context)

        # 3. 查询知识图谱（竞品信息）
        knowledge_context = self._query_knowledge_graph(entities)
        if knowledge_context:
            print("  → 知识图谱: 查询竞品信息...")

        # 4. 联邦搜索
        search_results = {}
        if context or source_url:
            federated = FederatedSearch()
            try:
                search_results = federated.research(
                    topic, category, context, entities, source_url
                )
            finally:
                federated.close()

        # 5. 构建 LLM prompt
        search_summary = search_results.get("summary", "")
        has_archive = len(search_results.get("results", {}).get("archive", [])) > 0

        prompt = f"""你是 AI 行业研究员。请对以下动态进行深度研究：

**主题**: {topic}
**分类**: {category}
**赛道**: {track}

## 已有信息
{context[:1000] if context else "无"}

## 搜索结果
{search_summary[:1500] if search_summary else "无"}

{f'''## 知识图谱
{knowledge_context}
''' if knowledge_context else ""}

---

请完成以下研究（**关键事实必须标注来源**）：

## 1. 事实梳理
- 这到底是个什么东西？（3-5句话）
- 为什么重要？（真正的创新点）
- 关键数据（参数、性能、规模、时间等）

## 2. 技术分析（如适用）
- 核心技术/方法
- 与现有方案的对比
- 技术壁垒

## 3. 竞争格局
- 主要玩家
- 市场位置
- 竞品

## 4. 时间线
- 关键时间节点

## 5. 关键来源
- 官方链接、论文、必读分析

{"## 6. 历史动态" if has_archive else ""}
{f"基于搜索结果中的历史动态，补充该主题的演进过程。" if has_archive else ""}

输出要求：
- 实事求是，不知道就说"需进一步研究"
- 关键信息标注来源（如 "根据日报YYYY-MM-DD"）
- 保持客观
"""

        result = self._call_llm(
            prompt,
            system="你是专业的AI行业研究员。",
            max_tokens=4000,
            stage="stage1"
        )

        return {
            "topic": topic,
            "stage": 1,
            "track": track,
            "entities": entities,
            "research": result or "[LLM 调用失败]",
            "search_summary": search_summary,
            "search_results": search_results,
            "knowledge_context": knowledge_context,
            "timestamp": datetime.now().isoformat()
        }

    def stage2_investment_analysis(self, stage1_result: Dict,
                                   portfolio: Dict = LINKX_PORTFOLIO) -> Dict[str, Any]:
        """Stage 2: 投资影响分析"""

        print("▶ Stage 2: 投资影响分析")

        topic = stage1_result["topic"]
        research = stage1_result["research"]
        track = stage1_result["track"]
        entities = stage1_result.get("entities", {})

        portfolio_text = "\n".join([
            f"- {cat}: {', '.join(comps)}"
            for cat, comps in portfolio.items()
        ])

        # 查询知识图谱中与被投企业的关系
        portfolio_relations = self._get_portfolio_competitors(entities)

        prompt = f"""你是 VC 投资分析师。基于以下研究，分析投资影响：

**主题**: {topic}
**赛道**: {track}

**研究结果**:
{research[:2000]}

**LINK-X 投资组合**:
{portfolio_text}

{f'''**知识图谱关联**:
{portfolio_relations}
''' if portfolio_relations else ""}

---

## 一句话判断
（机会/威胁/观察 + 理由）

## 影响分析
### 直接影响的被投
- 哪些被投受影响？
- 影响性质：技术借鉴/竞争压力/合作机会

### 行业格局影响

## 行动建议
针对每个受影响的被投，给出具体建议

## Sourcing 信号
- 赛道信号？
- 团队背景？
- 相关早期公司？

输出要求：
- 具体到被投企业
- 行动建议可执行
- 无影响明确说"暂无明显影响"
"""

        result = self._call_llm(
            prompt,
            system="你是专业的VC投资分析师。",
            max_tokens=3000,
            stage="stage2"
        )

        return {
            "topic": topic,
            "stage": 2,
            "analysis": result or "[LLM 调用失败]",
            "portfolio_relations": portfolio_relations,
            "timestamp": datetime.now().isoformat()
        }

    def generate_report(self, stage1: Dict, stage2: Optional[Dict] = None) -> str:
        """生成报告"""
        topic = stage1["topic"]
        track = stage1["track"]
        date_str = datetime.now().strftime("%Y-%m-%d")

        report = f"""# {topic} 研究报告

> 生成时间: {date_str} | 赛道: {track}

---

## Stage 1: 深度研究

{stage1.get("research", "")}

"""

        if stage2:
            report += f"""---

## Stage 2: 投资影响分析

{stage2.get("analysis", "")}

---
"""

        return report

    def save_report(self, topic: str, report: str) -> str:
        """保存报告"""
        safe_topic = re.sub(r'[^\w\s-]', '', topic)[:50]
        filename = f"{datetime.now().strftime('%Y%m%d')}-{safe_topic}.md"
        filepath = self.reports_dir / filename
        filepath.write_text(report, encoding="utf-8")
        return str(filepath)

    def validate_report(self, report: str, search_results: dict = None) -> str:
        """验证报告并附加验证报告"""
        try:
            from validator import Validator
            validator = Validator()
            result = validator.validate(report, search_results)
            
            # 打印验证结果摘要
            print(f"\n▶ 事实校验: {result.verified_count}/{result.total_claims} 已验证, 置信度 {result.confidence_score:.1%}")
            
            if result.error_count > 0:
                print(f"  ⚠️ 发现 {result.error_count} 个可能错误")
            
            # 如果置信度低或有错误，附加验证报告
            if result.confidence_score < 0.7 or result.error_count > 0:
                validation_report = validator.to_summary(result)
                return report + f"\n\n---\n\n## 附录：事实校验报告\n\n{validation_report}\n"
            return report
        except Exception as e:
            print(f"  [验证跳过: {e}]")
            return report


# ============ 工具函数 ============

def load_daily_news(date_str: str) -> Optional[str]:
    """加载日报内容"""
    md_path = SCRIPT_DIR / DAILY_NEWS_PATTERN.format(date_str)
    if md_path.exists():
        return md_path.read_text(encoding="utf-8")
    return None

def load_archive_news(date_str: str) -> Optional[List[Dict]]:
    """加载 JSON 档案"""
    json_path = ARCHIVE_DIR / f"news_{date_str}.json"
    if json_path.exists():
        try:
            data = json.loads(json_path.read_text(encoding="utf-8"))
            return data.get("articles", [])
        except:
            return []
    return None

def extract_news_items(md_content: str) -> List[Dict]:
    """从 MD 解析新闻条目"""
    items = []
    current_category = None
    lines = md_content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("### "):
            current_category = line[4:].strip()
            i += 1
            continue

        if line.startswith("**") and line.endswith("**"):
            title = line[2:-2].strip()
            body_lines, insight_lines, source = [], [], ""
            i += 1

            while i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith("**") and next_line.endswith("**"):
                    break
                if next_line.startswith("### "):
                    break
                if not next_line or next_line.startswith("---"):
                    i += 1
                    continue

                if next_line.startswith("- "):
                    body_lines.append(next_line[2:])
                elif "来源:" in next_line or next_line.startswith("   - 来源"):
                    source = next_line
                elif next_line.startswith("> 💡"):
                    insight_lines.append(next_line[5:].strip())
                elif insight_lines and (next_line.startswith("  >") or next_line.startswith("   ")):
                    insight_lines.append(next_line.strip())
                i += 1

            items.append({
                "category": current_category,
                "title": title,
                "body": " ".join(body_lines).strip(),
                "insight": " ".join(insight_lines).strip(),
                "source": source
            })
            continue

        i += 1

    return items


# ============ CLI ============

def main():
    parser = argparse.ArgumentParser(
        description="Research Agent - 从日报动态生成深度研究报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python research_agent.py --list-today
  python research_agent.py --date 2026-05-12 --index 0
  python research_agent.py --topic "Interaction Model"
  python research_agent.py --company "可灵AI" --full
        """
    )

    parser.add_argument("--topic", help="研究主题")
    parser.add_argument("--company", help="研究公司")
    parser.add_argument("--date", help="日报日期")
    parser.add_argument("--index", type=int, help="条目索引")
    parser.add_argument("--list-today", action="store_true")
    parser.add_argument("--full", action="store_true", help="完整研究")
    parser.add_argument("--show-plan", action="store_true", help="显示研究计划")
    parser.add_argument("--output", help="输出文件")
    parser.add_argument("--plan-only", action="store_true", help="只显示研究计划")

    args = parser.parse_args()

    agent = ResearchAgent()

    # 列出条目
    if args.list_today:
        today = datetime.now().strftime("%Y-%m-%d")
        md_content = load_daily_news(today)
        if not md_content:
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            md_content = load_daily_news(yesterday)
            date_display = yesterday
        else:
            date_display = today

        if not md_content:
            print("找不到日报")
            return

        items = extract_news_items(md_content)
        print(f"\n=== {date_display} 日报条目 ===\n")
        for i, item in enumerate(items):
            print(f"[{i}] {item['category']} | {item['title']}")
        return

    # 确定研究内容
    topic = args.topic or args.company
    context = ""
    category = ""
    source_url = ""

    if args.date:
        # 尝试从 JSON 加载（保留原始 link）
        articles = load_archive_news(args.date)
        md_content = load_daily_news(args.date)

        if md_content:
            items = extract_news_items(md_content)
            if args.index is not None and args.index < len(items):
                item = items[args.index]
                topic = item["title"]
                context = f"{item['body']}\n{item['insight']}"
                category = item["category"]

                # 尝试从 JSON 获取原始 link
                if articles and args.index < len(articles):
                    source_url = articles[args.index].get("link", "")
            elif args.index is None:
                print(f"请指定 --index (0-{len(items)-1})")
                return
            else:
                print(f"索引超出范围")
                return
        else:
            print(f"找不到 {args.date} 的日报")
            return

    elif args.company:
        topic = f"{args.company} 公司研究"
        context = f"研究目标：{args.company} 的技术路线、产品、竞争地位"
        category = "公司研究"

    if not topic:
        parser.print_help()
        return

    print(f"\n{'='*60}")
    print(f"研究主题: {topic}")
    print(f"{'='*60}\n")

    # Stage 1
    stage1 = agent.stage1_deep_research(topic, context, category, source_url)
    print("✓ Stage 1 完成\n")

    # Stage 2
    stage2 = None
    if args.full:
        stage2 = agent.stage2_investment_analysis(stage1)
        print("✓ Stage 2 完成\n")

    # 生成报告
    report = agent.generate_report(stage1, stage2)
    
    # 验证报告并附加验证结果（从 stage1 获取搜索结果）
    search_results_from_stage1 = stage1.get("search_results", {})
    report = agent.validate_report(report, search_results_from_stage1)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"✓ 报告已保存: {args.output}")
    else:
        filepath = agent.save_report(topic, report)
        print(f"✓ 报告已保存: {filepath}")

    # Token 统计
    agent.print_token_summary()

    # 预览
    print("\n" + "="*60)
    print(report[:500] + ("..." if len(report) > 500 else ""))
    print("="*60)


if __name__ == "__main__":
    main()