## 09月29日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 24 条

---

## 要点汇总

- 模型前沿：Anthropic 发布 Sonnet 5.5：Terminal-Bench 从 10.3% 跃至 70.6%，单任务成本最多降 30%
- 产业动态：AMD 宣布以约 82 亿美元全股票方式收购 World Labs; 英伟达发布 Open Agent Safety Platform：把安全控制从 Agent 内部挪到外部; Meta 新设企业 AI 部门 Meta Enterprise Platform，由 MongoDB CEO 掌舵; Shopify 向浏览器 AI 智能体开放结账：买家授权后可直接完成下单; Cognition 推出 Devin Mobile beta：Devin 智能体进入移动端
- 算力追踪：SpaceX Terafab 项目全面提速：3 月启动，4 月下单设备，现场已浇筑混凝土; The Information 调查：15 万亿美元 AI 建设潮正在重写数据中心融资规则
- 初创&融资：消费级 AI 智能体 Instinct 融资 10 亿美元 C 轮，估值一个月涨至 100 亿美元; 推理服务商 Modal Labs 据传以 157.5 亿美元估值接近完成 7.5 亿美元融资; 物理 AI 芯片公司 SiMa.ai 完成 1.5 亿美元 C 轮，估值达 14.5 亿美元; 海事情报初创 Quartermaster 完成 1.4 亿美元 B 轮，SmartMast 覆盖 25 国 650 艘船; Modulate 融资 2500 万美元：百余个小模型做语音深伪检测与意图分析; 保险科技 Outmarket 完成 3450 万美元 B 轮，距上轮融资仅四个月
- 研究关注：论文提出 RayOrch：在分布式数据流中保留父子血缘的多粒度执行框架; 论文提出 FuseReg：通过层融合正则化缩小表征自编码器的重建与生成差距; 论文提出 DCE+SRCL：递归自蒸馏让 8B 模型数学推理提升 35.6 个百分点; VBVR-Pro 发布：300 个可验证奖励任务把原生视觉推理做成闭环训练场; Sakana AI 提出 SAIL：测试时搜索把 VLM 机器人轨迹成功率从 25% 提至 73%
- X讨论：Bespoke Labs 重发 AutoResearchExam：24 小时开放式研究基准，Fable 5.1 以 0.602 居首; Jason Weston 团队提出 RL-XAR：用专家对齐评分规则训出超越前沿模型的 27B 写手; Vinod Khosla 警告：到 2030 年多数机器人初创公司估值将下挫

---

## 📖 详细参考

