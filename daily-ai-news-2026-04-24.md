# 04月24日 AI前沿动态

**自动汇总** | 24h | 共 15 条

## 要点速览

- **模型前沿**：OpenAI发布GPT-5.5，编程和知识工作全面突破; 字节跳动发布Seed3D 2.0; 腾讯发布Hy3-preview开源模型，快慢思考融合295B MoE
- **产业动态**：Claude多项产品更新：Agent记忆+生态连接; Anthropic二级市场估值破万亿美元，首次超越OpenAI
- **算力追踪**：AI巨头加速欧洲算力布局：Anthropic洽谈数据中心协议+Google首建奥地利数据中心
- **初创&融资**：腾讯、阿里巴巴洽谈投资DeepSeek，估值超200亿美元; OpenAI洽谈15亿美元投资私募合资企业DeployCo; 勇芯科技获近亿元A轮融资，专注Chiplet AIoT芯片; NeoCognition获4000万美元种子轮，押注AI自主进化
- **研究关注**：FASTER降低扩散模型RL算法计算成本; Poly-EPO解决RL微调过早崩溃问题; GiantsBench评估LLM科学发现能力
- **X讨论**：Kimi将1篇天体物理论文转化为40页报告和2万行数据集; Flipbook：模型实时渲染每个像素，告别传统UI

---

## 模型前沿

**OpenAI发布GPT-5.5，编程和知识工作全面突破**

OpenAI发布GPT-5.5，官方称为"迄今最智能模型"。编程方面，Terminal-Bench 2.0 达 82.7%，SWE-Bench Pro 达 58.6%，多位高级工程师评测认为推理和自主性显著超越 GPT-5.4 和 Claude Opus 4.7。知识工作方面，GDPval（44种职业的Agent任务）达 84.9%，Tau2-bench Telecom 达 98.0%。**关键亮点：模型与NVIDIA GB200/GB300 NVL72联合设计，推理速度比GPT-5.4提升20%（由Codex本身优化了推理栈）；API上下文窗口1M，Codex中400K；API定价 $5 输入/$30 输出 per 1M tokens。** 安全方面，OpenAI将GPT-5.5的网络能力和生物能力评为"High"级别，部署了更严格的分类器并推出Trusted Access for Cyber项目。

> 💡 GPT-5.5不是单纯的能力提升，而是"模型自优化推理栈"的首次验证——Codex帮助优化了服务自身的基础设施。与NVIDIA的联合设计也标志着模型-硬件协同进入新阶段。

