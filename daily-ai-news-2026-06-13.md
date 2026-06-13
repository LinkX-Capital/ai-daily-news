## 06月13日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：Moonshot开源Kimi-K2.7-Code编码模型，Kimi Code Bench v2提升21.8%
- 产业动态：美国政府强制下架Anthropic Claude Fable 5和Mythos 5，引发AI安全审查争议; OpenAI收购Ona，扩展Codex持久化Agent能力
- 算力追踪：Artificial Analysis发布AA-AgentPerf基准，NVIDIA GB300达61,354 Agents/MW
- 初创&融资：贝佐斯Prometheus完成120亿美元融资，估值410亿美元; Theker完成8500万美元A轮，打造通用可重构工厂机器人; Equal AI完成3000万美元B轮，印度AI来电筛选突破百万月活; Mistral据传融资30亿欧元，估值200亿欧元
- 研究关注：阿里与清华ViT³入围CVPR 2026最佳论文决选，推理时在线学习实现线性复杂度; 清华季向阳团队MPTS：以难度预测替代全量评估，降低大模型与具身Agent训练交互成本; World Labs发布三篇3D/空间智能研究; Xu等提出EvoArena框架揭示Agent在动态环境平均准确率仅39.6%; Cho等提出SpatialClaw，以代码为动作接口在20个空间推理基准达59.9%准确率; BlendIn（ACL 2026）按可靠性加权混合多模型输出实现LLM推理时对齐
- X讨论：Chelsea Finn团队分享DIRECT测试时计算路由与多机器人VLA协同两项研究; Google DeepMind可解释性团队提出Model Diffing Agents：自动发现模型间行为差异

---

## 📖 详细参考

### 模型前沿
**Moonshot开源Kimi-K2.7-Code编码模型，Kimi Code Bench v2提升21.8%**
- Moonshot AI发布并开源最新编码模型Kimi-K2.7-Code。相比上代K2.6，在Kimi Code Bench v2上提升**+21.8%**，Program Bench提升**+11.0%**，MLS Bench Lite提升**+31.5%**。推理效率方面，过度思考显著减少，推理token消耗降低**30%**。长程编码能力改善指令遵从和端到端编码任务成功率。同时预告**6倍高速模式**即将上线。模型已通过Kimi API和Kimi Code产品提供服务。
  > 💡 推理token消耗降低30%同时benchmark大幅提升，说明K2.7在编码场景的"思考效率"有结构性改进而非单纯堆参数。6倍高速模式若落地将进一步降低API调用成本，直接与Claude Code/GitHub Copilot在编码Agent赛道竞争。
   - 来源: [@kimi_moonshot](https://x.com/Kimi_Moonshot/status/2065377579130142937#m)

### 产业动态
**美国政府强制下架Anthropic Claude Fable 5和Mythos 5，引发AI安全审查争议**
- 美国政府以国家安全为由，命令Anthropic立即关闭Claude Fable 5和Claude Mythos 5两个模型的所有用户访问权限，指令于美东时间周五17:21收到。Anthropic已合规执行，但在博客文章中公开表达不满，称"发现一个狭窄的潜在越狱不应成为召回面向数亿用户商业模型的理由"。Mythos是Anthropic能力最强的模型，曾发现所有主流操作系统和浏览器的安全漏洞，此前仅通过Project Glasswing项目与约50家审查合格的组织（包括Amazon、Apple、Google、Microsoft、CrowdStrike）共享用于防御性网络安全工作。Fable 5于三天前发布，是加装安全护栏后的公开版本，据Vals AI基准测试为当时最强公开AI模型。政府称发现Fable 5存在"潜在狭窄、非通用越狱"，但Anthropic指出该能力在GPT-5.5等其他公开模型中已广泛存在。Sam Altman此前曾批评Anthropic对Mythos的处理方式是"恐惧营销"。
  > 💡 这是美国政府首次以国家安全为由强制下架前沿AI模型，Anthropic高调的安全叙事反而引来了最严厉的监管后果。该事件可能直接影响整个行业的模型发布策略——如果"狭窄越狱"成为下架标准，OpenAI、Google等厂商的新模型部署同样面临风险。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/12/anthropics-safety-warnings-may-have-just-backfired-the-government-has-pulled-the-plug-on-its-most-powerful-ai/)