### 模型前沿
**Anthropic 发布 Sonnet 5.5：Terminal-Bench 从 10.3% 跃至 70.6%，单任务成本最多降 30%**
- Anthropic 正式推出 Claude 5.5 家族第二款模型 Sonnet 5.5，定价与 Sonnet 5 持平（每百万 token 输入 2 美元、输出 10 美元），但生成输出**快 30% 以上**、完成同样任务的成本最多**低 30%**。智能体编码基准 Terminal-Bench 4.0 上得分 **70.6%**（Sonnet 5 为 10.3%，Opus 5.5 为 66.4%），GDPval-AA 以 1844 分几乎追平 Opus 5.5 的 1846；它也是首个仅凭截图通关 Pokémon Red 的 Sonnet 模型。因网络安全能力与 Opus 5 相当，Sonnet 5.5 是首款配备同级网络防护、并首个搭载防蒸馏安全分类器的 Sonnet 模型。Haiku 5.5 将在未来数周发布。
  > 💡 在中端价位上同时压低 token 消耗与提升速度，意味着 Anthropic 把智能体编排成本作为对竞争对手的主战场；率先把网络防护与防蒸馏分类器下放到 Sonnet 层级，也凸显出中等模型在企业部署中已具备高风险能力，安全门槛随之向上对齐。
   - 来源: [Anthropic](https://www.anthropic.com/claude-sonnet-5-5) | [@claudeai](https://x.com/claudeai/status/2104633115620823187) | [TechCrunch](https://techcrunch.com/2026/09/28/anthropic-releases-sonnet-5-5-which-it-calls-a-significantly-cheaper-faster-work-partner)

### 产业动态
**AMD 宣布以约 82 亿美元全股票方式收购 World Labs**
- AMD 已同意以约 **82 亿美元**的全股票交易收购成立两年的空间智能公司 World Labs，预计 2026 年底前完成。双方去年已开始在 AMD GPU 上的模型训练与推理优化深度合作。World Labs 首席执行官、AI 研究人员 Fei-Fei Li 将加入 AMD 担任执行副总裁兼首席科学家，直接与 CEO Lisa Su 共事；联合创始人 Justin Johnson 与 Ben Mildenhall 继续带领团队在 AMD 内组建前沿研究组织，共同构建横跨硬件、软件、平台与开放模型的端到端开放 AI 生态。
  > 💡 AMD 通过一次大体量人才收购把 Fei-Fei Li 与 World Labs 的空间智能模型纳入体系，把收购估值锚定在 3D 世界模型这一前沿方向，反映出芯片公司正把模型与人才储备当作新的战略资产；从技术合作走向整体收购，也说明空间智能模型的落地已离不开与算力硬件的深度耦合。
   - 来源: [The Information](https://www.theinformation.com/briefings/amd-buy-fei-fei-lis-world-labs-8-2-billion) | [World Labs](https://www.worldlabs.ai/blog/amd-announcement) | [@theworldlabs](https://x.com/theworldlabs/status/2104665621120311465)

**英伟达发布 Open Agent Safety Platform：把安全控制从 Agent 内部挪到外部**
- 英伟达发布 Open Agent Safety Platform，由两部分组成：开源安全运行时 OpenShell 在 NVIDIA Vera CPU 上追踪 agent 的全部动作并强制执行策略，可扩展支持 Arm 与 Intel 平台；Sentry 参考设计则在 BlueField-4 DPU 上提供带外看门狗，对试图越界的 agent 在**毫秒级**内隔离。Anthropic 已将 Claude Managed Agents 与 OpenShell/BlueField 集成，**100 多家组织**参与该平台。英伟达并未主张放慢开发节奏或新增监管，而是把部分安全控制从 Agent 内部抽离，形成独立、持续运行的看门机制。
  > 💡 英伟达选择把安全层做成独立于 Agent 的运行时底座，本质上是把安全工具变成基础设施的一部分，与 GPU/CPU/DPU 销售形成协同；100+ 组织的参与阵容说明「agent 安全」正在从模型厂商的自律问题转化为全栈基础设施标准问题。
   - 来源: [NVIDIA Newsroom](https://nvidianews.nvidia.com/news/open-agent-safety-platform) | [TechCrunch](https://techcrunch.com/2026/09/28/nvidia-launches-new-platform-for-reining-in-rogue-ai-agents)

**Meta 新设企业 AI 部门 Meta Enterprise Platform，由 MongoDB CEO 掌舵**
- Meta 正在成立一个新部门，面向企业销售其 AI 工具，并任命 MongoDB 首席执行官 Chirantan Desai 出任该部门 chief enterprise platform officer。Meta 首席执行官 Mark Zuckerberg 周一在 X 发文宣布，新部门名为 Meta Enterprise Platform，将聚焦把 Muse、Meta Business Agent 与 Muse Code 等产品带给企业客户。
  > 💡 Meta 把企业 AI 业务独立成事业部，并引入外部上市公司 CEO 掌舵，意味着消费级 AI 增长之外，企业付费渠道正成为新的优先级与组织重心。
   - 来源: [The Information](https://www.theinformation.com/briefings/meta-taps-mongodb-ceo-lead-new-enterprise-ai-division)

**Shopify 向浏览器 AI 智能体开放结账：买家授权后可直接完成下单**
- Shopify 宣布把 WebMCP 支持扩展到结账环节（含 Shop Pay），浏览器端 AI 智能体可以在买家授权下读取结账页、修改地址或配送方式并提交订单，无需依赖截图或抓取网页。新提供 get_checkout、update_checkout、complete_checkout 三个工具，已向所有符合条件的商家开放。Shopify 此前已支持店面与购物车的 WebMCP，两者均基于其通用商务协议 UCP；Muse 与 Instinct 等头部智能体已与 Shopify 达成 agentic commerce 直接合作，其中 Instinct 的合作于同日宣布。这与 Amazon 等平台屏蔽 AI 智能体代购的做法形成对比。
  > 💡 Shopify 把「结构化 API + 买家授权」作为智能体购物的接口契约，等于抢占 agent 商务链路的标准层；当最大的零售平台选择屏蔽、最大的建站平台选择开放，电商 agent 的入口之争将取决于谁先把授权与信任机制跑通。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/28/shopify-opens-checkout-to-browser-based-ai-agents/)

**Cognition 推出 Devin Mobile beta：Devin 智能体进入移动端**
- Cognition 宣布旗下 AI 软件工程师智能体 Devin 的移动版本 Devin Mobile 进入 beta 测试，用户可通过链接加入等候名单。
  > 💡 Devin 从云端开发环境走向移动端，说明编码智能体正从工程师的工作时段延伸到全天候任务委托；移动入口也可能成为 Devin 从开发者工具走向更广泛用户群的分发渠道。
   - 来源: [@cognition](https://x.com/cognition/status/2104597797672784234)

### 算力追踪
**SpaceX Terafab 项目全面提速：3 月启动，4 月下单设备，现场已浇筑混凝土**
- SpaceX 正在全速推进 Terafab 项目。该项目于 3 月启动，4 月完成设备订货，现场已进入混凝土浇筑阶段。SemiAnalysis 在社交媒体上以系列帖文披露了这一进度，并附上现场相关链接。
  > 💡 Terafab 从立项到土建施工仅用约半年时间，节奏明显快于传统晶圆厂；SpaceX 自建算力基础设施的决心与速度，反映出头部玩家希望把关键产能锁定在自有体系内。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2104647659273228375)

**The Information 调查：15 万亿美元 AI 建设潮正在重写数据中心融资规则**
- 报道称，AI 建设投入的资金与资源规模史无前例，正在打破传统数据中心的融资与建设模式，并引发投资者对风险评估方式的新疑问。文章引用了对 Volta 联合创始人兼 CEO Ricard Boada 与 Crusoe 首席数据中心官 Chris Dolan 的访谈，探讨在当前建设速度下融资与开发方式如何变化。报道涉及的相关方还包括亚马逊、微软、谷歌、英伟达、摩根士丹利、穆迪以及 Blackstone 等机构。
  > 💡 把数据中心建设上升到万亿美元级别后，融资结构本身正在脱离传统 REITs 与项目贷款范式，转向更靠近科技股权与可转债的混合工具；这意味着 AI 资本开支的风险定价开始由资本市场而非信贷市场主导。
   - 来源: [The Information](https://www.theinformation.com/articles/ais-15-trillion-buildout-rewriting-rules-data-center-financing)

### 初创&融资
**推理服务商 Modal Labs 据传以 157.5 亿美元估值接近完成 7.5 亿美元融资**
- 据知情人士透露，AI 推理基础设施提供商 Modal Labs 正在接近完成一轮 7.5 亿美元的融资，由 Accel 领投，投后估值（含本轮投资）为 157.5 亿美元。该轮融资的金额此前未被披露，Axios 与 Bloomberg 已报道了交易的其他细节。Modal Labs 拒绝对此置评。本轮融资距离其四个月前宣布的 3.55 亿美元融资、对应的 46.5 亿美元估值仅过去四个月，估值预计将超过三倍。
  > 💡 推理赛道单笔估值与估值倍数同步飙升，反映出开源模型落地对推理算力的强需求；尽管收入增长迅速，但推理厂商受制于算力采购与租赁成本，利润率仍然较薄。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/28/source-inference-provider-modal-labs-closing-in-on-750m-round-at-15-75b-valuation)

**消费级 AI 智能体 Instinct 融资 10 亿美元 C 轮，估值一个月涨至 100 亿美元**
- 消费级 AI 智能体 Instinct 完成 **10 亿美元 C 轮融资**，估值 **100 亿美元**，投资方包括 Sequoia Capital、Benchmark Capital 与 Coatue；这距其上一轮 25 亿美元估值的融资仅过去一个月。该产品 2026 年 8 月以邀请制上线，可代用户订机票、订餐厅、购物、付账单、取消订阅，执行任务时使用自己的电话号码和电脑，近期上线了代打电话的 concierge 功能与多智能体协调的 trusted person network。Instinct 目前面临 Meta Muse 的直接竞争——后者已登顶美国应用商店下载榜；其初版隐私政策曾因数据收集范围过大引发争议，随后修改，公司尚未披露用户规模数据。
  > 💡 一个月内估值翻两番，是「消费级 agent 是下一个超级入口」这一押注的极端定价；Instinct 没有移动 App、靠 SMS 交互，入口层正面撞上 Meta 的社交分发，此轮融资更像是在与 Muse 的入口战争中提前锁定弹药。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/28/viral-ai-agent-instinct-raises-1b-series-c-at-a-10b-valuation/)

**物理 AI 芯片公司 SiMa.ai 完成 1.5 亿美元 C 轮，估值达 14.5 亿美元**
- 边缘 AI 芯片公司 SiMa.ai 完成 **1.5 亿美元 C 轮融资**，估值 **14.5 亿美元**，由 Fidelity 与 Amplify 联合领投，Dell Technologies Capital、StepStone Group 等参投。公司由前 Groq COO Krishna Rangasayee 于 2018 年创立，开发让机器人、无人机、相机等设备直接在端侧运行 AI 的能效芯片，主打低延迟与低于 NVIDIA GPU 的价格，瞄准包括人形机器人在内的物理 AI 设备市场。本轮后总融资额超过 5 亿美元；上一轮为 2025 年 7 月的 8500 万美元 B 轮，彼时估值 9.6 亿美元。
  > 💡 估值一年涨五成、涨幅并不夸张，反映端侧物理 AI 芯片仍处于「讲量产故事」的阶段；人形机器人与具身智能放量在即，边缘推理芯片能否绕开 CUDA 生态建立自己的软件护城河，才是估值兑现的关键。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/28/physical-ai-chip-developer-sima-ai-hits-1-45b-valuation/)

**海事情报初创 Quartermaster 完成 1.4 亿美元 B 轮，SmartMast 覆盖 25 国 650 艘船**
- 海事情报初创 Quartermaster 完成 **1.4 亿美元 B 轮融资**，由 Insight Partners 主动发起领投，国防领域投资机构 Overmatch Ventures 与老股东 First Round Capital 参投；其中约 1 亿美元为股权，另 4000 万美元来自投行 Stifel 的债务工具。公司 5 月刚完成 4300 万美元 A 轮。其硬件产品 SmartMast 把相机与无线电集成到船桅装置上，实时回传远超 AIS 位置信标的海事数据；目前 **25 个国家超过 650 艘船**已安装，累计出货超 800 台。CEO Neil Sobin 称，伊朗战争及随之而来的航运混乱显著提升了政府与保险客户的紧迫性。
  > 💡 「地球上最大盲区」的海洋数据网络叠加地缘冲突推动的国防需求，让这家公司四个月内完成两级融资；自有硬件加数据独有权的组合，是 AI 应用层少见的「基础设施型」标的，其数据飞轮一旦转起来将很难被纯软件对手复制。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/28/maritime-intelligence-startup-quartermaster-raises-another-140m/)

