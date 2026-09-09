# 前沿模型周报 · 第 8 期

**L2 智能基础层｜2026.07.28—09.08｜六周合刊**

# 复杂任务能力上升，低成本与高上限并行

执行、分析与科研任务呈现不同的领先者；更高能力的溢价，与模型压缩、推理工程带来的降本同时出现。

主体事实截止 2026 年 9 月 8 日。科学评测收录状态、视频榜单与 Atlas 实时演示另含 9 月 9 日补充。**期末比较采用 AA v4.3；纵向比较沿用各发布时点的同版本数据。**

## 01 本期结论：四项变化

**复杂任务的代际进步已跨越多个厂商，完整交付仍是瓶颈。** Astra 的独立终端评测提升、GLM 同基座的软件工程进步、Fable 的知识交付改善，指向共同的执行能力增长；但 Astra 在跨应用任务中，目标得分为 68.5%，全部完成率仍只有 41.6%。能力提升已扩大可承接工作，可靠交付仍留有明显缺口。[横向证据](#s2) · [代际对照](#s3)

**模型各有强项，旧榜上接近旗舰的表现未必能延续到新任务。** Astra 与 Fable 5.1 在期末 AA 指数同为 53 分，前者领先终端执行，后者领先知识交付与科学编程。Google 的 Gemini 3.8 Flash 在旧终端榜接近旗舰，在新任务上仍有显著差距；选用哪个模型，已比单看总榜名次更依赖任务类型。[任务比较](#s2) · [新旧榜差异](#s7)

**相似能力正在变便宜，最高推理档位仍有昂贵溢价。** Gemini 3.8 Flash low 达到 Gemini 3.6 Flash high 的发布时综合分数，成本低约 30%；Fable 5.1 从 max 降至 xhigh，只少 1 分，成本低约 28%。压缩模型与优化运行软件又提供了独立的降本路径，能力提升正形成更多价格与速度组合。[成本与效率](#s4)

**AI4AI 已从生成训练材料延伸到验证环境、运行实验和优化自身计算系统。** 智谱披露了长任务环境、部分奖励信号与验证器的自动构建流程，并以 GLM-5.3 协助开发 Flash 推理引擎；Kimi 使用 agent 合成任务、构建工作区，早期 K3 检查点已参与后期内核优化。OpenAI 的使用范围包括实验执行与监控、基础设施排障、生产内核优化和 Jalapeño 芯片开发；Anthropic 则覆盖训练工程、代码审查、训练代码优化、弱到强监督等方法研究及 RL 环境审查。Google 本期披露模型评估与改进的 agent 循环，既有 AlphaEvolve 实践已进入训练和 TPU 优化；xAI 将模型生成数据用于补充训练与 SFT。Meta 除本期披露的微调竞赛外，既有 REA、KernelEvolve 已用于推荐模型实验和生产内核；Qwen 的科学复现成绩则仍属能力评测。训练供给与工程执行已有落地，原创研究的净收益仍受问题选择、验证成本与规模化迁移约束。[厂商实践与研究证据](#s6)；第 06 节区分本期进展、历史基础及能力演示。

## 02 横向能力：AA 综合能力指数 v4.3 同分，任务优势不同

### 期末快照：Astra 与 Fable 并列，GLM 领跑所列开放权重模型

**Astra 与 Fable 5.1 同为 53 分，GLM-5.3 与 Kimi K3 分别为 45、44 分。** 综合分接近的模型，在终端执行、知识交付和科学任务上仍有明显分工。

注：Artificial Analysis（AA）的综合能力指数 v4.3 汇总 10 项评测，覆盖知识工作与流程执行、编程、知识与长文档理解、科学推理；价格与速度另计。9/7 更新后纳入 TB4、替换部分任务，因此发布时的旧版分数与本表不可直接相减。[指数定义与更新](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-3)

| 模型 / 评测配置 | AA v4.3 | 能力定位与配置说明 |
|---|---:|---|
| GPT-6 Astra · max | **53** | 与 Fable 综合同分，终端与流程执行表现更突出。[模型页](https://artificialanalysis.ai/models/gpt-6-astra) |
| Claude Fable 5.1 · max with fallback | **53** | 知识交付与科学编程较强；评测含 fallback。[模型页](https://artificialanalysis.ai/models/claude-fable-5-1) |
| Claude Opus 5 · max | 51 | 综合分接近新旗舰，知识工作表现仍处于前沿。 |
| Claude Fable 5 · with fallback | 50 | 前代高端模型，综合分比 5.1 低 3 分。 |
| Muse Spark 1.3 · max | 48 | Meta 进入前沿竞争组；max 为受限预览配置。 |
| GPT-5.6 Sol · max | 47 | Astra 的纵向基线。 |
| GLM-5.3 · max · 开放权重 | **45** | 本期快照中开放权重的最高综合分。[模型页](https://artificialanalysis.ai/models/glm-5-3) |
| Kimi K3 · max · 开放权重 | **44** | 综合分紧随 GLM，支持原生视觉与长上下文。[模型页](https://artificialanalysis.ai/models/kimi-k3) |
| Grok 4.6 · high | 44 | 跨应用流程执行较强，目标完成得分接近 Astra。[模型页](https://artificialanalysis.ai/models/grok-4-6) |
| GLM-5.3-Flash · 开放权重 | **42** | 同为 42 分时，任务成本显著低于 Terra。[模型页](https://artificialanalysis.ai/models/glm-5-3-flash) |
| GPT-5.6 Terra · max | 42 | 与 GLM Flash 同分，任务成本更高。[模型页](https://artificialanalysis.ai/models/gpt-5-6-terra) |
| Gemini 3.8 Flash · high | 41 | low 档位的代际降本较明显，见第 04 节。[模型页](https://artificialanalysis.ai/models/gemini-3-8-flash) |
| Qwen3.8-2.4T-A95B · 开放权重 | 40 | 对应开放检查点；与 Qwen3.8-Max API 的配置有差别。 |
| GPT-5.6 Luna · max | 38 | 低成本能力基线。[模型页](https://artificialanalysis.ai/models/gpt-5-6-luna) |
| DeepSeek V4 Pro 0813 · max · 开放权重 | 36 | 编程专项增强尚未转化为综合指数领先。 |

注：这是所列配置的 9/8 截面；分数取整，小分差不代表统计显著。fallback 表示评测包含回退模型。完整配置说明见[附录](frontier-models-2026-09-08-evidence.md#s1)。

### 复杂终端任务：Astra 领先，流程完整交付仍低于一半

**Terminal-Bench 4.0（TB4）测试模型在计算机终端中完成复杂任务的能力，由验证程序检验结果。** 在 AA 的同版本评测中，Astra 领先 Fable 与 Opus；这类任务包含软件操作、环境处理和复杂执行。

| Terminal-Bench 4.0 · AA 实现 | 平均 pass@1 |
|---|---:|
| GPT-6 Astra · max | **59.1%** |
| Claude Fable 5.1 · max with fallback | 52.0% |
| Claude Opus 5 · max | 49.0% |
| GPT-5.6 Sol · max | 39.9% |

注：AA 使用 66 项任务，每项运行三次；表中为所列 max 配置，Fable 含 fallback。[TB4 定义与榜单](https://artificialanalysis.ai/evaluations/terminalbench-v4-0)

**跨应用工作流的难点，进一步落在“所有目标做完、同时遵守约束”。** AutomationBench-AA 的目标得分允许部分完成，完整任务完成率则要求全部目标完成且没有约束违规。

| AutomationBench-AA | 目标完成得分 Score | 完整任务完成率 Tasks Completed |
|---|---:|---:|
| GPT-6 Astra · max | **68.5%** | **41.6%** |
| Grok 4.6 · high | 66.7% | — |
| GLM-5.3 · max | 62.2% | — |
| Claude Fable 5.1 · max with fallback | — | 32.1% |
| Claude Opus 5 · max | — | 28.3% |

来源：[AutomationBench-AA](https://artificialanalysis.ai/evaluations/automationbench-aa)，657 个留出任务。“—”表示未列示。Astra 两项指标之间的距离，反映了局部进展与完整验收之间的缺口。

### Fable 领先知识交付，科学任务的优势随工作类型变化

**AA-Briefcase 评估表格、演示文稿、备忘录等成品的分析质量、呈现质量及要求满足度。** Fable 5.1 与 Opus 5 位于前列，Astra 的终端执行优势没有延续到这类知识交付任务。

| AA-Briefcase · 9/8 快照 | Elo | 页面所列 95% 置信区间 |
|---|---:|---:|
| Fable 5.1 · max with fallback | **1662** | 1652—1672 |
| Opus 5 · max | 1645 | 1638—1653 |
| Muse Spark 1.3 · max | 1589 | 1578—1600 |
| Astra · max | 1562 | 1553—1572 |
| GLM-5.3 · max | 1515 | 1506—1525 |
| Kimi K3 · max | 1497 | 1491—1504 |

注：Fable 与 Opus 的区间接近且略有重叠，尚不足以据点估计认定显著领先。Elo 为相对评分，并非准确率或生产率增幅。[榜单与定义](https://artificialanalysis.ai/evaluations/aa-briefcase)

**SciCode 评测科学编程，Terminal-Bench-Science 评测科研工作流。** 前者按代码子问题计分；后者包含五个科学领域的 70 项任务，检验数据分析、仿真和模型拟合等成果。

| 评测与来源 | Astra | Fable 5.1 | 相对优势 |
|---|---:|---:|---|
| **SciCode · AA 独立评测** | 56.5% | **63.1%** | Fable 高 6.6 个百分点。[榜单](https://artificialanalysis.ai/evaluations/scicode) |
| **TB-Science 0.1 · OpenAI 发布表** | **64.6%** | 52.6% | Astra 高 12.0 个百分点。[发布与设置](https://openai.com/index/gpt-6-astra/) |

注：SciCode 为 Astra max、Fable max with fallback。9/9 补核时，TB-Science 维护方公开榜尚未收录这两款模型，上行保留厂商披露属性；它是独立科学任务集，不是 TB4 的子榜。[任务定义](https://www.terminal-bench-science.ai/announcement) · [收录与详细口径](frontier-models-2026-09-08-evidence.md#s5)

## 03 纵向迭代：前代到本代，能力究竟变在哪里

**OpenAI 的增量集中在复杂执行与长输入利用，Anthropic 强化分析推理，Google 以 20 天的版本间隔推进 Flash 工作能力。** 同一轮升级并未均匀改善所有任务：已有高分项目增幅较小，部分可靠性指标甚至回落。

注：得分差以百分点表示，各行在同一来源、同一评测版本内比较。厂商对照未必固定新旧模型计算预算。

### OpenAI｜Sol → Astra：执行上限提高，对自身能力的误述减少

9 月 3 日 Astra 发布，距 7 月 9 日 Sol 发布相隔 56 天。科学工作流和长上下文检索增幅较大，DeepSWE 软件工程增幅只有 1.4 个百分点。

| 能力 / 同版本评测 | GPT-5.6 Sol | GPT-6 Astra | 增量 | 来源属性 |
|---|---:|---:|---:|---|
| 复杂终端 · TB4 / AA · max | 39.9% | **59.1%** | **+19.2** | AA 独立评测 |
| 跨应用流程 · AutomationBench | 18.1% | **41.4%** | **+23.3** | OpenAI 发布表 |
| 科学终端 · TB Science 0.1 | 22.4% | **64.6%** | **+42.2** | OpenAI 发布表 |
| 交互式抽象推理 · ARC-AGI-3 | 7.8% | **99.9%** | **+92.1** | OpenAI 发布表；执行设置有变化 |
| 数学 · FrontierMath Tier 4 v2 | 83.0% | **97.6%** | **+14.6** | OpenAI 发布表 |
| 长上下文 · MRCR v2 · 8-needle · 512K–1M | 73.8% | **96.3%** | **+22.5** | OpenAI 发布表 |
| 软件工程 · DeepSWE v1.1 | 72.7% | 74.1% | +1.4 | OpenAI 发布表 |
| GUI · OSWorld 2.0 离线集 · 部分得分 | 65.7% | 72.6% | +6.9 | OpenAI 发布表 |
| 可靠性 · 内部幻觉评测（低者更好） | 12.2% | **4.2%** | **−8.0** | OpenAI 内部评测；非线上总体错误率 |

来源：[AA TB4](https://artificialanalysis.ai/evaluations/terminalbench-v4-0) · [OpenAI 发布表](https://openai.com/index/gpt-6-astra/)。官方表取各推理档位最高结果；AutomationBench 与 AA 版本不同。ARC-AGI-3 执行框架调整了两项设置，涨幅包含系统贡献。详细设置见[附录](frontier-models-2026-09-08-evidence.md#s7)。

**能力幻觉减少，是执行能力之外的可靠性进步。** OpenAI 披露，Astra 对自身能力及可用操作条件作出误导性陈述的概率约为 Sol 的三分之一。这意味着模型更少把“做不到的操作”说成“可以完成”，有望减少错误委派；该内部指标与一般知识问答准确率不同。[发布说明](https://openai.com/index/gpt-6-astra/) · [系统卡](https://deploymentsafety.openai.com/gpt-6-astra)

**GUI 任务已出现能力与速度双改善。** OSWorld 延迟模拟从约 75 分钟缩至 40 分钟，同时得分由 65.7% 升至 72.6%；这是特定离线任务集上的进步。Astra 标准 API 输入／输出价为每百万 token $10／$50，任务经济性还取决于调用量。[发布与评测设置](https://openai.com/index/gpt-6-astra/)

### Anthropic｜Fable 5 → 5.1：推理与知识交付进步，可靠性并非齐升

9 月 1 日 AA 发布评测中的同口径对照如下。Fable 5.1 使用默认 fallback，约 4% 输出 token 由 Opus 4.8 / Opus 5 提供，结果代表这一服务配置。

| 能力 / 指标 | Fable 5 | Fable 5.1 | 变化 |
|---|---:|---:|---|
| 综合能力 · 发布时 AA 指数 | 62 | **66** | +4 分；不能与期末 v4.3 直接相减 |
| 高难知识推理 · HLE | 55.5% | **59.1%** | +3.6 个百分点 |
| 知识工作 · GDPval-AA v2 | 1,723 Elo | **1,853 Elo** | +130 Elo |
| 文档等专业交付 · AA-Briefcase | 1,572 Elo | **1,694 Elo** | +122 Elo |
| 可靠知识 · AA-Omniscience 准确率 | 65.4% | 67.2% | +1.8 个百分点；该项综合指数持平 |

来源：[AA 发布评测](https://artificialanalysis.ai/articles/claude-fable-5-1)。前代 Elo 按原文增量换算；榜单更新会改变 Elo，故本表与期末快照分开使用。Omniscience 更多作答也带来更多错误，净得分持平。

**Fable 5.1 的分析与推理更强，专业交付尚未拉开与 Opus 5 的差距。** 发布时两项知识工作评测与 Opus 的差距仍在误差范围内；Briefcase 细项显示分析质量更高、呈现质量较弱。更积极作答增加了正确答案，也增加了错误，可靠知识的净得分没有提高。

**能力提升伴随更长的输出与更高成本。** 发布评测中，max 输出 token 约为前代 1.7 倍，任务成本增加约 20%；较低推理档位的取舍见[效率比较](#s4)。

### Google｜Flash 3.6 → 3.7 → 3.8：连续推进工作能力，旗舰差距仍不均匀

8 月 13 日推出 3.7，20 天后推出 3.8。3.6 → 3.7 的主要增量已覆盖代码修复和文档理解，3.8 继续增强这些能力，同时提高新终端任务和 GUI 得分。

| 能力 / 指标 | 3.6 Flash | 3.7 Flash | 3.8 Flash | 最近一代变化 |
|---|---:|---:|---:|---|
| 长程软件工程 · DeepSWE v1.1 | 49.0% | 65.3% | **73.7%** | +8.4 个百分点 |
| 文档理解 · GDP.PDF · 全部通过率 | 22.0% | 34.0% | 35.0% | +1.0 个百分点 |
| 公开终端任务 · TB2.1 | — | 85.8% | **89.4%** | +3.6 个百分点 |
| 新终端任务 · TB4 | — | 11.2% | **19.1%** | +7.9 个百分点 |
| 知识工作 · GDPval-AA v2 | — | 1,482 Elo | 1,545 Elo | +63 Elo |
| GUI · OSWorld 2.0 · 部分得分 | — | 50.6% | 59.0% | +8.4 个百分点 |

来源：[3.7 发布](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/) · [3.8 评测表](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/)。表中汇集自测及外部数据；OSWorld 为补丁前任务与批量工具调用，与 OpenAI 离线集不同。DeepSWE 两次发布的累计增量受配置变化影响。

**Flash 的持续进步以编程和操作任务最突出，文档全部通过率的增幅已收窄。** 新终端任务上，它较前代提升，但仍落后旗舰；新旧榜的相对位置变化见[第 07 节](#s7)。

AA 发布评测中，3.7 → 3.8 high 的旧版综合分也从 56 升至 59，增量主要来自工具与工作任务。20 天间隔反映了 Flash 的产品迭代速度，公开资料尚未拆分基座、后训练及 agent 循环各自的贡献。[独立评测](https://artificialanalysis.ai/articles/gemini-3-8-flash)

### Meta｜Spark 1.2 → 1.3：编程增强，长上下文与知识表现有回落

8 月 5 日到 9 月 2 日相隔 28 天。AA 同次发布评测中，xhigh 的 TB2.1 从 80% 升至 85%、SciCode 从 56% 升至 59%；但 AA-LCR 从 83% 降至 79%，Omniscience 准确率从 45% 降至 42%，并伴随更多弃答。单任务成本从 $0.40 升至 $0.55。**这是能力结构发生变化的例子：编程方向更强，同时存在其他维度的取舍。**[AA：Spark 1.3](https://artificialanalysis.ai/articles/muse-spark-1-3)

### 其他厂商：后训练追赶与架构效率并行

| 厂商 | 可比的能力增量 | 本期迭代方向 |
|---|---|---|
| **智谱** | GLM-5.2 → 5.3：DeepSWE 46.2% → **66.9%**；TB3 4.6% → **28.3%**。 | **基座不变，后训练仍有大幅收益**；Flash 承接较低成本位置。[模型卡](https://huggingface.co/zai-org/GLM-5.3) |
| **xAI** | Grok 4.5 → 4.6：DeepSWE 54.0% → 65.9%；TB3 15.7% → 26.0%。 | 补充训练与 agent RL 联合增强长任务能力。[官方对照](https://x.ai/news/grok-4-6) |
| **Qwen** | 3.7-Max → 3.8-Max：TB2.1 74.5% → 86.6%；DeepSWE 21.6% → 56.6%。 | 后训练追赶代码能力，同时推进 Flash-Next 混合架构。[模型卡](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) |
| **Kimi** | K3 报告相对 K2 联合改变规模、架构与训练方案。 | 架构与扩展效率见第 05 节；期末综合能力处于开放权重前列。[报告](https://arxiv.org/abs/2607.24653) |
| **DeepSeek** | V4 Pro 0813 的 DeepSWE 为 62.7%，来自 GLM 比较表；前代可比基线不足。 | 编程增强与视觉扩展并行。[公开比较](https://huggingface.co/zai-org/GLM-5.3) |

**后训练与工程系统仍在释放已有基座的潜力。** GLM 的同基座对照尤其明确：较大的软件工程增量并不总要等待新一代预训练模型。MiniMax／fal 的视频迭代见第 08 节，Inkling 的模型压缩见第 04 节；其他节点与历史基线收于[附录](frontier-models-2026-09-08-evidence.md#s7)。

## 04 效率突破：相似能力降本，最高档位仍有溢价

### 同分模型之间，任务成本仍相差数倍

**Astra 与 Fable 综合同分时，AA 任务成本约低 57%；GLM-5.3-Flash 与 Terra 同为 42 分，成本约为后者的 18%。** 综合能力相近并未消除价格差异，知识交付等专项优势仍可能对应溢价。

| 模型 / 配置 | AA v4.3 | 平均任务成本 |
|---|---:|---:|
| Astra · max | 53 | **$3.26** |
| Fable 5.1 · max with fallback | 53 | $7.63 |
| GLM-5.3-Flash | 42 | **$0.25** |
| Terra · max | 42 | $1.40 |
| Luna · max | 38 | $0.18 |

注：AA 按指数权重计算输入、缓存、推理与答案 token 的平均 API 花费；不是成功交付成本，亦不含人工和外部工具。表为选定配置的 9/8 快照，同分不保证专项能力相同。[AA 方法](https://artificialanalysis.ai/methodology/intelligence-benchmarking) · [Astra](https://artificialanalysis.ai/models/gpt-6-astra) · [Fable](https://artificialanalysis.ai/models/claude-fable-5-1) · [GLM Flash](https://artificialanalysis.ai/models/glm-5-3-flash) · [Terra](https://artificialanalysis.ai/models/gpt-5-6-terra) · [Luna](https://artificialanalysis.ai/models/gpt-5-6-luna)

### 较低推理档位保留了大部分能力，成本改善更明显

| 同次发布评测中的比较 | 能力变化 | 任务成本变化 |
|---|---|---|
| **Flash 3.6 high → 3.8 low** | 旧版综合分均为 52 | **降低约 30%** |
| Flash 3.7 high → 3.8 high | 旧版综合分 56 → 59 | 约 $0.40 → $0.58 |
| **Fable 5.1 max → xhigh** | 发布时综合分 66 → 65 | $3.76 → **$2.72，降低约 28%** |

来源：[Flash 发布评测](https://artificialanalysis.ai/articles/gemini-3-8-flash) · [Fable 发布评测](https://artificialanalysis.ai/articles/claude-fable-5-1)。各行使用同次评测口径，不能与上表 v4.3 分数及任务成本直接相减。

**新一代模型把相似能力带到更低预算，更高档位则继续用计算换取上限。** Fable max 最后 1 分的额外开销，说明综合能力在高预算区间的边际收益已收窄；这仍可能对少数难任务有价值。

Astra 也有特定任务的代际降本证据：OpenAI 披露其较低成本配置在 TB-Science 得分 61.1%，高于 Sol 的最高成绩 22.4%，估算 API 成本低约 27%。结果限于该任务集与厂商设置，维护方尚未补入 Astra。[评测说明](https://openai.com/index/gpt-6-astra/)

### 模型压缩与运行软件优化，提供两条额外的降本路径

**小模型已经能够保留部分高端能力。** Inkling-Small 的激活参数从 41B 减至 12B，HLE text 从 29.7% 升至 31.6%。训练时间与配方也有变化，结果证明的是模型大小与这项能力关系改善，并非单变量蒸馏收益。[官方发布](https://thinkingmachines.ai/news/inkling-small/)

**同一模型还可以通过更好的软件实现减少开销。** 算子和调度优化减少数据搬运、等待与重复计算：OpenAI 披露 Sol 参与生产内核优化，使端到端服务成本下降 20%；H3 在相同权重、8×B300、相同提示与种子下，完整视频返回耗时从 82.2 秒缩至 56.9 秒，减少 30.8%。后者没有减少去噪步数或使用量化。[OpenAI](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/) · [H3 实测](https://vllm.ai/blog/2026-09-01-minimax-h3-production-serving)

**效率进步正在同时发生于模型设计和计算系统，用户价格还叠加了商业定价。** 例如 Flash 3.8 年内优惠价为标准价的一半，这部分降价并非技术资源消耗减半。架构训练效率见第 05 节，视频蒸馏见第 08 节；训练吞吐、参数规模和优惠价格的详细对照见[附录](frontier-models-2026-09-08-evidence.md#s8)。[Google 定价](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/)

## 05 架构趋势：循环深度与混合架构改变计算分配

### Looped Transformer：重复使用参数，也能增加计算深度

普通深层模型依次经过不同参数层；**Looped Transformer 在隐状态上重复使用部分模块，用更多内部计算增加有效深度。** 这与生成更长文字推理的计算位置不同。2025 年 recurrent-depth 研究已展示这一方向，近期动态中的两项研究进一步涉及计算效率与工具调用。[基础论文](https://arxiv.org/abs/2502.05171)

| 研究 | 本期新增证据 | 实验范围 |
|---|---|---|
| **SMELT · 9/1** | 匹配每 token FLOPs、非 embedding 参数与 KV cache，跨规模拟合训练 FLOPs 节省 **6.8%—18%**。 | 受控论文实验，尚非前沿厂商生产训练收益。[论文](https://arxiv.org/abs/2609.01343) |
| **组合工具调用 · 8/17** | 在 API-Bank、BFCL、NESTful 上，循环与可调计算对依赖链任务表现出收益。 | 下游工具任务实验；推理预算影响收益幅度。[论文](https://arxiv.org/abs/2608.18171) |

**Astra 的公开披露约束了计算深度范围，尚未揭示循环结构。** 9/2，OpenAI 首席科学家 Jakub Pachocki 表示，包括 Astra 在内的前沿模型，计算图深度与 GPT-4 的差距在两倍以内；没有明确确认或否认 recurrent depth，也未披露循环层和次数。[原帖](https://x.com/merettm/status/2095023204993490967)

更确定的变化是，**可读推理文本对模型计算的代表性正在减弱。** Pachocki 在 9/6 官方文章中指出，模型不依赖文字推理也变得更强，且更善于操作自身推理过程。这影响 CoT 监控的解释力；其原因可能包括内部计算与工具交互，尚不能具体归因于循环架构。[OpenAI 官方文章](https://openai.com/index/an-alien-mind/)

### Kimi 与 Qwen：上下文处理、层间连接和知识存储分工更细

**Kimi K3 的效率收益来自多项设计与训练方案的组合。** 报告披露 KDA 与 MLA 混合、Attention Residuals 和 MoE；相对论文中的 K2 基线，约 2.5 倍训练扩展效率是架构、数据与配方的共同拟合结果。激活参数同时由约 32.6B 增至 104.2B，该指标不等同于线上推理降本。[技术报告](https://arxiv.org/abs/2607.24653)

**Qwen3.8-Flash-Next 将序列处理与知识存储进一步拆分。** Gated DeltaNet 与局部注意力组合，另用 Gated Residual 改变层间连接，并配置 n-gram embedding。主体标为 125B／6B 激活，另列 51B n-gram embedding 与 4B MTP；单一总参数数字已难以完整描述计算开销。[模型卡](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)

这两类混合架构与深度循环解决不同问题：前者重新安排上下文和层间信息的处理，后者重复使用模块增加有效深度。**本期可量化的生产训练线索来自 Kimi 的联合方案；循环深度的效率证据仍主要来自论文实验。** 结构分类及统计边界见[附录](frontier-models-2026-09-08-evidence.md#s9)。

## 06 AI4AI：训练供给与计算工程先兑现收益

**AI4AI 已进入模型厂商的实际研发，但收益最清楚的环节仍有明确的验收标准。** 任务环境可以检验可解性，内核可以测试正确性和速度，芯片模块可以验证电路结果。相比之下，选出有价值的研究问题、把小规模结果迁移到下一代模型，仍更依赖人类判断。

### 厂商实践：从训练材料扩展到方法、软件与芯片

| 厂商 | 已披露的实践覆盖 | 成熟度与本期位置 |
|---|---|---|
| **OpenAI** | 多日实验、训练监控与排障、生产内核；Jalapeño 芯片方案、电路验证及配套软件。 | **研发与生产使用**；芯片计划年末部署。[研究](https://openai.com/index/research-acceleration-view-inside-openai/) · [芯片](https://openai.com/index/jalapeno-first-results/) |
| **Anthropic** | 训练故障定位、代码生成与审查、训练代码优化、弱到强监督、自动对齐方法研究、RL 环境审核。 | **工程使用＋研究实验**；8/28、8/31 补充方法与环境进展。[工程](https://www.anthropic.com/institute/recursive-self-improvement) · [方法](https://www.anthropic.com/research/automated-researchers-mitigate-alignment-failures) |
| **Google** | Flash 的模型评估与改进循环；AlphaEvolve 的训练内核、调度与 TPU 设计。 | **本期研发披露＋期前生产基础**。[Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) · [AlphaEvolve](https://deepmind.google/blog/alphaevolve-impact/) |
| **智谱** | 长任务环境、奖励与验证器生成，视觉数据与自验证轨迹；GLM-5.3 协助开发 Flash 内核和推理引擎。 | **官方训练流程与实际研发**，环境构建保留人工参与。[5.3](https://z.ai/blog/glm-5.3) · [Flash](https://z.ai/blog/glm-5.3-flash) |
| **Kimi** | 任务合成与工作区初始化；早期 K3 参与内核优化；MiniTriton 编译器与小模型芯片设计。 | **训练、研发及原型案例**；芯片为 RTL 仿真。[训练](https://arxiv.org/html/2607.24653v1#S4.SS2) · [系统案例](https://arxiv.org/html/2607.24653v1#S7) |
| **Meta** | REA 推荐模型实验；KernelEvolve 跨硬件内核及专用模型后训练；AIRA₃ 微调竞赛。 | **期前生产基础＋本期能力信号**。[REA](https://engineering.fb.com/2026/03/17/developer-tools/ranking-engineer-agent-rea-autonomous-ai-system-accelerating-meta-ads-ranking-innovation/) · [内核](https://engineering.fb.com/2026/04/02/developer-tools/kernelevolve-how-metas-ranking-engineer-agent-optimizes-ai-infrastructure/) |
| **xAI** | 模型生成补充训练数据；Grok 4.5 重生成 SFT 轨迹，模型检查并筛选。 | **官方训练流程**。[技术说明](https://x.ai/news/grok-4-6) |
| **Qwen** | PaperBench 科学复现与 MLS-Bench-Lite 工程评测改善。 | **能力评测**，尚无所引材料中的自家生产贡献披露。[模型卡](https://huggingface.co/Qwen/Qwen3.8-2.4T-A95B) |

注：历史生产基础与本期新增披露分开列示。Kimi 的任务生成 agent 未明确均由 K3 驱动，编译器和芯片原型与实际内核研发分别计量。各家完整实践、日期和结果见[附录](frontier-models-2026-09-08-evidence.md#s10)。

### 自动生成环境与优化计算系统，已形成两类实际反馈

**训练供给的自动化从“造题”延伸到“验证能否学到正确行为”。** 智谱由 research agent 构建长任务环境，judge agent 检查可解性，另生成验证器并检查奖励漏洞；部分任务直接合成 RL 奖励。Anthropic 的训练前、训练中环境审查也表明，生成能力扩张后，验收与奖励质量开始成为限制。[智谱训练流程](https://z.ai/blog/glm-5.3) · [Anthropic 环境审核](https://www.anthropic.com/news/improving-alignment-security-efforts)

**计算工程的成果已能反哺模型运行。** OpenAI 的生产内核、智谱的 Flash 推理引擎、Kimi 早期检查点参与后期内核优化，均有实际研发使用披露。Jalapeño 进一步把工作扩展到芯片与配套软件，选定软件模块获得 1.5—1.8 倍加速；该结果仍是模块级收益。[OpenAI 芯片结果](https://openai.com/index/jalapeno-first-results/)

### 研究方案筛选已有实验收益，开放研究仍难形成稳定产出

正向证据开始触及研究取舍：AI Research Preference Models 的一种配置以 **15 小时达到基线 24 小时的表现**；AI4AI-Bench 用重新训练与隐藏评估验证改动，最佳归一化得分为 **0.250**，高于原仓库基线 0.1，算法改动优于仅调配置。两者均属受限论文实验。[方案选择](https://arxiv.org/abs/2608.13940) · [AI4AI-Bench](https://arxiv.org/abs/2608.20318)

反向证据同样明确：在两个未公开研究问题的影子评估中，agent 完成了大量工程任务，却未给出原作者认可的实质研究答案；OpenAI 成功完成的 4—8 小时任务中，超过一半仍接受过人类介入。**工程产出增加已经可见，持续产生有价值的研究发现尚未得到同等程度的证明。**[研究案例](https://arxiv.org/abs/2607.27191) · [实际研发](https://openai.com/index/research-acceleration-view-inside-openai/)

## 07 评测前沿：持续正确、独立验收与未见任务更有区分度

**一次答对与持续交付，正在产生不同的模型排序。** 近期评测把持久工作区、完整成果包和隐藏任务纳入考核，暴露出单轮高分没有覆盖的失败方式。

### 持续任务会累积错误，模型也未必知道自己失败

| 评测 | 设计与结果 | 新增区分度 |
|---|---|---|
| **FrontierChallenge · 8/25** | 97 项科研任务要求同时交付代码、分析、图表；最佳配置完成 **20 项（20.6%）**。未通过的 Claude Code 轨迹中，75.5% 仍声称完成。 | 中间产物与完整成果包存在断层，失败识别本身也是能力缺口。[论文](https://arxiv.org/html/2608.24979v1) |
| **EvoCode-Bench · 7/29 动态收录** | 26 个任务、227 轮需求；Opus 4.6 单轮 SR 78.9，多轮 MT@4 44.0，排名从第一降至第三；完整完成率 34.6%。 | 维护自己留下的代码状态，比从参考状态继续开发更难，回归错误随轮数累积。[论文](https://arxiv.org/html/2605.24110v1) |
| **Mystery Game Puzzles · 8 月动态** | Epoch 隐去游戏身份、提示与轨迹，以 100 个局面测试下一步选择。 | 隐藏范围从答案推进到任务类型，降低针对性准备的空间。[方法](https://epoch.ai/benchmarks/mystery-game-puzzles) |

注：前两行是论文所测配置，不能代表 Astra／Fable 5.1 的当前成绩。EvoCode 为期前论文，SR 从参考状态继续，MT@4 为四次尝试、多轮失败即止得分，两种指标的任务条件不同。科研工作流 TB-Science 的定义与当前覆盖见第 02 节。

### 同一个模型，执行框架就能显著改变得分

**状态管理已经是模型能力能否发挥出来的重要变量。** OpenAI 7 月披露，仅为 Sol 开启保留推理与上下文压缩，ARC-AGI-3 公开集 RHAE 从 **13.3% 升至 38.3%**，输出 token 减少约六倍。此前丢弃推理、截断历史，会迫使模型反复理解同一游戏。该公开集指标与 Astra 发布表分数不同。[固定模型实验](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/)

**自动改写框架的收益，尚未稳定迁移到新任务与新模型。** HarnessDev 冻结框架后在隐藏任务上测试；开发期提升只有部分迁移，换执行模型后也未稳定保持。这意味着针对单次评测优化成功，与得到可复用的 agent 系统仍有距离。[HarnessDev，9/1](https://arxiv.org/html/2609.01437v1)

计算预算也影响所谓的方法进步：一项 1.5B—7B 模型的数学研究，在等生成 token 成本下比较七种方法，未发现其可靠胜过重复采样取多数答案。它是小模型实验，但为自审、反思等方法提供了直接的成本对照。[等成本实验](https://arxiv.org/html/2607.28576v1)

### Flash / Muse 争议：旧榜竞争位置没有稳定延续到新任务

| Google 发布表 | Flash 3.8 | Sol | Flash 相对差距 |
|---|---:|---:|---:|
| 旧终端任务 · TB2.1 | 89.4% | 88.8% | +0.6 个百分点 |
| 新终端任务 · TB4 | 19.1% | 37.3% | **−18.2 个百分点** |

来源：[Google 发布表](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) · [方法说明](https://deepmind.google/models/evals-methodology/gemini-3-8-flash)。TB2.1 汇集 Gemini 自测与 Terminus 2 外部榜单；TB4 引用官方榜的最佳档位，非固定预算实验，亦非 AA max 配置。

SemiAnalysis 对 Flash 及 Muse Spark 1.3 提出的解释是，厂商可能购买与公开基准高度相似的 RL 环境数据，造成任务结构过拟合。**跨榜相对位置的落差已有公开数字，数据采购及其因果解释仍是未经独立证实的指控。**[所引帖文](https://x.com/SemiAnalysis_/status/2097112791471522292)

这一争议提出了比原题泄漏更广的问题：即使没有使用原题，训练环境也可能与测试任务足够接近。AA v4.3 已将含私有题目或答案的评测权重提高到 **45%**，保留未见任务的测量价值正在上升。[AA 更新](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v4-3)

### 新基准也在修复环境噪声与服务差异

**TB4 的更新同时包含任务更替与测量降噪。** 它统一 8 小时上限、校准资源，移除 8 项任务并修复 19 项；移除原因只有两项是饱和，其余还包含公开解法、拒绝和兼容性问题。新旧版本的分数变化因此不只是模型变化。[维护说明](https://www.tbench.ai/news/terminal-bench-4-0)

AA 的 Endpoint Accuracy Index 则固定开放模型、以自托管为参考，衡量不同服务端点的能力损失。**同名模型的可交付能力，正在受到任务设计、执行框架和服务实现的共同检验。**[端点保真方法](https://artificialanalysis.ai/methodology/endpoint-accuracy-index)

## 08 多模态边界：短片质量改善，交互控制开始形成新能力

**本期的增量沿两条路径展开：H3 衍生模型改善音视频质量与生成速度，Director 和 Atlas 把生成推进到可在线干预的过程。** 前者更接近内容生产效率，后者开始改变产品的交互形态。

### MiniMax H3 → fal H3 Max：开放底座承接二次能力开发

MiniMax H3 统一使用文本、图像、视频和音频参考，原生输出同步音视频。开放的 **33B H3-Base** 支持首末帧、多参考控制和 768p 输出；完整 2K 流程仍包含托管组件。[官方模型卡](https://huggingface.co/MiniMaxAI/MiniMax-H3)

**fal 在开放权重上增加后训练与推理优化，H3 Max 的质量点估计高于原版。** 8/26 发布文披露提示遵循与视觉质量改善；9/9 补充的 AA 独立榜单提供了任务级参照：

| AA 视频 Arena · 含音频 | MiniMax H3 服务配置 | fal H3 Max |
|---|---:|---:|
| 文生视频 | 1,227 Elo（±7） | **1,235 Elo（±10）** |
| 图生视频 | 1,187 Elo（±8） | **1,200 Elo（±9）** |

注：括号为榜单 95% 区间半宽，存在重叠，尚不足以确认成对显著优势。Max 文生视频位于前列，图生视频点估计第一；两榜分数不跨榜比较。此为 9/9 补充快照。[文生榜](https://artificialanalysis.ai/video/leaderboard/text-to-video) · [图生榜](https://artificialanalysis.ai/video/leaderboard/image-to-video)

**开放底座上的能力增值，已能由专业服务商继续完成。** fal 的投入同时涉及后训练数据、模型行为和推理实现，因此 H3 Max 的价值超过单纯托管。其官方报告 5 秒视频约 3 秒内生成；Max Turbo 另侧重速度与成本，质量排名与 Max 分开使用。[fal 发布](https://fal.ai/learn/devs/introducing-h3-max-by-fal) · [产品线](https://fal.ai/minimax-h3-max)

### 生成快于播放，与用户实时控制是两道不同门槛

**FastH3 已在完整片段生成上跨过播放速度。** FastVideo 将 H3 蒸馏至四步，再由 vLLM-Omni 服务；8×B300 上，10.1 秒音视频约 8.7 秒返回，RTF（生成耗时／成片时长）约 0.86。它与第 04 节原权重的软件加速属于同一次联合披露的两层结果；蒸馏改变了模型，质量保留另需评估。[联合实测](https://vllm.ai/blog/2026-09-01-minimax-h3-production-serving)

注：测试计时到完整 MP4 返回，不是首帧或流式延迟；两组提示与种子不同，不能直接相除计算蒸馏加速倍率。FastH3 也不同于 fal H3 Max。原始配置与精确值见[附录](frontier-models-2026-09-08-evidence.md#s11)。

**fal 发布的 H3 Max Director，把短片生成扩展到可在线改写提示的连续视频流。** 角色、场景和叙事上下文可以延续，产品从一次性交付片段变成持续响应输入。此时首帧延迟、动作响应和长时保持比整片 RTF 更直接地决定体验；连续叙事仍不同于可验证的三维状态。[Director 官方端点](https://fal.ai/models/minimax/h3-max/director)

### World Labs Atlas：几何控制、场景重建与实时导航结合

**Atlas 把生成与空间重建放进同一底座，允许用明确的几何轨迹控制视角。** 9/1 披露的自回归扩散架构统一文本、图像、视频与 3D，支持新视角生成、稀疏视角重建和显式 3D 输出。用途由生成外观连贯的视频，延伸到按空间路径探索场景并交付几何数据。[World Labs 发布](https://www.worldlabs.ai/blog/atlas)

厂商测试中，相机轨迹越复杂，Atlas 相对所测视频模型的优势越大；稀疏视角重建也优于所列专用模型。这里的优势同时来自模型与原生控制接口。

注：评测由 World Labs 组织；Atlas 接收相机轨迹，竞品接收文字描述，配置与适用范围见[附录](frontier-models-2026-09-08-evidence.md#s6)。

**9/9 的官方演示进一步展示了实时生成与导航。** 据日报收录的 World Labs 和 Justin Johnson 帖文，优化后的 Atlas 在 NVIDIA B200 与 AMD MI355X 上性能相近，李飞飞转发演示。该信号指向同一模型的跨平台实时运行，尚缺统一配置的独立测试。[World Labs](https://x.com/theworldlabs/status/2097386577236476239) · [Justin Johnson](https://x.com/jcjohnss/status/2097423245742141907) · [李飞飞](https://x.com/drfeifei/status/2097429460115218568)

**Director 的增量是连续内容控制，Atlas 的增量是空间约束与几何表示。** 实时化使用户有机会边行动、边观察、再改变行动，但长时一致性和准确物理预测仍缺少充分的公开验证。同期 H3-World 的游戏控制适配、Runway Solaris 的界面生成，分别扩展动作与界面方向，详见[附录](frontier-models-2026-09-08-evidence.md#s11)。

## 09 下一期：三项最可能改变判断的证据

| 优先跟踪 | 关键新增证据 | 将改变什么判断 |
|---|---|---|
| **新任务上的完整交付** | Astra／Fable 的 TB-Science 维护方复测、持续任务结果与真实接管率；Flash／Muse 在轮换任务上的表现。 | 旗舰优势能否跨任务延续，模型升级能否减少监督负担。 |
| **能力—成本曲线** | 新旧模型同预算对照，以及相同成功率的总成本与耗时；循环结构的官方披露与规模化消融。 | 进步来自更有效的计算，还是主要来自更多计算。 |
| **AI4AI 的生产迁移** | 自动环境的审核成本、研究成果在更大模型上的迁移、工程优化的实际部署收益。 | 局部自动化能否形成持续的模型研发优势。 |

## 10 数据与来源

正文采用主体 9/8 截面，9/9 补充已就近标注。模型配置、实验条件、厂商完整实践与补充案例收于[参考资料与数据说明](frontier-models-2026-09-08-evidence.md)。动态榜单可能继续更新。

