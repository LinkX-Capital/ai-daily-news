# 📡 03月31日 AI前沿动态

**自动汇总** | 24h | 共 21 条

## 📌 要点速览

- **模型前沿**：阿里发布Qwen3.5-Omni：原生多模态模型，支持语音和多模态方式Vibe Coding; SemiAnalysis预告Qwen 3.6即将发布，专注Agentic Coding; UniPat AI发布Echo预测智能基础设施
- **产业动态**：Mistral AI融资$830M; OpenAI推出OpenAI Academy; 智谱AI发布AutoGLM大一统Agent产品; PMidjourney年收入突破$200M
- **算力追踪**：Starcloud融资$170M，在太空建设数据中心
- **初创&融资**：ScaleOps融资$130M，实时自动化基础设施应对GPU短缺和云成本上升; AI芯片初创Rebellions融资$400M估值$2.3B；此芯科技B轮融资近10亿元; Qodo融资$70M专注代码验证; Physical Intelligence讨论$11B估值融资
- **研究关注**：北京大学发布ProactiveVideoQA和MMDuet2
- **X讨论**：Jason Weston转发ParaGator：在线RL解决并行推理聚合难题; SemiAnalysis揭示芯片制造氦气供应风险; swyx解读Redpoint榜单，54%企业SaaS可被AI重构; Qwen展示Vibe Coding和语音控制

---

## 详情参考

### 模型前沿

**阿里发布Qwen3.5-Omni：原生多模态模型，支持语音和多模态方式Vibe Coding**

阿里通义实验室发布Qwen3.5-Omni，定位为原生多模态AGI基座，支持文本、图像、音频、视频统一理解。核心亮点是**Audio-Visual Vibe Coding**：对着摄像头描述想法，AI立即生成可运行网站或游戏。此外支持脚本级字幕（带时间戳和场景剪辑）、74种语言语音识别、29种语言情感语音生成。在215项基准上取得SOTA。**WebSearch和复杂Function Calling原生支持**，模型可自主决定何时获取实时数据。

> 💡 Qwen3.5-Omni的Vibe Coding标志着'说话就能编程'成为现实，多模态Agent能力正在快速追赶GPT-4o，国产开源模型持续逼近AGI。

