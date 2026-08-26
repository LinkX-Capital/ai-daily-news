## 08月26日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 22 条

---

## 要点汇总

- 产业动态：Figure 发布 Index 数据集：4个月众包1600万条机器人训练视频，承诺12个月投超10亿美元; Claude 记忆打通 chat 与 Cowork：可逐条查看编辑，敏感话题默认不存; OpenAI 推出 ChatGPT Business Premium 席位：100美元面向中小企业; Perplexity 推出全本地智能体栈：Portable Computer 完整运行于 NVIDIA DGX Spark; Skild S1：单条视频演示让机器人执行10分钟未见任务，成功率较语言提示高7倍; Meta 计划数周内推出 AI Agent 平台 Hatch; Atlassian 等软件公司押注知识图谱承接 Agent 数据需求
- 算力追踪：OpenAI 自研推理芯片 Jalapeño 亮相 Hot Chips：实测单位功耗吞吐超 Vera Rubin
- 初创&融资：感知智能数据公司 Mundo AI 完成2000万美元A轮; Stable Diffusion 母公司 Stability AI 完成 7600 万美元 B 轮融资; 实时语音交互大模型公司 BreezeBlue 完成 600 万美元种子轮融资; Pacific Fusion 在新墨西哥动工商用聚变示范设施
- 研究关注：Apodex 1.1：从「环境扩展」与「代理协同」两条路径同时扩 Agent 工作能力; EchoWM：开源可进入的多模态世界模型，同步生成 720p 视频、环境音与语音; ClawGym II：黑盒RL穿透Claude Code等harness，Pass@1提升14.81点; Chain-of-Experience：测试时经验迭代让8个LLM整体提升5.6%、API成本降19%; Looped语言模型提升组合式工具调用：准确率随递归深度上升; OPD泛化的双刃剑：迁移的是推理方式而非答案，多教师混现跷跷板
- X讨论：Simile置信度模型：预测群体模拟逐次误差，AUROC从0.566提至0.736; OpenRouter称token欺诈激增：拦截支付量达一个月前10倍; Andrew Ng开源agent OpenWorker新增安全工作流：代码漏洞、供应链注入与云配置扫描; Agility Robotics：Digit 已在 9 个客户现场累计运行超 6.5 万小时

---

## 📖 详细参考

