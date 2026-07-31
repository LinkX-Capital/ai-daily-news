# 前沿模型周报 · 第7期 | 2026.07.18 — 07.25

> **本周主线：能力跃迁与效率提升同时发生。**
>
> 本期不是单点模型发布汇总，而是观察前沿模型层的两条长期曲线：**能力跃迁**看新模型是否打开数字工作流、世界模型、具身闭环的新能力边界；**效率提升**看同等能力是否进入更低价格、更高吞吐、更低延迟或更好的路由系统。
>
> 置信度：**高** = 官方 blog / 技术报告 / benchmark 可核验；**中** = 官方或第三方信号明确，但仍需独立复测；**低** = 单一弱信号，只作跟踪。

---

## 信号矩阵

| 主线 | 本周信号 | 强度 | 关键判断 |
|---|---|---:|---|
| 能力跃迁 | Claude Opus 5 在 coding / workflow / computer use 上接近最高智能档；FLUX 3 把 video / audio / action prediction 放入同一 world model 路线 | ★★★ | 前沿能力从单轮回答继续扩展到数字任务执行与物理世界表征 |
| 效率提升 | Opus 5 以 $5/$25 价格层承接强 agent 主任务；Sakana Fugu / OpenRouter Classifiers 代表路由与治理效率；FLUX-mimic 给出低延迟闭环指标 | ★★★ | 竞争重点从模型裸分转向单位任务成本、路由效率、部署延迟和真实闭环 |

---

## 一、本周重大发布：能力卡片

> 本部分只记录足以改变能力边界、成本曲线或厂商位置的更新。OpenRouter Classifiers 属于路由治理基础设施，不作为重大模型发布；Sakana Fugu-Ultra v1.1 属于中等权重的模型编排更新，不与 Opus 5 / FLUX 3 同权重。

### Claude Opus 5 — Anthropic 强 agent 主模型下沉

