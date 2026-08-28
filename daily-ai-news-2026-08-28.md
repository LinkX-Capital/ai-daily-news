## 08月28日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 22 条

---

## 要点汇总

- 模型前沿：Gemini Omni 1.1 Flash上线API：场景延长至40秒、首尾帧插值与4K放大，360p草稿快60%
- 产业动态：Hugging Face 开售 399 美元开源鸭子机器人 Microduck; Barret Zoph加入Google任研究副总裁，将RL与后训练经验带入Gemini团队; Anthropic开放Model Hardware Standard研究预览; Prime Agent开源Agent框架：把ARC-AGI-3通过率从30%拉升至95.5%; Cohere发布文档解析模型Parse：ParseBench 79.2分领先同类，每千页1.5美元
- 算力追踪：Hot Chips：AI开始深度介入芯片设计，OpenAI与Google分享自研芯片AI提速细节; SemiAnalysis:六大基板厂2026年产能已被订满,总交期拉长至12—14个月
- 初创&融资：AI助理初创Instinct完成2.5亿美元B轮融资，估值25亿美元，累计融资3.5亿美元; 英伟达据报以129亿美元收购Hugging Face，交易尚未签署仍可能生变; Cognition年化营收约9亿美元，正以约450亿美元估值融资; 软银洽谈收购人形机器人公司1X Technologies的多数股权
- 研究关注：FrontierChallenge:跨领域科学工作流基准发布,前沿模型Pass Rate仅约20%; Meta^n递归自我改进Agent：固定元操作递归作用于自身产物，ARC-AGI-2上唯一得分非零; Handoff Tax量化Agent模型切换成本：升级强模型仅收回不足一半质量差距且更贵; VoiceMem流式双脑记忆架构：检索134毫秒不增加对话延迟，top-5召回超Mem0近30分
- X讨论：DeepMind试点密码学"双盲"模型评测：模型权重与评测题双向保密; Anthropic面向科学家开放1万个免费Claude席位; OpenAI联合百余家机构发起集体网络防御倡议; Terminal-Bench-Science科学工作流基准发布：70个任务，Claude Opus 5解决率仅约30%; fal基于MiniMax H3后训练发布H3 Max：5秒视频约3秒生成，人评质量三项第一

---

## 📖 详细参考

### 模型前沿
**Gemini Omni 1.1 Flash上线API：场景延长至40秒、首尾帧插值与4K放大，360p草稿快60%**
- Google 向开发者开放生成式视频模型 Gemini Omni 1.1 Flash（Gemini API 与 Google AI Studio）。场景延长功能可基于最多**10秒**先前上下文续写视频（此前模型仅参考最后一秒），按10秒步长延长、累计可达**40秒**；支持指定首尾帧生成连续过渡镜头；360p 草稿生成比720p标准分辨率**快60%、成本约为其三分之一**；输出可放大至1080p/4K；多模态输入支持最多3秒视频参考以保持角色一致性。Omni 1.1 同日起向全球 Google AI Plus/Pro/Ultra 订阅者开放（Google Flow 与 Gemini App 内的场景延长）。
  > 💡 把"低成本草稿+高精度成品"的双档工作流产品化，瞄准的是专业视频生产的迭代链路而非一次性生成——生成视频竞争的焦点正从画质转向可控性与迭代成本。
   - 来源: [Google Blog](https://blog.google/innovation-and-ai/technology/developers-tools/build-with-gemini-omni-1-1-flash/) | [@GoogleAI](https://x.com/GoogleAI/status/2093008998987403303)

### 产业动态
**Hugging Face 开售 399 美元开源鸭子机器人 Microduck**
- Hugging Face 发布 Microduck，这是一款外形像鸭子的开源机器人，售价 399 美元、圣诞前发货。CEO Clem Delangue 表示 Microduck 是一款可以用强化学习教新动作的开源机器人。这只 25 厘米高的鸭子能够摇摆行走、用喙夹取最多 800 克的物品、摔倒后自行站起、蹲下，甚至能踩轮滑。Microduck 通过摄像头、激光雷达和两个 IMU 感知环境，行为可在仿真中训练并直接部署到机器人本体，SDK、仿真环境与完整 RL 训练栈均放在 GitHub 上。Hugging Face 在 2025 年 4 月收购法国 Pollen Robotics 以推进低价开源 AI 硬件，双方此前还推出过 499 美元的 Reachy Mini 与 399 美元的 Reachy Mini Lite。
  > 💡 把仿真→部署→再训练闭环和 RL 训练栈打包开源，是把具身智能的门槛压到消费级价格带的一次试水，能否形成社区飞轮取决于开发者生态。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/27/hugging-face-is-selling-a-cute-399-open-source-duck-robot-microduck)

