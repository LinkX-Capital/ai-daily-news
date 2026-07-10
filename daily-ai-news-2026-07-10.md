## 07月10日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：Meta推出Muse Spark 1.1，面向Agentic任务的多模态推理模型; MosiAI开源MOSS-Transcribe-Diarize 0.9B端到端说话人标注转写模型
- 产业动态：OpenAI推出ChatGPT Work Agent，由GPT-5.6与Codex驱动; Cursor开发通用AI Agent对抗Anthropic Claude Cowork; PrismML称在iPhone上运行更大端侧AI模型; Google将披露广告中的AI生成内容
- 算力追踪：Musk承诺不切断Anthropic算力供应，xAI与Anthropic算力关系再生博弈; Meta新一代MTIA AI芯片计划9月投产
- 初创&融资：Ollama完成6500万美元B轮融资、月活开发者近900万; Lyzr用自家AI Agent完成1亿美元B轮融资; Mercor收购Deeptune，正洽谈200亿美元估值; Lovable洽谈3亿美元融资，估值或翻倍至132亿美元; Prime Intellect获1.3亿美元A轮融资，构建Open Superintelligence Stack; 巴黎AI语音初创Gradium获1亿美元种子轮融资，NVIDIA参投
- 研究关注：Jiacheng Miao等提出The Agentic Garden of Forking Paths揭示AI研究Agent分析偏差; Chen Tang等提出SciReasoner深度原生结构推理方法; Hongyu Qu等提出LaMem-VLA双潜在记忆框架; EdgeBench揭示智能体真实环境学习缩放规律
- X讨论：Sam Altman：5.6版本在性价比上对企业是巨大进步; Samaya发布FrontierFinance金融研究Agent长周期基准

---

## 📖 详细参考

