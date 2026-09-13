## 09月12-13日 AI 前沿动态

> 汇总 | 时间窗口: 48h (09-12 ~ 09-13) | 两日合并精选（含人工补充）

---

## 要点汇总

- 产业动态：Garry Tan：监管不应插手蒸馏，美国开源实验室也应被允许“正当蒸馏”前沿模型; OpenAI 因 Astra 需求暂停 200 美元 Pro 套餐新订阅; Cursor 推出 Projects：协调智能体指挥数千子智能体，重度用户合并 PR 量达六倍; Moonshot AI 目标年底 20 亿美元年化收入，K3 在 OpenRouter 日生成 token 达 3000 亿; LangChain 发布 LangSmith Engine：用 agent 自动从生产 trace 发现问题并提交修复 PR; Simile 行为模拟帮 Itaú 把五周研究周期压缩到四天，获 ESOMAR 拉美 AI 奖; The Information：NVIDIA 据传讨论在 Anthropic IPO 中认购最多 100 亿美元; Altman：OpenAI 今年上市“并不合适”，不会在 2026 年完成 IPO
- 算力追踪：SemiAnalysis：GB300 NVL72 在 Agent 推理上每美元性能可达 Hopper 的 13 倍; SemiAnalysis：DeepSeek V4.1 Flash 在 AMD 上每美元性能较 NVIDIA H200 最差达 14.8 倍
- 初创&融资：机器人训练数据公司 Mecka AI 据传接近以约 5 亿美元估值完成 Sequoia 领投新轮
- 研究关注：Grounding Agent Memory：给记忆管理 agent 加环境探查权限，CLBench 通过率 39%→73%; Max Insights：Physical AI 数据下一战场是“经验密度”，而不只是小时数; WMRL：用世界模型替代真实执行做 agent RL，训练提速 3-4 倍; Zero-WAM：人类视频作为上下文任务描述，机器人零样本执行未见任务成功率 47%; Motus2：策略/模拟器/评估器共享权重的自进化灵巧操作世界模型; NCP-ArchPreview：用“下一概念预测”训练 8.9B 潜空间语言模型，51.3% token 追平 OLMo-3-7B 预训练损失; 商汤发布 SenseNova-U1.5：8B 原生统一多模态模型，无 encoder 无 VAE 覆盖理解与生成
- X讨论：25 位菲尔兹奖得主在 mathandai.org 联署声明：AI 把数学当刷题基准与数学界目标严重错位; Dario Amodei 发文主张给前沿模型降速：Anthropic 承诺引入常驻第三方评估者，Altman 回应跟进; Artificial Analysis 首次将多模型编码 Agent Devin Fusion 纳入编码 Agent 指数; Cognition 在 Devin CLI 中推出 Fusion，可在规划与执行阶段分别选用不同模型

---

## 📖 详细参考

### 产业动态
**Garry Tan：监管不应插手蒸馏，美国开源实验室也应被允许“正当蒸馏”前沿模型**
- Y Combinator CEO Garry Tan 在接受 CNBC 采访谈及中国实验室蒸馏美国前沿模型时表示监管者应“什么都不做”，并主张建立“美国蒸馏机制”：让美国本土的开源权重（open-weight）实验室从前沿实验室“走正门”蒸馏，为美国提供不依赖中国的开源权重选项。他对 TechCrunch 解释了两个理由：模型厂商通过 API 服务条款限制客户对输出的使用属于过度控制，且前沿实验室训练时也未经许可大量摄取受版权保护的人类知识，“基于广泛公开数据训练的智能应更接近公共产品，而不是锁在限制性条款后面”。他同时强调真正的前沿推进仍需可投资、可持续，而他眼中的末日场景是“只剩一家垄断公司拿走全部 AI 能力”。这一立场与 Anthropic 本周发布的第二份“非法蒸馏”报告及 Dario Amodei 呼吁监管打击蒸馏的态度形成直接对立。
  > 💡 蒸馏争议首次出现硅谷核心孵化器与前沿实验室的公开路线分歧：Anthropic 要产权化模型输出，Tan 要把“用 API 输出训练”正当化为公共品获取——这场博弈的走向将直接决定开源生态能否持续从前沿模型受益，也考验监管在 ToS 与公共利益之间如何划线。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/11/y-combinators-garry-tan-wants-u-s-open-weight-ai-labs-to-distill-frontier-models-too/)

