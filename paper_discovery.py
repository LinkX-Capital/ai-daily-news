#!/usr/bin/env python3
"""
arXiv 每日论文发现脚本

从 arXiv RSS/API 抓取最近 N 天内的新论文，按关键词筛选高价值研究，
输出 markdown 清单供日报研究关注栏目使用。

数据源：arXiv API（免费，无需 API key，无严格限频）
覆盖分类：cs.CL, cs.LG, cs.AI, cs.CV, stat.ML

用法：
  python3 paper_discovery.py                    # 默认最近 1 个工作日
  python3 paper_discovery.py --days 3            # 最近 3 天
  python3 paper_discovery.py --date 2026-06-05   # 指定截止日期
  python3 paper_discovery.py --top 20            # 每组取 top 20
  python3 paper_discovery.py --all               # 显示全部匹配（不做 top N 截断）

输出：stdout，markdown 格式
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import quote

# ============ 配置 ============

ARXIV_API = "https://export.arxiv.org/api/query"

# 覆盖的 arXiv 分类
CATEGORIES = ["cs.CL", "cs.LG", "cs.AI", "cs.CV", "stat.ML"]

# 筛选关键词组：每组覆盖一个研究方向
# keyword: 标题/摘要中的关键词（不区分大小写，任一匹配即可）
# label: 显示标签
# weight: 权重（1-3，3 为最高优先级）
FILTER_GROUPS = [
    # Agent / 工具使用 / 自主系统
    {"keywords": ["agent", "tool use", "tool-use", "autonomous", "agentic"],
     "label": "Agent & 工具使用", "weight": 3},

    # 推理效率 / 推理优化
    {"keywords": ["reasoning efficiency", "inference optimization", "early exit",
                   "speculative decoding", "token budget", "overthinking"],
     "label": "推理效率", "weight": 3},

    # RLHF / 对齐 / 奖励模型
    {"keywords": ["RLHF", "reward model", "alignment", "preference optimization",
                   "DPO", "GRPO", "PPO", "RLVR"],
     "label": "对齐 & RLHF", "weight": 3},

    # 长上下文 / 记忆 / 注意力
    {"keywords": ["long context", "long-context", "memory mechanism", "KV cache",
                   "attention mechanism", "context window"],
     "label": "长上下文 & 记忆", "weight": 2},

    # 量化 / 蒸馏 / 压缩
    {"keywords": ["quantization", "distillation", "pruning", "compression",
                   "sparse model", "mixture of experts", "MoE"],
     "label": "量化 & 压缩", "weight": 2},

    # 多模态 / 世界模型 / VLA
    {"keywords": ["multimodal", "vision-language", "world model", "VLA",
                   "vision-language-action", "text-to-image", "text-to-video"],
     "label": "多模态 & 世界模型", "weight": 2},

    # 代码生成 / 数学推理
    {"keywords": ["code generation", "code LLM", "mathematical reasoning",
                   "theorem proving", "formal verification"],
     "label": "代码 & 数学推理", "weight": 2},

    # Transformer 架构创新
    {"keywords": ["transformer architecture", "state space model", "SSM",
                   "mamba", "linear attention", "new architecture"],
     "label": "架构创新", "weight": 2},

    # AI for Science
    {"keywords": ["AI for science", "drug discovery", "protein", "material",
                   "scientific discovery", "molecule"],
     "label": "AI for Science", "weight": 2},

    # 训练方法 / Scaling
    {"keywords": ["scaling law", "training recipe", "pre-training",
                   "post-training", "data curation", "synthetic data"],
     "label": "训练方法", "weight": 1},

    # 安全 / 可解释性
    {"keywords": ["mechanistic interpretability", "safety", "jailbreak",
                   "adversarial", "hallucination", "faithfulness"],
     "label": "安全 & 可解释性", "weight": 1},

    # 3D / 机器人
    {"keywords": ["3D generation", "3D reconstruction", "robot", "embodied",
                   "manipulation", "simulation"],
     "label": "3D & 机器人", "weight": 1},
]


def fetch_arxiv_papers(start_date: str, end_date: str, max_per_cat: int = 200) -> list:
    """从 arXiv API 抓取指定日期范围内的论文"""
    all_entries = []
    seen_ids = set()

    for cat in CATEGORIES:
        query = f'cat:{cat} AND submittedDate:[{start_date}0000 TO {end_date}2359]'
        url = f"{ARXIV_API}?search_query={quote(query)}&start=0&max_results={max_per_cat}&sortBy=submittedDate&sortOrder=descending"

        print(f"  📥 {cat} ...", end=" ", file=sys.stderr, flush=True)

        try:
            req = Request(url)
            with urlopen(req, timeout=30) as resp:
                data = resp.read().decode("utf-8")
        except (HTTPError, URLError) as e:
            print(f"❌ {e}", file=sys.stderr)
            continue

        root = ET.fromstring(data)
        ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

        count = 0
        for entry in root.findall("atom:entry", ns):
            # 跳过查询结果条目
            id_elem = entry.find("atom:id", ns)
            if id_elem is None or "/api/" in id_elem.text:
                continue

            arxiv_id = id_elem.text.split("/abs/")[-1].split("v")[0]
            if arxiv_id in seen_ids:
                continue
            seen_ids.add(arxiv_id)

            title = (entry.find("atom:title", ns).text or "").strip().replace("\n", " ")
            summary = (entry.find("atom:summary", ns).text or "").strip().replace("\n", " ")
            published = (entry.find("atom:published", ns).text or "")[:10]

            authors = []
            for author in entry.findall("atom:author", ns):
                name = author.find("atom:name", ns)
                if name is not None:
                    authors.append(name.text)

            categories = [c.get("term", "") for c in entry.findall("atom:category", ns)]

            all_entries.append({
                "arxiv_id": arxiv_id,
                "title": re.sub(r"\s+", " ", title),
                "abstract": re.sub(r"\s+", " ", summary),
                "authors": authors,
                "published": published,
                "categories": categories,
            })
            count += 1

        print(f"{count} 篇", file=sys.stderr)

    return all_entries


def score_paper(paper: dict) -> tuple:
    """对论文打分：返回 (总权重, 匹配组标签列表)
    每篇最多取权重最高的 3 个方向，避免泛泛论文得分虚高
    """
    text = f"{paper['title']} {paper['abstract']}".lower()
    matches = []

    for group in FILTER_GROUPS:
        for kw in group["keywords"]:
            if kw.lower() in text:
                matches.append((group["weight"], group["label"]))
                break  # 每组只匹配一次

    # 按权重降序，取前 3 个方向
    matches.sort(key=lambda x: x[0], reverse=True)
    top_matches = matches[:3]
    total_weight = sum(w for w, _ in top_matches)
    matched_groups = [g for _, g in top_matches]

    return total_weight, matched_groups


def format_authors(authors: list, max_names: int = 3) -> str:
    """格式化作者列表"""
    if not authors:
        return "Unknown"
    names = authors[:max_names]
    suffix = f" et al. ({len(authors)} authors)" if len(authors) > max_names else ""
    return ", ".join(names) + suffix


def main():
    parser = argparse.ArgumentParser(description="arXiv 每日论文发现")
    parser.add_argument("--days", type=int, default=1, help="回溯天数（默认 1）")
    parser.add_argument("--date", type=str, help="指定截止日期 YYYY-MM-DD（默认今天）")
    parser.add_argument("--top", type=int, default=15, help="取 top N 篇（默认 15）")
    parser.add_argument("--all", action="store_true", help="显示全部匹配（不做 top N 截断）")
    parser.add_argument("--min-weight", type=int, default=2, help="最低权重过滤（默认 2）")
    args = parser.parse_args()

    today = datetime.strptime(args.date, "%Y-%m-%d") if args.date else datetime.now()
    # arXiv 提交日期从周一开始到周五，周末无新论文
    # 回溯时加 buffer 确保覆盖到工作日
    start = today - timedelta(days=args.days)
    # 如果今天是周一且只看1天，需要回溯到周五
    if args.days <= 1 and today.weekday() == 0:  # Monday
        start = today - timedelta(days=3)  # 回到周五
    start_date = start.strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")

    print(f"📅 搜索范围: {start.strftime('%Y-%m-%d')} ~ {today.strftime('%Y-%m-%d')}", file=sys.stderr)
    print(f"📂 覆盖分类: {', '.join(CATEGORIES)}", file=sys.stderr)
    print(file=sys.stderr)

    # 抓取论文
    papers = fetch_arxiv_papers(start_date, end_date)
    print(f"\n📊 共抓取 {len(papers)} 篇论文", file=sys.stderr)

    # 打分筛选
    scored = []
    for p in papers:
        weight, groups = score_paper(p)
        if weight >= args.min_weight:
            p["weight"] = weight
            p["matched_groups"] = groups
            scored.append(p)

    # 按权重降序，同权重按日期降序
    scored.sort(key=lambda x: (x["weight"], x["published"]), reverse=True)

    # 截断
    if not args.all:
        scored = scored[:args.top]

    # 输出 markdown
    date_label = f"{start.strftime('%Y-%m-%d')} ~ {today.strftime('%Y-%m-%d')}"
    print(f"## arXiv 论文发现 ({date_label})")
    print()
    print(f"共抓取 **{len(papers)}** 篇，筛选后 **{len(scored)}** 篇高价值论文")
    print()

    if not scored:
        print("_未发现符合条件的论文_")
        return

    for i, p in enumerate(scored, 1):
        title = p["title"]
        arxiv_id = p["arxiv_id"]
        published = p["published"]
        authors = format_authors(p["authors"])
        abstract = p["abstract"]
        weight = p["weight"]
        groups = ", ".join(p["matched_groups"])

        print(f"### {i}. {title}")
        print(f"- **日期**: {published} | **权重**: {weight} | **方向**: {groups} | **作者**: {authors}")
        print(f"- **arXiv**: [{arxiv_id}](https://arxiv.org/abs/{arxiv_id})")
        if abstract:
            short = abstract[:300] + ("..." if len(abstract) > 300 else "")
            print(f"- **摘要**: {short}")
        print()


if __name__ == "__main__":
    main()
