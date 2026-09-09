# 前沿模型周报 · 参考资料与数据说明

**研究周期：2026.07.28—09.08｜主体数据截止：2026.09.08（北京时间）｜科学评测补核与多模态补充：2026.09.09**

[返回研究正文](frontier-models-2026-09-08-research.html)

## 数据口径

| 项目 | 定义与适用范围 |
|---|---|
| 期末横向比较 | AA Intelligence Index v4.3。历史发布分数采用当时版本，不与期末分数直接计算涨跌。 |
| 模型配置 | 推理强度、fallback、API 与开放检查点分别标注。max 是配置名，不保证每项任务都达到该模型的最高分。 |
| 厂商纵向对照 | 同一来源的前后代结果。竞品数据可能采用不同执行框架、工具或预算，不等同于统一独立复测。 |
| 任务成本 | AA 按指数权重计算的平均 API 花费，含输入、缓存、推理与答案 token；不含完整企业工作流的人工与外部系统成本。降幅按所列数值计算。 |
| 得分与不确定性 | 百分比得分差以百分点表示；Elo 不是准确率。置信区间按来源所列误差换算；“—”表示未列示数据。 |
| 日期 | 发布日期、论文日期、开放权重日期和实验发生日期分别对应不同事件。期前材料仅作为历史基线或技术背景。文本模型页为 9/8 快照；SciCode 与 Terminal-Bench-Science 的收录状态于 9/9 补核；第 08 节 AA 视频榜单为 9/9 补充，不作为此前历史排名。 |

## 证据适用范围

独立评测的结论限于其模型版本、任务集、执行框架和预算。厂商模型卡与研究报告中的结果保留自报属性；小规模论文实验的收益尚需在更大模型与生产环境中验证。

以下线索存在明确限制：**Pachocki 已披露包含 Astra 在内的模型计算图深度与 GPT-4 的差距在两倍以内，但未明确确认或否认 recurrent depth，亦未披露循环结构；Meta AIRA₃ 的竞赛成绩依据官方帖的日报转录，原帖全文未核验。** 前者仍不支持对模型增益作确定性架构归因，后者不构成开放式自主科研的证明。

**SemiAnalysis 对 Gemini 3.8 Flash / Muse Spark 1.3 的 benchmaxxing 及相似任务数据采购指控，依据所引帖文转述，未获独立证实。** Google 发布表可以支持新旧终端榜相对位置存在落差，不能据此确定训练数据来源或证明因果关系。

Atlas 的 B200 / MI355X 实时运行信息依据 9/9 日报所录官方帖及补充引文，原帖全文与演示未独立核验；该性能陈述不支持泛化的芯片性价比结论。fal 的 H3 Max 速度与内部偏好结果保留厂商自报属性；AA 文生 / 图生视频榜单分别提供质量参考，不测实时控制或世界状态。

Astra 发布页将“能力幻觉”描述为对自身能力与可用操作条件的误导性陈述；这与系统卡的用户报告事实错误评测分别理解。正文纵向表保留官方 Internal hallucination benchmark 的名称及 12.2% → 4.2% 数据，不将其视为线上总体幻觉率。

AI4AI 的日期与成熟度分别标注：Anthropic 上半年工程实践为背景，8/31 公告也包含对春季环境治理的回顾；Kimi K3 为 7/27 UTC 技术报告。Jalapeño 已有真实芯片结果，但生产部署为年末计划；Kimi 芯片案例为小模型设计与 RTL 仿真。GLM-5.3 与 Flash 官方发布页直接披露环境、奖励与验证器自动构建，以及基础设施 agent 参与推理引擎开发；无需以发言转述作为这些流程的依据。同基座能力增量与 2.3 倍以上 RL 系统吞吐仍不能分别归因于环境自动化或 agent。Google 的 AlphaEvolve 和 Meta 的 REA / KernelEvolve 为期前生产基础，未计作本期新增突破。

