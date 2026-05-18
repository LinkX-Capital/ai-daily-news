#!/usr/bin/env python3
"""
联邦搜索模块 - 复用日报内容 + 补充外部搜索

设计原则：
1. 日报已有的内容直接复用（body, insight, link）
2. 根据问题类型选择补充搜索源
3. 搜索结果标注来源，不混合
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import httpx


# ============ 配置 ============

SCRIPT_DIR = Path(__file__).parent
ARCHIVE_DIR = SCRIPT_DIR / "archive"
REPORTS_DIR = SCRIPT_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# 搜索来源配置
SEARCH_LIMITS = {
    "papers": 5,          # Semantic Scholar 论文数
    "web": 3,             # Web Search 结果数
    "archive_days": 90,   # Archive 回溯天数
}


# ============ Archive 搜索 ============

class ArchiveSearcher:
    """搜索历史日报档案，找到相关动态"""

    def __init__(self, archive_dir: Path = ARCHIVE_DIR):
        self.archive_dir = archive_dir
        self._cache = {}  # 日期 -> articles

    def _load_archive(self, date_str: str) -> List[Dict]:
        """加载指定日期的 JSON 档案"""
        if date_str in self._cache:
            return self._cache[date_str]

        json_path = self.archive_dir / f"news_{date_str}.json"
        if json_path.exists():
            try:
                data = json.loads(json_path.read_text(encoding="utf-8"))
                articles = data.get("articles", [])
                self._cache[date_str] = articles
                return articles
            except (json.JSONDecodeError, KeyError) as e:
                # 跳过损坏的文件
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
                # 检查标题、正文是否包含关键词
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
                            "source": article.get("source", ""),
                            "match_keyword": kw
                        })
                        break

            current += timedelta(days=1)

        # 按日期排序
        results.sort(key=lambda x: x["date"], reverse=True)
        return results[:10]  # 最多返回10条

    def search_by_company(self, company: str, days_back: int = 180) -> List[Dict]:
        """搜索特定公司的历史动态"""
        keywords = [company, company.lower(), company.replace("AI", "").replace(" ", "")]
        return self.search_by_keywords(keywords, days_back)


# ============ 外部搜索封装 ============

class ExternalSearcher:
    """封装外部搜索服务（MCP 工具或直接 API）"""

    def __init__(self):
        self.timeout = 30

    def search_papers(self, query: str, limit: int = 5) -> List[Dict]:
        """搜索学术论文（通过 Semantic Scholar）"""
        # 这里预留 MCP 工具接口
        # 暂时返回占位符
        return [{
            "source": "Semantic Scholar",
            "query": query,
            "note": "需集成 MCP semantic-scholar 工具"
        }]

    def search_web(self, query: str, limit: int = 3) -> List[Dict]:
        """Web 搜索（通过 web-search 或直接 API）"""
        # 这里预留 MCP 工具接口
        return [{
            "source": "Web Search",
            "query": query,
            "note": "需集成 MCP web-search 工具"
        }]


# ============ 问题生成器 ============

class QuestionGenerator:
    """基于动态生成关键研究问题"""

    def __init__(self):
        pass

    def generate_questions(self, topic: str, category: str,
                          context: str, entities: Dict) -> List[Dict]:
        """
        生成关键研究问题

        返回格式:
        [
            {
                "question": "...",
                "type": "technical|company|market|timeline",
                "sources": ["archive", "papers", "web"]  # 推荐搜索源
            }
        ]
        """

        questions = []

        # 1. 基础事实类问题（优先用 archive）
        if category in ["模型前沿", "研究关注"]:
            questions.append({
                "question": f"{topic} 的技术原理是什么？有什么核心创新点？",
                "type": "technical",
                "sources": ["papers", "web"]
            })
            questions.append({
                "question": f"{topic} 与现有方案（如前代产品/竞品）相比有什么优势？",
                "type": "technical",
                "sources": ["papers", "web"]
            })

        # 2. 公司/产品类问题
        companies = entities.get("companies", [])
        if companies:
            for company in companies[:2]:  # 最多2个公司
                questions.append({
                    "question": f"{company} 之前有哪些相关产品/发布？发展历程如何？",
                    "type": "company",
                    "sources": ["archive"]
                })
                questions.append({
                    "question": f"{company} 的主要竞争对手是谁？",
                    "type": "market",
                    "sources": ["web", "archive"]
                })

        # 3. 市场格局类
        if category in ["初创&融资", "产业动态"]:
            questions.append({
                "question": f"这个赛道有哪些主要玩家？市场格局如何？",
                "type": "market",
                "sources": ["archive", "web"]
            })

        # 4. 历史对比类
        products = entities.get("products", [])
        if products:
            for product in products[:2]:
                questions.append({
                    "question": f"{product} 之前有过哪些版本/更新？",
                    "type": "timeline",
                    "sources": ["archive"]
                })

        # 5. 融资/估值类
        if "融资" in category or "估值" in topic or "IPO" in topic:
            questions.append({
                "question": f"相关的融资历史、估值变化是怎样的？",
                "type": "company",
                "sources": ["archive", "web"]
            })

        return questions


# ============ 联邦搜索主类 ============

class FederatedSearch:
    """联邦搜索：协调多个数据源"""

    def __init__(self):
        self.archive = ArchiveSearcher()
        self.external = ExternalSearcher()
        self.question_gen = QuestionGenerator()

    def research(self, topic: str, category: str, context: str,
                 entities: Dict, existing_data: Dict = None) -> Dict[str, Any]:
        """
        执行联邦搜索研究

        Args:
            topic: 研究主题
            category: 分类
            context: 现有上下文（日报的 body + insight）
            entities: 提取的实体
            existing_data: 已有的数据（从 JSON 复用）

        Returns:
            {
                "questions": [...],
                "results": {
                    "archive": [...],
                    "papers": [...],
                    "web": [...]
                },
                "summary": "搜索结果摘要"
            }
        """

        # 复用已有数据
        reused = {
            "from_daily_report": {
                "body": existing_data.get("body", "") if existing_data else "",
                "insight": existing_data.get("insight", "") if existing_data else "",
                "link": existing_data.get("link", "") if existing_data else "",
            }
        }

        # 生成问题
        questions = self.question_gen.generate_questions(
            topic, category, context, entities
        )

        # 收集所有搜索关键词
        search_keywords = []
        search_keywords.extend(entities.get("companies", [])[:2])
        search_keywords.extend(entities.get("products", [])[:2])
        search_keywords.extend(entities.get("people", [])[:1])

        # 添加主题中的关键词
        topic_words = re.findall(r'[\w\u4e00-\u9fff]{2,}', topic)
        search_keywords.extend(topic_words[:3])

        # 去重
        search_keywords = list(set(search_keywords))

        # 执行搜索
        results = {
            "archive": [],
            "papers": [],
            "web": []
        }

        # 1. Archive 搜索（历史动态）
        if any("archive" in q.get("sources", []) for q in questions):
            print("  → 搜索历史日报档案...")
            archive_results = self.archive.search_by_keywords(
                search_keywords,
                days_back=SEARCH_LIMITS["archive_days"]
            )
            results["archive"] = archive_results
            if archive_results:
                print(f"    找到 {len(archive_results)} 条相关历史动态")

        # 2. 论文搜索（技术类问题）
        if any("papers" in q.get("sources", []) for q in questions):
            print("  → 搜索学术论文...")
            # 构建查询
            query = " ".join(search_keywords[:3])
            paper_results = self.external.search_papers(
                query,
                limit=SEARCH_LIMITS["papers"]
            )
            results["papers"] = paper_results

        # 3. Web 搜索（市场/公司类问题）
        if any("web" in q.get("sources", []) for q in questions):
            print("  → 搜索 Web 资源...")
            query = " ".join(search_keywords[:3])
            web_results = self.external.search_web(
                query,
                limit=SEARCH_LIMITS["web"]
            )
            results["web"] = web_results

        # 生成搜索结果摘要
        summary = self._summarize_results(questions, results, reused)

        return {
            "questions": questions,
            "results": results,
            "reused": reused,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }

    def _summarize_results(self, questions: List[Dict],
                          results: Dict, reused: Dict) -> str:
        """生成搜索结果摘要"""
        parts = []

        # 复用数据
        if reused["from_daily_report"]["body"]:
            parts.append("## 已有信息（来自日报）")
            parts.append(f"- 核心事实: {reused['from_daily_report']['body'][:200]}...")
            if reused["from_daily_report"]["insight"]:
                parts.append(f"- 初步判断: {reused['from_daily_report']['insight'][:150]}...")

        # Archive 结果
        if results["archive"]:
            parts.append(f"\n## 历史动态（过去{SEARCH_LIMITS['archive_days']}天）")
            for item in results["archive"][:5]:
                parts.append(f"- **{item['date']}**: {item['title'][:60]}...")

        # 论文结果
        if results["papers"] and not results["papers"][0].get("note"):
            parts.append(f"\n## 相关论文")
            for paper in results["papers"][:3]:
                parts.append(f"- {paper.get('title', 'N/A')}")

        # Web 结果
        if results["web"] and not results["web"][0].get("note"):
            parts.append(f"\n## Web 资源")
            for web in results["web"][:3]:
                parts.append(f"- {web.get('title', web.get('url', 'N/A'))}")

        return "\n".join(parts)


# ============ 测试 ============

if __name__ == "__main__":
    # 测试代码
    searcher = FederatedSearch()

    # 模拟一个研究请求
    topic = "快手计划分拆可灵AI融资20亿美元，估值200亿美元"
    category = "初创&融资"
    context = "快手计划分拆可灵AI，估值200亿美元，融资20亿美元..."
    entities = {
        "companies": ["快手", "可灵AI", "腾讯"],
        "products": ["可灵", "Kling"],
        "people": []
    }
    existing_data = {
        "body": "快手计划分拆旗下视频生成大模型业务可灵AI，以200亿美元估值融资20亿美元...",
        "insight": "可灵分拆估值200亿美元超过快手整体市值，视频生成AI已独立形成资本认可赛道",
        "link": "https://mp.weixin.qq.com/s/xxx"
    }

    print("=" * 60)
    print("联邦搜索测试")
    print("=" * 60)

    result = searcher.research(topic, category, context, entities, existing_data)

    print("\n" + "=" * 60)
    print("搜索结果摘要")
    print("=" * 60)
    print(result["summary"])