**Modulate 融资 2500 万美元：百余个小模型做语音深伪检测与意图分析**
- 波士顿语音智能公司 Modulate 完成 **2500 万美元**融资，Future Ventures 领投，Hyperplane 与 Lakestar 参投。公司运行 **100 多个小模型**，分为两类：信号提取模型识别声学情绪、语气、语言与是否合成语音；分析检测模型判断意图、违规与诈骗行为，面向受监管行业的语音智能体提供深伪检测、通话质量评估与合规监控。联合创始人 Mike Pappas 与 Carter Huffman 为 MIT 物理系同学，2017 年创立公司，早期做游戏语音变声；据 PitchBook，本轮前公司已融资 4100 万美元、估值 1.7 亿美元。
  > 💡 不追大模型而用小模型矩阵组合，在避开算力成本的同时把「听懂对话」做成可插拔的语音安全层；随着语音智能体与深伪诈骗同步爆发，语音侧的检测与合规正在成为独立赛道。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/28/modulate-raises-25m-for-its-voice-models-and-analysis-suite/)

**保险科技 Outmarket 完成 3450 万美元 B 轮，距上轮融资仅四个月**
- 前 Ethos 产品负责人 Vishal Sankhla 创立的 Outmarket 完成 **3450 万美元 B 轮融资**，SignalFire 领投，据知情人士估值 **3.35 亿美元**，距其 1700 万美元 A 轮仅四个月。公司用 AI 自动化保险经纪机构的文书流程，聚焦商业保险——市面上有超过 **250 种险种**，每种险种的申请表单与所需文档各不相同。新产品上线 14 个月已签约超过 **300 家保险代理机构**，其中包括全美前 100 家经纪机构中的 25%。
  > 💡 商业保险经纪的文书自动化是典型的「AI 替代重复劳动」场景，四个月连续两轮且估值接近翻倍，说明垂直行业的 AI 渗透正从演示走向按机构数付费的稳定收入；美国 95% 的保险仍经人手代理，这一存量渠道给了这类公司足够长的跑道。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/28/insuretech-outmarket-raises-34-5m-just-months-after-prior-round/)

