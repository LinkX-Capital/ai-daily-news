# AI Daily News Pipeline

## Skills

### improve-news
Improve news quality by filtering and categorizing.

**When to use:**
- User mentions filtering non-AI news
- User wants to fix incorrect categories
- User wants to reduce duplicate news from same company

**Usage:**
```
/improve-news
```

**What it does:**
1. Filters non-news content (event recruitment, job posts, podcasts, traditional industry)
2. Fixes incorrect categories based on content 本质
3. Deduplicates news from the same company (max 2 per company)

**Category rules:**
- 模型前沿: model releases, capabilities, benchmarks
- 产业动态: policy, partnerships, security, corporate news
- 算力追踪: hardware, chips, cloud services
- 初创&融资: funding, investment, acquisitions
- 研究关注: papers, academic research

**Filter rules:**
- Event recruitment: 招募, 征集中, 倒计时, 沙龙
- Job posts: 招聘, 求职, Hiring
- Pure traditional industry: pure car news, real estate, food
- Pure safety incidents: warehouse accidents
- Non-AI ads: ad format, advertising

**Frontier tech (keep these):**
- Quantum computing: quantum, 量子
- Brain-computer interface: brain-computer, 脑机, bci
- Nuclear fusion: fusion, 核聚变, 核融合, nuclear
- Semiconductor: 半导体, chip

---

### process-news
LLM 处理新闻时的格式规范。

**When to use:**
- User mentions format issues with news titles, body, key_points
- User wants to fix LLM output quality
- Setting up or updating feed_v5.py LLM prompt

**Output format rules:**

```
{
  "title": "事件主体+做什么+为什么重要",
  "body": "2句话完整摘要，说明发生了什么",
  "key_points": ["要点1（从body提取，不重复body内容）", "要点2"],
  "is_ai_related": true/false,
  "category": "分类"
}
```

**Title rules:**
- 格式：事件主体 + 做什么/发布什么 + 为什么重要
- 不用感叹号、不用媒体夸张口吻
- 错误示例：「彻底告别VE与VAE！商汤硬核重构多模态」「GPU时代落幕？硅谷巨头集体叛逃」
- 正确示例：「商汤发布新多模态架构：砍掉中间编码器，2B参数超越传统范式」「英伟达投入1500亿自研芯片：应对巨头叛逃，GPU时代或终结」

**Body rules:**
- 必须是完整的2句话摘要
- 不能只是关键词
- 说明发生了什么

**Key points rules:**
- 从 body 中提取新信息
- 不要重复 body 已说的内容
- 补充关键细节

**Important:**
- 禁止模糊称呼（如"AI研究者"、"研究人员"），必须具体到人名或公司名
- 链接必须与内容匹配，确保来源链接正确指向文章

**要点速览 rules:**
- 只显示"是什么"（取冒号之前的部分）
- 例如：「FlashAttention-4发布」「Claude消费者增长加速」
