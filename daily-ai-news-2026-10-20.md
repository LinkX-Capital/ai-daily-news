## 10月20日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 15 条

---

## 要点汇总

- 模型前沿：Inception 扩散模型 Mercury 3 上线 OpenRouter：生成速度较 Mercury 2.5 提升 4 倍至 1,000+ tok/s
- 产业动态：NVIDIA 发布开源权重模型 Nemotron 3.5 Super VL 与端侧 Bolt 系列：120B 主攻企业 Agent，Bolt 落地 AI PC; 五角大楼官员 Emil Michael 放话：AI 公司若不配合政府，将动用出口管制等行政工具; 密歇根大学分拆公司 Laplace Intelligence：用 AI 智能体在仿真中红队测试机器人与自动驾驶
- 算力追踪：报道称 DeepSeek 深度参与华为下一代 AI 芯片设计：工程师长期驻场，需求直接写入设计决策; Amazon 出资建设 12 台 Xe-100 小型核电堆：装机 960 兆瓦落户印第安纳旧煤电厂址，并锁定首批购电; SemiAnalysis：2027 年将成为数据中心"加速之年"，单年新增超 50GW、60GW 在建、年内已签 1.3 万亿美元租约
- 初创&融资：AI 芯片创业公司 Tenstorrent 融资 15 亿美元、估值达 62 亿美元，拒绝收购意向选择独立发展; RRAM 存算芯片研发商铭芯启睿完成超 4 亿元 A 轮融资，博原资本领投; 高气候风险住宅保险公司 Stand 完成 7000 万美元 C 轮融资，Saga Ventures 领投
- 研究关注：ACT3D：结果奖励 RL 让 VLM 自学 3D 主动探索，六基准平均 53.2% 超过 Gemini 3.6 Flash; Consistent Distribution Matching：免数据免仿真的扩散蒸馏，单步生成在 ImageNet 256 拿到 FID 2.04; LiveMACEBench：以实时金融市场为测试场的过程感知基准，30 天实测发现智能体结果与能力脱节
- X讨论：Cognition 宣称 Devin Fusion 以 68 分登顶 AA Coding Agent Index，较 Claude Code 单任务成本再降 31%; Humanoid 宣布参加 NVIDIA GTC Berlin，CEO 与 CPO 将带来两场演讲

---

## 📖 详细参考

