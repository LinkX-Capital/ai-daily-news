#!/usr/bin/env python3
"""
初始化知识图谱 - 添加预设实体关系
"""

from knowledge import Knowledge, Entity, EntityType, RelationType, Track
from datetime import datetime


def initialize_relations():
    """初始化预设关系"""
    knowledge = Knowledge()

    # 添加一些竞争关系
    # 视频生成赛道
    knowledge.graph.add_relation("kling", "runway", RelationType.COMPETES, 0.9, "视频生成赛道竞争")
    knowledge.graph.add_relation("kling", "sora", RelationType.COMPETES, 0.8, "视频生成能力对标")
    knowledge.graph.add_relation("kling", "pika", RelationType.COMPETES, 0.7, "视频生成赛道")
    knowledge.graph.add_relation("runway", "lumalabs", RelationType.COMPETES, 0.8, "3D/视频生成竞争")

    # 模型公司竞争
    knowledge.graph.add_relation("openai", "anthropic", RelationType.COMPETES, 0.9, "LLM 竞争")
    knowledge.graph.add_relation("openai", "google", RelationType.COMPETES, 0.8, "模型能力竞争")
    knowledge.graph.add_relation("anthropic", "google", RelationType.COMPETES, 0.7, "企业级 AI 市场竞争")
    knowledge.graph.add_relation("deepseek", "minimax", RelationType.COMPETES, 0.8, "开源模型竞争")

    # 合作关系
    knowledge.graph.add_relation("nvidia", "google", RelationType.COLLABORATES, 0.7, "GPU 优化合作")
    knowledge.graph.add_relation("nvidia", "vllm", RelationType.COLLABORATES, 0.9, "推理优化合作")

    # 投资关系
    knowledge.graph.add_relation("alphabet", "anthropic", RelationType.INVESTS_IN, 1.0, "Google 投资 Anthropic")

    # 保存
    knowledge.graph.save()

    print("✓ 已初始化预设关系")
    print(f"  实体数: {len(knowledge.graph.entities)}")
    print(f"  关系数: {len(knowledge.graph.relations)}")


if __name__ == "__main__":
    initialize_relations()
    knowledge = Knowledge()
    print("\n## 更新后的图谱摘要")
    print(knowledge.summary())
