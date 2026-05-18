#!/usr/bin/env python3
"""
Planner Agent - 研究问题拆解与规划

负责将研究主题拆解为可执行的子问题，并映射到数据源。

Usage:
    plan = Planner().plan(topic, context, entities)
    print(plan.to_summary())
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


# ============ 主题类型 ============

class TopicType(Enum):
    """研究主题类型"""
    FUNDING = "funding"           # 融资/估值/IPO
    TECH_RELEASE = "tech"         # 技术发布/模型/论文
    PRODUCT = "product"           # 产品更新/功能
    COMPANY = "company"           # 公司动态/人事
    RESEARCH = "research"         # 学术研究/论文
    MARKET = "market"             # 行业/市场分析
    UNKNOWN = "unknown"


# ============ 问题模板 ============

QUESTION_TEMPLATES = {
    TopicType.FUNDING: [
        {
            "id": "f1",
            "question": "{company}的融资历史和估值变化是怎样的？",
            "type": "company_history",
            "sources": ["archive", "web"],
            "priority": "high"
        },
        {
            "id": "f2",
            "question": "{amount}估值在{赛道}中处于什么水平？同赛道公司估值对比？",
            "type": "valuation_benchmark",
            "sources": ["archive", "knowledge", "web"],
            "priority": "high"
        },
        {
            "id": "f3",
            "question": "融资用途是什么？将用于哪些方向？",
            "type": "funding_use",
            "sources": ["source", "web"],
            "priority": "medium"
        },
        {
            "id": "f4",
            "question": "投资方是谁？他们的投资逻辑是什么？",
            "type": "investor_analysis",
            "sources": ["web", "source"],
            "priority": "medium"
        },
        {
            "id": "f5",
            "question": "这次融资对行业格局有什么影响？",
            "type": "industry_impact",
            "sources": ["archive", "web"],
            "priority": "high"
        }
    ],

    TopicType.TECH_RELEASE: [
        {
            "id": "t1",
            "question": "{product}的技术原理是什么？核心创新点在哪里？",
            "type": "tech_principle",
            "sources": ["papers", "source", "web"],
            "priority": "high"
        },
        {
            "id": "t2",
            "question": "与前代产品/竞品相比，{product}有什么优势？",
            "type": "competitive_analysis",
            "sources": ["archive", "web", "knowledge"],
            "priority": "high"
        },
        {
            "id": "t3",
            "question": "技术壁垒是什么？容易复制吗？",
            "type": "tech_barrier",
            "sources": ["papers", "web"],
            "priority": "medium"
        },
        {
            "id": "t4",
            "question": "这个技术的应用场景有哪些？商业化路径？",
            "type": "commercialization",
            "sources": ["web", "source"],
            "priority": "medium"
        }
    ],

    TopicType.PRODUCT: [
        {
            "id": "p1",
            "question": "新功能/新产品的核心特性是什么？解决什么问题？",
            "type": "product_feature",
            "sources": ["source", "web"],
            "priority": "high"
        },
        {
            "id": "p2",
            "question": "目标用户是谁？市场定位如何？",
            "type": "market_positioning",
            "sources": ["web", "source"],
            "priority": "medium"
        },
        {
            "id": "p3",
            "question": "与竞品相比有什么差异化优势？",
            "type": "competitive_diff",
            "sources": ["knowledge", "web"],
            "priority": "high"
        }
    ],

    TopicType.COMPANY: [
        {
            "id": "c1",
            "question": "{company}的发展历程和里程碑是什么？",
            "type": "company_timeline",
            "sources": ["archive", "web"],
            "priority": "high"
        },
        {
            "id": "c2",
            "question": "{company}的核心业务和盈利模式是什么？",
            "type": "business_model",
            "sources": ["web", "source"],
            "priority": "high"
        },
        {
            "id": "c3",
            "question": "这次动态对{company}的战略意义是什么？",
            "type": "strategic_impact",
            "sources": ["web", "archive"],
            "priority": "medium"
        }
    ],

    TopicType.RESEARCH: [
        {
            "id": "r1",
            "question": "论文的核心贡献是什么？解决了什么问题？",
            "type": "paper_contribution",
            "sources": ["papers", "source"],
            "priority": "high"
        },
        {
            "id": "r2",
            "question": "研究方法的创新点在哪里？",
            "type": "methodology",
            "sources": ["papers"],
            "priority": "high"
        },
        {
            "id": "r3",
            "question": "实验结果如何？benchmark 表现？",
            "type": "experimental_results",
            "sources": ["papers", "source"],
            "priority": "high"
        },
        {
            "id": "r4",
            "question": "这个研究的实际应用价值如何？",
            "type": "application_value",
            "sources": ["papers", "web"],
            "priority": "medium"
        }
    ],

    TopicType.MARKET: [
        {
            "id": "m1",
            "question": "这个赛道的市场规模和增长趋势如何？",
            "type": "market_size",
            "sources": ["web", "archive"],
            "priority": "high"
        },
        {
            "id": "m2",
            "question": "主要玩家有哪些？竞争格局如何？",
            "type": "competitive_landscape",
            "sources": ["knowledge", "archive", "web"],
            "priority": "high"
        },
        {
            "id": "m3",
            "question": "行业面临的主要挑战和机遇是什么？",
            "type": "challenges_opportunities",
            "sources": ["web", "archive"],
            "priority": "medium"
        }
    ]
}


# ============ 数据源说明 ============

SOURCE_DESCRIPTIONS = {
    "source": "来源原文（日报提供的链接，抓取全文）",
    "archive": "历史日报（过去90天相关动态）",
    "web": "Web 搜索（最新资讯）",
    "papers": "学术论文（Semantic Scholar）",
    "knowledge": "竞品图谱（手动维护的赛道-公司关系）"
}


# ============ 研究计划 ============

class ResearchQuestion:
    """单个研究问题"""

    def __init__(self, id: str, question: str, type: str,
                 sources: List[str], priority: str):
        self.id = id
        self.question = question
        self.type = type
        self.sources = sources
        self.priority = priority
        self.answer = None  # 执行后的答案
        self.sources_found = {}  # 实际找到的来源

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "question": self.question,
            "type": self.type,
            "sources": self.sources,
            "priority": self.priority,
            "sources_description": [SOURCE_DESCRIPTIONS.get(s, s) for s in self.sources],
            "answer": self.answer,
            "sources_found": self.sources_found
        }


class ResearchPlan:
    """研究计划"""

    def __init__(self, topic: str, topic_type: TopicType,
                 questions: List[ResearchQuestion],
                 entities: Dict = None):
        self.topic = topic
        self.topic_type = topic_type
        self.questions = questions
        self.entities = entities or {}
        self.created_at = datetime.now().isoformat()

    def to_summary(self) -> str:
        """生成计划摘要"""
        lines = [
            f"## 研究计划: {self.topic}",
            f"",
            f"**主题类型**: {self.topic_type.value}",
            f"**问题数量**: {len(self.questions)}",
            f"**预计时间**: {self._estimate_time()} 分钟",
            f"",
            f"### 研究问题",
            f""
        ]

        # 按优先级分组
        high_priority = [q for q in self.questions if q.priority == "high"]
        medium_priority = [q for q in self.questions if q.priority == "medium"]

        if high_priority:
            lines.append("#### 🔴 高优先级")
            for q in high_priority:
                lines.append(f"- [{q.id}] **{q.question}**")
                lines.append(f"  - 数据源: {', '.join(q.sources)}")
                lines.append(f"")

        if medium_priority:
            lines.append("#### 🟡 中优先级")
            for q in medium_priority:
                lines.append(f"- [{q.id}] **{q.question}**")
                lines.append(f"  - 数据源: {', '.join(q.sources)}")
                lines.append(f"")

        return "\n".join(lines)

    def to_dict(self) -> Dict:
        return {
            "topic": self.topic,
            "topic_type": self.topic_type.value,
            "questions": [q.to_dict() for q in self.questions],
            "entities": self.entities,
            "created_at": self.created_at
        }

    def _estimate_time(self) -> int:
        """估算研究时间（分钟）"""
        base_time = len(self.questions) * 2  # 每个问题基础2分钟
        high_extra = len([q for q in self.questions if q.priority == "high"]) * 2
        return base_time + high_extra


# ============ Planner ============

class Planner:
    """问题拆解与规划代理"""

    def __init__(self):
        pass

    def plan(self, topic: str, context: str = "",
             category: str = "", entities: Dict = None) -> ResearchPlan:
        """
        生成研究计划

        Args:
            topic: 研究主题
            context: 已有上下文（日报 body + insight）
            category: 新闻分类
            entities: 已提取的实体

        Returns:
            ResearchPlan: 研究计划
        """
        # 1. 识别主题类型
        topic_type = self._classify_topic_type(topic, context, category)

        # 2. 获取问题模板
        templates = QUESTION_TEMPLATES.get(topic_type, [])

        # 3. 生成具体问题
        questions = self._generate_questions(
            templates, topic, context, entities or {}
        )

        # 4. 去重和过滤
        questions = self._deduplicate_questions(questions, context)

        return ResearchPlan(
            topic=topic,
            topic_type=topic_type,
            questions=questions,
            entities=entities or {}
        )

    def _classify_topic_type(self, topic: str, context: str,
                            category: str) -> TopicType:
        """识别主题类型"""

        text = (topic + " " + context).lower()

        # 关键词匹配
        if any(kw in text for kw in ["融资", "估值", "ipo", "上市", "投资", " funding", "valuation"]):
            return TopicType.FUNDING

        if any(kw in text for kw in ["发布", "推出", "上线", "更新", "版本", "模型", "架构"]):
            if any(kw in text for kw in ["论文", "研究", "iclr", "neurips", "arxiv"]):
                return TopicType.RESEARCH
            if any(kw in text for kw in ["产品", "功能", "应用"]):
                return TopicType.PRODUCT
            return TopicType.TECH_RELEASE

        if any(kw in text for kw in ["公司", "团队", "创立", "ceo", "收购", "合并"]):
            return TopicType.COMPANY

        if category in ["模型前沿", "研究关注"]:
            return TopicType.TECH_RELEASE
        if category in ["初创&融资"]:
            return TopicType.FUNDING
        if category in ["产业动态"]:
            return TopicType.COMPANY

        return TopicType.UNKNOWN

    def _generate_questions(self, templates: List[Dict], topic: str,
                           context: str, entities: Dict) -> List[ResearchQuestion]:
        """基于模板生成具体问题"""

        questions = []

        # 提取占位符值
        company = self._extract_company(entities, topic, context)
        product = self._extract_product(entities, topic, context)
        amount = self._extract_amount(context)
        track = self._extract_track(topic, context)

        for template in templates:
            question_text = template["question"]

            # 填充占位符
            if "{company}" in question_text and company:
                question_text = question_text.replace("{company}", company)
            elif "{company}" in question_text:
                question_text = question_text.replace("{company}", "该公司")

            if "{product}" in question_text and product:
                question_text = question_text.replace("{product}", product)
            elif "{product}" in question_text:
                question_text = question_text.replace("{product}", "该产品")

            if "{amount}" in question_text and amount:
                question_text = question_text.replace("{amount}", amount)
            elif "{amount}" in question_text:
                question_text = question_text.replace("{amount}", "此")

            if "{赛道}" in question_text and track:
                question_text = question_text.replace("{赛道}", track)
            elif "{赛道}" in question_text:
                question_text = question_text.replace("{赛道}", "相关赛道")

            # 跳过无法填充的问题
            if any(kw in question_text for kw in ["{company}", "{product}", "{amount}"]):
                continue

            questions.append(ResearchQuestion(
                id=template["id"],
                question=question_text,
                type=template["type"],
                sources=template["sources"],
                priority=template["priority"]
            ))

        return questions

    def _extract_company(self, entities: Dict, topic: str, context: str) -> Optional[str]:
        """提取公司名"""
        companies = entities.get("companies", [])
        if companies:
            return companies[0]
        # 简单从 topic 提取
        match = re.search(r'([A-Z][a-z]+|[\\u4e00-\\u9fff]{2,4})公司|([A-Z][a-z]+)实验室', topic)
        if match:
            return match.group(1) or match.group(2)
        return None

    def _extract_product(self, entities: Dict, topic: str, context: str) -> Optional[str]:
        """提取产品名"""
        products = entities.get("products", [])
        if products:
            return products[0]
        return None

    def _extract_amount(self, context: str) -> Optional[str]:
        """提取金额"""
        match = re.search(r'(\d+(?:\.\d+)?[亿美元万亿]+)', context)
        if match:
            return match.group(1)
        return None

    def _extract_track(self, topic: str, context: str) -> Optional[str]:
        """提取赛道"""
        tracks = {
            "视频生成": "视频生成", "多模态": "多模态", "大模型": "大模型",
            "Agent": "Agent", "机器人": "具身智能", "推理": "推理优化"
        }
        text = topic + " " + context
        for kw, name in tracks.items():
            if kw.lower() in text.lower():
                return name
        return "相关"

    def _deduplicate_questions(self, questions: List[ResearchQuestion],
                              context: str) -> List[ResearchQuestion]:
        """去重：移除与已有信息重复的问题"""

        # 如果 context 中已经包含了答案，就跳过这个问题
        filtered = []
        for q in questions:
            # 简单判断：如果 context 足够长，保留所有问题
            # 实际可以用更复杂的语义匹配
            filtered.append(q)

        return filtered

    def refine_plan(self, plan: ResearchPlan, feedback: str) -> ResearchPlan:
        """根据反馈调整计划"""
        # TODO: 实现基于反馈的调整逻辑
        return plan


# ============ 测试 ============

if __name__ == "__main__":
    planner = Planner()

    # 测试用例
    test_cases = [
        {
            "topic": "快手计划分拆可灵AI融资20亿美元，估值200亿美元",
            "context": "快手计划分拆旗下视频生成大模型业务可灵AI，以200亿美元估值融资20亿美元...",
            "category": "初创&融资",
            "entities": {
                "companies": ["快手", "可灵AI"],
                "products": ["可灵", "Kling"]
            }
        },
        {
            "topic": "PRISM框架用分层决策替代Best-of-N",
            "context": "PRISM框架提出用分层决策架构替代传统Best-of-N搜索...",
            "category": "研究关注",
            "entities": {
                "products": ["PRISM"],
                "companies": []
            }
        }
    ]

    for i, tc in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"测试用例 {i}")
        print(f"{'='*60}")

        plan = planner.plan(
            topic=tc["topic"],
            context=tc["context"],
            category=tc["category"],
            entities=tc["entities"]
        )

        print(plan.to_summary())
