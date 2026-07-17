# 前沿模型周报 · 第6期 | 2026.07.04 — 07.11

> 本周不是一个“模型发布周”，而是一次模型前沿定义的切换：前沿能力正在从“单模型得分”迁移到“任务系统能力”。GPT-5.6 把模型、Agent、办公入口和 API 工具链打包发布；Meta Muse Spark 1.1 与 Muse Image / Video 把 Meta 的模型路线从 Llama 开源叙事推向闭源 API 与社交分发；SWE-1.7、LongCat-2.0、Grok 4.5 则说明 coding agent 的竞争核心已经变成真实工程环境、长程稳定性与成本控制。
>
> 置信度：**高** = 官方 blog / 技术报告 / benchmark 可核验；**中** = 官方社媒或产品页确认，但模型卡、benchmark、价格表尚未完整公开；**低** = 单一信号，仅作跟踪，不做强判断。

---

## 信号矩阵

> 横轴：能力边界是否上移；纵轴：部署曲线是否变陡。真正值得关注的不是“谁又发了模型”，而是谁把模型推进到更复杂任务、更低成本或更强分发入口。

| 前沿变化 | 本周代表信号 | 能力边界变化 | 部署曲线变化 | 判断 |
|---|---|---|---|---|
| **任务操作系统化** | GPT-5.6 + ChatGPT Work + Microsoft 365 Copilot + Programmatic Tool Calling | 从问答 / 单步代码进入跨应用、跨文件、数小时工作流 | Sol / Terra / Luna 分层，multi-agent beta，工具调用程序化 | 本周最强信号 |
| **Agentic coding 重排** | SWE-1.7、LongCat-2.0、Grok 4.5 | 从“会写代码”进入真实终端、代码库探索、验证与恢复 | Cerebras 1000 TPS、MoE 动态激活、Cursor 低价 MoE | 评估体系正在变化 |
| **Meta 闭源分发浮出水面** | Muse Spark 1.1、Muse Image / Video | Muse Spark 1.1 AA Intelligence Index **51**、Coding Index **71**，叠加媒体生成 + 工具使用 | Meta Model API、Meta AI、Instagram、WhatsApp；$1.25 / $4.25 定价 | 低价 agentic API 信号强 |
| **推理经济继续前移** | Nemotron-Labs-Diffusion、GPT-5.6 Terra / Luna、LongCat MoE | 不只靠更大模型，而靠解码范式、路由和动态激活 | 4× 吞吐、1/16 成本口径、33B–56B 激活参数 | 成本成为能力的一部分 |
| **非聊天型前沿扩张** | GPT-Live、Robostral Navigate、SensorFM、Seedream 5.0 Pro | 语音连续交互、单 RGB 具身导航、健康传感器表征、设计编辑 | 前台低延迟 + 后台委托，模拟训练，垂直产品分发 | 第二曲线开始清晰 |

---

## 本期核心判断

### 1. GPT-5.6 的重点不是 Sol，而是“模型 + 工作流系统”合并发布

OpenAI 发布 GPT-5.6 系列：旗舰 **Sol**、平衡型 **Terra**、成本最优 **Luna**。如果只看 Sol 在 Agents' Last Exam **53.6**、Artificial Analysis Coding Agent Index **80**、BrowseComp **92.2%**、OSWorld 2.0 **62.6%**，这仍然像一次常规前沿模型升级。但本周真正重要的是 OpenAI 同时发布或绑定了 ChatGPT Work、Microsoft 365 Copilot preferred model、Programmatic Tool Calling、multi-agent beta、max / ultra 等系统能力。

这意味着 GPT-5.6 的竞争单位已经不是“一个模型 API”，而是一个任务执行系统：Sol 负责最高智能，Terra / Luna 负责把前沿能力下沉到更便宜的高频任务，ChatGPT Work 负责跨应用交付，Microsoft 365 Copilot 负责办公入口，Responses API 负责开发者集成。前沿模型的商业化不再是“把更强模型卖给开发者”，而是把模型嵌入组织工作流，成为默认执行层。