**Barret Zoph加入Google任研究副总裁，将RL与后训练经验带入Gemini团队**
- Barret Zoph 曾与 Mira Murati 共同创立 Thinking Machines Lab 并任 CTO，今年1月与联创 Luke Metz 离开公司重返 OpenAI，随后被曝实际是遭解雇；他在 OpenAI 任职五个月、负责 AI 企业销售业务，于今年6月离职。据报道，Zoph 已加入 Google 担任研究副总裁（VP of Research），这恰好是他此前工作过的公司。Google 发言人回应称，期待他带着 RL（强化学习）与后训练专长回归 Gemini 团队。
  > 💡 一年半内三换门庭（Thinking Machines→OpenAI→Google），RL/后训练人才在推理模型竞争白热化阶段已成为巨头间直接争夺的核心资产；OpenAI 近八个月高管持续流出，则让"顶级研究者更倾向回到大平台资源位"成为值得跟踪的流向信号。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/27/barret-zoph-the-thinking-machines-co-founder-who-defected-to-openai-is-now-at-google/)

**Anthropic开放Model Hardware Standard研究预览：给AI Agent操作实验设备的共享规范**
- Anthropic 向首批科研实验室与先进制造商开放 Model Hardware Standard（MHS）研究预览，这是一套让 AI Agent 安全操作物理设备的共享规范。借助 MHS，Agent 可并行操作显微镜、液体处理仪、机械臂等多种实验与制造仪器，执行从常规药物发现实验到量子计算机激光校准的任务。实验室硬件集成通常需要数周甚至数月，MHS 将集成工作缩短至**数小时或数分钟**；Agent 能推理实验每一步、实时更新参数，并在部分情况下从硬件错误中自恢复，支撑全天候自主实验。MHS 的开发始于 Anthropic 与 HHMI Janelia Research Campus 的合作。
  > 💡 与其让每家实验室为每种仪器做定制集成，不如把"Agent 如何操作硬件"沉淀为协议层——这是 Anthropic 在科学智能方向的平台型卡位，若成为事实标准，Claude 将默认获得实验室自动化入口。
   - 来源: [Anthropic](https://www.anthropic.com/news/model-hardware-standard-research-preview) | [@AnthropicAI](https://x.com/AnthropicAI/status/2093038426140651791)

**Plaud发布AI耳机Plaud One：充电盒内置eSIM，可不依赖手机远程调度AI助理**
- 笔记硬件公司 Plaud（软硬件用户超**250万**）推出耳机形态新品 Plaud One，可录制通话；充电盒可录制线下对话并自带 eSIM——用户无需手机或电脑即可远程指示 Plaud 的 AI Agent 执行任务。转录后 Agent 可对接 Gmail、Google Calendar、Notion、Slack 等工具，撰写跟进邮件、生成文档或演示文稿。硬件规格上，Plaud One 配 12mm 单元与主动降噪，充电盒可在**5米**范围内清晰收音，耳机单次充电可录制6小时线下会议或3小时通话，配合充电盒总录音时长达**25小时**。Viaim 与 Anker 已有类似笔记耳机，Plaud 押注软件与 Agent 集成做差异化。
  > 💡 eSIM 让耳机盒成为独立联网的 Agent 入口，硬件公司正从"录音转写"卷向"离身调度的常驻个人助理"形态，可穿戴设备的价值锚点开始从传感器转向通信自主性。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/27/plauds-new-earphones-come-with-an-esim-enabled-case-for-talking-to-ai-agents/)

