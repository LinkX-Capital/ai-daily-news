#!/usr/bin/env python3
"""
AI 新闻规范化 skill
功能：
1. 过滤非新闻内容（活动招募、征集、播客）
2. 修正错误分类
3. 同一公司多条消息时筛选/合并
4. 规范化分类定义
"""

from typing import List, Dict, Tuple
from collections import defaultdict

# ========== 1. 非新闻内容过滤 ==========
NON_NEWS_KEYWORDS = [
    # 转推
    "rt by", "rt:", "rt @",

    # 活动招募/征集
    "征集中", "火热征集", "倒计时", "招募", "报名", "邀请函", "申报即日起", "申报启动", "申报截止",
    # 传统行业/非AI科技（纯硬件/消费电子）
    "pc shipments", "个人电脑", "笔记本电脑", "手机销量", "智能手表",
    "电动汽车", "rad power", "radpower",
    "nintendo", "switch", "playstation", "xbox",
    "沙龙", "峰会", "大会", "论坛", "Meetup", "meetup",
    "评选", "奖项", "颁奖", "典礼",
    # 播客/访谈/视频节目
    "podcast", "podcasts", "播客", "访谈", "专访", "对话",
    "episode", "节目", "访谈录",
    # 招聘/求职
    "招聘", "求职", "Hiring", "hiring", "职位", "岗位",
    # 传统能源/基建 - 只过滤纯传统基建
    # 注意：核聚变、脑机接口、量子计算都属于前沿科技，应该保留
    
    # 安全事故/死亡 - 仅限于纯安全事故，和AI无关的
    "osha", "fatality",  # 仓库安全事故等
    "仓库",
    # 纯广告/商业
    "ad format", "advertising",
    # 非AI的营销/活动
    "免费送", "排爆", "鸡蛋",
]

def is_non_news(title: str, summary: str = "") -> bool:
    """判断是否是非新闻内容"""
    text = (title + " " + (summary or "")).lower()

    # 检查非新闻关键词
    for kw in NON_NEWS_KEYWORDS:
        if kw.lower() in text:
            return True
    return False

# ========== 2. 分类修正规则 ==========
# 公司名 -> 正确分类
COMPANY_CATEGORY_RULES = {
    # 融资新闻 -> 初创&融资
    "融资": "初创&融资", "投资": "初创&融资", "funding": "初创&融资",
    "估值": "初创&融资", "ipo": "初创&融资", "上市": "初创&融资",
    "收购": "初创&融资", "并购": "初创&融资", "acquisition": "初创&融资",

    # 算力/硬件 -> 算力追踪
    "gpu": "算力追踪", "npu": "算力追踪", "tpu": "算力追踪",
    "芯片": "算力追踪", "nvidia": "算力追踪", "amd": "算力追踪",
    "blackwell": "算力追踪", "h100": "算力追踪",

    # 安全/漏洞/合规 -> 产业动态 (非模型)
    "安全": "产业动态", "漏洞": "产业动态", "vulnerability": "产业动态",
    "合规": "产业动态", " Pentagon": "产业动态", "defense": "产业动态",
    "fda": "产业动态", "监管": "产业动态",

    # 消费者增长/财报/合作 -> 产业动态
    "增长": "产业动态", "用户": "产业动态", "安装": "产业动态",
    "财报": "产业动态", "收入": "产业动态", "合作": "产业动态",
    "partner": "产业动态", "微软": "产业动态", "google": "产业动态",
}

# 修正分类的关键词
CATEGORY_FIX_RULES = {
    # 研究关注
    "论文": "研究关注", "paper": "研究关注", "arxiv": "研究关注",
    "cvpr": "研究关注", "icml": "研究关注", "neurips": "研究关注",
    "acl": "研究关注", "nature": "研究关注", "science": "研究关注",
    "大连理工": "研究关注", "清华大学": "研究关注",

    # 模型前沿 - 必须是模型发布/能力/评测
    "发布": "模型前沿", "release": "模型前沿", "launch": "模型前沿",
    "开源": "模型前沿", "open source": "模型前沿",
    "gpt-": "模型前沿", "claude": "模型前沿", "gemini": "模型前沿",
    "llama": "模型前沿", "qwen": "模型前沿", "deepseek": "模型前沿",
    "sora": "模型前沿", "veo": "模型前沿", "文生图": "模型前沿",
    "文生视频": "模型前沿", "多模态": "模型前沿",
    "benchmark": "模型前沿", "评测": "模型前沿", "sota": "模型前沿",

    # 机器人/具身智能
    "机器人": "模型前沿", "robot": "模型前沿", "龙虾": "模型前沿",
    "具身": "模型前沿", "embodied": "模型前沿", "world model": "模型前沿",
}

