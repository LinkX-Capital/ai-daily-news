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
