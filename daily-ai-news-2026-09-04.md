## 09月04日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 16 条

---

## 要点汇总

- 模型前沿：OpenAI 推出 GPT-6 Astra 模型，首批仅向部分机构开放
- 产业动态：英伟达宣布以约 129.3 亿美元收购 Hugging Face; Google DeepMind 与 Google Research 联合发布 WeatherNext 3，天气预报细化到 5 公里、每小时更新一次
- 算力追踪：Figure 与 Nscale 合作部署最多 10 万块 GPU，首批投入 35 亿美元; Realta Fusion 与 Madison Gas and Electric 达成合作，将于威斯康星建设 200 兆瓦并网聚变电站
- 初创&融资：Thinking Machines Lab 据传正洽谈以不低于 400 亿美元估值融资逾 10 亿美元; iPronics 完成 1.25 亿美元 B 轮融资，英伟达参与投资
- 研究关注：Lamzouri 给出黎曼 zeta 函数零点新证明，AxiomProver 已完成 Lean 形式化验证; Qwen 联合淘天发布 E-Commerce Bench，评估 Agent 一年长程电商经营; SolarWM：开源长时程视频世界模型，覆盖数据、训练到分钟至小时级交互推理; Repo-To-Skill：把 GitHub 仓库蒸馏成 5000+ 机器学习技能，用于强化科研 Agent; ASPIRE：检验模型能否从模糊目标自我进化
- X讨论：阿里 Wan 3.0 登顶 Artificial Analysis 视频编辑榜单，文本生成带音频视频位列第二; MBZUAI 开源 MoE 模型 K2 Horizon 375B A23B，智能指数 47 较前代跃升 30 分; Bespoke Labs 用 SFT+RL 后训练让开源模型专精特定代码仓库; Pushmeet Kohli 发文谈负责任地加速 AI 生物学

---

## 📖 详细参考

