## 04月09日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

#要点汇总#

- 模型前沿：神秘模型HappyHorse匿名登顶AI Video Arena后消失，身世成谜; World Labs发布Marble和Haven模型更新; Meta发布Muse Spark模型，Artificial Analysis智商指数52位列全球第四
- 产业动态：Tubi成为首个集成于ChatGPT的流媒体应用; Anthropic发布Managed Agents工程博客; Perplexity ARR突破5亿美元; TokenMaxxers为AI编程构建代码管理工具
- 算力追踪：Qwen3.6-Plus登顶OpenRouter三榜第一
- 初创&融资：Canva收购Simtheory和Ortto强化AI代理与营销自动化能力; 具身智能机器人公司Zerith零次方获超亿元A轮融资; 面壁智能开源2B语音模型，Q1融资超10亿元
- 研究关注：Google Research发布PaperVizAgent和ScholarPeer两个AI学术Agent; Meta研究员Jason Weston提出Thinking Mid-training新训练范式; 港中文/蚂蚁ICLR 2026论文揭示音频大模型"音频贡献缺失"现象并提出后训练新范式
- X讨论：Anthropic发布Claude Mythos Preview系统卡片，高于Opus的新模型层级，因网络安全能力过强不公开发布

---

## 📖 详细参考

### 模型前沿
**神秘模型HappyHorse匿名登顶AI Video Arena后消失，身世引发技术圈热议**
- 4月初，一个名为HappyHorse-1.0的神秘AI视频模型悄然出现在Artificial Analysis Video Arena盲测排行榜，**以Elo 1333超越Seedance 2.0（1273）登顶文生视频，Elo 1392登顶图生视频**，超越Kling 3.0、PixVerse V6等主流闭源模型。该模型采用40层单流Self-Attention Transformer，15B参数，支持文本/视频/音频三模态联合建模，仅需8步去噪。数日后V1/V2均从排行榜撤下。关于其身世，技术圈存在两种主流猜测：**一说背后团队是张迪领衔的阿里淘天集团未来生活实验室**——张迪是前快手副总裁、可灵AI技术负责人，2025年底加入阿里，主导成立仅一年的未来生活实验室已在国际顶会发表十余篇论文；**另一说是Sand.ai基于3月23日开源的daVinci-MagiHuman（Sand.ai与上海创智学院GAIR实验室联合开发，负责人分别为曹越和刘鹏飞）的优化迭代版本**，目的是验证模型在真实用户偏好下的表现上限。无论真相如何，**这是开源视频模型首次在真实用户盲测中匹敌顶级闭源模型**，视频生成的开源-闭源差距正在快速收窄。
  > 💡 "匿名登顶→引发猜测→悄然消失"已成新玩法，视频模型赛道进入"鲶鱼"频出阶段
   - 来源: [36氪](https://eu.36kr.com/en/p/3757826958635781)

**World Labs发布Marble和Haven模型更新**
- World Labs发布两项模型更新：Marble 1.1提升光照和对比度，显著减少视觉伪影；Haven模型同步更新。
  > 💡 AI视觉生成能力持续进化，细节处理成竞争焦点
   - 来源: [@theworldlabs](https://x.com/theworldlabs/status/2041554646561677701#m)

**Meta发布Muse Spark模型：Artificial Analysis智商指数52，位列全球第四**
- Meta推出Muse Spark，这是其Superintelligence Labs发布的首个模型，由Alexandr Wang领导。Muse Spark在Artificial Analysis Intelligence Index上得分52，仅次于Gemini 3.1 Pro、GPT-5.4和Claude Opus。
  > 💡 Meta强调正在"可预测且高效的扩展轨迹"上，后续将通过并行Agent协作在不显著增加延迟的前提下增加测试时推理。
   - 来源: [TechCrunch](https://techcrunch.com/2026/04/08/meta-debuts-the-muse-spark-model-in-a-ground-up-overhaul-of-its-ai/)

### 产业动态
**Tubi成为首个集成于ChatGPT的流媒体应用**
- 免费流媒体平台Tubi成为首个在ChatGPT中推出原生应用集成的流媒体服务，用户可通过ChatGPT直接访问Tubi内容。这是流媒体与AI平台深度融合的里程碑。
  > 💡 AI平台成为内容分发新渠道，流媒体争相抢占ChatGPT流量入口
   - 来源: [TechCrunch](https://techcrunch.com/2026/04/08/tubi-is-the-first-streamer-to-launch-a-native-app-within-chatgpt/)

**OpenAI公布企业AI下一阶段发展规划**
- OpenAI概述了企业AI的下一阶段发展，随着Frontier、ChatGPT Enterprise、Codex等产品的采用加速，各行业的企业AI应用正在扩展。
  > 💡 企业AI市场进入规模化落地阶段，竞争焦点转向垂直场景渗透
   - 来源: [OpenAI News](https://openai.com/index/next-phase-of-enterprise-ai)

**Anthropic发布Managed Agents工程博客，解决长时运行Agent托管难题**
- Anthropic工程博客发文介绍Managed Agents托管服务，探讨如何为长时间运行的AI Agent设计可靠的调度和状态管理系统。**随着Agent应用从单次对话转向长时运行任务，Agent基础设施的可靠性成为关键挑战**。
  > 💡 Agent从Demo走向生产的核心瓶颈是运行稳定性，托管层需求正在浮现
   - 来源: [@anthropicai](https://x.com/AnthropicAI/status/2041929199976640948#m)

**HuggingFace发布ALTLK-Evolve研究聚焦AI Agent在职学习**
- HuggingFace博客介绍了ALTLK-Evolve研究，聚焦AI Agent在实际工作中的持续学习和能力提升。
  > 💡 Agent能力从预训练向持续学习演进，在岗学习成重要方向
   - 来源: [HuggingFace Blog](https://huggingface.co/blog/ibm-research/altk-evolve)

**Perplexity ARR突破5亿美元，AI搜索商业化加速**
- Perplexity的年经常性收入（ARR）已达到5亿美元，相比去年大幅增长。作为AI搜索领域的头部公司，Perplexity通过企业订阅和API服务持续扩张收入。**这一数字表明AI搜索赛道正在从概念验证进入规模化变现阶段**，与Google搜索和传统搜索引擎的竞争将更加直接。
  > 💡 AI搜索不再是小众实验，ARR增速超预期，对传统搜索格局的冲击加速
   - 来源: [The Information](https://www.theinformation.com/briefings/perplexitys-arr-rises-500-million)

**TokenMaxxers：为"Token最大化者"构建代码管理软件的初创公司**
- 一家名为TokenMaxxers的初创公司正在为AI编程场景中的"Token最大化"用户群体开发代码管理工具。随着AI辅助编程的普及，**如何高效管理和优化代码库中的Token使用量成为新需求**，这催生了围绕AI编程工作流的基础设施级创业机会。
  > 💡 AI编程工具链正在催生新的开发者基础设施品类，Token管理可能成为标配能力
   - 来源: [The Information](https://www.theinformation.com/articles/startup-building-code-management-software-tokenmaxxers)

### 算力追踪
**Qwen3.6-Plus登顶OpenRouter三榜第一，免费试用结束转正式上线**
- Alibaba Qwen的Qwen3.6-Plus模型包揽OpenRouter每日、每周和趋势三个排行榜第一。该模型免费试用已结束，正式上线生产环境，OpenRouter上可享35%折扣。**国产模型在海外API平台的市场竞争力正在快速验证**。
  > 💡 Qwen3.6-Plus以性价比+性能组合拳抢占开发者生态，与GLM-5.1同日发力
   - 来源: [@alibaba_qwen](https://x.com/Alibaba_Qwen/status/2041871541080924477#m)

### 初创&融资
**Canva收购Simtheory和Ortto强化AI代理与营销自动化能力**
- Canva宣布收购Simtheory和Ortto两家公司，增强在AI代理、数据基础设施、营销自动化和客户互动方面的能力。这两项收购将使Canva在设计平台基础上进一步扩展到企业营销技术领域。
  > 💡 Canva正从设计工具向企业营销平台转型，AI代理能力将成为差异化竞争关键
   - 来源: [TechCrunch](https://techcrunch.com/2026/04/08/canva-doubles-down-on-ai-and-marketing-automation-with-simtheory-ortto-acquisitions/)

**具身智能机器人公司Zerith零次方获超亿元A轮融资**
- Zerith零次方是一家具身智能人形机器人研发商，近期完成超亿元A轮融资，由国内算力龙头润泽集团领投，宁波东力、创业接力、平湖泽新跟投。
  > 💡 具身智能人形机器人赛道持续受资本关注，算力龙头布局终端硬件
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14695432)

**面壁智能开源2B语音模型成功复现京剧贯口，Q1融资超10亿元**
- 面壁智能发布2B参数开源语音模型，成功复现郭德纲《莽撞人》最难贯口，引发海外关注。该公司Q1融资超10亿元，在端侧语音模型赛道密集布局。**2B参数实现高质量语音合成，说明小模型在特定任务上已具备实用价值**，开源策略有助于快速构建生态。
  > 💡 端侧语音模型成新战场，融资密集期开启语音交互新范式
   - 来源: [量子位](https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247881487&idx=1&sn=faf399aa06b8fb64a89ef3d9a2de297d) / [新智元](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA==&mid=2652690418&idx=1&sn=7c5e4d3ddcd64a77ef7200e98de9415a)

### 研究关注
**ICLR 2026论文揭示音频模态对大模型性能的关键作用并提出后训练新范式**
- 港中文与蚂蚁集团联合发表ICLR 2026论文，构建了迄今规模最大、质量最高的音频理解选择题数据集AudioMCQ。论文深入分析了音频-语言大模型中音频贡献对模型性能的关键作用，发现音频模态在传统训练流程中未被充分利用。论文提出针对音频的后训练新范式，通过精细化的音频建模突破多模态模型性能瓶颈。**这表明多模态模型的短板不在语言理解，而在音频等非文本模态的训练策略**。
  > 💡 当前音频大模型可能只是在"读题"而非"听音频"
   - 来源: [PaperWeekly](https://mp.weixin.qq.com/s?__biz=MzIwMTc4ODE0Mw==&mid=2247719344&idx=2&sn=a55cef66038c148c220f9e5d1053e9fe)

**Google Research发布PaperVizAgent和ScholarPeer两个AI学术Agent**
- Google Research发布两个面向学术研究的多Agent框架：PaperVizAgent用于从论文文本自动生成出版级学术插图，ScholarPeer用于自动化同行评审。PaperVizAgent通过五Agent协作（检索、规划、风格、可视化、批评）迭代优化，**综合得分60.2超过人类基线50.0**，是唯一超越人类水准的框架。ScholarPeer通过双流架构（领域叙事+主动验证）生成文献依据充分的评审，显著缩小了AI评审与人类评审的差距。**这意味着AI正在从"研究对象"转变为学术工作流的核心参与者**。
  > 💡 AI Agent深度嵌入学术发表流程，论文制图和审稿两大痛点同时被攻破
   - 来源: [Google Research Blog](https://research.google/blog/improving-the-academic-workflow-introducing-two-ai-agents-for-better-figures-and-peer-review/)

**Meta研究员Jason Weston提出"Thinking Mid-training"新训练范式**
- Meta研究员Jason Weston发表论文"Thinking Mid-training: RL of Interleaved Reasoning"，探索在预训练和后训练之间引入显式推理训练的新范式。**该工作试图弥合预训练（无显式推理）与后训练（推理密集）之间的鸿沟**，通过交错推理的强化学习提升模型推理能力。
  > 💡 推理能力不必等到后训练阶段注入，中期训练可能是更高效的路径
   - 来源: [@jaseweston](https://x.com/jaseweston/status/2041864833214095484#m)

### X讨论
**Anthropic发布Claude Mythos Preview系统卡片：高于Opus的新模型层级，因网络安全能力过强不公开发布**
- Anthropic发布244页系统卡片，公布Claude Mythos Preview详情。**Mythos是高于Opus的全新模型层级**，内部代号"Capybara"，性能提升是之前趋势线的4.3倍。SWE-bench Verified 93.9%（Opus 4.6为80.8%），Cybench 100%通过率（史上首次），USAMO 2026数学证明97.6%。定价$25/$125（Opus 4.6的5倍），**不公开发布，仅提供给Amazon、Apple、Microsoft、Cisco等12家合作伙伴用于防御性网络安全工作**。
  > 💡 AI模型首次因"能力太强"而被主动限制发布，网络安全成为AI能力的红色警戒线
   - 来源: [@anthropicai](https://x.com/AnthropicAI/status/2041580670774923517#m)


---
*更新时间: 2026-04-09 08:30*