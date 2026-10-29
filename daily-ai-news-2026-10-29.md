## 10月29日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 15 条

---

## 要点汇总

- 模型前沿：Google 发布 Gemini 4 Carbon：称能力显著超过不到一个月前的新模型
- 产业动态：报道称 Marvell 洽谈收购数据中心光通信厂商 Lumentum; ASE 展示 AMD Venice CPU 面板级封装方案，首期量产瞄准 2027 年一季度; AMD 跑通 DeepSeek-V4 Flash 强化学习：24 张 MI308X 覆盖端到端训练流程; GitHub 发布 Copilot Fusion：在 Anthropic 与 OpenAI 模型间动态编排; Agility Robotics 邀请教育与劳动力委员会成员参观 RoboFab 工厂
- 算力追踪：Microsoft 营收增长回升：Azure 加速，数据中心投入压制现金流; Oracle 设定数据中心资本开支峰值期：股价单日涨逾 10%; 美国拟向 Constellation 核电站提供 50 亿美元贷款：新增 1.1GW 容量支撑数据中心
- 初创&融资：自动化工厂初创 Foundry 完成 1 亿美元 A 轮融资，以物理 AI 机器人重构产线; 具身智能初创完成 1 亿美元融资，估值约 200 亿美元且尚无营收; 三维存算一体芯片企业微纳核芯完成 10 亿元人民币 C+ 轮融资
- 研究关注：Timestral：四款时间序列基础模型登顶 GIFT-Eval、TIME 与 fev-bench; MPO：以轮次为尺度分配信用，长程智能体在多类任务上优于强 RL 基线; PDRVLA：融合物理动态表征，四个仿真基准最高成功率 99.3%

---

## 📖 详细参考

