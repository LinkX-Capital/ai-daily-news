## 06月03日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：Together AI解析MiniMax-M3高效推理方案：支持百万Token上下文
- 产业动态：OpenAI发布Codex六款职业插件：数据分析师、创意制作、销售等; NVIDIA解析金融机构的交易基础模型趋势; Microsoft Build大会发布自研AI模型、OpenClaw风格Agent及Scout个人助手; Salesforce收购Contentful加码AI内容管理; Anthropic扩展Glasswing安全项目至15国150个组织
- 算力追踪：SK海力士计划五年内将内存芯片产能翻倍应对AI需求; Alphabet计划融资800亿美元用于AI基础设施; OpenAI拟公开跨芯片推理工具削弱NVIDIA软件优势
- 初创&融资：AULONG获500万美元A轮融资：金融AI Agent基础设施; ZeroDrift获1000万美元融资：AI模型合规服务; 橡木果机器人走出隐身：9名清华博士创办，主打零数据本能驱动
- 研究关注：UniLab：CPU模拟+GPU训练异构架构，训练效率提升3-10倍; τ₀-WM：统一视频-动作世界模型，27,300小时真实机器人数据; DataMaster：自主数据工程Agent，MLE-Bench奖牌率提升32%; TASTE：反转任务构建流程，Agent基准难度翻倍; Demo2Reward：VLM奖励模型的测试时Prompt优化; 具身认知：Sutton等论证感知应是主动行动而非被动处理
- X讨论：Google DeepMind开放Co-Scientist：AI科研助手面向个人研究者; SemiAnalysis分析：Cerebras晶圆级芯片的扩张困境与出路; 超大规模厂商密集推出GPU/XPU/CPU芯片，服务器设计趋向多元化

---

## 📖 详细参考

