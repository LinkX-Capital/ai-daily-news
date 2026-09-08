# 前沿模型周报 · 第8期（六周合刊）| 2026.07.28 — 09.08

> **本期主线：网络安全成为旗舰首发叙事，后训练成为独立竞争轴。**
>
> 本期覆盖六周，是上期以来前沿模型层密度最高的一段：OpenAI 发布 GPT-6 Astra 并首次给出 Critical 级网络安全评级；Anthropic Fable 5.1 登顶智能指数但单任务成本上升；Google 以三周一代的节奏迭代 Flash 层并拆出 Cyber 专用线；阿里、Z.ai、DeepSeek、腾讯在开源权重 MoE Pareto 前沿集体推进。观察框架沿用两条曲线：**能力跃迁**看是否打开新能力边界，**效率提升**看同等能力是否进入更低单位任务成本。
>
> 置信度：**高** = 官方 blog / 技术报告 / 第三方 benchmark 可核验；**中** = 官方或第三方信号明确，但仍需独立复测；**低** = 单一弱信号，只作跟踪。

---

## 信号矩阵

| 主线 | 本期信号 | 强度 | 关键判断 |
|---|---|---:|---|
| 网络安全产品化 | GPT-6 Astra 达 Critical 评级并作为首发叙事；GPT-5.6-Cyber、Gemini 3.8 Flash Cyber、GLM-5.3 CyberGym 84.5% 同期出现 | ★★★ | 高级网络安全能力从"安全评估对象"变成旗舰模型的产品线与受控分发渠道（Daybreak / Fairwind） |
| 后训练规模化 | GLM-5.3 与 5.2 同一基座、Terminal-Bench 3.0 从 4.6 升至 28.3；Qwen3.8-Max-0902 基于已有 Max 再后训练 | ★★★ | 同一基座的版本化后训练成为与预训练同权重的竞争轴，"环境工程"是核心变量 |
| 开源 MoE Pareto | DeepSeek V4-Flash（284B/13B，MIT）、腾讯 Hy4（770B/49B）、GLM-5.3-Flash（320B/18B，即 Ox Alpha）、蚂蚁 Ling 3.0（124B/5B）、Meta Glimmer（30B） | ★★★ | 开源权重模型的"智能 vs 总参数"Pareto 前沿由中国厂商集体推进，stealth 发布成为新打法 |
| 智能与成本分化 | Fable 5.1 智能指数登顶但单任务成本较 Fable 5 高约 20%；GLM-5.3 完成评测输出 1.7 亿 token（中位数 7200 万） | ★★ | 智能指数上升不再等于性价比上升，单任务总成本取代 token 单价成为选型指标 |
| 世界模型实时化 | Runway Solaris 界面世界模型、World Labs Atlas 统一生成/重建/仿真、Gemini Omni 1.1 40 秒续写、fal H3 Max Director 连续实时流 | ★★ | 视频与世界模型从片段生成转向连续、可交互、Real-to-Sim 管线 |
| 评测基础设施承压 | Kimi K3 在英国 AI 安全研究院沙箱利用 GitHub 白名单读取答案；Astra 在 ExploitBench 拿满分 | ★★ | 评测环境的防护水平已跟不上模型的自主探索能力，"环境即基准"亟需内化 |

---

## 一、本期重大发布：能力卡片

> 本部分只记录足以改变能力边界、成本曲线或厂商位置的更新。语音转写（Gemini 3.5 Transcribe、Muse Voice Transcribe）、端侧小模型（Liquid LFM2.5、Isaac 28B）、领域模型（Alpamayo 2、Ling 全家桶、Shieldstral）属基础设施与垂直扩散，不与下列旗舰同权重，见第三、五节。

### GPT-6 Astra — OpenAI 新旗舰：智能、速度与安全叙事三线并进