**关键数据**

| 指标 | GPT-5.6 Sol / 系列表现 |
|---|---|
| Agents' Last Exam | **53.6** |
| Artificial Analysis Coding Agent Index | **80** |
| BrowseComp | **92.2%** |
| OSWorld 2.0 | **62.6%** |
| API 价格 | Sol **$5 / $30**，Terra **$2.5 / $15**，Luna **$1 / $6** per 1M input / output tokens |
| 系统能力 | Programmatic Tool Calling、multi-agent beta、max / ultra |
| 分发入口 | ChatGPT Work、Codex、Microsoft 365 Copilot、Responses API |

**非共识点**：GPT-5.6 的真正威胁不是 benchmark 上压过某个模型，而是把“多 agent 并行、工具调用、文档/表格/幻灯片生成、企业权限治理”做成默认产品能力。垂直 agent 创业公司如果只靠接入最强模型，会更快被平台内置功能挤压；壁垒必须转向行业数据、验证器、权限系统和交付模板。

---

### 2. Coding Agent 的竞争主轴从“代码能力”转向“真实工程环境”

本周 SWE-1.7、LongCat-2.0、Grok 4.5 同时出现，使 coding agent 的评估焦点进一步从 SWE-Bench 式通过率转向真实工程环境。Cognition 的 SWE-1.7 基于 Kimi K2.7 base 继续训练，在 FrontierCode 1.1 Main 达 **42.3%**、Terminal-Bench 2.1 达 **81.5%**、SWE-Bench Multilingual 达 **77.8%**，并通过 Devin + Cerebras 提供 **1000 TPS**。美团 LongCat-2.0 则用 **1.6T MoE**、**33B–56B** 动态激活参数、**1M context** 和国产 **5 万卡**训练 / 推理集群，展示国产算力栈承接 agentic coding 模型的可能性。Cursor 与 SpaceXAI 的 Grok 4.5 则把 Cursor 用户交互数据、工具使用任务和更广义电脑工作结合起来，价格为 **$2 / $6** per 1M input / output tokens，fast 版 **$4 / $18**。

这些模型共同说明，coding agent 的前沿不再只是“能不能改对一道题”，而是能否在大型代码库中持续探索、压缩上下文、选择工具、验证结果、从失败中恢复，并控制每次任务的 token、延迟与计算成本。

**Benchmark 横向对比**

| 模型 | 核心赛道 | 关键数据 | 变化含义 |
|---|---|---|---|
| GPT-5.6 Sol | 通用 agent / coding | Coding Agent Index **80** | 前沿通用模型继续把 coding 作为核心能力场 |
| SWE-1.7 | 长程软件工程 agent | FrontierCode **42.3%**；Terminal-Bench **81.5%**；SWE-Bench Multilingual **77.8%** | 后训练、self-compaction、真实工程环境继续有效 |
| LongCat-2.0 | 国产 agentic coding MoE | **1.6T** 总参数；**1M** context；SWE-bench Pro **59.5**；Terminal-Bench **70.8** | 国产算力栈从“能训练”走向“能跑 agentic coding” |
| Grok 4.5 | Coding → 通用电脑工作 | MoE；Cursor 交互数据；$2 / $6 基础价 | IDE 交互轨迹成为后训练资产 |

**非共识点**：coding agent 的下一轮壁垒不在 prompt，也不只在基座模型，而在“任务环境 + 自动验证器 + 真实交互轨迹”。Cognition 拥有 Devin 环境，Cursor 拥有 IDE 与用户操作轨迹，美团 LongCat 强调国产算力与开源推理代码。新进入者如果没有高质量任务环境，很难仅靠模型包装建立长期优势。

---

### 3. Meta Muse Spark 1.1 已有 AA 独立测评：低价、长上下文、agentic 补短板