**OpenAI收购Ona，扩展Codex持久化Agent能力**
- OpenAI宣布收购Ona，将其安全云执行与编排技术整合进Codex生态。Codex目前每周有**超过500万用户**，较今年初增长**400%**。Ona的技术提供安全、持久的环境，使Agent能在用户关闭设备后继续工作，已帮助**200万开发者**在安全、可复现的云环境中工作。收购后，Codex将能扩展到单设备或活跃会话之外，支持Agent在客户自有云环境中运行，同时满足安全、治理和运维要求。交易需通过常规监管审批。
  > 💡 Codex从编码工具演变为持续性Agent平台，Ona的云执行能力是关键拼图——使Agent能"脱离笔记本"独立运行数小时乃至数天。这直接对标企业级Agent部署的需求，也是OpenAI在Agent基础设施层面与Anthropic Computer Use的差异竞争。
   - 来源: [OpenAI](https://openai.com/index/openai-to-acquire-ona)

### 算力追踪
**Artificial Analysis发布AA-AgentPerf：首个Agentic推理基准，NVIDIA GB300达61,354 Agents/MW**
- Artificial Analysis发布业界首个Agentic推理基准AA-AgentPerf，核心指标为**Agents per Megawatt**（每兆瓦可承载并发Agent数）。该基准回放真实编码Agent轨迹（最多200轮对话，序列长度超过100K token），并首次允许生产环境优化（KV cache复用、投机解码、prefill/decode分离）。首轮结果基于DeepSeek V4 Pro（最低服务级别：20 tokens/s，P95 TTFT ≤ 10s）：NVIDIA **GB300**（机架级，分离式推理）达到**61,354 Agents/MW**，**B300**（单节点）为**21,053 Agents/MW**，AMD **MI355X**为**3,551 Agents/MW**，NVIDIA **H200**为**2,594 Agents/MW**。机架级分离推理的功耗效率约为单节点Blackwell的3倍。值得注意的是，MI355X的配置仅优化约两周且无法稳定使用投机解码，AMD性能仍有较大提升空间。
  > 💡 AA-AgentPerf是业界首个针对真实Agent工作负载的基础设施评估基准——传统合成基准无法反映Agent的长上下文、短输出、KV cache密集复用特征。GB300的机架级优势表明，Agent推理的瓶颈正在从单卡算力转向系统级架构（网络、内存层级、调度器）。
   - 来源: [Artificial Analysis](https://artificialanalysis.ai/articles/aa-agentperf) | [@ArtificialAnlys](https://x.com/ArtificialAnlys/status/2065559824230957190)

### 初创&融资
**贝佐斯Prometheus完成120亿美元融资，估值410亿美元，打造"通用人工工程师"**
- Prometheus由Jeff Bezos与Vik Bajaj（Verily联合创始人、Google生命科学部门前负责人）联合创立，完成**120亿美元**新一轮融资，估值**410亿美元**。投资方包括贝佐斯本人、JPMorgan Chase、Goldman Sachs和BlackRock。这是公司第二轮融资——去年底首轮融资**62亿美元**。Prometheus正在构建"通用人工工程师"（artificial general engineer），即能自动化设计和制造复杂物理系统的软件，覆盖喷气发动机到药物分子设计。公司目前在旧金山、伦敦和苏黎世三地拥有**150名员工**，大部分资金将投入大规模算力。贝佐斯向CNBC表示，AI带来的生产力提升将创造"劳动力短缺"——需求超过供给，与主流"AI取代工作"论调相反。
  > 💡 410亿美元估值跻身AI独角兽第一梯队，物理AI（区别于纯语言模型）正在成为大额资本押注的新赛道。Prometheus两轮融资合计超180亿美元，是迄今对物理AI方向最大的单笔资本押注。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/11/jeff-bezoss-prometheus-raises-12b-to-build-an-artificial-general-engineer-for-the-physical-world/) | [IT桔子](https://www.itjuzi.com/investevent/14696103)

**Theker完成8500万美元A轮，打造通用可重构工厂机器人**
- 巴塞罗那机器人初创公司Theker完成**8500万美元**A轮融资，自称"欧洲史上最大机器人A轮"。本轮融资由美国VC **CRV**领投，**Samsung**和LVMH董事长Bernard Arnault关联的**Aglaé Ventures**等参投，Zara母公司Inditex为早期支持者。Theker与固定形态的人形机器人不同，其机器人的手、臂和整体形态可根据任务重新配置或调整尺寸，适用于分拣包裹、服装包装、仓储瓶罐处理等场景。公司直接跳过创新部门，与物流和运营部门对接以缩短销售周期。联合创始人Carla Gómez Cano表示团队计划年底前扩展至**120人**。
  > 💡 Theker的"可重构通用机器人"路线区别于人形机器人和单一任务专用机器人，瞄准的是制造业中"非标准化但可批量"的灰色地带。Samsung既可能是客户也可能是供应商，这种"投资+供应链"双重关系是工业机器人的典型策略。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/11/theker-just-raised-85m-to-build-the-factory-robot-that-doesnt-specialize-in-anything/)

**Equal AI完成3000万美元B轮，印度AI来电筛选助手突破百万月活**
- 印度AI来电筛选应用Equal AI完成**3000万美元**B轮融资，由**Prosus Ventures**和**Tomales Bay Capital**领投，累计融资超**4200万美元**。该应用自去年上线以来已达到**超过100万月活用户**和**30万日活用户**，通过AI代接听电话、识别来电原因并生成摘要，支持快捷回复（如"把快递放门口"）。应用支持**10种以上印度语言**及多语言混说（code-mixing），目前仅限Android。创始人Keshav Reddy来自印度GVK集团家族。竞争对手包括Google和Apple的来电筛选产品以及Truecaller。Prosus此前在西班牙投资了Luzia、在拉美投资了Zapia等本地化AI助手。
  > 💡 印度市场的来电骚扰问题极为严重（买车险后一周可能接到20个推销电话），Equal AI切入了一个高刚需低门槛的场景。Prosus的本地化AI投资组合策略表明，新兴市场的垂直AI助手比通用聊天机器人更容易建立用户粘性。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/11/equal-ai-raises-30m-to-screen-calls-so-indians-dont-have-to/)