### 模型前沿
**Google 发布 Gemini 4 Carbon：称能力显著超过不到一个月前的新模型**
- Google 发布 Gemini 4 Carbon，并称该模型的能力显著超过公司不到一个月前推出的模型。这是 Google 在近一年未发布新旗舰前沿模型后的又一次旗舰更新。
  > 💡 连续更新表明 Google 正加快前沿模型发布节奏，以应对 OpenAI、Anthropic 等竞争实验室带来的压力。
   - 来源: [The Information](https://www.theinformation.com/briefings/google-launches-gemini-4-carbon-second-major-ai-model-month)

### 产业动态
**报道称 Marvell 洽谈收购数据中心光通信厂商 Lumentum**
- 据知情人士透露，芯片厂商 Marvell Technologies 一直在洽谈收购数据中心光通信厂商 Lumentum。Lumentum 市值超过 800 亿美元，若交易达成，将成为规模最大的半导体交易之一。目前尚不清楚谈判进展，Bloomberg 报道称交易可能很快公布。
  > 💡 潜在交易将把 Marvell 的芯片业务与 Lumentum 的数据中心光通信能力结合起来，但谈判状态和交易落地仍不确定。
   - 来源: [The Information](https://www.theinformation.com/briefings/marvell-talks-buy-lumentum)

**ASE 展示 AMD Venice CPU 面板级封装方案，首期量产瞄准 2027 年一季度**
- ASE 展示了面向 AMD Venice CPU 的面板级封装方案，初步量产目标为 2027 年一季度，地点可能位于其高雄工厂。ASE 及其子公司 SPIL 已与 AMD 合作，在 Venice 中落实第二代 Fan-Out Embedded Bridge 技术。当前尺寸为 310 × 310 毫米的面板可容纳 25 个 Venice 中介层，但具体边缘损耗数据在现有证据中未完整披露。
  > 💡 Venice 的面板级封装已给出明确时间表，但首期可能仅限小规模生产；其实际价值仍取决于良率、成本以及从中介层方案迁移到量产系统后的表现。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2115527763767500836)

**AMD 跑通 DeepSeek-V4 Flash 强化学习：24 张 MI308X 覆盖端到端训练流程**
- AMD 使用 24 张 Instinct MI308X GPU 和 AITER 支持的强化学习技术栈，完成了 DeepSeek-V4 Flash 的端到端强化学习实验。测试覆盖三个 MI308X OAM 节点，包括长上下文 FP8 rollout、BF16 MoE actor 训练、在线 RDMA 权重更新、评估和检查点恢复，而非仅测试推理或单次训练步骤。训练与推理采用分离服务架构，两个节点承载 BF16 actor，第三个节点承载 FP8 rollout 引擎，并由 Ray 协调两组 GPU。
  > 💡 该实验证明 MI308X 集群能够覆盖模型强化学习的完整工程链路，并提供了三节点配置样板；其意义主要是验证软件栈与分布式训练的可行性，尚不能直接外推大规模训练的经济性。
   - 来源: [AMD ROCm Blogs](https://rocm.blogs.amd.com/ecosystems-and-partners/deepseek-v4-mi308-aiter-backed-rl/README.html)

**GitHub 发布 Copilot Fusion：在 Anthropic 与 OpenAI 模型间动态编排**
- GitHub 已将 Copilot Fusion 发布到 GitHub Copilot，该系统用于在 Anthropic 与 OpenAI 模型之间进行编排。GitHub 将 Copilot Fusion 定义为运行时编排系统，可按任务选择并协调模型，以优化性能、成本和延迟。Artificial Analysis 称，其在 Claude Code 上的得分比 Opus 5.5 低 2 分，但单任务成本减半。
  > 💡 Copilot Fusion 展示了多模型编排产品的一条可行路线：不再由用户固定选择模型，而是由运行时按任务目标权衡效果与成本；不过现有证据仅覆盖特定编码评测，仍需观察其在更多任务上的稳定性。
   - 来源: [@artificialanlys](https://x.com/ArtificialAnlys/status/2115477376981508419)

**Agility Robotics 邀请教育与劳动力委员会成员参观 RoboFab 工厂**
- Agility Robotics 表示，EdWorkforceCmte 的多数成员参观了其位于俄勒冈州塞勒姆的 RoboFab 工厂，实地了解人形机器人 Digit 的制造过程。双方讨论了机器人工程、客户使用 Digit 应对劳动力挑战的方式，以及支持美国机器人产业所需的教育与劳动力发展。
  > 💡 此次参观将 Digit 的产品制造、客户应用和人才发展置于同一讨论框架，有助于 Agility Robotics 强化产业合作与公众认知，但未披露新的订单或量产数据。
   - 来源: [@agilityrobotics](https://x.com/agilityrobotics/status/2115526516947956133)

### 算力追踪
**Microsoft 营收增长回升：Azure 加速，数据中心投入压制现金流**
- Microsoft 9 月季度营收同比增长 19%，达到 923 亿美元，较第二季度的增速提高 1 个百分点。Azure 云业务销售加速，部分由向 OpenAI 出租服务器的收入推动，抵消了 Xbox 和设备业务营收的小幅下降。Microsoft 表示，与 OpenAI 相关的营收占整体营收近 11%。
  > 💡 Azure 增长与 OpenAI 相关收入共同支撑 Microsoft 的营收表现，但数据中心投入仍对现金流形成压力。
   - 来源: [The Information](https://www.theinformation.com/briefings/microsoft-revenue-growth-accelerates-slightly-data-centers-dampen-cash-flows)

**Oracle 设定数据中心资本开支峰值期：股价单日涨逾 10%**
- Oracle 股价周三上涨超过 10%，此前公司给出了放缓数据中心资本开支并重新产生现金流的计划时间表。Oracle 将 2028 财年和 2029 财年的资本开支描述为“资本开支高峰期”。
  > 💡 市场对 Oracle 给出资本开支退坡与现金流改善的时间表作出积极反应，显示投资者正关注其高投入后的财务回报路径。
   - 来源: [The Information](https://www.theinformation.com/briefings/oracle-surges-10-caps-capex-projects-positive-cash-flow)

**美国拟向 Constellation 核电站提供 50 亿美元贷款：新增 1.1GW 容量支撑数据中心**
- 特朗普政府将向 Constellation Energy 提供 50 亿美元政府贷款，用于扩建八座核电站的发电容量，新增规模为 1.1GW。七座设施新增电力中的大部分或全部已被 Google、Amazon 和 Meta 订购。Constellation 表示，将利用融资提升 11 台现有反应堆的容量，并计划投入超过 70 亿美元，为 Google、Amazon 和 Meta 增加 1,080MW 核能容量；贷款承诺尚未最终敲定。
  > 💡 这项融资把数据中心电力需求与核电扩容直接绑定，有望降低相关项目的融资成本，但其对居民电价的实际影响尚未得到证实。
   - 来源: [TechCrunch](https://techcrunch.com/2026/10/28/trump-doe-loans-5b-to-nuclear-plants-that-will-power-data-centers)

### 初创&融资
**自动化工厂初创 Foundry 完成 1 亿美元 A 轮融资，以物理 AI 机器人重构产线**
- Foundry 向 The Information 表示，公司已完成总额 1 亿美元的新一轮融资。该轮 A 轮融资由 Marlinspike Partners 领投，Foundry 种子轮领投方 Khosla Ventures 参与。Foundry 成立不足一年，正围绕由 AI 模型驱动的机器人设计自动化工厂，让机器人以布线、紧固和精确放置等工作单元组织任务，而非适配既有生产线中的特定产品。
  > 💡 Foundry 的差异化不在于给现有产线加装机器人，而在于以物理 AI 和通用工作单元从流程底层设计制造体系；不过融资仍处于早期阶段，商业化效果需要后续订单和产能数据验证。
   - 来源: [The Information](https://www.theinformation.com/articles/foundry-raises-100-million-autonomous-factories)

**具身智能初创完成 1 亿美元融资，估值约 200 亿美元且尚无营收**
- 据量子位报道，一家具身智能领域初创公司完成 1 亿美元融资，估值达到约 200 亿美元。公司目前营收为零。报道提到该团队由斯坦福和伯克利相关研究者组建，并获得贝索斯与红杉等投资方支持。
  > 💡 零营收对应 200 亿美元估值，反映资本对具身智能平台型团队的未来预期，而非当前经营结果；在缺少产品交付、收入和融资轮次细节的情况下，投资回报仍高度依赖商业化进度。
   - 来源: [量子位](https://www.qbitai.com/2026/10/506042.html)

**三维存算一体芯片企业微纳核芯完成 10 亿元人民币 C+ 轮融资**
- 微纳核芯获得 10 亿元人民币 C+ 轮融资，由建投投资领投，领阳基金、国投泰康、盛堃投资、财金投资、晓池资本、凯泰资本和杭州资本参投。公司首创三维存算一体 3D-CIM™ 芯片技术体系，面向 AI 手机、AI PC、IoT、一体机、服务器及机器人等大模型推理应用提供芯片方案。
  > 💡 这笔融资将强化微纳核芯在存算一体芯片与端侧、边缘及服务器推理市场中的资金支撑，其技术能否转化为规模化产品仍取决于后续商业落地。
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14706711)

### 研究关注
**Timestral：四款时间序列基础模型登顶 GIFT-Eval、TIME 与 fev-bench**
- 论文提出 Timestral，一组面向概率预测的时间序列基础模型，包含 5M、28M、123M 和 209M 四种参数规模。Timestral-209M 与 Timestral-123M 在 GIFT-Eval、TIME 和 fev-bench 的各项指标中位居前两名，其方法包括解耦预测视野、协变量框架以及先使用合成语料预训练、再混合真实与合成数据后训练的两阶段流程。四款模型的权重已在 Hugging Face 提供，推理代码已在 GitHub 提供。
  > 💡 Timestral 以较小参数规模在多个时间序列预测基准中取得领先结果，同时开放权重与推理代码，为概率预测研究和实际应用提供了可复用的模型基础。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.37585)

**MPO：以轮次为尺度分配信用，长程智能体在多类任务上优于强 RL 基线**
- 论文针对长程 LLM 智能体提出多尺度策略优化方法 MPO，将多尺度优势估计与轮次级重要性采样结合，在轮次尺度上协调信用分配和策略更新。基于 4B 和 30B-A3B 模型在搜索、工具使用及自动化任务上的大量实验显示，MPO 相较强强化学习基线取得持续提升。
  > 💡 MPO 将长程智能体的优化粒度从单个动作令牌扩展到完整交互轮次，展示了更细粒度信用分配对长链路任务训练的潜力。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.35013)

**PDRVLA：融合物理动态表征，四个仿真基准最高成功率 99.3%**
- 论文提出 PDRVLA，通过轻量级物理动态模块从视觉语言特征中提取物理令牌，为动作生成提供条件，而无需在线生成未来视频。该模块通过直接预测未来 RGB、深度和光流特征进行学习，并使用冻结的预训练视频世界模型提供辅助监督，训练数据全部来自公开数据及人机数据合成、子任务标注和具身思维链标注。PDRVLA 在 LIBERO、LIBERO-Plus、RoboTwin 2.0 和 SimplerEnv 上的成功率分别为 99.3%、89.9%、93.6% 和 81.5%。
  > 💡 PDRVLA 避免在机器人控制环路中在线生成未来视频，并以物理动态表征改善动作生成，为降低世界模型类方法的实时控制延迟提供了可行路径。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.37381)


---
*更新时间: 2026-10-29 17:21*