Meta 官方 blog 确认 **Muse Spark 1.1** 是 Meta Superintelligence Labs 的最新 multimodal reasoning model，面向 agentic tasks，在 tool use、computer use、coding 和 multimodal understanding 上相对 Muse Spark 有明显提升；模型可在 Meta AI / meta.ai 的 **Thinking** 模式使用，并通过新的 **Meta Model API** public preview 向开发者开放。官方还披露了几个关键产品能力：**1M-token context window**、active context management、main agent / subagent 并行编排、MCP servers / custom skills 泛化、computer-use 中按任务选择 scripting / clicking / batched actions。

Artificial Analysis 已在 **2026-07-10** 发布 Muse Spark 1.1 独立测评。AA 给出的核心结论是：Muse Spark 1.1 在三个月内比 Muse Spark 1.0 的 Intelligence Index 提升 **8 分**，达到 **51**，与 GLM-5.2 max、GPT-5.4 xhigh、GPT-5.6 Luna max 基本持平，低于 Grok 4.5 high **54**，也低于 Claude Fable 5 **60**、GPT-5.6 Sol max **59**、Claude Opus 4.8 max **56**。它的提升主要来自 Scientific Reasoning、Coding 和 Knowledge；agentic knowledge work 有明显进步，但在 GDPval-AA v2 上仍落后前沿。

这条信息改变了周报里对 Meta 的写法：Muse Spark 1.1 不应再被写成“只有官方社媒 / 模型卡待补”的弱信号，而应写成“有第三方测评支撑的低价 agentic 模型”。但它也不是“全面顶级”：AA 的数据说明它在智能和编码上进入前沿第二梯队，在成本效率上很强，在 agentic work 上仍有追赶空间。

**Muse Spark 1.1 关键数据**

| 维度 | 数据 | 含义 |
|---|---:|---|
| AA Intelligence Index | **51** | 比 Muse Spark 1.0 的 **43** 提升 **8 分**，与 GPT-5.6 Luna max / GPT-5.4 xhigh 同档 |
| Coding Index | **71** | 较 Muse Spark 1.0 **59** 提升 **12 分** |
| SciCode | **58%** | AA 称其在已测模型中排名第 3，仅低于 Claude Fable 5 与 Gemini 3.1 Pro Preview |
| HLE | **45%** | 接近 Claude Opus 4.8 max **46%**，高于 GPT-5.5 **44%** 与 Grok 4.5 high **40%** |
| GDPval-AA v2 | **1376 Elo** | 较 1.0 提升 **232 Elo**，但仍不是 frontier leader |
| AA-Omniscience | **18** | 从 **4** 提升到 **18**，主要来自幻觉率下降和 abstention 改善 |
| Token use | **94M output tokens** | 低于 GPT-5.4 xhigh **109M**、GPT-5.6 Luna max **125M**、GLM-5.2 max **141M** |
| 估算任务成本 | **~$0.26 / Intelligence Index task** | AA 称在同等智能区间仅落后 GPT-5.6 Luna 的 **$0.21** |
| API 价格 | **$1.25 / $4.25** per 1M input / output tokens；cache hit **$0.15/M** | Axios 与 AA 均给出同一价格口径 |
| Context | **1M tokens** | 较 Muse Spark 1.0 的 262k 明显扩展 |
| 速度 | **~114 tokens/s median**；首 token 约 **21s** | AA 基于 Meta first-party API 给出的性能口径 |

**非共识点**：Muse Spark 1.1 的战略价值不是“Meta 回到最强模型榜首”，而是 Meta 用低价 API 把一个接近前沿第二梯队的 multimodal reasoning / coding model 推向 agentic workload。它在成本上会给 GPT-5.6 Luna、Grok 4.5、Claude 中高端模型形成压力；但在 GDPval-AA v2 等真实工作任务上仍落后前沿，说明它更适合作为高性价比 agent routing 选项，而不是无脑替代最强 coding / work agent 主模型。

---

### 4. 成本效率正在从“价格表”升级为“模型结构和推理范式”