### 模型前沿
**Inception 扩散模型 Mercury 3 上线 OpenRouter：生成速度较 Mercury 2.5 提升 4 倍至 1,000+ tok/s**
- Inception 的新一代扩散模型 Mercury 3 已上线 OpenRouter，生成速度超过 1,000 tokens/s、支持 1M 上下文，速度为 Mercury 2.5 的 4 倍。据 Inception 方面报告，该模型在 IFBench、GPQA Diamond 与 SWE-Bench Atlas 上击败 GPT-6 Luna 与 Haiku 5.5。上线期间定价五折，输入为每百万 tokens 0.10 美元、输出为每百万 tokens 0.35 美元。
  > 💡 扩散语言模型把"快"做成核心卖点，1,000+ tok/s 叠加 1M 上下文直指 Agent 长链路任务的吞吐经济学；但当前跑分是厂商自报口径，半价也属上线促销，规模化后的真实性价比仍需第三方评测与稳定定价验证。
   - 来源: [@openrouter](https://x.com/OpenRouter/status/2112225779782398131)

### 产业动态
**NVIDIA 发布开源权重模型 Nemotron 3.5 Super VL 与端侧 Bolt 系列：120B 主攻企业 Agent，Bolt 落地 AI PC**
- NVIDIA 发布面向常驻 Agent 与边缘计算的开源权重模型：Nemotron 3.5 Super VL 为 1200 亿参数，定位企业级 Agent，官方称参数量虽少于 Nemotron 3 Ultra，但在指令遵循与工具使用任务上可达到相近准确率。同时发布的两款轻量 Bolt 模型面向本地运行，适配搭载 RTX Spark 芯片的 AI PC 与配备 DGX Spark 的工作站，相关设备正通过 Microsoft、Dell 等伙伴进入市场。NVIDIA 称 Super VL 在文档智能、财务核算、科学实验、医疗保险理赔与安全攻防等特定 Agent 任务上经后训练后，完成任务速度快于 Anthropic 与 OpenAI 的竞品模型，并列出 Skydance、EY、Ramp、CrowdStrike、Perplexity、Salesforce 等使用方。
  > 💡 开源权重加分层部署是 NVIDIA 把模型生态绑到自家硬件上的打法——模型免费开放，真正的护城河在 RTX Spark、DGX 设备与 NVIDIA 基础设施的出货；对企业自建推理栈是降低选型成本的选择，但速度对比仍是官方口径，需第三方验证。
   - 来源: [TechCrunch](https://techcrunch.com/2026/10/19/nvidia-launches-new-open-models-to-run-agents-in-the-enterprise-and-on-pcs)

**五角大楼官员 Emil Michael 放话：AI 公司若不配合政府，将动用出口管制等行政工具**
- Emil Michael 是美国国防部高级官员，也是 Trump 本月宣布的 Super Intelligence Force 四位牵头官员之一。他在接受 The Information 采访时表示，如果 AI 公司不与政府合作，将动用包括出口管制在内的一系列行政工具来约束其行为，并把呼吁加强监管的前沿实验室比作要求别人替自己停车的醉汉。此前他曾主导与 Anthropic 的公开冲突，在后者拒绝移除安全护栏后推动国防部将其列为供应链风险。如今他作为政府与 Anthropic 等 AI 公司的联络人，负责牵头制定网络入侵、黑客攻击等关键事件的处理协议。
  > 💡 同一官员既手握"政府联络人"的合作通道，又公开保留出口管制的强制选项，说明华盛顿对前沿实验室的策略已转向合作与施压并举；安全护栏是否保留正在从技术争论升级为国家安全议题，Anthropic 与政府关系的走向将持续牵动行业。
   - 来源: [The Information](https://www.theinformation.com/articles/pentagons-emil-michael-vows-export-controls-ai-labs-cooperate-government)

**密歇根大学分拆公司 Laplace Intelligence：用 AI 智能体在仿真中红队测试机器人与自动驾驶**
- 位于 Ann Arbor 的 Laplace Intelligence 一年前从密歇根大学分拆成立，联合创始人为 CEO Howie Sun 与首席科学家 Henry Liu。公司构建面向机器人与物理 AI 的自动化红队测试，用 AI 智能体与交互式仿真在部署前对机器人与自动驾驶车辆做压力验证，通过刻意诱导失败来暴露问题。Sun 过去八年在学术界研究如何在仿真中挑战自动驾驶 AI，2023 年与当时的导师 Liu 合作的论文登上 Nature 封面。公司目前已实现盈利，入选 TechCrunch Disrupt（10 月 13 日至 15 日，旧金山）Startup Battlefield 200 的 20 强，并于 10 月 13 日登台展示。Sun 表示，目标是帮助企业在部署前发现并修复问题，并逐步建立可供客户、保险方与监管者信赖的共享证据库。
  > 💡 “AI 测 AI”在物理世界比纯软件场景更迫切，因为失败代价不可回滚；仿真红队若能产出保险与监管认可的量化证据，有机会从安全验证工具升级为物理 AI 部署链路上的合规基础设施。
   - 来源: [TechCrunch](https://techcrunch.com/2026/10/19/laplace-intelligence-red-teams-robots-and-self-driving-cars-before-they-hit-the-real-world)

### 算力追踪
**报道称 DeepSeek 深度参与华为下一代 AI 芯片设计：工程师长期驻场，需求直接写入设计决策**
- 据报道，DeepSeek 正与华为深度合作，参与其未来 AI 芯片的设计，两位知情人士称这一合作有望帮助中国在不依赖英伟达技术的情况下构建前沿模型。据悉双方关系超出了客户与芯片供应商之间常见的路线图沟通：华为工程师正把 DeepSeek 的需求与建议纳入具体设计决策，例如模型如何在处理器之间计算与搬运数据，相关芯片将于明年及以后推出。其中一位知情人士称，华为工程师已在 DeepSeek 办公场地长期派驻。
  > 💡 模型公司反向定义芯片设计，说明 DeepSeek 的计算与数据搬运策略正成为国产芯片的事实规格来源；对英伟达的威胁不在单卡性能，而在于芯片与头部模型工作负载的贴合度，这会加速中国前沿模型与本土算力的绑定。
   - 来源: [The Information](https://www.theinformation.com/articles/deepseek-shaping-huaweis-ai-chips-growing-challenge-nvidia)

**Amazon 出资建设 12 台 Xe-100 小型核电堆：装机 960 兆瓦落户印第安纳旧煤电厂址，并锁定首批购电**
- Amazon 宣布出资支持在印第安纳州建设装机 960 兆瓦的核电站，并将成为该电站电力的首个买家，电站由公用事业公司 AEP 运营，X-energy 提供 12 台 Xe-100 小型模块化反应堆，选址位于 Terre Haute 以南一座已拆除的燃煤电厂旧址。这是双方两年内的第二份商业协议，规模为上一份的三倍；Amazon 曾于 2024 年 10 月领投 X-energy 7 亿美元 C-1 轮，两家公司计划到 2039 年在美国新建 5 吉瓦核电装机。这些反应堆将接入公共电网，Amazon 称电力同时服务其数据中心。项目进度取决于 X-energy 能否按期交付位于休斯敦东南 Dow Chemical 园区的首座电站：该选址将部署四台 Xe-100，目前尚未开工，建造许可处于美国监管审批的后期阶段，且近期卷入德州政府指控涉及水务与固废法规许可"惯常违规"的诉讼。
  > 💡 从买绿电升级为出资建核电并锁定首购，是巨头对数据中心负荷扩张最直接的供给侧锁定方式；但 X-energy 首个项目尚未动工又涉诉讼，SMR 供应链能否支撑 2039 年 5 吉瓦目标仍是最大不确定因素。
   - 来源: [TechCrunch](https://techcrunch.com/2026/10/19/amazon-to-fund-12-small-nuclear-reactors-at-former-indiana-coal-plant)

**SemiAnalysis：2027 年将成为数据中心"加速之年"，单年新增超 50GW、60GW 在建、年内已签 1.3 万亿美元租约**
- SemiAnalysis 发布数据中心 2027 年前瞻分析，称 2027 年将是"加速之年"，单年新增容量超过 50GW。该机构的前瞻指标显示，目前有 60GW 数据中心在建，年内至今已签署的租约合同总额达 1.3 万亿美元。分析同时判断，算力短缺的瓶颈可能从电力侧转移到芯片侧。
  > 💡 租约先行、建设跟进，1.3 万亿美元的合同额意味着未来几年的交付压力已经锁定；若短缺确实从电力转向芯片，产业链约束将从"能否供电"变成"能否拿到芯片"，服务器与芯片排产节奏将成为 2027 年的关键变量。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2112069964131713517)

### 初创&融资
**AI 芯片创业公司 Tenstorrent 融资 15 亿美元、估值达 62 亿美元，拒绝收购意向选择独立发展**
- 聚焦推理的 AI 芯片公司 Tenstorrent 完成 15 亿美元融资，估值 62 亿美元，较 2024 年底的 26 亿美元估值翻倍以上，本轮由 Trace Capital 与 Innovation X 领投，Cadence Ventures、Eclipse、Fidelity、SanDisk 和 T. Rowe Price 等参投。据此前报道，这家成立十年的公司五个月前曾收到 Intel 与 Qualcomm 方面最高 50 亿美元估值的收购意向。CEO Jim Keller 向 Bloomberg 表示，在验证 Galaxy 服务器可以运行 DeepSeek 模型后，公司决定保持独立并继续融资，新资金将用于扩展面向开源权重模型服务和视频生成的芯片。
  > 💡 在英伟达供给紧张、开源模型推理需求放量的窗口期，独立算力标的的稀缺性明显抬升，估值翻倍反映的是这种筹码价值；但拒绝被收购也意味着必须靠 Galaxy 方案的真实出货兑现估值，软件生态仍是其与英伟达竞争的最大短板。
   - 来源: [TechCrunch](https://techcrunch.com/2026/10/19/tenstorrent-hits-6-2b-valuation-to-scale-open-weight-ai-chips)

**RRAM 存算芯片研发商铭芯启睿完成超 4 亿元 A 轮融资，博原资本领投**
- 铭芯启睿专注研发突破传统架构计算瓶颈的新型 RRAM 存储与 AI 计算技术，产品聚焦三个方向，包括面向 AI 大模型场景的混合异构存算系统，以及嵌入式 IP 与独立式存储芯片。公司宣布完成超 4 亿元 A 轮融资，由博原资本领投，博世创投、创领资本、米哈游、中关村科学城公司、兆易创新等跟投。复容投资、国开科创、恒裕资本、锦秋基金、顺禧基金、小米战投、中科创星等老股东持续加注。
  > 💡 存算一体是绕开冯·诺依曼瓶颈与 HBM 供给约束的替代路线之一，本轮股东名单同时出现博世、兆易创新等产业方和米哈游这类下游算力需求方，说明该路线在产业链两侧都拿到真金白银背书；下一个看点是混合异构存算系统能否在大模型场景拿出实测吞吐与成本数据。
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14706218)

**高气候风险住宅保险公司 Stand 完成 7000 万美元 C 轮融资，Saga Ventures 领投**
- Stand 主营野火、飓风等高气候风险区域的住宅财产保险，用物理仿真结合 AI 为房屋搭建数字孪生、逐栋模拟灾害场景以测算房产风险，并向业主提供加固方案，完成防灾改造即可下调保费。保单由 A 评级保险主体承保，再保险网络完善，当前承保房产价值超百亿美元，业务落地加州与佛罗里达。近日公司完成 7000 万美元 C 轮融资，Saga Ventures 领投，Jackson Square Ventures、Neotribe Ventures、Inspired Capital、Equal Ventures、Eclipse Ventures、Lowercarbon Capital 参投。
  > 💡 传统保险公司撤出高风险房产留下的定价真空，正是 AI 风险建模的切入口，超百亿美元承保规模说明模式已跑通一定体量；但业务高度依赖区域保险监管，极端灾害集中爆发时的大额赔付风险始终存在，数字孪生的测算精度与再保险安排将是扩张速度的关键约束。
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14706227)

### 研究关注
**ACT3D：结果奖励 RL 让 VLM 自学 3D 主动探索，六基准平均 53.2% 超过 Gemini 3.6 Flash**
- 论文提出 ACT3D，研究视觉语言模型在保持单图原生视觉编码的前提下如何学会在 3D 空间中思考与主动探索：3D 表示仅作为可通过动作（如向左移动）与观测（渲染图像）交互的环境，模型从初始第一人称视角与视觉问题出发，迭代推理、导航并调整视角后再给出最终答案。训练先做轨迹监督微调，再施加以最终答案正确性为主要奖励信号的强化学习，RL 阶段不直接监督该看哪些视点或采取哪些探索动作，模型只能从交互对表现的提升中自行学出探索策略。在六个 3D 基准上，ACT3D 平均准确率达 53.2%，较基座 Qwen 模型提升 22.0%，并超过专有模型 Gemini 3.6 Flash；同时以少 50-70% 的输入帧数超过现有开源 3D 方法，在未见过领域上较监督初始化平均再提升 5.9%。分析显示探索行为随问题条件自适应：初始视角即可回答的问题增益仅 0.6%，需要大量探索的问题增益达 16.3%，模型会搜索被遮挡目标、避免不必要的探索并获取互补视点。
  > 💡 探索策略没有被显式监督，却在纯结果奖励下自行涌现，说明"何时看、看哪里"可以作为任务奖励的副产品学出，为具身与空间智能省掉了人工标注视点轨迹的成本；两类问题 0.6% 对 16.3% 的增益差也提示，探索能力的主要价值集中在遮挡搜索与空间对比类任务上。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.21783)

**Consistent Distribution Matching：免数据免仿真的扩散蒸馏，单步生成在 ImageNet 256 拿到 FID 2.04**
- 论文提出 Consistent Distribution Matching，一种免仿真、免数据的蒸馏方法，用于加速扩散与流模型的推理并保留生成能力。框架只包含一个冻结教师与一个可训练学生共两个模型，把样本生成与得分估计统一到同一个学生网络，并只优化单一目标。论文证明最小化该目标意味着学生的流图推送分布按 Wasserstein 距离收敛到教师的边缘分布。在 ImageNet 256×256 上，该方法训练 40 个 epoch 后，单次函数评估（1-NFE）取得 FID 2.04，4-NFE 取得 FID 1.37，超越了现有无数据蒸馏的最优基线。代码与模型已开放。
  > 💡 现有蒸馏方法常依赖精选数据集、昂贵的教师 rollout 或代理网络，训练与扩展复杂度高；该方法把蒸馏压缩到两模型一目标，且单步 FID 2.04 已具备实用意义，对推理成本敏感的图像生成部署是一条直接可走的加速路径。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.09221)

**LiveMACEBench：以实时金融市场为测试场的过程感知基准，30 天实测发现智能体结果与能力脱节**
- 论文提出 LiveMACEBench，一个过程感知基准，把实时演变的金融市场作为持久运行 LLM 智能体的天然测试场。五家前沿 LLM 在工具使用、持久记忆、规则遵循与多智能体协作四项配置对齐的条件下沿连续轨迹运行，评估同时覆盖实际结果与从完整决策轨迹导出的机制级诊断。30 天实测发现明显的“结果—能力”差距：实际收益常与能力维度的测量相背离，相近的结果也可能来自截然不同的机制使用模式。轨迹级诊断进一步暴露各能力维度的不同瓶颈，说明机制可及、机制有效使用与下游表现并非可互换的能力度量。
  > 💡 只看收益排行会掩盖智能体的真实短板，尤其在环境随智能体行为闭环变化时；把活市场从排行榜改造成诊断环境，为评估 agent 在动态条件下的可靠性提供了可复制的度量框架。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.09872)

### X讨论
**Cognition 宣称 Devin Fusion 以 68 分登顶 AA Coding Agent Index，较 Claude Code 单任务成本再降 31%**
- Cognition 宣布 Devin Fusion 在 Artificial Analysis Coding Agent Index 上取得 68 分，宣称位居榜首。该方案以 Opus 5.5 担任主导模型、GPT-6 Luna 担任辅助角色。与同样搭载 Opus 5.5 的 Claude Code 相比，Devin Fusion 在性能与价格两端均占优，单任务成本降低 31%。
  > 💡 Devin Fusion 的成绩由旗舰模型组合与编排层驱动，而非自研基座，说明 Coding Agent 榜单竞争正从单模型能力转向模型配比与 harness 工程。若第三方复测坐实 68 分与 31% 降本，Claude Code 在按任务计费的企业市场将直接承压。
   - 来源: [@cognition](https://x.com/cognition/status/2112290148205436979)

**Humanoid 宣布参加 NVIDIA GTC Berlin，CEO 与 CPO 将带来两场演讲**
- Humanoid 宣布将参加 NVIDIA GTC Berlin，公司领导层将在会上进行两场演讲。演讲人分别为创始人兼 CEO Artem Sokolov 与首席产品官 Sotirios Stasinopoulos。公司在宣传中称这两场对话值得关注。
  > 💡 创始人 CEO 与 CPO 双双登台，说明公司把 GTC Berlin 当作面向开发者与生态伙伴的重点曝光场合；结合此前 GTC Berlin 参会名单引发的持续关注，人形机器人厂商的高调亮相本身也是一种生态站位动作。
   - 来源: [@thehumanoidai](https://x.com/TheHumanoidAI/status/2112199364386935159)


---
*更新时间: 2026-10-20 06:58*