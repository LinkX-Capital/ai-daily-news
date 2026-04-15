## 04月15日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 产业动态：Anthropic发布Claude Code重大更新，桌面版支持多会话并行，新增Routines定时自动化任务; Google发布Gemini Robotics-ER 1.6,提升机器人推理能力; The World Labs发布Spark 2.0,高保真3DGS进入网页; OpenRouter上线Reranker排序模型; 盛大AI研究院发布流式动作生成技术
- 算力追踪：Epoch AI报告五大超算厂商控制全球超2/3 AI算力
- 初创&融资：AI数据中心初创Fluidstack正进行10亿美元融资; AI视频生成公司Sand.ai完成5000万美元融资; CREAO AI完成Pre-A轮千万美元融资,用Agent OS重构工作入口; OpenAI收购AI财务规划公司Hiro Finance
- 研究关注：NTU发布世界模型交互新范式; 北航与字节提出SAGE-RL,揭示大模型推理可按需调节
- X讨论：Anthropic发布 Automated Alignment Researcher 研究

---

## 详细参考

### 产业动态
**Anthropic发布Claude Code重大更新：桌面版支持多会话并行，新增Routines定时自动化任务**
- Claude Code桌面版全新设计，新增侧边栏支持用户在同一窗口并行运行多个Claude会话，便于管理和切换不同任务。同时推出Routines功能（研究预览），用户可配置一个routine（包含prompt、repo和connectors），支持按计划定时运行、API调用触发或事件响应触发。**Routines运行在Anthropic云端基础设施上，不需要保持电脑开机**，意味着开发者可以让AI编程助手真正成为后台持续工作的智能体。
  > AI编程工具从被动应答走向主动执行，云端自动化是Agent从概念到生产的关键一步
   - 来源: [@claudeai - 桌面版](https://x.com/claudeai/status/2044131493966909862#m) | [@claudeai - Routines](https://x.com/claudeai/status/2044095086460309790)

**Google发布Gemini Robotics-ER 1.6，提升机器人推理能力**
- Gemini Robotics-ER 1.6是Google DeepMind推出的推理优先模型升级版，帮助机器人理解环境并完成真实世界任务。该模型增强了推理能力，使机器人能更好应对复杂任务场景。
  > 机器人模型从泛化能力转向推理能力，VLA路线竞争加剧
   - 来源: [Google DeepMind](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-robotics-er-1-6/)

**The World Labs发布Spark 2.0，高保真3DGS进入网页**
- The World Labs发布Spark 2.0，将高质量3D Gaussian Splatting场景带入网页端。该技术让高保真3D内容可在任意设备上访问，是空间计算的重要进展。
  > 3D生成从本地走向网页，端侧体验优化推动空间互联网普及
   - 来源: [@theworldlabs](https://x.com/theworldlabs/status/2044096996148171035#m)

**OpenRouter上线Reranker排序模型**
- OpenRouter推出Reranker排序模型，功能是在RAG流程中对文本块进行相关性排序。嵌入搜索找到相关 chunk，reranker进一步判断排序优先級。首批包括cohere/rerank-4-pro等模型。
  > RAG工作流完善推动企业应用落地，排序模型成关键拼图
   - 来源: [@openrouter](https://x.com/OpenRouter/status/2044070463723204730#m)

**盛大AI研究院发布流式动作生成技术，推理延迟仅1帧**
- 盛大AI研究院发布新工作，实现动作序列无限长且生成零延迟。技术突破流式生成超越非流式的效果，一句话即可让虚拟人动作丝滑如真实人类，推理延迟仅1帧（约33ms）。
  > 动作生成低延迟突破为人形机器人交互奠定基础，时序生成是Diffusion外的另一路线
   - 来源: [量子位](https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247883024&idx=3&sn=2de93fe100ad0f43d1c3402476af6020)

### 算力追踪
**Epoch AI: 五大超算厂商控制全球超2/3 AI算力**
- Epoch AI发布AI Chip Owners数据报告，**Google、Microsoft、Meta、Amazon、Oracle五家公司目前控制约2/3的全球AI算力**，较2024年初的~60%进一步上升。许多AI实验室（包括OpenAI和Anthropic）几乎完全依赖这些超算厂商获取算力资源。
  > 算力集中度持续攀升，AI实验室对云厂商的依赖关系决定了产业格局的上层建筑
   - 来源: [Epoch AI](https://epochai.substack.com/p/five-hyperscalers-now-own-over-two)

### 研究关注
**NTU发布世界模型交互新范式，解决主动操作难题**
- 新加坡南洋理工大学发布世界模型交互新范式，攻克主动操作难题。该研究被称为头号玩家照进现实，为世界模型的主动交互提供新方法论。
  > 世界模型从被动理解走向主动交互，物理引擎与学习融合是关键路径
   - 来源: [新智元](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA==&mid=2652691877&idx=3&sn=8256bbc70570c075269f74878cc0148b)

**北航与字节提出SAGE-RL，揭示大模型推理可按需调节**
- 北京航天航空大学与字节合作提出SAGE-RL方法，发现大模型具备根据任务难度自动调节推理能力的隐藏天赋。研究表明长推理不一定更强，模型可以自己踩刹车按需调整。
  > 推理tokens可优化空间被验证，RL scaling law新方向，模型自身具备推理资源调节能力
   - 来源: [PaperWeekly](https://mp.weixin.qq.com/s?__biz=MzIwMTc4ODE0Mw==&mid=2247719552&idx=2&sn=e414a3299500b622cc0a8175271890d1)

### 初创&融资
**AI数据中心初创Fluidstack正进行10亿美元融资，估值180亿美元**
- Fluidstack是一家AI数据中心初创公司，在为Anthropic建设数据中心获得500亿美元合同后，正在进行10亿美元融资。消息人士透露，此轮融资后估值将达到180亿美元，而就在几个月前其估值仅为75亿美元。
  > 算力供给侧竞争加剧，Fluidstack以数据中心+大客户合同模式快速崛起，挑战传统云厂商地位
   - 来源: [TechCrunch](https://techcrunch.com/2026/04/14/ai-datacenter-startup-fluidstack-in-talks-for-1b-round-at-18b-valuation-months-after-hitting-7-5b-says-report/)

**AI视频生成公司Sand.ai完成5000万美元融资**
- Sand.ai是一家中国AI视频生成技术公司，核心团队来自微软亚洲研究院和阿里巴巴达摩院。公司主要研究方向为视频生成大模型和通用人工智能，技术路线为自回归世界模型。近期完成新一轮约5000万美元融资。
  > 中国视频生成赛道的自研世界模型路线获得资本认可，与Sora等Diffusion路线形成竞争
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14695680)

**CREAO AI完成Pre-A轮千万美元融资，用Agent OS重构工作入口**
- Agentic创业公司CREAO AI完成千万级美元Pre-A轮融资，由Prosperity7 Ventures（阿美风险投资）和经纬创投领投，云启资本、砺思资本、高瓴创投、红杉中国、华业天成资本跟投。成立不到一年累计融资超3000万美元，用户突破20万（几乎全部自然增长）。CTO Peter Pang为Meta Llama 3团队前研究科学家。产品定位"Agent OS"——AI既造工具也跑工具的闭环系统，区别于Gumloop的可视化工作流和Relevance的预配置智能体。
  > Agent从"更好的回答者"走向"自主执行闭环"，AI造工具+AI用工具的模式是Agent落地的新范式
   - 来源: [云启资本/Z Potentials](https://mp.weixin.qq.com/s/CGeWCscKeVbFpAH3oDF6pA)

**OpenAI收购AI财务规划公司Hiro Finance**
- OpenAI收购AI个人理财初创Hiro Finance，创始人Ethan Bloch（此前创办Digit以约$2.3亿出售）及约10人团队加入OpenAI。Hiro成立于2024年，提供AI驱动的财务规划工具，用户输入薪资、债务等信息后可模拟不同财务情景。Hiro将于4月20日关停服务。**这暗示OpenAI在为ChatGPT构建财务规划能力**，此前OpenAI已有面向企业财务团队的营销定位。
  > OpenAI通过收购补充垂直场景能力，ChatGPT从通用助手向专业领域纵深扩展
   - 来源: [TechCrunch](https://techcrunch.com/2026/04/13/openai-has-bought-ai-personal-finance-startup-hiro/)

### X讨论
**Anthropic发布 Automated Alignment Researcher 研究**
- Anthropic Fellows团队发布新研究，探讨开发自动化对齐研究员。实验旨在了解Claude Opus 4.6是否能加速AI对齐研究进程。该研究涉及将AI模型用于AI安全对齐方向。
  > AI对齐研究自动化提上日程，模型反向服务于自身安全治理是重要方向探索
   - 来源: [@anthropicai](https://x.com/AnthropicAI/status/2044138481790648323#m)


---
*更新时间: 2026-04-15 07:45*
