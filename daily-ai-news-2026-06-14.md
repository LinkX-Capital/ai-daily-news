## 06月14日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：智谱全量开放GLM-5.2，支持1M上下文
- 产业动态：OpenRouter推出Fusion模型融合功能，Fable 5+GPT-5.5组合在DRACO基准超越所有单模型; Google发布Gemini-SQL2：基于Gemini 3.1 Pro的text-to-SQL能力，BIRD单模型榜达80.04%
- 研究关注：港中文提出全光信号处理芯片，无需光电转换实现吞吐量1.6 Tbps、延迟仅60ps; MiniMax提出稀疏注意力MSA：1M上下文注意力计算量降低28.4倍，H800上decoding加速7.6倍; MaxProof：MiniMax-M3系列种群级测试时规模化，IMO 2025达35/42超金牌线; SR²AM：用RL让Agent学会推理自我调节，8B模型性能匹敌百倍参数系统
- X讨论：里约热内卢发布开源模型Rio 3.5 Open 397B：基于Qwen 3.5后训练，引入SwiReasoning动态推理

---

## 📖 详细参考

### 模型前沿
**智谱全量开放GLM-5.2，支持1M上下文**
- GLM-5.2是智谱迄今能力最强的开源模型，支持**真正可用的1M上下文**，在长程任务独立完成能力上持续领先，定位为最强的国产Coding模型。已面向GLM Coding Plan全量用户开放。在前沿模型突然受限的背景下，智谱选择全面开源作为回应，唐杰将策略定义为"radical openness"。官方公告未提及具体benchmark数据。
  > 💡 在部分前沿模型（如Claude系列）面临访问限制的窗口期，智谱选择MIT协议全权重开源+Coding Plan铺量，时机精准地争夺因受限而迁移的开发者群体。
   - 来源: [@jietang](https://x.com/jietang/status/2065784751345287314) | [智谱官方](https://mp.weixin.qq.com/s/LDrbtLM0wiCTJorvd5GY9w)

### 产业动态
**OpenRouter推出Fusion模型融合功能，Fable 5+GPT-5.5组合在DRACO基准超越所有单模型**
- OpenRouter上线Fusion功能，将同一prompt并行分发给一组panel模型（每个均启用web search），再由judge模型对各方回复做结构化分析（共识点、矛盾、盲区），最终由calling model生成综合答案。在Perplexity AI的DRACO深度研究基准（100个任务，覆盖学术、金融、法律、医疗等10个领域）上，**Fable 5 + GPT-5.5融合后得分69.0%**，超越所有单一模型，包括单独的Fable 5（**65.3%**）。一组budget面板（Gemini 3 Flash + Kimi K2.6 + DeepSeek V4 Pro）得分**64.7%**，在约50%成本下超越GPT-5.5（60.0%）和Opus 4.8（58.8%）。实验还发现Opus 4.8与自身融合即可从58.8%提升至**65.5%**（+6.7pp），说明synthesis步骤本身贡献了显著增益。API可通过单一slug `openrouter/fusion`调用，也可自定义panel和judge模型组合。
  > 💡 模型融合（model fusion）验证了"多样性即智能"——不同架构模型组合的增益不仅来自知识互补，更来自synthesis步骤对矛盾和盲区的结构化消除。budget面板以半价超越frontier单模型，可能改变推理成本结构的经济算盘。
   - 来源: [OpenRouter Blog](https://openrouter.ai/blog/announcements/fusion-beats-frontier/) | [@openrouter](https://x.com/OpenRouter/status/2065856871215329545#m)

**Google发布Gemini-SQL2：基于Gemini 3.1 Pro的text-to-SQL能力，BIRD单模型榜达80.04%**
- Gemini-SQL2是Google基于Gemini 3.1 Pro的text-to-SQL能力，将自然语言问题转化为可执行的SQL查询。在BIRD Text-to-SQL单模型榜单上达到**80.04%**执行准确率，衡量标准为SQL必须正确运行并返回正确结果。Google同时占据前两名（Gemini-SQL2和上一代Gemini-SQL），超过GPT-5.5-xhigh（~**72.5%**）和Claude Opus 4.6（~**70.1%**）。人类基线为**92.96%**，仍差**12.92分**。BIRD基准涵盖95个数据库、37个领域共12,751个问题-SQL对，要求处理脏值和外部知识。目前未公开API和技术报告。
  > 💡 text-to-SQL是GenAI落地企业数据分析的核心场景。Google在BIRD榜单包揽前两名，表明专门化能力在后训练阶段仍有显著提升空间——通用frontier模型在该任务上被专用能力拉开8-10分。
   - 来源: [@GoogleResearch](https://x.com/GoogleResearch/status/2065475343205740911) | [MarkTechPost](https://www.marktechpost.com/2026/06/12/google-releases-gemini-sql2-gemini-3-1-pro-text-to-sql-scores-80-04-on-bird-single-model-leaderboard/)

### 研究关注
**港中文提出全光信号处理芯片，无需光电转换实现吞吐量1.6 Tbps、延迟仅60ps**
- 当前高速光通信依赖电域DSP补偿信号失真，DSP的高功耗与延迟正成为数据中心互连瓶颈。该芯片无需光电转换即可在光域完成信号均衡——实现**1.6 Tbps**聚合吞吐量（8路WDM通道×100 GBaud），处理延迟仅**<60 ps**，能耗**67.5 fJ/bit**，WDM带宽窗口扩展**6.8倍**。核心技术为深度光学储备池计算架构。一作Benshan Wang，通讯作者Chaoran Huang（香港中文大学），发表于Science。
  > 💡 若全光互连方案进入商用，超大规模集群的GPU有效算力可能成倍提升，对H100/B200集群的部署经济性将产生直接影响，光子芯片产业链值得关注。
   - 来源: [Science](https://www.science.org/doi/10.1126/science.ady5344) | [DeepTech深科技](http://mp.weixin.qq.com/s?__biz=MzA3NTIyODUzNA==&mid=2649798495&idx=1&sn=a267f86b5a52aef001ecd7af8795bb66&chksm=865184f83c2c5ed2d114b2f6045a00ebf467df7a0a39eae3cfb2280d7c1931da2129feb83848&scene=0&xtrack=1#rd)

**MiniMax提出稀疏注意力MSA：1M上下文注意力计算量降低28.4倍，H800上decoding加速7.6倍**
- MiniMax Sparse Attention（MSA）基于GQA架构，通过轻量级Index Branch对KV块评分并选取Top-k子集，Main Branch仅对选中块执行精确注意力。在**109B参数**、原生多模态模型上，MSA与GQA性能持平，但在**1M上下文**下将单token注意力计算量降低**28.4倍**。配套自研kernel在H800上实现**14.2倍prefill加速**和**7.6倍decoding加速**。搭载MSA的生产级多模态模型MiniMax-M3（**427B**）已开源，推理kernel已开源至GitHub。
  > 💡 稀疏注意力是长上下文模型推理降本的核心路径。MSA在保持精度的前提下实现接近一个数量级的wall-clock加速，可能改变百万token级推理的成本结构。
   - 来源: [arXiv](https://arxiv.org/abs/2606.13392) | [HuggingFace Daily Papers](https://huggingface.co/papers/2606.13392)

**MaxProof：MiniMax-M3系列种群级测试时规模化，IMO 2025达35/42超金牌线**
- MaxProof基于MiniMax-M3系列，将证明生成、证明验证、批判条件证明修复三项能力训练至同一模型，使用低误报率的防御式生成验证器。测试时模型同时充当生成器、验证器、修复器和排序器，通过锦标赛选择在候选证明种群中搜索最优解。在IMO 2025达到**35/42**，在USAMO 2026达到**36/42**，**两项均超过人类金牌线**。
  > 💡 将测试时规模化与RL验证器结合是数学推理能力提升的热门方向，核心挑战在于验证器自身的可靠性与推理成本的平衡。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2606.13473)

**SR²AM：用RL让Agent学会推理自我调节，8B模型性能匹敌百倍参数系统**
- SR²AM针对Agent推理token浪费的问题，将决策分解为反应执行、模拟推理和自我调节三个层级，其中自我调节通过端到端RL优化——模型自主学会何时规划、规划多深，而非依赖外部路由器。一作Mingkai Deng（@mdeng34）强调regulation策略是涌现的而非预设。v0.1-**8B** Pass@1匹敌**120-355B**系统，v1.0-**30B**匹敌**685B-1T**系统，同时推理token减少**25.8-95.3%**。RL训练后规划深度增加**22.8%**，规划频率仅增加**2.0%**，模型学会"看得更远而非想得更频繁"。
  > 💡 当前Agent的推理token浪费严重（长CoT无可靠精度增益）。SR²AM通过显式分解规划与执行、用RL学习自我调节，展示了小模型+高效推理路线的潜力，直击推理成本痛点。
   - 来源: [arXiv](https://arxiv.org/abs/2605.22138) | [@mdeng34](https://x.com/mdeng34/status/2065598571144261787)

### X讨论
**Jeff Dean提议复用旧手机以缓解数据中心算力压力**
- Google首席科学家Jeff Dean发推指出，全球每年有数亿部功能完好的旧手机被丢弃。他提出复用这些旧手机用于AI推理计算的构想，以替代部分数据中心GPU需求。
  > 💡 边缘推理+旧硬件复用若可行，将挑战以NVIDIA H100/B200为核心的集中式算力供给模式，但移动端芯片的内存带宽和能效比能否匹配LLM推理仍是未验证问题。
   - 来源: [@jeffdean](https://x.com/JeffDean/status/2065649717573505188#m)

**里约热内卢发布开源模型Rio 3.5 Open 397B：基于Qwen 3.5后训练，引入SwiReasoning动态推理**
- 里约热内卢市政府IT公司IplanRIO基于Qwen 3.5 397B（MoE，**397B总参数/17B活跃**）后训练，发布Rio 3.5 Open 397B。核心创新为SwiReasoning框架——基于next-token分布的熵信号在显式链式思维与隐空间推理间动态切换，低置信度时进入隐空间探索多条路径，恢复后切回显式输出。模型专门针对隐空间推理效率做了后训练优化。相比基座，Terminal-Bench提升**+18.3**分，SWE-Bench Multilingual达**77.0**（同级最优），HMMT 2026提升**+6.0**。支持**1M上下文**，MIT协议开源。
  > 💡 主权AI需求正从国家级下沉至市级政府，中国开源基座（Qwen系列）成为多国地方政府低成本构建本地化模型的实际选择。SwiReasoning的training-free特性意味着任何开源模型均可集成，token效率优化正从训练侧扩展到推理框架侧。
   - 来源: [HuggingFace](https://huggingface.co/prefeitura-rio/Rio-3.5-Open-397B) | [@semianalysis_](https://x.com/SemiAnalysis_/status/2065894494935933191#m)

---
*更新时间: 2026-06-14 06:47*