### 产业动态
**Figure 发布 Index 数据集：4个月众包1600万条机器人训练视频，承诺12个月投超10亿美元**
- Figure 将运营 4 个月的 stealth 众包数据应用正式命名为 Index 并登陆 Google Play 与 App Store：覆盖 **108** 个国家/地区的 **26.4万** 下载、**4.4万** 周活用户，Creator 网络累计上传 **1600万条视频**，平台每秒处理 **30 分钟** 视频上传，已累计向 Creator 支付 **1500万美元**；每 1000 小时数据覆盖 **373** 个任务、**1146** 个物体、**116** 个环境。数据管线包含过滤、反欺诈、去重、再平衡与标注五个阶段，用于 Helix 模型训练；公司称外部数据供应商无法达到 Helix 要求的吞吐、多样性与质量标准，因此自建管线，并承诺未来 **12** 个月在数据与算力上投入超 **10亿美元**，为「订购机器人即服务」铺路。
  > 💡 机器人公司绕开数据供应商、把数据采集做成消费级应用加现金分成的飞轮，是具身智能从遥操作采集转向互联网众包的标志性动作，Helix 的泛化上限将直接由这条管线决定。
   - 来源: [Figure](https://www.figure.ai/news/introducing-index) | [@Figure_robot](https://x.com/Figure_robot/status/2092303621392376314)

**Claude 记忆打通 chat 与 Cowork：可逐条查看编辑，敏感话题默认不存**
- Anthropic 将 Claude 的记忆扩展到 Claude Cowork：chat 与云端执行的 Cowork 任务共享同一份记忆，聊天中积累的项目背景、偏好会直接带入任务执行，Cowork 中出现的新信息也会回流到 chat。记忆改为边聊边写入，无需用户说「记住这个」；用户可在 Memory 设置的 Topics 下逐条查看、编辑或删除，修改一处后所有后续对话生效。健康、种族、信仰等敏感话题默认不入记忆，可手动开启且开启后每次保存会有提示，SSN、犯罪记录等即使开启也不会存储。该功能在 Free/Pro/Max 计划的 web、桌面与移动端默认开启，Team/Enterprise 由管理员控制且默认关闭。
  > 💡 记忆正在成为个人助手的跨产品资产——同一个 memory 层把 chat、Cowork 与后续 agent 任务缝在一起，而逐条可控与敏感话题分级是这类产品设计里真正的差异化。
   - 来源: [Claude](https://claude.com/blog/claudes-memory-works-everywhere-and-you-decide-whats-in-it) | [@claudeai](https://x.com/claudeai/status/2092299704864284888)

**OpenAI 推出 ChatGPT Business Premium 席位：100美元面向中小企业**
- OpenAI 推出 ChatGPT Business Premium 席位，定价 **100美元/席**，面向中小企业与创业团队。官方称新席位为精简团队提供更强的工具、更快的工作流，以及此前仅保留给大公司的能力，方案可随团队规模与目标灵活扩展。
  > 💡 ChatGPT 企业产品线开始分层定价，100美元档位瞄准的是把此前企业专属能力下放给预算有限的小团队，进一步摊薄企业级功能的单位定价。
   - 来源: [@OpenAI](https://x.com/OpenAI/status/2092335305366069305)

**Perplexity 推出全本地智能体栈：Portable Computer 完整运行于 NVIDIA DGX Spark**
- Perplexity 推出 Portable Computer，把 Perplexity Computer 的 agent harness、orchestrator 与后训练模型完整搬到 NVIDIA DGX Spark 本地运行，orchestrator LLM、subagent LLM 与执行沙箱均不依赖云端；本地模型可选 PPLX 27B 或 Qwen 3.8 27B（Nemotron 3.5 Lightning 即将支持），某一步需要前沿推理或联网时，orchestrator 会先征得批准再将该步路由到 **15+** 云模型并把结果带回本地任务。本地模型处理的部分不按 token 计费，使 repo 级迁移等高吞吐任务在自有硬件上变得可行；产品面向 Pro/Max 订阅用户开放，提供 apt 安装方式。
  > 💡 DGX Spark 类端侧算力加全本地 agent 栈正在成形为新产品品类：隐私只是入口卖点，真正的经济账是高吞吐任务零 token 成本、云模型只在关键步付费。
   - 来源: [Perplexity](https://www.perplexity.ai/hub/products/portable-computer) | [@perplexity_ai](https://x.com/perplexity_ai/status/2092268362386780270)

**Skild S1：单条视频演示让机器人执行10分钟未见任务，成功率较语言提示高7倍**
- Skild 发布旗舰机器人基础模型 S1，主打 in-context learning：给一条视频演示即可执行训练中从未见过的任务，最长 **10 分钟** 长程操作，无需任何微调或后训练。受控实验中，在 **10万小时** 预训练数据上，演示提示在未见任务上达到 **66%** 成功率，而语言提示仅 **9%**（约 **7 倍** 差距）；单条演示的价值约等于 **380** 条后训练样本；物体被移走、更换、光照改变等扰动下任务仍能完成，并出现常识行为——演示里用浇水壶浇花而现场只有水杯时，S1 会改用水杯。公司称 S1 已在商业合作伙伴处投入使用。
  > 💡 S1 把语言模型的 in-context learning 范式完整搬进机器人操作：若「演示即指令」的 scaling 曲线持续，机器人部署将从逐任务采集微调变成现场演示即上线，这可能是具身智能里数据效率最高的一条路线。
   - 来源: [Skild](https://www.skild.ai/blogs/s1) | [@agilityrobotics](https://x.com/agilityrobotics/status/2092337323828727890)

**Meta 计划数周内推出 AI Agent 平台 Hatch**
- 据报道，Meta 内部文件显示，Meta Platforms 计划在未来数周内推出消费版 OpenClaw AI Agent，内部代号为 Hatch，并目标在 10 月发布最新 AI 模型 Watermelon。Hatch 是 Meta 首席执行官 Mark Zuckerberg 将 AI 投入变现、分散广告收入依赖的重要一环，公司曾考虑采用分层定价，其中高级订阅月费最高可能达到 199.99 美元，包含更高的使用额度。
  > 💡 199.99 美元的订阅定价直接对标 OpenAI 与 Anthropic 的高端档位，叠加独立 Agent 产品线，说明 Meta 正尝试以独立品牌和高 ARPU 把 AI 投入转化为第二增长曲线，而非仅作为广告业务的辅助。
   - 来源: [The Information](https://www.theinformation.com/articles/meta-plans-launch-hatch-ai-agent-platform-coming-weeks)

**Atlassian 等软件公司押注知识图谱承接 Agent 数据需求**
- 随着能自动执行编程等白领任务的 AI Agent 兴起，Atlassian 等软件公司开始提供知识图谱（graph database）类产品，以帮助 AI 分析组织内部不同类型数据之间的关系。Microsoft 等公司甚至对其客户的数据设置了壁垒，限制其他软件商访问。知识图谱与 Databricks、Snowflake 等以行列方式组织海量数据的管理平台不同，支持者认为其能让 AI 做更少的处理运算，从而节省成本。
  > 💡 知识图谱的卖点是“减少 AI 处理量、降低成本”，这实际上是在抢占 Agent 工作流中数据预处理与上下文装配的中间层，谁能掌控这一层，谁就能在 Agent 时代分走推理算力之外的预算。
   - 来源: [The Information](https://www.theinformation.com/articles/atlassian-rides-knowledge-graph-boom)

### 算力追踪
**OpenAI 自研推理芯片 Jalapeño 亮相 Hot Chips：实测单位功耗吞吐超 Vera Rubin**
- OpenAI 在 Hot Chips 公开自研推理 ASIC Jalapeño 的首批结果。SemiAnalysis 受邀进入 OpenAI 实验室核验 InferenceX 实测——在未启用投机解码与多 token 预测的前提下，Jalapeño 的单位功耗输出吞吐超过 NVIDIA 与 CoreWeave 7 月公布的 Vera Rubin 结果，DeepSeek R1 并发 1 下超 **700 tok/s/user**，Kimi K2.5 场景约为次优芯片的 **9 倍**，TCO 与 Rubin 基本持平；SemiAnalysis 注明所有性能数字由 OpenAI 提供，且尚无长上下文多轮的 AgentX 结果。官方口径：芯片 TDP **700W**、搭载 **HBM4**（带宽 15.4TB/s，引脚速率略高于 Rubin），预计 **2026 年底**小规模部署、**2027 年**上量。
  > 💡 首代自研芯片即在对标 Rubin 的单位功耗吞吐上占先，配合 Codex 写 kernel 的极速软件 bring-up，OpenAI 正把「数据中心受电力限制」变成自己的主场优势；对 NVIDIA 而言，CUDA 护城河第一次被前沿实验室的软硬件协同真实撕开口子，但 2026 年底才开始小规模部署，短期产能层面仍不构成实质替代。
   - 来源: [SemiAnalysis](https://newsletter.semianalysis.com/p/openai-jalapeno-better-than-nvidia) | [@SemiAnalysis_](https://x.com/SemiAnalysis_/status/2092314842396828077) | [TechCrunch](https://techcrunch.com/2026/08/25/openais-jalapeno-chip-is-built-for-fast-inference-at-scale-benchmarks-show) | [OpenAI](https://openai.com/index/jalapeno-first-results) | [@OpenAI](https://x.com/OpenAI/status/2092300846675505602)

### 初创&融资
**感知智能数据公司 Mundo AI 完成2000万美元A轮**
- 为前沿 AI 实验室构建数据的 Mundo AI 宣布完成 **2000万美元** A 轮融资（公司官网公告横幅口径为融资 **2400万美元**）。Mundo 定位「感知智能的数据层」，与前沿实验室和 AI 公司合作，围绕音频、视频与新兴模态构建数据集、评测与应用研究，聚焦语音识别与真实对话理解之间的鸿沟、视觉模型在上下文与时序物理意图上的缺口，以及「所需数据尚不存在」的前沿问题。
  > 💡 当前沿实验室的瓶颈从模型架构转向感知数据，「为实验室造数据」正在形成 perceptual data 层的新赛道，音频/视频的长尾交互场景是最主要的供给缺口。
   - 来源: [@Pluggedcircle](https://x.com/Pluggedcircle/status/2092233438908584042) | [Mundo](https://mundoai.world/research/perce)

**Stable Diffusion 母公司 Stability AI 完成 7600 万美元 B 轮融资**
- Stability AI 于周二宣布完成 7600 万美元 B 轮融资，公司累计融资总额升至 2.32 亿美元。本轮投资方包括环球音乐集团、索尼音乐集团、华纳音乐集团及游戏公司 Electronic Arts，AMD Ventures 与 Pacific Alliance Ventures 也参与了本轮融资。Stability AI 表示，新资金将用于扩展其“创意制作”产品套件及专业服务业务，公司目前提供面向音乐、视频与图像生成的 AI 模型。
  > 💡 三大唱片公司与 EA 同时入场，说明 Stability AI 已不再只是模型供应商，而是以版权与内容分发绑定的方式嵌入娱乐工业工作流；这对其未来在生成式版权诉讼中的处境是双向变量。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/25/stability-ai-maker-of-image-generator-stable-diffusion-raises-76-million-in-fresh-funding)

**实时语音交互大模型公司 BreezeBlue 完成 600 万美元种子轮融资**
- 据报道，实时语音交互公司 BreezeBlue 完成 **600万美元** 种子轮，由元璟资本与红点中国联合领投。公司由前 MiniMax 技术合伙人、视觉生成模型团队负责人杨斌于 2025 年底创立，团队 15 人，成员来自 Google、字节、阿里、阶跃、华为等公司。其自研 Breeze TTS 2 在 Artificial Analysis 的 Text-to-Speech 榜单排名全球并列第四，超过 ElevenLabs v3 与 Gemini 3.1 Flash TTS（参评音色全部为零样本音色设计生成，未用评测场景定制微调），模型侧首字延迟低至 **40ms**（低于 ElevenLabs Flash v2.5 官方披露的 50ms），支持 **50多种** 语言；已通过 API 落地虚拟主播、互动漫剧、角色扮演与 AI 游戏等场景，C 端创作平台 BreezeCreator 已服务全球数万名创作者。
  > 💡 语音公司的下一个战场不是「更像人声」，而是把声音变成可设计、可导演、可长期复用的角色资产，再往实时人机交互层延伸——这恰是大语言模型不容易顺手吞掉的方向。
   - 来源: [智能涌现](https://mp.weixin.qq.com/s?__biz=MzkwMDQ2NDU2Nw==&mid=2247518090&idx=1&sn=50bb3957be1971079bf6ea6820b17f71&chksm=c19da59ca87bfa744d6f24c0c8d7e4309a9035d25520d10e58e8e3233cee210c52d3b5f1c7a0&scene=126&sessionid=1787632423#rd) | [IT桔子](https://www.itjuzi.com/investevent/14703387)

**Pacific Fusion 在新墨西哥动工商用聚变示范设施**
- 聚变初创公司 Pacific Fusion 在新墨西哥州破土动工一座示范设施,目标是在该设施上实现能源产出与设施自用能耗持平,即业内所称的 net facility gain。联合创始人兼首席运营官 Carrie von Muench 表示,据其所知全美目前没有在建的同类设施。该设施位于阿尔伯克基,会测试 Pacific Fusion 的聚变技术路线,即利用强度高且精确协同的电脉冲在铅笔擦大小的燃料靶周围建立磁场并将其压缩,使燃料原子发生聚变反应。首席技术官 Keith LeChien 称该示范设施每天可发射数次「炮」级别的脉冲。公司目标在 2030 年前实现 net facility gain,并争取在 2030 年代中期投运商用聚变电厂,商用堆的发电量需要是示范系统的约 5 倍,以支撑电厂级辅助设备的能耗。
  > 💡 Pacific Fusion 把「设施级净能量增益」与「商用堆 5 倍能量产出」分成两个独立里程碑来推进,先在示范设施验证脉冲式磁惯性约束路径,再考虑电厂化,显示出对成本曲线的保守态度。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/25/pacific-fusion-next-fusion-machine-could-clear-key-hurdle-to-commercial-power)

### 研究关注
**Apodex 1.1：从「环境扩展」与「代理协同」两条路径同时扩 Agent 工作能力**
- Apodex 1.1 把复杂任务所需的「工作能力」拆为两条互补的扩展轴：Environment Scaling 用于扩展可执行文件、检索与代码环境的多样性与可验证性，Agentic Coordination Scaling 用于训练代理分解长时程任务、并行委派工作、整合异步结果并重新规划。论文还设计了一个共享执行层与 AgentOS 来维护跨工具和代理的任务状态与来源，并将环境轨迹与协同轨迹转化为稳定行为。论文报告：在金融、科研、数学、编程与检索等多类复杂专业任务上，Apodex 1.1 进入领先性能区间，且其 35B 参数的 Apodex 1.1 Mini 仍保留较强的本地可部署工作能力。
  > 💡 Apodex 1.1 的关键贡献不在模型规模，而在把 agentic 工作能力拆成「环境可验证性」和「协同规划」两条独立 scaling 轴，意味着 agentic 训练正在向系统级工程而非单纯模型堆参数演化。
   - 来源: [arXiv](https://arxiv.org/abs/2608.23283) | [HuggingFace Daily Papers](https://huggingface.co/papers/2608.23283)

**EchoWM：开源可进入的多模态世界模型，同步生成 720p 视频、环境音与语音**
- EchoWM 是一个面向「可进入式生成媒体」的多模态世界模型，在用户连续导航的同时联合生成 720p 视频、环境音、音乐与语音。模型以相机意图为交互核心：第一人称场景由相机运动直接定义，第三人称场景则从数据中学习相机与角色的耦合动力学，离散命令与连续位姿被映射到共享的度量尺度相对 6-DoF 轨迹。训练侧，论文构建了一个互补的数据引擎并采用「渐进训练 + 自回归后训练」的两阶段方案以支持长时程生成。评测显示，EchoWM 在公开世界模型基准上具备较强的轨迹跟随与视觉质量，并能在长时程生成中维持环境音与语音的同步。
  > 💡 EchoWM 将世界模型从「单模态视频预测」推向「音视频联合 + 6-DoF 交互」，是 Open World Model 路线的重要补位；同步生成环境音与语音是相对 Video-only 方案更高的工程门槛，也是可进入式生成媒体的实际分水岭。
   - 来源: [arXiv](https://arxiv.org/abs/2608.23189) | [HuggingFace Daily Papers](https://huggingface.co/papers/2608.23189)

**ClawGym II：黑盒RL穿透Claude Code等harness，Pass@1提升14.81点**
- 论文提出面向复杂 agent harness 的黑盒强化学习框架：用沙箱基础设施隔离任务环境与 harness 做大规模并发 rollout，在模型边界放置 serving proxy 捕获模型调用并重组为 prefix tree，再将 critic-based PPO 与 critic-free GRPO 适配到树上优化，全程把 harness 当黑盒，并支持单个模型被多个异构 harness 联合训练（mix-harness）。在 Qwen3-30A3B 上，黑盒 RL 经 OpenClaw 与 Claude Code 分别将 ClawGym-Bench 的 Pass@1 提升 **9.98** 与 **14.81** 点，且在 200-400 个优化步内保持稳定，在 JobBench、OfficeQA 等更难任务上也取得一致收益。
  > 💡 harness 生态已是事实上的生产环境，却长期游离于 RL 训练之外；把 harness 当黑盒纳入训练回路，等于让模型在真实工作环境里学强化学习，而不是在干净沙箱里学。
   - 来源: [arXiv](https://arxiv.org/abs/2608.16798)

**Chain-of-Experience：测试时经验迭代让8个LLM整体提升5.6%、API成本降19%**
- 论文提出 Chain-of-Experience（CoE）设定，系统研究 LLM 在测试时通过迭代交互持续变强的能力：模型借助自身反馈或环境信号（如答案正确性、公开编程测试通过率）多轮积累经验轨迹，形成超越零样本推理的持续改进回路。在数学、编程与知识任务上对 **8** 个 LLM（含 GPT-5、Gemini-2.5 Pro、Claude-4.5 Sonnet）的评测显示，利用迭代经验稳定优于无反馈基线，仅靠自我反馈即有明显收益，整体提升 **5.6%** 且 API 成本降低 **19%**；组合互补反馈通道有额外增益，模型基础能力越强改进幅度越大，且在弱反馈或伪反馈下保持稳健，收益多出现在迭代早期。
  > 💡 传统 benchmark 把模型当静态对象测，CoE 把「从经验中变强」本身作为被测能力——在 agent 时代，学习速度可能比单次准确率更能区分模型。
   - 来源: [arXiv](https://arxiv.org/abs/2608.18027)

**Looped语言模型提升组合式工具调用：准确率随递归深度上升**
- 论文在组合式工具调用场景下研究循环（looped）语言模型：模型需要协调多次 API 调用、维护中间状态并保持跨工具依赖。在与非循环模型相同 SFT 配方的对照实验中，循环结构在需要依赖追踪的组合式调用上普遍获益，而对孤立的单词 API 调用提升有限且更依赖具体模型；在 API-Bank、BFCL、NESTful 上，多步工具调用准确率总体随推理时递归深度增加而上升，而按需分配算力的自适应推理取得更优的算力-性能权衡。
  > 💡 循环结构此前主要在推理基准上被验证，这项工作把它与 agent 工作负载连了起来——「对难题多想几轮」对「把多步工具用对」同样成立。
   - 来源: [arXiv](https://arxiv.org/abs/2608.18171)

**OPD泛化的双刃剑：迁移的是推理方式而非答案，多教师混现跷跷板**
- 论文对 on-policy 蒸馏（OPD）的泛化行为做控制变量研究，让泛化因素从域内分布偏移、跨域迁移到多教师设定逐一变化。核心发现是 OPD 迁移的是教师的推理方式而非具体答案：训练难度几乎不影响效果，教师从未解出的题也有用；师生同源时，学生跨语言、推理长度乃至其他领域都接近教师，而跨源配对基本只拟合训练分布。这种广迁移是双刃剑：把提示路由给领域专家教师并不能限定各教师的影响范围，多教师组合会形成跷跷板效应——一个教师能力的增强会压低另一个。
  > 💡 多教师蒸馏常被当成「能力拼装」，这项工作说明教师影响会越界扩散——选教师先看出身，路由解决不了混训的相互干扰。
   - 来源: [arXiv](https://arxiv.org/abs/2608.16647)

### X讨论
**Simile置信度模型：预测群体模拟逐次误差，AUROC从0.566提至0.736**
- 人类行为模拟公司 Simile 发布首篇技术博客，介绍其预测模拟误差的 confidence model：模拟模型输出人群行为的动作分布，confidence model 负责预测每次模拟与真实结果的 TVD 误差。在约 **8600** 个留出问题上，基于问题基础特征的回归 AUROC 仅 **0.566**，语义 embedding 提升至 **0.686**，读取仿真模型内部激活的 probing 达 **0.730**，直接微调仿真模型本身（CFT）达到 **0.736**（RMSE 0.0776、Pearson r=0.565），而从通用模型 Qwen3.5-27B 直接微调仅 0.720，说明训练仿真模型的过程本身形成了关于不确定性的表征。产品侧将置信度分为四档：「High」档预测有 **95%** 概率达到决策级质量（TVD<0.16），「Low」档仅 **38%**。Percy Liang 转发称，平均意义上的评测无法覆盖单次查询，置信度模型让「这一次模拟是否可信」变得实时可判。
  > 💡 群体仿真的商业化瓶颈不是能不能模拟，而是敢不敢据此决策——把逐查询置信度做成产品级能力，是 simulation 从演示走向决策依据的关键一步。
   - 来源: [Simile](https://www.simile.com/blog/confidence?v=2) | [@simile_ai](https://x.com/simile_ai/status/2092299277154291843) | [@percyliang](https://x.com/percyliang/status/2092302845987225809)

**OpenRouter称token欺诈激增：拦截支付量达一个月前10倍**
- OpenRouter 联合创始人 Alex Atallah 表示，生态范围内的 token 欺诈正在激增，OpenRouter 当前拦截的支付量已达 **一个月前的10倍**。OpenRouter 与 Stripe 会替开发者处理这类欺诈风险，并放出了相应的接入指引。
  > 💡 免费/低价 token 供给在放大流量的同时也在放大欺诈面，支付与风控正在从后台职能变成 inference 聚合平台的核心基础设施。
   - 来源: [@alexatallah](https://x.com/alexatallah/status/2092253354420326443) | [@OpenRouter](https://x.com/OpenRouter/status/2092260618577305620)

**Andrew Ng开源agent OpenWorker新增安全工作流：代码漏洞、供应链注入与云配置扫描**
- Andrew Ng 的开源桌面 agent OpenWorker 发布新版本，内置三个网络安全 agent：扫描代码漏洞、检测依赖中的供应链注入、检查云安全配置的攻击面，帮助开发者在部署前完成更多安全工作。OpenWorker 定位「交付成品而非聊天」的开源 AI 同事，本地优先运行，支持 **25+** 连接器（GitHub、Slack、Jira、Notion 等）与 Slack 内 @OpenWorker 触发，写操作与 shell 命令均需人工批准，引擎基于 aisuite 构建；harness 完全开源可审计，模型可自选，包括经 Ollama 全本地运行开源权重模型，敏感代码不出本机。
  > 💡 开源 harness 加自选模型的组合拳瞄准的是安全团队——「攻击者已经在用 AI，防御者需要同样的杠杆」，而可审计性正是闭源 harness 给不了的卖点。
   - 来源: [@AndrewYNg](https://x.com/AndrewYNg/status/2092315079576555806) | [GitHub](https://github.com/andrewyng/openworker)

**Agility Robotics：Digit 已在 9 个客户现场累计运行超 6.5 万小时**
- Agility Robotics 首席执行官 Peggy Johnson 在 Bloomberg 节目中讨论了物理 AI 需求的增长以及 Digit 在真实设施环境中的落地情况。她透露 Digit 已被部署到 9 个客户现场，累计实际运行时间超过 6.5 万小时。Agility 将人形机器人定位为正在与行业标准同步走向实际应用的阶段。
  > 💡 9 个现场与 6.5 万小时仍是行业头部公司才拿得出手的运行数据，说明人形机器人在真实设施中的可用性仍高度集中于少数先发玩家，距离通用部署仍有一段距离。
   - 来源: [@agilityrobotics](https://x.com/agilityrobotics/status/2092337323828727890)

---
*更新时间: 2026-08-26 06:45*