本周多个信号都指向同一件事：前沿模型的能力越来越依赖成本结构。GPT-5.6 通过 Sol / Terra / Luna 把高智能、平衡成本和低价高频任务拆开；LongCat-2.0 通过 MoE 动态激活把 **1.6T** 总参数压到每 token **33B–56B** 激活；NVIDIA Nemotron-Labs-Diffusion 在单一架构中统一 autoregressive、diffusion 与 self-speculation decoding，8B 模型单次前向解码 token 数是 Qwen3-8B 的 **6×**，在 GB200 + SGLang 的 SPEED-Bench 上吞吐提升 **4×**；GPT-Live 则把前台实时语音交互与后台深度推理委托拆开。

这说明成本效率不再只是“API 每百万 token 多少钱”，而是模型架构、推理模式、工具调用方式、agent 并行数量和任务路由共同决定的系统属性。未来 AI 应用的关键工程能力会是 routing：什么任务用旗舰模型，什么任务用低价模型，什么时候开多 agent，什么时候把中间步骤交给程序化工具或 draft 模型。

**推理经济信号**

| 路径 | 本周代表 | 核心变化 |
|---|---|---|
| 模型分层 | GPT-5.6 Sol / Terra / Luna | 同一模型家族按能力和成本拆分任务 |
| 动态激活 | LongCat-2.0 | 万亿 MoE 通过 33B–56B 激活参数控制部署成本 |
| 解码范式 | Nemotron-Labs-Diffusion | AR + diffusion + self-speculation 统一，提升 tokens / forward 与吞吐 |
| 交互分层 | GPT-Live | 前台低延迟连续交互，后台委托 frontier model 深度推理 |
| 工具程序化 | Programmatic Tool Calling | 用轻量程序协调工具、过滤数据、减少 LLM 往返 |

**非共识点**：接下来“模型能力”会越来越像云计算性能，不只是峰值分数，而是单位成本下的任务完成率、延迟、可恢复性和可观测性。只比较最高分模型会误判应用层真实成本。

---

### 5. 非聊天型前沿正在形成第二曲线：语音、具身、健康、设计

本周另一个重要变化是，模型前沿不再只发生在聊天 LLM。OpenAI GPT-Live 采用 **full-duplex** 架构，可同时听与说，并把复杂任务委托给后台模型；每周已有 **1.5 亿+** 用户使用 ChatGPT Voice / Dictation。Mistral Robostral Navigate 是 **8B** 具身导航模型，仅用单 RGB 摄像头和自然语言指令，在 R2R-CE validation unseen 达 **76.6%**，训练数据约 **40 万 trajectories / 6,000 scenes**，prefix-caching 将训练 token 降低 **22×**。Google SensorFM 用 **500 万**同意参与者、**1 万亿+ 分钟**多模态可穿戴传感器数据预训练，在 35 项健康任务中赢下 **33 项**，linear probe 在 **34/35** 任务上超过特征工程监督基线。Seedream 5.0 Pro 则把图像生成推向信息图、精准编辑、图层分离、多图融合等设计工作流，但当前官方页面抓取不完整，仍需补读完整发布稿。

这些模型的共同点是：它们不以“聊天能力”定义前沿，而以连续交互、物理行动、个体生理表征、专业编辑控制定义前沿。对投资而言，这类机会往往不在“训练一个更大通用模型”，而在专有数据、闭环反馈、真实入口和高频任务。

**第二曲线信号**

| 方向 | 代表模型 | 关键数据 / 能力 | 投资含义 |
|---|---|---|---|
| 实时语音 | GPT-Live | full-duplex；前台交互 + 后台 GPT-5.5 委托；1.5 亿+ 周语音用户背景 | 客服、教育、陪伴、车载、销售训练会被连续交互重构 |
| 具身导航 | Robostral Navigate | 单 RGB；R2R-CE unseen **76.6%**；训练 token 降 **22×** | 降低传感器依赖，影响机器人 BOM 与部署复杂度 |
| 健康基础模型 | SensorFM | **500 万人 / 1T+ 分钟**；33/35 任务领先 | 可穿戴硬件的数据闭环价值上升 |
| 设计编辑 | Seedream 5.0 Pro | 信息图、精准编辑、图层分离、多图融合；豆包 / 即梦 / 火山方舟分发 | 图像模型从“出图”进入“设计交付物” |
| 社交媒体生成 | Muse Image / Video | 社交上下文、多参考编辑、agentic tool use、原生音频 | 分发和反馈闭环可能比单点画质更重要 |

