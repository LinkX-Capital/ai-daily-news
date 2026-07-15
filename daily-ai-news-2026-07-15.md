## 07月15日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：PrismML 推出 Bonsai 27B，首个可在手机端本地运行的 27B 级模型; 腾讯混元为 295B MoE 旗舰 Hy3 发布 1-bit/4-bit 版本，可单卡服务
- 产业动态：OpenAI 首款硬件设备据报为可移动无屏音箱，定位 ChatGPT 的实体伴侣; Cognition 回顾收购 Windsurf 一周年：团队增至 350 人，年化收入突破 5 亿美元; Google与纽约大都会艺术博物馆合作，推出Met Prototypes & Play生成式AI体验; NVIDIA NeMo团队推出agentic优先RL框架Molt，vLLM负责rollout
- 算力追踪：纽约州签署全美首个数据中心建设暂停行政令，AI 算力扩张遭遇州级监管天花板; AWS 算力供不应求，初创公司转向新云厂商寻求 GPU; Reflection AI 与 Nebius 签订 10 亿美元算力订单
- 初创&融资：DeepSeek 在首轮 74 亿美元融资后启动新一轮，据报拟再融 15 亿美元并计划 2027 年 IPO; 强化学习之父 Richard Sutton 离开 Keen Technologies，创办 RL 新公司 Oak Lab; Nous Research 洽谈新一轮融资，估值 15 亿美元
- 研究关注：SAO 单 rollout 异步优化在 agentic RL 上稳定超越 GRPO，已用于 GLM-5.2 训练; Sparse Delta Memory 用稀疏寻址扩容线性 RNN 隐状态，长程检索显著提升; Direct-OPD 把弱模型 RL 增益迁移给强模型，Qwen3-1.7B 在 AIME 从 48.3% 升至 58.3%; Sakana AI 提出「智能细胞砖」：模块化物理单元靠局部协作实现形状识别与损伤自愈; ABot-AgentOS 提出机器人 Agent 操作系统与可执行基准 EmbodiedWorldBench; MIT 团队证实 LLM 自发涌现与人脑对应的功能模块化架构
- X讨论：Demis Hassabis 发表前沿 AI 治理框架，呼吁建立美国主导的全球 AI 监管机构; Perplexity 开源 WANDR 基准：评测需「广而深」检索的研究 agent，最强系统仅 0.363 soft F1; OpenRouter 上线 MCP Server，Agent 可在编辑器内发现、排序、测试并对比模型

---

## 📖 详细参考

