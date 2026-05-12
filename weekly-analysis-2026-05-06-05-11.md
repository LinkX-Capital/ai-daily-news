# AI 前沿认知扫描 | 2026.05.06 — 05.11

> 基于每日信号 + 认知协作 prompt | 核心目标：发现新连接 + 暴露盲区

---

## Part 1：新发现的新连接

**[连接1] ProgramBench 0% + Heuristic Learning → AI 正在同时证明"它不能做架构决策"和"它可以用代码替代训练自己"**

- **ProgramBench 0%**：Meta/Sakana AI 等发布 ProgramBench，要求 AI 从零重建完整软件（给可执行文件+文档，无源码，禁止联网），9 个模型完成率均为 **0%**，放宽到 ≥95% 测试通过最佳仅 Opus 4.7 的 **3%**。论文指出模型倾向于生成单文件巨型实现，与人类代码结构严重偏离
- **Heuristic Learning（翁家翌/OpenAI）**：Codex 写纯代码在 Atari Breakout 达到理论满分 **864 分**、MuJoCo Ant 达 **6146**（媲美 Deep RL）。核心是让 Coding Agent 持续维护程序代码系统替代神经网络梯度更新。翁家翌认为这可能是 pretraining→RLHF→RL/RLVR 之后的下一范式
- 两条信号放在同一个框架里看：**AI 在"自己设计架构"上完全失败，但在"在给定目标下用代码实现"上已经可以替代梯度训练**
- 这不是矛盾，而是两条路径的分化：
  - 一条路需要 AI 能做架构决策 → **当前完全失败**
  - 另一条路不需要 AI 做架构决策，只需要 AI 能根据规格写代码 → **当前已 work**
- **关键洞察**：Karpathy 说"软件是 agent 工作流缓存"，翁家翌正在把这个判断变成现实——agent 正在生成替代它自己训练方式的东西。MEMORY 里没有这条连接
- 置信度：中高。风险：Heuristic Learning 在 Atari/MuJoCo 上有效不代表在其他领域同样有效，边界未知

**[连接2] Cloudflare 裁员 1100+人 + ElevenLabs ARR $5亿 → AI 替代工作从预测变现实，但付费仍以 B2B 为主**

- **Cloudflare**：裁员 20%（1100+人）向"AI-first agentic 运营"转型。CEO 明确说"AI 让岗位本身消失了，不是削减成本"。内部 AI 使用量过去三个月增长 **600%+**，但 Q1 财报强于预期仍**大跌 14%**（Q2 指引低于预期）
- **ElevenLabs**：ARR 从 **$3.5 亿增至 $5 亿**（+43%），增长主要来自面向企业的 voice agent 销售，新增投资者包括 BlackRock、NVIDIA Ventures、Wellington。消费者端增长相对有限
- 两条信号放在一起：**AI 替代工作已经从"预测"变成"现实"（Cloudflare 是美国近期最大规模 AI 相关裁员）**，但替代工作的付费仍然主要是 B2B
- 与 B/C 端框架呼应：AI 替代工作 → B 端付费；AI 辅助创作 → C 端获客不获收。白领知识工作的替代比我之前认为的更早发生
- ⚠️ **修正**：ElevenLabs ARR 增长来自企业端 ≠ C 端市场不成熟，也可能是 ElevenLabs 的 GTM 更侧重 B 端。这个推断没有证据支撑，已删除原解读
- 置信度：高

**[连接3] NVIDIA $400亿股权投资 + Anthropic $2000亿 Google Cloud 承诺 + SpaceX Terafab $119B → L1 层基础设施锁定正在用资本加速**

