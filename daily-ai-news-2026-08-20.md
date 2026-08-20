## 08月20日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 17 条

---

## 要点汇总

- 产业动态：Generalist AI 发布 GEN-1.5：一次演示即学会新任务，零样本即兴泛化到未见工具与场景; OpenAI 预览 Private Safety Processing：零数据保留下也能跨交互做安全监控
- 算力追踪：Cerebras 发布下一代 CS-4：性能与功耗同步翻倍; TerraPower 押注储能优势切入 AI 数据中心供电; Marvell 深度绑定 Google 自研芯片：122 亿美元认股权证与采购目标挂钩
- 初创&融资：Stripe 确认以 75 亿美元收购 AI 模型聚合平台 OpenRouter; NVIDIA 洽谈以 200 亿美元估值投资 AI 数据标注商 Mercor; AI 原生会计创业公司 Rillet 三个月 ARR 翻倍，1 亿美元 C 轮拿下独角兽估值; 低功耗 AI 芯片公司 Velaura AI 完成 1.1 亿美元 A 轮，估值迈过 10 亿美元; Relativity Networks 获 2200 万美元融资，把空芯光纤带进数据中心
- 研究关注：SA-MRPO：按饱和度重分配梯度，让多目标RL把力气用在“还没学会”的目标上; Debate 训练显著降低 RLAIF 中的 Reward Hacking; Agentic ESOpt：用进化策略微调长时域 LLM Agent; Agent Lightning v1.0：让部署时的 Agent Harness 直接参与后训练; ASI-Bench：逐步撤除人类指导，实测 AI 距自主科研还有多远
- X讨论：唐杰长文谈 Scaling Law：GLM-5.3 同参数规模下靠后训练 scaling 取得显著收益; TPU 与 Mooncake 集成，KVCache 池化走向 TPU 推理

---

## 📖 详细参考

