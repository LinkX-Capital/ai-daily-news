## 05月21日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：OpenAI通用模型解决Erdős平面单位距离问题，近80年数学开放问题首获突破; 千问发布Qwen3.7-Max旗舰模型，面向智能体时代
- 产业动态： Stability AI发布Stable Audio 3.0，开源音乐模型可生成6分钟歌曲; OpenAI准备数周内提交IPO申请，与Anthropic竞逐AI公司上市第一股; SpaceX S1文件披露与Anthropic最高400亿美元云服务协议; VERL-Omni团队发布通用RL后训练框架; Google发布Gemini for Science工具集
- 算力追踪：NVIDIA季度营收816亿美元同比增长85%，持有初创公司股份估值430亿美元; 平头哥发布真武M890 AI芯片，128卡超节点服务器已上线阿里云
- 初创&融资：NanoClaw创始人拒绝2000万美元收购，转而完成1200万美元种子轮融资; IrisGo获Andrew Ng领投280万美元种子轮，打造桌面AI助手
- 研究关注：ACL 2026论文VChain为视频生成引入视觉思维链; WEM提出世界-自我解耦的具身世界模型新范式; SWEET用图像编辑替代视频生成做具身规划
- X讨论：Sam Altman展望AGI三大加速方向：科研、企业和个人; swyx："读-想-问"迭代循环优于单向深度研究

---

## 📖 详细参考