### 研究关注
**RayOrch：在分布式数据流中保留父子血缘的多粒度执行框架**
- 论文针对基础模型训练数据管线中父项展开为变长子序列、需要跨父节点批量又必须保留顺序与血缘的难题，提出 RayOrch 编程模型与分布式执行引擎。程序可声明有序、可变基数的展开以及对应的归 gather 操作，由编译器校验配对，并在运行时记录子项归属、父节点、不可变序号与终止状态。在 NVIDIA H20 GPU 上，RayOrch 将 MinerU 从 4 卡扩展到 64 卡获得 **15.14 倍**加速，将视频管线从 8 卡扩展到 64 卡获得 **7.82 倍**加速；在 MinerU 上端到端时间较 Ray Data 缩短 **13.1%**、较 Daft 缩短 **29.0%**，在 Docling 上较 Ray Data 缩短 **16.0%**。代码已在 GitHub 开源。
  > 💡 在 GPU 集群扩展到 64 卡时仍能保持十倍以上的线性增益，说明数据准备环节正在重演训练侧的扩展曲线；血缘与失败隔离被前置到执行引擎层，意味着高质量数据管线本身正在成为基础模型竞争的基础设施。
   - 来源: [arXiv](https://arxiv.org/abs/2609.18703) | [HuggingFace Daily Papers](https://huggingface.co/papers/2609.18703)

**FuseReg：通过层融合正则化缩小表征自编码器的重建与生成差距**
- 论文针对表征自编码器需要在生成器与像素解码器之间选择共享层的问题，提出 FuseReg 方法，用对编码器层随机子集的训练取代基于启发式的固定层融合。论文从理论上分析该机制可显式惩罚跨层不一致的敏感度。在 ImageNet-256 上，使用 DINOv3-L 时，单一 FuseReg 解码器可在不经重训练的情况下处理全层、稀疏层与单层融合，并取得比针对固定融合训练的专用解码器更高的 PSNR。在生成侧，仅替换解码器即可在 RAEv2 DiT-XL 生成器不变的情况下把无引导 gFID 降低 27%；若扩散训练阶段也联合正则化，可在 DiT-Base 上把无引导 gFID 再降 29%。
  > 💡 把层选择从一次性设计决策变成训练时的正则化目标，使单一模型同时适配不同融合粒度，意味着表征自编码器在视觉生成侧的部署成本和调参成本都有明显下降空间；该方法不改动预训练编码器，对存量视觉骨干的复用价值较高。
   - 来源: [arXiv](https://arxiv.org/abs/2609.31620) | [HuggingFace Daily Papers](https://huggingface.co/papers/2609.31620)

**论文提出 DCE+SRCL：递归自蒸馏让 8B 模型数学推理提升 35.6 个百分点**
- On-policy 自蒸馏（OPSD）用一个冻结的、能看到标准答案的模型副本充当教师，冻结有利于训练稳定，但教师无法吸收学生训练中学到的改进。论文提出递归框架解决这一限制：一是 Dynamic Co-Evolution（DCE），让特权教师与学生共同演化，上一轮学到的修正指导下一轮；二是 Self-Refined Concise Learning（SRCL），在模型自身回答的更短、经验证的改写上训练，抑制越改越长、过度自我批评的倾向。在多个模型规模与四个竞赛级数学基准上，DCE+SRCL 均超过 OPSD；Qwen3-8B 上达到 **65.97% Average@12**，高出 OPSD **35.62 个百分点**，同时平均输出长度较 DCE 再降 **7.80%**。
  > 💡 「教师与学生共同演化 + 简洁性约束」把自我蒸馏从一次性知识搬运变成可迭代的自我改进循环；不依赖外部教师意味着这套流程可低成本套用在任何已有模型上，是通往 recursive self-improvement 的一条务实路径。
   - 来源: [arXiv](https://arxiv.org/abs/2609.30652)

**VBVR-Pro：300 个可验证奖励任务把原生视觉推理做成闭环训练场**
- 原生视觉推理把视觉生成本身作为推理介质，但进展长期受限于缺少可扩展的训练任务、可靠反馈与受控比较。VBVR-Pro 提供闭环测试环境：把视觉推理组织成 **300 个程序化生成任务**；用确定性任务规则构建可验证奖励打分器，并系统揭示了主流 MLLM 作为评审（VLM-as-a-judge）的常见失败模式；还在 30 多种图像、视频与交错生成器上做受控模态实验。在 VBVR-Pro 上训练的模型向 RISE-Video、MME-CoF-Pro、BabyVision 等 **7 个外部视觉推理基准**强迁移，可验证奖励可支撑大规模多任务 RL 并带来更强的 RL 后表现；分析显示需要持久时空状态跟踪的任务上视频生成最强，交错生成是计算高效的替代方案。数据、模型、打分器与代码全部开源。
  > 💡 用「程序化任务 + 规则打分器」绕开 VLM-as-a-judge 的不可靠，等于把 RLVR 的思路移植到视觉生成介质；「vision-native 轨迹」的探针证据也为视觉链路是否真正参与推理提供了可检验的工具。
   - 来源: [arXiv](https://arxiv.org/abs/2608.26105)

**Sakana AI 提出 SAIL：测试时搜索把 VLM 机器人轨迹成功率从 25% 提至 73%**
- 基础模型单次生成的机器人轨迹并不可靠，性能高度依赖上下文，且运动目标上的小误差即可导致整个任务失败。Sakana AI 与东京大学提出 SAIL：策略 VLM 基于少量成功演示生成轨迹，在模拟器中测试，由评估 VLM 审查执行视频、定位进展停滞点并反馈修订，配合蒙特卡洛树搜索探索候选，最终只把选中的轨迹发送给物理机器人。在六个模拟操作任务上，搜索预算从 1 个候选增加到 45 个，轨迹生成成功率从 **25% 提升至 73%**；真机实验同样验证了测试时扩展的收益。该工作将发表于 IROS 2026。
  > 💡 「先在模拟里试错、再把最佳答案交给真机」把测试时扩展从语言推理移植到机器人控制，避开了在物理世界直接探索的安全成本；对「算力换可靠性」的路线而言，这是具身智能侧一个可复现的参照点。
   - 来源: [Sakana AI](https://sakana.ai/sail/) | [arXiv](https://arxiv.org/abs/2603.08269)

### X讨论
**Bespoke Labs 重发 AutoResearchExam：24 小时开放式研究基准，Fable 5.1 以 0.602 居首**
- Bespoke Labs 重新发布 AutoResearchExam 基准并配发演示视频。基准包含 **29 个开放式 ML 研究任务**，在 24 小时自动研究窗口内以统一 Terminus 2 harness 运行，主指标为隐藏测试集 AUARC，agent 全程只能看到验证分数，以区分真实泛化与验证集过拟合。24 小时榜单上 Claude Fable 5.1 以 **0.602** 微弱领先 GPT-6 Astra 的 0.600，Claude Opus 5 以 0.579 列第三；官方推文同时贴出更新榜单，称 Opus 5.5 登顶、前四名中 Anthropic 占三席。行为分析还显示，Anthropic 两款模型仅约 **7%** 的轮次是纯超参调优。
  > 💡 把「持续 24 小时自我改进 + 泛化到隐藏测试集」作为评测对象，等于给 recursive self-improvement 建了可量化的标尺；验证-测试差距与纯 HPO 占比的拆解，让「刷榜」和「真研究」第一次可以被区分开。
   - 来源: [@bespokelabsai](https://x.com/bespokelabsai/status/2104597984822562838) | [@bespokelabsai](https://x.com/bespokelabsai/status/2104597986370294077) | [AutoResearchExam](https://benchmarks.bespokelabs.ai/autoresearchexam/)

**Jason Weston 团队提出 RL-XAR：用专家对齐评分规则训出超越前沿模型的 27B 写手**
- Meta 研究者 Jason Weston 团队发布「Unslopping AI」。研究先证实标准 LLM 评审偏好模型而非专家人类：用 LLM 生成的常规 rubric 评分更是 **100%** 选模型——若 AI slop 被评为更好，用它做奖励训练只会产出更多 slop。RL-XAR 收集高质量人类文本，元优化出一套能把「人类专家 > 模型」差距拉开的评分 rubric（验证集差距从 -4.2 反转到 **+2.76**），再用这些 rubric 做 RL 并迭代到分不出差距。用该流程训练的 Qwen3.5-27B 在论文章节写作上以最严 rubric 得分 **9.60/10（人类=10）**居所有写手之首，故事续写从 2.8 提到 **8.2**、超过次优的 Claude 5 Opus（6.8），作者盲测对比中以 16:2 被偏好。
  > 💡 病根被定位在「评审无法识别专家写作」——非专家标注训练出的奖励模型天然带着标注者的天花板；先反向元优化出会打分的 rubric 再当奖励用，等于给写作质量造了一个 GAN 式可迭代的奖励函数，是 RLVR 思路向不可验证任务延伸的干净样本。
   - 来源: [@jaseweston](https://x.com/jaseweston/status/2104564368792854860) | [Meta RAM Blog](https://facebookresearch.github.io/RAM/blogs/unslop/)

**Vinod Khosla 警告：到 2030 年多数机器人初创公司估值将下挫**
- Vinod Khosla 在接受采访时表示，到 2030 年会有超过一半的机器人初创公司估值低于当前水平，而能够留在高位的公司将获得巨大倍数。Khosla 此前曾预测机器人领域将在未来两年迎来“ChatGPT 时刻”，此番言论延续了他对该赛道长期看好但短期过热的判断。报道同时提到，中国国家经济规划机构去年警告全国有逾 150 家公司涉足人形机器人赛道，宇树在上海证交所上市首月表现震荡，相关监管据报已收紧了人形机器人初创的 IPO 审批。
  > 💡 Khosla 的判断与中、美两侧的迹象互相印证：一边是 150+ 公司同质化竞争与监管收紧 IPO，一边是 VC 资金集中押注少数头部标的；这意味着机器人赛道未来五年可能呈现“少数高倍数、多数估值回撤”的分化格局，硬件交付能力将成为分水岭。
   - 来源: [The Information](https://www.theinformation.com/articles/valuations-robotics-startups-will-fall-2030-says-vinod-khosla)

---
*更新时间: 2026-09-29 06:45*