📌 来源：[@Ali_TongyiLab](https://x.com/Ali_TongyiLab/status/2038609308750143762)

**UniPat AI发布Echo预测智能基础设施：含动态评测引擎和EchoZ-1.0模型**

UniPat AI构建预测智能基础设施Echo，包含动态评测引擎、面向未来事件的训练范式和预测专用模型EchoZ-1.0。预测智能指模型预测未来事件的能力，是通往通用智能的关键能力之一。该基础设施提供标准化评测和训练方法。论文还公布EchoZ-1.0模型在多项预测任务上的表现。这是首个系统性的预测智能研究和评测框架。

> 💡 预测智能是LLM时间推理能力的核心检验Echo为时间序列推理和规划提供了新范式。

📌 来源：[机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651024564&idx=1&sn=6fb075d1ca107111ac46eeb2215716fd&chksm=8531946d8041ab4c723648389d4c4c5008b3300e1fd81bac947f42dc1ed6785ca604838204bf&scene=0&xtrack=1#rd)

**SemiAnalysis预告：Qwen 3.6即将发布，Qwen 3.6 Plus Preview不是视觉语言模型**

SemiAnalysis透露Qwen 3.6即将发布，暗示可能"随时发布"。同时OpenRouter澄清**Qwen 3.6 Plus Preview不是视觉语言模型**，而是升级版旗舰模型，专注于提升Agentic Coding、前端编程和通用能力。

> 💡 Qwen 3.6专注Agentic Coding而非多模态视觉，差异化竞争策略明确，语音编程助手成为主战场。

📌 来源：[@SemiAnalysis_](https://x.com/SemiAnalysis_/status/2038691215806267570#m) | [@OpenRouter](https://x.com/OpenRouter/status/2038701611179294799#m)

### 产业动态

**Mistral AI融资$830M：巴黎附近建设数据中心计划2026年Q2运营**

Mistral AI通过债务融资$830M，计划在巴黎附近建设数据中心，目标2026年第二季度开始运营。这是Mistral首次自建数据中心，此前公司依赖第三方云服务商。数据中心选址法国，可能享受该国核能供电优势，降低训练电力成本。Mistral作为欧洲领先的独立AI公司，自建数据中心彰显其在AI基础设施方面的野心。

> 💡 自建数据中心是AI公司控制成本和独立性的关键，欧洲核能供电可显著降低训练电力成本。

📌 来源：[TechCrunch](https://techcrunch.com/2026/03/30/mistral-ai-raises-830m-in-debt-to-set-up-a-data-center-near-paris/)

**OpenAI推出OpenAI Academy：免费AI教育平台覆盖全球学习者**

OpenAI推出OpenAI Academy免费AI教育平台，旨在向全球学习者提供人工智能技能培训。平台涵盖从基础到高级的AI课程，结合理论学习和实践项目。OpenAI表示希望通过降低AI学习门槛来扩大开发者生态。Academy将提供证书认证，与主流教育机构合作。

> 💡 AI教育平台是培养开发者生态的关键棋子，OpenAI正在从应用层向教育层延伸，构建更完整的生态闭环。

📌 来源：[量子位](https://www.qbitai.com/2026/03/393460.html)

**智谱AI发布AutoGLM大一统Agent产品：网页+手机+文档三端协同**

智谱AI发布AutoGLM大一统Agent产品，实现网页、手机、文档三端的协同操作。用户可以通过自然语言指令让AutoGLM在多个设备和平台间完成复杂任务。该产品整合了智谱在大模型和Agent技术方面的积累，被认为是国内版Claude Computer的对标产品。AutoGLM支持跨应用任务编排。

> 💡 多端协同Agent是下一代AI助手的技术制高点，智谱AutoGLM若能真正实现跨平台任务执行，将是国产AI的重要突破。

📌 来源：[量子位](https://www.qbitai.com/2026/03/393433.html)

**Midjourney年收入突破$200M：AI图像生成商业模式验证成功**

Midjourney年收入已显著超过$200M（2023年数据），且此后持续增长。据多个来源显示，Midjourney 2025年收入达到$500M，2026年预测$500-600M ARR。公司仅凭约10-11名员工实现这一规模，人均收入约$1800万。相比OpenAI的Sora因商业化困境关闭，Midjourney证明了付费订阅模式在创意工具市场的可行性。更值得注意的是，Midjourney从未接受外部投资，完全自筹资金，保持对产品方向的控制。

> 💡 Midjourney的$0 VC模式在AI时代极为罕见，高利润率+强产品力是根本，但这也意味着没有资本弹药应对价格战。

📌 来源：[The Information](https://www.theinformation.com/briefings/midjourney-revenue-now-significantly-200-million)

### 算力追踪

**Starcloud融资$170M：在太空建设数据中心**

Starcloud完成$170M A轮融资，计划在太空建设数据中心。该公司认为太空环境可以提供更低的温度、更少的冷却成本，以及几乎无限的扩展空间。数据中心建设预计将分阶段进行，初期可能先建设近地轨道设施。太空数据中心概念由来已久，但实际落地面临高昂的发射成本和技术挑战。

> 💡 太空数据中心是算力供给的长远探索，在轨AI计算可能成为未来差异化方向，但商业化路径仍遥远。

📌 来源：[TechCrunch](https://techcrunch.com/2026/03/30/starcloud-raises-170-million-series-ato-build-data-centers-in-space/)

### 初创&融资

**ScaleOps融资$130M：实时自动化基础设施应对GPU短缺和云成本上升**

ScaleOps完成$130M融资，专注于通过实时基础设施自动化来解决GPU短缺和AI云成本飙升问题。公司的核心技术能够在运行时自动优化计算资源分配，减少GPU空闲时间。当前AI推理成本高企，部分原因是GPU利用率不足。ScaleOps的方案适用于各种AI云服务商，帮助提升整体计算效率。

> 💡 AI推理成本中GPU利用率是关键杠杆，实时自动化有望降低推理成本，对冲算力短缺。

📌 来源：[TechCrunch](https://techcrunch.com/2026/03/30/scaleops-130m-series-c-kubernetes-efficiency-ai-demand-funding/)

**AI芯片初创Rebellions融资$400M估值$2.3B：专为AI推理设计挑战NVIDIA**

韩国AI芯片初创Rebellions完成$400M融资，估值达$2.3B，计划今年晚些时候上市。公司专门设计用于AI推理的芯片，是NVIDIA在推理侧的潜在挑战者。Rebellions产品定位与训练芯片不同，强调推理场景的能效比。当前数据中心推理需求快速增长，专用推理芯片市场空间巨大。此轮融资为pre-IPO轮，表明公司已准备好公开市场检验。

> 💡 推理芯片是NVIDIA相对薄弱环节，专用推理芯片公司有望在边缘端和大规模推理场景打开突破口。

📌 来源：[TechCrunch](https://techcrunch.com/2026/03/30/ai-chip-startup-rebellions-raises-400-million-at-2-3b-valuation-in-pre-ipo-round/)

**此芯科技B轮融资近10亿元：通用智能计算芯片解决方案提供商**

此芯科技完成近10亿元人民币B轮融资。投资方包括多家知名机构。公司主要致力于开发兼容ARM指令集的通用智能计算体系，提供芯片产品和通用计算一站式解决方案。公司在CPU内核研发、SoC和全栈软件开发等领域具备技术积累。通用智能计算芯片可应用于数据中心、PC、移动设备等场景。此轮融资表明资本市场对国产AI芯片的持续看好。

> 💡 ARM兼容路线利于生态迁移，国产AI芯片在PC和端侧场景有机会实现差异化突破。

📌 来源：[IT桔子](https://www.itjuzi.com/investevent/14694871)

**Qodo融资$70M专注代码验证：AI编程规模化下的质量保障**

Qodo完成$70M融资，致力于代码验证服务。随着AI大规模生成代码，确保代码正确性成为关键挑战。Qodo的技术可自动检测代码错误、安全漏洞和逻辑问题。该公司定位为AI编程工作流的质量保障层。当前软件开发中AI生成的代码比例上升，但错误率仍是企业采用的主要顾虑。代码验证工具有望成为AI编程不可或缺的一环。

> 💡 代码验证是AI编程落地的最后一道防线，有望复制安全扫描工具的成功路径。

📌 来源：[TechCrunch](https://techcrunch.com/2026/03/30/qodo-bets-on-code-verification-as-ai-coding-scales-raises-70m/)

**Physical Intelligence讨论$11B估值融资：具身智能赛道估值飙升**

Physical Intelligence正在讨论新一轮融资，估值达到$11B，计划融资约$1B。更值得注意的是，$11B估值将在4个月内实现翻倍——公司2025年底刚完成$400M融资，估值$2.4B。Founders Fund和Thrive Capital等顶级机构支持。公司致力于开发能驱动各类机器人的通用AI模型，具身智能正在成为AI融资新风口。$1B单轮融资规模也显示该领域竞争正在升温。

> 💡 4个月估值翻倍至$11B，具身智能已成AI最热赛道，但$2.4B到$11B的跳跃也意味着投资人正在为梦想支付高溢价。

📌 来源：[The Information](https://www.theinformation.com/briefings/physical-intelligence-said-discuss-11-billion-valuation)

### 研究关注

**北京大学发布ProactiveVideoQA和MMDuet2：视频多模态模型的主动交互训练评估方案**

北京大学王选计算机研究所发布两篇论文，提出视频多模态大模型的主动交互能力。当前主流模型采用被动响应模式，即等待用户提问后生成回复。ProactiveVideoQA和MMDuet2研究如何让模型在视频播放过程中自主判断何时发起回复，实现真正的主动交互。该研究涵盖训练方法、评估指标等完整方案。

> 💡 主动交互是视频AI assistants用户体验的关键突破，但技术难度在于判断何时介入，需要平衡主动性与干扰性。

📌 来源：[机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651024564&idx=2&sn=35264986836dd290aa3618d110aaeb85&chksm=858f08d7857fe485619d3954aaa9afa450ebccc9ab06e3d8bcd06dde6b482cf7e24bc25de445&scene=0&xtrack=1#rd)

### X讨论

**Jason Weston转发ParaGator：在线RL解决并行推理聚合难题**

Jason Weston转发ParaGator论文，提出通过在线RL同时训练selector和aggregator来解决并行推理聚合问题。核心发现是聚合效果在联合训练时最优。相比静态聚合方法，**ParaGator能动态选择最优推理路径**，这对降低推理成本有重要意义。实验显示该方法在多个基准上取得SOTA。

> 💡 推理效率是LLM落地的关键瓶颈，动态聚合方案有望在保证质量的同时显著降低成本。

📌 来源：[@jaseweston](https://x.com/jaseweston/status/2038609971160424748#m)

**SemiAnalysis揭示芯片制造氦气供应风险：三大中心50%+氦气依赖卡塔尔**

SemiAnalysis通过ChipBook追踪发现，三大半导体制造中心（台湾、韩国、新加坡）各自50%以上的氦气供应来自卡塔尔。氦气是光刻和冷却的关键材料，**卡塔尔地缘风险可能冲击芯片产能**。此外，氦气开采技术门槛高，供应链短期难以多元化。这意味着芯片制造商可能面临供应中断风险。

> 💡 半导体供应链上游材料的地缘风险被严重低估，芯片厂正在加速氦气储备和供应多元化布局。

📌 来源：[@semianalysis_](https://x.com/SemiAnalysis_/status/2038602289884127679#m)

**swyx解读Redpoint榜单：54%企业SaaS可被AI重构**

swyx讨论Redpoint的研究称54%的企业SaaS业务可以被AI重新构建，46%的其他业务同样适用。**这意味着AI颠覆企业软件的速度可能远超预期**。Redpoint是顶级VC，其判断反映资本对AI落地速度的重新评估。AI正在从辅助工具变成重写行业格局的核心力量。

> 💡 企业软件AI化不是渐变而是重构，拥有垂直场景数据和分发渠道的存量玩家面临最大压力。

📌 来源：[@swyx](https://x.com/swyx/status/2038509566800118021#m)

**Qwen展示Vibe Coding和语音控制：多模态编程助手成新战场**

Qwen发布Audio-Visual Vibe Coding等多个demo，展示语音风格/情感控制、多轮对话打断等能力。用户可以**通过语音和多模态方式自然地与AI交互编程**，大幅降低编程门槛。Qwen正在语音TTS和多模态编程助手方向与GPT-4o语音模式竞争。

> 💡 语音编程可能是下一个杀手级场景，谁先实现自然对话式编程谁就能抓住开发者心智。

📌 来源：[@alibaba_qwen](https://x.com/Alibaba_Qwen/status/2038641496455557565#m)

**vLLM-Omni v0.18.0：新增Qwen3-TTS支持，多模态推理框架持续扩张**

vLLM-Omni v0.18.0发布，324个commits，83位贡献者（38位新）。**新增Qwen3-TTS和Qwen3-Omni生产级支持**，标志vLLM生态与国产模型的整合进一步深化。Omni系列（语音+视觉+文本）正在成为推理框架标配，多模态竞争从模型层扩展到基础设施层。

> 💡 推理框架的多模态支持正在成为竞争焦点，生态整合能力比单点技术更重要。

📌 来源：[@vllm_project](https://x.com/vllm_project/status/2038415516772299011#m)

