## 04月22日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 共 11 条

---

## 要点汇总

- 模型前沿：Claude Opus 4.7在ECI评测并列第三，GPT-5.4 Pro以158分领先; Ant Group发布Ling-2.6-flash（Elephant Alpha）; Kimi K2.6登顶开源智能体模型
- 产业动态：Google发布Gemini Deep Research Max; OpenAI Codex推出Chronicle屏幕记忆功能; SpaceX与Cursor合作开发编程AI，获600亿美元收购期权
- 算力追踪：AMD与GlobalFoundries合作开发MI500 CPO光互连方案
- 初创&融资：自变量机器人完成近20亿元B轮融资; NeoCognition获4000万美元种子轮
- X讨论：PrismML发布首个商用1-bit LLM; OpenAI Codex两周内用户从300万增至400万

---

## 详细参考

### 模型前沿

**Claude Opus 4.7在ECI评测并列第三，GPT-5.4 Pro以158分领先**
- Epoch AI发布最新ECI评测：**GPT-5.4 Pro以158分领先，Gemini 3.1 Pro 157分第二，Claude Opus 4.7与GPT-5.4并列156分**。Opus 4.7相比上代Opus 4.6（155分）提升1分。值得注意的是，Opus 4.7在编程专项MCP-Atlas上以77.3%领先GPT-5.4（68.1%）和Gemini 3.1 Pro（73.9%），**说明综合指数接近但编程能力已拉开差距**。
  > ECI前四名分数集中在154-158（仅4分差距），前沿模型的综合能力正在趋同，区分度转向编程、Agent等垂直能力。Anthropic以$5/$25定价达到与$15/$60的GPT-5.4并列，性价比优势明显。
  - 来源: [Epoch AI](https://epochai.substack.com/p/opus-47-scores-near-frontier-on-eci)

**Ant Group发布Ling-2.6-flash：104B/7.4B MoE模型，此前以"Elephant Alpha"匿名霸榜OpenRouter**
- Ant Group旗下inclusionAI发布Ling-2.6-flash，**104B总参数/7.4B激活参数的MoE架构**，激活率仅约7%，专为Agent任务的高token效率设计。该模型此前以匿名身份"Elephant Alpha"在OpenRouter上运行——256K上下文、32K最大输出、免费使用，社区猜测数周后于4月21日揭晓真实身份。**7.4B激活参数达到接近同级别全激活模型的效果，意味着推理成本可以大幅降低**。
  > Ling-2.6-flash延续了MoE架构"以总参数换激活效率"的路线，7%的极端激活率将推理成本压缩到极致。
  - 来源: [@OpenRouter](https://x.com/OpenRouter/status/2046663557899813181#m)

**Kimi K2.6登顶开源智能体模型，Claw-Eval pass³ 62.3%并展示长程编码**
- Moonshot AI发布Kimi K2.6，在Claw-Eval评测中以**pass³ 62.3%位列开源模型第一、总榜第四**，pass@3达80.9%。同时展示了长程编码能力：自主下载并部署Qwen3.5-0.8B模型。HLE with Tools达54.0（+3.8），OSWorld-Verified 73.1%。
  >据社区测算，K2.6价格约为Claude Opus的1/8。权重已开源。
  - 来源: [@kimi_moonshot](https://x.com/_TobiasLee/status/2046493043285737582#m)

### 产业动态

**Google发布Gemini Deep Research Max：基于Gemini 3.1 Pro的企业级自主研究Agent**
- Google发布下一代Deep Research Agent，推出两个版本：Deep Research（低延迟交互场景）和Deep Research Max（最大深度，利用扩展推理计算）。**基于Gemini 3.1 Pro，新增MCP支持、原生图表/信息图生成、多模态输入（PDF/CSV/图片/音频/视频）**。Max版面向异步批量场景（如夜间自动生成尽调报告），可同时搜索网页、远程MCP服务器、文件存储。已在Gemini App、NotebookLM、Google Finance中部署。**正在与FactSet、S&P、PitchBook合作MCP服务器设计**。
  > Google将Deep Research从"研究工具"升级为"企业工作流基础设施"，MCP支持意味着可接入任何专业数据源。
  - 来源: [Google Blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/next-generation-gemini-deep-research/)

**OpenAI Codex推出Chronicle屏幕记忆功能**
- OpenAI为Codex推出Chronicle功能，**持续捕获用户屏幕内容以构建记忆上下文**。这是上周发布的Codex memory功能的扩展——Codex现在可以记住用户正在做的事情，在后续编码任务中利用这些上下文。功能一经公布即引发隐私担忧，**持续截屏可能包含密码、私钥等敏感信息**。
  > 屏幕记忆是AI编程从"工具"走向"同事"的关键一步，但隐私风险可能成为企业采用的障碍。这也说明编程工具竞争已从模型能力转向上下文理解和工作流整合——与今天SpaceX/Cursor的交易形成呼应，AI编程赛道的竞争维度正在从推理质量扩展到记忆、上下文、算力整合。
  - 来源: [@OpenAIDevs](https://x.com/OpenAIDevs/status/2046288243768082699)

**SpaceX与Cursor合作开发编程AI，获600亿美元收购期权**
- SpaceX宣布与Cursor合作开发下一代编程AI，协议包含惊人条款：**SpaceX可在今年晚些时候以$60B收购Cursor，或支付$10B作为合作费用**。结合SpaceX Colossus超算（百万H100等效算力）与Cursor的程序员分发能力。此前Cursor两名最高级工程师已跳槽至xAI直接向Musk汇报，xAI也开始向Cursor出租数万张GPU。Cursor估值从2025年1月$2.5B飙升至11月D轮后的$29.3B，**收购价$60B是D轮的2倍**。
  >Cursor至今仍依赖Claude和GPT模型，而Anthropic和OpenAI正推出自己的编程工具与Cursor直接竞争。
  - 来源: [TechCrunch](https://techcrunch.com/2026/04/21/spacex-is-working-with-cursor-and-has-an-option-to-buy-the-startup-for-60-billion/)

### 算力追踪

**AMD与GlobalFoundries合作开发MI500 CPO光互连方案**
- AMD将为下一代Instinct MI500加速器开发基于MRM的**CPO（Co-Packaged Optics，共封装光学）解决方案**。PIC（光子集成电路）由GlobalFoundries制造，日月光负责封装。CPO将光互连直接集成在芯片封装内，可大幅提升AI集群的互连带宽和能效。
  > CPO是突破AI训练集群通信瓶颈的关键技术路径，与今天SemiAnalysis报告的网络议题直接呼应。AMD选择GlobalFoundries（而非台积电）做PIC制造，反映供应链多元化策略。
  - 来源: [36氪/财联社](https://36kr.com/newsflashes/3776438293005064?f=rss)

### 初创&融资

**自变量机器人完成近20亿元B轮融资，四家互联网大厂齐聚**
- 具身智能公司"自变量机器人"完成近20亿元B轮融资，**小米战投和红杉中国领投**。此前美团（A轮）、阿里（A+轮）、字节（A++轮）分别领投或独投。自变量已成为**国内唯一同时被美团、阿里、字节、小米四家互联网大厂投资的具身智能企业**。
  > 四家大厂同时押注同一家具身智能公司，说明具身智能赛道已进入"下注窗口期"。
  - 来源: [36氪](https://36kr.com/newsflashes/3776193532281346?f=rss)

**NeoCognition获4000万美元种子轮，构建自学习Agent**
- Ohio State大学教授Yu Su创办的NeoCognition以**$40M种子轮融资出隐身模式**。Cambium Capital和Walden Catalyst领投，Vista Equity Partners、Intel CEO Lip-Bu Tan、Databricks联创Ion Stoica参投。团队约15人，多数为PhD。**核心思路：让Agent像人类一样通过自主学习成为任何领域的专家**（构建微世界模型），而非针对特定垂直手工工程化。面向企业SaaS公司销售Agent系统。
  > $40M种子轮反映Agent赛道融资热度。Vista（最大软件PE之一）的参与提供了企业客户渠道。但当前Agent可靠性仅约50%，"自学习Agent"的可靠性问题是整个行业的共同挑战。
  - 来源: [TechCrunch](https://techcrunch.com/2026/04/21/ai-research-lab-neocognition-lands-40m-seed-to-build-agents-that-learn-like-humans/)

### X讨论

**PrismML发布首个商用1-bit LLM：8.2B参数仅1.15GB，可运行于iPhone**
- Caltech孵化的PrismML发布**首个端到端1-bit LLM** Bonsai 8B：8.2B参数全1-bit量化，内存占用仅1.15GB，比同参数量16-bit模型小14倍。**在iPhone 17 Pro上以40 tok/s运行**，M4 Pro上131 tok/s，RTX 4090上368 tok/s。智能密度达1.06/GB，是Qwen3 8B（0.10/GB）的10倍。同时发布4B和1.7B版本，Apache 2.0开源。Khosla Ventures、Cerberus和Google参投。
  > 1-bit量化首次证明可以在不损失推理能力的前提下实现商用级精度，AI从云端走向端侧的关键瓶颈被突破。如果专用1-bit硬件落地，推理效率可能再提升一个数量级。
  - 来源: [@prismml](https://x.com/ronaldmannak/status/2046612331350962666#m)

**OpenAI Codex两周内用户从300万增至400万，AI编程工具进入爆发期**
- OpenAI Codex周活跃用户**两周内从300万增至400万（增长33%）**。结合此前数据：Codex三个月内实现5倍增长，MoM增长率持续70%以上。**对比Cursor（~400万DAU）和GitHub Copilot（~180万订阅），Codex增速已超越所有竞品历史曲线**。OpenAI不得不反复重置速率限制，反映算力供应压力。
  > AI编程工具用户增长已从早期采用者进入主流爆发期，Codex两周增长100万说明需求远未被满足。
  - 来源: [@sama](https://x.com/sama/status/2046604989527912590)


---
*更新时间: 2026-04-22 (已修订)*