def fix_category(title: str, summary: str = "", current_cat: str = "") -> str:
    """按内容本质分类 - 简单规则"""
    text = (title + " " + (summary or "")).lower()
    
    # 初创&融资：融资、投资、收购、上市
    if any(k in text for k in ["融资", "投资", "funding", "round", "估值", "ipo", "上市", "收购", "并购", "acquire", "天使", "a轮", "b轮", "c轮"]):
        return "初创&融资"
    
    # 算力追踪：硬件、芯片、云服务（明确是硬件相关）
    if any(k in text for k in ["gpu", "npu", "tpu", "芯片", "nvidia", "amd", "intel", "blackwell", "h100", "b100", "云计算", "aws", "azure", "gcp"]) and not any(k in text for k in ["sue", "诉讼", " tariffs"]):
        return "算力追踪"
    
    # 研究关注：论文、学术研究
    if any(k in text for k in ["论文", "paper", "arxiv", "cvpr", "icml", "neurips", "acl", "nature", "science"]):
        return "研究关注"
    if any(k in text for k in ["大连理工", "清华", "北大", "浙大", "MIT", "Stanford", "Berkeley", "CMU"]):
        return "研究关注"
    # 机器人/具身智能 -> 研究关注
    if any(k in text for k in ["龙虾", "robot", "机器人", "openclaw", "机械爪"]):
        return "研究关注"
    
    # 模型前沿：模型发布、能力、benchmark
    # 必须明确是模型本身的消息
    if any(k in text for k in ["gpt-5", "gpt-4.5", "o3", "o4", "claude 4", "claude 3.5", "gemini 2", "llama 4", "qwen3", "deepseek v"]):
        return "模型前沿"
    if any(k in text for k in ["sora", "veo", "dalle", "midjourney", "文生图", "文生视频", "视频生成", "图像生成", "stable diffusion"]):
        return "模型前沿"
    if any(k in text for k in ["flashattention"]) and "发布" in text:
        return "模型前沿"
    if any(k in text for k in ["benchmark", "评测", "sota", "state-of-the-art"]) and any(k in text for k in ["model", "模型", "gpt", "claude", "llama", "多模态"]):
        return "模型前沿"
    
    # 产业动态：其他一切（政策、合作、产品、安全事故等）
    return "产业动态"

# ========== 3. 同一公司多条消息处理 ==========
def group_by_company(articles: List[Dict]) -> Dict[str, List[Dict]]:
    """按公司分组"""
    companies = ["openai", "anthropic", "google", "nvidia", "meta", "microsoft",
                 "amazon", "apple", "deepmind", "deepseek", "字节", "阿里", "百度",
                 "腾讯", "特斯拉", "tesla", "mistral", "huggingface", "stability"]

    grouped = defaultdict(list)
    for a in articles:
        title = a.get("title", "").lower()
        summary = a.get("summary", "").lower()
        text = title + " " + summary

        found_company = None
        for c in companies:
            if c in text:
                found_company = c
                break

        if found_company:
            grouped[found_company].append(a)
        else:
            grouped["other"].append(a)

    return grouped

def filter_company_duplicates(articles: List[Dict], max_per_company: int = 2) -> List[Dict]:
    """同一公司只保留最重要的一条"""
    grouped = group_by_company(articles)

    result = []
    for company, arts in grouped.items():
        if company == "other":
            result.extend(arts)
        else:
            # 按优先级排序，保留前两条
            sorted_arts = sorted(arts, key=lambda x: x.get("priority", 0), reverse=True)
            result.extend(sorted_arts[:max_per_company])

    return result