### 模型前沿
**Meta推出Muse Spark 1.1，面向Agentic任务的多模态推理模型**
- Meta Superintelligence Labs推出Muse Spark 1.1，定位为面向Agentic任务的多模态推理模型，重点覆盖工具/计算机使用、编码、多模态理解与长上下文工作流。Meta同时开放Meta Model API公测，开发者可通过API调用Muse Spark 1.1；该模型也已进入Meta AI App和meta.ai的Thinking模式。官方还称，Meta内部开发者和研究人员已在日常使用Muse Spark 1.1，模型在Meta Internal Coding Bench上较Muse Spark提升，并被研究人员用于自动化模型开发与评估任务。
  > 💡 Meta从“内部AI工具链”走向对外模型API，意味着其不再只把强模型能力沉淀在自家产品和研究流程里，而是开始直接进入开发者模型基础设施竞争。
   - 来源: [Meta AI](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/), [@aiatmeta](https://x.com/AIatMeta/status/2075221102172016989#m)

**MosiAI开源MOSS-Transcribe-Diarize 0.9B，端到端生成带时间戳的说话人转写**
- MosiAI官方宣布开源MOSS-Transcribe-Diarize-0.9B，并称其采用端到端audio-to-structured-transcript范式，遵循Apache 2.0许可证，支持128k长上下文转写和最长约90分钟音频输入，可一次性输出说话人标签与时间戳。论文将该任务定义为Speaker-Attributed, Time-Stamped Transcription（SATS），并称模型还能覆盖说话人分离和声学事件标注等结构化转写结果。
  > 💡 多说话人长音频转写正在从“ASR+说话人分离”的流水线走向端到端统一模型，会议纪要、播客、客服质检等场景的工程链路有望进一步简化。
   - 来源: [@MosiAI_Official](https://x.com/MosiAI_Official/status/2075059157443756245), [@ModelScope2022](https://x.com/ModelScope2022/status/2075158135350694027), [ModelScope Papers](https://modelscope.ai/papers/2601.01554), [arXiv](https://arxiv.org/abs/2601.01554)

### 产业动态
**OpenAI推出ChatGPT Work Agent，由GPT-5.6与Codex驱动**
- OpenAI发布ChatGPT Work，定位为可在应用和文件中采取行动的智能体，能够从连接的工具和工作流中收集信息，生成表格、幻灯片、文档、Web应用和报告，并将复杂项目拆成步骤持续处理数小时。该能力由GPT-5.6提供支持，并内置Codex技术；网页端和移动端自2026-07-09起面向Pro、Enterprise、Edu开放，Plus和Business将在未来几天开放；桌面端的聊天、Work和Codex能力面向所有套餐开放，Codex应用将并入新的ChatGPT桌面应用。
  > 💡 OpenAI把Codex从代码工具进一步嵌入通用办公Agent，意味着ChatGPT正在从“回答问题的界面”变成“执行跨应用工作的工作台”，与Claude Cowork等企业Agent形成更直接竞争。
   - 来源: [OpenAI](https://openai.com/zh-Hans-CN/index/chatgpt-for-your-most-ambitious-work/), [@openai](https://x.com/OpenAI/status/2075274271845404744#m)

**Cursor开发通用AI Agent对抗Anthropic Claude Cowork**
- 据The Information报道，AI编程工具Cursor正在开发一款通用AI Agent，对标Anthropic的Claude Cowork等工具。知情人士称，该项目内部称为Sand，定位为通用个性化助手，是Cursor从代码编辑器向更广泛Agent产品扩展的一部分。相关工作在公司开始租用更多算力后推进，目前仍处于早期阶段。
  > 💡 Cursor从代码场景切入通用Agent是产品边界的自然延伸，但缺乏模型自研能力的Cursor在与Anthropic正面竞争时将高度依赖第三方模型供应。
   - 来源: [The Information](https://www.theinformation.com/articles/cursor-developing-ai-agent-compete-claude-cowork)

**PrismML称在iPhone上运行更大端侧AI模型**
- 端侧AI初创公司PrismML称已在iPhone上运行比以往移动端更大的AI模型；Apple也在探索将更强模型压缩到iPhone端侧运行，以降低云端推理成本并增强隐私。Yahoo Finance报道，相关模型为Alibaba开源Qwen 3.6、约270亿参数，可在iPhone 17 Pro本地运行；PrismML将模型从约54GB压缩至不足4GB，技术路线涉及1-bit和ternary权重架构。
  > 💡 这条目前只能作为端侧AI路线信号观察，不能写成已被公开benchmark验证的技术突破。
   - 来源: [The Information](https://www.theinformation.com/articles/khosla-backed-startup-claims-breakthrough-largest-ever-ai-model-iphone), [Yahoo Finance](https://au.finance.yahoo.com/news/apple-eyeing-startup-prismml-bring-134817752.html)

**Google将披露广告中的AI生成内容**
- Google宣布将开始披露广告中哪些内容由AI生成或数字修改合成。新功能将添加至**My Ad Center**面板，用户可通过Google Search、YouTube和Google Discover上的三点菜单或信息图标访问，该面板将新增**"How this ad was made"**选项，显示广告是否由AI创建或编辑。当广告商使用Google生成式AI广告工具时，披露将自动启用；若广告在其他平台创建，广告商需自行标注，**Google不会进行主动核查**。该功能面向全球用户开放，部分市场若当地法律要求也将被标记为AI生成内容。
  > 💡 广告AI披露要求未来可能向Meta、TikTok等平台扩散，AI生成内容标识或将成为行业标配。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/09/google-will-now-disclose-which-ads-are-made-with-ai/)

### 算力追踪
**Musk承诺不切断Anthropic算力供应，xAI与Anthropic算力关系再生博弈**
- Elon Musk公开承诺不会切断对Anthropic的算力供应，并对其AI模型Mythos/Fable表示赞赏。TechCrunch报道称，Anthropic目前与xAI存在合作意向，相关模型工作负载规模涉及约400亿美元营收体量。
  > 💡 Anthropic此前刚与TeraWulf签署190亿美元算力租赁协议以分散风险，Musk此时承诺不切断供应反映算力供应商竞争加剧，多元化算力布局已成头部AI公司标配。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/09/elon-musk-praises-mythos-fable-promises-not-to-cut-off-anthropic/)

**Meta新一代MTIA AI芯片计划9月投产**
- Meta计划于2026年9月开始生产其新一代AI专用芯片，至少一款芯片已在约6周内通过测试。Meta与Broadcom合作设计芯片，并将交由TSMC制造，同时采购Samsung内存、Sandisk存储和Sumitomo Electric光纤设备。相关芯片属于Meta Training and Inference Accelerator（MTIA）项目，采用模块化chiplet路线，面向推荐/排序模型训练、更广泛AI负载和应用侧推理。
  > 💡 Meta自研AI芯片进入新一轮量产窗口，核心目标是降低对NVIDIA/AMD GPU的边际依赖，但其1250亿至1450亿美元年度资本开支预期也说明，自研芯片短期更多是补充而非替代。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/09/metas-new-ai-chips-will-begin-production-in-september/)

### 初创&融资
**Ollama完成6500万美元B轮融资，月活开发者近900万**
- 开源AI开发工具Ollama完成6500万美元B轮融资，由Theory Ventures领投；此前公司曾完成Benchmark领投的1500万美元A轮，累计融资达到8800万美元。Ollama帮助开发者在个人电脑上快速运行开源权重模型，GitHub已获得约17.6万星和近1.7万fork；公司称月活开发者超过890万，并已进入85%的财富500强企业，团队规模仅14人。
  > 💡 Ollama的融资与增长说明本地模型运行正在成为AI开发者基础设施的默认入口之一，开源权重模型生态的商业化价值不只在模型本身，也在开发体验和分发层。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/09/popular-open-source-ai-developer-tool-ollama-raises-65m-grows-to-nearly-9m-users/)

**Lyzr用自家AI Agent完成1亿美元B轮融资**
- 企业AI Agent初创公司Lyzr使用自研系统SivaClaw主导自身1亿美元B轮融资流程，估值约5亿美元。该Agent处理了130多位投资人的问题、起草投资备忘录，并追踪投资人停留在哪些融资材料页面；公司称已吸引约4亿美元投资意向，来源覆盖硅谷、中东和金融行业投资者。
  > 💡 Lyzr把融资过程本身变成产品演示，说明企业Agent正在从“辅助销售材料”走向执行真实商业流程；但1亿美元融资由Agent驱动的叙事仍需关注最终投资方和条款披露。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/09/an-ai-agent-startup-just-let-its-agent-run-its-100-million-fundraise/)

