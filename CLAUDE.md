# AI Daily News Pipeline

## Feedback Log

Read `feedback.md` at the start of each session. It contains accumulated corrections from user reviews. When the user corrects a news item, append a new entry using the format defined in that file. The `rule_hint` field is especially important — it captures generalizable rules for future prompt optimization.

Key patterns from feedback so far:
- Title should be the most impactful story, not just the first one
- Body = facts + data + factual impact + quotes; AI's own so-what → insight only
- Key points / Insight = AI's own analysis and judgments only (facts/data go in body)
- No exclamation marks or sensational language in titles
- Keep foreign company/person names in English
- Every article must have at least 1 key_point/insight
- Summary briefing items should only show key facts, no descriptive filler
- Check source link availability (replace nitter.net)
- Body must have quantifiable data; fetch from official sources if vague
- Body hard floor: 3 sentences minimum; if insufficient, fetch more data or mark ⚠️
- Official first-hand source preferred (arXiv > media reporting)
- Verify "首次发布/透露" claims — check if model/product was already released earlier
- Merge multiple sources for the same event: take the richest data from all sources
- **Must read source before writing body** — never fabricate details from headlines/summaries
- **Degrade gracefully** — when source is unreachable, mark ⚠️ and write minimal confirmed facts only; never invent content to meet quality rules
- **No unsourced absolute claims** — "首个/首选/最大/核心地位" require explicit source support

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
  "body": "3-6句话完整摘要，基于原文事实",
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

**Body rules (2026-05 修订):**
- **3-6句话**，信息密度要高
- **关键事实/数据**：是什么、关键突破/创新、具体数字、关键事件和关联信息
- **只写事实，但要抓住关键影响**：不是纯新闻聚合——除了"发生了什么"，还要写出事实性的关键影响（如市场反应、股价变动、行业格局变化）和具体人物/公司的评价或观点（需注明是谁说的）。读完body能了解来龙去脉和为什么重要。但这里的"影响"必须是可验证的事实，不是AI自己的推测。AI自己的判断/趋势预测 → 放insight，不放body
- 关键事实/数据加粗
- 读完能了解来龙去脉，不点进原文也能跟人聊

**降级规则（信息不足时）：**
- 如果只能写出一句slogan级别描述（模糊空洞），要么去原文挖更多信息，要么不收录
- 来源不可达（微信反爬等）且无法验证内容时：标注"⚠️ 来源未验证"，只写已确认的最小事实集，不编造细节
- 宁可不达标（少于3句），也不能编造内容凑数

**事实核查硬性规则：**
- **写body前必须读原文**：用MCP/curl抓取来源文章，基于原文内容写body。禁止凭pipeline摘要或标题扩写润色
- **区分媒体和研究者**：DeepTech/机器之心/量子位是报道者不是研究者，不能把媒体的报道框架当成研究的原创贡献。论文类新闻必须找到arXiv/论文原文确认作者和内容
- **禁止无来源的绝对性判断**：body中禁止"首个""首次""首选""最大""核心地位"等表述，除非原文明确支撑。如果原文提到了prior work/竞品，绝对不能称"首个"
- **禁止无来源的市场地位判断**：body中禁止"首选引擎""领先平台"等竞争格局表述。这类判断如果要写，放insight且标注是AI分析

**Key points / Insight rules:**
- **AI 判断/分析**：意味着什么、有什么影响、趋势判断（放在 insight 里，不放 body）
- 每条新闻必须至少有 1 条 insight
- 不重复标题已说的内容

**Summary md 格式:**
- 不要生成 `> 展开阐释 + 关键细节 + 为什么重要 + 来源链接` 这行描述文字

**body vs insight 示例：**
- body：「Anthropic 发布 Claude 4，在编程和推理上超越 GPT-4。**SWE-bench 得分 72.3%**，较上代提升 15 个百分点。Sam Altman 评价称"这是真正的竞争对手"」
- insight：「意味着 AI 编程助手竞争加剧，中小开发者可能加速迁移」

**重要：**
- 禁止模糊称呼（如"AI研究者"、"研究人员"），必须具体到人名或公司名
- 海外公司/人名不翻译为中文，保持英文（如 OpenAI、Google、Anthropic、NVIDIA、Sam Altman）
- 链接必须与内容匹配，确保来源链接正确指向文章
- nitter.net 链接不可用，需替换为正确的 x.com 链接

**已废弃规则（勿再使用）：**
- ~~body必须有so what/为什么重要~~ → 已移至insight，body只写事实（#17, 2026-04-28）
- ~~body不是纯新闻聚合要有判断~~ → 修订为：body要抓住事实性的关键影响（市场反应/行业变化/专家评价），但不加AI自己的判断。"不是纯新闻聚合"≠"要有AI判断"，而是"要有事实性影响"
- ~~body硬性下限3句，禁止输出不足3句~~ → 修订为：优先补到3句，但宁可不达标也不编造（#22-#25, 2026-05-05）

**要点速览 rules:**
- 只显示"是什么"（取冒号之前的部分），不截断标题
- 例如：「FlashAttention-4发布」「Claude消费者增长加速」