Kimi 的任务合成与工作区构建分别见技术报告 §4.2.2、§4.2.5：这两段披露训练管线使用 agent，未明确这些 agent 均由 K3 驱动。§7 分别披露早期 K3 检查点参与实际内核优化、MiniTriton 编译器案例，以及采用开源 EDA 工具和 Nangate45 标准单元库的小模型芯片设计与 RTL 仿真。各项均为作者披露；未据此认定编译器已进入生产、芯片已经流片，或各环节已构成自主研发全流程。[技术报告](https://arxiv.org/html/2607.24653v1)

## 模型与厂商资料

| 对象 | 原始来源 |
|---|---|
| OpenAI | [Astra 发布](https://openai.com/index/gpt-6-astra/) · [系统卡](https://deploymentsafety.openai.com/gpt-6-astra) · [GPT-5.6 服务优化](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/) |
| Anthropic | [Fable 5.1 发布时独立评测](https://artificialanalysis.ai/articles/claude-fable-5-1) · [期末模型页](https://artificialanalysis.ai/models/claude-fable-5-1) |
| Google | [Gemini 3.7 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/) · [3.8 Flash 发布](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) · [3.8 独立评测](https://artificialanalysis.ai/articles/gemini-3-8-flash) |
| Meta | [Muse Code / Spark 1.2](https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2) · [Spark 1.3 独立评测](https://artificialanalysis.ai/articles/muse-spark-1-3) |
| xAI | [Grok 4.6 发布与技术对照](https://x.ai/news/grok-4-6) |
| Z.ai | [GLM-5.3 发布](https://z.ai/blog/glm-5.3) · [GLM-5.3-Flash 发布](https://z.ai/blog/glm-5.3-flash) · [GLM-5.3 模型卡](https://huggingface.co/zai-org/GLM-5.3) · [GLM-5.3-Flash 独立评测](https://artificialanalysis.ai/models/glm-5-3-flash) |
| Qwen | [Qwen3.8-2.4T-A95B 模型卡](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) |
| DeepSeek | [V4 Pro 0813 服务端点](https://openrouter.ai/deepseek/deepseek-v4-pro-0813) |
| MiniMax / fal | [H3 模型卡](https://huggingface.co/MiniMaxAI/MiniMax-H3) · [H3 Max 发布](https://fal.ai/learn/devs/introducing-h3-max-by-fal) · [Director](https://fal.ai/models/minimax/h3-max/director) |
| 世界模型 | [World Labs Atlas](https://www.worldlabs.ai/blog/atlas) · [Runway Solaris](https://runway.com/news/research/introducing-solaris) |

## 评测与研究论文

| 主题 | 原始来源 | 研究内容 |
|---|---|---|
| 期末标尺 | [AA Intelligence Index v4.3 · 9/7](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-3) | 期末指数构成、模型分数与成本。 |
| 公开基准与迁移争议 | [SemiAnalysis 帖文](https://x.com/SemiAnalysis_/status/2097112791471522292) · [Google 评测方法](https://deepmind.google/models/evals-methodology/gemini-3-8-flash) | 区分可观察的跨任务落差与未经证实的数据采购解释。 |
| 终端执行 | [AA Terminal-Bench 4.0](https://artificialanalysis.ai/evaluations/terminalbench-v4-0) · [维护者变更说明](https://www.tbench.ai/news/terminal-bench-4-0) | 分离模型进步与环境、任务、判分变化。 |
| 流程完整交付 | [AutomationBench-AA](https://artificialanalysis.ai/evaluations/automationbench-aa) | 目标得分、完整完成率与约束违规规则。 |
| 端点保真 | [Endpoint Accuracy Index 方法](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) | 开放权重的模型能力怎样传递到实际服务。 |
| 循环架构背景 | [Recurrent Depth Approach · 2025/2](https://arxiv.org/abs/2502.05171) | 深度循环的技术定义与早期实验。 |
| 本期循环架构 | [SMELT · 9/1](https://arxiv.org/abs/2609.01343) · [Compositional Tool Calling · 8/17](https://arxiv.org/abs/2608.18171) | 用匹配实验和下游任务检验路线价值。 |
| 混合架构 | [Kimi K3 · 7/27 UTC](https://arxiv.org/abs/2607.24653) · [Qwen3.8-Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) | 序列状态、深度连接和知识存储的计算分工。 |
| 模型压缩 | [Inkling-Small · 7/30](https://thinkingmachines.ai/news/inkling-small/) · [模型卡](https://thinkingmachines.ai/model-card/inkling-small/) | 模型大小与部分能力关系改善的具体案例。 |
| 研发实践 | [OpenAI · 9/6](https://openai.com/index/research-acceleration-view-inside-openai/) | 真实使用中的介入、投入与产出边界。 |
| AI 辅助芯片设计 | [Jalapeño · 8/25](https://openai.com/index/jalapeno-first-results/) | AI 参与设计、流片前迭代和芯片编程；选定模块的加速不等于全模型加速。 |
| 训练工程与研究背景 | [Anthropic：When AI builds itself](https://www.anthropic.com/institute/recursive-self-improvement) | 上半年训练工程与代码审查、固定约束下训练代码加速、弱到强监督研究；分别区分实际使用与实验。 |
| RL 环境质量控制 | [Anthropic · 8/31](https://www.anthropic.com/news/improving-alignment-security-efforts) | 自动环境审查、认证与奖励漏洞；包含春季实践回顾。 |
| 智谱环境与系统研发 | [GLM-5.3](https://z.ai/blog/glm-5.3) · [Flash](https://z.ai/blog/glm-5.3-flash) | 自动构建环境、部分奖励及验证器；视觉数据与自验证；基础设施 agent 参与内核和服务优化。 |
| Google 既有研发基础 | [AlphaEvolve 2025](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) · [2026/5](https://deepmind.google/blog/alphaevolve-impact/) | 训练内核、算力调度与 TPU 设计，属于期前生产基础。 |
| Meta 既有研发基础 | [REA](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/) · [KernelEvolve](https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure/) | 推荐模型实验、跨硬件内核生成、轨迹用于专用模型后训练；属于期前生产基础。 |
| Kimi 任务合成与系统研发 | [K3 §4.2](https://arxiv.org/html/2607.24653v1#S4.SS2) · [§7](https://arxiv.org/html/2607.24653v1#S7) · [MiniTriton](https://github.com/MoonshotAI/minitriton) · [nano-kpu](https://github.com/MoonshotAI/nano-kpu) | agent 合成任务、初始化工作区，以及内核、编译器和芯片原型案例。 |
| 自动后训练研究 | [Anthropic · 8/28](https://www.anthropic.com/research/automated-researchers-mitigate-alignment-failures) | 自动研究方法及迁移到更大模型的证据。 |
| 研究方案选择 | [AI Research Preference Models · 8/14](https://arxiv.org/abs/2608.13940) | 研究瓶颈是否从执行转向实验选择。 |
| 研发能力量尺 | [AI4AI-Bench · 8/20](https://arxiv.org/abs/2608.20318) | 以重新训练和隐藏评估检验算法改进。 |
| 开放研究反例 | [Two Case Studies · 7/29](https://arxiv.org/abs/2607.27191) | 工程工作与实质研究贡献之间的差距。 |
| 执行框架共同演化 | [HarnessDev · 9/1](https://arxiv.org/abs/2609.01437) · [WHALE · 8/31](https://arxiv.org/abs/2609.00196) | 模型、harness 及两者联合优化的贡献如何归因。 |
| 新的硬任务边界 | [FrontierChallenge · 8/25](https://arxiv.org/abs/2608.24979) | 部分分数、模型自称完成与真正完成是否一致。 |
| 视频推理效率 | [vLLM-Omni / FastH3 · 9/1](https://vllm.ai/blog/2026-09-01-minimax-h3-production-serving) | 固定条件下的原权重服务优化，与四步蒸馏的完整响应测试。 |
| 视频质量 | [AA 文生视频](https://artificialanalysis.ai/video/leaderboard/text-to-video) · [AA 图生视频](https://artificialanalysis.ai/video/leaderboard/image-to-video) | 9/9 含音频榜单补充；两项 Elo 和置信区间分别使用。 |
| 视频底座的世界控制 | [H3-World · 9/1](https://arxiv.org/abs/2609.01560) | 从语言指令到角色与相机的时间对齐控制；不同于 fal Director。 |
| Atlas 实时运行补充 | [World Labs](https://x.com/theworldlabs/status/2097386577236476239) · [Justin Johnson](https://x.com/jcjohnss/status/2097423245742141907) · [李飞飞](https://x.com/drfeifei/status/2097429460115218568) | 9/9 日报收录的实时运行与跨芯片性能陈述；配置及独立复测待补。 |
| 世界模型量尺 | [PAWBench · 8/27，9/3 修订](https://arxiv.org/abs/2608.27345) | 从单条逼真视频转向未来分布与多样性。 |


知识工作与科学编程：[AA-Briefcase 定义与榜单](https://artificialanalysis.ai/evaluations/aa-briefcase) · [SciCode 定义与榜单](https://artificialanalysis.ai/evaluations/scicode)。综合指数与成本计算：[AA 方法论](https://artificialanalysis.ai/methodology/intelligence-benchmarking)。


## 科学评测补核 · 2026.09.09

[SciCode 的 AA 榜单](https://artificialanalysis.ai/evaluations/scicode)已收录 Astra max：未舍入值 0.564814814814815，正文显示 56.5%；Fable 5.1 max with fallback 为 0.630787037037037，显示 63.1%。这些为子问题计分，不能换算成完整科研项目成功率。

[Terminal-Bench-Science 维护方榜单](https://www.terminal-bench-science.ai/)的 0.1 数据含 12 个模型配置，9/9 补核时未列 Astra、Fable 5.1；每项任务运行三次，70 项任务对应 210 次试验。[OpenAI 发布表](https://openai.com/index/gpt-6-astra/)另列 Astra 64.6%、Fable 5.1 52.6%。正文保留厂商披露属性，不将“维护方榜单未收录”等同于“从未评测”，也不以其他网站转载成绩代替维护方记录。


## 架构与评测补充来源

| 对象 | 来源与适用范围 |
|---|---|
| Astra 计算深度与监控 | [Pachocki 9/2 原帖](https://x.com/merettm/status/2095023204993490967) · [9/6 官方文章](https://openai.com/index/an-alien-mind/)。计算图深度的范围不等于循环次数披露。 |
| 固定模型的框架对照 | [OpenAI：两项设置与 ARC-AGI-3](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/)。Sol、公开任务集 RHAE 13.3% → 38.3%；与 Astra 发布表分别使用。 |
| 持续代码维护 | [EvoCode-Bench](https://arxiv.org/html/2605.24110v1)。期前论文在 7/29 日报收录；SR 从参考状态继续，MT@4 保持工作区并采用四次尝试、失败即止计分。所测版本不含 Astra。 |
| 隐藏任务类型 | [Mystery Game Puzzles](https://epoch.ai/benchmarks/mystery-game-puzzles)。隐去游戏身份、提示与轨迹，降低针对性准备；正文不把早期快照当作最新排名。 |
| 等成本推理实验 | [Sample More, Reflect Less](https://arxiv.org/html/2607.28576v1)。1.5B—7B、两个数学基准、七种方法；以生成 token 计成本，不能当作全部输入输出 API 费用或旗舰模型结论。 |
| Atlas 空间评测 | [World Labs](https://www.worldlabs.ai/blog/atlas)。厂商组织相机跟随人评与稀疏视角重建实验，前者由第三方人员评分，后者复测所列基线；原生相机轨迹与文字提示的输入差异保留。B200 / MI355X 演示未披露完整卡数、精度、并发、功耗和成本配置，正文不扩展为通用硬件竞争判断。 |


## 纵向与专项评测明细

[横向能力](frontier-models-2026-09-08-research.html#s2) · [纵向迭代](frontier-models-2026-09-08-research.html#s3)。以下表中章号均指研究正文。

正文各厂商的代际对照采用同一来源内的版本比较。以下补充完整节点与专项能力。

| 厂商 / 本期节点 | 前后变化与迭代方向 | 对效率和节奏的判断 |
|---|---|---|
| **xAI** · 8/12 Grok 4.6 | 对 4.5，官方 DeepSWE v1.1：54.0% → 65.9%；TB3：15.7% → 26.0%。增加补充训练、模型生成数据及 agent RL。 | 从交互扩展到长任务；API 起价 $2/$6 每百万输入/输出 token。尚不能把更强等同于单任务更便宜。[官方对照](https://x.ai/news/grok-4-6) |
| **Z.ai** · 8 月中 GLM-5.3 发布；8 月下旬开放权重及 Flash | 5.2 → 5.3 **基座不变**：TB3 4.6% → 28.3%；DeepSWE v1.1 46.2% → 66.9%；PostTrainBench 31.7 → 39.8。 | 是后训练仍有大幅收益的强证据；不能据此量化它与预训练的相对贡献。大模型与 Flash 分别承担能力和成本位置。[官方模型卡](https://huggingface.co/zai-org/GLM-5.3) |
| **Qwen** · 8 月初 3.8-Max；9/2 Max 更新；Flash-Next 架构披露 | 3.7-Max → 3.8-Max 官方表：TB2.1 74.5% → 86.6%；DeepSWE 21.6% → 56.6%。后续继续后训练，同时探索新的混合架构。 | 同时经营大模型上限与架构效率；开放检查点和 Max API 并非完全同一配置。[3.8 模型卡](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) · [Flash-Next](https://huggingface.co/Qwen/Qwen3.8-Flash-Next) |
| **MiniMax / fal** · H3 → H3 Max → Director | 开放音视频底座进一步承接后训练、快速生成与连续交互，详见第 08 节。 | 能力增量与推理工程共同作用；FastH3 蒸馏是另一条路线，不能合并归功于同一模型。 |
| **Kimi** · K3 技术报告与权重披露 | 论文相对 K2 描述更大规模、KDA + MLA、Attention Residuals 与训练配方的联合改进。 | 本期披露补充了架构与训练效率证据；论文日期与模型首次发布日并非同一事件。2.5× scaling efficiency 的定义见第 05 节。[K3 报告](https://arxiv.org/abs/2607.24653) |
| **DeepSeek** · 8 月 V4 Flash / Pro 0813 / Vision Exp | 本期沿编程增强、部署与视觉扩展推进。GLM 的公开比较表列 V4 Pro 0813 的 DeepSWE 为 62.7%。 | 前代涨幅缺少充分可比的基线证据；服务价格因渠道和配置而异。[8/13 日报](/Users/shenyalan/ai-daily-news/daily-ai-news-2026-08-13.md) · [评测表](https://huggingface.co/zai-org/GLM-5.3) · [服务端点](https://openrouter.ai/deepseek/deepseek-v4-pro-0813) |
| **Thinking Machines** · 7/15 Inkling（期前）；7/30 Inkling-Small | 约 **15 天**推出小版：总参数 975B → 276B、激活 41B → 12B；HLE text 29.7% → 31.6%。 | 这是模型大小与部分能力关系改善的案例；小版训练启动更晚且配方不同，不是单变量蒸馏实验。[官方发布](https://thinkingmachines.ai/news/inkling-small/) |

| 能力面 | 本期关键证据 | 如何解释 |
|---|---|---|
| 知识工作与科研工作流 | AA 的 AA-Briefcase、SciCode 中 Fable 5.1 更强；OpenAI 发布的科学工作流比较中 Astra 更强。 | 能力优势随任务变化，且独立评测与厂商披露的证据等级不同。上表分别列示来源。 |
| 前沿数学与抽象推理 | Astra 官方披露 FrontierMath Tier 4 **v2** 98%、ARC-AGI-3 99.9%。 | 对相应版本的区分度构成压力；仍需看题目、工具、预算和独立复测，不能泛化为数学问题已解决。[Astra 发布](https://openai.com/index/gpt-6-astra/) |
| GUI 操作 | 官方 OSWorld 2.0 延迟模拟：Astra 72.6% / 约 40 分钟；Sol 65.7% / 约 75 分钟。 | 同时提高完成率、缩短模拟任务时长，是局部能力—速度双改善；不是所有真实任务普遍快 47%。[Astra 发布](https://openai.com/index/gpt-6-astra/) |
| 网络安全 | Astra 官方 ExploitBench 100%，Sol 78.5%；但其系统卡在更困难的外部评估中仍有未解任务。 | 旧量尺局部见顶，应转向更难环境、失败分布与访问条件；不能把单项满分写成整个能力面饱和。[发布页](https://openai.com/index/gpt-6-astra/) · [系统卡](https://deploymentsafety.openai.com/gpt-6-astra) |
| 长上下文与可靠知识 | Muse Spark 1.3 xhigh 在 AA-LCR 由 83% 降至 79%，AA-Omniscience 准确率由 45% 降至 42%，后者伴随更多弃答。 | 编程更强不保证其他能力同步改善；拒答增加与知识增强要分别记录。[AA：Spark 1.3](https://artificialanalysis.ai/articles/muse-spark-1-3) |

来源：[AA TB4](https://artificialanalysis.ai/evaluations/terminalbench-v4-0) · [OpenAI 发布表与评测脚注](https://openai.com/index/gpt-6-astra/)。官方表采用各推理档位最高结果；Sol 指 API / Codex / Work 版本。AutomationBench 与第 02 节的 AutomationBench-AA 不同；TB Science 也不是一般终端 TB4。FrontierMath Tier 4 v2 为 97.6%。ARC-AGI-3 的 Astra 使用调整了两项设置的 Responses API 执行框架，巨大增量不能全部归因于模型权重。

**效率与节奏：** OSWorld 延迟模拟从约 75 分钟缩至 40 分钟，同时得分提高，是局部双改善。Astra 标准 API 为每百万输入 / 输出 $10 / $50，不能由该模拟推出整体交付成本下降。Sol 于 7 月 9 日公开发布，到 Astra 相隔 56 天；期间既有 7 月 30 日服务优化，也有 8 月 21 日 Sol 为期三个月、超过 20% 的降价。该降价属于服务供给变化，与旗舰发布时间分别记录。[Astra](https://openai.com/index/gpt-6-astra/) · [Sol 发布及 8/21 更新](https://openai.com/index/gpt-5-6/) · [7/30 服务更新](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/)

来源：[3.7 发布](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/) · [3.8 官方评测表](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) · [方法说明](https://deepmind.google/models/evals-methodology/gemini-3-8-flash)。这是 Google 发布表汇集的自测及外部榜单数据，并非全部由同一个评测方复测。其 OSWorld 使用 8/8 补丁前任务及批量工具调用，不能与上方 OpenAI 离线集直接横比。DeepSWE 的 3.6 基线来自上一代发布表，跨两次发布的累计增量仍受配置变化影响。


## 效率实验与价格明细

[返回正文：效率突破](frontier-models-2026-09-08-research.html#s4)

| 改进发生在哪 | 本期可量化证据 | 收益及适用范围 |
|---|---|---|
| **缩小参数规模，保留部分能力** | Inkling → Small：总参数 **975B → 276B**、激活参数 **41B → 12B**；HLE text **29.7% → 31.6%**。 | 更小模型保持或超过部分能力；训练启动时间及配方不同，不能把参数降幅当作服务成本降幅。[发布](https://thinkingmachines.ai/news/inkling-small/) |
| **厂商训练实践 · 架构与配方** | Kimi K3 技术报告披露，相对论文 K2 基线约 **2.5 倍训练扩展效率**。 | 是架构、数据和训练配方的共同结果，非线上任务成本降幅。对照条件见第 05 节。 |
| **研究论文 · 循环架构的计算收益** | SMELT 匹配实验拟合的训练 FLOPs 节省约 **6.8%—18%**。 | 属于受控研究中的计算量收益，尚非前沿厂商生产训练的部署成果。实验条件见第 05 节。 |
| **生产内核与推理系统** | OpenAI 披露 Sol 参与内核改写与优化，使模型端到端服务成本下降 **20%**。 | 属于生产执行效率；另列的 token 生成效率实验采用不同口径，不能叠加降幅。[技术披露](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/) |
| **同权重的视频服务** | H3 在 **8×B300**、同提示及种子下，完整视频返回耗时 **82.239 → 56.917 秒**，缩短 **30.8%**。 | 未靠减少去噪步数或量化换取速度，是同模型、同测试条件的系统加速。[测试](https://vllm.ai/blog/2026-09-01-minimax-h3-production-serving) |
| **视频蒸馏与服务协同** | FastH3 蒸馏至四步后，配合服务优化，10.125 秒音视频约 **8.68—8.71 秒**返回。 | 模型与系统共同变化，需要另检验质量；不是 H3 原权重软件优化的单独贡献。配置及边界见第 08 节。 |
| **RL 训练系统** | 智谱在长任务编程 RL 中，通过缓存、教师切换、调度与负载均衡等改进，披露端到端训练吞吐提高至原来的 **2.3 倍以上**。 | 系统改进的合并自报结果；吞吐不等于达到同一能力所需的总训练成本，亦非基础设施 agent 的独立贡献。[GLM-5.3 发布](https://z.ai/blog/glm-5.3) |

**促销定价也影响用户侧成本。** Google 为 3.8 Flash 保持每百万输入/输出 $0.75/$3.75 的年内优惠，标准价为 $1.50/$7.50。这一价差反映商业定价，技术效率仍需通过资源消耗与服务性能验证。[Google：3.8 Flash 发布](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/)


## 架构分类与计算口径

[返回正文：架构趋势](frontier-models-2026-09-08-research.html#s5)

| “循环 / 混合”的不同含义 | 实际改变什么 | 对应的能力与成本指标 |
|---|---|---|
| **深度循环** | 隐状态重复经过共享模块，改变有效计算深度。 | 在相同参数、FLOPs 与推理预算下是否更强；循环增加的延迟。 |
| **序列递归 / 混合注意力** | 跨 token 更新状态，并与注意力组合处理上下文。 | 长序列吞吐、记忆容量与检索准确率；KDA、DeltaNet 不等同于深度循环。 |
| **跨层信息连接** | 改变层间信息如何传递与融合。 | 优化稳定性、有效深度与消融；Attention Residuals 不等于重复执行层。 |
| **外部 agent 循环** | 多次调用模型、工具与验证器，权重可以完全不变。 | 长任务成功率、调用数、纠错和成本；不能从 agent loop 推断底层 Transformer 结构。 |


## AI4AI 厂商实践完整记录

[返回正文：AI4AI](frontier-models-2026-09-08-research.html#s6)

本期披露与历史生产基础分别注明；训练流程、研发使用、论文实验与原型演示不合并统计。

| 厂商 / 覆盖环节 | 实际实践与本期进展 | 成熟度、日期与来源 |
|---|---|---|
| **OpenAI · 实验、训练运维、推理软件、芯片** | 研究 agent 参与多日实验、代码实现、运行监控和基础设施排障；Sol 优化生产内核及 token 生成，并监控训练、处理异常。AI 参与 Jalapeño 方案探索、电路优化与验证，Astra 协助优化配套模型软件。 | **研发及生产使用。** 7/30、8/25、9/6 披露；内核工作降低服务成本 20%，芯片配套选定模块加速 1.5—1.8 倍，芯片计划年末部署。3.1 agent 工作日 / 人类工作日是活动量。[服务](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/) · [芯片](https://openai.com/index/jalapeno-first-results/) · [研究](https://openai.com/index/research-acceleration-view-inside-openai/) |
| **Anthropic · 训练工程、代码质量、研究方法、环境审核** | Claude 参与训练故障定位、代码生成与审查；训练代码优化实验检验固定正确性约束下的加速；弱到强监督研究由 agent 提出并检验方案。本期自动研究者进一步探索对齐方法，另披露 RL 环境的训练前及训练中审查。 | **工程使用＋研究实验。** 上半年研究与工程为基线；弱到强监督结果未直接迁移到生产规模。8/28 对齐研究包含留出评估及更大模型迁移；8/31 环境治理仍需人工复核。[工程及早期研究](https://www.anthropic.com/institute/recursive-self-improvement) · [对齐研究](https://www.anthropic.com/research/automated-researchers-mitigate-alignment-failures) · [环境审核](https://www.anthropic.com/news/improving-alignment-security-efforts) |
| **Google · 模型迭代、训练算法、算力调度、TPU 设计** | 本期 3.8 Flash 披露 agent 循环评估并改进底层模型。既有 AlphaEvolve 已优化 Gemini 训练内核、数据中心调度和 TPU 电路；2026 年 5 月披露其成为下一代 TPU 设计的常用工具。 | **既有生产应用＋本期研发披露。** 2025 年报告关键内核加速 23%、Gemini 总训练时间缩短 1%，两者不是同一指标；本期模型迭代的净贡献未拆分。[本期](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) · [2025 基线](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) · [2026/5 进展](https://deepmind.google/blog/alphaevolve-impact/) |
| **智谱 · 环境、奖励、验证器、视觉数据、推理基础设施** | GLM-5.3 的 research agent 合成长任务环境，judge agent 验证可解性，验证器独立生成并检查奖励漏洞；部分任务直接合成 RL 奖励。Flash 发布披露视觉编码数据与自验证轨迹，以及 **GLM-5.3 基础设施 agent 协助开发内核、排查瓶颈、优化推理引擎**。 | **官方训练流程与实际研发使用。** 本期 5.3 / Flash 发布页直接披露；环境生成仍有显著人工参与。5.3 的同基座能力提升不能全部归因于环境自动化；系统吞吐收益也不能全归因于 agent。[5.3](https://z.ai/blog/glm-5.3) · [Flash](https://z.ai/blog/glm-5.3-flash) |
| **Kimi · 任务与工作区、内核、编译器、芯片原型** | 训练管线使用 agent 扩展知识图谱、合成任务并构建模拟工作区；早期 K3 检查点承担后期研发中大部分内核优化。案例包括 MiniTriton 编译器及 48 小时的小模型芯片设计与验证。 | **训练流程＋研发使用＋案例演示。** 7/27 UTC 报告；任务生成 agent 未明确均由 K3 驱动。内核有实际使用披露；编译器为案例成果，芯片仅设计与 RTL 仿真，未披露流片。[训练 §4.2](https://arxiv.org/html/2607.24653v1#S4.SS2) · [案例 §7](https://arxiv.org/html/2607.24653v1#S7) |
| **Meta · 模型实验、生产内核、专用模型后训练** | 既有 REA 在推荐模型研发中提出假设、启动训练、排障并迭代；KernelEvolve 生成跨硬件内核，并将搜索与验证轨迹用于专用小模型后训练。本期 AIRA₃ 公告另展示微调竞赛能力。 | **生产基础＋受限任务信号。** REA / KernelEvolve 为 3—4 月背景，后者在所测广告模型上提高推理吞吐逾 60%、训练吞吐逾 25%，不能外推至 Muse 全模型。AIRA₃ 第 8 / 约 4,000 队依据官方帖的日报转录。[REA](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/) · [KernelEvolve](https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure/) · [AIRA₃](https://x.com/AIatMeta/status/2096271545589190927) |
| **xAI · 补充训练数据、SFT 轨迹、质量筛选** | Grok 4.6 的补充训练使用筛选后的模型生成推理与技术数据；Grok 4.5 重生成跨领域、跨推理档位及框架的 SFT 轨迹，再经模型检查过滤。 | **官方训练流程。** 内核优化还被列为 RL 训练任务，但这本身不证明模型已优化 xAI 的生产内核。[4.6 技术说明](https://x.ai/news/grok-4-6) |
| **Qwen · 科学复现与 ML 工程评测** | Qwen3.8-Max 发布表中，PaperBench **64.8 → 93.0**、MLS-Bench-Lite **31.7 → 41.0**，显示研究执行能力改善。 | **能力评测。** PaperBench 为 BasicAgent / Code-Dev 设置；所引模型卡未披露自家生产训练或原创研究的实际贡献，不能与上述生产实践等量齐观。[模型卡及评测配置](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) |


## 多模态产品、实测与补充案例

[返回正文：多模态边界](frontier-models-2026-09-08-research.html#s8)

| 模型 / 路线 | 相对底座新增什么 | 能力与效率的含义 |
|---|---|---|
| **MiniMax H3 / H3-Base** · 7 月末发布、8 月初开放核心权重 | 统一多模态参考、同步音视频、首末帧与参考控制。 | 为后续定制和部署提供底座；生成控制能力与完整系统的开放范围分别评价。 |
| **fal H3 Max** · 8/26 发布文 | 在 H3 开放权重上增加后训练数据，针对提示遵循和视觉质量优化，并协同设计推理系统。 | 不是简单换一个托管端点；厂商报告质量改善、5 秒视频约 3 秒内生成，兼具能力和速度信号。[fal 发布](https://fal.ai/learn/devs/introducing-h3-max-by-fal) |
| **H3 Max Turbo** | H3 Max 产品线进一步面向速度与成本优化。 | 不能将 Max 的质量排名直接赋给 Turbo；价格须区分促销与标准价。[fal 产品页](https://fal.ai/minimax-h3-max) |
| **H3 Max Director** · 9/5—6 合刊收录 | 从有限片段转向连续视频流，可在生成过程中更新提示并保留角色、场景和叙事上下文。 | 交互形式发生变化；仍需量化控制延迟、长时漂移与断流率。它与 Max 的短片生成模式不同。[Director 官方端点](https://fal.ai/models/minimax/h3-max/director) · [发布帖](https://x.com/fal/status/2095599871449342288) |

| 优化层次 / 实测条件 | 前后变化 | 可以支持的结论 |
|---|---|---|
| **系统优化：原权重 H3** · vLLM-Omni · 8×B300 | 同提示和种子下，约 10 秒视频的端到端耗时 **82.239 → 56.917 秒**，降低 30.8%。 | 没有依靠减少去噪步数、量化或稀疏注意力的系统优化；该条件下仍慢于播放。 |
| **蒸馏模型＋服务：FastH3** · FastVideo / vLLM-Omni · 8×B300 · 1344×768 | 将 H3 蒸馏到四步；完整 **10.125 秒**音视频约 **8.68—8.71 秒**返回，RTF 约 0.86。 | 蒸馏与服务优化使整片生成跨过实时速度门槛；这里测的不是首帧或流式延迟。 |

来源：[vLLM：H3 与 FastH3 的完整响应测试](https://vllm.ai/blog/2026-09-01-minimax-h3-production-serving)。两组测试都使用 8×B300、以完整 MP4 返回计时，但原权重与 FastH3 的提示和种子不同，不能直接用 56.917 / 8.68 计算蒸馏加速倍率。FastH3 也不同于 fal H3 Max；其质量保留需单独评估。

| 方向 / 代表 | 已有证据 | 下一步怎样判断跃迁 |
|---|---|---|
| 连续生成 · H3 Max Director | 在线提示影响持续的视频流。 | 控制到画面的延迟、角色与场景长期保持、重启与断流。 |
| 空间建模 · Atlas | 相机控制、重建与 3D 输出，新增实时导航演示。 | 轨迹误差、绕行后场景一致性、几何误差及实时模式的质量损失。 |
| 视频底座的动作控制 · H3-World | 独立研究将 H3 的语言能力用于角色和镜头控制；以 8,000 个游戏样本和约 0.199% 可训练参数进行适配。 | 动作是否准确落在目标时段，以及控制能力是否迁移到未见场景。[论文](https://arxiv.org/abs/2609.01560) |
| 界面交互 · Runway Solaris | 展示随输入响应的界面生成，基于 Gen-4.5 蒸馏。 | 画面响应是否保留软件状态与逻辑，任务结果能否验收。[官方发布](https://runway.com/news/research/introducing-solaris) |

