# AI Daily News Pipeline

## Feedback Log

Read `feedback.md` at the start of each session. It contains accumulated corrections from user reviews. When the user corrects a news item, append a new entry using the format defined in that file. The `rule_hint` field is especially important — it captures generalizable rules for future prompt optimization.

Key patterns from feedback so far:
- Title should be the most impactful story, not just the first one
- Body = facts + data + so what; Insight = AI judgments only
- Key points / Insight = AI's own analysis and judgments only (facts/data go in body)
- No exclamation marks or sensational language in titles
- Keep foreign company/person names in English
- Every article must have at least 1 key_point/insight
- Summary briefing items should only show key facts, no descriptive filler
- Check source link availability (replace nitter.net)
- Body must have quantifiable data; fetch from official sources if vague
- Official first-hand source preferred (arXiv > media reporting)
- Verify "首次发布/透露" claims — check if model/product was already released earlier
- Merge multiple sources for the same event: take the richest data from all sources

---

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
  "body": "3-6句话完整摘要，说明发生了什么+基于事实的so why it matters",
  "key_points": ["AI判断/分析1", "AI判断/分析2"],
  "is_ai_related": true/false,
  "category": "分类"
}
```

**Title rules:**
- 格式：事件主体 + 做什么/发布什么 + 为什么重要
- 取当天最有影响力的动态，不是简单取第一条
- 不用感叹号、不用媒体夸张口吻
- 错误示例：「彻底告别VE与VAE！商汤硬核重构多模态」「GPU时代落幕？硅谷巨头集体叛逃」
- 正确示例：「商汤发布新多模态架构：砍掉中间编码器，2B参数超越传统范式」「英伟达投入1500亿自研芯片：应对巨头叛逃，GPU时代或终结」

**Body rules (2026-03 重大升级):**
- **3-6句话**，信息密度要高
- **关键事实/数据**：是什么、关键突破/创新、具体数字、关键事件和关联信息
- **基于事实的 so what**：说明发生了什么 + 为什么这件事重要（基于事实分析，不是 AI 主观判断，主观判断放在 insight）
- 关键事实/数据加粗
- 不是纯新闻聚合
- 读完能了解来龙去脉，不点进原文也能跟人聊
- 如果只能写出一句slogan级别描述（模糊空洞），要么去原文挖更多信息，要么不收录

**Key points / Insight rules:**
- **AI 判断/分析**：意味着什么、有什么影响、趋势判断（放在 insight 里，不放 body）
- 每条新闻必须至少有 1 条 insight
- 不重复标题已说的内容

**Summary md 格式:**
- 不要生成 `> 展开阐释 + 关键细节 + 为什么重要 + 来源链接` 这行描述文字

**so what 示例：**
- ❌ 纯描述：「Anthropic 发布了 Claude 4」
- ✅ 有判断：「Anthropic 发布 Claude 4，在编程和推理上超越 GPT-4，**意味着 AI 编程助手竞争加剧**，中小开发者可能加速迁移」

**重要：**
- 禁止模糊称呼（如"AI研究者"、"研究人员"），必须具体到人名或公司名
- 海外公司/人名不翻译为中文，保持英文（如 OpenAI、Google、Anthropic、NVIDIA、Sam Altman）
- 链接必须与内容匹配，确保来源链接正确指向文章
- nitter.net 链接不可用，需替换为正确的 x.com 链接

**要点速览 rules:**
- 只显示"是什么"（取冒号之前的部分），不截断标题
- 例如：「FlashAttention-4发布」「Claude消费者增长加速」