**Mercor收购AI Agent训练初创Deeptune，正洽谈200亿美元估值**
- AI训练平台Mercor正洽谈新一轮融资，目标估值约200亿美元，高于其2025年10月3.5亿美元C轮时的100亿美元估值。创始人兼CEO Brendan Foody称公司年化收入运行率已超过20亿美元，较4个月前增长约100%。Mercor近日收购了AI Agent训练初创公司Deeptune，Deeptune全员将加入Mercor。
  > 💡 Mercor从数据/专家劳动力平台快速转向AI Agent训练基础设施，收入增速、收购和潜在融资同步出现，显示“高质量人类反馈+Agent训练”正在成为资本追逐的新核心资产。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/09/mercor-is-in-talks-for-a-20b-valuation/), [The Information](https://www.theinformation.com/briefings/mercor-buys-andreessen-horowitz-backed-startup-deeptune)

**Lovable洽谈3亿美元融资，估值或翻倍至132亿美元**
- 瑞典vibe-coding初创公司Lovable正洽谈3亿美元融资，估值约132亿美元，较2025年12月66亿美元估值翻倍；Menlo Ventures预计领投。Lovable成立不足3年，2026年6月年化收入运行率已达5亿美元，用户包括创始人、个人设计师、销售人员以及Workday、Asana、NVIDIA等企业客户。
  > 💡 Lovable估值半年翻倍反映vibe coding仍是AI应用层最热的收入场景之一，资本正在把“自然语言生成软件”视为AI时代的新生产力入口。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/08/lovable-reportedly-in-talks-to-double-its-valuation-to-13-2b/)

