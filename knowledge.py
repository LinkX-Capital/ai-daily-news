#!/usr/bin/env python3
"""
Knowledge Agent - 竞品图谱与知识管理

功能：
1. 实体管理（公司、产品、人物）
2. 关系管理（竞争、合作、投资、供应链）
3. 赛道分类与查询
4. 从历史数据中学习/更新图谱
5. 竞品对比分析

Usage:
    knowledge = Knowledge()
    knowledge.get_competitors("可灵AI")
    knowledge.add_relation("可灵AI", "Runway", "competes")
"""

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Set, Any
from enum import Enum
from pathlib import Path


# ============ 数据结构 ============

class EntityType(Enum):
    """实体类型"""
    COMPANY = "company"
    PRODUCT = "product"
    PERSON = "person"
    INVESTOR = "investor"


class RelationType(Enum):
    """关系类型"""
    COMPETES = "competes"       # 竞争
    COLLABORATES = "collaborates" # 合作
    INVESTS_IN = "invests_in"    # 投资
    ACQUIRED = "acquired"        # 收购
    SUPPLIES = "supplies"        # 供应链
    PARTNERS = "partners"        # 合作伙伴
    SAME_PARENT = "same_parent"  # 同母公司
    TECHNOLOGY_DERIVED = "technology_derived"  # 技术衍生


class Track(Enum):
    """赛道分类"""
    L1_COMPUTE = "L1-计算范式"
    L2_MODEL = "L2-模型架构"
    L3_INFRA = "L3-AI Infra"
    L4_APPLICATION = "L4-应用Agent"
    UNKNOWN = "未分类"


@dataclass
class Entity:
    """实体（公司/产品/人物）"""
    id: str                    # 唯一标识
    name: str                  # 名称
    type: EntityType           # 类型
    aliases: List[str] = field(default_factory=list)  # 别名
    track: Track = Track.UNKNOWN
    description: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)
    tags: Set[str] = field(default_factory=set)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, Entity):
            return self.id == other.id
        return False


@dataclass
class Relation:
    """关系"""
    source: str               # 源实体ID
    target: str               # 目标实体ID
    type: RelationType       # 关系类型
    strength: float = 1.0     # 关系强度（0-1）
    evidence: str = ""         # 证据/来源
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


# ============ 知识图谱存储 ============

