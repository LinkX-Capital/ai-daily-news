## 07月31日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 19 条

---

## 要点汇总

- 模型前沿：OpenAI下调GPT-5.6 Luna(80%)与Terra(20%) API价格并推出Fast mode; Google DeepMind发布Gemini Robotics 2三模型，主打全身智能与几小时跨形态适配; Thinking Machines发布Inkling-Small，276B MoE/12B激活追平甚至反超Inkling
- 产业动态：AWS任命前苹果与谷歌工程老兵Herrnstadt负责核心AI产品; Microsoft 365 Copilot付费席位破3000万，推出Cowork与autopilot agent Scout
- 算力追踪：台积电开发类似Intel的先进封装技术，以应对AI芯片封装瓶颈; 美国参议员施压苹果放弃采购中国存储芯片
- 初创&融资：Simile五个月内再融2亿美元估值20亿，Stanford三教授联创、NYT称其模拟准确率85%-99%; Okta约2亿美元收购AI身份安全初创Permiso; 以色列服务器网络芯片公司Xsight融资3亿美元，估值达28亿; Dili融2170万美元，用AI做美国基建项目合规
- 研究关注：TurboVLA提出V+L直连A新范式，消费级RTX 4090上跑出32 Hz; HumanCLAW框架将VLM决策与执行解耦，9款测试模型全部落败; Echoverse用12个深度演化世界训练computer-use agent，9B模型分数近翻倍; EvoLib让黑盒LLM推理时自学习无需模型更新; Evolvent开源RSIBench-Data评估agent递归自我改进; CoRT用反事实重放做token级信用分配给GRPO带来4.4个百分点平均增益; 论文首次系统评估LLM agent文件系统记忆：组织减半检索成本却换不来更好答案
- X讨论：Cline用递归自我改进把Kimi K3推到Terminal-Bench 2.1的88.8%，成本不到Fable 5十分之一

---

## 📖 详细参考