**Mistral据传融资30亿欧元，估值200亿欧元**
- 据Bloomberg报道，法国AI实验室Mistral AI正在早期讨论中寻求融资约**30亿欧元**（约35亿美元），估值约**200亿欧元**（约231.5亿美元），较去年9月C轮的**117亿欧元**估值接近翻倍。Mistral目前累计融资约**40亿美元**（Pitchbook数据），远低于OpenAI（1860亿美元）和Anthropic（1612.5亿美元）。公司正在巴黎附近建设数据中心，并已与法国军方、卢森堡政府及多家欧洲大型企业建立合作，定位为"主权"欧洲AI替代方案。
  > 💡 Mistral的估值增速反映欧洲AI主权叙事正在产生资本溢价，但其融资规模和估值仍与美国头部实验室差距显著。在各国政府 distancing from American tech 的趋势下，Mistral的"主权AI"定位是差异化竞争壁垒。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/12/mistral-is-rumored-to-be-raising-e3b-at-e20-valuation/)

### 研究关注
**阿里与清华ViT³入围CVPR 2026最佳论文决选：推理时在线学习实现线性复杂度，匹配高度优化Transformer**
- ViT³（Vision Test-Time Training）将注意力操作重构为在线学习问题——在测试时从key-value对构建紧凑内部模型，实现**线性计算复杂度**和可并行计算。论文通过系统性实验提炼了**6条视觉TTT设计原则**，涵盖内部模块和内部训练的关键选择。在图像分类、图像生成、目标检测和语义分割四类任务上，ViT³**持续匹配或超越**Mamba和线性注意力等先进线性复杂度模型，并**有效缩小与高度优化的vision Transformer的差距**。论文由清华Gao Huang组和阿里（Yu Cheng、Bo Zheng）合作完成，代码已开源（github.com/LeapLabTHU/ViTTT）。
  > 💡 TTT路线在CVPR最佳论文层面获得认可，意味着将注意力重构为测试时在线学习正在成为替代标准注意力机制、实现线性复杂度的主流路线之一。
   - 来源: [arXiv](https://arxiv.org/abs/2512.01643) | [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651038804&idx=1&sn=d2bab50f9d5db279727d50646d23ff9b&chksm=855bbcc8502a410f886256fe1bf4558abb391b7384a45567516fc60036267ed0cad8cf51aebf&scene=0&xtrack=1#rd)

**清华季向阳团队MPTS：以难度预测替代全量评估，降低大模型与具身Agent训练交互成本**
- 清华大学自动化系季向阳教授团队在Nature Communications发表Model Predictive Task Sampling（MPTS）框架，这是该团队"条件交互"（conditional interaction）研究体系的最新成果。核心观点是：大模型和具身Agent训练的真正瓶颈不是算力，而是交互成本——prompt与模型、Agent与环境之间的每次交互都消耗内存、算力和时间，具身场景下还存在硬件损耗和安全风险。MPTS用轻量级生成模型（Risk Predictive Model）在线预测任务适应难度，无需执行昂贵全量评估即可排序任务优先级，采样准则可配置（鲁棒性优先或加速优先）。
- 该团队的研究体系横跨两个领域：(1) 具身Agent的鲁棒快速适配（Nature Communications + ICML）；(2) LLM高效后训练，代表算法**MoPPS**在RLVR中在线预测prompt难度以跳过低信息量rollout，已被**Meta、Apple、阿里巴巴（Qwen/Roll）、腾讯混元**的训练团队采纳为基线。
- 学术上获得**Yann LeCun和Yoshua Bengio**正面引用，完整发表记录涵盖Nature Communications、T-PAMI、ICML、KDD、ICLR、NeurIPS。理论根源可追溯至贝叶斯大脑假说——从Helmholtz的"感知即无意识推理"到Hinton/Friston的自由能原理与主动推理。
  > 💡 "交互效率"是被低估的训练瓶颈维度：当GPU堆叠不再是唯一解时，"哪些任务值得交互"这个选择问题变得关键。MoPPS被Meta/Apple/阿里/腾讯采纳，说明学术界采样算法已进入工业训练pipeline，具有直接的生产价值。
   - 来源: [Nature Communications](https://www.nature.com/articles/s41467-026-74004-0) | [@AlbertW24045555](https://x.com/AlbertW24045555/status/2064964292978569514)

**World Labs发布三篇3D/空间智能研究：覆盖像素级几何重建、4D人体动态与联合深度生成**
- World Labs发布三篇新研究，覆盖3D几何生成、4D人体重建和深度估计：
  1. **World Tracing**（Hao Zhang等）：提出生成式像素对齐几何表示，单张图像输入即可预测每像素**6层有序3D点**（可见表面+遮挡几何）。通过世界追踪扩散Transformer（WT-DiT）训练，在可见表面重建和完整几何生成上均超越深度估计器和图生3D模型。可直接接入现有网格生成器实现无需训练的纹理网格、3D场景编辑和几何引导视频合成。
  2. **Flex4DHuman**（Jen-Hao Cheng等）：通过仅依赖相对相机姿态条件的多视角视频扩散，将单目或稀疏视角视频转换为同步密集多视角视频，可直接重建**4D高斯泼溅**，无需几何先验或多相机采集系统。面向AR/VR、游戏和仿真场景。
  3. **Modality Forcing**（Bardienus Duisterhof等，CMU + World Labs）：将预训练T2I模型通过简单后训练改造为联合图像-深度生成器。每个模态独立加噪，支持图→深度、深度→图或联合生成。在NYUv2等5个基准上AbsRel达到**2.52**，较现有联合生成模型降低**57%**，与最强判别式深度估计器MoGe v2竞争。随T2I模型规模（300M→3B）和预训练数据量扩展，深度质量持续提升。
  > 💡 三篇论文从"看见世界"（World Tracing的像素对齐几何）、"重建动态人"（Flex4DHuman的4D高斯）到"理解空间"（Modality Forcing的联合深度生成）构成World Labs的3D/空间智能技术链路。Modality Forcing的关键洞察是T2I预训练本身就是可扩展的空间感知基础——图像生成能力越强，深度估计越准。
   - 来源: [@theworldlabs](https://x.com/theworldlabs/status/2065466830052098058#m) | [World Tracing](https://haoz19.github.io/world-tracing-page/) | [Flex4DHuman](https://andy-cheng.github.io/Flex4DHuman/) | [Modality Forcing](https://modality-forcing.github.io/)

**EvoArena：动态环境下LLM Agent平均准确率仅39.6%，记忆演化机制将GAIA基准提升6.1%**
- EvoArena基准套件将环境变化建模为终端、软件和社交领域的渐进更新序列，揭示当前Agent在动态环境中的平均准确率仅**39.6%**。论文同时提出EvoMem——一种基于补丁的记忆范式，将记忆演化记录为结构化更新历史。EvoMem在EvoArena上平均提升**1.5%**，在标准基准GAIA和LoCoMo上分别提升**6.1%**和**4.8%**，链式任务准确率提升**3.7%**。论文由Jundong Xu等14位作者完成（含Salesforce Caiming Xiong、MIT Hae Won Park、NUS Bryan Hooi等）。
  > 💡 Agent记忆管理是当前实用化落地的关键瓶颈，动态环境下的记忆演化机制对长流程、多步骤Agent任务的可靠性提升有直接价值。
   - 来源: [arXiv](https://arxiv.org/abs/2606.13681)

**SpatialClaw：以代码为动作接口，20个空间推理基准平均59.9%准确率超竞品11.2分**
- SpatialClaw提出以代码作为Agent空间推理的动作接口：维护一个预加载输入帧和感知/几何原语的有状态Python kernel，让VLM Agent每步根据前序输出编写可执行代码单元。该方法无需训练，在**20个**静态和动态3D/4D空间推理基准上达到**59.9%**平均准确率，超越近期空间Agent **+11.2分**，在**2个模型家族的6个VLM骨干**上保持一致增益。
  > 💡 空间推理是具身智能和机器人应用的核心能力，动作接口的重新设计可能比单纯增加模型规模更能直接提升Agent在空间任务上的表现。
   - 来源: [arXiv](https://arxiv.org/abs/2606.13673)

**BlendIn（ACL 2026）：按可靠性加权混合多模型输出，实现LLM推理时对齐，提升50%**
- BlendIn提出推理时对齐的概率模型混合框架，将传统的"是否干预"二元决策转变为创建两个模型的混合分布，根据可靠性按比例加权各模型贡献。论文揭示了一个关键问题：从对齐模型中提取的指导（guidance）在不同目标模型上有效性差异极大，无效指导反而引发更多干预和混乱。BlendIn在保留有益指导的同时降低不可靠建议的权重，在挑战性模型对上实现**最高50%的性能提升**。
  > 💡 推理时对齐的干预粒度问题是RLHF之外的另一条实用路径，50%的提升幅度和ACL 2026接收表明该方向已具备学术认可和工程实用性。
   - 来源: [arXiv](https://arxiv.org/abs/2606.11201)

### X讨论
**Chelsea Finn团队分享两项机器人研究：DIRECT测试时计算路由与多机器人VLA协同**
- Chelsea Finn（Google DeepMind及斯坦福教授）团队发布两项研究：
  1. **DIRECT**：具身规划器测试时计算路由框架，发现盲目扩展test-time compute在机器人领域浪费严重——44%的VLABench任务上非思考模型以**<2%的延迟**（1.9s vs 118s）匹配或超越Thinking模型。DIRECT通过轻量级路由器根据场景上下文动态选择最优规划器配置，将不规则的模型规模扩展曲线变为单调提升。在Franka机器人多步grocery bagging任务上达**95%成功率/6.85秒**，优于Thinking规划器的90%/**19.58秒**。在270,000+次模拟路由和245条硬件轨迹上验证。
  2. **多机器人VLA协同**：将VLA模型微调为可控制团队中任意机器人的通用控制器，在多机器人协同任务上**匹配或超越训练单独模型或单一集中式模型**的表现，且可轻松扩展到大型团队。
  > 💡 DIRECT的核心发现——test-time scaling在机器人领域并非普适有效——与LLM中"思考越久越好"的趋势形成鲜明对比。机器人任务的异质性意味着固定延迟-能力折衷不可取，按任务难度动态路由是更务实的工程路径。
   - 来源: [@chelseabfinn (DIRECT)](https://x.com/chelseabfinn/status/2065561801916571717#m) | [DIRECT项目页](https://jadee-dao.github.io/direct/) | [arXiv](https://arxiv.org/abs/2606.12402) | [@chelseabfinn (VLA)](https://x.com/chelseabfinn/status/2065559130929291630#m)

**Google DeepMind可解释性团队提出Model Diffing Agents：自动发现模型间行为差异**
- Google DeepMind语言模型可解释性团队（Bilal Chughtai、Neel Nanda等）发布Model Diffing Agents研究。核心方法：构建一个审计Agent，自主编写prompt来搜索和验证两个LLM之间的系统性行为差异。在相同模型对比中假阳性率极低（接近零），在条件系统指令注入的模型上能准确识别隐藏行为及其触发条件。相比单模型审计，双模型diffing在细微行为差异（如Python缩进风格、LaTeX使用习惯）上表现明显更优。应用于真实模型对（gemini-2.5-pro vs gemini-3-pro）时发现了如"斐波那契默认算法不同"、"创意写作中的名字坍缩（Elias Thorne）"等有趣差异。
  > 💡 "模型diff"思路借鉴了代码diff的概念——理解一个百万行程序的最佳方式之一是看增量变化，而非从头阅读。对AI安全而言，这类工具能在模型迭代中自动发现"未知的未知"行为变化，补充现有评估范式只能检测"你在找的东西"的盲区。
   - 来源: [@bilalchughtai_](https://x.com/bilalchughtai_/status/2065484515573911946) | [LessWrong](https://www.lesswrong.com/posts/qi4mNbZYAFDYwfRba/building-and-evaluating-model-diffing-agents)

---
*更新时间: 2026-06-13 06:51*
