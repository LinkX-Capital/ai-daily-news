# 2026-03-18 X讨论抓取预览（修复后）

> 抓取时间: 2026-03-18 08:19
> 总数: 20条推文（已过滤过期推文）
> 时间窗口: 24小时 ✅

---

## 📊 分类统计

- 🏢 **公司推文（待分类）**: 17条
- 👤 **个人推文（X讨论）**: 3条
- ❓ **其他推文（X讨论）**: 0条

---

## 🔥 重点推文

### 公司官方公告（17条待分类）

**OpenAI (2条)**
- GPT-5.4 mini 发布：支持编码、计算机使用、多模态、子代理，速度快2倍
- GPT-5.4 nano 同步发布，已在 API 上线

**Google DeepMind (2条)**
- AGI 进度如何衡量？需要整个社区的努力
- AI 是电力，也是人类思想的延伸

**Meta AI (2条)**
- Canopy Height Maps v2 (CHMv2) 发布，开源森林高度数据
- 定制芯片对扩展下一代 AI 至关重要

**Anthropic (1条)**
- The Anthropic Institute 发布，推进 AI 安全前沿研究

**MiniMax AI (3条)**
- MiniMax 2.7 in action! Space Invaders demo
- 团队在 NVIDIA GTC，欢迎交流
- GTC 期间在湾区举办活动

**智谱AI (1条)**
- 🤗 庆祝 NVIDIA GTC 和 GLM-5-Turbo 发布，运行特别活动

**Perplexity (2条)**
- Fortune、AWS、AlixPartners 等公司使用 Comet
- Enterprise 计划中 Comet 集成更多功能

**vLLM Project (2条)**
- MiniCPM-o 4.5 — 9B 全模态模型，实时处理视觉语音文本
- 🎉 祝贺 Mistral AI 发布 Mistral Small 4

**OpenRouter (2条)**
- Hunter Alpha beats GLM-5？接近 Claude 水平
- Try Nano: openrouter.ai/openai

### 个人推文（3条X讨论）

**Sam Altman (@sama)**
- 感谢写详细反馈的用户

**swyx (@swyx)**
- 🆕 Claude Cowork, Skills, and the Future of AI Coworkers
- I made a @claudeai skill out of it. Productizing @swyx!!

---

## ⏰ 时间窗口检查

✅ **修复前**: 97条推文（67条超过48小时）
✅ **修复后**: 20条推文（100%在24小时内）

**时间分布**:
- 1-6小时: 7条
- 6-12小时: 10条
- 12-24小时: 3条

---

## 📁 存档文件

- **完整数据**: `/Users/shenyalan/ai-daily-news/archive/tweets_2026-03-18.json`
- **缓存文件**: `/Users/shenyalan/ai-daily-news/tweet_fetcher/cache.json`
- **预览文件**: `/Users/shenyalan/ai-daily-news/tweets_2026-03-18_preview.md`

---

## ✅ 修复内容

### 问题
- `tweet_fetcher/__init__.py` 的 `fetch_user_tweets()` 函数没有检查时间窗口
- 导致过期推文（最长5958小时）也被抓取

### 解决方案
- 在第133行添加时间窗口检查：`if not is_recent(published): continue`
- 确保只保留24小时内的推文

### 验证
- ✅ 修复前: 97条推文（93条过期）
- ✅ 修复后: 20条推文（0条过期）

---

## 📌 下一步

1. **公司推文需要 LLM 分类**（17条待分类）：
   - 模型前沿：GPT-5.4 mini/nano、GLM-5-Turbo
   - 产业动态：Anthropic Institute、GTC活动
   - 算力追踪：定制芯片
   - 初创&融资：Enterprise 集成

2. **个人推文可直接使用**（3条X讨论）

3. **建议保留的重要推文**：
   - GPT-5.4 mini/nano 发布
   - CHMv2 开源数据集
   - Anthropic Institute
   - MiniMax 2.7 demo
   - Mistral Small 4 发布
   - Claude Cowork/Skills

---

**状态**: ✅ 时间窗口过滤已修复并验证