**Prime Agent开源Agent框架：把ARC-AGI-3通过率从30%拉升至95.5%**
- 语言模型是顺序处理器，而长时程任务需要的计算超出模型权重与活跃上下文。Prime Agent 是一个面向长时程评测与编码工作流的开源 Agent 框架：持久 IPython REPL 按"递归语言模型"抽象做程序化上下文处理与测试时计算，Continual Harness 在轨迹之间保留历史、记忆、技能与子Agent规格，递归子Agent之间通过直接通信协作。框架统一负责执行、恢复、验证与资源记账、把策略构建留给模型本身，避免框架失败被误判为模型失败。在该框架下，ARC-AGI-3 RHAE Best@1 从30%提升至**95.5%**，并在长上下文编码、GPU kernel 生成、模拟器构建与自主 nanoGPT 训练任务上持平或超过原生与流行框架；在 Factorio 上，精化迭代支撑连续的科技树推进、专属子Agent实现并行作业。代码已开源。
  > 💡 同一个模型换一套执行框架，抽象推理通过率提升两倍以上——在评测前沿模型之前，harness 本身已是不可忽略的变量，"裸模型能力"与"工程化能力"的边界正在被重新划定。
   - 来源: [arXiv](https://arxiv.org/abs/2608.23552) | [@PrimeIntellect](https://x.com/PrimeIntellect/status/2092657486151221609)

**Cohere发布文档解析模型Parse：ParseBench 79.2分领先同类，每千页1.5美元**
- Cohere 推出企业文档解析视觉语言模型 Parse（parse-v5.0），把含表格、嵌图的复杂多模态文档转为结构化 Markdown，支持九大语言，用于文档索引、RAG 与 Agent 检索。在自评基准 ParseBench 三维平均分上 Parse 得**79.2**，高于 Mistral OCR 4（74.5）、Databricks AI Parse（72.4）与 LlamaParse 性价比档（78.3），较 AWS Textract 与 Google Document AI 高出20分以上，仅落后于 GPT-5.5（84.4）、Opus 4.8（84.3）、Gemini 3.5 Flash（81.8）等通用前沿大模型。吞吐为单 GPU 4.5页/秒（8×H100节点36页/秒），API 定价**每千页1.5美元**，已上线 Cohere API、Model Vault、Microsoft Foundry 与 AWS SageMaker。
  > 💡 用小专模型把文档解析成本压到前沿模型的一个零头，Cohere 在 Embed/Rerank 之后补齐企业检索栈的"入口"环节——解析质量直接决定下游 RAG 与 Agent 检索的上限。
   - 来源: [Cohere](https://cohere.com/blog/parse) | [@cohere](https://x.com/cohere/status/2092962399754055863)

### 算力追踪
**Hot Chips：AI开始深度介入芯片设计，OpenAI与Google分享自研芯片AI提速细节**
- 在加州帕罗奥图举办的 Hot Chips 半导体会议上，AI 加速芯片设计成为工程师、研究人员和创业公司讨论的主线。OpenAI 团队在演讲中表示，自研 Jalapeño 推理芯片在AI推理上优于英伟达 Blackwell 的部分原因，是 Sol 与 Astra 模型参与了设计与软件流程；Google TPU 团队则披露 DeepMind 利用 AI 帮助 TPU v8 在能效与算力上各提升约6%；英伟达也已推出用于电路布局与数据流优化等多款 AI 设计软件库。会上宣布融资2500万美元的芯片设计初创公司 Agentrys 计划用 AI Agent 帮助芯片设计自动化，其 CEO、原英伟达设计自动化负责人 Mark Ren 认为未来芯片设计将由具备自驱迭代能力的 Agentic 系统承担。
  > 💡 当芯片设计本身开始被 AI 反向改造，推理芯片的差异化来源正从单纯硬件参数扩展到内部研发流程，谁先把设计闭环跑通，谁就更有可能持续保持每瓦性能的代际优势。
   - 来源: [The Information](https://www.theinformation.com/articles/buzz-years-hot-chips-conference-ai-supercharging-chip-design)

**SemiAnalysis:六大基板厂2026年产能已被订满,总交期拉长至12—14个月**
- SemiAnalysis在社交平台发文指出,六大ABF基板供应商2026年产能均已订满,总交期延长至12至14个月。在新一代ASIC/GPU平台演进过程中,封装尺寸扩大至9000—14000平方毫米,层数提升至20—24层,单件占用产线时间显著增加。该机构重申对ABF基板供应链的看多判断,认为这一瓶颈环节将获得更强的定价权。
  > 💡 封装基板从过去的次要配套件升级为限制AI算力出货的关键瓶颈,且本轮供给紧张由面积与层数同步抬升的工艺升级叠加驱动,意味着紧缺周期和议价能力都强于普通产能扩张周期。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2092780027611894235)

### 初创&融资
**AI助理初创Instinct完成2.5亿美元B轮融资，估值25亿美元，累计融资3.5亿美元**
- 据报道，个人AI助理公司 Instinct（运营主体 Spear Street Technology）已完成**2.5亿美元**B轮融资，由 Index Ventures 与 Benchmark 联合领投，估值**25亿美元**，累计融资达3.5亿美元。产品目前处于私有测试阶段，用户将其接入个人应用与设备后，可通过短信和电话与之交互、由其代办事务；公司由23岁创始人 Noah Shinn 于去年创立。早期用户已用它规划跨国公路旅行、购买日用品与演出门票、取消订阅，甚至有人用它筹备婚礼；同时该应用因要求过度宽泛的设备权限及服务条款引发隐私争议。
  > 💡 成立约一年即坐上25亿美元估值，资本对"能调度个人应用与设备的常驻助理"的押注已从概念验证进入高价卡位阶段；但权限边界与隐私条款的争议提示，这类产品的信任天花板才是真正的规模化瓶颈。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/26/viral-ai-startup-instinct-has-raised-350-million-at-a-2-5-billion-valuation/) | [The Information](https://www.theinformation.com/briefings/four-month-old-ai-assistant-startup-instinct-raises-2-5-billion-valuation)

**英伟达据报以129亿美元收购Hugging Face，交易尚未签署仍可能生变**
- 据报道，英伟达已同意以**129亿美元**收购开源模型平台 Hugging Face；另有媒体报道称谈判对该公司的估值超过**130亿美元**、截至周三晚间尚未签署协议且仍可能破裂，英伟达与 Hugging Face 均未回应置评。Hugging Face 成立于2016年，是开发者分享下载开源模型的最大社区之一。报道分析称，收购将让英伟达在开源AI生态获得强入口：开源生态越繁荣，客户对闭源实验室"自研芯片+自研模型"组合的依赖越低，对英伟达硬件的需求越稳固；英伟达此前也已投入数百亿美元自建开源模型。
  > 💡 IT桔子此前已披露同一交易（金额同为129亿美元），两条信源相互印证；但"已同意"与"未签署"的关键差异提示交易仍处尾声博弈。无论最终结构如何，最大开源模型社区并入最大算力厂商，都会重塑外界对开源生态中立性的预期。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/26/nvidia-closes-in-on-hugging-face-acquisition/) | [IT桔子](https://www.itjuzi.com/merger/14364)

**Cognition年化营收约9亿美元，正以约450亿美元估值融资**
- 报道援引知情人士数据称，Cognition 旗下 Devin 编程助手的年化营收已升至约9亿美元，相当于每月7500万美元，自年初以来增长超过三倍。Cognition 已披露的大客户包括 BNY、Santander 与 Mercedes，公司目前正在进行的融资轮可能给出约450亿美元的估值。
  > 💡 在 Anthropic 与 OpenAI 的夹击下，AI 应用层公司仍能凭借垂直场景拿下大客户并保持高增速，这说明 coding 类 Agent 正在把原本属于云软件和外包开发的预算纳入新的付费口径。
   - 来源: [The Information](https://www.theinformation.com/articles/inside-cognitions-booming-growth-high-cash-burn)

**软银洽谈收购人形机器人公司1X Technologies的多数股权**
- 据报道,软银正与OpenAI支持的人形机器人开发商1X Technologies洽谈收购多数股权。该交易若落地将服务于软银的机器人战略,并为1X把软体机器人送入更多家庭争取更长的资金跑道。1X成立已12年,去年秋季曾尝试以100亿美元估值融资10亿美元,但实际到账金额低于预期。
  > 💡 软银若取得控股权,1X从OpenAI生态系的合作方进一步绑定为软银的机器人载体;但1X此前100亿美元估值融资目标未达成,提示出这条人形机器人赛道即便有大额背书,商业化前夜的估值消化仍存在压力。
   - 来源: [The Information](https://www.theinformation.com/briefings/softbank-explores-buying-majority-stake-1x-humanoid-maker)

### 研究关注
**FrontierChallenge:跨领域科学工作流基准发布,前沿模型Pass Rate仅约20%**
- FrontierChallenge是一个跨领域基准,共包含300个端到端科学工作流,首批释放并评估其中97个,覆盖量子化学、分子动力学、材料表征、分析化学、生命科学以及电化学/环境等方向,每项任务给定固定输入并要求产出指定的科学交付物。评估覆盖12个前沿模型和3种Agent脚手架,采用Pass Rate与Avg. Score两项指标,最优配置仅完成其中20项任务,Pass Rate为20.6%。在分析化学和电化学/环境领域,Avg. Score分别达到87.6和94.9,但对应最高Pass Rate分别只有4%和0%;此外在未通过Claude Code的任务轨迹中,有75.5%仍以自然语言宣称完成。
  > 💡 高部分得分与自信式完成声明都无法可靠预测任务真的交付,意味着评估科学Agent必须把端到端工作流执行与交付物完整性作为同一指标,这对Agent评测方法是一次方向性纠偏。
   - 来源: [arXiv](https://arxiv.org/abs/2608.24979)｜[HuggingFace Daily Papers](https://huggingface.co/papers/2608.24979)

**Meta^n递归自我改进Agent：固定元操作递归作用于自身产物，ARC-AGI-2上唯一得分非零**
- 自我改进 Agent 通常只精化答案而不改产生答案的过程；增加元层的方法把该层固定，自编辑系统又必须保留部分编辑机制才能稳定，导致实际可实现的元深度被限制在约2层。Meta^n 的做法是让元操作 Ω 保持不变、递归作用于自己的产物：Ω 反复读取下层求解栈的执行轨迹与产生轨迹的代码，写出下一层（一个策略性预处理加可调用函数库）；由于 Ω 不变而输入严格增长，系统不会失稳且每层推理视角更高，递归深度由收敛决定、层链由进化式档案搜索。在两个骨干模型的八个基准族上全面超过此前自我改进 Agent；在专为抵抗技能记忆设计的 ARC-AGI-2 上是**唯一得分高于零**的方法。消融显示递归增益主要来自层间条件传递，且各层角色随深度自发分化、无任何提示规定。
  > 💡 "不改刀本身、只换切的对象"绕开了自指系统的稳定性死结，让递归深度第一次由收敛而非设计决定；层角色无人规定却自发分化，是复杂系统中结构涌现的一个干净证据。
   - 来源: [arXiv](https://arxiv.org/abs/2608.24735)

**Handoff Tax量化Agent模型切换成本：升级强模型仅收回不足一半质量差距且更贵**
- 编码 Agent 的长任务常需在强弱模型间切换：弱模型卡住时升级、重推理完成后降档省钱，而每次切换都要求接收模型接续一条"非原生"轨迹。该研究用 Claude 与 GPT 两族的高低成本模型配对，变化切换方向、时机与接口（完整轨迹传递/压缩/仅保留仓库状态），发现两个模型族结论一致：完整轨迹升级（弱→强）仅收回**不足一半**的质量差距且成本显著更高，作者称之为"交接税"（handoff tax）；反向降档（强→弱）则是划算的成本-质量点。最优接口还随方向反转：升级时削减弱模型轨迹信息反而更好，降档时删掉强模型轨迹则损害质量。
  > 💡 "便宜模型干杂活、卡住再叫强模型"的流行策略存在隐性税——强模型接手弱模型留下的完整轨迹反而被拖累；工程上更优的做法或许是交接时只转交摘要与仓库状态，而非全量对话历史。
   - 来源: [arXiv](https://arxiv.org/abs/2608.24358)

**VoiceMem流式双脑记忆架构：检索134毫秒不增加对话延迟，top-5召回超Mem0近30分**
- 全双工语音语言模型缺少流式、准确且有情感理解的记忆系统。VoiceMem 采用"双脑"并行架构：信息左脑负责事实检索，情感右脑做长短时情感归因与双节点人格建模，配合流式记忆 I/O；同时给出记忆感知的语音模型训练、长时程评测与可替换记忆后端的解耦部署管线。实测三点优势：左脑 top-5 检索比 Mem0 等经典系统 top-200 高近**30分**；右脑在三个人格基准上全面领先、总分比此前最佳系统高**4.29分**；检索延迟**134毫秒**，在标准 VAD 时延之内、不增加对话延迟。
  > 💡 语音 Agent 的记忆瓶颈不在"存什么"而在"边说边取"——把情感状态与事实分开建索引、再用百毫秒级检索兜住实时性，是个人化语音交互走向可部署的务实模板。
   - 来源: [arXiv](https://arxiv.org/abs/2608.26005)

### X讨论
**DeepMind试点密码学"双盲"模型评测：模型权重与评测题双向保密**
- 模型若提前"见过"评测题（基准污染），得分就不再可信，而传统外部评测存在取舍：要么评测方交出测试题、可能被厂商看到，要么厂商交出模型权重、泄露知识产权。DeepMind 联合新加坡AI安全研究所、OpenMined、AVERI 与 MLCommons 试点对专有前沿模型的双盲评测：评测在 Google Cloud 机密计算的密码学"盒子"内运行，评测方看不到 Gemini 模型权重，Google 也看不到评测方的保密测试题，以密码学证据防止基准污染，此次试点对象为一款 Gemini Flash Lite 模型。
  > 💡 当"模型是否提前见过考题"无法自证时，第三方评测公信力就成为前沿模型治理的软肋；把保密从合同承诺变成可验证的技术事实，若形成行业标准将改变各国AI安全研究所对闭源模型的评测方式。
   - 来源: [Google DeepMind](https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/) | [@GoogleDeepMind](https://x.com/GoogleDeepMind/status/2092961763553677387)

**Anthropic面向科学家开放1万个免费Claude席位，AI for Science单项目最高5万美元额度**
- Anthropic 宣布扩大对科研群体的支持：通过新的科学家团队计划向全球科学家开放**1万个** Claude 订阅席位，为期一年，标准席免费、5倍用量的高级席每月15美元，并计划未来数月大幅扩展规模。AI for Science 免费额度计划同步扩展，从过去侧重生物科学扩大到其他学科，包括曾推动黎曼ζ函数进展与蛋白质设计工作这类计算密集型研究；任何研究者均可申请，单项目最高**5万美元**额度。注册需为学术或非营利机构的 PI 或同等身份。生物与化学方向研究者仍限用 Opus 级模型，Fable 模型继续屏蔽专业生物学与药物开发查询；与美国政府合作的生命科学 Mythos 级模型访问计划已录取首批参与者。
  > 💡 免费/折扣席位加算力额度的组合，是在科研群体中培养使用习惯并绑定科学智能工作流的双轨打法，直接对标 Google、OpenAI 的科研补贴竞赛。
   - 来源: [Anthropic](https://www.anthropic.com/news/expanding-support-for-scientists) | [@claudeai](https://x.com/claudeai/status/2093059087298601113)

**OpenAI联合百余家机构发起集体网络防御倡议，Anthropic、Google、Microsoft均在署名之列**
- OpenAI 发布集体网络防御倡议，称未来数月 AI 驱动的网络攻击将随模型能力提升而更普遍、更复杂，医院、水处理厂等关键基础设施面临风险，并提出三项原则：承认现状安全水平不够、用具备网络能力的 AI 武装更多防御者、动员集体响应。署名方超过**120家**，包括 Anthropic、Google、Microsoft、AWS、Cloudflare、CrowdStrike、Palo Alto Networks、Mastercard、Visa、Citi 等安全厂商、云厂商与金融机构。倡议分别向各类组织、网络安全公司、政府和前沿AI公司提出行动清单，包括加速修复高风险弱点、对 AI 生成代码提高安全标准、政府资助关键基础设施防御等。
  > 💡 前沿AI公司罕见地与主要竞争对手及整个安全产业集体署名，把"防御者窗口期"框定为公共议程——这既是防御姿态，也是在为 offensive AI 能力扩散提前建立行业治理框架。
   - 来源: [OpenAI](https://openai.com/collective-cyberdefense/) | [@OpenAI](https://x.com/OpenAI/status/2093074192636018977)

**Terminal-Bench-Science科学工作流基准发布：70个任务，Claude Opus 5解决率仅约30%**
- Terminal-Bench-Science 是评估 AI Agent 在跨科学领域研究工作流上表现的基准，由 Terminal-Bench 团队联合全球科研机构的领域专家共同建设，是斯坦福牵头的持续性社区项目。v0.1 版本包含**70个任务**；作为参照，Claude Opus 5 在其上的解决率仅约**30%**。
  > 💡 从通用终端任务转向真实科研工作流，头部模型解决率随即遭腰斩——与同日 FrontierChallenge 的 Pass Rate 20.6% 相互印证，科学 Agent 的能力缺口比通用 Agent 榜单显示的大得多。
   - 来源: [Terminal-Bench-Science](https://www.terminal-bench-science.ai/) | [@StevenDillmann](https://x.com/StevenDillmann/status/2093041660615852448)

**fal基于MiniMax H3后训练发布H3 Max：5秒视频约3秒生成，人评质量三项第一**
- fal 基于开源权重的 MiniMax H3 做后训练并协同设计推理系统，推出 H3 Max：生成5秒视频约需3秒，约为官方 MiniMax H3 端点吞吐的**35倍**。在与12个主流视频模型（含官方 H3、Gemini Omni Flash、Wan 3.0、Seedance 2.5、Kling 3、Veo 3.1）的人工偏好对比中，H3 Max 在整体质量、提示理解、美学三个维度均排名第一，对每个对比模型都赢得多数对决；Artificial Analysis 与 Design Arena 的独立榜单亦排名第一。模型在 NVIDIA GB200 NVL72 系统上完成训练与部署，首周半价，已在 fal Playground 与 API 上线。
  > 💡 后训练与推理栈协同设计把"质量-速度"权衡边界整体外推——在开源权重之上，推理优化能力正成为模型发行方之外的第二层竞争力，也验证了"开放权重+基础设施厂商"分工模式的商业可行性。
   - 来源: [fal Blog](https://blog.fal.ai/introducing-h3-max-by-fal/) | [@fal](https://x.com/fal/status/2093068605114204456)

---
*更新时间: 2026-08-28 09:40*