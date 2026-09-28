# 前沿模型周报 · 第 9 期

**L2 智能基础层｜2026.09.09—09.28｜三周合刊**

# 旗舰能力下放，中端与开源重划性价比边界

GPT-6 Sol/Luna 与 Opus 5.5 同日把旗舰能力压进中端价位；开源权重 AA 天花板抬至 46 分；扩散 LLM 与决策模型把非自回归范式推到分发层门口。

主体事实截止 2026 年 9 月 28 日。综合能力分数优先采用 Artificial Analysis（AA）智能指数，厂商发布表数字单独标注口径，两类数字不可直接比较。

## 01 本期结论：四项变化

**旗舰能力下放明显加快，"每任务成本"正在取代"每 token 价格"成为定价叙事主轴。** GPT-6 Astra 发布仅 19 天后，OpenAI 推出 GPT-6 Sol 与 Luna，API 价格较 GPT-5.6 促销价再降 50%；官方表中 Sol 在 AutomationBench 超过 Opus 5（max）而每任务成本仅其 **9%**，DeepSWE v1.1 距 Fable 5.1 xhigh 只差 1.1 个百分点、成本低约 80%。同日 Anthropic 发布 Opus 5.5：多数工作达到 Fable 5.1 水平，典型负载运行成本较 Opus 5 低 **40%**，缓存读取价格降至输入价约 1/20——直接命中 agent 工作流的最大成本项。[旗舰下探](#s3)

**开源权重 AA 天花板从 45 分抬到 46 分，且首次由硬件厂商刷新。** 小米 MiMo-V2.6-Pro 取得 46 分（前代 26 分），超过 GLM-5.3 与 Kimi K3 登顶开源权重；同步公开 RL 训练账单——Pro 与 Flash 历时不到 6 天、成本约 262 万与 85 万美元。xAI Grok 4.7 换更大基座，TB4 官方口径从 20.3% 翻倍至 38.0%，AA 亦为 46 分。开源与闭源旗舰（53 分）名义差距约 7 分，同等智能下价格差达 1/20—1/60（小米口径，待第三方验证）。[开源权重](#s4)

**非自回归范式在三周内集中落地，并立即被开源复刻与平台量化。** Inception Mercury 2.5 以扩散架构跑出 1107 tok/s、智能较上代提升 40%；TypeSafe Jev 放弃文本生成、输出结构化决策值，宣称快 40—200 倍且输出 token 免费；Bespoke 两天用 LoRA 复刻出 90.1% 匹配率的开源版；OpenRouter 实测 Jev 在任务路由上比次快模型快 5 倍以上、准确率持平。新范式的护城河正落在工程与信任，而非算法本身。[范式分化](#s5)

**多模态竞争从"看得懂"转向"实时推理与智能体化"，专用模型开始反超通用旗舰。** Gemini 3.8 Live Extended Thinking 把深度推理带入实时语音；Qwen3.8-Omni-Flash 把音视频输入成本压低约 89%、智能体评测平均提升 19.5 分。Periodic Labs 万亿参数 Neon 在 XRD 衍射分析上超越 GPT-6 Astra 与 Fable 5.1（厂商自测，仅用约 1,300 张 H200）；Figure Helix 2.5 在 30 个陌生家庭零样本完成家务，成功率 9%→56%，并报告首个"人→机迁移 scaling law"。[多模态](#s6) · [专用模型](#s7)

## 02 横向格局：两个 46 分，与尚未收齐的期末快照

**本期 AA 指数的关键变化是新增两个 46 分：MiMo-V2.6-Pro（开源登顶）与 Grok 4.7。** 闭源双顶点 Fable 5.1 与 Astra 维持 53 分。Opus 5.5、GPT-6 Sol/Luna、Gemini 3.8 Live 发布较晚，本期素材内尚无 AA 分数。

| 模型 | AA 指数 | 数据时点 | 说明 |
|---|---:|---|---|
| Claude Fable 5.1 · max with fallback | **53** | 9/8、9/22 素材一致 | 闭源前沿双顶点之一。[模型页](https://artificialanalysis.ai/models/claude-fable-5-1) |
| GPT-6 Astra · max | **53** | 9/8、9/22 素材一致 | 与 Fable 综合同分，终端执行较强。[模型页](https://artificialanalysis.ai/models/gpt-6-astra) |
| Claude Opus 5 · max | 51 | 9/8 快照 | Opus 5.5（9/22 发布）AA 分数素材内未见。 |
| Muse Spark 1.3 · max | 48 | 9/8 快照 | Meta 前沿竞争组。 |
| GPT-5.6 Sol · max | 47 | 9/8 快照 | 注意：与 9/22 发布的 **GPT-6 Sol** 是两代不同模型。 |
| MiMo-V2.6-Pro · 开放权重 | **46** | 9/22 | **开源权重登顶**，前代 26 分。[来源](https://x.com/ArtificialAnlys/status/2102128560962187701) |
| Grok 4.7 | **46** | 9/22 | 较 4.6 的 44 分 +2。[来源](https://x.com/ArtificialAnlys/status/2102074898327932987) |
| GLM-5.3 · max · 开放权重 | 45 | 9/8 快照 | 上期开源领先者，被 MiMo 超越。 |
| Kimi K3 · max · 开放权重 | 44 | 9/8 快照 | 综合分紧随 GLM。 |
| Gemini 3.8 Flash · high | 41 | 9/8 快照 | Live 版（9/16）面向实时语音，属不同产品线。 |
| DeepSeek V4.1 Flash · 开放权重 | 40 | 9/11 | 552B 总参超越 1.6T 的 V4 Pro 0813（36 分）。 |
| Qwen3.8-2.4T-A95B · 开放权重 | 40 | 9/8 快照 | 对应开放检查点。 |

注：各行时点不同，**这不是同一日的完整截面**，仅汇总本期素材中可确认的分数；AA 榜单动态更新。[指数定义](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-3)

## 03 旗舰下探：GPT-6 Sol/Luna 与 Opus 5.5 同日发布

### OpenAI｜GPT-6 Sol 与 Luna：同代训练方法，价格直接砍半

9 月 22 日，OpenAI 发布 GPT-6 Sol 与 Luna，与 Astra 采用相似训练方法，把专业工作、事实性、编码与计算机使用能力带入更快更便宜的档位，**API 价格较 GPT-5.6 促销价下调 50%**。官方基准对照：

| 官方基准 | GPT-6 Sol 表现 | 对照 | 成本关系 |
|---|---|---|---|
| AutomationBench | Sol（xhigh）超过 Opus 5（max） | Opus 5 | **每任务成本仅其 9%** |
| Agents' Last Exam | Sol（max）**56.4%** | 高于 Opus 5 最高分 | 成本低 60% |
| DeepSWE v1.1 | Sol（max）**68.8%** | Fable 5.1 xhigh 为 69.9%，差 1.1 个百分点 | **成本低约 80%** |
| OSWorld 2.0 | Sol（xhigh）**60.5%** | 与 Opus 5（medium）持平 | 成本低约 80% |

来源：[OpenAI 发布页](https://openai.com/index/introducing-gpt-6-sol-and-luna)。内部事实性评测中 Sol 错误率约为前代一半；缓存输入享 90% 折扣，GitHub 披露数月来需新鲜处理的 token 份额因此降低超 50%。两款模型即日上线 ChatGPT Work 与 Codex。

### Anthropic｜Opus 5.5：中端反超旗舰口径，缓存读取降价 60%

同日 Anthropic 发布 Claude 5.5 家族首款模型 Opus 5.5：多数工作达到 Fable 5.1 水平，**典型负载运行成本较 Opus 5 低 40%**；定价输入 4 美元、输出 20 美元（各降 20%），**缓存读取 0.20 美元/百万、降 60%**，输出提速超 30%。

| Anthropic 官方口径 | Opus 5.5 | 对照 |
|---|---:|---|
| Terminal-Bench 4.0 | **66.4%** | Fable 5.1 为 55.8%、GPT-6 Astra 为 57.9% |
| GDPval-AA v2.1 | 1846 Elo | 知识工作评测 |
| FrontierCode 默认档 | 胜过 GPT-6 Astra | **每任务成本仅其约 20%** |

来源：[Anthropic](https://www.anthropic.com/claude-opus-5-5) · [Claude Blog](https://claude.com/blog/what-a-task-costs-on-opus-5-5)。注意：TB4 数字为 Anthropic 发布口径，与 AA 独立评测（第 8 期 Astra 59.1%、Fable 52.0%）不可直接比较。这是 Anthropic 呼吁"pacing the frontier"后首个发布，发布前经 Frontier Design 与 METR 外部评测；因生物与网络安全能力接近 Mythos 水平而沿用 Fable 级防护，多数网络安全任务回退至 Opus 4.8。早期用户一天内完成 68 万行代码迁移；Claude Code 企业部署平均成本约 13 美元/开发者/活跃日。Sonnet 5.5 与 Haiku 5.5 数周内发布。

**两家同日发布不是巧合：价值锚点正从旗舰 max 档下移到中端。** OpenAI 在 Astra 发布 19 天内完成同代能力铺开，速度明显快于上一代；Anthropic 用更小尺寸在终端任务上反超自家旗舰口径。缓存价格成为新的主战场——agent 工作流的重复上下文使缓存读取取代输出 token 成为最大成本项，两家分别给出 90% 折扣与 60% 降价。

## 04 开源权重：MiMo-V2.6 登顶，RL 成本首次全公开

### 小米 MiMo-V2.6：26 → 46 分，附 RL 训练账单

小米发布并开源全模态 MiMo-V2.6 系列（Pro/Flash），同步开源权重、技术报告与 **7k+ RL 任务环境**。Pro 为 MoE 架构（总参 1.02T、激活 42B），AA 指数从 26 分跃至 **46 分**登顶开源。罕见的是公开 RL 训练全过程账单与实时 dashboard：

| MiMo-V2.6 | RL 训练时长 | RL 训练成本 | DeepSWE v1.1 |
|---|---|---:|---|
| Pro（1.02T/42B 激活） | 不到 6 天 | 约 **262 万美元** | 提升约 14 分 |
| Flash | 不到 6 天 | 约 **85 万美元** | 提升约 17 分 |

来源：[小米 MiMo 官网](https://mimo.xiaomi.com/zh/mimo-v2-6) · [AA 快照](https://x.com/ArtificialAnlys/status/2102128560962187701)。定价沿用 V2.5，官方称同等智能下价格为海外模型的 **1/20 至 1/60**（小米口径）；新增 3D 空间推理与计算机操作能力。

**RL 账单公开把"规模化 Agentic RL 要花多少钱、跑多久"变成公共知识**——对跟进者既是路线图也是成本锚点：不到一周、百万美元级即可完成一轮登上开源顶位的后训练。

### Grok 4.7：换更大基座，TB4 翻倍、价格不变

xAI（SpaceXAI）9 月 22 日发布 Grok 4.7：**新的更大基座模型**加更长 RL，价格与速度与 4.6 持平（每百万 token 输入 2 美元、输出 6 美元）。官方口径 Terminal-Bench 4.0 从 20.3% 跃升至 **38.0%**，CursorBench 4.0 达 46.3%，Harvey 法律基准 19.6% 领先同档；LatchBio 生物安全基准 62.4% 居首、HackerBench 危险提示通过率仅 3.3%。AA 指数 46 分（+2）。当日上线 Cursor 与 Grok Build。[xAI 发布](https://x.ai/news/grok-4-7)

### DeepSeek V4.1 Flash：552B 超越自家 1.6T 旗舰

DeepSeek V4.1 Flash 以 **552B 总参**取得 AA 40 分，超过 1.6T 参数的 V4 Pro 0813（36 分），成为 DeepSeek 当前旗舰；单 token 成本约为 Pro 的四分之一，具备原生视觉理解，是新架构家族中最小成员。AA 指出其因生成内容较长，在智能—成本 Pareto 前沿上的位置略低于边界——综合评分开始受生成风格反噬。[AA](https://x.com/ArtificialAnlys/status/2098148674203488422) · [HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)

### GLM-5.3-FlashX：10 万张国产芯片上的 200 tok/s

智谱上线 GLM-5.3-FlashX，推理速度最高 **200 tokens/s**；基于 **10 万张国产芯片**的推理算力加大 Infra 投入与推理优化。GLM-5.3-Flash 曾以"Ox Alpha"之名面向全球开发者，调用量持续攀升。速度与部署侧的竞争说明 Flash 级战场已从 benchmark 转向推理体验，且这一轮提速不依赖海外供给。[智谱](https://mp.weixin.qq.com/s/ZJHhQrDeiwOGkkaqHw7kqA)

**开源阵营与闭源的名义差距约 7 分（46 vs 53），但价格差一到两个数量级。** 若 1/20—1/60 的定价对比经第三方任务成本验证成立，中端闭源模型将同时承受开源上方的性能压力与下方的价格压力。

## 05 范式分化：扩散 LLM 与"决策模型"进入分发层

### Mercury 2.5：扩散 LLM 摸到成本优化前沿模型门槛

Inception 发布 Mercury 2.5，自称市场最强、据信迄今训练过的**最大扩散语言模型**：智能较 Mercury 2 提升 **40%**，官方称可与 GPT-5.6 Luna（low）、Gemini 3.5 Flash-Lite、Claude Haiku 4.5 等成本优化模型对标；广泛可得的 NVIDIA GPU 上跑出 **1107 tok/s**，支持 260K 上下文，定价每百万输入 0.20 美元、输出 0.75 美元。公司称自 Mercury 2 以来用量增长超一个数量级，已通过 API、OpenRouter 与 Baseten 提供。若 40% 提升在第三方基准站得住，"亚秒级首 token + 千级吞吐"将从 demo 变成生产可选。[Inception Labs](https://www.inceptionlabs.ai/blog/introducing-mercury-2-5)

### Jev 与 System One 模型：放弃文本生成，输出结构化决策

TypeSafe AI（前 OpenAI 研究者 Diogo Almeida 创办）发布首类"System One 模型"：**不生成文本，输出类型安全的结构化决策值并附带校准概率**，训练方法为 RLCD（面向校准决策的强化学习），采样为并行而非自回归。首个模型 Jev 宣称在相近智能下比 LLM 快 **40—200 倍**（自建评测最高 193.6 倍快、444.6 倍便宜），输入定价 0.042 美元/百万 token、**输出 token 免费**，端到端响应 70—500ms，schema 匹配由构造保证。官方同时自曝局限：参考答案偏向 OpenAI/Anthropic 模型、评测集自建。[TypeSafe AI](https://typesafe.ai/blog/introducing-system-one-models-and-jev)

| 决策模型生态 · 三日内成型 | 结果 |
|---|---|
| **Bespoke-Nimble-9B**（开源复刻） | LoRA+对比数据策展，留出集匹配参考标签 **90.1%**（Jev 93.2%、基座 66.4%）；H100 单决策约 100ms。[GitHub](https://github.com/bespokelabsai/nimble) |
| **OpenRouter Ori Eval**（平台实测） | 30 类任务路由、200 用例：Jev 比次快模型快 **5 倍以上**，准确率与最常用分类 LLM 持平，成本第二低。[Ori Eval](https://openrouter.ai/ori/eval) |

**新范式从发布到开源复刻只用两天，从发布到平台量化只用三天。** 分发层（OpenRouter）正在成为新范式的第一检验场；Jev 的护城河更多在工程与信任而非不可复制性——若社区基准形成，"决策模型"可能从创业叙事变成 LLM 微调的标准下游任务。

## 06 多模态与实时：语音推理、音视频智能体与图像工作流

**Google 把"Extended Thinking"从文本推理档位移植到实时语音层。** Gemini 3.8 Live 面向规模、速度与成本，支持句中打断、97 种语言即时切换与视觉上下文；Live Extended Thinking 把深度推理带入语音对话。分层推出：Gemini API 与 AI Studio 即日可用，企业与消费侧渐次开放。与 OpenAI GPT-Live-1 的"语音层+后端推理委托"相比，两家都承认全双工语音与深度推理不能挤在一个模型里，分歧在同族双模型与可插拔后端——语音 agent 的推理深度成为新竞争轴。[Google Blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/)

**Qwen3.8-Omni-Flash：音视频理解从"看得懂"转向"看完能办事"。** 官方称首个围绕智能体能力构建的全能模态模型：原生音视频理解、推理与工具调用合一；音视频能力逼近 Gemini 3.8 Flash（官方口径），智能体评测（WildClawBench-MM/UniClawBench）平均提升 **19.5 分**；支持 100 万 token 上下文与智能体感知，在 OmniVideoBench 上比静态理解少用 51.8% token，**视频输入成本较 Qwen3.5-Omni-Plus 降低约 89%**。配套开源 Qwen-MM-Plugins 与 Qwen-Live Harness。[Qwen](https://qwen.ai/blog?id=qwen3.8-omni-flash)

**OpenAI ChatGPT Images 2.5：重心从生成质量转向编辑可控性与工作流。** 用户每周在 ChatGPT Images 与 GPT-Image API 创建**超 30 亿张图像**；新模型参考图主体保持更强、多轮编辑指令不再随轮次退化，延迟较 Images 2.0 最高降 50%。产品侧新增 Sketch 手绘参考、Templates 模板、图片批注定位编辑与 prompt 分享；API 推出 Flare（默认，快 50%）与 Sunburst（精细创意编辑）双模型。[OpenAI](https://openai.com/index/introducing-chatgpt-images-2-5/)

另：PrismML 三值化模型 Ternary Bonsai 2 27B 以 5.9GB footprint 保留全精度 98.2% 综合性能（基座 Qwen3.8 27B，262K 上下文，RTX 5090 上 143 tokens/s），把开源权重的部署门槛压到单卡级别。[PrismML](https://prismml.com/news/bonsai-2-27b)

## 07 专用模型：科学实验室与家庭机器人

### Periodic Labs Neon：专有数据飞轮在垂直任务击败通用旗舰

Liam Fedus 参与创办的 Periodic Labs 公开材料发现布局：Menlo Park 24/7 高通量实验设施，用自有实验数据做 mid-training 与 RL，训练出**1 万亿参数**的模型 Neon，称在 X 射线衍射（XRD）分析上**超越 GPT-6 Astra 与 Claude Fable 5.1**（厂商测试），训练仅用约 1,300 张 H200。核心主张是"实验室产出数据训练科学 AI、AI 反过来指导实验"的闭环：实验进行期间持续用已有数据改进模型而非让 GPU 闲置；当前聚焦超导体、磁体与半导体材料。Jeff Dean 公开转发祝贺。关键看 XRD 之外的能力能否随实验室规模同步扩展。[Periodic Labs](https://periodic.com/news/building-labs-that-learn)

### Figure Helix 2.5：零样本进家门，与首个具身 scaling law

Figure 在湾区租下 30 个真实家庭，机器人到现场**不做任何额外训练与适配**即执行整理客厅、叠毛巾、铺床等长程任务。Index 预训练将零样本成功率从 **9% 提升至 56%**，行为定义数据用量减半、泛化范围扩大 30 倍；并报告首个在人形机器人上测得的"人→机迁移 scaling law"：训练前即可将测试 loss 预测至小数点后四位，预测误差仅为总变异的 0.54%。Index 以约每秒 35 分钟人类经验数据的速度扩张，Helix 累计训练算力投入达 35 亿美元（官方口径）。"零样本进家门"是从演示走向家庭服务的关键门槛，可预测的 scaling law 让具身扩展从炼丹变成工程问题。[Figure](https://www.figure.ai/news/helix-2-5-zero-shot-30-home-generalization)

**两个信号同向：专有数据闭环 + 中等算力，足以在垂直任务上越过通用旗舰；而 30 个家庭的实地部署数据本身也在构筑护城河。**

## 08 下一期：三项最可能改变判断的证据

| 优先跟踪 | 关键新增证据 | 将改变什么判断 |
|---|---|---|
| **中端旗舰的第三方复测** | Opus 5.5 与 GPT-6 Sol 的 AA 收录分数、TB4 独立口径结果、真实 agent 负载成本。 | 官方对照的"中端即旗舰"能否在独立评测复现；缓存降价的实际节省幅度。 |
| **开源 46 分的成色** | MiMo-V2.6 在 AA 更新后的分数稳定性、海外可得性、第三方任务成本对 1/20—1/60 定价对比的验证。 | 开源与闭源 7 分差距是实质收窄还是榜单时点差异；价格战是否烧进闭源腹地。 |
| **非自回归范式的生产采用** | Mercury 2.5 的第三方基准；决策模型在 OpenRouter 的真实用量、标准基准是否形成。 | 扩散 LLM 与决策模型是新品类，还是退化为 LLM 微调的标准下游任务。 |

## 09 数据与来源

素材取自 2026.09.09—09.28 的 17 期日报「模型前沿」小节（其中 14 条构成本期主体，8 个发布日无模型发布类条目）。综合能力分数来自 Artificial Analysis 智能指数（动态更新，非同一日截面）；各厂商发布表数字均已就近标注口径，两类数字不可直接相减。往期见[第 8 期](frontier-models-2026-09-08.md)（2026.07.28—09.08）。