class KnowledgeGraph:
    """知识图谱存储"""

    def __init__(self, data_file: Path = None):
        self.data_file = data_file or Path(__file__).parent / "knowledge_graph.json"
        self.entities: Dict[str, Entity] = {}
        self.relations: List[Relation] = []

        # 加载数据
        self._load()

    def _load(self):
        """从文件加载图谱数据"""
        if self.data_file.exists():
            try:
                data = json.loads(self.data_file.read_text(encoding="utf-8"))

                # 加载实体
                for entity_data in data.get("entities", []):
                    entity = Entity(
                        id=entity_data["id"],
                        name=entity_data["name"],
                        type=EntityType(entity_data["type"]),
                        aliases=entity_data.get("aliases", []),
                        track=Track(entity_data.get("track", "unknown")),
                        description=entity_data.get("description", ""),
                        attributes=entity_data.get("attributes", {}),
                        tags=set(entity_data.get("tags", []))
                    )
                    self.entities[entity.id] = entity

                # 加载关系
                for rel_data in data.get("relations", []):
                    relation = Relation(
                        source=rel_data["source"],
                        target=rel_data["target"],
                        type=RelationType(rel_data["type"]),
                        strength=rel_data.get("strength", 1.0),
                        evidence=rel_data.get("evidence", ""),
                        timestamp=rel_data.get("timestamp", "")
                    )
                    self.relations.append(relation)

                print(f"✓ 已加载 {len(self.entities)} 个实体, {len(self.relations)} 条关系")
            except Exception as e:
                print(f"⚠️ 加载知识图谱失败: {e}")

    def save(self):
        """保存图谱到文件"""
        data = {
            "entities": [
                {
                    "id": e.id,
                    "name": e.name,
                    "type": e.type.value,
                    "aliases": e.aliases,
                    "track": e.track.value,
                    "description": e.description,
                    "attributes": e.attributes,
                    "tags": list(e.tags),
                    "last_updated": e.attributes.get("last_updated", "")
                }
                for e in self.entities.values()
            ],
            "relations": [
                {
                    "source": r.source,
                    "target": r.target,
                    "type": r.type.value,
                    "strength": r.strength,
                    "evidence": r.evidence,
                    "timestamp": r.timestamp
                }
                for r in self.relations
            ],
            "last_updated": datetime.now().isoformat()
        }

        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.data_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # ============ 实体管理 ============

    def add_entity(self, entity: Entity) -> Entity:
        """添加或更新实体"""
        if entity.id in self.entities:
            # 更新现有实体
            existing = self.entities[entity.id]
            existing.name = entity.name or existing.name
            existing.type = entity.type or existing.type
            existing.aliases = list(set(existing.aliases + entity.aliases))
            existing.track = entity.track if entity.track != Track.UNKNOWN else existing.track
            existing.description = entity.description or existing.description
            existing.attributes.update(entity.attributes)
            existing.tags.update(entity.tags)
            return existing
        else:
            self.entities[entity.id] = entity
            return entity

    def get_entity(self, entity_id: str) -> Optional[Entity]:
        """获取实体"""
        return self.entities.get(entity_id)

    def get_entity_by_name(self, name: str) -> Optional[Entity]:
        """通过名称获取实体（支持别名匹配）"""
        # 精确匹配
        for entity in self.entities.values():
            if entity.name == name:
                return entity
            if name in entity.aliases:
                return entity
        # 模糊匹配
        name_lower = name.lower()
        for entity in self.entities.values():
            if name_lower in entity.name.lower():
                return entity
            for alias in entity.aliases:
                if name_lower in alias.lower():
                    return entity
        return None

    def search_entities(self, keyword: str, track: Track = None) -> List[Entity]:
        """搜索实体"""
        keyword_lower = keyword.lower()
        results = []
        for entity in self.entities.values():
            if track and entity.track != track:
                continue
            if (keyword_lower in entity.name.lower() or
                any(keyword_lower in alias.lower() for alias in entity.aliases) or
                keyword_lower in entity.description.lower()):
                results.append(entity)
        return results

    # ============ 关系管理 ============

    def add_relation(self, source: str, target: str,
                    type: RelationType, strength: float = 1.0,
                    evidence: str = ""):
        """添加关系"""
        # 检查关系是否已存在
        for rel in self.relations:
            if rel.source == source and rel.target == target and rel.type == type:
                # 更新强度
                rel.strength = max(rel.strength, strength)
                rel.evidence = evidence or rel.evidence
                return

        # 添加新关系
        self.relations.append(Relation(
            source=source,
            target=target,
            type=type,
            strength=strength,
            evidence=evidence
        ))

    def get_relations(self, entity_id: str,
                     relation_type: RelationType = None) -> List[Relation]:
        """获取实体的关系"""
        results = []
        for rel in self.relations:
            if rel.source == entity_id:
                if relation_type is None or rel.type == relation_type:
                    results.append(rel)
            elif rel.target == entity_id:
                if relation_type is None or rel.type == relation_type:
                    results.append(rel)
        return results

    def get_competitors(self, entity_id: str) -> List[Entity]:
        """获取竞争对手"""
        competitors = set()

        for rel in self.relations:
            if rel.type == RelationType.COMPETES:
                if rel.source == entity_id:
                    target = self.entities.get(rel.target)
                    if target:
                        competitors.add(target)
                elif rel.target == entity_id:
                    source = self.entities.get(rel.source)
                    if source:
                        competitors.add(source)

        return list(competitors)

    def get_partners(self, entity_id: str) -> List[Entity]:
        """获取合作伙伴"""
        partners = []

        for rel in self.relations:
            if rel.type == RelationType.COLLABORATES or rel.type == RelationType.PARTNERS:
                if rel.source == entity_id:
                    target = self.entities.get(rel.target)
                    if target:
                        partners.append(target)
                elif rel.target == entity_id:
                    source = self.entities.get(rel.source)
                    if source:
                        partners.append(source)

        return partners

    # ============ 赛道查询 ============

    def get_track_entities(self, track: Track) -> List[Entity]:
        """获取赛道内所有实体"""
        return [e for e in self.entities.values() if e.track == track]

    def classify_track(self, entity_name: str,
                    description: str = "") -> Track:
        """根据名称和描述分类赛道"""
        name_lower = entity_name.lower()
        desc_lower = description.lower()
        combined = name_lower + " " + desc_lower

        # L1-计算范式
        if any(kw in combined for kw in ["芯片", "量子", "核聚变", "semiconductor",
                                          "hardware", "compute", "算力"]):
            return Track.L1_COMPUTE

        # L2-模型架构
        if any(kw in combined for kw in ["大模型", "llm", "语言模型", "多模态",
                                          "transformer", "diffusion", "训练"]):
            return Track.L2_MODEL

        # L3-AI Infra
        if any(kw in combined for kw in ["推理", "推理加速", "部署", "框架",
                                          "infrastructure", "cloud"]):
            return Track.L3_INFRA

        # L4-应用Agent
        if any(kw in combined for kw in ["agent", "应用", "产品", "商业化",
                                          "视频生成", "机器人", "具身"]):
            return Track.L4_APPLICATION

        return Track.UNKNOWN

    # ============ 学习更新 ============

    def learn_from_news(self, news_articles: List[Dict]):
        """从新闻文章中学习更新图谱"""
        for article in news_articles:
            title = article.get("title", "")
            body = article.get("body", "")
            context = title + " " + body

            # 提取实体和关系
            entities = self._extract_entities_from_text(context)
            relations = self._extract_relations_from_text(context, entities)

            # 更新图谱
            for entity in entities:
                self.add_entity(entity)

            for relation in relations:
                self.add_relation(**relation)

        # 保存更新
        self.save()

    def _extract_entities_from_names(self) -> List[Entity]:
        """从预设名称列表初始化实体"""
        # 视频生成公司
        video_gen_companies = [
            ("kling", "可灵AI", EntityType.COMPANY, Track.L4_APPLICATION, "快手旗下视频生成"),
            ("kling_omni", "Kling Omni", EntityType.PRODUCT, Track.L4_APPLICATION, "可灵AI高级版"),
            ("runway", "Runway", EntityType.COMPANY, Track.L4_APPLICATION, "美国视频生成，Gen-3 Alpha"),
            ("gen3", "Gen-3 Alpha", EntityType.PRODUCT, Track.L4_APPLICATION, "Runway产品"),
            ("lumalabs", "Luma AI", EntityType.COMPANY, Track.L4_APPLICATION, "视频生成/3D"),
            ("pika", "Pika Labs", EntityType.COMPANY, Track.L4_APPLICATION, "视频生成"),
            ("sora", "Sora", EntityType.PRODUCT, Track.L2_MODEL, "OpenAI视频生成"),
            ("sv3d", "Stable Video Diffusion", EntityType.PRODUCT, Track.L4_APPLICATION, "Stability AI"),
            ("vidu", "Vidu", EntityType.PRODUCT, Track.L4_APPLICATION, "生数科技视频生成"),
        ]

        # 模型公司
        model_companies = [
            ("openai", "OpenAI", EntityType.COMPANY, Track.L2_MODEL, "ChatGPT/GPT系列"),
            ("anthropic", "Anthropic", EntityType.COMPANY, Track.L2_MODEL, "Claude系列"),
            ("google", "Google DeepMind", EntityType.COMPANY, Track.L2_MODEL, "Gemini系列"),
            ("deepseek", "DeepSeek", EntityType.COMPANY, Track.L2_MODEL, "DeepSeek系列"),
            ("minimax", "MiniMax", EntityType.COMPANY, Track.L2_MODEL, "abab系列"),
            ("moonshot", "月之暗面", EntityType.COMPANY, Track.L2_MODEL, "Kimi"),
        ]

        # Infra公司
        infra_companies = [
            ("nvidia", "NVIDIA", EntityType.COMPANY, Track.L1_COMPUTE, "GPU芯片"),
            ("vllm", "vLLM", EntityType.PRODUCT, Track.L3_INFRA, "推理优化框架"),
            ("tensorrt", "TensorRT", EntityType.PRODUCT, Track.L3_INFRA, "推理加速"),
        ]

        entities = []
        for data in video_gen_companies + model_companies + infra_companies:
            entities.append(Entity(
                id=data[0],
                name=data[1],
                type=data[2],
                track=data[3],
                description=data[4]
            ))

        return entities

    def _extract_entities_from_text(self, text: str) -> List[Entity]:
        """从文本中提取实体"""
        entities = []

        # 简化实现：从已知实体中匹配
        for entity in self.entities.values():
            if entity.name in text or any(alias in text for alias in entity.aliases):
                entities.append(entity)

        return entities

    def _extract_relations_from_text(self, text: str,
                                   entities: List[Entity]) -> List[Dict]:
        """从文本中提取关系"""
        relations = []

        # 竞争关系关键词
        compete_patterns = [
            (r"(.+?)\s*(?:超越|击败|优于|超过|领先于)\s*(.+?)", "超越"),
            (r"(.+?)\s*(?:对标|对比|对比)\s*(.+?)", "对标"),
        ]

        # 合作关系关键词
        collab_patterns = [
            (r"(.+?)\s*(?:合作|联合|联手|共同)\s*(.+?)", "合作"),
            (r"(.+?)\s*(?:投资|领投|参投)\s*(.+?)", "投资"),
        ]

        # 简化实现：如果文本中提到"公司A vs 公司B"
        if len(entities) >= 2:
            for i in range(len(entities) - 1):
                for j in range(i + 1, len(entities)):
                    e1, e2 = entities[i], entities[j]

                    # 检查是否在文本中一起出现
                    if e1.name in text and e2.name in text:
                        # 判断关系类型
                        for pattern, rel_type_key in compete_patterns:
                            matches = re.findall(pattern, text)
                            for match in matches:
                                if e1.name in match or e2.name in match:
                                    relations.append({
                                        "source": e1.id,
                                        "target": e2.id,
                                        "type": RelationType.COMPETES,
                                        "evidence": f"从新闻提取: {match[:50]}"
                                    })

                        for pattern, rel_type_key in collab_patterns:
                            matches = re.findall(pattern, text)
                            for match in matches:
                                if e1.name in match or e2.name in match:
                                    rel_type = RelationType.COLLABORATES
                                    if "投资" in match:
                                        rel_type = RelationType.INVESTS_IN
                                    relations.append({
                                        "source": e1.id,
                                        "target": e2.id,
                                        "type": rel_type,
                                        "evidence": f"从新闻提取: {match[:50]}"
                                    })

        return relations

    # ============ 对比分析 ============

    def compare_entities(self, entity_ids: List[str]) -> Dict[str, Any]:
        """对比多个实体"""
        entities = [self.get_entity(eid) for eid in entity_ids]
        entities = [e for e in entities if e]

        if len(entities) < 2:
            return {"error": "至少需要2个实体进行对比"}

        # 收集赛道、标签等信息
        tracks = {}
        attributes_comparison = {}

        for entity in entities:
            tracks[entity.name] = entity.track.value
            attributes_comparison[entity.name] = entity.attributes

        # 查找关系
        relations_matrix = {}
        for i, e1 in enumerate(entities):
            relations_matrix[e1.name] = {}
            for e2 in entities:
                if e1 == e2:
                    relations_matrix[e1.name][e2.name] = "self"
                else:
                    # 检查是否存在关系
                    has_relation = False
                    for rel in self.relations:
                        if ((rel.source == e1.id and rel.target == e2.id) or
                            (rel.source == e2.id and rel.target == e1.id)):
                            relations_matrix[e1.name][e2.name] = rel.type.value
                            has_relation = True
                            break
                    if not has_relation:
                        relations_matrix[e1.name][e2.name] = "unknown"

        return {
            "entities": [
                {
                    "id": e.id,
                    "name": e.name,
                    "type": e.type.value,
                    "track": e.track.value,
                    "description": e.description,
                    "tags": list(e.tags)
                }
                for e in entities
            ],
            "tracks": tracks,
            "attributes_comparison": attributes_comparison,
            "relations": relations_matrix
        }

    def get_summary(self) -> str:
        """获取图谱摘要"""
        lines = [
            "## 知识图谱摘要",
            f"",
            f"**实体总数**: {len(self.entities)}",
            f"**关系总数**: {len(self.relations)}",
            f"",
            f"### 按赛道分类",
            f""
        ]

        # 按赛道统计
        track_counts = {}
        for entity in self.entities.values():
            track_counts[entity.track.value] = track_counts.get(entity.track.value, 0) + 1

        for track, count in sorted(track_counts.items()):
            lines.append(f"- **{track}**: {count}")

        lines.append(f"")
        lines.append(f"### 关系类型统计")
        lines.append(f"")

        # 按关系类型统计
        relation_counts = {}
        for rel in self.relations:
            relation_counts[rel.type.value] = relation_counts.get(rel.type.value, 0) + 1

        for rel_type, count in sorted(relation_counts.items()):
            lines.append(f"- **{rel_type}**: {count}")

        return "\n".join(lines)