**Prime Intellect获1.3亿美元A轮融资，构建Open Superintelligence Stack**
- Prime Intellect宣布完成1.3亿美元A轮融资，由Radical Ventures领投，NVIDIA Ventures、Intel Capital、Dell Technologies Capital及既有投资方参投，累计融资超过1.5亿美元。公司将自身定位为Open Superintelligence Stack，覆盖训练、推理、算力、RL/post-training、环境、沙箱、评测和部署等环节；官方称客户数超过6000家，年化收入在不到一年内增长至超过1亿美元。
  > 💡 Prime Intellect的叙事重点已从“去中心化算力平台”升级为开放模型优化基础设施：让企业拥有自己的RL与后训练闭环，而不是完全依赖封闭前沿模型。
   - 来源: [@PrimeIntellect](https://x.com/PrimeIntellect/status/2074899489190785419), [Prime Intellect](https://www.primeintellect.ai/blog/series-a)

**巴黎AI语音初创Gradium获1亿美元种子轮融资，NVIDIA参投**
- 总部位于巴黎的AI语音初创公司Gradium完成1亿美元种子轮融资，NVIDIA参与投资。公司计划利用这笔资金在湾区设立办公室并扩充AI语音团队。Gradium专注AI语音生成技术。
  > 💡 NVIDIA持续押注AI语音赛道，反映其对实时语音交互作为下一代AI入口的判断；种子轮即获亿元级别，表明头部芯片厂商正通过早期投资锁定下游应用生态。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/09/paris-based-ai-voice-startup-gradium-raises-100m-seed-backed-by-nvidia/)

