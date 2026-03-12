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
2. Fixes incorrect categories based on the content itself
3. Deduplicates news from the same company (max 2 per company)

**Category rules:**
- 模型前沿: model releases, capabilities, benchmarks
- 产业动态: policy, partnerships, security, corporate news
- 算力追踪: hardware, chips, cloud services
- 初创&融资: funding, investment, acquisitions
- 研究关注: papers, academic research

**Filter rules:**
- Event & recruitment: 招募, 征集中, 倒计时, 沙龙，报名，活动
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
  "body": "3-6句话完整摘要，说明发生了什么+为什么重要（必须有so what）",
  "key_points": ["关键判断/数据1", "关键判断/数据2"],
  "is_ai_related": true/false,
  "category": "分类"
}
```

**Title rules:**
- 格式：事件主体 + 做什么/发布什么 + 为什么重要
- 不用感叹号、不用媒体夸张口吻
- 错误示例：「彻底告别VE与VAE！商汤硬核重构多模态」「GPU时代落幕？硅谷巨头集体叛逃」
- 正确示例：「商汤发布新多模态架构：砍掉中间编码器，2B参数超越传统范式」「英伟达投入1500亿自研芯片：应对巨头叛逃，GPU时代或终结」

**Body rules (2026-03 重大升级):**
- **3-6句话**，信息密度要高
- **必须有 so what**：不只是「发生了什么」，还要说「为什么重要」或「意味着什么」
- 关键句子、关键判断加粗
- 要有判断，不是纯新闻聚合
- 读完能了解来龙去脉，不点进原文也能跟人聊
- 如果只能写出一句slogan级别描述（模糊空洞），要么去原文挖更多信息，要么不收录
- 每条都可以有一句点评或判断，但所有条目保持一致
- 相关条目要串联：同一故事的不同面要指出关联

**Key points rules:**
- 从 body 中提取关键判断/数据/结论
- 不要重复 body 已说的内容
- 加粗标注读者扫读时最该看的重点

**so what 示例：**
- ❌ 纯描述：「Anthropic 发布了 Claude 4」
- ✅ 有判断：「Anthropic 发布 Claude 4，在编程和推理上超越 GPT-4，**意味着 AI 编程助手竞争加剧**，中小开发者可能加速迁移」

**重要：**
- 禁止模糊称呼（如"AI研究者"、"研究人员"），必须具体到人名或公司名
- 海外公司/人名不翻译为中文，保持英文（如 OpenAI、Google、Anthropic、NVIDIA、Sam Altman）
- 链接必须与内容匹配，确保来源链接正确指向文章

**要点速览 rules:**
- 只显示"是什么"（取冒号之前的部分）
- 例如：「FlashAttention-4发布」「Claude消费者增长加速」