- **NVIDIA**：2026 年至今已承诺超过 **$400 亿**用于 AI 公司股权投资，最大一笔向 OpenAI 投 **$300 亿**。Wedbush 分析师称"circular investment theme"——投资客户反购 GPU，实质是用资本锁定需求
- **Anthropic**：承诺向 Google Cloud TPU 投入 **$2000 亿**。此前 Google 已向 Anthropic 投资 $400 亿并承诺 5GW 算力，Anthropic 还与 SpaceX/Colossus 1 和 Akamai（$18 亿/7 年）达成算力合作，算力来源多元化
- **SpaceX Terafab**：提交德州芯片工厂提案，初期 **$55B**，总投资最高 **$119B**，Intel 合作，目标覆盖 AI 服务器/卫星/太空数据中心/Tesla 自动驾驶/机器人。SpaceX+xAI 合并实体估值 **$1.25 万亿**，预计 6 月 IPO
- 三条信号指向同一方向：**L1 层的基础设施竞争正在从"技术竞争"扩展到"资本锁定"**
- 这不只是"NVIDIA 在投资客户"那么简单——当 NVIDIA 同时投资 OpenAI 和 Anthropic，而 Anthropic 的算力来自 Google TPU 时，这指向**芯片→算力→模型→应用的全链条正在被少数几家资本方的交叉投资绑定**
- Panthalassa（海上算力，Peter Thiel 领投 $1.4 亿）是从能源侧独立切入的一极
- 置信度：高

**[连接4] Apple iOS 27 允许第三方 AI + Claude for Microsoft 365 + Codex Chrome 插件 → AI 分发渠道从"平台独占"转向"开放竞争"**

- **Apple**（Bloomberg/Gurman）：iOS 27 允许用户选择第三方 AI 模型驱动设备端功能，包括文本生成与编辑、图像生成等。用户通过 App Store 选择 Anthropic/Google/OpenAI 等
- **Claude for Microsoft 365**：正式全面可用，作为 AppSource 第三方加载项嵌入 Office 侧边栏，覆盖 Excel/PowerPoint/Word（Claude for Outlook 公开测试）。跨应用上下文共享是核心能力
- **Codex Chrome 插件**：支持 macOS/Windows 浏览器内直接运行，支持跨标签页后台并行工作
- 三条信号指向同一趋势：**AI 正在绕过平台原生 AI，直接嵌入用户已有的工作流**，而非要求用户迁移到新平台
- 置信度：中（Apple I/O 尚未官宣，WWDC 6 月才公布）

**[连接5] SSA 52x 加速 + TwELL 稀疏格式 + Pareto Code 路由器 → 效率/路由正在成为"可购买的基础设施"而非"模型能力"**

- **SSA（SubQ）**：1M token prefill 加速 **52.2x**，FLOP 降低 62.5%，RULER 128K 95.0%（持平 Opus 4.6）。精确限制注意力只计算携带信号的位置，非近似
- **TwELL（Sakana AI + NVIDIA）**：开源 GPU kernel，tile-wise ELLPACK 稀疏格式，推理 **30x 加速**（H100）、训练 **24x 加速**（峰值内存降低 24%），作者包括 Transformer 论文共同作者 Llion Jones
- **Pareto Code（OpenRouter/Nous）**：免费编程路由器，设置 `min_coding_score` 自动选最便宜达标编程模型，基于 Artificial Analysis 排名
- 三条信号都在说：效率和路由正在从"模型内建能力"变成**可独立优化和交易的组件**
- 这与 Fugu/AHE/RecursiveMAS 指向的"编排层独立化"是同一个方向的不同切面
- 置信度：中高

---

## Part 2：我的盲区清单

### 我不确定的事情（⚠️标注）

⚠️ **Jack Clark 预测 2028 年 AI 递归自我改进 60% 概率** — 60% 这个数字是怎么得出的？没有方法论信息。如果有方法论支撑，它可能改变对齐紧迫性判断；如果是直觉，它可能只是宣传

⚠️ **Heuristic Learning 的边界** — Atari/MuJoCo 有效不代表在机器人控制、代码生成、科学推理上同样有效。训练稳定性未知。**这是本周最重要的未知信号**

⚠️ **Genesis AI GENE-26.5 的 1:1 人手设计** — 这与你"本体终局"研究相关，但我不确定这个设计选择对"数据规模化"的实际影响

⚠️ **Anthropic 开源对齐工具 Petri** — 捐赠给 Meridian Labs 是战略决策还是战术撤退？

⚠️ **Apple iOS 27 第三方 AI 开放** — WWDC 6 月才公布，存在不确定性

### 我可能错了的地方

**[长上下文效率 ≠ 模型能力]** → SSA 52x 和 TwELL 显示长上下文效率正在变成可分离优化的基础设施组件。我之前追踪"哪个模型长上下文最强"这个问题的意义可能在下沉

**[白领替代比预期更早]** → Cloudflare 裁员明确是白领岗位。ElevenLabs ARR 增长主要来自企业端，可能反映的不是 ElevenLabs 更强，而是 B2B 语音市场比消费者市场更成熟