# ========== 4. 规范化分类 ==========
# 模型前沿：只关注模型本身的发布、能力、评测
MODEL_FRONTEND_KEYWORDS = [
    "gpt-", "gpt4", "gpt5", "claude", "gemini", "llama", "qwen", "deepseek",
    "minimax", "kimi", "sora", "veo", "dalle", "midjourney",
    "模型", "发布", "开源", "能力", "benchmark", "评测", "sota",
    "多模态", "视频生成", "图像生成", "文生图", "文生视频",
    "参数", "训练", "微调", "推理",
]

def is_model_frontend(title: str, summary: str = "") -> bool:
    """判断是否属于模型前沿"""
    text = (title + " " + (summary or "")).lower()
    return any(kw in text for kw in MODEL_FRONTEND_KEYWORDS)

def normalize_category(article: Dict) -> List[str]:
    """规范化分类"""
    title = article.get("title", "").lower()
    summary = article.get("summary", "").lower()
    text = title + " " + summary
    
    # 后处理修正：用户增长类新闻必须归产业动态
    if any(k in text for k in ["用户增长", "用户数", "安装量", "日活", "活跃用户", 
                                "consumer growth", "daily active", "new installs", "growth surge"]):
        return ["产业动态"]
    
    # 后处理修正：商汤多模态 -> 模型前沿
    if "商汤" in title and "多模态" in summary:
        return ["模型前沿"]
    title = article.get("title", "")
    summary = article.get("summary", "")
    current_cats = article.get("categories", [])

    # 1. 修正错误分类
    fixed_cat = fix_category(title, summary, current_cats[0] if current_cats else "")

    # 2. 如果不是模型前沿但被分到模型前沿，移出
    if fixed_cat == "模型前沿" and not is_model_frontend(title, summary):
        # 尝试重新分类
        text = (title + " " + summary).lower()

        if any(k in text for k in ["论文", "研究", "cvpr", "icml", "arxiv"]):
            return ["研究关注"]
        elif any(k in text for k in ["融资", "投资", "估值", "上市", "收购"]):
            return ["初创&融资"]
        elif any(k in text for k in ["gpu", "芯片", "算力", "nvidia"]):
            return ["算力追踪"]
        else:
            return ["产业动态"]

    return [fixed_cat] if fixed_cat else ["产业动态"]

# ========== 主函数 ==========
def improve_news(articles: List[Dict], do_filter: bool = True) -> List[Dict]:
    """规范化新闻
    
    Args:
        articles: 新闻列表
        do_filter: 是否过滤非新闻内容（LLM会过滤，传入False可跳过）
    """
    improved = []

    for a in articles:
        title = a.get("title", "")
        summary = a.get("summary", "")

        # 1. 过滤非新闻（LLM处理后可以跳过）
        if do_filter and is_non_news(title, summary):
            print(f"   过滤: {title[:40]}...")
            continue

        # 2. 修正分类
        new_cats = normalize_category(a)
        a["categories"] = new_cats

        # 3. 更新优先级基于新分类
        if new_cats[0] == "模型前沿":
            a["priority"] = a.get("priority", 0) * 1.2
        elif new_cats[0] == "研究关注":
            a["priority"] = a.get("priority", 0) * 1.1

        improved.append(a)

    if do_filter:
        print(f"   过滤后: {len(improved)} 条")

    # 4. 同一公司多条消息处理
    improved = filter_company_duplicates(improved)
    print(f"   去重后: {len(improved)} 条")

    return improved

if __name__ == "__main__":
    # 测试
    test_articles = [
        {"title": "倒计时10天，2026 AI最佳场景渗透案例火热征集中", "summary": "", "priority": 100, "categories": ["模型前沿"]},
        {"title": "Transformer论文作者重造龙虾，Rust搓出钢铁版", "summary": "", "priority": 100, "categories": ["模型前沿"]},
        {"title": "此间无限获得千万美元天使投资", "summary": "", "priority": 100, "categories": ["模型前沿"]},
        {"title": "Anthropic's Claude found 22 vulnerabilities in Firefox", "summary": "", "priority": 100, "categories": ["模型前沿"]},
    ]

    result = improve_news(test_articles)
    print("\n结果:")
    for a in result:
        print(f"  - {a['title'][:30]}... -> {a['categories']}")