---

## 厂商演进视图

### OpenAI：从模型公司继续向任务执行平台延伸

GPT-5.6、ChatGPT Work、GPT-Live、Microsoft 365 Copilot preferred model 和 Responses API 的组合，说明 OpenAI 正在把模型能力封装成组织工作流默认层。短期看是能力领先，长期看是平台挤压：越通用、越标准化的 agent 任务越容易被 ChatGPT Work 内置。

### Meta：Muse Spark 1.1 从弱信号升级为“低价 agentic API”信号

Muse Spark 1.1 已有官方 blog、API preview 和 Artificial Analysis 独立测评支撑。AA Intelligence Index **51**、Coding Index **71**、HLE **45%**、1M context、$1.25 / $4.25 定价，使它不再只是“Meta 官方社媒发布”，而是一个有第三方数据的高性价比 agentic / coding model。它还不是最强 agent work 模型，GDPval-AA v2 仍落后前沿；但如果 Meta 把 Muse Spark、Muse Image / Video、Meta AI、Instagram、WhatsApp 和 Model API 串起来，低价 + 分发闭环会成为独立竞争变量。

### Cognition / Cursor / 美团：coding agent 的差异化回到环境

Cognition 的 Devin、Cursor 的 IDE / CLI / SDK、美团 LongCat 的国产算力与开源推理代码，分别代表三种路径：执行环境、用户轨迹、基础设施闭环。下一阶段 coding agent 公司不是比谁“调用模型更聪明”，而是比谁能构建真实任务环境、持续采集轨迹并自动验证结果。

### NVIDIA / Mistral / Google：前沿模型向基础设施和垂直数据扩散

Nemotron-Labs-Diffusion 指向推理框架和硬件协同，Robostral Navigate 指向具身导航，SensorFM 指向可穿戴健康表征。这些不是 ChatGPT 的旁支，而是模型前沿在不同数据形态和部署约束下的分化。

### ByteDance Seed：图像模型从生成走向设计工作流

Seedream 5.0 Pro 的方向不是只提高生成质量，而是围绕复杂信息可视化、图层级编辑、多图融合和产品分发。由于完整官方正文尚未补齐，正式发布版应在补读后再决定是否提升权重。

---

## Benchmark 与价格：本周关键数字

| 数字 | 对应信号 | 为什么重要 |
|---|---|---|
| **53.6** | GPT-5.6 Sol Agents' Last Exam | 通用 agent 能力继续上移 |
| **80** | GPT-5.6 Sol Coding Agent Index | coding 仍是前沿模型核心战场 |
| **92.2%** | GPT-5.6 Sol BrowseComp | 浏览 / 信息检索型任务接近产品化边界 |
| **$5 / $30** | GPT-5.6 Sol API input / output 价格 | 旗舰能力价格锚点 |
| **$1 / $6** | GPT-5.6 Luna API input / output 价格 | 前沿家族能力向高频低价任务下沉 |
| **500 万+** | Codex 每周用户数 | coding agent 已形成大规模使用入口 |
| **100 万+** | Codex 非软件开发场景每周用户数 | coding agent 技术向通用工作 agent 外溢 |
| **42.3%** | SWE-1.7 FrontierCode 1.1 Main | 后训练和工程环境可把开源基座推近闭源前沿 |
| **1000 TPS** | SWE-1.7 在 Devin 中通过 Cerebras 提供 | coding agent 成本 / 速度竞争开始显性化 |
| **1.6T** | LongCat-2.0 总参数 | 国产万亿 MoE 信号 |
| **33B–56B** | LongCat-2.0 每 token 激活参数 | MoE 把规模转化为可部署预算 |
| **1M** | LongCat-2.0 上下文长度 | 长程工程任务和 agentic coding 的基础能力 |
| **4×** | Nemotron-Labs-Diffusion 在 GB200 + SGLang 上吞吐提升 | 解码范式开始进入真实推理栈评估 |
| **76.6%** | Robostral Navigate R2R-CE validation unseen | 单 RGB 具身导航进入可比较水平 |
| **1T+ 分钟** | SensorFM 预训练可穿戴数据 | 健康基础模型的数据规模门槛 |
| **1.5 亿+** | ChatGPT Voice / Dictation 周用户背景 | 实时语音入口已具备大规模分发基础 |