**[L1 层"资本锁定"是我框架的盲区]** → NVIDIA $400 亿投资、NVIDIA $300 亿投 OpenAI、Anthropic $2000 亿承诺——算力竞争已经不只是"买多少 GPU"，而是用资本锁定需求和供应。我的 MEMORY 框架里 L1 层主要追踪技术竞争，缺少"资本绑定"子维度

### 框架更新建议

**L1 层建议新增子维度："资本绑定"**

本周四条信号用"技术竞争"框架无法完全解释：
- NVIDIA 用投资换出货量（$400 亿）
- Anthropic 用承诺换 TPU 优先权（$2000 亿）
- SpaceX 用垂直整合绕开芯片采购（$119B Terafab）
- Panthalassa 用能源创新绕开陆地电网（$1.4 亿）

**L2 层"能力"定义正在分裂**

本周出现多个相互矛盾的能力评估维度：
- ProgramBench：**0%** → 架构决策不是模型能力
- Heuristic Learning：代码生成可替代梯度训练
- SSA/TwELL：效率不等于模型能力
- Opus 4.7 谄媚率 -50%：行为质量是能力的一部分

**L2 层的"能力跃迁"需要拆解成多个独立维度，否则无法解释这些互相矛盾的数据**

### 我的置信度陷阱

1. **Claude/Microsoft 365 集成是 B 端渗透关键路径** — 高置信度。但 Google I/O 可能反击（Gemini 嵌入 Android Office 替代 Copilot）
2. **Heuristic Learning 是下一范式** — 仅基于博客文章，无第三方验证。我可能因为结果"符合叙事框架"而过度解读

---

## Part 3：本周定性

> **这周最重要的一件事是：AI 正在用两条完全不同的路径同时逼近"替代自身训练"——一条是 RL 自博弈（David Silver），另一条是让 AI 写代码替代梯度训练（翁家翌/Heuristic Learning）。而与此同时，ProgramBench 显示 AI 在"自主架构决策"上仍然是 0%。这意味着 AI 正在变得擅长"执行"但还不擅长"设计"，而这两条路径都在试图绕开"设计"这个它做不好的事情。**

---

## 你的筛选

**Part 1 连接优先级：**

- [ ] **[连接1] ProgramBench + Heuristic Learning → 重要，值得深挖**
- [ ] **[连接2] Cloudflare 裁员 + ElevenLabs → 有意思，但不确定**
- [ ] **[连接3] L1 资本锁定 → 重要，值得深挖**
- [ ] **[连接4] AI 分发渠道开放 → 待验证信号**（⚠️ Apple iOS 27 尚未官宣，WWDC 6月才公布，降级为"等待验证的趋势"而非"已发现的新连接"）
- [ ] **[连接5] 效率/路由组件化 → 有意思，但不确定**

**Part 2 盲区追踪：**

- 下周最值得追踪：Heuristic Learning 边界 / Jack Clark 预测方法论 / L1 资本锁定格局
- L1 新增"资本绑定"子维度：是否同意？
- L2 能力维度拆解：是否认同？

---

## 框架更新记录（已落实）

| 更新 | 来源 | 状态 |
|------|------|------|
| L1 新增 L1-b 资本绑定子维度 | 连接3 | ✅ 已同步至 framework.md |
| L2 能力维度分裂：架构决策/执行/效率(L2架构创新)/行为对齐四维独立追踪 | 连接1 | ✅ 已同步至 framework.md |
| L2/L3 边界重定义：L2效率=架构创新，L3效率=模型无关推理工具 | 评估修订 | ✅ 已同步至 framework.md |
| L3 重构：从"AI Infrastructure"改为"Harness统摄"，Harness = 脚手架系统层 | 评估修订 | ✅ 已同步至 framework.md |
| L4b 重定义：从"Agent 经济"改为"垂直 & C 端 Agent 应用" | 评估修订 | ✅ 已同步至 framework.md |
| 信号追踪矩阵扩展：L1-a/b/L3/L4c/d + AI分发渠道 | 框架更新建议 | ✅ 已同步至 framework.md |

---

*生成时间：2026-05-11 | 评估修订：2026-05-12 | 框架修订：2026-05-12*