### 模型前沿
**OpenAI通用模型解决Erdős平面单位距离问题，为近80年数学开放问题首获突破**
- OpenAI宣布其通用推理模型解决了**平面单位距离问题（planar unit distance problem）**，该问题由数学家Paul Erdős于**1946年**提出，是组合几何领域的经典开放问题。近80年来数学界普遍认为最优解大致为方形网格结构，OpenAI模型发现了**全新的构造族**，性能优于方形网格，从而推翻了这一假设。OpenAI称这是**首次由AI自主解决数学领域核心开放问题**。Sam Altman表示这是重要里程碑，但对AI对数学认知的影响有复杂感受。菲尔兹奖得主Timothy Gowers转发时提醒数学同行"坐稳了再看"。
  > 💡 通用模型（非专门数学系统）自主解决80年开放问题，标志着AI在数学推理上从辅助工具迈向独立研究者的范式转变
   - 来源: [@OpenAI](https://x.com/OpenAI/status/2057176201782075690#m), [@sama](https://x.com/sama/status/2057203171198636251#m)

**千问发布Qwen3.7-Max旗舰模型，面向智能体时代，编程与推理多项benchmark领先**
- 阿里千问团队发布**Qwen3.7-Max**，定位"面向智能体时代的新一代旗舰模型"。编程智能体方面，SWE-Pro得分**60.6**、SWE-Verified **80.4**（与Opus-4.6 Max的80.8相当），Terminal Bench 2.0-Terminus **69.7**超越DeepSeek-V4-Pro Max的67.9。通用智能体方面，MCP-Mark **60.8**、MCP-Atlas **76.4**、Skillbench **59.2**均领先。推理方面，GPQA Diamond **92.4**（超越Opus-4.6的91.3）、HLE **41.4**、HMMT 2026 Feb **97.1**。最大亮点：在一项**35小时连续自主执行**的GPU kernel优化实验中，模型完成**1158次工具调用**，在从未见过的硬件平台（平头哥真武M890 PPU）上将SGLang Extend Attention kernel加速**10.0x**，显著超越GLM 5.1（7.3x）、Kimi K2.6（5.0x）、DeepSeek V4 Pro（3.3x）。模型支持Claude Code、OpenClaw、Qwen Code等多种智能体框架的跨框架泛化，即将通过阿里云百炼API提供服务。
  > 💡 Qwen3.7-Max在长程自主执行（35h/1158次工具调用）上的表现是关键差异化能力，环境扩展方法带来的泛化性而非过拟合特定框架是其技术路线的核心
   - 来源: [阿里研究院](https://mp.weixin.qq.com/s/dE5A43cQNzxpi3Chd6Cr9g)

### 产业动态
**Stability AI发布Stable Audio 3.0，开源音乐模型可生成6分钟歌曲，支持设备端完整作曲**
- Stability AI发布**Stable Audio 3.0**模型家族，采用全新语义-声学自编码器架构。三个开源权重版本：**3.0 Small SFX**（音效）、**3.0 Small**（最长2分钟完整音乐，据称为目前唯一支持设备端完整作曲的模型）、**3.0 Medium**和3.0 Large（生成超过**6分钟**音乐）。支持**可变长度生成**（精确到秒的粒度）、**音频修复**（单段/多段编辑、因果续写）和**LoRa微调**（首次发布音频LoRa训练文档）。所有模型基于**完全授权数据**训练，Stability AI Community License下用户拥有输出版权并可商用。已与Universal Music Group和Warner Music Group达成合作。3.0 Small和Medium权重已在HuggingFace开放下载，Large通过API提供。
  > 💡 设备端完整作曲+6分钟生成+授权数据训练的组合，是开源音频生成模型的里程碑；LoRa微调文档的发布将推动社区定制化
   - 来源: [Stability AI](https://stability.ai/news-updates/meet-stable-audio-3-the-model-family-built-for-artistic-experimentation-with-open-weight-models), [TechCrunch](https://techcrunch.com/2026/05/20/stability-ai-release-a-new-audio-model-that-can-create-six-minute-songs/)

**OpenAI准备数周内提交IPO申请，Goldman Sachs和Morgan Stanley起草招股书**
- 据报道，OpenAI正准备在未来数周内提交IPO申请。**Goldman Sachs**和**Morgan Stanley**一直在起草IPO招股书。此举可能加速OpenAI的上市进程，使其在与竞争对手Anthropic的"谁先到达公开市场"竞赛中占得先机。此前Anthropic CEO Dario Amodei曾表示Anthropic也可能在未来考虑上市。
  > 💡 OpenAI与Anthropic竞逐AI公司上市第一股，标志AI行业从融资驱动进入资本市场验证阶段
   - 来源: [The Information](https://www.theinformation.com/briefings/openai-prepares-file-ipo-coming-weeks)

**SpaceX S1文件披露：xAI去年亏损64亿美元，Anthropic云协议最高400亿，计划2028部署轨道AI数据中心**
- SpaceX S1文件首次公开xAI财务数据：2025年运营亏损**64亿美元**，收入仅32亿美元（亏损同比从15.6亿扩大至64亿）。AI部门capex从2025全年127亿美元飙升至2026Q1单季**77亿美元**（年化约308亿美元）。Grok AI月活用户**1.17亿**（占X+Grok 5.5亿总MAU的约五分之一）。文件披露已与Anthropic签署**最高400亿美元**云服务协议，下一代Grok将扩展至"**万亿级参数**"。Colossus和Colossus II数据中心合计提供约**1GW**算力。SpaceX计划最早**2028年**部署轨道AI计算卫星，称"AI的未来将由物理栈的控制权决定"。潜在估值**1.75万亿美元**。
  > 💡 SpaceX将航天基础设施与AI算力结合的商业模式初现轮廓；64亿美元年亏损+308亿年化capex说明Musk在AI上的赌注远超市场预期
   - 来源: [TechCrunch](https://techcrunch.com/2026/05/20/xai-burned-6-4b-last-year-spacexs-ipo-filing-shows-why-the-spending-is-far-from-over/), [@semianalysis_](https://x.com/SemiAnalysis_/status/2057218884051034412#m), [The Information](https://www.theinformation.com/articles/spacex-reveals-40-billion-anthropic-deal-catch)

**VERL-Omni团队发布通用RL后训练框架，支持多模态生成模型统一微调**
- VERL-Omni团队发布通用强化学习后训练框架，面向多模态生成模型。该框架基于VERL和vLLM-Omni构建，支持视觉、语言、音频等多模态任务的统一训练。vLLM-Omni负责多模态rollout的step-wise连续批处理和embedding缓存；vLLM同时充当VLM-as-judge/OCR奖励模型，与rollout和训练重叠执行。在Qwen-Image OCR演示中，将reward移至独立GPU可将单步wall-clock时间降低约**14%**。已发布Qwen-Image的FlowGRPO/MixGRPO/GRPO-Guard训练方案，BAGEL和Qwen3-Omni-Thinker PR已就绪。
  > 💡 多模态生成式RL后训练此前缺乏统一框架，VERL-Omni的连续批处理+reward重叠执行设计对工程效率提升明显
   - 来源: [@vllm_project](https://x.com/vllm_project/status/2056912763172364350#m), [GitHub](https://github.com/verl-project/verl)

**Google发布Gemini for Science工具集，含三大实验性工具与Science Skills工具包**
- Google推出**Gemini for Science**，包含三大实验性工具：**Hypothesis Generation**（基于Co-Scientist，通过多Agent"想法锦标赛"生成并验证假设，带可点击引用）、**Computational Discovery**（基于AlphaEvolve和ERA，并行生成和评分数千个代码变体以加速计算实验）、**Literature Insights**（基于NotebookLM，将文献搜索结果结构化为可对比分析的表格）。同时发布**Science Skills**工具包，集成**30+**生命科学数据库（UniProt、AlphaFold、AlphaGenome等），可在Antigravity平台上将结构生物信息学和基因组分析从数小时缩短至数分钟。ERA和Co-Scientist相关论文已在Nature发表。已与**100+**机构合作（包括Stanford、Imperial College London、The Crick Institute），目前以trusted tester模式在labs.google/science开放注册。
  > 💡 Google从AlphaFold单点工具演进到多Agent科学工作流编排，Co-Scientist的"想法锦标赛"模式是AI辅助科研的新范式
   - 来源: [Google Blog](https://blog.google/innovation-and-ai/technology/research/gemini-for-science-io-2026/), [@googleai](https://x.com/GoogleAI/status/2057161314825584892#m)

### 算力追踪
**NVIDIA季度营收超预期达816亿美元，同比增长85%，持有初创公司股份估值430亿美元**
- NVIDIA公布截至4月26日三个月营收达816亿美元，同比增长85%，超出市场预期。公司同时披露持有初创公司股权估值430亿美元。但NVIDIA预计下一季度营收增速将环比放缓。
  > 💡 NVIDIA营收增速仍强劲但增长放缓预示拐点，430亿美元持仓反映其生态控制力
   - 来源: [TechCrunch](https://techcrunch.com/2026/05/20/nvidia-posts-another-record-quarter-reveals-43-billion-of-holdings-in-startups/)

**平头哥发布真武M890 AI芯片与128卡超节点服务器，已上线阿里云百炼**
- 阿里在2026阿里云峰会上发布基于平头哥新一代AI芯片**真武M890**的磐久AL128超节点服务器。真武M890内置**144GB显存**，性能为上代真武810E的**3倍**，片间互联带宽**800GB/s**，原生支持FP32到FP4多种数据精度。搭配自研互联芯片ICN Switch 1.0（吞吐量**25.6Tbps**），128张AI芯片通过单机柜紧密耦合互联，P2P时延低于**150ns**，单柜带宽达Pb/s级，可视为"128张卡组成一台计算机"。已上线阿里云百炼，支持Qwen、DeepSeek、Kimi等主流模型。自研T-Head SAIL软件栈提供端到端支撑。真武系列芯片已累计出货**56万片**，服务20+行业400+客户。未来两年将推出算力更强的真武V900和J900。
  > 💡 真武M890是Qwen3.7-Max的35小时kernel优化实验所用硬件；128卡超节点+百纳秒时延直指Agent时代海量并发推理需求
   - 来源: [平头哥半导体](https://mp.weixin.qq.com/s/GhLLVM3TgJXYPxR1WpTsAQ), [The Information](https://www.theinformation.com/briefings/alibaba-unveils-new-ai-chip-china-accelerates-adoption-domestic-chips)

### 初创&融资
**NanoClaw创始人拒绝2000万美元收购，转而完成1200万美元种子轮融资**
- NanoCo（安全沙箱化OpenClaw替代品**NanoClaw**的开发商）完成**1200万美元**超额认购种子轮，由Valley Capital Partners领投，Docker、Vercel、Monday.com、Slow Ventures参投，Hugging Face CEO Clem Delangue等天使投资人跟投。创始人Gavriel Cohen和Lazer Cohen兄弟在获得Andrej Karpathy推文背书和新加坡外交部长称其为"第二大脑"的病毒式传播后，先后收到两份收购要约（六位数及约**2000万美元**），均被拒绝。从写下第一行代码到签署term sheet仅**不到6周**。NanoClaw运行在容器化沙箱中，已与Docker和Vercel达成合作，Amazon、Google、Meta等公司高管在使用中，已开始提供企业部署服务。
  > 💡 开源安全Agent赛道验证：拒绝收购选择融资，说明创始人看好独立发展路径；Karpathy+外交部长背书的病毒传播模式值得研究
   - 来源: [TechCrunch](https://techcrunch.com/2026/05/20/nanoclaw-creator-turns-down-20m-buyout-offer-raises-12m-seed-instead/)

**IrisGo获Andrew Ng领投280万美元种子轮，打造主动式桌面AI助手**
- IrisGo完成**280万美元**种子轮，由Andrew Ng的AI Fund领投，Nvidia和Google参投。创始人Jeffrey Lai（前Apple工程师，参与中文版Siri开发）打造的桌面AI助手可**观察用户桌面行为并自动学习工作流**——演示一次即可记住流程并在未来自动执行。产品内置技能库（邮件起草、发票处理、报告生成等），同时从用户行为中自动发现可自动化任务。采用**混合架构**：部分数据处理在设备端完成以保护隐私，复杂任务经用户授权后通过端到端加密上传云端。已发布macOS和Windows beta版，并与Acer达成**预装协议**。Iris这个名字是Siri的反写。
  > 💡 "观察学习+自动执行"的主动式AI助手区别于被动prompt模式，预装策略是触达用户的关键渠道
   - 来源: [TechCrunch](https://techcrunch.com/2026/05/20/irisgo-a-startup-backed-by-andrew-ng-looks-to-become-the-ai-desktop-buddy-you-never-knew-you-needed/)

### 研究关注
**ACL 2026接收论文VChain：为视频生成引入视觉思维链推理**
- Ziqi Huang（南洋理工大学）等作者提出**VChain**框架，针对视频生成模型在复杂动态因果链上的薄弱环节，引入推理时（inference-time）**视觉思维链（Chain-of-Visual-Thought）**机制。核心方法：利用大语言多模态模型（如GPT-4o）的视觉状态推理能力，先生成一组**稀疏关键帧**作为时间线上的"快照"，再仅在这些关键时刻对预训练视频生成器进行**稀疏推理时调优**。该方案tuning效率高，引入最小额外开销且避免密集监督。在复杂多步骤场景的实验中显著提升生成质量。作者包括Paul Debevec和Ziwei Liu。
  > 💡 VChain将LLM的推理能力"注入"视频生成管线，思路不同于常见的端到端训练；稀疏调优策略在效率和质量间取得平衡
   - 来源: [arXiv](https://arxiv.org/abs/2510.05094), [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651034077&idx=3&sn=10890eda5f07b911cf486dfecc8e6ecd&chksm=85ab667f1cb44d11e31c081b5556fd2b4a31fa9dcad2c174f55d9b01d4ffd2872015fd45cb0a&scene=0&xtrack=1#rd)

**WEM：提出世界-自我解耦的具身世界模型新范式，构建混合导航-操作长程评测基准**
- Zuyao Lin等提出**World-Ego Modeling（WEM）**，指出当前具身世界模型将"世界演化"（场景规律）和"自我演化"（机器人动态）纠缠在同一预测流中，导致长程混合任务（导航+操作交替）性能退化。论文从运动、语义、意图三个视角定义世界-自我边界，分析前/后/全三种解耦策略，并提出**WEM模型**：隐式分离的世界-自我规划器 + 级联并行MoE扩散生成器。同时构建**HTEWorld**基准，包含**12.5万视频片段**（超450万帧）、细粒度动作标注和300条多轮评测轨迹（超2000条指令），是目前首个面向混合导航-操作任务的长程世界建模评测。WEM在HTEWorld上达到SOTA，同时在纯操作基准上保持竞争力。
  > 💡 世界-自我解耦思路将"场景不变量"和"机器人动态"分离预测，与VChain的稀疏关键帧思路有异曲同工之处；HTEWorld填补了混合任务评测的空白
   - 来源: [arXiv](https://arxiv.org/abs/2605.19957)

**SWEET：用图像编辑替代视频生成做具身规划，推理成本大幅降低**
- Yiren Song、Mike Zheng Shou等提出**SWEET**，质疑具身控制中密集视频生成的必要性。论文对比视频生成模型Wan2.2和图像编辑模型FLUX-Kontext，发现图像编辑在生成任务级关键帧时**视觉保真度更高且推理成本大幅降低**。基于此提出一次性稀疏视觉规划框架：通过逐步图像编辑生成任务相关操作关键帧序列，再用目标条件扩散动作预测器将相邻关键帧转化为可执行动作块。引入混合训练策略（filtered edited targets）减少真实与编辑视觉子目标间的差异。在DROID和RoboMimic上的实验表明SWEET在可见和未见场景中均提升关键帧预测质量，并打通了从关键帧规划到可执行机器人动作的完整管线。
  > 💡 用图像编辑替代密集视频rollout是降低具身视觉规划成本的有效路径，与WEM的稀疏世界建模思路形成互补
   - 来源: [arXiv](https://arxiv.org/abs/2605.19319)

### X讨论
**Sam Altman展望AGI三大加速方向：科研、企业和个人**
- Sam Altman在Nothing But Tech播客中阐述OpenAI三大方向：**加速科学研究**（预计数学进展将"令人惊叹"，AI可能推动阿尔茨海默症等疾病研究，明年或有成果）、**加速经济生产力**（AI正在催生"自动化创业"，小团队甚至一人公司可借助AI构建产品，他称"两个创始人加一万块GPU"是新范式）、**个人AGI**（让每个人都拥有理解自己全部上下文和生活背景的AI助手）。他还指出**机器人和自动化制造**是关键领域，认为"计算机能完成高级智力任务但人类仍需充当物理执行器"的未来不可接受。这番发言紧随OpenAI数学突破公布之后。
  > 💡 Altman从技术突破转向应用叙事，"AGI加速"框架试图定义AI商业化的下一阶段；"一人公司"的说法将AGI叙事从企业下沉到个人
   - 来源: [@sama](https://x.com/sama/status/2057218997503086888#m)

**swyx："读-想-问"迭代循环优于单向深度研究**
- swyx认为，自OpenAI o3发布后深度研究模式已基本失效。他对比两种模式：**thoughtless prompt → long report nobody reads**（无脑prompt出长篇报告没人看）不如 **read → think → ask** 的迭代循环——对主动学习和意图获取，交互性远比单向信息检索重要。
  > 💡 该观点代表部分从业者对DeepResearch类产品的反思，但"深度研究已死"系个人判断非行业共识
   - 来源: [@swyx](https://x.com/swyx/status/2057064854679331177#m)

---
*更新时间: 2026-05-21 08:15*