### 产业动态
**Generalist AI 发布 GEN-1.5：一次演示即学会新任务，零样本即兴泛化到未见工具与场景**
- Generalist AI 发布机器人基础模型 GEN-1.5：只需在上下文窗口放入 3–12 秒的单次演示（“物理提示”），模型即可不做任何梯度更新、直接执行新任务，10 项任务平均成功率 **59%**；再用 5 分钟数据做 10 步梯度微调，成功率升至 **83%**。更关键的是零样本物理泛化：仅演示过用刷子扫方块，模型遇到香蕉会当刷子用、遇到簸箕则自创“抬起倾倒”的全新动作序列（两种用法均不在训练数据中），还能双手互换、自主移开障碍物、把方块按颜色归类——公司称此类即兴行为在微调步数越少时越强，因为轻适配模型更贴近预训练先验。模型处理视频、传感、语言与本体感知输入，输出 100 Hz 动作轨迹，预训练已持续 8 个月以上，公司强调一次性学习与即兴泛化均未经专门设计、从大规模物理交互数据中涌现；另展示组合泛化、零样本 sim-to-real（预训练不含仿真数据）与人到机器人迁移。
  > 💡 GPT-3 式的 in-context learning 在机器人基础模型上规模化涌现（Generalist 称为其所知首例）——预训练越过阈值后，任务适应成本趋近于零。若“演示即编程”成立，机器人从专家数月编程变成任何人几秒示范，改变的是部署速度与使用者边界。
   - 来源: [Generalist AI Blog](https://generalistai.com/blog/gen-1.5) | [@GeneralistAI](https://x.com/GeneralistAI/status/2090161970536497210)

**OpenAI 预览 Private Safety Processing：零数据保留下也能跨交互做安全监控**
- OpenAI 重申对符合条件的 API 客户提供零数据保留（ZDR）：请求处理完成后不保留 prompts 与模型响应，OpenAI 人员不可查看客户内容，企业数据默认不用于模型训练。同时预览 Private Safety Processing：自动化系统跨关联交互识别滥用模式（如多账户协同试探、agent 任务中偏离用户意图），OpenAI 人员无法接触底层内容、仅收到窄范围安全信号；内容可存于客户自控基础设施，或以客户持钥加密方式存于 OpenAI 侧。该功能正在与早期客户测试，计划 9 月开始推出并发布技术白皮书，Glean CISO Sunil Agrawal 公开表态支持。
  > 💡 前沿模型部署中“安全监控要求数据留存”与“企业隐私承诺”的冲突，是拦在受监管行业采购前的硬约束。OpenAI 用自动化信号+客户持钥加密把两者解耦，ZDR 从静态承诺升级为可持续演进的工程方案，瞄准的是企业级市场的信任瓶颈。
   - 来源: [OpenAI](https://openai.com/index/our-commitment-to-zero-data-retention)

### 算力追踪
**Cerebras 发布下一代 CS-4：性能与功耗同步翻倍**
- SemiAnalysis 披露 Cerebras CS-4 细节：沿用与 CS-3 相同的 5nm WSE-3 晶圆，靠供电与散热改进把时钟频率翻倍，SemiAnalysis 预计每晶圆 tokens/s/user 从 CS-3 的约 2,000 提升至近 **4,000**，且有效 BOM 成本可能与上代持平；片上内存带宽 **43 PB/s**（公司宣传约为 Nvidia Rubin 的 2,000 倍），但每晶圆 44GB SRAM 容量未变仍是核心短板。机架改为模块化“backpack”设计，每架 3 晶圆（上代 2 晶圆）、TDP 125–135kW；新 I/O 模块可现场升级，开放片外 I/O 从 1.2 升至 2.4 Tb/s，支持与 HBM 系统组成解耦推理，已与 AMD、AWS Trainium 合作，SemiAnalysis 认为明显为 AWS EFA NIC 预留了位置。公司路线图承诺每年性能翻倍、2027 年吞吐提升 20 倍。
  > 💡 在同一代硅片上靠功率与系统工程把性价比翻倍，Cerebras 把竞争焦点从制程转向“每美元 token 交互性”；但 44GB SRAM 容量约束决定了它必须走与 GPU 集群解耦组网的差异化路线，而非正面替代。
   - 来源: [SemiAnalysis](https://newsletter.semianalysis.com/p/cerebrass-next-generation-cs-4-fast) | [@SemiAnalysis_](https://x.com/SemiAnalysis_/status/2089893209128280303)

**TerraPower 押注储能优势切入 AI 数据中心供电**
- 由 Bill Gates 创立的核电创业公司 TerraPower 被彭博报道将于今年宣布其首个数据中心项目。该项目预计 2027 年破土动工，将成为公司第二座核电站，首座已在美国怀俄明州开建。TerraPower 此前未透露客户身份，但今年 1 月已宣布 Meta 同意采购其八座 Natrium 核电站。TerraPower 的核心卖点在于其反应堆与储能系统联动的设计：储能模块可在电力需求波动时吸收过剩电力或补足缺口，使反应堆保持接近满功率运行。现有反应堆功率每分钟只能升降约 5%，即使新一代小型模块化反应堆也只能做到每分钟约 10%。
  > 💡 TerraPower 用储能套件避开核电爬坡慢的硬伤，把 AI 数据中心需要的“稳定基荷”卖成可调度的连续供电方案，差异化卖点比单纯堆功率更稀缺。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/19/terrapowers-nuclear-reactor-has-a-secret-weapon-for-powering-ai-data-centers)

**Marvell 深度绑定 Google 自研芯片：122 亿美元认股权证与采购目标挂钩**
- Marvell 宣布与 Google 达成合作，为后者 TPU 生态开发覆盖广泛芯片及相关技术；Google 同时获得认股权证，可按每股 206.58 美元买入至多 5897 万股 Marvell 股份，全额行权约 **122 亿美元**，将使 Google 成为 Marvell 第五大股东（据 LSEG 数据）。权证大部分份额须 Google 在 2033 财年前达成约定采购目标方可解锁，潜在持股规模与采购量直接绑定。消息公布后 Marvell 盘前涨超 11%，Google 原主要定制芯片伙伴 Broadcom 跌逾 2%——后者与 Google 的定制 AI 芯片合作协议已签到 2031 年。
  > 💡 云巨头用“采购换股权”把芯片设计伙伴锁进自家路线图：对 Marvell 是订单与资本的双重背书，对 Google 是在 Broadcom 之外建立第二定制芯片供应源；股权解锁与采购量挂钩，把利益同盟变成可审计的合同条款。
   - 来源: [Reuters](https://www.reuters.com/technology/marvell-grants-google-122-billion-stock-warrant-custom-chip-deal-2026-08-19/)

### 初创&融资
**Stripe 确认以 75 亿美元收购 AI 模型聚合平台 OpenRouter**
- Stripe 官方宣布已同意收购 AI 模型网关与路由平台 OpenRouter，后者帮助企业跨 **80+ 供应商的 400+ 模型**动态评估每条请求并按任务复杂度、价格、速度、可靠性路由，客户包括 NVIDIA、Zoom 和 Lovable。Stripe 去年已推出 Token Billing 等产品帮助企业优化 token 成本，此次收购旨在同时管理 AI 时代盈利的两面——最大化收入与效果、最小化成本；CEO Patrick Collison 称“token 是 AI 公司的核心货币”，OpenRouter CEO Alex Atallah 表示“智能将是多模型的，没有单一模型对所有任务最优”。据《纽约时报》报道，交易总额 75 亿美元，其中 15 亿美元支付给创始团队、60 亿美元支付给既有投资人。
  > 💡 Stripe 把模型路由与计费入口收入自己手中，支付网络与 AI 推理调度的耦合加深：OpenRouter 一类的中间层从独立基础设施变成支付巨头的内部能力，“token 经济基础设施”成为 Stripe 的明牌战略。
   - 来源: [Stripe Newsroom](https://stripe.com/zh-us/newsroom/news/stripe-agrees-to-acquire-openrouter) | [@patrickc](https://x.com/patrickc/status/2090125021910020520)

**NVIDIA 洽谈以 200 亿美元估值投资 AI 数据标注商 Mercor**
- 据知情人士透露，NVIDIA 正在洽谈投资数据标注服务商 Mercor，该投资将是一轮 200 亿美元估值融资的一部分。现有投资人 General Catalyst 已在商谈领投这轮融资。报道指出，Mercor 历史上大部分收入来自 OpenAI、Google 和 Anthropic 等闭源模型厂商，但随着 NVIDIA 推进其 Nemotron 开源模型，Mercor 来自 NVIDIA 的收入正在增长。
  > 💡 NVIDIA 既向 Mercor 下单又讨论入股，是把数据标注同时绑成 Nemotron 开源模型与自研芯片生态的供应环节，模型、芯片、训练数据三件套的纵向整合正在加深。
   - 来源: [The Information](https://www.theinformation.com/articles/nvidia-discusses-funding-ai-data-supplier-mercor-20-billion-valuation)

**AI 原生会计创业公司 Rillet 三个月 ARR 翻倍，1 亿美元 C 轮拿下独角兽估值**
- AI 原生会计创业公司 Rillet 宣布完成 1 亿美元 C 轮融资，估值 10 亿美元，由 Iconiq 领投，Andreessen Horowitz 与 Sequoia 等老股东跟投。Rillet 2024 年才走出隐身模式，目前客户超过 600 家，并称过去三个月 ARR 翻倍。联合创始人兼 CEO Nicolas Kopp 在 X 上表示本轮融资在 48 小时内敲定，并非主动启动，而是 EY 结盟、ARR 与客户增长带来了投资人超额兴趣。Rillet 累计融资已超过 2 亿美元。
  > 💡 48 小时完成 C 轮、ARR 三个月翻倍，说明 AI 垂直 SaaS 在企业记账与 ERP 替换市场上已进入用收入兑现估值的阶段。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/19/rillet-raises-100m-series-c-at-1b-valuation-2-years-after-emerging-from-stealth)

**低功耗 AI 芯片公司 Velaura AI 完成 1.1 亿美元 A 轮，估值迈过 10 亿美元**
- 低功耗 AI 芯片公司 Velaura AI 完成 1.1 亿美元 A 轮融资，估值超过 10 亿美元，由 Seligman Ventures 领投，新投资方 Capricorn Investment Group 及老股东 Samsung Catalyst Fund等参投。核心产品 Titan Core 芯片设计平台瞄准数据中心与机器人等 Physical AI 场景的能效提升，联合创始人兼 CEO Rajiv Khemani 向 Reuters 表示技术已部署于 **3000 万颗以上芯片**、正与四大云厂商中的三家洽谈，并称“AI 的下一个时代不仅由更好的模型定义，也由根本更好的计算经济学定义”。商业模式为预付授权费+按节电份额抽成的版税，Khemani 确认类似 Arm 早期按芯片授权的模式；据 IT桔子，其专利低压库与 EDA 流程可在不改动上层软件的前提下将 AI 加速器能效提升 2–4 倍，并已与多家云厂商在 3nm/2nm 节点合作。
  > 💡 “预付+节电分成”把节电效果直接货币化，硅 IP 授权路径避开与 NVIDIA CUDA 生态正面竞争；3000 万颗芯片的部署验证+三大云厂商在谈，让这家 A 轮公司直接站上估值十亿美元。
   - 来源: [Reuters](https://www.reuters.com/legal/transactional/chip-designer-velaura-ai-valued-more-than-1-billion-after-funding-round-2026-08-18/) | [IT桔子](https://www.itjuzi.com/investevent/14703008)

**Relativity Networks 获 2200 万美元融资，把空芯光纤带进数据中心**
- 空芯光纤创业公司 Relativity Networks 宣布 2200 万美元 SAFE note 融资，由 Rhapsody Venture Partners、Bell Ventures 等参与，另获一家未具名头部云厂商 **4000 万美元**后续订单。空芯光纤让光在纤芯真空腔中传播、逼近光速理论极限，信号时延从常规光纤每公里约 5 微秒降至 **3.5 微秒**；CEO Jason Eichenholz 称随着最大系统把算力跨多园区分布，时延优势意味着可用地理跨度同比扩大，“AI 第一个时代优化算力，第二个时代优化数据中心内组网，我们看到的第三个时代是优化地理”。
  > 💡 光纤时延第一次成为数据中心选址变量：跨园区同步推理的半径扩大，缓解的是电网与用地约束而非算力本身。空芯光纤从长距骨干走向 AI 园区组网，是个此前少有人押注的物理层赛道。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/19/relativity-networks-raises-22-million-to-bring-a-faster-kind-of-fiber-to-data-centers/)

### 研究关注
**SA-MRPO：按饱和度重分配梯度，让多目标RL把力气用在“还没学会”的目标上**
- 后训练 RL 常把多个奖励目标（如正确性、格式、长度）按固定权重加总成单一奖励再优化，论文指出这有两个问题：奖励组合完全不同的 rollout 可能拿到相同的 advantage，且已经“学会”的目标和还没学会的目标始终按同一比例占用梯度预算，训练力气浪费在已饱和目标上。SA-MRPO 的做法是：对每个奖励目标独立做组内标准化，再根据批量层面的饱和度估计动态下调接近解决目标的权重，把优化预算腾给还有提升空间的目标——该机制作用足够强，甚至能反转一次梯度更新的方向。数学推理的 15 个基准对比中，SA-MRPO 相对 GDPO 在更难正确性目标上 12 次占优（AIME24 最高 +5%），自适应推理 5 个基准平均 +3.8%（AMC23 最高 +9.2%），编码 pass rate 最高 +2.3%，同时已满足的简单目标不出现回退。
  > 💡 把“哪些目标还需要学”作为动态资源分配信号，标志着后训练 RL 正从“统一加权奖励”转向“按学习余量调度梯度”，对多任务模型的工程化训练尤为关键。
   - 来源: [arXiv](https://arxiv.org/abs/2608.16072)

**Debate 训练显著降低 RLAIF 中的 Reward Hacking**
- RLAIF 用 LLM 裁判打分充当奖励信号，策略在训练中会学会利用裁判的系统性错误骗取高分、实际表现反而下降（reward hacking），且裁判越弱于策略问题越严重——这正是“用弱模型监督强模型”这一对齐核心设定下的难题。论文引入辩论：让生成器与批评者就答案对抗、由一个更弱的 LLM 裁决胜负，使策略的漏洞在对抗中被暴露而非被利用。数学任务上，单玩家 RLAIF 基线很快攻陷弱裁判，辩论训练则全程维持裁判表现，峰值验证准确率挽回 **45%** 的性能差距；裁判进一步变弱导致的加速攻陷，可通过增加一轮辩论补偿。团队还发现给批评者设字数上限（150 词内有效）能防止其反向攻陷裁判，代价是限制批评的表达清晰度。
  > 💡 这是“可扩展监督”路线少见的大规模实证正结果——用对抗结构而非更强裁判对冲 reward hacking，直接回应“弱裁判监督强模型”这一超对齐核心设定。
   - 来源: [arXiv](https://arxiv.org/abs/2608.17776)

**Agentic ESOpt：用进化策略微调长时域 LLM Agent**
- 长时域 agent 轨迹分支多、奖励稀疏，RL 的反向传播训练栈显存开销大到难以微调大模型，信用分配（哪一步贡献了最终成败）也随轨迹变长急剧恶化。论文主张改用进化策略（ES）：在当前参数附近采样扰动、让整个 agent 跑完任务后只用最终奖励做奖励加权更新——因此仅需推理级显存即可全参数优化，无需分解奖励，黑盒接口还能与提示空间进化组合。在 WebArena-Lite 上对 Qwen-3.5-27B 的全参数优化较 No Skill 基线提升 **6.69%**；在测试时自动启发式设计中让提示与参数在线共同进化，36 个设置里 28 个优于匹配基线。
  > 💡 agent 轨迹越长、奖励越稀疏，反向传播训练栈的边际成本越高；ES 的“低显存全参训练”卖点在长时域 agent 时代重新变得务实。
   - 来源: [arXiv](https://arxiv.org/abs/2608.17310)

**Agent Lightning v1.0：让部署时的 Agent Harness 直接参与后训练**
- 真实 agent 运行在自己的 harness（管理工具调用、上下文与控制流的外壳）里，而传统 agent RL 要求训练引擎接管环境交互循环，训练与部署两套环境难以保持一致。论文系统化 harnessed agentic RL 范式：由 harness 拥有环境交互循环，训练器只观察 LLM 请求-响应对序列——任意框架写的 agent 无需重写即可接入 RL 训练，代价是需要解决重分词、样本合并、优势计算等新挑战。团队发布约 3500 行代码的轻量框架作为研究测试床，并用 6K 训练样本与适度算力把 Qwen3.5-9B 在 SWE-bench Verified 从 41.8% 提升至 **56.4%**（+14.6 分），完整工作流与训练脚本已开源。
  > 💡 这一解耦架构已被 verl Uni-Agent、AReaL 2.0、slime 等框架跟进，正在成为 agent RL 的事实标准：任何框架写的 agent 都能直接接 RL 训练器。
   - 来源: [arXiv](https://arxiv.org/abs/2608.17528)

**ASI-Bench：逐步撤除人类指导，实测 AI 距自主科研还有多远**
- 论文发布首个联合评估“创新探索+自主科研执行”的基准 ASI-Bench：40+ 专家投入 31000+ 人时构建，覆盖 11 个科学领域 60 个项目级任务；关键设计是在同一项目内逐步撤除人类指导——从提供完整方法论文档，到只给方法名，再到完全由 agent 自主选法、执行研究并产出可验证结果。18 个 SOTA agent-模型组合的平均分随之从 **50.91** 跌至 **29.10**、再到 **26.62**，说明当前系统离开人类方法论指导后，距离自主完成端到端项目级科研还很远。
  > 💡 用“逐步撤梯子”的实验设计把“AI 距自主科研多远”从口号变成可量化指标——答案是从 50 分掉到 27 分那么远。
   - 来源: [arXiv](https://arxiv.org/abs/2608.17271)

### X讨论
**唐杰长文谈 Scaling Law：GLM-5.3 同参数规模下靠后训练 scaling 取得显著收益**
- 智谱唐杰发表长文梳理 scaling law 演变：从 Kaplan 的参数优先（2.7:1）到 Chinchilla 的 20 tokens/参数，到推理时代转向小模型过度训练（Llama-2-7B、Gemma-2-9B 分别约 290、889 tokens/参数），再到 MoE 下总参数与激活参数职责分离——总参数管知识容量，激活参数与有效深度管推理链长度。文中披露 GLM-5.3 是一个受控实验：与 GLM-5.2 同基础模型、同架构、同总参数与激活参数，仅一个月的长时域环境与 RL scaling 就带来“不算边际”的收益；并预告下一个旋钮可能是 mid-training、pre-training。
  > 💡 把 scaling 显式拆成多个可独立调节的旋钮（基座规模、数据、单次前向算力、后训练）并公开宣称参数之外仍有大量余量，是清晰的“后训练时代”技术叙事——行业竞争重心正从预训练参数竞赛转向后训练环境工程。
   - 来源: [@jietang](https://x.com/jietang/status/2089941544581403107)

**TPU 与 Mooncake 集成，KVCache 池化走向 TPU 推理**
- SemiAnalysis 称 Google TPU 正与流行的开源推理优化库 Mooncake 合作，将 TPU 接入 Mooncake Store。与 NVL72 上的做法类似，KVCache DRAM P2P 池化初期将经由 scale-out 网络（TPU 的 TENT 互连）实现，而非 ICI/NVLink。Mooncake 的作用是提升生产推理的性能/TCO。
  > 💡 KVCache 分离式存储正从 GPU 生态外溢到 TPU，推理基础设施的内存层在独立成可复用组件；但走 scale-out 网络而非片间互连，意味着初期只能吃到池化的部分收益。
   - 来源: [@SemiAnalysis_](https://x.com/SemiAnalysis_/status/2090197436614557797)

---
*更新时间: 2026-08-20*