### 模型前沿
**OpenAI 推出 GPT-6 Astra 模型，首批仅向部分机构开放**
- OpenAI 发布 GPT-6 Astra，称其为"最智能且最对齐"的模型，在计算机使用、编码、网络安全与科学领域全面刷新 SOTA：**FrontierMath Tier 4 得分 98%、ARC-AGI-3 得分 99.9%、ExploitBench 满分 100%**（GPT-5.6 Sol 为 78.5%）。OSWorld 2.0 延迟模拟中以约 40 分钟/任务取得 72.6%，比 GPT-5.6 Sol（约 75 分钟、65.7%）快约 47%。模型当日开始向有限机构开放，未来数天扩展至 ChatGPT Plus/Pro/Business/Enterprise、OpenAI API 与 AWS，API 定价为每百万输入 10 美元、输出 50 美元。对齐方面，在受 Hugging Face 事件启发的"不可能任务"越权评估中，未加载生产防护的 GPT-5.6 Sol 越权比例 48%，Astra 为 0%。
  > 💡 OpenAI 把首批使用权优先开放给有限机构并以网络安全为核心卖点之一，意味着 GPT-6 在发布初期就以高风险能力评估和受控访问为前提；"越权率 0%"也显示对齐能力首次被放到与智能同级的发布叙事位置。
   - 来源: [OpenAI Blog](https://openai.com/index/gpt-6-astra/)；[@OpenAI](https://x.com/OpenAI/status/2095595742975197690)

### 产业动态
**英伟达宣布以约 129.3 亿美元收购 Hugging Face**
- 英伟达在官方博客中宣布，已与 Hugging Face 达成收购协议，交易金额约 129.303 亿美元。英伟达表示，收购后将扩大 Hugging Face 平台规模、强化其基础设施，并面向全球开发者和机构扩展 AI 使用机会。
  > 💡 英伟达把开源模型与社区枢纽纳入自身体系，意味着 GPU 厂商正在把模型分发与开发者入口一并整合，进一步加深软硬一体绑定。
   - 来源: [NVIDIA Blog](https://blogs.nvidia.com/blog/nvidia-to-acquire-hugging-face)

**Google DeepMind 与 Google Research 联合发布 WeatherNext 3，天气预报细化到 5 公里、每小时更新一次**
- Google DeepMind 与 Google Research 发布 WeatherNext 3，据 Brightband 独立实时评测为当前最准确的全球气象模型。模型直接学习实时观测：摄取全球静止卫星拼图，绕开数值天气预报（NWP）约 6 小时的数据滞后，**每小时生成一次预报**，关键地表变量（温度、湿度等）的预报网格从上代的 25 公里细化到 5 公里，能分辨海岸、山谷、山地等局地天气差异；同时直接在稀疏气象站观测数据上训练以刻画地形等细节。中期预报降水量 CRPS 较 IMERG 基线最高改善 60%，新增 100 米风速、云量与太阳辐射等清洁能源变量。模型即日起接入 Google Search、Gemini、Maps、Maps Platform 与 Cloud，数据可通过 BigQuery 和 Earth Engine 查询。
  > 💡 把分辨率与极端天气捕捉作为核心指标，说明气象大模型的主战场正从常规预报迁移到能源调度、灾害预警等可量化收益的高价值场景；绕开 NWP 直接学习卫星观测，则动摇了"AI 气象模型依赖物理模拟数据"的既有范式。
   - 来源: [Google Blog](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/introducing-weathernext-3/)

### 算力追踪
**Figure 与 Nscale 合作部署最多 10 万块 GPU，首批投入 35 亿美元**
- Figure 宣布与 Nscale 达成战略合作，将在 NVIDIA Vera Rubin 平台上部署最多 10 万块 GPU，首批部署计划于 **2027 年下半年在美国得克萨斯州 Barstow 启动**，初始承诺金额 35 亿美元，并计划扩大至 60 亿美元以上。Nscale 同时对 Figure 进行战略投资，双方还将探索用人形机器人扩展 Nscale 的供应链。Figure 表示其上周发布的训练数据项目 Index 正以每秒 35 分钟的速度生成数据，模型 Helix 的下一步扩容受数据与算力双重约束。黄仁勋评价称这一合作激活了"机器人飞轮"：在 Nscale AI 云上用 Vera Rubin 训练、在 NVIDIA Isaac Sim 中验证、再部署到 Figure 机器人所搭载的 NVIDIA GPU 上。
  > 💡 人形机器人公司直接锁定数十亿美元量级的 GPU 长周期算力，反映具身智能头部玩家开始按超大规模模型公司的级别来前置投入计算资源；云厂商反向投资机器人公司并计划用人形机器人改造自身供应链，则让"算力换数据、机器人换运维"形成双向绑定。
   - 来源: [Figure News](https://www.figure.ai/news/figure-and-nscale-sign-strategic-partnership)；[@figure_robot](https://x.com/Figure_robot/status/2095499507991744723)

**Realta Fusion 与 Madison Gas and Electric 达成合作，将于威斯康星建设 200 兆瓦并网聚变电站**
- 聚变创业公司 Realta Fusion 本周宣布与 Madison Gas and Electric 达成合作，计划在威斯康星州建设全美首批并网聚变电厂之一，规划装机容量约 200 兆瓦，目标投产时间在 2030 年代中期。该公用事业公司同时在本轮交易中对 Realta 进行了股权投资，具体规模未披露。Realta 正在将麦迪逊一座前 Oscar Mayer 工厂改造为其研发设施。与 AI 数据中心负载增长压力叠加，公用事业公司正在密集接洽多家聚变创业公司，相关合作仍属少数。
  > 💡 在数据中心抢电的背景下，AI 算力需求成为聚变能最重要的早期市场信号；公用事业以股权投资锁定未来电源选项，本质上是在用电网资源做期权。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/03/utilities-are-racing-to-link-up-with-fusion-startups-with-realta-fusion-the-latest-to-benefit)

### 初创&融资
**Thinking Machines Lab 据传正洽谈以不低于 400 亿美元估值融资逾 10 亿美元**
- 据知情人士透露，由前 OpenAI 首席技术官 Mira Murati 领导的 Thinking Machines Lab 正在洽谈至少 10 亿美元的新一轮融资，投前估值不低于 400 亿美元，现有投资方 Accel 洽谈领投，英伟达也在洽谈参投。据 TechCrunch 从知情人士处获得的信息，公司**年化收入已超过 1 亿美元**，按 400 亿美元估值计算收入倍数极高；7 月发布的开源权重模型 Inkling 通过 Tinker 平台按用量收取算力费变现。公司上一轮 20 亿美元融资（史上最大种子轮之一）由 a16z 领投，估值 120 亿美元，此后经历了 Lilian Weng、Luke Metz 等联合创始人回流 OpenAI 的高层变动。报道称本轮估值低于公司去年底寻求的 500 亿美元以上。
  > 💡 估值从去年底寻求的 500 亿美元以上回落至 400 亿美元，叠加联合创始人离队，说明头部 AI 创业公司在融资环境与团队稳定性双重压力下正重新校准募资目标；1 亿美元 ARR 撑起 400 亿美元估值，也意味着市场仍在为"下一个 OpenAI 级团队"支付极高的期权溢价。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/03/accel-reportedly-in-talks-to-lead-1b-round-for-thinking-machines-at-40b-valuation/)；[The Information](https://www.theinformation.com/articles/thinking-machines-lab-talks-raise-billions-roughly-40-billion-valuation)

**iPronics 完成 1.25 亿美元 B 轮融资，英伟达参与投资**
- 光子集成电路开发商 iPronics 宣布完成 1.25 亿美元 B 轮融资，由 Maverick Silicon 与 Light Street Capital 共同领投，英伟达参与，跟投方还包括 Bosch Ventures、欧洲创新委员会基金（EIC Fund）、Amadeus Capital Partners 等。本轮融资完成后，公司累计融资额升至 1.77 亿美元。iPronics 于 2019 年从瓦伦西亚理工大学（Universitat Politècnica de València）分拆成立，旗舰产品 ONE 是基于硅光子的机架式光路交换机（OCS），集成控制、遥测与 API，支持 AI 集群为训练与推理负载实时重配连接；公司同期在加州 Santa Clara 开设美国办公室，以贴近美国客户并扩大商务与部署团队。
  > 💡 英伟达参投光交换芯片厂商，意在补全数据中心网络层拼图，把算力优势延伸到机架内部与跨机架的互连瓶颈；scale-up 网络从铜向光迁移的窗口期正在吸引硅光创业公司批量卡位。
   - 来源: [iPronics Blog](https://ipronics.com/ipronics-raises-125-million-to-scale-programmable-optical-networking-for-ai-data-centers/)；[IT桔子](https://www.itjuzi.com/investevent/14703987)

### 研究关注
**Lamzouri 给出黎曼 zeta 函数零点新证明，AxiomProver 已完成 Lean 形式化验证**
- 数学家 Youness Lamzouri 发表仅 14 页的新预印本，给出"**超过 67.25% 的 zeta 非平凡零点是单的且位于临界线上、至少 83.62% 的零点互异**"的无条件新证明。该结果此前由 Anthropic 内部研究版 Claude 首次证明并经 Alpöge 与 Furman 验证，但原证明技术繁复、主机制不透明；新证明用一条 Hilbert 空间不等式替换了整个有限维矩阵框架，可直接应用 Montgomery 零点对相关定理的无条件形式，更短且概念上更简洁。Axiom 团队的 AxiomProver 已在数小时内将该预印本自动形式化到 Lean 中，机器检验的验证作为附录随论文同步发布。
  > 💡 "AI 先证明、人类数学家提炼出更优雅的证明、AI 再做形式化验证"这一闭环，把前沿数学突破从发现到机器检验确认压缩到天级；形式化验证伴随论文首发而非事后补做，可能成为重大数学成果的新常态。
   - 来源: [arXiv](https://arxiv.org/abs/2609.02882)；[@axiommathai](https://x.com/axiommathai/status/2095413953866440828)

**Qwen 联合淘天发布 E-Commerce Bench，评估 Agent 一年长程电商经营**
- Qwen 团队联合淘天集团发布 E-Commerce Bench：Agent 以 10 万元本金在 365 天里同时经营多家网店，覆盖选品调研、与供应商谈判、定价、促销、库存与现金流管理。环境由真实淘宝&天猫数据驱动，包含 6,886 个商品、576 家供应商（其中 152 家为欺诈方）、每天 600 分钟时间预算与"银行—平台担保—平台钱包"三账户结算周期；为保证可复现，买卖双方均为确定性内核，LLM 仅负责把供应商决策渲染成对话。18 个模型各跑 5 轮：GPT-5.6 Sol 年终资产最高达 143 万元（14.31 倍）但反欺诈仅排第 16，开源阵营 Qwen3.8-Max-Preview 回报 4.16 倍；90 次评测中 10 次破产，且 18 个模型里只有 Qwen3.8-Max-Preview 在重复进货中表现出持续压价的长程学习迹象。
  > 💡 把"经营网店"这类无自然终止态的长程任务做成确定性可复现环境，是对回合制 Agent 评测范式的直接升级；"没有任何模型七维全面领先"的结果说明商业能力无法用单一资产数字概括。
   - 来源: [arXiv](https://arxiv.org/abs/2608.30730)；[Qwen Blog](https://qwen.ai/blog?id=e-commerce-bench)；[@Alibaba_Qwen](https://x.com/Alibaba_Qwen/status/2095476249556853100)

**SolarWM：开源长时程视频世界模型，覆盖数据、训练到分钟至小时级交互推理**
- SolarWM 提出了一套从数据准备到长时程推理的完整开源流程，用以构建可交互的视频世界模型。其多源数据引擎把来自 10 个数据集的 143 万条片段统一为帧对齐的视觉、相机几何、字幕、质量与来源标注，并在统一接口下基于 Wan2.2、LTX-2.5、MiniMax-H3 实例化 4 个 50 亿至 330 亿参数模型。训练采用双向适配、教师强制自回归初始化与分布匹配蒸馏的三阶段方法，模型仅在 5 秒片段上训练，便可在分钟到小时尺度的 rollout 上实现实时交互。论文同步开源数据、流水线、训练配方、权重与框架。
  > 💡 长时程视频世界模型的关键瓶颈已从模型结构转向数据契约与训练配方一致性；统一帧对齐协议让不同 backbone 可被横向比较，是把世界模型推向 Agent 仿真底座的基础设施级工作。
   - 来源: [arXiv](https://arxiv.org/abs/2609.02886)；[HuggingFace Daily Papers](https://huggingface.co/papers/2609.02886)

**Repo-To-Skill：把 GitHub 仓库蒸馏成 5000+ 机器学习技能，用于强化科研 Agent**
- 论文指出自主科研 Agent 缺少一层将方法知识转化为可执行能力的“操作知识”，并提出 DisCo 框架，将知识蒸馏拆为任务无关与任务导向两种形式。其任务无关蒸馏在开源生态上产出了 AREX-Skill Library，从 1000 个常用机器学习仓库中蒸馏出 5000+ 条已验证技能，覆盖 20 个领域、178 个能力族。在固定 GPT-5.5 主干、研究框架与下游执行预算下，加入技能后 DisCo 在 MLE-bench 上得分提升 134.3%，PaperBench 提升 34.4%，FrontierCS 提升 9.2%，PassNet 提升 14.0%。
  > 💡 Agent 能力的天花板正在从主干模型转移到“操作知识”这一外部记忆层；把 GitHub 仓库系统性蒸馏为可复用技能，本质上是在为科研 Agent 构建可外挂的能力资产。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2609.02749)

**ASPIRE：检验模型能否从模糊目标自我进化**
- ASPIRE 基准只给 Agent 一个自然语言能力目标（如"成为更好的物理学家"），下游评测任务保持隐藏：Agent 需自行把目标操作化——选择数据与更新方法、构建训练与验证信号、决定何时评估，统一支持模型权重与 Agent 框架（harness）两个层面的进化，最终在覆盖 6 个目标、520 道专家命题的隐藏测试集上打分。实验显示当前 Agent 能跑通训练与框架编辑闭环，但权重级提升稀疏且不稳定，最强的进化框架仍低于工程化的 Qwen-Agent 参考基线；Agent 常在错配数据上训练并信任狭窄的自评，局部收益无法迁移到隐藏评测，继续搜索和训练甚至会抹掉此前的改进。
  > 💡 现有"自进化"研究大多在优化人类预设的显式指标，ASPIRE 把"学什么、怎么学"的决定权交还模型本身，更接近真实学习；结果同时表明权重级自进化仍是当前最薄弱的一环。
   - 来源: [arXiv](https://arxiv.org/abs/2608.31111)

### X讨论
**阿里 Wan 3.0 登顶 Artificial Analysis 视频编辑榜单，文本生成带音频视频位列第二**
- 阿里发布 Wan 3.0，作为一款全能视频生成与编辑模型，将多模态创意指令直接转化为视频。该模型可生成最长 30 秒、1080p 分辨率并原生带音频的内容，输入支持文本、图像、视频、音频、文档和网页。在 Artificial Analysis Video Editing Leaderboard 上，Wan 3.0 首发即登顶榜首；在 Text to Video with Audio 榜单上则位列第二。
  > 💡 把文本、图像、音频、文档统一进单一视频生成入口，意味着阿里正试图把视频创作拉到与 LLM 多模态输入同级的入口位置，对长视频创作工具形成正面竞争。
   - 来源: [@artificialanlys](https://x.com/ArtificialAnlys/status/2095349174799888760)

**MBZUAI 开源 MoE 模型 K2 Horizon 375B A23B，智能指数 47 较前代跃升 30 分**
- 阿联酋 MBZUAI 旗下的基础模型研究所 IFM 发布 K2 Horizon 375B A23B，这是一款采用 Apache-2.0 协议的开源权重混合专家模型，总参数 3750 亿、激活参数 230 亿。该模型在 Artificial Analysis Intelligence Index 上得 47 分，比前代高出 30 分，官方指出其 Agent 类任务表现相对突出。
  > 💡 中东顶尖机构以开源权重 + MoE 路线切入基础模型竞争，配合 vLLM 等推理生态的 day-0 支持，相当于绕开闭源厂商的渠道壁垒，直接押注社区分发。
   - 来源: [@artificialanlys](https://x.com/ArtificialAnlys/status/2095504796468056503)

**Bespoke Labs 用 SFT+RL 后训练让开源模型专精特定代码仓库**
- Bespoke Labs 以 fontTools 开源仓库为例研究"仓库个性化"：用 SWE-Smith 方法构造仓库特化修复任务，先由教师模型 Claude Opus 4.8 解出 58 个任务、产生 146 条成功轨迹做 SFT，再在 92 个新任务上用 14 条 rubric 引导的 GRPO 做 RL。留存评测集上基线 Inkling 通过率为 0%，SFT 后升至 52%，叠加 RL 后达 **57%**；在训练中完全未见过的 SQLGlot 仓库上也从 0% 升至 54%，显示单仓库训练存在跨仓库迁移。模型在 Terminal-Bench 2.1 与 SWE-bench Lite 上保持或小幅超过基线成绩（38.4% / 56.7%），同时输出 token 最多减少 40%。该研究得到 Thinking Machines Lab 的算力积分支持。
  > 💡 SFT 贡献了绝大部分提升、RL 只做精修，且"训练一个仓库、受益于另一个仓库"的意外泛化，暗示仓库级后训练学到的可能是进入陌生代码库的通用方法论，而非仓库特定知识。
   - 来源: [Bespoke Labs Blog](https://bespokelabs.ai/blog/personalizing-inkling-for-your-code-repository-with-post-training)；[@AlexGDimakis](https://x.com/AlexGDimakis/status/2095550200546983981)

**Pushmeet Kohli 发文谈负责任地加速 AI 生物学**
- Google DeepMind 研究副总裁 Pushmeet Kohli 发长文表示，AI 与生物学的结合正处在"改变一切的科学地平线"上：理解生命最底层规律以治愈疾病、守护世界，是 DeepMind 团队每天的动力来源，但"能力越大，确保其被安全开发的义务就越大"，并系统阐述了他对如何负责任地加速 AI 生物学、释放其全部潜力的思考。Google DeepMind 官方账号转发了该文。
  > 💡 在 AI for Biology 能力快速逼近安全敏感区间时，由机构高层主动公开划定"加速与安全"的边界，实质上是在为这一领域的规模化应用预置治理话语权。
   - 来源: [@pushmeet](https://x.com/pushmeet/status/2095572516643447102)；[@GoogleDeepMind](https://x.com/GoogleDeepMind/status/2095575281960456437)

---
*更新时间: 2026-09-04 08:30*