### 模型前沿
**OpenAI下调GPT-5.6 Luna与Terra API价格，引入Fast mode**
- OpenAI自7月30日下调GPT-5.6两款API价格：**Luna降80%**、**Terra降20%**，Sol不变。新定价Terra **每百万输入2美元/输出12美元**，Luna **每百万输入0.20美元/输出1.20美元**。OpenAI称Luna性能对标约一年前frontier级模型，单任务成本仅约其6美分、速度快近9倍，在Agents' Last Exam上以低近99%的单任务成本超过Fable 5。同步推出**Fast mode**取代Priority Processing，Sol的Fast模式较标准快**2.5倍**、价格2倍且智能不变。OpenAI另披露，GPT-5.6 Sol在人工主导流程中自主重写优化production kernel，使端到端服务成本降**20%**、token生成效率提**15%以上**。
  > 💡 Luna 80%降幅把对标一年前frontier级能力的门槛压到0.20美元/百万输入token，配合Sol自主优化kernel反哺服务成本，说明头部厂商用效率闭环而非单纯补贴支撑价格战，企业侧"按任务结果选模型"的混合编排会压缩中游模型生存空间。
   - 来源: [OpenAI](https://openai.com/index/advancing-the-price-performance-frontier-with-gpt-5-6/) | [@OpenAI](https://x.com/OpenAI/status/2082878156483219672)

**Google DeepMind发布Gemini Robotics 2，三大模型主打全身智能与跨形态适配**
- Google DeepMind发布Gemini Robotics 2，含三个模型：**Gemini Robotics 2**（VLA）、**Gemini Robotics ER 2**（embodied reasoning VLM，做高层规划）、**Gemini Robotics On-Device 2**（端侧高效VLA）。首次实现**全身控制**：驱动Apptronik Apollo 2人形机器人完成走路、蹲下、清理房间，覆盖"from feet to fingertips"，可控制**22自由度SharpaWave五指手**打结、密封ziplock袋。**同一checkpoint**跨三种embodiment（Apollo 2+SharpaWave、Apollo 2+Inspire hands、Franka Duo+Robotiq gripper）。ER 2可执行**数分钟、数百步**长任务并新增**多机器人协作**；On-Device 2**不到200条示例、几小时**即可适配形态差异大的新双臂平台（Dexmate、SO101、Trossen）。安全方面引入**ASIMOV-Agentic**基准，ER 2为目前最安全型号，已在Google AI Studio与Gemini Enterprise Agent Platform私密预览。
  > 💡 VLA从"桌面作业"推进到"全身+多机器人协作+几小时跨形态适配"，三模型分层对标星连框架"推理经济"向"具身"层下探；同checkpoint跨三种手部硬件，意味通用机器人正从单平台demo收敛为模型-硬件解耦栈。
   - 来源: [Google DeepMind](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/) | [@GoogleDeepMind](https://x.com/GoogleDeepMind/status/2082844162928381956)

**Thinking Machines发布Inkling-Small，276B MoE以1/4参数追平甚至反超Inkling**
- Thinking Machines Lab于7月30日发布并开源全权重模型Inkling-Small，为**276B总参数、12B激活**的Mixture-of-Experts transformer，在NVIDIA GB300 NVL72系统上训练。Inkling-Small晚于Inkling开始训练，受益于改进的预训练数据配比、refined ML recipe、以Inkling为老师的on-policy distillation，以及额外两周的agentic coding RL。官方称其以约Inkling四分之一的大小达到相当性能，在推理与agentic任务上甚至反超：HLE达**31.6%**（高于Inkling的29.7%，且在每个思考预算上优势保持），SWEBench-Verified超过**80%**。模型为encoder-free原生多模态（音频与图像与文本联合处理），可变思考强度（minimal→xhigh）、最高**1M token上下文**，可用Python裁剪/缩放/检视图像。已可在Tinker平台（限时折扣）与Tinker Playground试用并放出HuggingFace model card。
  > 💡 MoE+on-policy distillation+agentic coding RL的组合，让"小模型"在推理与编程两项硬基准上反超老师模型，说明知识蒸馏正从被动模仿转向"老师定义能力边界、学生用RL补强agentic短板"的主动路线；12B激活、1M上下文叠加可变思考强度，把开源权重单任务算力压到极低区间，对中小企业按TFLOPs/成本比较的推理选型形成直接冲击。
   - 来源: [Thinking Machines Lab](https://thinkingmachines.ai/news/inkling-small/) | [@thinkymachines](https://x.com/thinkymachines/status/2082885869426631032)

### 产业动态
**AWS任命前苹果与谷歌工程老兵Herrnstadt负责核心AI产品**
- AWS发言人证实，曾任职于苹果和Google的工程资深人士Ori Herrnstadt于5月加入AWS，担任compute AI服务副总裁。其职责范围涵盖去年10月发布的AgentCore（用于构建、运行和管理AI Agent的服务）以及用于训练和运行AI模型的SageMaker。
  > 💡 AWS把AgentCore和SageMaker统一交给一位空降VP，显示出云厂商正把Agent平台与模型训练/推理平台整合为同一产品线，以应对Anthropic、OpenAI等模型公司向上游渗透的压力。
   - 来源: [The Information](https://www.theinformation.com/briefings/exclusive-aws-taps-apple-executive-lead-key-ai-products)

**Microsoft 365 Copilot付费席位破3000万，推出Cowork与autopilot agent Scout**
- Microsoft在财报电话中披露，Microsoft 365 Copilot付费席位已超过**3000万**，净增席位环比翻倍。Microsoft AI at Work首席营销官Jared Spataro撰文称，企业AI正从"采纳"阶段（部署、license、节省工时）进入"转型"阶段，即围绕agent重新设计工作流。6月正式发布的**Copilot Cowork**采用多模型设计，由用户定义任务后端到端运行并返回完成结果，测试显示其成本比单模型方案低**30%-40%**。Microsoft同时推出首个自动驾驶agent **Microsoft Scout**，具备独立身份与权限、在后台保持活跃以推动工作流转。Microsoft将这一波产品定义为"模型+agentic harness、能闭合自身反馈回路（规划-执行-测试-修正）"的新形态。
  > 💡 付费席位破3000万且净增环比翻倍，是Copilot从license订阅转向按工作成果计费的拐点信号；Cowork的多模型比单模型便宜30%-40%直接说明"单大模型包打天下"在企业侧已不经济，混合编排+autopilot将成为办公Agent的默认形态。
   - 来源: [Microsoft 365 Blog](https://www.microsoft.com/en-us/microsoft-365/blog/2026/07/30/the-next-measure-of-ai-momentum-is-work-transformed/)

### 算力追踪
**台积电开发类似Intel的先进封装技术，以应对AI芯片封装瓶颈**
- 据知情人士透露，台积电正在开发一种与Intel已提供的先进芯片封装技术类似的新方案，旨在把多块硅片集成在同一封装内并实现互连。随着AI需求推动芯片设计者把更多处理器和高带宽内存整合进更复杂的封装，封装环节已成为半导体制造中的关键瓶颈。
  > 💡 先进封装已从过去的低价值后段工序升级为AI算力供给的决定性环节，台积电自研对应方案意在收回被Intel占据的封装方案主导权。
   - 来源: [The Information](https://www.theinformation.com/articles/tsmc-develops-ai-chip-packaging-tech-counter-intel)

**美国参议员施压苹果放弃采购中国存储芯片**
- 据Bloomberg报道，一群美国参议员以国家安全为由，敦促Apple放弃任何从长鑫存储和长江存储采购存储芯片的计划。由印第安纳州共和党议员Jim Banks与纽约州民主党议员Chuck Schumer牵头的议员团在致苹果CEO Tim Cook的信中警告，使用上述中国厂商的芯片可能带来风险。
  > 💡 此举意味着美国对华存储芯片的限制从出口端延伸到了美国本土品牌的采购端，长鑫、长江存储在打入苹果供应链方面将面临更明确的政治阻力。
   - 来源: [The Information](https://www.theinformation.com/briefings/u-s-senators-press-apple-buy-chinese-memory-chips)

### 初创&融资
**Simile五个月内再融2亿美元，估值冲至20亿**
- Simile于7月30日完成Greenoaks领投的2亿美元B轮，估值20亿美元，距1亿美元A轮走出隐身仅约五个月，参投方含Index Ventures、Hanabi、Bain Capital Ventures、A*、Definition及CVS Health Ventures。公司由32岁Stanford博士Joon Sung Park基于2023年论文（AI agents模仿Sims式环境中的人类行为）创办，联创包括Stanford教授Michael Bernstein（ImageNet论文作者之一）、Percy Liang（2021年"foundation model"概念论文首席研究员、Together AI联创）及前Hebbia/Valence GTM负责人Lainie Yallen。初始模型基于对1000名代表性参与者的两小时访谈，再与Gallup等补充全球数百万人数据，产品负责人Mihika Kapoor称响应准确率**85%-99%**；正构建人类行为基础模型并配套预测模拟准确率的confidence model。商业模式为按agent数量计费，单客户从数十万到数百万agent。客户含CVS Health（40万"agentic twins"研究药物依从性）、Deloitte、Wealthfront、Gallup；竞品有Helm、Artificial Societies、Rehearsals、Aaru。Percy Liang称"Simile 2026 之于 simulation = OpenAI 2019 之于 AI assistant"。
  > 💡 "ImageNet论文作者+foundation model概念论文首席+AI agents行为模拟论文作者"的联创阵容，把Simile从"合成用户"抬到"人类行为基础模型"叙事；confidence model回应模拟可信度质疑，按agent计费把"模拟全人类"锚定到可计价单元——但五个月连续两轮十亿美元级估值，研究方法学成熟度与资本估值差距仍大。
   - 来源: [The New York Times](https://www.nytimes.com/2026/07/30/business/dealbook/simile-ai-agents-funding.html) | [TechCrunch](https://techcrunch.com/2026/07/30/synthetic-user-startup-simile-raises-200m-at-2b-valuation-5-months-after-100m-series-a) | [Simile (@simile_ai)](https://x.com/simile_ai/status/2082873889407827980) | [Percy Liang (@percyliang)](https://x.com/percyliang/status/2082874025999745209)

**Okta约2亿美元收购AI身份安全初创Permiso，押注机器身份与AI agent安全**
- 身份管理公司Okta于7月30日宣布收购AI身份安全初创Permiso Security，交易预计在其2027财年第三季度完成。TechCrunch获悉该交易估值略低于**2亿美元**、几乎为全现金，Okta CEO Todd McKinnon未否认该数字。Permiso于2022年走出隐身，由前FireEye高管Paul Nguyen与Jason Martin联合创办，专注检测云环境中使用被盗身份横向移动的攻击，近期扩展到监测AI agent等机器身份，并于4月推出**SandyClaw**平台在沙箱中分析AI agent技能以识别恶意行为。Permiso累计融资约2900万美元，2024年4月Altimeter Capital领投的1850万美元A轮估值的投后约8000万美元。Okta首席产品官Ely Kahn称此举将把身份威胁检测与响应能力接入Okta的身份安全架构。
  > 💡 以约2亿美元吞下累计融资仅2900万的Permiso，是身份厂商从"登录验证"转向"授权后持续监测"的关键并购；AI agent作为新型机器身份涌入企业后，身份安全的需求重心正从人迁移到非人类实体，Permiso的SandyClaw沙箱式agent技能审计成为标的的核心溢价点。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/30/okta-buys-ai-security-startup-permiso-source-says-for-about-200m/)

**以色列服务器网络芯片公司Xsight融资3亿美元，估值达28亿**
- Xsight是一家成立九年的以色列初创公司，专注于服务器网络与存储芯片，本次以28亿美元估值完成3亿美元融资。领投方为富达投资，参与方包括Atreides Management、Valor Equity Partners、Battery Ventures和Intel Capital，距离上一轮主要融资已过去约五年。过去一个月内，同类网络芯片初创Eliyan和Upscale AI分别以10亿美元和20亿美元估值完成融资。
  > 💡 GPU热潮正向配套的服务器网络与存储环节外溢，多家网络芯片公司在一个月内集中完成大额融资，提示算力扩张的瓶颈正从单卡算力迁移到集群互连与数据吞吐。
   - 来源: [The Information](https://www.theinformation.com/articles/server-networking-boom-drives-300-million-funding-xsight)

**Dili融2170万美元，用AI做美国基建项目合规**
- AI合规初创Dili于7月30日宣布完成1500万美元A轮融资，加上此前670万美元种子轮，累计融资达**2170万美元**。A轮由Khosla Ventures领投，Allianz、Rebel Fund、Brick and Mortar Ventures的Darren Bechtel及Y Combinator的Garry Tan参投，Dili曾入选YC 2023年夏季批次。Dili专注美国基建项目的合规，覆盖Davis-Bacon prevailing wage、IRA清洁能源项目的PWA规则以及OSHA/EPA等重叠要求，CEO Anand Chaturvedi称不合规可导致数百万美元罚款。架构上当代AI模型仅在数据层用于把非结构化文档转为结构化数据，再由确定性系统按静态合规规则排序，以避免LLM的不确定性渗入最终判定，原本需一整天的工作可压缩至数分钟。
  > 💡 Dili的"LLM只做数据抽取、合规判定交给确定性系统"是对AI合规可信赖性焦虑的务实回答，也是AI落地"高 stakes 但规则静态"场景的范式模板；叠加美国基建潮与IRA政策窗口，合规自动化正成为基础设施投资的外溢赛道。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/30/dili-raises-15-million-to-bring-ai-compliance-to-the-infrastructure-boom/)

### 研究关注
**TurboVLA提出V+L直连A新范式，消费级RTX 4090上跑出32 Hz**
- TurboVLA把视觉-语言-动作模型的传统V→L→A路径改为V+L→A，独立编码视觉与语言特征，通过轻量双向交互直接交换信息，再由紧凑解码器预测连续动作块。在LIBERO基准上，TurboVLA以仅2亿参数实现97.7%平均成功率，单次推理延迟31.2毫秒、显存占用0.9 GB，在消费级RTX 4090上跑出32 Hz控制频率。论文由华中科技大学Xiang Bai、Han Ding团队（Hengyi Xie等）提交，代码已在Hugging Face与GitHub公开。
  > 💡 去掉LLM作为中央接口、让V与L在动作端汇合，可显著降低VLA推理开销，这一路线为低成本实时机器人策略部署提供了替代LLM中心范式的选项。
   - 来源: [arXiv](https://arxiv.org/abs/2607.27205) | [HuggingFace Daily Papers](https://huggingface.co/papers/2607.27205)

**HumanCLAW框架将VLM决策与执行解耦，9款测试模型全部落败**
- 论文提出HumanCLAW评估框架，在每一步让现成VLM发出原子技能指令，再翻译为亚秒级、连续且具物理后果（重力、碰撞）的全身动作，由此把动作决策与底层执行解耦开。基于该框架构建的HumanCLAW-Bench包含1218条跨41个室内场景的egocentric长程找物-导航-交互任务。研究者在9款主流VLM上进行测试，发现没有任何一款模型能解决该基准，最好成绩仅16.8%成功率。论文进一步指出，瓶颈并不在于目标识别，而在于缺乏embodied self-awareness：VLM无法持续跟踪自身位置、是否到达目标或是否撞上障碍物。论文作者包括Siyao Li、Lingni Ma、Michael Zollhoefer以及CMU/NUS的Manling Li、Ziwei Liu、Ranjay Krishna等。
  > 💡 把决策与执行剥离后，VLM的具身短板从'会不会做动作'前移到'知不知道自己在哪'，提示下一阶段VLM评估需要把自我状态感知作为独立维度。
   - 来源: [arXiv](https://arxiv.org/abs/2607.27180) | [HuggingFace Daily Papers](https://huggingface.co/papers/2607.27180)

**Echoverse：12个深度演化世界训练computer-use agent，9B模型分数近翻倍**
- Microsoft Research发布Echoverse，为computer-use agent构建12个训练世界：10个深度领域世界+2个能力世界（后者把日期选择器、嵌套过滤器等单控件以多种形态反复训练）。深度体现在复现应用真实行为、预填真实数据、跨屏幕与用户保持状态一致。在12个世界上训练后，9B模型基础分从**36.5%提至67.1%**（近翻倍），距GPT-5.4约14个百分点。经验：高仿真保真度是必需——浅层版同站训练会让模型回退、深层版才改进；针对agent常失败的UI控件做多形态训练，能让模型在未见过的领域也操作；模型、世界、verifier共同演化；用grounded verifier作奖励做RL可把agent推过模仿阶段。Microsoft开放其中4个世界的代码、数据与grader。
  > 💡 关键不是堆世界数量而是"深度+演化"：浅层环境致回退、深层才出增益，说明computer-use agent训练从"截图规模竞赛"转向"有真实后果的状态保真度竞赛"；verifier与模型共同演化是把agent从模仿推到RL自主达成目标的关键引擎。
   - 来源: [Microsoft Research](https://www.microsoft.com/en-us/research/blog/echoverse-deep-evolving-environments-for-computer-use-agents/) | [Publication](https://www.microsoft.com/en-us/research/publication/echoverse-deep-evolving-environments-for-training-computer-use-agents-at-scale/)

**EvoLib：让黑盒LLM在推理时自学习、无需模型更新**
- Microsoft Research提出EvoLib（论文 *Test-Time Learning with an Evolving Library*），让大语言模型在推理过程中从自身经验学习，无需ground-truth标签或外部反馈。EvoLib把过去的尝试转化为可复用技能与反思性洞察并应用于未来任务，有用的技能与洞察被持续提炼、整合、重新加权，把实例级观察逐步转为越来越通用的知识，并可跨任务迁移。因不需要模型更新，EvoLib可叠加到任意通过API部署的黑盒语言模型与AI系统上。作者包括Weijia Xu、Alessandro Sordoni、Michel Galley、Eric Yuan、Jianfeng Gao等。
  > 💡 "记忆≠学习"是这篇的核心命题：把经验档案提炼为可演化、可迁移的技能库而非简单存取记忆，且能挂载到任意API黑盒模型上，使test-time learning成为不依赖模型权重的轻量自学习层；与Echoverse的"训练时演化"形成推理时/训练时两条互补路径。
   - 来源: [Microsoft Research](https://www.microsoft.com/en-us/research/blog/evolib-turning-experience-into-evolving-knowledge/) | [arXiv](https://arxiv.org/abs/2605.14477)

**Evolvent AI开源RSIBench-Data：评估agent能否像研究者一样做数据中心的递归自我改进**
- Evolvent AI发布并开源RSIBench-Data，该benchmark不再问"agent能否解决又一个难题"，而是问"agent能否像研究者工作"：诊断模型弱点、设计训练数据、根据反馈refine post-training策略、最终产出更好的模型。实验显示agent已能做自主研究和有意义的策略改进，但离可靠的递归自我改进仍有距离。论文披露一个扎眼结果：**78%在越过最好分数后继续的搜索最终变得更差**——agent能在能识别和保留好结果之前就找到好idea，checkpoint选择本身是研究的一部分而非收尾。项目代码与网站已开源，团队邀请模型实验室送模型来测。
  > 💡 把"递归自我改进"从口号拆成可测维度（诊断-设计-训练-反馈），并暴露出"能找到好idea但识别不住"的checkpoint选择短板，是对Cline那条"单prompt跑出SOTA"叙事的关键校准：递归自我改进目前的价值瓶颈在"评估与保留"而非"生成"。
   - 来源: [arXiv](https://arxiv.org/abs/2607.25886)

**CoRT用反事实重放做token级信用分配，给GRPO带来4.4个百分点平均增益**
- 论文提出CoRT（反事实重放，Counterfactual Replay for Token-Level Rubric-Guided Policy Optimization），针对rubric-based RL中GRPO把结构化判断压成标量奖励再均匀广播到所有token、导致response内无显式信用分配的缺陷。CoRT不训练辅助评分模型，而是用反事实重放在原始rubric prompt与匹配的无criteria prompt下对同一response重新评分，以token级对数似然差异作为"对rubric上下文依赖度"的代理，映射为有界、归一化的权重重分配GRPO的有符号advantage。在多个指令微调模型与奖励粒度上，CoRT绝大多数对比优于response级GRPO，平均增益**4.4个百分点**，且无需额外相关性学习阶段即可与学习的token级信用基线竞争。
  > 💡 用"同一response两次条件prompt的反事实对数似然差"替代辅助评分器做token级信用分配，是把rubric信号从response级下沉到token级的低成本路径，保留GRPO简单与稳定。
   - 来源: [arXiv](https://arxiv.org/abs/2607.25659)

**论文首次系统评估LLM agent的文件系统记忆：组织能省钱却换不来更好答案**
- 论文首次系统研究LLM agent把长期记忆存为文件系统（markdown目录树，agent用通用文件工具自读自写自重排）的做法，检验两个此前未被验证的假设：agent能否在记忆累积、冲突、过时中保持store有序，以及组织是否"值"。设定形式化为围绕一个记忆文件系统的三角色——management agent整合组织内容、search agent带引用回答、execution agent提供被蒸馏为skills的任务轨迹。在长对话基准与具身任务上变动记忆形态（自组织层级/原文dump/chunk检索）、流规模、工具harness及agent强度。结论：organized store在材料量大时约**减半检索成本**；但除最强management agent外组织都会退化，且**无被测agent把组织转化为更好答案**；**单独改变工具集对store形状的重塑力度与换模型一样强**。作者包括UCSD的Jiawei Han、Julian McAuley等。
  > 💡 对"agent记忆=文件夹+自己整理"这一默认实践的第一份系统审计：组织只在检索成本维度成立、答案质量维度失效，说明瓶颈在"把整理转化为决策收益"而非"会不会整理"；"换工具集≈换模型"提示记忆系统工程层与模型层权重相当，与EvoLib"把经验提炼为可演化技能库"形成参照——文件系统记忆是substrate不是learning system。
   - 来源: [arXiv](https://arxiv.org/abs/2607.26637) | [@dair_ai](https://x.com/dair_ai/status/2082883931582713893)

### X讨论
**Cline用递归自我改进把Kimi K3推到Terminal-Bench 2.1的88.8%，成本不到Fable 5十分之一**
- Cline发布编码agent的递归自我改进实验：一条prompt触发以GPT-5.6-Sol为leader、Kimi K3执行的17小时连续运行，消耗约10亿token（4亿coding+6亿eval），在Terminal-Bench 2.1取得**88.8%**、成本仅**49.8美元**（Fable 5花552美元、GPT-5.6 Terra花400美元）。Cline称模型自主提交PR式hill climb，把过去需4人团队数周的人肉trace阅读-假设-修复压缩为单工程师单prompt；用Fable 5做同样实验时其AI安全过滤器反复把模型降级到Opus-4.8而放弃。Moonshot自身vendor-reported SOTA为88.3%，Cline用通用harness首次递归campaign即追平，并称瓶颈已不是模型而是使用模型的人。
  > 💡 单prompt×17小时×10亿token跑出SOTA，是"agent改进agent的harness"首次工程化落地的硬证据；Fable 5因安全过滤放弃递归、Cline通用harness追平vendor自报SOTA，分别指向"安全过滤与自主性张力"和"厂商报告与第三方harness的差距"两条线索。
   - 来源: [Cline](https://cline.bot/blog/recursive-self-improvement-for-coding-agents) | [@cline](https://x.com/cline/status/2082544250148057240)

---
*更新时间: 2026-07-31 10:10*