### 模型前沿
**Together AI解析MiniMax-M3高效推理方案：支持百万Token上下文**
- Together AI发文解析如何高效服务MiniMax-M3模型，采用KV-block-major稀疏注意力、分页MSA解码和Rust多模态调度器，实现百万Token上下文和多模态支持。MiniMax官方在联合直播中补充：MSA（MiniMax Sparse Attention）与CSA/HCA不同，保留未压缩的KV缓存并做block级top-K选择，使注意力内核占per-decode时间从上一代的**~30%降至~5%**。M3不仅限于编码，还支持原生多模态输入（图像+视频）、长程Agentic任务甚至桌面操作，并具备视觉编码自评估能力。
  > 💡 Together的稀疏注意力方案若成熟，将为长上下文推理提供更低的算力成本。
   - 来源: [Together AI Blog](https://www.together.ai/blog/serving-minimax-m3-for-efficient-inference-unlocking-1m-token-context-and-multimodality-without-regrets) | [@MiniMax_AI](https://x.com/MiniMax_AI/status/2061944204604101020)

### 产业动态
**OpenAI发布Codex六款职业插件：数据分析师、创意制作、销售等**
- OpenAI发布六款面向特定职业的Codex插件，覆盖**数据分析、创意制作、销售、产品设计、股权投资和投资银行**领域。每款插件在Codex应用内整合了对应工作流所需的集成、指令和上下文信息，使Codex能近似扮演特定岗位角色。其中数据分析插件可将数据直接转化为答案，支持查询、可视化和统计分析。OpenAI同时发布了官方博文详解每款插件的设计思路。OpenAI高级副总裁Sachin Katti透露，公司计划**将Codex与ChatGPT合并**，并宣布了新的企业工具。
  > 💡 Codex插件从通用工具转向职业细分，OpenAI正在将AI能力包装为可嵌入现有工作流的SaaS产品。
   - 来源: [OpenAI Blog](https://openai.com/index/codex-for-every-role-tool-workflow) | [TechCrunch](https://techcrunch.com/2026/06/02/openai-launches-new-codex-tools-for-white-collar-work/) | [The Information](https://www.theinformation.com/briefings/openai-says-will-combine-codex-chatgpt-soon-announces-business-tools) | [@openai](https://x.com/OpenAI/status/2061887715520721151#m)

**NVIDIA解析金融机构的交易基础模型趋势**
- NVIDIA发文指出，金融机构正从分散的欺诈、信用、推荐模型转向统一的交易基础模型（Transaction Foundation Models）。**Mastercard**结合NVIDIA NeMo AutoModel和Databricks开发交易基础模型；**Revolut**使用NVIDIA技术实现欺诈检测精度提高**20%**，交叉销售准确率提升**9.6%**；**Adyen**部署交易基础模型处理支付额达**1万亿美元**，推理速度提升**195倍**。
  > 💡 事务基础模型若成主流，将为金融AI提供更低的定制成本和更高的推理一致性。
   - 来源: [NVIDIA Blog](https://blogs.nvidia.com/blog/financial-institutions-transaction-foundation-models/)

**Microsoft Build大会：发布自研AI模型、OpenClaw风格Agent及Scout个人助手**
- Microsoft在Build大会上发布面向开发者和企业客户的新AI软件，包括自研AI模型和OpenClaw风格的Agent工具，允许企业客户利用内部数据自动化工作流任务。同时发布**Scout**——一款**always-on个人Agent**，深度集成到Microsoft 365日常应用中（由Corporate VP Omar Shahine负责）。Scout基于OpenClaw技术构建，将OpenClaw的能力和灵活性带入Microsoft 365。此外还发布了**Work IQ APIs**，为企业提供组织知识图谱的API接口。
  > 💡 Microsoft将OpenClaw能力整合进365，Scout是前沿Agent能力产品化的首个信号，365用户基础将加速其规模化。
   - 来源: [Microsoft 365 Blog](https://www.microsoft.com/en-us/microsoft-365/blog/2026/06/02/introducing-microsoft-scout-your-always-on-personal-agent/) | [The Information](https://www.theinformation.com/briefings/microsoft-unveils-new-homegrown-ai-openclaw-inspired-agents-businesses) | [TechCrunch](https://techcrunch.com/2026/06/02/microsoft-launches-scout-an-openclaw-inspired-personal-assistant/)

**Salesforce收购Contentful：加码AI内容管理**
- Salesforce收购内容管理平台Contentful，作为其AI战略的最新布局。Contentful提供基于API的头部less CMS服务，被广泛用于企业数字化内容管理。
  > 💡 Contentful的结构化内容能力将为Salesforce的AI Agent提供更丰富的企业知识底座。
   - 来源: [The Information](https://www.theinformation.com/briefings/salesforce-acquires-contentful-latest-move-boost-ai)

**Anthropic扩展Glasswing安全项目至15国150个组织**
- Anthropic将其安全漏洞项目**Glasswing**和**Mythos**扩展至**15个国家的150个组织**，覆盖电力、水务、医疗和通信等关键基础设施领域，这些领域一旦遭受网络攻击可能影响**1亿人**。
  > 💡 Anthropic将安全能力从产品特性升级为公共服务，既是社会责任也是企业品牌战略。
   - 来源: [The Information](https://www.theinformation.com/briefings/anthropic-expands-glasswing-150-new-organizations) | [TechCrunch](https://techcrunch.com/2026/06/02/anthropic-scales-claude-mythos-to-critical-infrastructure-in-15-countries/)

### 算力追踪
**SK海力士计划五年内将内存芯片产能翻倍应对AI需求**
- 据Bloomberg报道，SK海力士计划在五年内将内存芯片产能翻倍，以应对AI驱动下的全球供应链紧张。扩产计划主要针对HBM等高带宽内存产品。董事长Chey Tae-won在台北表示，内存短缺可能持续到**2030年**。
  > 💡 HBM扩产将缓解AI训练侧的显存瓶颈，但也可能加剧与三星、镁光的产能竞争。
   - 来源: [The Information](https://www.theinformation.com/briefings/sk-hynix-double-capacity-ai-strains-memory-supply)

**Alphabet计划融资800亿美元用于AI基础设施**
- Alphabet宣布计划融资**800亿美元**用于AI基础设施扩建。公司声明称其AI解决方案和服务的企业和消费者需求"已超过公司可用供给"。融资部分也将用于支付员工股权税。
  > 💡 800亿美元的AI基建投入规模前所未有，反映巨头对算力瓶颈的紧迫感已超过资本市场的审慎。
   - 来源: [The Information](https://www.theinformation.com/briefings/google-raise-80-billion-ai-spending-employee-equity) | [TechCrunch](https://techcrunch.com/2026/06/01/alphabet-plans-to-raise-80-billion-to-pay-for-ai-buildout/)

**OpenAI拟公开跨芯片推理工具：削弱NVIDIA软件优势**
- OpenAI基础设施负责人Sachin Katti表示，公司对公开分享其自研的跨芯片AI推理软件持开放态度。该工具使AI模型能在不同芯片供应商的硬件上运行，有望削弱NVIDIA CUDA生态的软件锁定优势。
  > 💡 若OpenAI将跨芯片工具开源，将直接挑战NVIDIA在AI推理侧的软件护城河，加速硬件多元化。
   - 来源: [The Information](https://www.theinformation.com/articles/openai-release-internal-tool-weaken-nvidias-software-advantage)

### 初创&融资
**AULONG获500万美元A轮融资：金融AI Agent基础设施**
- 金融AI Agent基础设施服务商AULONG获得500万美元A轮融资，由Symbolic Capital和Khosla Ventures联合领投。AULONG选择金融场景切入，因其具备高频数据、复杂变量、明确风险边界等特征，适合训练执行型AI Agent。
  > 💡 AULONG选择金融作为Agent落地场景，体现了该领域对高精度执行型Agent的迫切需求。
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14698196)

**ZeroDrift获1000万美元融资：AI模型合规服务**
- ZeroDrift获得**1000万美元**融资，提供AI合规中间层服务，部署在AI模型与终端用户之间，实时标记并替换可能存在合规问题的消息内容。
  > 💡 AI合规中间层是模型安全赛道的新切入点，随着监管收紧，企业对"模型自我防护"的需求将快速增长。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/02/zerodrift-raises-10-million-to-protect-ai-models-from-themselves/)

**橡木果机器人走出隐身：9名清华博士创办，主打零数据本能驱动**
- 橡木果机器人由哈佛归国博士姜峣于2018年发起，9名清华博士团队，区别于数据驱动的传统范式，主打让机器人依靠「本能」完成任务，核心判断为语言和操作是两种完全不同的智能。
  > 💡 「本能」驱动与数据驱动形成互补，在数据稀缺的物理操作场景具有差异化潜力。
   - 来源: [DeepTech深科技](http://mp.weixin.qq.com/s?__biz=MzA3NTIyODUzNA==&mid=2649797703&idx=1&sn=7b0774e77f73313d1dc77cdaa0e5bdf9&chksm=86554a416625fc0c975aee1e7ebd2dd07bd3dea8de86bf2d446af5318c9b3729581a2c9050fc&scene=0&xtrack=1#rd)

### 研究关注
**UniLab：CPU模拟+GPU训练异构架构，机器人RL训练效率提升3-10倍**
- 当前机器人RL训练普遍采用GPU-resident方案（物理模拟、rollout、学习都在GPU上），UniLab提出将CPU并行模拟与GPU策略更新解耦的异构架构，通过统一运行时管理数据搬运和同步。在代表性机器人控制任务上**端到端效率提升3-10倍**，且减少对NVIDIA CUDA依赖，支持macOS/AMD ROCm/Intel XPU后端。
  > 💡 GPU模拟是高效训练的有效路径但非唯一路径，打破CUDA锁定对机器人RL社区意义重大。
   - 来源: [arXiv](https://arxiv.org/abs/2605.30313) | [量子位](https://www.qbitai.com/2026/06/427729.html)

**τ₀-WM：统一视频-动作世界模型，27,300小时真实机器人数据训练**
- 机器人操作需要模型在执行前就能预判和评估动作后果。τ₀-WM基于共享视频扩散骨干，同时提供视频动作模型（预测未来视觉+连续动作块）和动作条件视频模拟器（推演候选动作并打分），推理时通过采样+重去噪一致性筛选+模拟器修正的测试时计算策略选最优动作。训练数据约**27,300小时**真实机器人遥操作和失败轨迹，在长程精细操作任务上超越基线。
  > 💡 将"想象-评估-执行"统一为单一框架，为机器人长程操作提供了新的推理范式。
   - 来源: [arXiv](https://arxiv.org/abs/2606.01027)

**DataMaster：自主数据工程Agent，MLE-Bench奖牌率提升32%**
- 数据工程仍高度依赖人工试错，DataMaster让Agent自主完成外部数据发现、选择、清洗和组合，同时保持学习算法不变。通过树状搜索组织不同数据工程分支、共享数据池复用已发现数据源、全局记忆跨分支传递经验。在**MLE-Bench Lite奖牌率提升32.27%**，PostTrainBench GPQA得分**31.02% vs 基线30.35%**。
  > 💡 数据工程从手动流程变为自主搜索，有望成为AutoML之后的新范式。
   - 来源: [arXiv](https://arxiv.org/abs/2605.10906) | [机器之心](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651036359&idx=3&sn=4a37dcabcf03195ad573d1aa43e29555&chksm=857ba6525f47796fc16e795dc44710c8e64c4a36bd33be5a0d6e794b2a587c5c7c806ce051bd&scene=0&xtrack=1#rd)

**TASTE：反转任务构建流程，Agent基准难度翻倍且工具组合覆盖超2倍**
- 现有Agent基准（如τ²-Bench）已趋于饱和，高分可能反映的是基准不足而非Agent真实能力。TASTE反转传统任务构建流程：先用自适应对比n-gram模型采样有效工具序列，再通过聚类选取代表性序列、实例化为完整任务、迭代难度演化。基于此构建的τ^c-Bench上，**11个Agent/LLM对性能大幅下降**（如Gemini-3-Flash从0.82-0.94降至0.28-0.61），且工具组合数量**超过τ²-Bench的两倍**。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2605.28556)

**Demo2Reward：VLM奖励模型的测试时Prompt优化，无需额外训练**
- 获取高质量奖励信号是RL的核心瓶颈。Demo2Reward仅需3-10条专家演示轨迹，在测试时自动调整Prompt优化VLM奖励模型，无需重新训练。在模拟机器人任务和多种策略骨架上**始终优于零样本和少样本VLM奖励模型**，有效减少误报同时保留正报。
  > 💡 测试时Prompt优化为RL数据稀缺困境提供了低成本解法。
   - 来源: [arXiv](https://arxiv.org/abs/2606.00083)

**具身认知：Sutton等论证感知应是主动行动而非被动处理，主流AI范式忽视了感知与行动的不可分性**
- 从规则系统到LLM，主流AI都将认知视为内部处理过程——大脑接收感官输入、处理后发出指令。该论文从具身认知视角出发，认为感知应是主动的、技能性的世界参与，Agent通过行动和行动塑造经验的方式来感知。论文提出体验、行动-感知不可分性、自主性和具身化四个核心概念，指出RL虽在行动、Agent-环境交互、反馈驱动适应上与具身认知有结构共鸣，但关键要素仍然缺失或发育不足。
  > 💡 为突破"感知-处理-输出"范式提供了理论框架，具身认知可能是下一代AI的重要方向。
   - 来源: [arXiv](https://arxiv.org/abs/2605.24238v1) | [机器之心](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651036359&idx=2&sn=216de3faa9f2b86de3bf762aad6709ba&chksm=85cee313a988175fb1a0ee44bb70fed3406917fed6e4f20c01b14ffb8a2058116f969d2536c4&scene=0&xtrack=1#rd)

### X讨论
**Google DeepMind开放Co-Scientist：AI科研助手面向个人研究者**
- Google DeepMind宣布将Co-Scientist工具向个人研究者开放，支持思路构思、文献检索、数值计算、定理证明和理论体系搭建。平台具备异步有状态工作空间，可记录研究过程。初步实测中，AI协作数学家在前沿数学四级难度题库中正确率达到**48%**。
  > 💡 Co-Scientist若能显著缩短科研周期，将在学术和药物发现领域形成差异化竞争力。
   - 来源: [@googledeepmind](https://x.com/GoogleDeepMind/status/2061857539977842793#m)

**SemiAnalysis分析：Cerebras晶圆级芯片的扩张困境与出路**
- SemiAnalysis分析指出，Cerebras的46,225mm²晶圆级芯片（**台积电5nm工艺，4万亿晶体管**）面临制造良率瓶颈。其解决方案是在晶圆上键合第二片晶圆实现扩展，但这引入了新的大规模封装挑战，生产成本高昂限制了市场竞争力。
  > 💡 晶圆级芯片在理论算力上领先，但封装良率问题可能限制其大规模商业化进程。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2061915957337923748#m)

**超大规模厂商密集推出GPU/XPU/CPU芯片，服务器设计趋向多元化**
- 主要超大规模厂商正密集推出多种GPU、XPU和CPU芯片，推动服务器机架和板级设计多元化，以满足不同客户需求。NVIDIA、AMD、Intel等芯片厂商在**过去一年**内相继发布新一代AI训练和推理芯片，包括NVIDIA H100、H200系列，AMD MI300X系列，以及Intel Gaudi系列。超大规模云服务商如Microsoft、Amazon、Google在自研芯片上的投入显著增加，推动数据中心服务器设计从传统单一形态向多形态、多元化方向演进。分析指出，芯片密集更新与服务器设计多元化趋势反映了AI工作负载的多样性及客户定制化需求的增长。
  > 💡 芯片多元化将打破NVIDIA在AI训练硬件的垄断格局，但也增加了系统集成的复杂度。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2061855674561110121#m)

---
*更新时间: 2026-06-03 10:30*