📌 来源: [OpenAI Blog](https://openai.com/index/introducing-gpt-5-5/) | [TechCrunch](https://techcrunch.com/2026/04/23/openai-chatgpt-gpt-5-5-ai-model-superapp/) | [@swyx](https://x.com/swyx/status/2047378670986342685#m)

**字节跳动发布Seed3D 2.0，Coarse-to-Fine两阶段3D生成**

字节跳动正式发布新一代3D生成大模型Seed3D 2.0，核心架构升级为Coarse-to-Fine两阶段生成策略，将"整体结构"和"几何细节"解耦分开优化，在锐利边缘、薄壁结构和复杂拓扑等难点上取得突破。纹理方面采用统一PBR生成模型联合建模完整PBR贴图，MoE架构提升高分辨率材质细节与边界精度，引入VLM先验增强未知光照下的材质分解稳定性。**超越单物生成，Seed3D 2.0还能完成部件级分割与补全、铰接资产生成（输出URDF标准格式，兼容Isaac Sim等仿真引擎）、以及基于图像/视频/文本的场景组合生成。** 60位3D建模经验打分员的盲评对比中，Seed3D 2.0对所有基线模型的偏好率均达69%以上。

> 💡 Seed3D 2.0的突破不只是"更好看的3D模型"，而是让生成式3D从展示级走向部署级——铰接资产和场景组合直接服务于具身智能的仿真训练需求。3D生成正在成为通往世界模型的关键路径。

📌 来源: [Seed官网](https://seed.bytedance.com/zh/seed3d_2_0) | [36氪](https://36kr.com/newsflashes/3778928879129865?f=rss)

**腾讯发布Hy3-preview开源模型，快慢思考融合295B MoE**

腾讯混元发布Hy3-Preview，总参数295B MoE（21B active），最大支持256K上下文，是腾讯2月重建预训练和强化学习基础设施后的首个模型。核心特色是"快慢思考融合"——在复杂推理（FrontierScience-Olympiad、清华求真书院数学博资考）、代码智能体（SWE-Bench Verified、Terminal-Bench 2.0）、搜索智能体（BrowseComp、WideSearch）等多个方向均有强竞争力。**腾讯强调三个原则：能力体系化不偏科、跳出刷榜做真实评测、追求性价比。** 模型已在元宝、QQ、腾讯文档等十余个腾讯产品上线，开源权重支持vLLM/SGLang，API个人版最低28元/月。

> 💡 腾讯的差异化在于"模型-产品Co-Design"——与元宝深度协同调优文风和意图理解，在用户体验层面而非纯benchmark层面做竞争。295B MoE + 21B active的性价比路线值得关注。

📌 来源: [腾讯混元官网](https://hy.tencent.com/research/hy3) | [@openrouter](https://x.com/OpenRouter/status/2047356098764808289#m)

## 产业动态

**Claude多项产品更新：Agent记忆功能进入公测，外部应用连接扩展至生活场景**

Claude Managed Agents的记忆功能进入公开测试，agent可从每个会话中学习并跨会话积累上下文，使用为智能优化的记忆层，无需每次重复提供背景信息。同日Claude扩展外部应用连接，新增Tripadvisor、Booking、Resy、Instacart、Spotify、Audible等生活类服务。**Anthropic推进Agent能力和生态连接两条线，显示出从"工作助手"向"全场景AI助手"加速演进的意图。** 记忆能力是Agent从一次性工具向长期助手演进的关键，生态连接数量则成为与ChatGPT差异化竞争的核心指标。据消息称Anthropic在Forge Global等未上市企业股权交易平台上的估值已升至约1万亿美元，超过OpenAI的8800亿美元。买家正在竞相抢购Anthropic日益减少的二级市场股票。

> 💡 Anthropic产品节奏加快：记忆功能解决Agent跨会话连贯性问题，外部连接扩展从工作延伸到生活。但跨应用数据隐私和权限管理仍是用户主要顾虑。

📌 来源: [@claudeai](https://x.com/claudeai/status/2047421844311949513#m) | [@claudeai](https://x.com/claudeai/status/2047383764347572389#m)｜[二级市场估值-36氪/财联社](https://36kr.com/newsflashes/3779005902066946?f=rss)


## 算力追踪

**AI巨头加速欧洲算力布局：Anthropic自建+Google首入奥地利**

Anthropic正积极推进在欧洲达成数据中心合作协议，以六位数薪酬聘请专人负责洽谈算力容量协议，表明正从依赖云厂商向自建算力基础设施演进。同日Google宣布在奥地利Kronstorf建设其首个数据中心，创造100个直接就业岗位，满足日益增长的数字服务和AI算力需求。Google奥地利数据中心配备Enns河水质改善基金、太阳能绿色屋顶和废热回收系统，并与上奥地利应用科技大学启动技能培训合作（此前已培训14万+奥地利人）。

> 💡 AI公司竞相在欧洲部署算力基础设施，背后是数据主权合规需求和AI推理本地化的双重驱动。

📌 来源: [36氪/新浪财经](https://36kr.com/newsflashes/3779388327629831?f=rss) | [Google Blog](https://blog.google/innovation-and-ai/infrastructure-and-cloud/global-network/google-data-center-austria/)

## 初创&融资

**腾讯、阿里巴巴洽谈投资DeepSeek，估值从100亿美元上调至200亿+**

The Information独家报道：腾讯和阿里巴巴正在与DeepSeek洽谈投资，这是DeepSeek首次接受外部融资。目标融资额超过3亿美元，估值从最初的约100亿美元因市场热度上调至200亿美元以上（部分报道达255亿）。**DeepSeek至今未产生实质性收入，模型完全开源。**

> 💡 DeepSeek首次接受外部融资是行业信号事件。无收入+全开源获200亿+估值，说明资本在下注开源模型的技术溢价和生态影响力，而非当前商业化能力。对中国AI格局而言，DeepSeek获得巨头背书可能重塑"国家队"版图。

📌 来源: [The Information](https://www.theinformation.com/articles/tencent-alibaba-talks-invest-deepseek-20-billion-plus-valuation)

**OpenAI洽谈15亿美元投资DeployCo，联手PE巨头抢攻企业AI部署**

OpenAI正与TPG、Bain Capital、Advent、Brookfield、Goanna等私募巨头组建合资企业DeployCo（内部代号），OpenAI承诺投资最高15亿美元，合资企业总估值约100亿美元。**DeployCo的核心商业模式是为PE投资组合企业提供AI部署服务，OpenAI向PE出资人保证回报与企业AI采用率挂钩。** 融资预计5月初关闭，之后DeployCo将开始招聘工程师团队为客户部署AI。Financial Times指出此举旨在对抗Anthropic在企业市场的攻势。

> 💡 DeployCo的"AI公司+PE联盟"模式是全新物种——OpenAI不只卖API，而是与资本方联合锁定企业客户部署链路。回报与采用率挂钩的机制意味着OpenAI对产品实际落地效果有高度自信（或高度压力）。

📌 来源: [The Information](https://www.theinformation.com/briefings/openai-talks-invest-1-5-billion-private-equity-joint-venture) | [Reuters](https://www.reuters.com/legal/transactional/openai-talks-commit-up-15-billion-private-equity-joint-venture-ft-reports-2026-04-22/)

**勇芯科技获近亿元A轮融资，专注Chiplet AIoT芯片**

勇芯科技完成近亿元A轮融资，由蚂蚁集团投资。公司面向AIoT市场，提供Chiplet芯片级解决方案，通过先进封装将多颗裸die封装，可用于医疗、工业、家居等百亿连接数场景。

> 💡 Chiplet路线在国内AIoT芯片领域获资本认可，蚂蚁集团投资布局物联网基础设施。

📌 来源: [IT桔子](https://www.itjuzi.com/investevent/14695441)

**NeoCognition获4000万美元种子轮，押注AI智能体自主进化**

俄亥俄州立大学教授苏瑜（清华本科、UCSB博士、前Microsoft研究员）创立的NeoCognition获得4000万美元种子轮融资，由Cambium Capital和Walden Catalyst联合领投，Vista Equity Partners及英特尔CEO陈立武等跟投。团队约15人，多为博士。公司核心思路是让AI智能体通过构建"微观世界模型"实现持续学习，从通才转变为领域专家。**当前AI智能体成功率仅约50%，NeoCognition试图从根本上解决通用Agent不可靠的问题。** 

> 💡 从"通用Agent"到"自主进化的专家Agent"，是Agent赛道的重要分叉。4000万美元种子轮规模不小，反映资本市场对Agent可靠性问题的重视。

📌 来源: [智东西](https://zhidx.com/p/551566.html)

## 研究关注

**Poly-EPO：通过set RL训练探索性推理模型**

Stanford团队（Chelsea Finn等）提出Polychromic Exploratory Policy Optimization（Poly-EPO），核心思路是训练LM生成一组响应，使其在奖励函数下集体准确且推理策略具有探索性。技术路线上，先建立set RL框架下的通用优化方法（通过修改advantage计算适配标准RL算法），再用Poly-EPO实例化——显式协同exploration和exploitation。**实验表明Poly-EPO提升了泛化能力（更高pass@k覆盖率），保持了生成多样性，并能随test-time compute有效扩展。** 

> 💡 Poly-EPO直接回应了当前RL微调中模型过早收敛到单一推理模式的问题。"set RL"思路与单样本RL的关键区别在于：不只优化单次回答的正确性，而是优化一组回答的覆盖度和多样性。这对需要多次采样的推理场景（数学、编程）有直接价值。

📌 来源: [arXiv](https://arxiv.org/abs/2604.17654) | [@chelseabfinn](https://x.com/chelseabfinn/status/2047155228546638026#m)

**FASTER：将去噪过程建模为MDP，大幅降低扩散策略计算成本**

FASTER（Value-Guided Sampling for Fast RL）将扩散策略的去噪过程建模为动作过滤MDP——在每个去噪步骤中，学习到的critic决定保留哪些候选、丢弃哪些，避免对所有噪声候选完成完整去噪。**关键发现：仅在噪声层级（计算代价最低的阶段）进行一次过滤，就能达到与完整去噪所有候选后选最优值相同的性能。** 

> 💡 扩散模型在机器人控制等场景兴起，但推理速度一直是瓶颈。FASTER的"早筛"策略简单有效，将计算量从O(N×去噪步数)降到接近O(N+去噪步数)。这意味着扩散策略的推理成本可以大幅降低而不损失质量。

📌 来源: [项目页](https://pd-perry.github.io/faster/) | [@chelseabfinn](https://x.com/chelseabfinn/status/2047151949607530787#m)

**GIANTS：训练LLM从文献中预见科学突破**

Stanford & NYU团队提出GIANTS（Generative Insight Anticipation from Scientific Literature），定义了"insight anticipation"任务：给定两篇被引用的父论文摘要，模型需要预测其结合后产生的下游论文核心洞察。**GiantsBench包含17,839个跨8个科学领域的示例，GIANTS-4B（基于Qwen3-4B，用GRPO强化学习训练）在完整测试集上比Gemini-3-Pro相对提升35%，在未见父论文的严格测试集上提升34%。** 人类评估中GIANTS-4B胜率89.7%，第三方SciJudge-30B也以68%的胜率偏好GIANTS-4B。LM judge评分与人类评分Spearman相关性达0.761。

> 💡 这不是"AI做科研"，而是测试模型是否能完成科学发现中最关键的"组合式洞察"步骤。4B小模型通过RL超越Gemini-3-Pro，再次验证了专用RL训练在特定任务上的巨大杠杆。

📌 来源: [项目页](https://giants-insights.github.io/) | [@chelseabfinn](https://x.com/chelseabfinn/status/2047158378028568699#m)

## X讨论

**Kimi将1篇天体物理论文转化为40页报告和2万行数据集**

Moonshot AI展示Kimi将一篇天体物理论文转化为40页报告、2万行数据集和14张天文学级图表，并封装为可复用Skill。

> 💡 Kimi在学术文档处理上的长上下文和结构化输出能力转化为具体生产力工具，但效果取决于论文质量。

📌 来源: [@kimi_moonshot](https://x.com/Kimi_Moonshot/status/2047190593634463817#m)

**Flipbook：模型实时渲染每个像素，告别传统UI**

Zain Shah（前OpenAI、YC S13）等三人发布原型项目Flipbook——想象屏幕上每个像素都由模型实时流式渲染，没有HTML、没有布局引擎、没有代码，只呈现用户想看的内容。推文获得4.3M浏览量、22K转发。

> 💡 从"模型生成代码"到"模型直接渲染像素"是交互范式的跃迁，类似从命令行到GUI的转变。当前还是prototype阶段，但概念影响力很大。如果这条路走通，将从根本上重新定义"用户界面"这个概念——UI不再是被设计出来的，而是被模型实时生成的。

📌 来源: [@zan2434](https://x.com/zan2434/status/2046982383430496444)

*更新时间: 2026-04-24*
