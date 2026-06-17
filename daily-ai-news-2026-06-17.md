## 06月17日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：Z.ai GLM-5.2，1M上下文+开源权重，长程编程能力逼近Claude Opus 4.8; NVIDIA Nemotron 3 Ultra，550B MoE混合Mamba-Transformer架构，推理吞吐量达SOTA的6倍;阿里Qwen发布Qwen-Robot Suite机器人套件，含导航/操作/世界模型三款模型
- 产业动态：AI会议记录设备商Plaud软件ARR突破1亿美元，累计出货超200万台; Google发布Android 17与Wear OS 7，多任务功能升级并扩展Gemini能力; OpenAI提出部署模拟方法，在模型发布前预测其实际行为; Google开源OKF规范，为AI Agent知识库提供通用Markdown格式标准
- 算力追踪：Coherent扩建德州工厂，扩大AI数据中心光通信器件产能
- 初创&融资：DeepSeek完成超70亿元融资，采用非常规交易结构; SpaceX以600亿美元股票收购Cursor，创AI并购纪录; 马来西亚Respond.io完成6250万美元B轮融资; Probably获900万美元种子轮构建高可靠AI
- 研究关注：Stop When Further Reasoning Won't Help：基于注意力分布的推理模型自适应早停; Next-ToBE：用概率化token-bag替代one-hot目标，激活LLM前瞻推理能力（ICLR 2026）; RHO：自监督Agent Harness优化，无需标注数据即可持续改进Agent能力; Rethinking the Role of Efficient Attention in Hybrid Architectures：混合架构中高效注意力的系统性分析; Bayesian-Agent：将Agent技能视为假设，用贝叶斯后验驱动技能演化; Fill the GAP：诊断视觉latent reasoning的特征空间不匹配问题并提出对齐方案
- X讨论：Artificial Analysis发布Intelligence Index v4.1，转向agentic评测; SemiAnalysis深度分析RL训练系统效率瓶颈; Anthropic分析40万条Claude Code对话，领域专业知识比编程技能更决定AI工具效果; Agility Robotics分享人形机器人数据飞轮方法论，真实部署数据为核心壁垒

---

## 📖 详细参考