# ============ Knowledge Agent 主类 ============

class Knowledge:
    """Knowledge Agent - 知识图谱管理代理"""

    def __init__(self, data_file: Path = None):
        self.graph = KnowledgeGraph(data_file)

        # 初始化预设数据
        if not self.graph.entities:
            print("初始化预设实体...")
            entities = self.graph._extract_entities_from_names()
            for entity in entities:
                self.graph.add_entity(entity)
            self.graph.save()
            print(f"✓ 初始化 {len(entities)} 个预设实体")

    # ============ 查询接口 ============

    def get_competitors(self, entity_name: str) -> List[Dict]:
        """获取竞争对手"""
        entity = self.graph.get_entity_by_name(entity_name)
        if not entity:
            return []

        competitors = self.graph.get_competitors(entity.id)

        return [
            {
                "name": c.name,
                "id": c.id,
                "track": c.track.value,
                "description": c.description
            }
            for c in competitors
        ]

    def get_track_info(self, track_name: str) -> Dict[str, Any]:
        """获取赛道信息"""
        # 尝试匹配赛道
        track = None
        for t in Track:
            if t.value.lower() == track_name.lower() or track_name in t.value:
                track = t
                break

        if not track:
            track = Track.UNKNOWN

        entities = self.graph.get_track_entities(track)

        return {
            "track": track.value,
            "entity_count": len(entities),
            "entities": [
                {
                    "name": e.name,
                    "id": e.id,
                    "description": e.description
                }
                for e in entities
            ]
        }

    def compare(self, names: List[str]) -> str:
        """对比多个实体，生成对比报告"""
        entity_ids = []
        for name in names:
            entity = self.graph.get_entity_by_name(name)
            if entity:
                entity_ids.append(entity.id)

        if len(entity_ids) < 2:
            return "错误：找不到足够的实体进行对比"

        comparison = self.graph.compare_entities(entity_ids)

        # 生成报告
        lines = [
            f"## 竞品对比分析",
            f"",
            f"### 实体概览"
        ]

        for entity_info in comparison["entities"]:
            lines.append(f"- **{entity_info['name']}** ({entity_info['track']})")

        lines.append("")
        lines.append(f"### 关系网络")
        lines.append("")

        relations = comparison["relations"]
        for e1_name, relations_map in relations.items():
            for e2_name, relation in relations_map.items():
                if relation != "unknown" and relation != "self":
                    lines.append(f"- {e1_name} → {e2_name}: {relation}")

        return "\n".join(lines)

    def update_from_news(self, date_str: str = None, days_back: int = 7):
        """从历史新闻更新图谱"""
        from archive_searcher import ArchiveSearcher

        searcher = ArchiveSearcher()

        # 获取日期范围
        from datetime import timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        if date_str:
            # 只加载指定日期
            articles = searcher._load_archive(date_str)
        else:
            # 加载多日数据
            articles = []
            current = start_date
            while current <= end_date:
                date_str_n = current.strftime("%Y-%m-%d")
                articles.extend(searcher._load_archive(date_str_n))
                current += timedelta(days=1)

        print(f"从 {len(articles)} 篇文章中学习...")

        # 学习更新
        self.graph.learn_from_news(articles)

        print(f"✓ 图谱已更新")

    def save(self):
        """保存图谱"""
        self.graph.save()

    def summary(self) -> str:
        """获取知识图谱摘要"""
        return self.graph.get_summary()


