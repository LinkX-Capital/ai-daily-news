# 前沿模型周报 · 第 9 期

**L2 智能基础层｜2026.09.09—10.08｜四周合刊**

# 旗舰换代与能力下放，安全叙事成为新分水岭

四周内 Gemini 4 Argon 重夺软件工程 SOTA、GPT-6 全量推送；GPT-6 Sol 上市一个月即被 6.1 替换，Haiku 5.5 把运行成本压低 75%；开源模型在闭源旗舰因安全拒绝而失分的测试上首次登顶。

主体事实截止 2026 年 10 月 8 日。综合能力分数优先采用 Artificial Analysis（AA）智能指数，厂商发布表数字单独标注口径，两类数字不可直接比较。

## 01 本期结论：五项变化

**旗舰换代与能力下放同时发生，中端与旗舰的边界在按周移动。** 10/1 Google 发布新前沿旗舰 Gemini 4 Argon，DeepSWE v1.1 以 77.9% 创 SOTA、输出上限扩至 100 万 token，当前仅向可信防御者分阶段开放；9/30 OpenAI 发布 GPT-6.1 Sol，AA 指数距 Astra 仅 1 分、每指数任务成本约其四分之一，发布即替代上市仅 7 天的 GPT-6 Sol；9/29 Anthropic 的 Sonnet 5.5 在 TB4 官方口径取得 70.6%、超过两天前发布的 Opus 5.5（66.4%）。旗舰、中端、低端的换代节奏都已压缩到以天计。[旗舰换代](#s3)

**成本战打到最低价段，"单位智能成本"成为行业锚点。** Anthropic 三周内把 5.5 家族铺满价位段：Opus 5.5 典型负载成本较 Opus 5 低 40%，Sonnet 5.5 单任务成本最多低 30%，Haiku 5.5 平均运行成本较上代低 **75%** 并引入 10 万 token 内 0.10/0.50 美元的分级定价；OpenAI 侧 GPT-6.1 Sol 每指数任务成本 0.72 美元对 Astra 的 3.26 美元。缓存价格成为 agent 工作流的主战场。[旗舰换代](#s3)

**开源权重天花板抬至 46 分，并首次在安全测试上卡位闭源拒绝区。** 小米 MiMo-V2.6-Pro AA 46 分登顶开源（前代 26 分），公开 RL 账单：Pro 262 万美元、不到 6 天；Mistral Large 4（1T/52B 激活）自称欧美最强开源，在"复现并修复真实漏洞"测试得 **82%** 为所有模型最高——闭源旗舰 Opus 5.5 与 Astra 因安全拒绝在该测试接近 0 分；蚂蚁 Ling 3.1 Flash AA 指数 20→41 翻倍。[开源权重](#s4)

**非自回归范式从发布走向基准化，上期判断开始兑现。** 扩散 LLM Mercury 2.5 跑出 1107 tok/s；TypeSafe Jev 宣称快 40—200 倍，两天被 Bespoke 开源复刻至 90.1%；10 月国内 StartLux 开源决策模型在 Decision Index 0.2.1 的 38 项基准中 31 项超过 Jev、综合得分 63；vLLM Semantic Router Decision 2.0 以 Apache-2.0 开源 0.6B—27B 路由模型。决策模型正从创业叙事变成有基准、有开源基建的独立赛道。[范式分化](#s5)

**多模态竞争改写到交互层，专用模型继续反超通用旗舰。** Gemini 3.8 Live 把深度推理带入实时语音；Qwen3.8-Omni-Flash 音视频输入成本降约 89%；GPT-6 全量推送 12 亿用户，Intelligent UI 让模型即时生成可交互组件——固定软件界面开始被按需组装的界面取代。Periodic Labs 万亿参数 Neon 在 XRD 上超越 GPT-6 Astra/Fable 5.1（厂商自测）；Figure Helix 2.5 零样本家庭任务 9%→56%。[多模态与实时](#s6) · [专用模型](#s7)

## 02 横向格局：AA 快照重排，GPT-6.1 Sol 逼近双顶点

**本期 AA 指数关键变化：GPT-6.1 Sol 以 52 分逼近 53 分的双顶点；MiMo-V2.6-Pro 与 Grok 4.7 同为 46 分；Haiku 5.5 跳涨 26 分至 43；Ling 3.1 Flash 翻倍至 41。** Gemini 4 Argon 尚未公开发布（分阶段开放），Opus 5.5、Sonnet 5.5、GPT-6 Sol/Luna 本期素材内无 AA 分数。

| 模型 | AA 指数 | 数据时点 | 说明 |
|---|---:|---|---|
| Claude Fable 5.1 · max with fallback | **53** | 9/8、9/22 素材一致 | 闭源前沿双顶点之一。[模型页](https://artificialanalysis.ai/models/claude-fable-5-1) |
| GPT-6 Astra · max | **53** | 9/8、9/22 素材一致 | 与 Fable 综合同分，终端执行较强。[模型页](https://artificialanalysis.ai/models/gpt-6-astra) |
| GPT-6.1 Sol | **52** | 9/30 | 距 Astra 1 分；每指数任务成本 0.72 美元 vs 3.26 美元。[AA](https://x.com/ArtificialAnlys/status/2105025585332605357) |
| Claude Opus 5 · max | 51 | 9/8 快照 | Opus 5.5（9/22）AA 分数素材内未见。 |
| Muse Spark 1.3 · max | 48 | 9/8 快照 | Meta 前沿竞争组。 |
| GPT-5.6 Sol · max | 47 | 9/8 快照 | 与 GPT-6 Sol（9/22）、GPT-6.1 Sol（9/30）是三代不同模型。 |
| MiMo-V2.6-Pro · 开放权重 | **46** | 9/22 | **开源权重登顶**，前代 26 分。[来源](https://x.com/ArtificialAnlys/status/2102128560962187701) |
| Grok 4.7 | **46** | 9/22 | 较 4.6 的 44 分 +2。[来源](https://x.com/ArtificialAnlys/status/2102074898327932987) |
| GLM-5.3 · max · 开放权重 | 45 | 9/8 快照 | 上期开源领先者，被 MiMo 超越。 |
| Kimi K3 · max · 开放权重 | 44 | 9/8 快照 | 综合分紧随 GLM。 |
| Claude Haiku 5.5 | **43** | 10/8 | 较上代提升 **26 分**；低价档首次具备实战 agent 能力。[AA](https://x.com/ArtificialAnlys/status/2107911905822351609) |
| Gemini 3.8 Flash · high | 41 | 9/8 快照 | Live 版面向实时语音，属不同产品线。 |
| Ling 3.1 Flash · 开放权重 | **41** | 10/7 | 560B/25B 激活，从上一代 20 分翻倍。[AA](https://x.com/ArtificialAnlys/status/2107440860849901822) |
| DeepSeek V4.1 Flash · 开放权重 | 40 | 9/11 | 552B 总参超越 1.6T 的 V4 Pro 0813（36 分）。 |
| Qwen3.8-2.4T-A95B · 开放权重 | 40 | 9/8 快照 | 对应开放检查点。 |

注：各行时点不同，**这不是同一日的完整截面**，仅汇总本期素材中可确认的分数；AA 榜单动态更新。[指数定义](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-3)

## 03 旗舰换代与下探：Argon 领跑，Sol 一月两代，5.5 家族压满价位段

### Google｜Gemini 4 Argon：新前沿旗舰，先给防御者再公开

10 月 1 日发布的新一代前沿模型，输出上限从 64K 扩至行业领先的 **100 万 token**，定价输入 2 美元、输出 10 美元/百万，缓存输入再享 95% 折扣（Google 发布口径）：

| Google 发布口径 | 结果 |
|---|---|
| DeepSWE v1.1（真实软件工程） | **77.9%** 创 SOTA |
| Zapier AutomationBench | **51.3%** 居第一 |
| Vals Index（知识工作） | 第一 |
| CWE-bench v1（漏洞修补） | 68% 并列第一 |

来源：[Google 发布](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-4-argon/)。模型可自主发现并修补漏洞，Wiz 已用它发现全球医院医疗软件中此前前沿模型均未发现的关键漏洞；当前通过 Fairwind Program 向可信网络防御者分阶段开放，并参与美国政府 pre-release 自愿审查。内部已用于量子算法优化（超已发表基线 40%）与 C/C++ 向 Rust 大规模迁移。**「对防御者摘除护栏 + 先给红队再公开发布」，为前沿模型的安全发布流程立了新范式。**

### OpenAI｜GPT-6 Sol/Luna → GPT-6.1 Sol：中端一个月两代

9/22 发布 GPT-6 Sol 与 Luna（与 Astra 相似训练方法，API 价格较 GPT-5.6 促销价降 50%）；仅 7 天后 GPT-6.1 Sol 即取代之：

| 官方基准 | GPT-6 Sol（9/22） | GPT-6.1 Sol（9/30） |
|---|---|---|
| AutomationBench | Sol（xhigh）超过 Opus 5（max），每任务成本仅其 **9%** | — |
| DeepSWE v1.1 | Sol（max）**68.8%**（Fable 5.1 xhigh 69.9%，差 1.1 分） | 与 Astra 持平，超 GPT-6 Sol 最佳分 **6.4 个百分点** |
| Terminal-Bench Science 0.1 | — | 分数较 GPT-6 Sol **翻倍**，单任务成本 5.47 美元（Opus 5.5 为 23.21 美元） |
| 事实性 | 内部评测错误率约为前代一半 | 低推理档错误率 11.4% → **7.7%** |

来源：[GPT-6 Sol/Luna](https://openai.com/index/introducing-gpt-6-sol-and-luna) · [GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol)。GPT-6.1 Sol 定价与 GPT-6 Sol 持平（2/10 美元），缓存输入降至 **0.10 美元**；AA 评测称其发布即替代 GPT-6 Sol，智能指数 52 分、每指数任务成本 0.72 美元对 Astra 的 3.26 美元；Ultrafast 版即将上线，最高提速 8 倍。**「二代型号一个月内替换一代」，OpenAI 正把中端型号当成本效率的快消品迭代。**

### Anthropic｜5.5 家族三周集结：Opus → Sonnet → Haiku 压满价位段

| Anthropic 官方口径 | Opus 5.5（9/22） | Sonnet 5.5（9/29） | Haiku 5.5（10/8） |
|---|---|---|---|
| Terminal-Bench 4.0 | 66.4%（Astra 57.9%、Fable 5.1 55.8%） | **70.6%**（Sonnet 5 为 10.3%） | 39.2%（上代 0%） |
| GDPval-AA | 1846 Elo（v2.1） | 1844 Elo，几乎追平 Opus | 1620（上代 735、GPT-6 Luna 1437） |
| OSWorld | — | — | 2.1 离线子集 **72.4%**（上代 15.7%） |
| 成本叙事 | 典型负载较 Opus 5 低 **40%**；缓存读取降 60% | 定价持平 Sonnet 5，输出快 30%+，单任务最多低 **30%** | 平均运行成本较 Haiku 4.5 低 **75%**；10 万 token 内 0.10/0.50 美元分级定价 |
| AA 指数 | 素材内未见 | 素材内未见 | **43**（+26） |

来源：[Opus 5.5](https://www.anthropic.com/claude-opus-5-5) · [Sonnet 5.5](https://www.anthropic.com/claude-sonnet-5-5) · [Haiku 5.5](https://www.anthropic.com/claude-haiku-5-5)。Opus 5.5 是"pacing the frontier"后首个发布，经 Frontier Design 与 METR 外部评测，因生物/网络安全能力接近 Mythos 水平沿用 Fable 级防护；Sonnet 5.5 因网安能力与 Opus 5 相当而首次配备同级防护，并是首个搭载防蒸馏安全分类器的 Sonnet；Haiku 5.5 是首个支持 effort 设置与自适应思考的 Haiku 档。Sonnet 5.5 缓存读取价格减半（多数智能体任务约省 20%）。

**三家在同一个月里做了同一件事：把旗舰能力沿价格轴快速复制。** OpenAI 用"发布即替代"压缩代际周期，Anthropic 用家族三档一次铺满，Google 用 Argon 在顶部重新立标杆——差异只剩安全叙事：Argon 先给防御者，Opus 沿用 Fable 级防护，Mistral 则在闭源拒绝的测试上做文章。

## 04 开源权重：MiMo 登顶、Mistral 安全卡位与欧洲主权

### 小米 MiMo-V2.6：26 → 46 分，附 RL 训练账单

小米发布并开源全模态 MiMo-V2.6 系列（Pro/Flash），同步开源权重、技术报告与 **7k+ RL 任务环境**。Pro 为 MoE 架构（总参 1.02T、激活 42B），AA 指数从 26 分跃至 **46 分**登顶开源，并罕见公开 RL 全过程账单：Pro 与 Flash 历时不到 6 天、成本约 **262 万与 85 万美元**，DeepSWE v1.1 分别提升约 14 与 17 分。官方称同等智能下价格为海外模型的 **1/20 至 1/60**（小米口径）。[小米](https://mimo.xiaomi.com/zh/mimo-v2-6) · [AA](https://x.com/ArtificialAnlys/status/2102128560962187701)

### Mistral Large 4（Le Chonk）：在闭源旗舰拒绝的测试上拿全场最高

10/7 发布的 1 万亿参数、520 亿激活原生多模态开源旗舰，自称欧美最强开源权重模型，API 公开预览、月底开放权重（Mistral 官方口径）：

| Mistral 官方口径 | 结果 |
|---|---|
| 复现并修复真实漏洞 | **82%** 全场最高（Opus 5.5 与 Astra 因安全拒绝接近 0 分） |
| Cybench 解决率 | 93% |
| DeepSWE v1.1 | 61.7% |
| Surge AI 盲测代码质量 | 第二，仅次 Claude Opus 5 |
| Dense 200 视觉定位 | 42% 超 GPT-6 Astra（41%） |

来源：[Mistral AI](https://mistral.ai/news/mistral-large-4/)。模型在 Mistral 位于欧洲的自有数据中心以 **3800 块 Grace Blackwell GPU** 从头训练，可经自有基础设施在欧洲法律下端到端部署。**「闭源旗舰因拒绝而得零分的测试上拿全场最高分」是开源安全叙事的精准卡位——防御性安全工作恰恰需要证明漏洞真实存在；「欧洲自有算力从头训练 + 主权部署」则使其成为 AI 主权叙事的旗舰样本。**

### 其他节点：Grok、DeepSeek、GLM、Ling、Beam

- **Grok 4.7**（9/22）：新更大基座，TB4 官方口径 20.3%→**38.0%**，CursorBench 46.3%，AA 46 分（+2），价格与 4.6 持平（2/6 美元）。[xAI](https://x.ai/news/grok-4-7)
- **DeepSeek V4.1 Flash**（9/11）：552B 总参 AA 40 分，超越 1.6T 的 V4 Pro 0813；单 token 成本约四分之一，原生视觉；因输出冗长在 Pareto 前沿略低于边界。[AA](https://x.com/ArtificialAnlys/status/2098148674203488422)
- **GLM-5.3-FlashX**（9/19）：推理速度最高 **200 tokens/s**，基于 10 万张国产芯片的推理算力。[智谱](https://mp.weixin.qq.com/s/ZJHhQrDeiwOGkkaqHw7kqA)
- **蚂蚁 Ling 3.1 Flash**（10/7）：560B/25B 激活，100 万上下文，AA 指数 **20→41** 翻倍，agentic 提升最明显。[AA](https://x.com/ArtificialAnlys/status/2107440860849901822)
- **Reflection AI Beam**（10/6 预告）：英伟达支持的美国初创宣布首个开源权重模型，评测中、月底发布，定位"美国对标中国开源模型的选手"。[The Information](https://www.theinformation.com/briefings/reflection-ai-announces-first-open-source-model-beam)

**开源与闭源名义差距约 7 分（46 vs 53），但价格差一到两个数量级；安全维度上，开源与闭源的分工第一次被明码标价。**

## 05 范式分化：决策模型从发布走向基准化

### 扩散 LLM：Mercury 2.5 摸到成本优化前沿模型门槛

Inception 发布 Mercury 2.5，自称市场最强、据信迄今训练过的**最大扩散语言模型**：智能较 Mercury 2 提升 **40%**，官方称可与 GPT-5.6 Luna（low）、Gemini 3.5 Flash-Lite、Claude Haiku 4.5 对标；广泛可得的 NVIDIA GPU 上 **1107 tok/s**，260K 上下文，定价 0.20/0.75 美元；自 Mercury 2 以来用量增长超一个数量级。[Inception Labs](https://www.inceptionlabs.ai/blog/introducing-mercury-2-5)

### 决策模型：两周内形成"发布—复刻—平台实测—基准—开源基建"全链条

| 事件 | 结果 |
|---|---|
| **TypeSafe Jev**（9/17） | System One 模型：输出结构化决策值+校准概率（RLCD 训练），宣称快 40—200 倍、输出 token 免费，端到端 70—500ms；官方自曝评测局限。[TypeSafe AI](https://typesafe.ai/blog/introducing-system-one-models-and-jev) |
| **Bespoke-Nimble-9B**（9/19） | 两天 LoRA 复刻，留出集匹配参考标签 **90.1%**（Jev 93.2%、基座 66.4%）。[GitHub](https://github.com/bespokelabsai/nimble) |
| **OpenRouter Ori Eval**（9/20） | 30 类任务路由实测：Jev 比次快模型快 **5 倍以上**，准确率持平。[Ori Eval](https://openrouter.ai/ori/eval) |
| **StartLux 开源决策模型**（10/4） | Decision Index 0.2.1 的 38 项基准中 **31 项超过 Jev**，综合得分 **63**；国内开源社区广泛关注（机器之心报道）。[来源](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw%3D%3D&mid=2651060998&idx=1&sn=5e2496eb644e86fdf2d880a258074514&chksm=854cd911aca99dd4270bbd040abd159d1797882dbc38e6fdcded97821751c0d4e8d370673853&scene=0&xtrack=1) |
| **vLLM Semantic Router Decision 2.0**（10/4） | 0.6B—27B 开源模型，单次前向回答 **64 个问题**，Apache-2.0。[vLLM](https://x.com/vllm_project/status/2106193438098256191) |

**上期判断正在兑现：决策模型从"创业叙事"变成了有基准（Decision Index）、有开源基建（vLLM）、有中国玩家的独立赛道。** 值得注意的是基准本身尚在竞争——各家自建评测的口径差异，比传统 LLM 榜单更大。

## 06 多模态与实时：从语音推理到模型生成界面

**GPT-6 全量推送 ChatGPT：界面本身开始由模型生成。** 面向每周超 **12 亿**用户推送，免费与 Go 档由 Luna 驱动、付费档由 Sol 驱动。Intelligent UI 让模型用文本、图形、可点按钮、表单与图表组合回答，可当场生成可交互小工具；依赖原生可流式组件库与边生成边渲染的编译器。速度上，需网页搜索的问题 Instant 档较上代平均提前 **44%** 开始回答。「固定软件界面」的范式开始被按需组装的界面取代。[OpenAI](https://openai.com/zh-Hans-CN/index/gpt-6-for-everyone/)

**Google 把深度推理带入实时语音层。** Gemini 3.8 Live 支持句中打断、97 种语言即时切换与视觉上下文；Live Extended Thinking 应对多步思考任务，与 OpenAI GPT-Live-1 的分歧在同族双模型与可插拔后端。[Google Blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/)

**Qwen3.8-Omni-Flash：音视频理解转向"看完能办事"。** 智能体评测平均提升 **19.5 分**，OmniVideoBench 上比静态理解少用 51.8% token，视频输入成本较上代降约 **89%**。[Qwen](https://qwen.ai/blog?id=qwen3.8-omni-flash)

**图像赛道焦点转向多轮编辑保真。** OpenAI Images 2.5（周创建量超 30 亿张、延迟最高降 50%）主打编辑可控性；Ideogram 4.5 主打消除多轮编辑伪影累积——官方对比显示 GPT Image 2.5 Sunburst 与 Nano Banana 系列数轮内输出即不可用（厂商对比），并首次进入 AA-Image-Editing 榜（第 23 名）。[OpenAI](https://openai.com/index/introducing-chatgpt-images-2-5/) · [Ideogram](https://ideogram.ai/models/4.5)

另：PrismML Ternary Bonsai 2 27B 以 5.9GB 保留全精度 98.2% 性能（部署门槛压到单卡）；Perplexity 9B 上下文嵌入刷新 ConTEB 与 context-bench SOTA（答案召回超 voyage-context-4 达 14.4 个百分点）；微软发布对标 ElevenLabs 的语音模型；Cohere 开源 1T 以下最强翻译模型 North Small Translate。

## 07 专用模型：科学实验室与家庭机器人

### Periodic Labs Neon：专有数据飞轮在垂直任务击败通用旗舰

Liam Fedus 参与创办的 Periodic Labs 公开材料发现布局：Menlo Park 24/7 高通量实验设施，用自有实验数据做 mid-training 与 RL，训练出**1 万亿参数**的模型 Neon，称在 X 射线衍射（XRD）分析上**超越 GPT-6 Astra 与 Claude Fable 5.1**（厂商测试），训练仅用约 1,300 张 H200。核心主张是"实验室产出数据训练科学 AI、AI 反过来指导实验"的闭环；当前聚焦超导体、磁体与半导体材料，Jeff Dean 公开转发祝贺。关键看 XRD 之外的能力能否随实验室规模同步扩展。[Periodic Labs](https://periodic.com/news/building-labs-that-learn)

### Figure Helix 2.5：零样本进家门，与首个具身 scaling law

Figure 在湾区租下 30 个真实家庭，机器人到现场**不做任何额外训练与适配**即执行整理客厅、叠毛巾、铺床等长程任务。Index 预训练将零样本成功率从 **9% 提升至 56%**，行为定义数据用量减半、泛化范围扩大 30 倍；并自称测得首个"人→机迁移 scaling law"（人类经验数据→人形机器人，8× 数据范围、模型尺寸固定）：训练前即可将测试 loss 预测至小数点后四位，预测误差仅为总变异的 0.54%（厂商自测）。Index 以约每秒 35 分钟人类经验数据的速度扩张，Helix 累计训练算力投入达 35 亿美元（官方口径）。[Figure](https://www.figure.ai/news/helix-2-5-zero-shot-30-home-generalization)

**两个信号同向：专有数据闭环 + 中等算力，足以在垂直任务上越过通用旗舰；而 30 个家庭的实地部署数据本身也在构筑护城河。**

## 08 下一期：三项最可能改变判断的证据

| 优先跟踪 | 关键新增证据 | 将改变什么判断 |
|---|---|---|
| **Argon 公开后的独立评测** | AA 收录分数、公开发布时间表、DeepSWE/AutomationBench 第三方复测；Fairwind 防御者的实际使用报告。 | 77.9% SOTA 与百万输出窗口在开放条件下是否成立；"先给防御者"能否成为发布范式。 |
| **成本战的真实节省** | Haiku 5.5 与 GPT-6.1 Sol 在真实 agent 负载下的任务成本、缓存命中率、失败重试成本；5.5 家族 AA 分数补齐。 | 75%/四分之一的降价在官方口径之外能兑现多少；单位智能成本是否成为采购主指标。 |
| **开源安全叙事的成色** | Mistral Large 4 权重放出后的第三方复测、企业采用情况；MiMo/Ling 海外可得性与任务成本验证；决策模型基准能否收敛。 | 开源在闭源拒绝区的领先是否稳定；1/20—1/60 定价对比是否经得起第三方验证。 |

## 09 数据与来源

素材取自 2026.09.09—10.08 的 27 期日报「模型前沿」小节。综合能力分数来自 Artificial Analysis 智能指数（动态更新，非同一日截面）；各厂商发布表数字均已就近标注口径，两类数字不可直接相减。往期见[第 8 期](frontier-models-2026-09-08.md)（2026.07.28—09.08）。