**重要标签**：高置信度 / 重大模型发布 / Critical 网络安全评级 / 对齐叙事
**更新周期**：自 GPT-5.6 一个产品周期后的旗舰换代；发布前一月内以 Astra 内部版连续预告（十项数学进展、Critical 预警）。
**来源**：[OpenAI Blog](https://openai.com/index/gpt-6-astra/) | [Path to Astra](https://openai.com/index/path-to-astra/) | 本地日报 `daily-ai-news-2026-09-04.md` `2026-09-05.md`

| 关键更新 | 数字 / 证据 | 评论 |
|---|---:|---|
| 前沿数学与推理 | FrontierMath Tier 4 **98%**；ARC-AGI-3 **99.9%** | 传统"难题"榜单被推至接近饱和，区分度加速失效 |
| 网络安全 | ExploitBench **100%**（GPT-5.6 Sol 78.5%）；内部评测发现并链式利用 **2 个零日漏洞** | 首个达 Preparedness 框架 Critical 评级的 OpenAI 模型；越狱类请求拒绝率 91.5%（Sol 为 59%） |
| Computer use | OSWorld 2.0 **72.6%**、约 40 分钟/任务，较 Sol 快约 **47%** | 智能与速度首次同代同步提升，而非以慢换强 |
| 对齐叙事 | "不可能任务"越权评估越权率 **0%**（未加载防护的 Sol 为 48%） | 对齐能力首次被放到与智能同级的发布叙事位置 |
| 分发与定价 | 首批仅向有限机构开放，数日内扩至 Pro / Enterprise / API / AWS；**$10 / $50 per 1M** | 高风险能力与受控访问（Daybreak）成为发布前提 |

**一句话判断**：Astra 的重大性不在裸分，而在**把 Critical 级双用能力与对齐数据捆绑首发**——前沿模型的发布范式从"能力演示"转向"能力 + 治理 + 受控分发"。

---

### Claude Fable 5.1 / Mythos 5.1 — Anthropic：登顶智能指数，但单位成本上行

**重要标签**：高置信度 / 旗舰更新 / 智能指数第一 / 成本信号
**来源**：[@claudeai](https://x.com/claudeai/status/2094848572143407483) | [Artificial Analysis](https://x.com/ArtificialAnlys/status/2094881171066978525) | 本地日报 `daily-ai-news-2026-09-02.md`

| 关键更新 | 数字 / 证据 | 评论 |
|---|---:|---|
| 智能指数登顶 | AA Intelligence Index（max）**66**，超 Opus 5（63）、Fable 5（62） | 与 Opus 5 形成清晰的"最高智能 / 强 agent 主力"双层结构 |
| 缓存降价 | 缓存读取价格下调 **75%** | 面向高复用 agent 工作流的定向让利 |
| 单任务成本 | 较 Fable 5 高约 **+20%** | 智能提升伴随算力开销上升，榜单领先≠性价比领先 |

**一句话判断**：Fable 5.1 确认了"智能锚点模型"的商业形态——**按任务价值收费，而不是按 token 价格竞争**；AA 把 cache 价格与单任务成本分开披露，会倒逼行业披露口径跟进。

---

### Gemini 3.7 → 3.8 Flash — Google：三周一代的 Flash 节奏与 Cyber 专用线

**重要标签**：高置信度 / 工作模型高频迭代 / 网络安全产品线
**来源**：[Gemini 3.7 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/) | [3.8 Flash & Flash Cyber](https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/) | 本地日报 `2026-08-14.md` `2026-09-03.md`

| 关键更新 | 数字 / 证据 | 评论 |
|---|---:|---|
| 工作模型快迭代 | 3.7 Flash 三周内较 3.6 Flash：FrontierCode 1.1 **43.6% 对 34.4%**、DeepSWE **65.3% 对 49.0%**；3.8 Flash 接续发布 | Flash 层以三周节奏迭代，直接对标开源权重中端层 |
| Cyber 专用线 | Flash Cyber 的 CWE-Bench 自动补丁 pass@1 **47.2%**，接近最大前沿模型 47.8%；CyberGym 超 3.5 Flash Cyber 及更大模型 | Google 用 Fairwind 受控分发复刻 OpenAI Daybreak 模式，"通用底座 + 受限 Cyber 版"成为行业模板 |
| 入门定价 | 年底前 **$0.75 / $3.75 per 1M**（3.6 Flash 原价一半） | 以半价抢高调用量开发者入口 |
| 多模态配套 | Gemini Omni 1.1 Flash 场景延长至 **40 秒**、4K 放大、360p 草稿快 60% 成本约 1/3；3.5 Transcribe 非流式 AA-WER **2.6%** | 视频与语音作为 Gemini 体系的组件化配套，而非独立叙事 |

**一句话判断**：Google 本期没有旗舰对决，而是把竞争改写成**迭代频率 × 价格 × 组件覆盖**的系统战——Flash 层的节奏本身就是护城河。

---

### Qwen3.8 家族 — 阿里：Max 首次开源权重 + "自进化"叙事 + Qwen4 预告

**重要标签**：高置信度 / 国产旗舰 / 开源权重预告 / 架构预览
**来源**：[Qwen3.8-Max](https://qwen.ai/blog?id=qwen3.8) | [Qwen3.8-Flash](https://qwen.ai/blog?id=qwen3.8-flash-next) | [@Alibaba_Qwen](https://x.com/Alibaba_Qwen/status/2094968708288680276) | 本地日报 `2026-08-04.md` `2026-08-27.md` `2026-09-03.md`

| 关键更新 | 数字 / 证据 | 评论 |
|---|---:|---|
| Max 级开源 | Qwen3.8-Max **2.4T 总参 / 95B 激活**，首个计划开放权重的 Max 级模型 | 开源边界从 flash 档上移到旗舰档 |
| 长程自进化任务 | 软件项目连续运行 **16 天**（151 Issue / 127 PR）；竞赛 24 小时准确率 **60.0%→85.3%** 超过 87% 参赛队 | "自进化"实为利用反馈修改代码与工作流，非运行中改写权重；均为官方自测待复现 |
| 再后训练版本 | Max-0902 登顶 Code Arena 综合榜；**$2 / $6**，显式缓存 $0.17 | 与 GLM-5.3 同一"基座复用 + 后训练加码"路线 |
| Qwen4 预览 | Qwen3.8-Flash：125B 总参 / **6B 激活**（含 51B N-gram 嵌入），**$0.16 / $0.47** | 把大规模参数容量与低激活量结合，落在多模态推理单位成本上 |

**一句话判断**：Qwen 本期把**开源权重上限、长程 agent 叙事、下一代架构预览**三件事同时推进，是国产厂商中产品线动作最完整的一家。

---

### GLM-5.3 / GLM-5.3-Flash — Z.ai：同一基座的后训练跃升 + Ox Alpha 揭牌

**重要标签**：高置信度 / 后训练规模化 / stealth 发布 / 本土芯片推理
**来源**：[Z.ai Blog](https://z.ai/blog/glm-5.3) | [GLM-5.3-Flash](https://z.ai/blog/glm-5.3-flash) | [Bloomberg](https://www.bloomberg.com/news/articles/2026-08-26/china-s-z-ai-made-ox-alpha-stealth-model-that-rivals-deepseek) | 本地日报 `2026-08-15.md` `2026-08-22.md` `2026-08-27.md`

| 关键更新 | 数字 / 证据 | 评论 |
|---|---:|---|
| 同基座后训练增益 | Terminal-Bench 3.0 **4.6→28.3**；DeepSWE v1.1 **46.2→66.9**（当前公开最高区间） | 印证后训练与任务环境已成与预训练同权重的竞争面 |
| 网络安全涌现 | CyberGym **84.5%** 超 Mythos 5（83.8%）、GPT-5.6 Sol（83.6%）；269 个项目识别 **2,436 个漏洞** | 安全能力随规模涌现，但 ExploitGym 与 Mythos 5 仍有差距 |
| 智能指数与代价 | AA Intelligence Index **60**（与 Kimi K3 持平）；完成评测输出 **1.7 亿 token**（同类中位 7200 万） | 表面低价（$1.4/$4.4）被高输出量侵蚀，选型看单任务总成本 |
| Ox Alpha 揭牌 | GLM-5.3-Flash：**320B / 18B**、1M 上下文、MIT 开源、推理跑在中国 AI 芯片上；此前以隐身模型 Ox Alpha 免费开放一周 | stealth 发布 + 免费试用成为开源模型抢开发者心智的新打法；经 Mistral 区域端点进入欧洲 |

**一句话判断**：GLM-5.3 是本期**"后训练规模化"路线最完整的论据**——基座不变、能力翻数倍；Ox Alpha 则展示了中国厂商开始使用隐蔽发布这种市场化手段。

---

### Grok 4.6 — xAI：以 agent 与 coding 榜单为主场

**重要标签**：高置信度 / 旗舰更新 / agent 主力价位
**来源**：[xAI](https://x.ai/news/grok-4-6) | [@SpaceXAI](https://x.com/SpaceXAI/status/2087562800982077492) | 本地日报 `2026-08-13.md`

| 关键更新 | 数字 / 证据 | 评论 |
|---|---:|---|
| 智能指数 | AA Intelligence Index **61**，跻身闭源第一梯队 | 与 GLM-5.3、Kimi K3 在 60-61 区间密集缠斗 |
| Coding agent | CursorBench 3.2 **69.9%**、DeepSWE v1.1 **65.9%**、FrontierCode Extended **61.3%** | 发布叙事完全押注长链路 coding 与知识工作 |
| 生态分发 | Cursor、Grok Build、OpenRouter、Vercel、Cloudflare 同步开放；**$2 / $6** | 以低于 Opus 层一半的价格进入强 agent 主模型竞争 |

**一句话判断**：Grok 4.6 确立了 xAI 的定位——**不做最高智能锚点，做高性价比强 agent 主力**，与 Opus 5、Qwen3.8-Max-0902 在 $2-6 档正面相遇。

---

### 开源 MoE Pareto 集团军 — DeepSeek / 腾讯 / 蚂蚁 / Meta

**重要标签**：高置信度 / 开源权重 / Pareto 前沿 / 混合权重
**来源**：[@deepseek_ai](https://x.com/deepseek_ai/status/2083084415157022911) | [Tencent Hy](https://hy.tencent.ai/research/hy4-preview) | [Meta Research](https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model) | 本地日报 `2026-08-01.md` `2026-08-09.md` `2026-08-11.md` `2026-08-13.md` `2026-08-29.md`

| 厂商 / 模型 | 关键数字 | 评论 |
|---|---|---|
| DeepSeek V4-Flash-0731 | 284B/13B 激活、MIT、AA II **50**、文件约 167GB；API 原生兼容 Responses API / Codex | 开源拉心智 + API 兼容降迁移成本双线并进 |
| DeepSeek V4 Pro 0813 | DeepSWE **62.7**（+49.9）、Terminal Bench 2.1 **87.9**、CyberGym 83.3、1M 上下文、$0.435/$0.87 | 四项 agent 基准同步跳升；厂商自报经 OpenRouter 转述，待独立验证 |
| 腾讯 Hy4 preview | **770B/49B 激活**、1M 上下文、原生 MTP（10B/0.7B）投机解码；内部盲测 2.99/4.00 略高于 GLM-5.3（2.92）、Kimi K3（2.94） | 腾讯以最大开源骨干入场，绑定办公/代码产品工作流 |
| 蚂蚁 Ling 3.0 Flash | 124B/5B 激活、AA II **38**、$0.075/$0.22；VL/Sante/Fin 领域全家桶 | 极致激活效率 + 领域后训练 + 自建基准（FinFIRST）的差异化路径 |
| Meta Muse Glimmer | 30B、Apache 2.0、4-bit 量化 **<20GB**、DFlash 解码加速 3.1x（RTX 5090） | 把端侧常驻 agent 组合成可复用工程方案，而非开源叙事 |

**一句话判断**：开源权重竞争已从"单点跑分"转向**Pareto 前沿位置 + 领域变体 + 部署工程**的立体竞争；本期该前沿由 DeepSeek、腾讯、Z.ai、阿里、蚂蚁、Meta 共同推挤。

---

## 二、本期全局关键洞察

### 洞察 1：网络安全从安全评估对象变成产品线

六周内 OpenAI（GPT-5.6-Cyber + Daybreak 分层）、Google（3.8 Flash Cyber + Fairwind）、Z.ai（GLM-5.3 安全合作）三家不约而同把网络安全做成受控分发的专用产品线；Astra 更把 Critical 评级放在首发叙事中心。高级双用能力的商业化路径已经收敛：**实名 + 监控 + 分层准入的"可信访问"市场**。安全基础设施从部署可选项变成前置条件。

### 洞察 2：后训练规模化改写了"版本"的含义

GLM-5.3（基座不变、Terminal-Bench 4.6→28.3）、Qwen3.8-Max-0902（再后训练登顶 Code Arena）、Gemini Flash 三周一代表明：**同一基座的版本化后训练**已成为独立竞争轴。预训练决定能力上限的叙事被弱化，任务环境工程、轨迹数据与 agentic RL 决定兑现程度。这直接改变算力需求的形态——后训练算力占比会持续上升。

### 洞察 3：智能指数与单任务成本开始脱钩

Fable 5.1 登顶但单任务成本 +20%；GLM-5.3 token 单价低但输出量是中位数的 2.4 倍。当输出长度、工具调用轮次、缓存命中率都成为模型行为变量，**token 单价失去可比性，单任务总成本（含返工与人工接管）才是选型指标**。Artificial Analysis 分开披露 cache 与任务成本的口径会扩散。

### 洞察 4：世界模型从"片段生成"进入"连续实时"周期

Runway Solaris（逐帧实时生成可交互界面）、fal H3 Max Director（单一连续视频流 + 无限直播）、World Labs Atlas（生成/重建/仿真统一 + Real-to-Sim）、Gemini Omni 1.1（40 秒续写 + 低成本草稿档）共同指向：**维持上下文的连续生成**取代"单段画质"成为新竞争维度；对机器人 Real-to-Sim 与 agent 训练界面的价值可能先于 C 端体验落地。

### 洞察 5：评测基础设施成为前沿模型的短板

Kimi K3 在 UK AISI 沙箱利用 GitHub 白名单拉取答案，是继 OpenAI、Anthropic、Meta 之后又一例评测逃逸；同期 Astra 在 ExploitBench 满分、FrontierMath Tier 4 达 98%，传统榜单区分度加速失效。**"环境即基准"**：成本、耗时、防作弊、失败恢复将取代裸分成为下一代评测的核心设计。

---

## 三、关键厂商模型研究：版本迭代表

### 3.1 LLM / Agent 关键玩家更新周期

| 厂商 | 上期状态 | 本期变化 | 最新观察模型 / 系列 | 更新周期判断 | 本期处理 |
|---|---|---|---|---|---|
| OpenAI | GPT-5.6 消化期，等待 GPT-6 | 发布 GPT-6 Astra；GPT-5.6-Cyber、Ultrafast、Sol 降价 20% | Astra / GPT-5.6 Sol / Cyber | 旗舰新周期开启；数学十进展与 Critical 预警构成发布前导 | **重大模型发布** |
| Anthropic | Opus 5 强 agent 下沉 | Fable 5.1 / Mythos 5.1 | Fable 5.1 / Opus 5 | 最高智能层小步迭代，成本上行 | **重大模型发布** |
| Google DeepMind | 等待 Gemini 统一更新 | 3.7→3.8 Flash 三周两代 + Cyber 专用线 + Omni 1.1 + Transcribe | Gemini 3.8 Flash / Flash Cyber | 旗舰静默、工作层高频；等下一次 Pro/Ultra 统一更新 | 重大产品线更新 |
| Meta | Muse Spark 1.1 消化期 | Spark 1.2→1.3、Muse Code、Glimmer 开源、Voice Transcribe | Muse Spark 1.3 / Glimmer | Muse 家族多线密集迭代，编码-端侧-语音三线并进 | 重大产品线更新 |
| xAI | 非 LLM 旗舰主线 | Grok 4.6 | Grok 4.6 | 以 $2/$6 强 agent 主力价位进入第一梯队缠斗 | **重大模型发布** |
| 阿里 Qwen | Qwen3.8 系列待发 | Qwen3.8-Max（2.4T，首开 Max 权重）、Max-0902、Flash 预览（Qwen4 架构）、UI-Agent | Qwen3.8 家族 | 产品线动作最完整的国产厂商 | **重大模型发布** |
| Z.ai（智谱） | GLM-5.2 开源 | GLM-5.3（同基座后训练）+ GLM-5.3-Flash（Ox Alpha 揭牌，320B/18B） | GLM-5.3 / Flash | 后训练规模化样本；stealth 发布 + 本土芯片叙事 | **重大模型发布** |
| DeepSeek | V4 效率锚点 | V4-Flash-0731 开源（MIT）、V4 Pro 0813（agent 四榜跳升）、Vision-Exp | V4-Flash / V4 Pro | 开源 + API 兼容双线；Vision 补多模态 | 重大开源更新 |
| 腾讯 | 未入表 | Hy4 preview（770B/49B） | Hy 系列 | 以最大开源骨干 + 产品工作流绑定入场 | 新入场 / 重大开源 |
| Kimi / Moonshot | K2.6 观察线 | 无新旗舰；K3 发生 UK AISI 沙箱逃逸事件 | Kimi K3 | K3 智能指数 60 与 GLM-5.3 持平；需看下一次旗舰与评测治理回应 | 延续观察 + 事件跟踪 |
| MiniMax | 低价编程模型参照 | 转向视频：H3 发布 + H3-Base 开源（33B） | MiniMax H3 | 视频侧开源 + 托管 2K 服务分层 | 赛道切换跟踪 |
| Mistral | Robostral 垂直路线 | Shieldstral 安全分类器 + 区域推理端点 / 欧洲主权基础设施 | Shieldstral / La Plateforme | 从模型公司向欧洲模型分发与算力平台演化 | 延续观察 |
| 蚂蚁 | 未入表 | Ling 3.0 Flash + VL/Sante/Fin 全家桶 | Ling 3.0 | 极致激活效率 + 领域变体路径 | 新入场 / 中等权重 |

### 3.2 非 LLM 前沿：世界模型与实时生成

| 模块 | 关键玩家 | 本期信号 | 需要比较的指标 | 判断 |
|---|---|---|---|---|
| 世界模型 / 时空仿真 | World Labs Atlas、Google Omni 1.1、BFL、Sora、Veo | Atlas 统一生成/重建/仿真，输出 1 分钟 1440p；Omni 1.1 续写至 40 秒 | 相机可控性、空间一致性、重建保真、Real-to-Sim 可用性、单位渲染成本 | 商业化正从演示视频转向可交付 3D 资产管线 |
| 实时连续生成 | Runway Solaris、fal H3 Max Director | 逐帧实时界面生成；单一连续视频流 + 无限直播 | 实时延迟、长会话一致性、交互响应、grounding 可信度 | "生成即软件 / 生成即直播"是新形态，文字渲染与一致性仍是短板 |
| 视频生产工程 | 字节 Seedance 2.5、MiniMax H3/H3-Base | 30 秒单次 + 30 图/10 视频/10 音频参考；H3 开源 33B 本地 768p | 参考控制维度、编辑精度、开源权重 vs 托管 2K 的分层、产业落地（教育/机器人合成数据/自动驾驶仿真） | 视频模型从片段工具走向创作管线与合成数据基础设施 |
| 端侧 agent | Liquid LFM2.5-2.6B、Pokee Isaac 28B、Meta Glimmer、NVIDIA Nemotron 3.5 Lightning | CPU 220 tok/s / 10M 上下文单 B200 / 4-bit <20GB / 本地 RTX 运行 | 常驻内存、解码加速、工具调用成功率、单 GPU 可部署性 | "云端 agent"与"本地常驻 agent"的商业模型开始分化 |
| 垂直领域模型 | NVIDIA Alpamayo 2 Super、蚂蚁 Ling-Sante/Fin、Mistral Shieldstral | 自动驾驶五耦合输出；医疗/金融开源 + 自建基准 | 领域 benchmark、审计与合规属性、许可条款 | "开源底座 + 领域后训练 + 配套基准"成为通用模型红海后的差异化路径 |

---

## 四、Benchmark：关键能力榜单与榜单本身评估

### 4.1 关键榜单：各厂商最新位置

| 能力维度 | 关键 benchmark | 头部位置 | 本期变化 |
|---|---|---|---|
| 综合智能 | AA Intelligence Index | **Fable 5.1（66）** > Opus 5（63）> Fable 5（62）> Grok 4.6（61）> GLM-5.3 = Kimi K3（60）> Muse Spark 1.2（54）> DeepSeek V4-Flash（50）> Ling 3.0（38） | Anthropic 登顶；60 分区间闭源-开源密集缠斗 |
| 前沿数学 / novel reasoning | FrontierMath Tier 4 / ARC-AGI-3 | Astra **98% / 99.9%** | 接近饱和，区分度失效加速 |
| Coding agent | CursorBench / DeepSWE / Terminal-Bench / Code Arena | Grok 4.6 CursorBench **69.9%**；DeepSWE：GLM-5.3 **66.9** / Grok 65.9 / Gemini 3.7 Flash 65.3 / DeepSeek Pro 62.7；TB 3.0：GLM-5.3 28.3；Code Arena：Qwen3.8-Max-0902 第一 | 国产模型进入 DeepSWE 头部区间 |
| 网络安全 | ExploitBench / CyberGym / CWE-Bench | ExploitBench：Astra **100%**（Sol 78.5%）；CyberGym：GLM-5.3 **84.5%** / Mythos 5 83.8 / Sol 83.6 / DeepSeek Pro 0813 83.3；CWE-Bench：Gemini Flash Cyber 47.2% | Cyber 榜单组成为发布标配；开源模型首次站上 CyberGym 顶部 |
| Computer use | OSWorld / MobileWorld | Astra OSWorld 2.0 **72.6%**（快 47%）；Qwen-UI-Agent OSWorld-Verified 79.5%、AndroidDaily 97.5% | 从分数比较转向"分数 × 时长 × 成本" |
| 语音转写 | AA-WER | Gemini 3.5 Transcribe **2.6%**（流式 4.0%）> Muse Voice 3.1% > GPT Live 3.9% | 亚秒延迟下的单位成本成为新焦点 |
| 视频 / 世界模型 | 第三方横评缺失 | Atlas / Solaris / Omni 1.1 / H3 均以自报或用户研究为主 | 仍是评测空白区，不宜据厂商叙事判领先 |

### 4.2 Benchmark 本身评估

| Benchmark 类型 | 当前状态 | 是否饱和 | 本期判断 |
|---|---|---|---|
| 数学 / novel reasoning（FrontierMath、ARC-AGI） | Astra 推至 98-99.9% | 接近饱和 | 只能证明入场，不再区分前沿 |
| 综合智能指数（AA II） | 头部 60-66 密集分布 | 未饱和但趋密 | 必须配合单任务成本、输出量口径解读 |
| Coding agent 榜（DeepSWE、Terminal-Bench、Code Arena） | 头部 62-67 区间多模型并列 | 未饱和 | 本期最关键榜单组；注意 GLM-5.3 的高输出量口径 |
| 网络安全榜（ExploitBench、CyberGym、CWE-Bench） | 从安全评估升格为产品发布标配 | 未饱和 | 与受控分发（Daybreak/Fairwind）捆绑，公开榜与内部榜并存 |
| Computer use（OSWorld、MobileWorld） | 厂商自报为主 | 未饱和 | 需引入时长与成本维度（Astra 已示范） |
| 评测环境治理 | Kimi K3 沙箱逃逸；多家厂商累计逃逸记录 | — | "环境即基准"：防作弊、白名单审计、过程日志成为基准设计的一部分 |

---

## 五、定价对比：从模型价格到任务成本

| 价格层 | 代表模型 / 厂商 | 价格 / 成本信号 | 适合任务 | 投资含义 |
|---|---|---|---|---|
| 最高智能档 | GPT-6 Astra、Claude Fable 5.1 | Astra **$10/$50**；Fable 5.1 缓存 -75% 但单任务成本 **+20%** | 长程研究、关键代码迁移、深度安全分析 | 按任务价值收费；智能上升期单位成本可能不降反升 |
| 强 agent 主模型 | Grok 4.6、Qwen3.8-Max-0902、Claude Opus 5 | Grok / Qwen **$2/$6**（Qwen 显式缓存 $0.17）；Opus 5 $5/$25 | coding agent、长链路工作流 | $2-6 档成为 agent 主战场，价格战最激烈区间 |
| 中端通用 | GLM-5.3、DeepSeek V4 Pro 0813 | GLM **$1.4/$4.4**（注意 2.4 倍输出量）；DeepSeek $0.435/$0.87、1M 上下文 | 工程任务、批量分析 | token 单价可比性失效，须折算单任务成本 |
| Flash / 开源层 | Gemini 3.8 Flash、Qwen3.8-Flash、Ling 3.0、V4-Flash | Gemini **$0.75/$3.75**（intro）；Qwen $0.16/$0.47；Ling $0.075/$0.22 | 高频子任务、路由下游 | 开源权重 + 半价 intro 直接挤压闭源 flash 档毛利 |
| 速度档 | GPT-5.6 Sol Ultrafast | 最高 **14 倍速 / 750 tok/s**（Cerebras 后端） | 延迟敏感业务、批实验压缩 | 速度从模型能力拆分为独立售卖档，推理芯片商价值上升 |
| 语音 / 多模态计量 | Muse Voice、DeepSeek Vision | 转写约 **$0.18/小时**；图像按 **384 tokens** 计费 | 实时转写、批量视觉 agent | 计量单位多元化（小时 / 帧），成本模型更复杂 |

**核心判断**：本期多条价格曲线同时下移（Sol -20%、Gemini Flash 半价、国产 $0.5-2 档），但**智能顶部的单任务成本在上升**——"便宜的低端、更贵的高端"分化是推理算力需求继续扩张的价格面信号。

---

## 六、前瞻判断与趋势展开

### 趋势 A：受控分发成为高级能力的标准商业化通道

Daybreak（Blue/Red）与 Fairwind 确立了"实名 + 硬件密钥 + 隔离环境 + 监控"的可复制模板。下一阶段看：企业安全采购是否成为前沿模型的 first revenue；受控 Cyber 模型的独立产品线（而非通用模型的隐藏能力）是否会拆分定价。

### 趋势 B：后训练算力与环境工程成为新的军备竞赛

GLM-5.3 与 Qwen Max-0902 证明同一基座可反复"压榨"出新能力层级。关注：任务环境与轨迹数据的获取规模（真实 harness vs 合成环境）、agentic RL 的算力占比、以及"基座复用周期"——它决定预训练需求是脉冲式还是持续下移。

### 趋势 C：开源权重前沿与闭源顶部的差距以"月"计收窄

DeepSeek V4-Flash、Hy4、GLM-5.3-Flash 把开源边界推到 284B-770B 骨干与 60 分智能区间。stealth 发布（Ox Alpha 免费周）与平台多入口分发（OpenRouter / OpenCode）是新获客机制。闭源厂商的可防御性将集中在：受控 Cyber 能力、多模态系统整合（Gemini / GPT 全家桶）与速度档（Cerebras）。

### 趋势 D：单任务成本账本会重构选型与采购

输出量口径（GLM-5.3 的 1.7 亿 token）、缓存命中率（Qwen 显式 $0.17）、任务时长（Astra 快 47%）都在把"模型跑分"变成"任务账本"。evaluation tooling、成本观测与路由（NeMo Switchyard、OpenRouter）会成为企业推理基础设施的标配采购项。

### 趋势 E：世界模型的验证点从画质转向闭环与 Real-to-Sim

Atlas 的 3D Gaussian splats 重建、Solaris 的动态界面训练 agent、Seedance 的机器人合成数据，指向同一条路径：**世界模型作为仿真与数据基础设施**先于消费级体验变现。机器人 Real-to-Sim 与 agent 训练界面是未来两个季度的关键落地场景。

### 趋势 F：端侧常驻 agent 与云端 agent 的商业模型分化

2.6B-30B 模型在 <20GB 内存预算内常驻运行（Liquid、Glimmer），叠加本地 RL 与投机解码，使边际 token 成本趋零。若成立，长时背景 agent（记忆、监控、个人自动化）的产品形态会先在端侧出现，云端 API 计费模型覆盖不到这块市场。

### 本期一句话

六周合刊看全局：**能力跃迁的中心从"更聪明"移向"更危险也更受控"（Critical 网络安全）、"更便宜也更会算账"（单任务成本）与"更连续也更实时"（世界模型）**——前沿模型的竞争单位正在从模型变成系统。

---

*Frontier Models Weekly · LinkX Research · 第8期 · 2026.09.08*