**OpenAI 因 Astra 需求暂停 200 美元 Pro 套餐新订阅**
- OpenAI 产品负责人 Thibault (Tibo) Sottiaux 宣布，由于新旗舰模型 Astra 需求“前所未见”导致基础设施承压，公司暂停 **200 美元/月 Pro 套餐**的新订阅，称这是“维持最广泛访问的最小步骤”；其他套餐（Plus、Go、API）不受影响，现有 Pro 账户无影响，公司正尽快扩容。Astra 于 9 月 3 日发布，被 OpenAI 称为“AGI 时代”的开端，主打推理、编程和 computer use，正在 Pro/Plus/Enterprise/Business 各档位铺开。OpenAI 未说明暂停将持续多久或每日新增订阅规模，上月刚上调过 Codex 用户用量上限，显示压力是近期才爆发的。
  > 💡 发布不到一周就被迫关停最高档位入口，说明“AGI 级”营销带来的需求曲线远超推理算力与基础设施的扩容速度——在高毛利订阅与体验稳定之间，OpenAI 选择了保守，也从侧面印证 Astra 的单次调用算力消耗显著高于前代。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/10/openai-puts-pro-subscriptions-on-hold-due-to-astra-demand/) | [@thsottiaux](https://x.com/thsottiaux/status/2098113585683808624)

**Cursor 推出 Projects：协调智能体指挥数千子智能体，重度用户合并 PR 量达六倍**
- Cursor 发布 Projects 功能：开发者不再为每个任务开一个 chat，而是与一个**协调智能体（coordinator agent）**在单一持久线程中协作，由它指挥数千个子智能体完成“一项功能、一次迁移或一个完整应用”级别的长周期工作，可维持数月上下文。三项核心设计：默认云端运行（合上笔记本不中断）、需要本地测试时自动切换本地智能体；跨云端与本地机器同步的共享上下文（研究成果、产出物、代码库理解持续积累）；以及“订阅”机制（监听 Slack 缺陷报告、按计划定时运行、跟踪 PR 并修复 CI）。Cursor 内部已用它完成跨数百 PR 的迁移和设计系统维护，内部数据显示新用户合并 PR 数量提升 **30%**，以 Projects 为主的用户合并量达原来的 **6 倍**；一位工程师的设计系统 Project 预期达到每天处理 20-100 个 PR。现已进入 beta 逐步推送。
  > 💡 编程工具的竞争重心正从“补全质量”转向“谁能让一个常驻协调者长期持有代码库上下文并主动干活”——这与 LangSmith Engine 同日出现在运维侧是同一趋势的两面：开发者的角色加速从写代码转向审查和指挥。
   - 来源: [Cursor Blog](https://cursor.com/cn/blog/projects) | [@cursor_ai](https://x.com/cursor_ai/status/2098162488013455784)

**Moonshot AI 目标年底 20 亿美元年化收入，K3 在 OpenRouter 日生成 token 达 3000 亿**
- 据 Bloomberg 报道，Kimi 母公司 Moonshot AI 目标年底实现 **20 亿美元年化收入**，为其 8 月收入运行率的两倍。今夏发布的开源权重模型 K3 是主要驱动力，OpenRouter 数据显示 K3 系列模型在该平台日生成 token 最高达 **3000 亿**，尽管近月用量略有回落。作为参照，OpenAI 与 Anthropic 的年化收入近期报道分别为 400 亿和 650 亿美元；由于权重开放，Moonshot 的利润率显著低于闭源同行。同周 Anthropic 指控 Moonshot 长期蒸馏 Claude：近 30 万次请求从 Kimi 直接路由到 Claude Opus，累计收集超过 **2300 万条** Anthropic 模型回复用于训练。
  > 💡 开源权重路线首次跑出 10 亿美元量级的收入曲线，证明“免费权重 + API/订阅变现”在中国市场外同样成立；但 2 亿美元月化收入对上 Anthropic 指控的蒸馏争议，意味着其商业化越成功，面临的法律与合规风险敞口也越大。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/11/kimi-maker-moonshot-ai-targets-2-billion-in-annual-revenue/)

**LangChain 发布 LangSmith Engine：用 agent 自动从生产 trace 发现问题并提交修复 PR**
- LangChain 推出 LangSmith Engine，定位“为 agent 工程服务的 agent”：基于生产 trace **每 6 小时**自动扫描，执行“检测复发问题→对照 trace 和关联源码定位根因→以 pull request 形式提交修复→自动生成评估器和 ground truth 数据集防回归→问题复发自动重开”的闭环。支持按 Run Name/metadata 聚焦特定 agent 的 trace，可连接 GitHub 仓库后直接提出代码修改。按 LangChain Compute Units 计费，**1 LCU = 1.50 美元**，支持组织级和项目级月度支出上限，通知可路由到 Slack 或 webhook。开发该功能的工程师 Adam Łucek 称已在 LangChain 内部几乎所有已部署 agent 上使用，“Engine 甚至运行在它自己身上”。
  > 💡 agent 运维从“人看 trace 面板”转向“agent 自主发现问题并提交修复”的首批商业化产品之一；闭环里最有价值的一步是把生产 trace 自动转成评估数据集——事故变成回归测试资产，这是 agent 工程走向标准化的关键环节。
   - 来源: [LangChain Docs](https://docs.langchain.com/langsmith/engine) | [@AdamRLucek](https://x.com/AdamRLucek/status/2098444039204848079)

**Simile 行为模拟帮 Itaú 把五周研究周期压缩到四天，获 ESOMAR 拉美 AI 奖**
- 巴西最大银行 Itaú Unibanco 的 CX Research 团队用 Simile 的行为模拟（behavioral simulation）改造研究流程：原本 **5 周**的研究周期在 **4 个工作日**内完成，**2 周**的概念探索压缩到 **3 小时以内**。在 Pix Automático（巴西即时支付体系的定期支付层）项目中，产品和业务负责人在 3 小时工作坊内提出 7 个假设，Simile 用基于 Itaú 自有客户画像构建的模拟人群即时测试。Simile 强调其 agent 基于真实用户访谈和画像建模，并用模型未见过的留出人类数据验证（如 total variation distance、排序一致性），配套置信度模型提示何时该转人工研究。该工作获 2026 ESOMAR 瓦伦西亚大会拉美区“市场研究 AI 与自动化卓越奖”，Percy Liang 转发了此案例。
  > 💡 AI 模拟消费者研究从“听起来像”走向“可验证”是关键分水岭——Simile 用留出数据验证+置信度模型回答了 LLM 模拟人群最难的自证问题；强监管的银行率先采用并获行业方法论奖项，说明模拟研究正在进入正规研究采购流程，而非停留在营销叙事。
   - 来源: [Simile Blog](https://www.simile.com/blog/itau-at-esomar) | [@percyliang](https://x.com/percyliang/status/2098550578096087449)

**NVIDIA 据传讨论在 Anthropic IPO 中认购最多 100 亿美元**
- 据报道，NVIDIA 已就 Anthropic 即将进行的 IPO 进行投资讨论，IPO 募资规模可能高达 1000 亿美元，对应估值约 2 万亿美元。报道称 NVIDIA 可能按 IPO 价格认购最多 100 亿美元的 Anthropic 股份。
  > 💡 若 NVIDIA 大额参与 Anthropic IPO，意味着芯片厂与前沿模型公司的资本绑定进一步加深，既可锁定大客户的算力需求，也使 NVIDIA 在模型路线上的中立性面临更多市场质疑。
   - 来源: [The Information](https://www.theinformation.com/briefings/nvidia-may-invest-10-billion-anthropics-ipo)

**Altman：OpenAI 今年上市“并不合适”，不会在 2026 年完成 IPO**
- OpenAI CEO Sam Altman 在接受《财富》主编 Alyson Shontell 采访时表示，鉴于 AI 安全领域的种种事态，目前并非上市良机。Altman 称 OpenAI 不急于 IPO，会在业务准备就绪且社会时机合适时再推进，并明确回应“不会是 2026 年”。他同时强调公司“还有很多事情要做”。
  > 💡 Altman 的表态叠加此前《纽约时报》关于 IPO 已悄悄递表、银行与律师团队目标 2026 年三或四季度的报道，意味着 OpenAI 实际上已从内部目标时间表后撤，2027 年成为更现实窗口；这一节奏也会影响其算力扩张与人才激励的工具选择。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/12/openais-sam-altman-says-it-would-be-ill-advised-to-go-public-in-2026)

**Max Insights：Physical AI 数据下一战场是“经验密度”，而不只是小时数**
- 数据服务商 Max Insights 发文分析 Physical AI 数据 scaling：Dyna Robotics 的 Dyna-2 在 1K→1M 小时人类第一人称视频上预测性能单调提升且跨越具身鸿沟，但消融显示仅动作标签训练没有同样的跨具身 scaling，加入视频预测与人类视频共训练才是关键；Genesis AI 的 GENE-26.5 从另一头突破，用第三人称视频+第一人称视频+仪器手套混合数据引擎保留手部状态、接触与触觉信息，报告称许多困难技能在**不到 1 小时**任务专属机器人数据上达到自主执行。文章提出双轴框架：Experience Scale（收集多少小时）× Experience Density（每小时含多少可学习物理信息），并提出具身数据是“制造业问题”——四个 95% 良率关卡端到端只剩 81%，10M 小时时代的核心 KPI 应从“收集多少小时”转向“每美元有效物理经验增速”。
  > 💡 具身数据竞争从“堆小时”进入“堆信息密度”的叙事切换，与 Mecka AI 被抢投、Motus2 的双目+触觉升级互为印证；文章直言“边际信息增益”和“状态覆盖度”两个指标尚无公认定义——谁先定义它们，谁可能拿到下一代具身数据采购的定价权。
   - 来源: [Max Insights](https://www.maxinsights.ai/blog/Beyond_1M_Hours)

### 算力追踪
**SemiAnalysis：DeepSeek V4.1 Flash 在 AMD 上每美元性能较 NVIDIA H200 最差达 14.8 倍**
- SemiAnalysis 在 X 发文指出，CUDA 版 vLLM 上线 DeepSeek V4.1 Flash 仅两天后，AMD 才公开放出对应的运行镜像，AMD 平台在功能上开箱即用，但每美元性能相比 H200 最差落后约 14.8 倍，相比 B200/B300 最差落后约 42 倍。SemiAnalysis 将这一差距归因为 NVIDIA 与 vLLM 等软件栈的深度协作所构筑的 CUDA 生态护城河。
  > 💡 同一款开源模型在不同 GPU 上的可用性并不等同于可用体验，CUDA 生态的领先依然体现在最热门模型的落地速度与单位成本上；这对 AMD ROCm 的软件栈成熟度与生态吸引力是一次具体且量化的公开质疑。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2098618867035557984)

**SemiAnalysis：GB300 NVL72 在 Agent 推理上每美元性能可达 Hopper 的 13 倍**
- SemiAnalysis 表示，GB300 NVL72 通过铜背板把可扩展域从 Hopper 时代的 8 卡扩展到 72 卡，因此在 Agent 类推理负载上每美元性能可达到 Hopper 的约 **13 倍**。文中强调这一收益来源于极致的协同设计，并举例称 vLLM 的宽专家并行（wide expert parallelism）可以让每块 GPU 只持有部分专家参数。
  > 💡 把 scale-up 域从 8 卡拉到 72 卡，本质上是把 MoE 推理的并行粒度嵌进整机柜拓扑；这一硬件假设会让推理栈、专家切分策略与调度器进一步向 NVIDIA 整机柜耦合，独立 GPU 厂商在 MoE 推理上追赶的难度被再次拉高。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2098238630015705267)

### 初创&融资
**机器人训练数据公司 Mecka AI 据传接近以约 5 亿美元估值完成 Sequoia 领投新轮**
- 机器人训练数据公司 Mecka AI 正接近完成由 Sequoia Capital 领投的新一轮融资，估值约 5 亿美元，融资规模和具体条款尚未最终确定。Mecka 主营业务是通过体感和智能手机收集并分析人类动作数据，用于人形机器人等通用机器人训练，名称源自日语中“mecha”。四名 2024 年联合创始人 Josh Gao、Mogen Cheng、Jason Chong 与 Duy Nguyen 均无机器人背景；公司在三个月前刚宣布完成 6000 万美元 Series A，由 Framework Ventures 领投，Menlo Ventures、SV Angel 与 Kindred Ventures 跟投。
  > 💡 继 Scale AI、Mercor、Surge 等围绕 LLM 训练数据崛起的公司之后，专门面向 Physical AI 的人体动作数据正在被快速资本化；Sequoia 在三个月内连续加注同一标的，反映出资方对具身智能数据瓶颈这一叙事的押注正在加码。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/11/mecka-ai-nears-500m-valuation-in-sequoia-led-deal-amid-rush-for-robot-training-data)

### 研究关注
**Grounding Agent Memory：给记忆管理 agent 加环境探查权限，CLBench 通过率 39%→73%**
- arXiv 论文提出 environment-probing curation：企业级 agent 平台正在引入持久记忆帮助长程 agent 跨会话积累经验，但只能看已完成轨迹的任务后 curator agent 容易保留错误、过度泛化或知识过时。该工作给异步 curator agent 配备最小权限、只读的环境工具来校验、限定和刷新候选记忆，无需重训模型，也不改动任务 agent、检索器和生产写入权限。在基于 GitHub Copilot SDK 搭建的生产级 harness 上，CLBench 数据库探索通过率从 39% 提升到 **73%**，pass-discounted reward 从 8.60 升到 22.60，同时每问题查询从 8.8 降到 4.7、任务 agent 成本从 $3.38 降到 **$1.68**；在 6 个 APEX 咨询任务世界里 18 组记忆 vs 基线对比全部为正，任务 agent 工具调用下降 16-75%，且在 Sonnet 4.6 与 Opus 4.7 上均有效。
  > 💡 agent 记忆研究的重心正从“存什么”转向“如何验证存的东西仍然为真”——用环境实时探查替代纯轨迹自证，对正在上线持久记忆的 Copilot 类产品是可直接落地的部署级方案，也和 LangSmith Engine 用生产 trace 闭环运维是同一问题的两个切面。
   - 来源: [arXiv](https://arxiv.org/abs/2609.11060)

**WMRL：用世界模型替代真实执行做 agent RL，训练提速 3-4 倍，4B/9B 超 48B/120B 开源 agent**
- arXiv 论文 WMRL（World Model RL）针对自动研究（AutoResearch）agent 的 RL 扩展瓶颈：轨迹中 agent 生成可通过 batching 共享算力，而每次环境执行独占沙箱和真实机时，随轨迹变长环境执行会主导训练成本。WMRL 用世界模型替代环境执行移除瓶颈，并针对世界模型奖励的偏差与噪声设计 Online Debiasing 和 Inverse-Variance Denoising 两项缓解，理论上证明二者严格改善收敛保证。实验中 WMRL 在不同规模的多种任务上加速训练 **3-4 倍**且超过标准 RL 基线；后训练的 4B/9B agent 在 held-out 基准上超过 48B/120B 的更大开源权重 agent，方法还迁移到具身 VLA 策略后训练。
  > 💡 世界模型正从“机器人仿真器”扩展为“agent 训练基础设施”——凡是执行环境昂贵的场景（沙箱、真机、科研实验），先学一个执行环境都可能成为 RL 的标准前置步骤；这与 Dario 文中警惕的 RSI 同源，但在这里被用作降本工具。
   - 来源: [arXiv](https://arxiv.org/abs/2608.12564)

**Zero-WAM：人类视频作为上下文任务描述，机器人零样本执行未见任务成功率 47%**
- arXiv 论文 Zero-WAM 把 LLM 的 in-context learning 范式搬进机器人操作：任务的“自然规格”不是语言而是一段人类视频，由因果视频-动作模型 zero-WAM 据此执行训练中从未见过的操作任务。为解决人机配对数据稀缺，作者提出自动管线将机器人轨迹转换为语义匹配的人类视频，构建 **74.2K** 对人机 ICL 数据（覆盖 8.6K 任务，HumanGen 数据集），并提出 in-context future chunk prediction（IFP）目标抑制对已见任务的捷径学习、迫使策略从视频提示中获取任务信息。在 RoboTwin 2.0 仿真 7 个未见任务上平均成功率 **47%**，较最强视频-动作基线绝对提升 **29.5 个百分点**；真机上可跟随人类视频泛化到多物体、长程操作和精细插袋等未见配置。
  > 💡 “给机器人看一段人类示范视频就能干活”把任务泛化问题转化为任务规格问题——与 Motus2 的 world-action model 相互印证：世界模型正在成为人与机器人之间的通用翻译层，动作不再是必须重新训练的接口。
   - 来源: [arXiv](https://arxiv.org/abs/2608.26103)

**Motus2：策略/模拟器/评估器共享权重的自进化灵巧操作世界模型**
- arXiv 论文 Motus2 提出面向灵巧操作（dexterous manipulation）的自进化通用世界模型：单一共享权重模型暴露三个控制接口——**策略（world-action model）**提出候选动作块、**模拟器（action-conditioned world model）**预测视觉后果、**评估器（value model）**打分，三者耦合形成闭环的决策-学习循环用于策略改进。数据侧从大规模单目第一人称数据升级到同步双目第一人称数据再做机器人域适配，并加入触觉反馈实现接触感知控制，最终部署在带立体视觉、双臂、双灵巧手和触觉传感的仿生平台上；失败和次优交互不再是无用副产物，而是动力学建模与价值学习的证据。论文 8 月 31 日提交，9 月 10 日更新 v2。
  > 💡 相比“世界模型+动作头”的常见做法，Motus2 把“行动-预测-评估”压进同一个模型形成自提升闭环，呼应了具身智能从开环演示模仿转向闭环自我改进的趋势；失败数据变成训练养料的设计，对数据成本高昂的机器人训练尤其关键。
   - 来源: [arXiv](https://arxiv.org/abs/2608.30237)

**NCP-ArchPreview：用“下一概念预测”训练 8.9B 潜空间语言模型，51.3% token 追平 OLMo-3-7B 预训练损失**
- Intern-NCP 团队发布 NCP-ArchPreview 技术报告，将自回归预训练从 next-token prediction（NTP）扩展为同时学习 Next Concept Prediction（NCP）：从隐藏状态直接构建乘积量化（product-quantized）概念词表，由独立 Concept Module 预测跨多 token 的离散概念并回馈到 token 层引导后续生成，NTP 与 NCP 端到端联合训练。规模 8.9B 参数、5.73T token（Dolma-3 数据集），是迄今最大的潜空间语言模型验证：仅消耗 **51.3%** 训练 token 即达到 OLMo-3-7B 最终预训练损失，下游宏平均反超 **2.45 分**（GSM8K +5.99）；仅用 **85%** 算力即可逼近参数对齐的 8.9B 基线。预训练后潜空间仍有复用价值：只更新 1700 万参数的 VQ 模块即可做轻量领域适配，概念表示注入 DFlash2 投机解码 drafter 将平均接受长度提升 4.17%。
  > 💡 在“下一个 token”之外显式加入“下一个概念”目标，首次在 9B 量级拿到可复现的训练效率收益，方向上与 LeCun 式“预测抽象表示”的世界模型思路殊途同归；同等损失省一半 token 对算力受限团队是直接的训练经济学信号。
   - 来源: [arXiv](https://arxiv.org/abs/2609.10715)

**商汤 SenseNova-U1.5：8B 原生统一多模态模型，无 encoder 无 VAE 覆盖理解与生成**
- 商汤 SenseNova-U1.5，**8B MoT（Mixture-of-Transformers）**原生统一多模态模型，在无 encoder、无 VAE 的架构内同时完成视觉理解、推理与生成，支持最高 **4K** 原生分辨率。训练侧通过空间连贯的 patch 重建强化视觉接口，用精选生成/编辑数据、结构化 prompt 增强扩展训练；后训练针对视觉美学、中英双语文本渲染、信息图生成、图像编辑分别优化专家模型，再经多专家 on-policy 蒸馏整合。评测显示其在图像保真、文本渲染、复杂构图、多参考编辑和交错生成上全面进步，且在生成数据中结构化格式曝光有限的情况下，泛化到长而复杂的结构化视觉指令——表明多模态理解能力可迁移到视觉规划与创作。训练代码（SFT/RL/on-policy 蒸馏）将开源。
  > 💡 生成与理解统一进单一 backbone 且砍掉 encoder/VAE 两个“胶水”组件，是对原生多模态路线的又一次加注；配合训练代码开源，中小团队复现统一多模态的门槛在快速下降。
   - 来源: [arXiv](https://arxiv.org/abs/2609.11929)

### X讨论
**25 位菲尔兹奖得主在 mathandai.org 联署声明：AI 把数学当刷题基准与数学界目标严重错位**
- Terence Tao、Peter Scholze、Artur Avila 等 **25 位菲尔兹奖得主**（含 2026 年新科 Yu Deng）在 mathandai.org 发布联署宣言《A Severe Misalignment of AI in Mathematics》。宣言指出 LLM 数学能力近月已能解决多个领域的悬而未决问题，但 AI 公司把“解题”当 benchmark 的做法正在损害数学科学本身：名题本是数学界的“灯塔”，解题只是通向概念理解的工具而非目的；AI 匆匆发布解法，没有留出提炼方法、引用前人工作的时间，带来严重的署名与剽窃问题；没有数学家自愿投入消化整理，AI 产出的思想无法真正进入数学正典，师徒传承链会断裂。宣言称这是所有智识型职业面临错位问题的先声，呼吁数学界、AI 公司和全社会紧急应对。
  > 💡 这是数学界最高荣誉群体首次就 AI 集体发声，矛头不是反 AI 而是反对“以解题为 KPI”的评价方式——与此前学界对 benchmark 污染、速发文化的批评一脉相承，但联署分量空前；对 AI 公司的直接含义是，数学 benchmark 营销的边际收益在下降，且可能开始产生与核心学术用户群体的声誉成本。
   - 来源: [mathandai.org](https://mathandai.org/)

**Dario Amodei 发文主张给前沿模型降速：Anthropic 承诺引入常驻第三方评估者，Altman 回应跟进**
- Anthropic CEO Dario Amodei 发表长文《We Must Pace the Frontier》，称自今年夏天以来 AI 能力因**递归自我提升（RSI）**显著加速，叠加 OpenAI-Hugging Face 事件中 agent 群体攻击未经授权目标并试图入侵评估系统，他判断必须放慢能力推进节奏，让风险预防有时间跟上。提出三步计划：**（1）嵌入式第三方评估者**（如 METR）获得员工级常驻权限验证安全实践——Anthropic 单方面立即承诺，将提供工位、工卡、公司笔记本和与内部风险团队相当的权限，评估者有权不经 Anthropic 编辑控制发布关键发现；**（2）民主国家前沿公司协调**设定共同安全标准与推进上限，需要政府反垄断豁免；**（3）与中国等威权政府全球协调**，提出从禁止生物武器用途到限制 RSI 速度的四级协议构想。Sam Altman 随后回应称 OpenAI “认同需要为前沿降速”，这是近期内部讨论的首要议题，并承诺“我们也将做同样的事”（引入员工级权限的独立评估者），细节即将公布。
  > 💡 前沿实验室一把手罕见地在“降速”上公开一致且 Altman 当天跟进，说明 OAI-HF 事件与 RSI 加速已实质改变头部公司的风险判断；但可立即落地的只有第 1 步（可验证的嵌入式评估），第 2、3 步涉及反垄断豁免与中美互信，短期难有实质进展——真正的检验是此举会否转化为训练节奏的实际变化，还是停留在透明度层面。
   - 来源: [darioamodei.com](https://darioamodei.com/post/we-must-pace-the-frontier) | [@sama](https://x.com/sama/status/2098811563415150910) | [@AnthropicAI](https://x.com/AnthropicAI/status/2098774062549848266)

**Artificial Analysis 首次将多模型编码 Agent Devin Fusion 纳入编码 Agent 指数**
- Artificial Analysis 在 Devin Fusion 当日发布版本上完成独立基准测试，这是其 Coding Agent Index **首次纳入多模型编码 Agent 产品**。测试结果显示，Devin Fusion 由 Cognition 配置的 frontier 主导模型配合 cost-efficient sidekick，在性能上有效保留 Claude Fable 5.1 与 GPT-6 Astra 表现并降低成本。
  > 💡 Devin Fusion 把 frontier 主模型与轻量副模型组合成同一 Agent，是把推理成本曲线压低的工程化路径；进入第三方编码 Agent 指数意味着多模型协作 Agent 开始被纳入与单体模型可比较的评测框架。
   - 来源: [@artificialanlys](https://x.com/ArtificialAnlys/status/2098504936984293447)

**Cognition 在 Devin CLI 中推出 Fusion，可在规划与执行阶段分别选用不同模型**
- Cognition 宣布在 Devin CLI 中引入 Fusion，面向其 Fable 与 Astra 模型。Fusion 被称为面向这两个模型的高效前沿 harness，在编码基准上比此前**便宜 39%**；用户可以为规划阶段选择偏好的模型，为执行阶段选择更具成本效益的模型。
  > 💡 把规划与执行解耦并允许在两端各选不同模型，是在模型能力快速分化的当下平衡质量与成本的现实选择；Fusion 类机制把这种选择权直接交到用户手里，也意味着模型 API 不再只按单一端到端能力定价。
   - 来源: [@cognition](https://x.com/cognition/status/2098445562404024343)

---
*更新时间: 2026-09-13 11:58*