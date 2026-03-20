# 推文分类逻辑修复总结

## 问题诊断

根据用户反馈，存在以下问题：

1. **"研究者动态"分类仍然存在** - 应该完全移除
2. **分类规则不正确**：
   - 个人账号应该归类到"X讨论"
   - 公司账号应该按内容本质分类（由LLM判断）
3. **账号识别失败** - GoogleDeepMind等公司账号被误分类
4. **大小写敏感** - "GoogleAI" vs "googleai" 匹配失败

## 修复内容

### 1. 更新公司账号列表 (config.json)

**添加了缺失的公司账号：**
- `GoogleDeepMind` (主要问题)
- `AnthropicAI`
- `AIatMeta`

**更新后的完整列表 (22个)：**
```json
[
  "openai", "AnthropicAI", "claudeai", "GoogleDeepMind", "GoogleAI",
  "AIatMeta", "Meta", "Alibaba_Qwen", "deepseek_ai", "xai",
  "theworldlabs", "physical_int", "vllm_project", "liquid",
  "EpochaiLabs", "MiniMax_AI", "Kimi_Moonshot", "zai_org",
  "perplexity_ai", "essential_ai", "bespokelabsai", "openrouter"
]
```

### 2. 更新研究者账号列表 (config.json)

**添加了缺失的研究者账号：**
- `_jasonwei` (OpenAI)
- `jaseweston` (Meta)
- `chelseabfinn` (Stanford)
- `pabbeel` (UCB)
- `AndrewYNg` (吴恩达)

**更新后的完整列表 (21个)：**
```json
[
  "denny_zhou", "NeelNanda5", "yitayml", "shunyuyao12",
  "thesephist", "TheGregYang", "svlevine",
  "ylecun", "percyliang", "drfeifei",
  "sama", "swyx", "jeffdean", "karpathy",
  "JerryWeiAI", "bobmcgrewai", "_jasonwei",
  "jaseweston", "chelseabfinn", "pabbeel", "AndrewYNg"
]
```

### 3. 修复分类逻辑 (feed_v5.py:1173-1210)

**核心修复：大小写不敏感匹配**
```python
# 修复前（大小写敏感）
is_company = any(c in source for c in COMPANY_ACCOUNTS)
is_researcher = any(r in source for r in RESEARCHER_ACCOUNTS)

# 修复后（大小写不敏感）
is_company = any(c.lower() in source for c in COMPANY_ACCOUNTS)
is_researcher = any(r.lower() in source for r in RESEARCHER_ACCOUNTS)
```

**分类规则（已实现）：**
```python
if is_company:
    categories = ["待分类"]  # 公司推文 → LLM按内容分类
elif is_researcher:
    categories = ["X讨论"]   # 个人账号 → X讨论
else:
    categories = ["X讨论"]   # 其他推文 → X讨论
```

**"研究者动态"分类已完全移除**

## 测试结果

### 分类测试 (92条缓存推文)

```
🏢 公司推文 → 待分类 (47条)
  包括: @GoogleDeepMind, @GoogleAI, @OpenAI, @AnthropicAI,
        @AIatMeta, @MiniMax_AI, @perplexity_ai 等

👤 个人推文 → X讨论 (45条)
  包括: @sama, @jeffdean, @karpathy, @denny_zhou, @_jasonwei,
        @jaseweston, @chelseabfinn, @pabbeel, @AndrewYNg 等

❓ 其他推文 → X讨论 (0条)
  所有账号已正确归类
```

### 关键推文保留验证

✅ **已验证以下重要推文会被正确分类：**
- MiniMax M2.7 即将发布 → 待分类 (MiniMax_AI是公司账号)
- Perplexity Computer 功能升级 → 待分类 (perplexity_ai是公司账号)
- xAI Grok TTS API 发布 → 待分类 (xai是公司账号)
- 吴恩达新推文 → X讨论 (AndrewYNg是研究者账号)

## 修改的文件

1. **config.json**
   - 添加 `GoogleDeepMind`, `AnthropicAI`, `AIatMeta` 到公司账号
   - 添加 `_jasonwei`, `jaseweston`, `chelseabfinn`, `pabbeel`, `AndrewYNg` 到研究者账号

2. **feed_v5.py** (已在之前修复)
   - 行 1183-1184: 大小写不敏感匹配
   - 行 1187-1198: 正确的分类逻辑
   - "研究者动态" 分类已移除

3. **测试文件** (新建)
   - test_classification.py - 单元测试
   - test_full_classification.py - 完整流程测试

## 工作流程

1. **公司推文** → "待分类" → **LLM处理** → 根据内容归入：
   - 模型前沿
   - 产业动态
   - 算力追踪
   - 研究关注
   - 等

2. **个人推文** → "X讨论" → 直接输出

3. **"研究者动态"分类** → **已完全移除**

## 验证通过

✅ 所有测试通过
✅ 大小写匹配正确
✅ 所有账号正确归类
✅ "研究者动态"已移除
✅ 重要推文会被保留

---

*修复时间: 2026-03-17*