### 研究关注
**Jiacheng Miao等提出The Agentic Garden of Forking Paths，揭示AI研究Agent可复现并放大分析偏差**
- Stanford的Jiacheng Miao、Jonathan K. Pritchard、James Zou提出The Agentic Garden of Forking Paths，研究AI Agent能否复现人类科研分析中的“分叉路径”。论文发现，在四个高风险领域中，仅通过为AI研究者分配不同persona，就足以让Agent基于同一数据和问题得出不同甚至相反结论，且结论会系统性对齐其预设信念。在42个人类研究团队分析同一移民数据集的实验中，AI Agent复现了72%的人类意识形态差距；同时，86%的AI报告通过独立AI审查，78%通过人类专家多数审查。
  > 💡 这项工作提示科研Agent的风险不只是“分析出错”，而是能低成本、大规模探索许多看似合理的分析路径，并选择性呈现支持某一结论的结果；论文提出m-value和Agentic Bootstrap，试图把“原本可能被报告的分析分布”显性化。
   - 来源: [@TheTuringPost](https://x.com/TheTuringPost/status/2075289747875107013), [arXiv](https://arxiv.org/abs/2607.01507)

**Chen Tang等提出SciReasoner，以深度原生结构推理提升科学结构-属性理解**
- Chen Tang、Yizhou Wang、Jianyu Wu等人提出SciReasoner，一个面向科学结构推理的多模态基础模型，覆盖蛋白质、小分子、无机晶体等结构体系。方法将三维坐标、拓扑关系和周期连接等结构信息离散为统一的结构感知词表，使LLM能够直接在原生结构表示上推理。论文称SciReasoner在86个基准中的67个达到SOTA，并在Gene Ontology、逆合成和晶体性质预测等任务上取得明显提升。
  > 💡 SciReasoner的价值不只在材料结构-性能预测，也在于把“结构”作为模型原生语言的一部分处理，为蛋白质、分子和晶体任务提供更统一的科学推理接口。
   - 来源: [arXiv](https://arxiv.org/abs/2607.07708), [HuggingFace Daily Papers](https://huggingface.co/papers/2607.07708)

**Hongyu Qu等提出LaMem-VLA，为机器人VLA模型加入双潜在记忆**
- Hongyu Qu、Xiao Ma、Tao Kong等人提出LaMem-VLA，面向视觉-语言-动作（VLA）模型的长程任务记忆问题。该方法设置短期记忆库和长期记忆库，并通过curator、seeker、condenser、weaver等模块筛选、检索、压缩和融合历史观测，将关键历史信息重构为潜在记忆token，与当前观测和指令一同进入VLA推理。论文在SimplerEnv和LIBERO上验证了长程操作任务收益。
  > 💡 机器人Agent要从“看见当前帧就动作”走向可持续执行复杂任务，记忆机制会成为VLA模型的重要基础组件。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2607.07608), [arXiv](https://arxiv.org/abs/2607.07608)

**EdgeBench揭示智能体真实环境学习缩放规律**
- Deyao Zhu等人提出EdgeBench，用约38,000小时的智能体-环境交互数据分析真实环境学习能力，覆盖134个长周期任务，包括科学发现、软件工程、组合优化、专业工作、形式数学和交互式游戏。论文发现智能体在环境学习过程中的总体表现符合log-sigmoid缩放规律（R²=0.998），并估计环境学习速度大约每三个月翻倍；作者同时开源51个任务和完整评测框架。
  > 💡 EdgeBench把Agent评测从静态问答推向长时间、可交互的真实任务环境，为衡量“边做边学”的Agent能力提供了更接近生产场景的尺度。
   - 来源: [arXiv](https://arxiv.org/abs/2607.05155)

### X讨论
**Sam Altman：5.6版本在性价比上对企业是巨大进步**
- OpenAI CEO Sam Altman在X平台回应企业AI成本关切，指出5.6版本在每任务成本上有所改善，Terra和Luna同样如此。OpenAI官方宣布GPT-5.6系列进入GA，覆盖ChatGPT、Codex和OpenAI API：GPT-5.6 Sol面向最高难度任务，支持`ultra`模式默认并行协调4个Agent，`max`推理强度也高于此前的`xhigh`；GPT-5.6 Terra定位为主力平衡模型；GPT-5.6 Luna主打低延迟与低成本。官方同时推出Responses API的Programmatic Tool Calling与多Agent beta，并披露API价格：Sol输入/输出为每百万token 5/30美元，Terra为2.5/15美元，Luna为1/6美元。基准方面，官方称Sol在Artificial Analysis Coding Agent Index达80、Terminal-Bench 2.1达88.8，Ultra模式在Terminal-Bench 2.1达91.9、BrowseComp达92.2，Luna在MMLU-Pro上达90.5且速度最快。
  > 💡 Altman强调的“性价比”不只是降价，而是OpenAI把GPT-5.6拆成高能力Sol、均衡Terra、低成本Luna三条企业推理曲线，并用`ultra`多Agent与Programmatic Tool Calling把复杂任务执行能力产品化。
   - 来源: [@sama](https://x.com/sama/status/2075267201058426944#m), [OpenAI](https://openai.com/index/gpt-5-6/)

**Samaya发布FrontierFinance金融研究Agent长周期基准**
- Samaya Research发布FrontierFinance，定位为面向完整投资研究工作流的开放金融Agent评测。当前v3.1公共集包含220个开放式金融研究查询、11,543条专家rubric，其中64.9%为essential criteria，覆盖金融数据与建模、行业/宏观研究、财报事件、公司研究、催化剂监控和筛选发现等6类任务。系统榜单显示Samaya System得分50.8%，Claude Fable 5 + Finance Agent v2为49.2%，Claude Opus 4.8 + Finance Agent v2为45.0%，GPT 5.5 + Finance Agent v2为43.5%；普通Web Search基线中，Claude Opus 4.8为33.0%，Gemini 3.1 Pro为30.7%，GPT 5.5为20.7%。
  > 💡 FrontierFinance把金融Agent评测从单点问答推进到长周期、可交付的投资研究任务，专家rubric和工作流覆盖度比传统金融QA基准更接近真实分析师工作。
   - 来源: [@maithra_raghu](https://x.com/maithra_raghu/status/2075240565625757730), [Samaya Research](https://research.samaya.ai/benchmarks/frontier-finance)

---
*更新时间: 2026-07-10 09:03*