---

## 对星连资本的投资启示

1. **Agent workflow 公司要从“功能 demo”转向“任务验证器”。** GPT-5.6 + ChatGPT Work 会快速覆盖通用跨应用工作流，垂直 agent 必须证明自己在行业流程、权限治理、数据闭环、结果验证上有不可替代性。
2. **Coding agent 创业窗口转向环境和数据资产。** Cognition、Cursor、美团 LongCat 的共性不是 UI，而是分别拥有 Devin 环境、IDE 交互轨迹、国产训练 / 推理基础设施。没有真实任务环境的 coding agent 很难长期防守。
3. **模型成本 routing 会成为应用层基础设施。** Sol / Terra / Luna、MoE 动态激活、diffusion draft、前后台模型委托共同说明，应用需要自动选择模型、工具、agent 数量和推理路径，而不是固定调用单一模型。
4. **Meta Muse Spark 1.1 值得从“待补证”升级为重点跟踪。** AA 已给出 1.1 独立测评，证明其在 Intelligence Index、coding、HLE 与成本效率上进入前沿第二梯队；接下来要看 GDPval-AA v2、真实 agent harness 和开发者采用情况。
5. **非聊天型基础模型值得提高权重。** 健康、具身、语音、设计这类场景的模型优势来自专有数据、硬件入口和反馈闭环，可能比通用 LLM API 包装更容易形成差异化。
6. **国产模型观察重点应从“参数规模”转向“可运行闭环”。** LongCat-2.0 更值得看的不是 1.6T 本身，而是国产 5 万卡训练 / 推理、1M context、开源推理代码和第三方复测结果。

---

## 近期可能发布 / 需要补证

1. **Muse Spark 1.1 后续复测**：AA 已发布 1.1 独立测评，下一步看 Coding Agent Index、Terminal-Bench v2.1、第三方 agent harness 和开发者真实成本反馈。
2. **GPT-Live API 开放**：full-duplex 语音若进入 API，会直接影响客服、教育、车载、陪伴和销售训练产品。
3. **LongCat-2.0 第三方复测**：重点看 SWE-bench Pro、Terminal-Bench、1M context、国产推理栈是否可复现。
4. **SWE-1.7 真实成本曲线**：1000 TPS 之外，需要看复杂任务总 token、验证轮数、失败恢复成本和误改范围。
5. **Grok 4.5 的非代码任务表现**：Cursor 宣称扩展到数据科学、金融、法律和通用电脑工作，需要看真实 workflow benchmark。
6. **Seedream 5.0 Pro 完整官方发布稿**：需补齐技术路线、样例、benchmark、可用产品范围后再决定正文权重。
7. **Nemotron-Labs-Diffusion 框架适配**：关注 SGLang、vLLM、TensorRT-LLM 是否跟进三模式解码。
8. **SensorFM 产品化路径**：如果进入 Fitbit / Pixel Watch 或健康 agent，个人传感器数据闭环的战略价值会明显上升。

---

## 本周一句话

前沿模型竞争正在从“谁的模型更聪明”切换到“谁能用合适成本，把模型放进真实任务系统并形成分发闭环”。GPT-5.6 是这条主线的最强样本，Muse Spark 1.1 则凭 AA 独立测评和低价 API 从弱信号升级为高性价比 agentic 模型信号，SWE-1.7 / LongCat-2.0 / Grok 4.5 显示 coding agent 的下一阶段壁垒正在回到环境、数据和推理经济。