**重要标签**：高置信度 / 重大模型发布 / Agent 主模型 / Opus 层更新  
**更新周期**：相对上一期，Anthropic 从观察对象变成本期主更新厂商；Opus 5 代表新一轮 Opus 层更新。  
**来源**：[Anthropic Newsroom](https://www.anthropic.com/news/claude-opus-5) / [smol.ai](https://news.smol.ai/issues/26-07-24-opus-5/) / 本地日报 `daily-ai-news-2026-07-25.md`

| 关键更新 | 数字 / 证据 | 评论 |
|---|---:|---|
| API 价格维持 Opus 层 | **$5 / $25 per 1M input / output tokens** | 重点不是最强智能，而是把强 agent 能力压到可规模化价格层 |
| 长程 agent 能力提升 | Frontier-Bench v0.1 较 Opus 4.8 **2×+** | 比单题 coding 更接近真实 agent 工作流 |
| coding agent 接近最高档 | CursorBench 3.2 距 Fable 5 峰值 **0.5%** | Opus 5 可能成为高价值 coding agent 默认模型 |
| novel problem solving 强势 | ARC-AGI 3 为次优模型 **3×** | Anthropic 在 novel task 上继续保持前沿位置 |
| 工作流自动化经济性改善 | Zapier AutomationBench 同等成本通过率约 **1.5×** | 企业自动化更看单位任务成本，而不是裸分数 |
| computer use 成本效率 | OSWorld 2.0 约 **1/3 Fable 5 成本**超过 Fable 最佳结果 | 说明 Opus 5 与 Fable 5 有清晰路由分工可能 |

**一句话判断**：Opus 5 的重大性在于 **强 agent 主模型价格锚下移**，不是又一个最高智能展示模型。

---

### FLUX 3 — BFL 从图像生成进入世界模型周期

**重要标签**：高置信度 / 重大模型发布 / 世界模型 / 视频 + 音频 + 动作预测  
**更新周期**：BFL 从上期非主线厂商，进入本期非 LLM 前沿核心更新；这是从图像生成周期进入 video / audio / action prediction 新周期。  
**来源**：[BFL Blog: FLUX 3](https://bfl.ai/blog/flux-3) / [BFL Blog: FLUX 3 x mimic](https://bfl.ai/blog/flux-3-mimic) / [BFL X](https://x.com/bfl_ai/status/2080308988961554582)

| 关键更新 | 数字 / 证据 | 评论 |
|---|---:|---|
| 模型定位升级 | Real World Models / multimodal foundation model | 不是单纯视频生成，而是 world model 叙事 |
| 统一多模态训练 | image / video / audio 联合训练 | 多模态从多个生成器拼接走向统一 backbone |
| 视频生成能力 | 最长 **20 秒**，原生音频 | 进入可用视频生产工作流，但仍需横评 |
| 动作预测接入 | FLUX-mimic 将 backbone 用于 action prediction | 视觉生成模型开始触及 robotics foundation model |
| 训练计算结构 | video prediction compute **95%+** | BFL 把视频预测视为物理世界表征的主要路径 |
| 闭环延迟 | backbone **<80ms**；系统反应约 **101ms** | 机器人控制必须看延迟和稳定性，而非画质 |

**一句话判断**：FLUX 3 的重大性在于把 BFL 放进 **视频世界模型 × 具身智能** 竞争图，但领先程度仍需第三方 benchmark 与真实机器人任务验证。

---

### Sakana Fugu-Ultra v1.1 — 模型编排路线的中等权重更新

**重要标签**：中置信度 / 编排系统 / 效率提升 / 非基础模型旗舰  
**更新周期**：不是基础模型周期更新，而是多模型编排系统迭代。  

| 关键更新 | 数字 / 证据 | 评论 |
|---|---:|---|
| 多模型编排增强 | ProgramBench / Terminal Bench 2.1 较 v1.0 最高 **+7.9** | 说明模型组合与路由可能形成额外能力增益 |
| Claude Code 兼容接口 | 面向真实 coding agent 工作流 | 需要看延迟、成本叠加与路由错误率 |

**一句话判断**：Fugu 的意义不是单模型 SOTA，而是提示前沿竞争开始出现 **模型编排层**。

---

## 二、本周全局关键洞察

### 洞察 1：前沿 LLM 的主战场已经从聊天转向任务系统

Opus 5 的 benchmark 选择非常明确：Frontier-Bench、CursorBench、Zapier AutomationBench、OSWorld、ECI/SWE-ECI。这些都不是传统“题库型智力测验”，而是更接近 coding agent、workflow automation、computer use 的任务系统指标。前沿模型的商业价值正在由“回答质量”迁移到“能否低成本完成真实工作”。

### 洞察 2：强模型分层正在变成路由问题

Fable 5 继续承担最高智能锚点，Opus 5 则更像高价值 agent 主模型。OpenAI、Anthropic、Google、Meta、DeepSeek、Kimi、GLM、MiniMax 等厂商的竞争，不再是单一榜单谁第一，而是谁能在不同任务层给出最优价格 / 能力组合。

### 洞察 3：世界模型与具身智能应单独观察，不应混入 LLM 厂商表

FLUX 3、Sora、Veo、Runway、World Labs、Physical Intelligence、Skild、Figure、Google robotics、Mistral Robostral 属于另一条前沿路线。它们的关键指标不是 token benchmark，而是视频预测、空间一致性、动作预测、低延迟闭环、跨硬件泛化和真实部署。

### 洞察 4：Benchmark 本身成为需要被研究的对象

如果所有头部模型都在某个 benchmark 上接近饱和，这个榜单就只能证明“已达入场门槛”，不能区分前沿位置。下一阶段需要关注 benchmark 是否能区分真实任务：成本、耗时、工具调用、失败恢复、人工接管率、低延迟闭环。

---

## 三、关键厂商模型研究：版本迭代表

### 3.1 LLM / Agent 关键玩家更新周期

| 厂商 | 上期状态 | 本期变化 | 最新观察模型 / 系列 | 更新周期判断 | 本期处理 |
|---|---|---|---|---|---|
| OpenAI | 上期 GPT-5.6 + ChatGPT Work / GPT-Live 是主线 | 本期无新旗舰 | GPT-5.6 / Sora / agent platform | 上轮重大更新消化期，下一次看 GPT-6、agent platform 与 Sora 是否联动 | 延续观察 |
| Anthropic | 上期未发生同级旗舰更新 | 发布 Claude Opus 5 | Fable 5 / Opus 5 | 进入新一轮 Opus 层更新，强 agent 能力下沉到可规模化价格层 | 重大模型发布 |
| Google DeepMind | 上期作为多模态、具身和基础设施扩散观察对象 | 本期无关键新旗舰 | Gemini / Veo / robotics stack | 等待 Gemini、Veo、robotics stack 下一次统一更新 | 延续观察 |
| Meta | 上期 Muse Spark 1.1 升级为低价 agentic API 信号 | 本期无同级更新 | Muse Spark 1.1 / Muse Image / Video | Muse 仍在消化期，看 API 采用与 AA/GDPval 复测 | 延续观察 |
| Mistral | 上期 Robostral Navigate 代表具身导航与垂直模型扩散 | 本期无同级更新 | Robostral / Magistral / Codestral 路线 | 重点在垂直、边缘、具身路线，不是本周 LLM 旗舰竞争 | 延续观察 |
| DeepSeek | 4/27 参考期 V4 是效率革命代表 | 本期无新旗舰 | DeepSeek V4 / V4-Flash / V4-Pro | 仍是开源与推理成本效率锚点 | 延续观察 |
| GLM / 智谱 | 4/27 参考期 GLM-5.1 代表国产性能溢价和高频迭代 | 本期无新旗舰 | GLM-5.1 / GLM 系列 | 继续观察从低价换量转向性能溢价的节奏 | 延续观察 |
| MiniMax | 4/27 参考期代表低价高性价比编程模型 | 本期无新旗舰 | MiniMax M 系列 | 继续作为大规模子任务和低价路由层参照 | 延续观察 |
| Kimi / Moonshot | 上期 LongCat-2.0、Kimi base 与 coding agent 生态相关 | 本期无同级更新 | Kimi / LongCat / K2.6 观察线 | 看下一次是否继续在 SWE-Pro、Terminal-Bench、agent swarm 上追近闭源 | 延续观察 |
| Sakana AI | 上期不是主线 | Fugu-Ultra v1.1 | Fugu-Ultra | 编排系统迭代，不是基础模型旗舰 | 中等权重 |

### 3.2 非 LLM 前沿：世界模型与具身智能

| 模块 | 关键玩家 | 本周信号 | 需要比较的指标 | 判断 |
|---|---|---|---|---|
| 视频 / 世界模型 | BFL FLUX 3、OpenAI Sora、Google Veo、Runway、Pika、World Labs | FLUX 3 发布，强调 image / video / audio 联合训练与 Real World Models | 视频时长、音画同步、空间一致性、多镜头 chaining、可控性、价格、第三方视频 benchmark | FLUX 3 是本周非 LLM 前沿核心新增点，但仍需横评确认位置 |
| Robotics foundation model | FLUX-mimic、Physical Intelligence、Skild、Figure、Google robotics、Mistral Robostral | FLUX-mimic 把 FLUX 3 backbone 接入 action prediction，给出 <80ms backbone / 101ms 系统延迟信号 | action prediction、闭环延迟、跨硬件泛化、失败恢复、安全边界、工业部署 | 世界模型能否进入机器人控制，是比视频画质更重要的验证点 |
| 生成内容生产系统 | Runway、Midjourney、BFL、Pika、Adobe、Meta Muse | BFL 把视频生成与 world model 叙事合并 | 生产工作流、编辑可控性、一致性、版权 / 数据、商业 API 成本 | 内容生成模型会继续分化为创意工具与物理世界表征两条路线 |

---

## 四、Benchmark：关键能力榜单与榜单本身评估

### 4.1 关键榜单：各厂商最新位置

| 能力维度 | 关键 benchmark | OpenAI | Anthropic | Google | Meta | DeepSeek / GLM / MiniMax / Kimi | 本期变化 |
|---|---|---|---|---|---|---|---|
| Coding agent | CursorBench / SWE-Pro / SWE-bench Verified | GPT-5.6 仍是上一期 workflow 对照组 | Opus 5 距 Fable 5 CursorBench 峰值 **0.5%** | 待 Gemini 下一轮 | Muse Spark 1.1 AA Coding Index **71**（上期信号） | Kimi / GLM / DeepSeek 是国产追赶线 | Anthropic 本期给出最强新增信号 |
| 长程 agent | Frontier-Bench v0.1 | 待最新可比数据 | Opus 5 较 Opus 4.8 **2×+** | 待最新可比数据 | 待补 | 待补 | Opus 5 明确强化长程任务 |
| Computer use | OSWorld 2.0 / Terminal-Bench | GPT 系仍是参照 | Opus 5 约 **1/3 Fable 5 成本**超过 Fable 最佳结果 | Gemini / DeepMind 待补 | 待补 | Kimi / GLM / DeepSeek 需看 Terminal-Bench | 从分数转向任务成本比较 |
| Workflow automation | Zapier AutomationBench / AA-Briefcase | 待补 | Opus 5 同等成本通过率约 **1.5×** | 待补 | 待补 | 待补 | 企业自动化 benchmark 权重上升 |
| Novel reasoning | ARC-AGI 3 / GPQA / HLE | 待 GPT 最新公开横评 | Opus 5 ARC-AGI 3 为次优 **3×** | Gemini 仍需横评 | 待补 | Kimi / DeepSeek / GLM 需看 GPQA/HLE | novel problem solving 仍未饱和 |
| 视频 / 世界模型 | 第三方视频榜单 / world model task | Sora 仍是参照 | — | Veo / Gemini video 待横评 | Muse Video 作为社交分发信号 | FLUX 3 / Runway / Pika 需横评 | FLUX 3 暂无足够第三方 benchmark，不宜直接判领先 |
| 具身闭环 | robotics latency / closed-loop task | — | — | Google robotics 是长期参照 | — | FLUX-mimic 给出 **<80ms / 101ms** | 新榜单尚不成熟，关键在真实任务复测 |

### 4.2 Benchmark 本身评估

| Benchmark 类型 | 当前状态 | 是否饱和 | 区分维度是否足够 | 本期判断 |
|---|---|---|---|---|
| 传统知识 / 推理榜单（MMLU、GPQA 等） | 仍可作为智力底座参照 | 部分趋近饱和 | 对 agent 工作流区分不足 | 只能做基础能力门槛，不足以判断商业价值 |
| Coding 单题榜（HumanEval、LiveCodeBench 等） | 仍有用，但和真实工程距离大 | 中高饱和风险 | 对长程改动、环境理解、返工率不足 | 权重下降，应结合 SWE-Pro、CursorBench、Terminal-Bench |
| Coding agent / workflow 榜（CursorBench、Frontier-Bench、SWE-Pro） | 权重快速上升 | 暂未饱和 | 更接近真实工程任务，但仍需成本维度 | 本期最关键榜单组 |
| Computer use / automation（OSWorld、Zapier、AA-Briefcase） | 新兴关键榜单 | 未饱和 | 能观察工具调用、任务完成、成本 | 应成为 agent 商业化核心 benchmark |
| 视频 / 世界模型 benchmark | 仍分散，缺少统一权威横评 | 未饱和 | 对物理一致性、长期稳定性、可控性不足 | FLUX 3 需要此类 benchmark 才能确认位置 |
| 机器人闭环 benchmark | 极早期 | 未饱和 | 真实部署、延迟、安全失败、跨硬件泛化仍缺 | 未来 physical AI 的关键评测缺口 |

---

## 五、定价对比：从模型价格到任务成本

| 价格层 | 代表模型 / 厂商 | 价格 / 成本信号 | 适合任务 | 投资含义 |
|---|---|---|---|---|
| 最高智能档 | Fable 5 / GPT 最高档 / Gemini 最高档 | 高价，适合最高难任务 | 长程研究、复杂决策、关键代码迁移 | 用作最高价值任务锚点，不适合所有调用 |
| 强 agent 主模型 | Claude Opus 5 | **$5 / $25 per 1M input / output tokens** | coding agent、office workflow、browser/computer use | 若真实任务成本下降，会重置 agent 应用毛利模型 |
| 中端通用与编码模型 | Gemini / DeepSeek Pro / GLM / Kimi / Meta Muse | 价格与能力分布需持续横评 | 大量工程任务、复杂摘要、数据分析 | 多模型路由会在这一层产生主要成本优化 |
| 低价 / Flash 层 | DeepSeek Flash、MiniMax、轻量模型 | 低 $/M token，高吞吐 | 分类、提取、批处理、低风险子任务 | 应用系统不该把所有任务交给最高档模型 |
| 编排 / 路由层 | Fugu、OpenRouter Classifiers、LLM gateway | 不是 token 价格，而是降低错误路由和管理成本 | 任务分发、模型选择、成本治理、审计 | 企业推理基础设施机会上升 |
| 物理闭环成本 | FLUX-mimic / robotics stack | 关键是 latency、硬件、数据和部署成本 | 工业机器人、视觉控制、动作预测 | 不能只看模型 API 价，要看总部署成本 |

**核心判断**：前沿模型的效率提升不只来自 API 降价，也来自更好的模型分层、任务路由、缓存、工具调用、失败恢复和低延迟部署。

---

## 六、前瞻判断与趋势展开

### 趋势 A：Agent-native 模型会继续压低真实工作流成本

Opus 5 的意义在于把强 agent 能力带到更可规模化的价格层。下一步需要看它在 Devin、Cursor、Zapier、Terminal-Bench、AA-Briefcase、FrontierCode 等真实任务复测中的单位任务成本、返工率和人工接管率。

### 趋势 B：模型路由会成为应用层基础设施

当最高智能模型、强 agent 主模型、中端模型、低价子任务模型同时存在，企业不会只押一个模型。OpenRouter Classifiers 和 Fugu-Ultra v1.1 说明 routing / verifier / observability 会从工程技巧升级为基础设施。

### 趋势 C：世界模型与具身智能会从视频 demo 转向闭环任务

FLUX 3 的真正验证不在视频画质，而在是否能支持动作预测、低延迟控制和跨硬件泛化。未来一段时间，Sora、Veo、FLUX、Runway、World Labs、Physical Intelligence、Skild、Figure 的比较应围绕“世界表征能否进入真实任务”。

### 趋势 D：Benchmark 公司和 evaluation tooling 会变得更重要

如果模型竞争转向真实任务系统，那么 benchmark 也必须从“分数榜”升级为“任务账本”：记录成本、时间、工具调用、失败恢复、人工接管和安全边界。能提供可信横评与企业内评测系统的公司，会成为模型层竞争的基础设施。

### 本周一句话

前沿模型周报看的是全局：本期真正的变化不是某个模型单点更强，而是 **能力跃迁** 与 **效率提升** 同时把模型竞争推向真实任务系统、模型路由、世界模型和具身闭环。