### 模型前沿
**PrismML 推出 Bonsai 27B，首个可在手机端本地运行的 27B 级模型**
- PrismML 发布 Bonsai 27B 系列多模态模型，基于 **Qwen 3.6 27B**，将 27B 模型 16-bit 下约 **54GB** 的显存占用压缩到手机可承载的量级，提供两个版本：1-bit Bonsai 27B 仅 **3.9GB**（每权重 1.125 有效 bit），在知识、推理、数学、代码、指令跟随、agentic 与视觉等基准上保留 **90%** 得分；Ternary Bonsai 27B 为 **5.9GB**（每权重 1.71 有效 bit），保留 **95%** 得分。模型以 Apache 2.0 开源，由 Caltech 教授、信息论学者 Babak Hassibi 主导，定位是把最大可能的智能推到 iPhone 等边缘端。
  > 💡 1-bit/三值化极端量化是把大模型塞进手机的少数可行路径，Bonsai 27B 以 3.9GB 保留 90% 能力，意味着 27B 级模型首次进入手机端实用区间；这与同日腾讯 Hy3 用 1-bit 把 295B MoE 压到单卡可服务，共同指向「极端低比特量化」成为 2026 年端侧与单卡部署的主流技术路线。
   - 来源: [PrismML](https://prismml.com/news/bonsai-27b) | [@BabakHassibi](https://x.com/BabakHassibi/status/2077120949451923483) | [@PrismML](https://x.com/PrismML/status/2077084891284721827)

**腾讯混元为 295B MoE 旗舰 Hy3 发布 1-bit/4-bit 版本，可单卡服务**
- 腾讯混元为其已发布的旗舰模型 **Hy3** 推出 **1-bit 与 4-bit** 量化版本。Hy3 为 **295B MoE** 架构、Apache 2.0 开源、商用友好、面向 agentic 场景（首发时曾在 OpenRouter 提供两周免费 API），官方称同体量领先、可对标万亿级旗舰；本次量化版本使该 295B 模型可在**单张 GPU** 上服务，支持通过 llama.cpp 启用 MTP（多 token 预测）运行。
  > 💡 295B MoE 用 1-bit 压到单卡可服务，是「旗舰模型单卡化」的标志性案例，直接降低 agentic 应用的部署门槛与单位成本；腾讯借此把开源旗舰从「能跑」推向「便宜可大规模服务」，与 PrismML 端侧 1-bit 路线形成端-云两端呼应。
   - 来源: [@TencentHunyuan](https://x.com/TencentHunyuan/status/2076953120765280284) | [HuggingFace](https://huggingface.co/tencent/Hy3)

### 产业动态
**OpenAI 首款硬件设备据报为可移动无屏音箱，定位 ChatGPT 的实体伴侣**
- 据 Bloomberg，OpenAI 与 Jony Ive 合作的硬件首款设备是一款**无屏幕、可移动**的音箱，包含「可自行移动的机械部件」，设计目标是「感觉像同伴，成为 OpenAI ChatGPT 的实体化身」。产品定位为 ambient companion，而非带屏智能终端。
  > 💡 OpenAI 硬件选择「无屏 + 可移动 + 伴侣化」形态，回避与手机/带屏 AI 硬件正面竞争、押注环境式语音伴侣；这与 Humane、Rabbit 等 AI 硬件遇冷形成对照，能否跑通取决于语音交互与场景黏性。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/14/openais-first-hardware-device-is-reportedly-a-screenless-speaker-that-can-move/)

**Cognition 回顾收购 Windsurf 一周年：团队增至 350 人，年化收入突破 5 亿美元**
- Cognition 发文回顾收购 Windsurf 一周年。过去 12 个月团队从 **44 人增至 350 人**，品牌合并后年化收入（ARR）从 **7300 万美元增至 5 亿美元以上**；自研模型迭代至 **SWE-1.7**（上周发布，号称其训练过最高效、最强模型，推理约 1000 tokens/s），并推出 Devin Review、Devin CLI、Devin 2.2、Windsurf 2.0 与 Devin Desktop（统一品牌入口），还面向政府推出 Cognition for Government 并推出「AI 生产力保证」。Devin 已从初级工程师水平进化到可启动、调度、管理其他 Devin 的中高级水平，并能用 computer use 自测与自修复。
  > 💡 一年内 ARR 翻近 7 倍、团队扩张 8 倍，Cognition 用「自研编码模型 + 多 agent 调度 + IDE/桌面统一入口」把 Devin 从单任务工具推向自驱动软件开发平台；AI 编程赛道正从「补全/单任务」向「调度多个 agent 的工程师操作系统」升级，Cognition 的营收增速为该赛道商业化进度提供了硬参照。
   - 来源: [Cognition Blog](https://cognition.com/blog/one-year-of-building-together) | [@cognition](https://x.com/cognition/status/2077080430038200605)

**Google与纽约大都会艺术博物馆合作，推出Met Prototypes & Play生成式AI体验**
- Google在The Keyword博客宣布与纽约大都会艺术博物馆（The Met）合作上线Met Prototypes & Play项目，利用生成式AI让用户以新方式探索馆藏。双方此次合作旨在庆祝**15年**的数字创新伙伴关系，并推出两个生成式AI项目：其中Art Aura工具可帮助用户探索艺术品之间的主题联系，同时推出新的驻馆技术员项目以提升实体馆参观体验。用户可通过新的Google Arts & Culture登陆页面浏览超过**200,000**件数字化藏品。Google Arts & Culture副总裁兼创始人Amit Sood表示，这些项目旨在加深人们在线发现和体验艺术的方式。
  > 💡 Google持续把生成式AI落地到文化场馆场景，更多是品牌示范和用户教育，而非变现驱动。
   - 来源: [The Keyword](https://blog.google/company-news/outreach-and-initiatives/arts-culture/the-met-ai-initiatives/)

**NVIDIA NeMo团队推出agentic优先RL框架Molt，vLLM负责rollout**
- NVIDIA NeMo 在 labs-molt 开源面向研究的 agentic-first RL 框架 **Molt**（Apache 2.0，约 8.6K 行代码）。栈极简：**Ray** 负责放置与异步队列、**vLLM** 负责 rollout、**NVIDIA AutoModel + FSDP2** 负责纯 PyTorch 训练，定位为可扩展到 **1T 级 MoE** 的全异步、多模态、多轮 agentic RL 最小栈。核心设计是「agent 即程序、单一可训练 actor」--奖励为任意 Python（grader、多轮工具、VLM 环境、LLM-as-judge），rollout/训练/权重同步全异步重叠；官方对标 OpenRLHF/verl/slime，强调单 actor、agentic 研究优先，是 NVIDIA 自家在 agentic RL 后训练栈上的正面布局。
  > 💡 Molt 是 NVIDIA 在 agentic RL 后训练栈上对 OpenRLHF/verl/slime 的正面回应，差异化在单 actor、全异步的极简 PyTorch 栈、原生支持 1T 级 MoE 与多模态多轮工具，把 agentic RL 研究门槛与 frontier-scale 训练打通；与同期 vime（AMD ROCm）、SAO（GLM）共同说明 agentic RL 后训练栈正成为模型竞争新战场，vLLM 作为 rollout 引擎被多框架收敛采用、正从推理框架固化为 RL 基础设施组件。
   - 来源: [GitHub](https://github.com/NVIDIA-NeMo/labs-molt) | [Tech Report](https://www.researchgate.net/publication/409325071_Molt_A_Scalable_PyTorch-Native_Training_Framework_for_Agentic_Reinforcement_Learning) | [@vllm_project](https://x.com/vllm_project/status/2076857285046055206#m)

### 算力追踪
**纽约州签署全美首个数据中心建设暂停行政令，AI 算力扩张遭遇州级监管天花板**
- 纽约州州长 Kathy Hochul 于本周二签署行政令，对全州大型数据中心（50 兆瓦及以上）实施临时审批冻结，成为美国首个出台此类全州暂停措施的州，针对 AI 驱动的数据中心建设热潮，要求州能源部门评估其对电网、环境与水资源的影响后再定后续政策。冻结期内暂停受理新建与扩建申请，涉及 AWS、Microsoft、Google 等主要云厂商在该州的扩张计划。
  > 💡 纽约州是全美首个以行政令直接冻结 AI 数据中心审批的州，此前类似阻力主要集中在弗吉尼亚、得克萨斯等数据中心密集州的县市级层面；地方反数据中心情绪正从县市级向州级升级，可能影响北美大型云厂商选址，并推动增量产能导向水电资源更充裕的州。
   - 来源: [The Information](https://www.theinformation.com/briefings/new-york-becomes-first-state-enact-data-center-moratorium) | [TechCrunch](https://techcrunch.com/2026/07/14/new-york-state-halts-construction-of-all-new-data-centers/)

**AWS 算力供不应求，初创公司转向新云厂商寻求 GPU**
- 据 The Information，部分 AI 初创在 AWS 上难以获得足够的 Nvidia 算力，转而尝试新兴云厂商。开源 AI 开发商 Arcee 2024 年曾承诺三年向 AWS 支付 800 万美元用于存数据与跑模型，但因拿不到足够 Nvidia 服务器，最终大部分负载跑到别处。报道反映头部云厂商在 AI 算力需求下面临供应瓶颈，为新兴云厂商留下市场窗口。
  > 💡 AWS 算力供不应求把部分负载推向新兴云，与同日 Reflection-Nebius 10 亿美元算力订单共同说明：AI 算力需求已超出超大规模云厂商的供给节奏，二线/新兴云与专项算力供应商正在分流增量负载。
   - 来源: [The Information](https://www.theinformation.com/articles/startups-try-new-cloud-companies-aws-faces-heavy-demand)

**Reflection AI 与 Nebius 签订 10 亿美元算力订单**
- Reflection AI 与算力供应商 Nebius 签订 **10 亿美元**算力访问协议。Reflection 成立于 2024 年，专注开源 AI 与编码 agent。该订单反映头部 AI 初创在算力采购上的规模化投入，也凸显独立算力供应商 Nebius 在承接大额订单上的角色。
  > 💡 10 亿美元级算力订单显示 AI 初创对长期算力锁定的押注规模，Nebius 作为独立算力供应商正成为超大规模云之外的重要供给方；算力采购正从「按需租用」走向「多年期大额锁定」，是算力市场结构变化的风向。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/14/reflection-inks-1b-compute-deal-with-nebius/)

### 初创&融资
**DeepSeek 在首轮 74 亿美元融资后启动新一轮，据报拟再融 15 亿美元并计划 2027 年 IPO**
- DeepSeek 在完成首轮 **74 亿美元**融资（投后估值逾 500 亿美元）后仅数周即启动新一轮融资，节奏在中国大模型公司中极为罕见。据 TechCrunch 援引知情人士，本轮拟募集约 **15 亿美元**、估值约 **710 亿美元**，并寻求在 **2027 年**完成 IPO（最早或于今年底）。快速资本化路径反映其在顶级模型研发、算力采购与海外拓展上的资金需求，叠加 IPO 计划，与国内同行形成差异化。
  > 💡 DeepSeek 将新一轮融资与 18 个月内 IPO 锁定，资本市场对头部中国大模型公司给出明确退出预期；若 2027 年完成 IPO，将成为少数在港/A股之外寻求上市路径的中国大模型公司，融资节奏本身亦是产业信号。
   - 来源: [The Information](https://www.theinformation.com/briefings/deepseek-plots-another-funding-round-weeks-raising-7-4-billion) | [TechCrunch](https://techcrunch.com/2026/07/14/deepseek-reportedly-in-talks-to-raise-1-5b-then-ipo/)

**强化学习之父 Richard Sutton 离开 Keen Technologies，创办 RL 新公司 Oak Lab**
- 强化学习奠基人 Richard Sutton 宣布与 Khurram Javed 离开 John Carmack 创办的 Keen Technologies，自立创办新公司 **Oak Lab**，继续以强化学习为核心、强调智能源于运行时经验，但主张当前深度学习方法「弱且低效」，需要的不是更多微调而是「根本性新思路与彻底重构」才能为 AI 的更高目标提供坚实基础。Sutton 对 Keen 与同路线的 Ineffable 仍表认可，三者共同押注 RL 与运行时学习，但 Oak Lab 选择了不同于 Keen 的技术路径。
  > 💡 Sutton 作为 RL 理论奠基人（TD 学习、强化学习教科书作者）亲自下场创业，且明确质疑主流深度学习路线、主张范式级重构，是 RL 学派对当前「scaling + 深度学习」主流的标志性分流信号；与 Keen（Carmack）、Ineffable 形成「RL 三家」格局，值得跟踪其是否能在运行时学习上跑通区别于梯度下降的新机制。
   - 来源: [@RichardSSutton](https://x.com/RichardSSutton/status/2076663628301058329) | [@mark_k](https://x.com/mark_k/status/2076667108688003127)

**Nous Research 洽谈新一轮融资，估值 15 亿美元**
- 开源模型与 agent 厂商 Nous Research（Hermes 系列、agent 产品）正洽谈新一轮融资，估值约 **15 亿美元**，拟至少募集 **7500 万美元**，由 Robot Ventures 领投，USV 等参投。融资反映开源模型/agent 赛道的资本热度，以及 Nous 在开源社区中的地位。
  > 💡 Nous Research 以开源 Hermes 系列与 agent 能力获 15 亿美元估值，显示开源模型/agent 路线在资本市场获得独立定价；与同期 Oak Lab、Reflection 等共同构成「开源 + agent」创业潮的资金面信号。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/13/hermes-agent-maker-nous-research-in-talks-for-new-funding-at-1-5b-valuation/)

### 研究关注
**SAO 单 rollout 异步优化在 agentic RL 上稳定超越 GRPO，已用于 GLM-5.2 训练**
- 针对 agentic 长程任务中传统同步、batch 交错 RL 流水线低效、异步 RL 又面临训练稳定性与 off-policy 挑战的问题，清华 GLM 团队（唐杰、董雨潇，第一作者侯振宇）提出 **Single-rollout Asynchronous Optimization（SAO）**：用「每条 prompt 仅一次 rollout」的单 rollout 采样替代 GRPO 的组采样以降低 off-policy 效应并改善泛化，配合 value-model 训练设计与严格的双向 token 级 clipping 提升优化稳定性。方法可稳定训练 **1000 步**，在 **SWE-Bench Verified、BeyondAIME、IMOAnswerBench** 等 agentic 编码与推理基准上持续优于 GRPO 及其变体，并在模拟在线学习（环境持续演化）场景下尤为有效；该方案已部署于开源 **GLM-5.2（750B-A40B）** 的 agentic RL 训练流程。
  > 💡 SAO 直击 agentic RL 的两个真实瓶颈--长程 rollout 让组采样低效、异步更新引入 off-policy 不稳定；其「单 rollout + 双向 clipping」把异步 RL 从「快但不稳」推向「快且稳」，并已被 GLM-5.2 采纳，是 agentic RL 后训练工程化的重要信号；与同期 NVIDIA Molt、vime 等 agentic RL 框架共同说明 RL 后训练基础设施正成为新一轮模型竞争的核心战场。
   - 来源: [arXiv](https://arxiv.org/abs/2607.07508) | [@jietang](https://x.com/jietang/status/2076913247316492510)

**Sparse Delta Memory 用稀疏寻址扩容线性 RNN 隐状态，长程检索显著提升**
- 线性注意力模型每 token 计算与状态大小固定，长上下文召回弱于 softmax Transformer，而增大状态提升召回却推高 FLOPs。Meta FAIR 团队（Hervé Jégou、Gabriel Synnaeve、Matthijs Douze、Justin Carpentier、Loïc Cabannes 等）提出 **Sparse Delta Memory（SDM）**，在 Gated DeltaNet 基础上把稠密 key-value 外积替换为对大规模显式内存的**稀疏读写**，将门控线性 RNN 隐状态扩到高一个量级容量。在 **isoFLOP、等参数**约束下，更大状态容量显著提升 in-context learning 与长上下文检索；把 SDM 内存初始状态作为参数化记忆学习后，模型在常识与推理任务上普遍提升。
  > 💡 线性 RNN 的核心瓶颈是固定状态容量限制长程召回；SDM 用稀疏寻址扩容而不等比例增加 FLOPs，由 FAIR 核心团队出品，是沿「状态容量可扩展」推进线性 RNN、在长上下文上追赶 Transformer 的代表性路线。
   - 来源: [arXiv](https://arxiv.org/abs/2607.07386)

**Direct-OPD 把弱模型 RL 增益迁移给强模型，Qwen3-1.7B 在 AIME 从 48.3% 升至 58.3%**
- RLVR 能提升 LLM 推理但每个新强模型都要重跑大量 rollout，后训练成为瓶颈。清华智能产业研究院（AIR）团队（张亚勤、马维英、周浩等，第一作者冯世远）提出弱到强替代：在小模型上跑 RL（rollout 更便宜），再把所学迁移给强模型。直接蒸馏 post-RL 弱教师不够（其策略混杂 RL 收益与小模型局限），故提出 **Direct On-Policy Distillation（Direct-OPD）**：用「post-RL 教师 vs 其 pre-RL 参考」的 log 比作为对强学生 on-policy 状态的稠密隐式奖励，迁移 RL 引起的策略偏移而非最终策略。实验中仅用 **8 张 A100、4 小时**即把 **Qwen3-1.7B** 在 AIME 2024 上从 **48.3%** 提到 **58.3%**，优于多种基线。
  > 💡 直击 RL 后训练算力瓶颈--强模型直接跑 RLVR 太贵，Direct-OPD 把昂贵 rollout 留在小模型、再「提纯」迁移给强模型；思路新颖、数据硬（4 小时/8 卡显著涨点），来自张亚勤、马维英团队，是后训练效率方向的高信号工作。
   - 来源: [arXiv](https://arxiv.org/abs/2607.05394)

**Sakana AI 提出「智能细胞砖」：模块化物理单元靠局部协作实现形状识别与损伤自愈**
- Sakana AI 联合学术团队（含 Sebastian Risi 等）在 Nature Communications 发表 **Smart Cellular Bricks（智能细胞砖）**。该系统由若干模块化「砖块」物理单元组成，每块砖内嵌一个**神经细胞自动机**（neural cellular automata，一种让单元按学到的局部规则自组织的仿生 AI，类似生物细胞自组织）；砖块之间只与相邻邻居通信、各自本地处理，却能集体完成形状分类，并在部分单元故障时自愈。系统在保持高分类准确率的同时对故障鲁棒，是受生物启发的可自修复模块化物理系统，面向软体/模块化机器人等真实场景。
  > 💡 这是 Sakana 把「涌现/演化式 AI」从数字世界向物理模块化系统延伸的尝试；去中心化、可自修复的模块化思路对软体/模块化机器人有启发，但属较垂直的生物启发计算，对主流大模型产业格局直接影响有限。
   - 来源: [Sakana AI](https://sakana.ai/smart-cellular-bricks/) | [Nature Communications](https://www.doi.org/10.1038/s41467-026-75166-7)

**ABot-AgentOS 提出机器人 Agent 操作系统与可执行基准 EmbodiedWorldBench**
- 长程具身 agent 需要一个位于底层控制器之上的运行时层来统一推理、记忆、工具、验证与跨本体执行。该工作提出通用机器人 Agent 操作系统 **ABot-AgentOS**，提供场景条件规划、上下文隔离的技能执行、多阶段验证、多模态记忆与端云协同，并引入通用多模态图记忆（把对话、视觉观测、空间上下文、时序关系、任务轨迹转为类型化节点与边）。配套发布可执行基准 **EmbodiedWorldBench**，含 **16** 个室内/室外/混合场景、**4** 个难度档、**200+** 任务并采用轨迹接地评分；其失败驱动自演化循环将诊断出的记忆失败转为受控运行时资产，避免评测集泄露，在基准子集上较单控制器基线在任务成功率与目标完成度上均有提升。
  > 💡 把具身 agent 从「单步 VLA 预测」上升到带记忆/验证/自演化的运行时操作系统并给出可执行基准，方向符合具身智能从模型层向系统层演进；但作者团队影响力不突出、属系统整合类工作，分享优先级低于同期有强团队或新机制的研究。
   - 来源: [arXiv](https://arxiv.org/abs/2607.10350)

**MIT 团队证实 LLM 自发涌现与人脑对应的功能模块化架构**
- MIT 团队（第一作者韩芃睿，资深作者 Evelina Fedorenko、Jacob Andreas）在预印本《Modular Cognitive Architecture Emerges in Large Language Models》中，用 **attribution patching** 对 **6** 个前沿 LLM（24B–123B）在跨 **4 个认知域**（语言、形式推理、物理推理、社会推理，分别对应人脑语言网络、多需求网络、直觉物理网络、心智理论网络）的 **46** 项任务上定位任务支撑神经元。发现 LLM 自发涌现与人脑类似的模块化结构：同人脑网络的任务在 LLM 中招募重叠神经元、不同网络招募不同神经元（域内重叠 **12.9%** vs 域间 **3.0%**，约 4.3 倍，聚类 ARI=**0.78**）；因果消融验证选择性--消融某域神经元致该域准确率下降 **25.9%**、跨域仅 **2.5%**（10.3 倍）。形式与内容可分离：消融语言神经元致语法错但推理保留，消融物理神经元致推理反转但语法完好；控制实验显示 GPT-2（124M）因无法解题而不出现精细模块化，说明模块化以任务能力为前提，且并非源于代谢成本（Transformer 前向无此压力），而可能源于避免计算干扰。DeepTech 曾就此对韩芃睿做长篇访谈。
  > 💡 该工作用因果消融（而非仅相关性）证明 LLM 功能模块化与人脑对应、且以能力为前提，为模型可解释性、能力定位与安全审计提供机制级工具；Fedorenko 是人脑语言网络研究权威、Andreas 为 MIT 知名学者，团队影响力强，是本日研究关注中机制洞察最清晰的一项。
   - 来源: [项目主页](https://pengrui-han.github.io/LLM_Modularity_Page/) | [DeepTech深科技](http://mp.weixin.qq.com/s?__biz=MzA3NTIyODUzNA==&mid=2649800678&idx=1&sn=136cf939f982733f7a85f4eecff740c2&chksm=86c048d2bcdcccaf4de715a28e34ef9d21d011a72a86bd0accccec97fd6f444c72fa6c4a4d26&scene=0&xtrack=1#rd)

### X讨论
**Demis Hassabis 发表前沿 AI 治理框架，呼吁建立美国主导的全球 AI 监管机构**
- Google DeepMind CEO、2024 年诺贝尔化学奖得主 Demis Hassabis 在 X 发表长文《A Framework for Frontier AI and the Dawning of a New Age》，称 AGI「大概只有短短几年」之遥、其影响或达工业革命的 **10 倍且以 10 倍速度**展开，人类正站在「奇点山脚下」。其核心倡议是美国牵头建立 Frontier AI Standards Body，参照 **FINRA** 模式由联邦监管的公私合营/自律组织构成，董事会含独立技术专家与开源代表、资金主要来自业界；该机构按基准阈值认定「Frontier-class」模型与「Frontier Labs」，要求 Lab 公布 model card、强化内部网络安全、关键岗位审查并投入安全研究。Frontier Labs 起初在发布前 **30 天**自愿送审，评估流程成熟后转为进入美国市场的前置强制；评估覆盖网络安全、生物威胁等高风险域与 agentic 安全（如绕过护栏、欺骗），约每季度更新并最终建立独立 held-out 测试防过拟合，必要时可**协调 Frontier Labs 放缓开发**。框架适用于达到阈值的模型（不分国别、开源闭源），初创与学术界非前沿模型豁免。据 Axios，Hassabis 已数月游说特朗普政府、其他实验室及欧洲官员，希望今年底前启动，并称特朗普政府反馈「非常积极」。
  > 💡 这是头部 AI 实验室掌门人首次系统提出带强制力（发布前评估 + 行业级放缓）的全球治理方案，且明确押注美国主导；若年底前落地，将直接改变前沿模型的发布节奏与合规成本，对 OpenAI、Anthropic、DeepMind 自身及中国大模型出海均构成新的监管变量。
   - 来源: [The Verge](https://www.theverge.com/tech/965270/google-deepmind-demis-hassabis-global-ai-watchdog) | [@demishassabis](https://x.com/demishassabis/status/2076957440109625718)

**Perplexity 开源 WANDR 基准：评测需「广而深」检索的研究 agent，最强系统仅 0.363 soft F1**
- Perplexity 开源 **WANDR（Wide ANd Deep Research）** 基准与评测框架，含 **500** 个现实、高难度的知识工作数据采集任务（竞争图谱、尽调、文献综述、市场分析、人才寻访等），是其深度研究基准 DRACO 的「广度」姊妹版。任务用可组合的「资格键层级」表达（如 company(n)->employee(m)->url(k)），每条路径可独立验证，采用无参考答案、基于 agent 所引证据的逐记录验证评分。评测 6 个生产系统：Perplexity Search as Code 以 **0.363 soft F1 / 0.133 hard F1** 领先，Anthropic 次之（0.249/0.072），其余最高 0.121/0.035--广而深研究远未解决；关键发现是部分进展常见而完整覆盖稀缺，规模与层级深度越大掉点越严重，发现（discovery）是首要结构瓶颈。
  > 💡 WANDR 抓住研究 agent 的真实痛点--不是找一个答案，而是大规模发现并对每条证据完整取证；最强系统 hard F1 仅 0.13 说明当前 agent 在「广度覆盖 + 逐条证据完备」上仍有数量级差距，其逐记录/逐分支评分可为研究 agent 的 RL 训练提供部分奖励信号。
   - 来源: [Perplexity Research](https://research.perplexity.ai/articles/wandr-benchmark-evaluating-research-agents-that-must-search-wide-and-deep) | [@perplexity_ai](https://x.com/perplexity_ai/status/2077099503723946121)

**OpenRouter 上线 MCP Server，Agent 可在编辑器内发现、排序、测试并对比模型**
- OpenRouter 发布官方 MCP Server（远程托管、OAuth 登录、无需本地安装），支持 Claude Code、Codex CLI、Cursor、OpenCode 等客户端接入。Agent 可在不离开编辑器的情况下调用一组工具：models-list 按价格、上下文长度、benchmark 索引、工具调用成功率等筛选排序模型，rankings-daily 与 app-rankings 查看用量及趋势，benchmarks 拉取 Artificial Analysis 与 Design Arena 评分，chat-send 发送测试推理（唯一计费调用），并支持查询账户余额；模型推荐基于实时数据而非模型记忆，使「该任务用哪个模型」的决策在编辑器内闭环。
  > 💡 OpenRouter 把模型市场能力（实时价格、benchmark、用量排行）以 MCP 工具暴露给编码 agent，本质是让 agent 自主完成「模型选型-测试-对比」闭环；这把模型路由从开发者手动决策下沉为 agent 运行时能力，叠加其 7 天/10 美元默认额度的独立密钥设计，可能进一步强化 OpenRouter 作为 agent 时代「模型聚合层」的位置。
   - 来源: [OpenRouter Docs](https://openrouter.ai/docs/guides/overview/mcp-server) | [@OpenRouter](https://x.com/OpenRouter/status/2077131714678435994)

---
*更新时间: 2026-07-15 08:10*