### 模型前沿
**Z.ai GLM-5.2：1M上下文+MIT开源权重，长程编程能力逼近Claude Opus 4.8**
- Z.ai 旗舰模型 GLM-5.2，首次支持稳定的**100万 token 上下文**，采用 MIT 开源许可证。在 Terminal-Bench 2.1 上得分**81.0**（对比 Opus 4.8: 85.0、GPT-5.5: 84.0），SWE-bench Pro 得分**62.1**（超过 GPT-5.5 的 58.6）。在长程编程 benchmark FrontierSWE 上以**74.4**仅落后 Opus 4.8 1%，在 PostTrainBench 上排名第二（仅次于 Opus 4.8），是所有长程 benchmark 中排名最高的开源模型。架构方面提出 IndexShare 技术，每4层稀疏注意力共享一个索引器，在1M上下文下将 per-token FLOPs 降低**2.9倍**。提供 Max 和 High 两档推理强度可选，API 定价与 GLM-5.1 持平。
  > 💡 GLM-5.2 在编程能力上已进入第一梯队，与 Claude Opus 4.8 差距缩小至1-3个百分点，同时以 MIT 许可证完全开源——这对开源社区和自部署企业是重大利好。1M上下文的"工程可用性"（而非仅支持更多token）是其核心差异化。
   - 来源: [Z.ai Blog](https://z.ai/blog/glm-5.2) | [X](https://x.com/Zai_org/status/2066938937344495629)

**NVIDIA Nemotron 3 Ultra：550B MoE混合Mamba-Transformer，推理吞吐量达SOTA的6倍**
- NVIDIA Nemotron 3 Ultra，**5500亿**总参数、**550亿**活跃参数的 MoE Hybrid Mamba-Attention 模型，在**20万亿** token 上预训练，上下文扩展至**100万** token。关键技术包括 LatentMoE、Multi Token Prediction (MTP)、NVFP4 预训练、多环境 RLVR 和 Multi-teacher On-Policy Distillation (MOPD)。推理吞吐量达到同等精度 SOTA 公开模型的**约6倍**，适合长时间自主 agentic 任务。NVIDIA 开源了 base/post-trained/量化三版权重及训练数据和 recipe。
  > 💡 Nemotron 3 Ultra 的核心卖点是"同等精度下6倍吞吐"——Hybrid Mamba 架构 + NVFP4 预训练的组合在推理效率上形成了显著优势。开源权重+训练数据+recipe 的完整发布策略对自部署企业有直接吸引力。
   - 来源: [arXiv](https://arxiv.org/abs/2606.15007)

**阿里Qwen发布Qwen-Robot Suite机器人套件，含导航/操作/世界模型三款模型**
- 阿里Qwen团队推出Qwen-Robot Suite，包含三款模型：导航模型Qwen-RobotNav（统一五大导航任务至同一框架）、操作模型Qwen-RobotManip（基于**超38,100小时**开源语料预训练，在真机测评中包揽前两名），以及世界模型Qwen-RobotWorld（可推演模拟机器人后续动作状态）。将自然语言作为机器人控制接口是核心设计理念。
  > 💡 Qwen将多模态大模型能力向具身智能延伸，与近期港中文MiniMax稀疏注意力、Anthropic编程经济性研究形成互补，反映出大模型厂商正从纯语言/视觉向机器人基础模型全面拓展。
   - 来源: [Qwen Blog](https://qwen.ai/blog?id=qwen-robotsuite) | [@alibaba_qwen](https://x.com/Alibaba_Qwen/status/2066870201380118843#m)

### 产业动态
**AI会议记录设备商Plaud软件ARR突破1亿美元，累计出货超200万台**
- Plaud宣布其软件业务ARR已突破1亿美元，AI录音笔/会议记录设备累计出货超过200万台。Plaud定位AI会议记录赛道，通过硬件+订阅软件模式实现规模化。
  > 💡 Plaud在拥挤赛道中以软硬结合方式跑出1亿美元ARR，验证了AI硬件订阅化的可行路径，但2百万台的硬件基数能否持续转化软件留存是关键考验。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/16/plaud-says-its-software-business-topped-100m-in-arr-after-shipping-over-2m-ai-notetakers/)

**Google发布Android 17与Wear OS 7，多任务功能升级并扩展Gemini能力**
- Google发布Android 17和Wear OS 7，新增多任务功能、家长控制、安全工具及智能手表升级。系统层面进一步扩展Gemini能力，新增Lyria 3音乐生成模型、Gemini Omni多模态模型等AI功能，将AI助手整合到更多原生应用与设备形态中。
  > 💡 Gemian功能扩展与系统深度整合是Google应对Apple Intelligence竞争的关键策略，端侧AI能力将成为Android生态差异化的下一战场。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/16/android-17-launches-with-new-multitasking-tools-as-google-expands-gemini-features/)

**OpenAI提出部署模拟方法，在模型发布前预测其实际行为**
- OpenAI发布Deployment Simulation方法，通过真实对话数据模拟部署环境，在模型发布前预测AI模型行为。该方法在SWE-Bench Pro上取得**57%**成绩，Terminal-Bench 2.0得分**77.3%**（较上代提升13个百分点），完成同等任务所需token不到上代的一半，单token推理速度提升超过**25%**。
  > 💡 模型评测正从静态benchmark转向部署场景模拟，这一范式转变对提升模型安全性和对齐评估的可信度具有实质价值，可能成为行业新标准。
   - 来源: [OpenAI News](https://openai.com/index/deployment-simulation)

**Google开源OKF规范：为AI Agent知识库提供通用Markdown格式标准**
- Google 发布 **Open Knowledge Format (OKF) v0.1**，解决 AI Agent 落地的核心痛点：agent 需要的上下文知识（表结构定义、指标含义、操作手册、API 文档等）散落在 wiki、元数据目录、代码注释和工程师脑子里，每个搭 agent 的团队都在从头解决同一个"上下文拼装"问题。Karpathy 近期提出的"LLM Wiki"模式（让 agent 自己读写 Markdown 知识库）已在实践中反复出现——CLAUDE.md、AGENTS.md、Obsidian 知识库接 agent 等——但每家做法都是定制的，知识被锁在各自的团队里出不来。OKF 定义了最小互操作契约：一个 bundle 就是一目录 Markdown 文件，仅需一个 `type` 字段，文件间用普通链接形成关系图，人能读、agent 能解析、不需要任何 SDK 或云平台绑定。Google 同步发布了 BigQuery 自动生成 OKF 文档的 agent、HTML 可视化工具和三个样例 bundle，Knowledge Catalog 已支持 OKF 摄入。
  > 💡 OKF 试图解决 AI Agent 落地的核心痛点——知识碎片化。每个搭 agent 的团队都在重复解决上下文拼装问题，OKF 如果成为事实标准，将显著降低 agent 知识管理的重复成本。
   - 来源: [Google Cloud Blog](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/) | [GitHub](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)

### 算力追踪
**Coherent扩建德州工厂，扩大AI数据中心光通信器件产能**
- 光通信器件厂商Coherent在德州Sherman扩建制造工厂，重点扩大面向AI数据中心的光器件产能。扩建后工厂将制造每通道**400G/3.2T**收发器及面向**12.8T**的新兴架构，发展共封装光学（CPO）和开放光网络平台。Coherent是NVIDIA光通信供应链重要供应商。
  > 💡 光通信是AI数据中心Scale-out瓶颈环节，Coherent扩产将进一步绑定与NVIDIA等AI基础设施客户的供应关系，折射出光器件供需仍偏紧的格局。
   - 来源: [NVIDIA Blog](https://blogs.nvidia.com/blog/coherent-texas-ai-optical/)

### 初创&融资
**DeepSeek完成超70亿元融资，采用非常规交易结构**
- 中国AI实验室DeepSeek完成首轮外部融资，规模超过**50亿元人民币（约74亿美元）**，估值超过**500亿美元**。梁文峰个人出资**200亿元**（最大单笔），腾讯投资**100亿元**，宁德时代（CATL）投资**50亿元**，京东、网易和 IDG 资本各出资**30亿元**。国家人工智能产业投资基金直接投资 DeepSeek **10亿元**，是唯一享有投票权和不受五年锁定期限制的投资方。所有其他外部投资者的资金投入梁文峰管理的有限合伙企业，无投票权但可获财务信息优先权和未来融资优先投资权。梁文峰要求核查所有 LP 身份以排除不明投资者，五年锁定期旨在筛选掉追求快速退出的资本。
  > 💡 DeepSeek以非常规结构完成创纪录融资，反映出在中美AI竞争与算力受限背景下，资本正重新评估中国头部AI实验室的稀缺价值，融资结构设计可能涉及国资引导与算力资源绑定。
   - 来源: [The Information](https://www.theinformation.com/briefings/deepseek-closes-record-7-billion-plus-funding-unusual-deal-structure)

**SpaceX以600亿美元股票收购Cursor，创AI领域并购纪录**
- SpaceX 在完成史上最大 IPO（发行价对应估值约**1.77万亿美元**）后仅数天，宣布以**600亿美元股票**收购 AI 编程创业公司 Cursor，预计今年Q3完成交割。此前4月 SpaceX 已约定：要么以600亿美元收购 Cursor，要么支付**100亿美元分手费**。Cursor 在此之前正筹备由 a16z、Thrive、Nvidia 领投的20亿美元融资轮，估值约500亿美元。SpaceX 向 IPO 投资者承诺的AI市场空间达**26万亿美元**，其中企业应用占22.7万亿。自上周五 IPO 以来，SpaceX 股价从135美元涨至盘前200美元以上，市值增加近1万亿美元。
  > 💡 这笔交易刷新了AI行业并购纪录，也标志着 SpaceX 从航天公司向AI全栈巨头的转型加速。Cursor 选择被收购而非独立融资，暗示AI编程赛道的独立生存窗口正在收窄——资金消耗速度超过了独立运营的盈亏平衡点。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/16/spacex-to-acquire-cursor-for-60b-in-stock-days-after-blockbuster-ipo/) | [The Information](https://www.theinformation.com/briefings/spacex-finalizes-60-billion-deal-acquire-cursor)

**马来西亚AI消息平台Respond.io完成6250万美元B轮融资，ARR达3500万美元**
- 总部位于吉隆坡的 AI 客户对话管理平台 Respond.io 完成**6250万美元B轮融资**，由 Camber Partners 领投。公司当前 ARR 为**3500万美元**，同比增长**169%**，利润率30%。平台覆盖 WhatsApp、Instagram、TikTok、微信等多渠道，季度处理消息量达**20亿条**。公司采用按对话量而非按席位收费的模式，创始人 Gerardo Salandra 表示"AI越普及我们增长越快"。新资金将用于在北美和欧洲进行收购扩张。
  > 💡 Respond.io 以按对话量定价的模式绕过了AI对传统SaaS按席位订阅模式的冲击，同时积累的消息数据形成飞轮效应。东南亚AI应用层的全球化扩张路径值得关注。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/15/malaysias-respond-io-raises-62-5m-eyes-acquisitions-in-north-america-and-europe/)

**Probably获900万美元种子轮，用确定性验证器框架将LLM推向99.99%准确率**
- 创始人 Peter Elias 创办的 AI 可靠性初创公司 Probably 完成**900万美元种子轮融资**，由 a16z 领投。公司核心方法是用确定性验证器（deterministic validator）检查 LLM 输出，任何与数据集不匹配的结果会被退回重做，形成所谓的"数据科学机甲"。该方法使 Probably 能运行在比前沿模型**弱四个等级**的小模型上，可在本地桌面电脑运行，大幅降低 token 成本。首款产品为数据科学工具，每条结果附带引用和审计轨迹，未来计划扩展至会计、医疗等精度敏感场景。
  > 💡 Probably 代表了反主流的AI工程思路：与其追求更大的模型，不如用验证框架让小模型达到确定性系统的精度。这种 harness engineering 模式为企业级AI部署提供了降低 token 成本的另一条路径。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/16/probably-raises-9m-to-build-a-more-reliable-kind-of-ai/)

### 研究关注
**Stop When Further Reasoning Won't Help：基于注意力分布的推理模型自适应早停**
- 论文针对大型推理模型（LRM）的 overthinking 问题——冗余 token 输出导致准确率下降。作者从注意力分布角度分析推理过程，提出一种简单的免训练早停方法：当注意力分布表明继续推理不会带来增益时自动停止生成。该方法无需额外训练资源，也不依赖精心设计的 prompt 或不可靠的置信度信号。
  > 💡 overthinking 是当前推理模型（o1/R1 类）的普遍问题，基于注意力状态的早停提供了一种零成本、可即插即用的解决方案，对推理 API 的 token 成本优化有直接实用价值。
   - 来源: [arXiv](https://arxiv.org/abs/2606.15070)

**Next-ToBE：用概率化 token-bag 替代 one-hot 目标，激活 LLM 前瞻推理能力（ICLR 2026）**
- 论文（刘一贺等，华东师大+复旦）指出 next-token prediction 的 one-hot 目标会抑制 LLM 隐含的前瞻能力——模型本可通过当前 softmax 概率预捕获未来窗口内的 token。Next-ToBE 将 one-hot 目标替换为覆盖额外未来 token 的 soft target 分布，近期 token 保持最高权重，远期”look-ahead token”按时间与语义相关性动态加权，从而在训练中注入前瞻压力。该方法在推理性能上显著提升，且比 MTP 基线具有更高的内存和计算效率，在预训练场景下也能从零培养前瞻能力。
  > 💡 next-token 短视是 CoT、test-time scaling 路线的共性瓶颈。Next-ToBE 从训练目标层面修正比纯推理时 trick 更具结构性影响，且不增加推理开销。
   - 来源: [ICLR 2026](https://openreview.net/pdf?id=T8IJojfaOh) | [PaperWeekly](https://mp.weixin.qq.com/s?__biz=MzIwMTc4ODE0Mw==&mid=2247720971&idx=2&sn=dbc7ce93a7438c76efc3a48af0dfbb9d)

**RHO：自监督Agent Harness优化，无需标注数据即可持续改进Agent能力**
- 论文提出 Retrospective Harness Optimization (RHO)，一种无需 ground-truth 验证集的 agent harness 自优化方法。RHO 从历史 trajectory 中选取多样化挑战任务子集并行重解，通过 self-validation 和 self-consistency 分析 rollout，生成候选 harness 更新，再由 agent 自身的 pairwise self-preference 选择最有效方案。在 SWE-Bench Pro 等三个领域验证，单轮优化即可提升 pass rate。
  > 💡 RHO 解决了 agent 部署后持续优化的核心痛点——没有标注数据时如何自我改进。self-preference 机制避免了对外部评估的依赖，具有很强的工程实用性。
   - 来源: [arXiv](https://arxiv.org/abs/2606.05922)

**Rethinking the Role of Efficient Attention in Hybrid Architectures：混合架构中高效注意力的系统性分析**
- 论文对混合架构（full attention + sliding-window attention / recurrent mixer）进行系统性分析，涵盖 scaling behavior、mechanism analysis 和 architecture design 三个维度。研究发现高效注意力设计主要影响长上下文能力的涌现速度，而不同设计在充分训练后趋于收敛。该分析为混合架构的模块选择和配置提供了经验指导。
  > 💡 混合架构已成为前沿模型的标配（如 GLM-5.2 的 IndexShare），但对各模块能力的精确拆解仍然稀缺。本文的 scaling 视角为架构设计提供了量化依据。
   - 来源: [arXiv](https://arxiv.org/abs/2606.15378)

**Bayesian-Agent：将Agent技能视为假设，用贝叶斯后验驱动技能演化**
- 论文将可复用技能和 SOP 视为”冻结模型在特定 prompt/上下文/harness 下是否会成功”的假设，维护 feature-conditioned categorical posterior，并映射为可审查动作：patch、split、compress、retire、explore。结合 deepseek-v4-flash，增量修复将 SOP-Bench 从 80% 进一步提升。后验摘要可用于审计，模型 prompt 获得可执行 guardrail 和失败模式补丁。
  > 💡 将贝叶斯推断引入 agent 技能管理是一个新颖视角——技能不再是静态资产，而是可被概率更新和分叉/淘汰的”活假设”，为 agent harness 的自动化治理提供了理论框架。
   - 来源: [arXiv](https://arxiv.org/abs/2606.08348)

**Fill the GAP：诊断视觉latent reasoning的特征空间不匹配问题并提出对齐方案**
- 论文（Yanting Miao、Pascal Poupart 等）指出视觉 latent reasoning 不稳定的根源：基于 pre-norm 的多模态大模型将 decoder 隐藏状态作为 latent 输入复用，但这些状态的 norm 与模型训练时消费的 input embedding 差异显著，导致直接 latent 反馈不可靠。论文提出 GAP（Granular Alignment Paradigm），通过细粒度对齐策略弥合 norm 差距，使 decoder 输出在反馈为输入前先映射到模型可消费的特征空间。实验验证 GAP 在多个视觉推理 benchmark 上显著提升了稳定性，减少了 latent reasoning 方法在 pre-norm 架构上的增益波动。
  > 💡 特征空间层面的 norm 不匹配诊断是多模态 latent reasoning 领域的关键洞察——解释了为何”输出当输入”的 latent 范式效果不稳定，为后续改进提供了明确方向。
   - 来源: [arXiv](https://arxiv.org/abs/2605.12374) | [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651039317&idx=3&sn=ebe0a5f022e945b5e64e7c29e9b913da&chksm=8587851814ad6145fc438e1ec300f2becff94b7d1ff86fdd64a3b783d10b762946d0020e3e0d&scene=0&xtrack=1#rd)

### X讨论
**Artificial Analysis发布Intelligence Index v4.1，全面转向agentic工作负载评测**
- Artificial Analysis 发布 Intelligence Index v4.1，核心变化包括：升级 Terminal-Bench Hard 至 Terminal-Bench 2.1、τ²-Bench 升级至 τ³-Bench Banking、GDPval-AA 升级至 v2（Elo 基准重设为人类1000，轮换前沿模型评委，回合上限提至250），移除已饱和的 IFBench。新增每任务成本/时间/token数三项指标。排名方面：Claude Fable 5（60分）领跑但未开放，Claude Opus 4.8 max（**56分**）为最强可用模型，GPT-5.5 xhigh（55分）仅差1分。开源模型中 DeepSeek V4 Pro max 和 MiniMax M3 并列**44分**。每任务成本方面，Opus 4.8 为**$1.78/任务**，GPT-5.5 为 $0.99，DeepSeek V4 Pro 仅 **$0.04**——比闭源前沿模型便宜20-45倍。
  > 💡 v4.1标志着模型评测全面从静态知识问答转向agentic任务执行能力，而"每任务成本"指标的引入直接回答了企业最关心的问题：同等智能水平下，开源模型的成本优势已达数量级。
   - 来源: [X](https://x.com/ArtificialAnlys/status/2066700136018071841)

**SemiAnalysis深度分析RL训练系统效率：训练器与生成器吞吐量匹配是核心瓶颈**
- SemiAnalysis 发布深度技术文章，剖析 RL 训练系统效率的核心问题：生成器（推理）和训练器（梯度更新）的吞吐量匹配。文章将 RL 系统建模为队列——生成器生产样本，训练器消费样本。在 Qwen3-235B 和 GLM-5 上的实验均显示系统处于**generation-bound**状态：训练器30%-74%的时间在空等。主因是模型输出长度在训练中急剧增长（GLM-5实验中每轮响应长度和工具调用次数增至**3倍**），导致推理时间主导端到端延迟。文章还分析了 sandbox 扩展性瓶颈（960并发时出现初始化失败）和 partial rollout 带来的环境状态级 policy staleness 问题，并对 Thinking Machines 的 Tinker 平台进行了 TCO 对比。
  > 💡 这篇文章是理解 RL post-training 基础设施的最佳系统性参考——揭示了一个被低估的事实：RL 训练效率的瓶颈不在 GPU 算力本身，而在于推理引擎效率、sandbox 扩展性和算法-系统的协同设计。
   - 来源: [SemiAnalysis](https://newsletter.semianalysis.com/p/rl-systems-mind-the-gap-matching) | [X](https://x.com/SemiAnalysis_/status/2066941079920791760)

**Anthropic分析40万条Claude Code对话，揭示编程任务经济价值增长**
- Anthropic 对**约40万条** Claude Code 会话（来自约23.5万用户，2025年10月至2026年4月）进行隐私保护分析，发现用户做出约**70%**的规划决策，Claude 做出约**80%**的执行决策——"人定做什么、AI定怎么做"的分工明确。调试类会话占比从33%降至**19%**，任务估计经济价值平均上升**27%**。领域专家的每次指令可触发**2倍**于新手的活动量和**5倍**的输出。各职业的成功率与软件工程师差距在7个百分点以内，领域专业知识比编程技能更能决定使用效果。
  > 💡 Anthropic通过大规模真实使用数据量化编程AI的经济价值，发现"领域专业知识"而非"编程技能"是决定AI编程工具效果的关键变量——这对劳动力市场的影响判断具有重要参考价值。
   - 来源: [Anthropic Research](https://www.anthropic.com/research/claude-code-expertise) | [@anthropicai](https://x.com/AnthropicAI/status/2066969534322688427#m)

**Agility Robotics分享人形机器人数据飞轮方法论，真实部署数据为核心壁垒**
- Agility Robotics（Digit 人形机器人制造商）发文阐述其 AI 训练数据获取策略：VR 遥操作示教（LfD）、仿真训练（基于 NVIDIA Isaac Lab 的强化学习）和**真实客户设施部署数据**三种方式。其中真实部署数据是同行最难复制的——Digit 在客户现场持续作业产生的数据回流训练，形成数据飞轮。技术栈分为三层：认知层（LLM/VLA 模型）、技能层（LfD）、控制层（RL/仿真），分别对应不同时间尺度的决策。公司目标是实现通过云端更新为人形机器人推送新技能。
  > 💡 与 LLM 训练依赖互联网公开数据不同，机器人运动数据几乎不存在公开来源——谁先在真实场景中跑起来并回收数据，谁就建立不可逆的壁垒。Agility 的方法论揭示了具身智能竞争中"部署即研发"的底层逻辑。
   - 来源: [Agility Robotics Blog](https://www.agilityrobotics.com/content/agility-and-ai) | [X](https://x.com/agilityrobotics/status/2066990246869475760)


---
*更新时间: 2026-06-17 06:51*