# ============ CLI ============

if __name__ == "__main__":
    import sys

    knowledge = Knowledge()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "competitors":
            if len(sys.argv) > 2:
                entity_name = sys.argv[2]
                competitors = knowledge.get_competitors(entity_name)
                print(f"\n## {entity_name} 的竞争对手\n")
                if competitors:
                    for c in competitors:
                        print(f"- **{c['name']}** ({c['track']})")
                else:
                    print("未找到竞争对手")
            else:
                print("用法: python knowledge.py competitors <公司名>")

        elif command == "track":
            if len(sys.argv) > 2:
                track_name = sys.argv[2]
                info = knowledge.get_track_info(track_name)
                print(f"\n## {info['track']} 赛道\n")
                print(f"实体数量: {info['entity_count']}")
                print("\n主要实体:")
                for e in info['entities'][:10]:
                    print(f"- **{e['name']}**: {e.get('description', 'N/A')}")
            else:
                # 列出所有赛道
                print("\n## 可用赛道\n")
                for track in Track:
                    if track != Track.UNKNOWN:
                        entities = knowledge.graph.get_track_entities(track)
                        print(f"- {track.value}: {len(entities)} 个实体")

        elif command == "compare":
            if len(sys.argv) > 2:
                names = sys.argv[2:]
                report = knowledge.compare(names)
                print(report)
            else:
                print("用法: python knowledge.py compare <实体1> <实体2> ...")

        elif command == "update":
            days_back = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            knowledge.update_from_news(days_back=days_back)

        elif command == "summary":
            print(knowledge.summary())

        else:
            print("未知命令")
    else:
        # 交互模式演示
        print("""
== Knowledge Agent 交互演示 ==

可用命令:
  python knowledge.py competitors <公司名>
  python knowledge.py track <赛道名>
  python knowledge.py compare <实体1> <实体2> ...
  python knowledge.py update [天数]
  python knowledge.py summary

示例:
  python knowledge.py competitors 可灵AI
  python knowledge.py track L2-模型架构
  python knowledge.py compare 可灵AI Runway Sora
  python knowledge.py update 7
        """)
