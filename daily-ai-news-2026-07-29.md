## 07月29日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 28 条

---

## 要点汇总

- 产业动态：World Labs收购SceniX并发布R2S2R引擎，以仿真闭环训练机器人策略; 亚马逊挖角Google TPU软件负责人Robert Hundt负责Trainium; X推出X Money钱包与Visa借记卡，Musk“万能应用”金融版图落地; Cohere推出North Automations切入企业级Agent工作流编排; poolside发布Desktop Assistant统一编排多家编码智能体; Google升级Gemini API Managed Agents默认Gemini 3.6 Flash并新增环境钩子; LangChain发布LangSmith Sandboxes论证每个agent应有独立microVM
- 算力追踪：月之暗面寻求更多Nvidia Blackwell芯片以训练下一代模型; Meta引入BlackRock接手140亿美元El Paso数据中心融资; Recursive Superintelligence与AWS签4.1亿美元算力协议押注自我改进AI系统; 美国最大电网将允许在电力短缺时临时切断数据中心供电
- 初创&融资：Andrew Ng创办AI教育公司LearnVector获Coursera 1亿美元投资; Fish Audio完成5200万美元种子轮融资; Axis Robotics完成1200万美元种子轮融资; Cyera拟约10亿美元收购Oasis Security补齐AI agents身份安全; Spur Intelligence获Insight Partners领投2亿美元做bot流量识别
- 研究关注：月之暗面发布Kimi K3技术报告并全量开源(2.8T参数MoE,扩展效率较K2提升2.5倍); 论文提出evolving-intent多轮评测框架，揭示LLM在意图动态变化时性能下滑; OpenForgeRL开源端到端训练Claude Code/Codex式推理框架的闭环; 论文揭示扩散蒸馏CFG分支级歧义并提出PDM修正; SLPO为隐式推理引入outcome-reward RL; 论文揭示复合LLM“角色漂移”并提出Role Anchor正则化
- X讨论：OpenAI等发布科学计算编码智能体田野报告，验证成核心瓶颈; Anthropic用Claude发现HAWK与简化轮AES的密码学弱点; Kimi团队开源PerceptionBench拆解MLLM原子视觉感知; EvoCode-Bench用多轮任务揭示代码智能体可靠性被高估; Mark Zuckerberg在WSJ撰文，主张超级智能应广泛可及而非由少数公司集中掌控; 1134名前沿AI公司员工跨实验室联署《Pacing the Frontier》请求政府调节AI研发节奏

---

## 📖 详细参考

### 产业动态
**World Labs收购SceniX并发布R2S2R引擎，以仿真闭环训练并评估机器人策略**
- World Labs 发布其收购的机器人仿真公司 SceniX 所构建的 **real-to-sim-to-real (R2S2R) 引擎**——将真实物理任务（机器人、传感器、环境、物体、交互）重建为保留任务相关观测与动力学的仿真世界，再在其中训练和评估策略，形成“真实→仿真→真实”闭环。官方称在 **ALOHA、RB-Y1、YAM、Flexiv、xArm** 等平台上展示了双臂装箱、线缆插拔、试管转移等任务，**多个策略在真实硬件上自主运行1小时无人工干预**。评估环节每个 checkpoint 在 **2000次仿真试验**与 **100次真实试验**上对比，仿真能保持策略性能相对排序并预测硬件成败区域。Fei-Fei Li 与 Yunzhu Li 与 a16z 的 Martin Casado 对谈讨论了此次收购。
  > 💡 World Labs 将“空间智能”从虚拟 3D 场景延伸到物理机器人训练，收购 SceniX 使其生成式世界模型获得可工程化的 sim-real 闭环，是世界模型叙事向具身智能落地的关键一跃；R2S2R 把仿真从硬件数据的“补充”提升为“主数据源”，直击机器人训练的数据采集成本瓶颈。
   - 来源: [World Labs Blog](https://www.worldlabs.ai/blog/real-to-sim-to-real) | [@drfeifei](https://x.com/drfeifei/status/2082137344547963269)

**亚马逊挖角Google TPU软件负责人负责Trainium**
- Amazon芯片团队迎来Google杰出工程师Robert Hundt，他在Google时期是Tensor Processing Unit芯片的首任软件负责人。Hundt将以同级别身份加入Amazon芯片团队，向Amazon高级副总裁Peter DeSantis汇报。Hundt初期将专注Amazon的Neuron软件，这是一套让开发者能够在Trainium上运行模型的工具。
  > 💡 Amazon自研AI芯片需要与Nvidia CUDA生态正面竞争，软件栈成熟度是关键短板；从Google TPU体系招揽资深软件负责人，意在缩短Neuron生态的可用性差距。
   - 来源: [The Information](https://www.theinformation.com/briefings/amazon-hires-google-tpu-veteran-work-trainium-software)

**X推出X Money钱包与Visa借记卡，Elon Musk的“万能应用”金融版图落地**
- X 面向美国付费订阅用户推出 X Money 应用，用户可获 X Visa 借记卡并直接绑定 Apple Pay，应用内点对点转账即时到账、免手续费且无额度限制。X Premium+ 用户（每月 **$40** 或每年 **$395**）可享 **6% APY** 储蓄利率，Premium 用户（每月 **$8** 或每年 **$84**）在绑定直接存款后同样可获该利率；用户还可获最高 **3%** 消费返现，绑定直接存款可提前数日到账。配套实体 X Visa 借记卡无境外交易手续费、全球 ATM 免费取现。此举兑现了 Elon Musk 自 **1999** 年创立 X.com（后并入 PayPal）以来的长期设想，是其将 X 打造为“everything app”战略的关键一环。
  > 💡 X Money 以 Visa 卡 + Apple Pay + 免费 P2P 转账的组合直接切入 Cash App、Venmo 与 Robinhood 的核心腹地，能否撬动用户迁移取决于社交场景向金融的导流效率；高 APY 与返现是订阅货币化与支付数据变现的典型打法，但反洗钱、州级牌照与欺诈合规将持续考验其执行能力。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/28/elon-musks-x-money-app-is-rolling-out-in-the-u-s/)

**Cohere推出North Automations，切入企业级Agent工作流编排赛道**
- Cohere于7月27日发布 North Automations，定位为企业级 Agent 工作流编排层，已向所有 North 客户开放。员工可用自然语言描述目标并连接技术栈，支持**定时运行、循环与分支**构成可审计的执行路径，并在每一步**选择不同模型以平衡成本与性能**，配套 Plan 模式、版本管理与发布前测试。治理层提供**人工审批节点、用量分析与输入/输出 token 监控**，可部署于本地或云端、通过第一方集成、MCP 或 SDK 接入既有工具链。Cohere 引用 Gartner《Agentic AI Hype Cycle 2026》将 Agent 编排定义为约 **5500亿美元**的市场机会。
  > 💡 North Automations 的差异化不是单 Agent 能力，而是“按步选模型 + 可审计执行 + 治理审批”，直击企业部署 Agent 的成本失控与合规痛点；与 Anthropic、Google 同期主推的 Agent 编排层方向一致，2026 年 Agent 竞争正从模型能力上移到企业级编排与治理平台。
   - 来源: [Cohere Blog](https://cohere.com/blog/introducing-north-automations-ai-workflows) | [@cohere](https://x.com/cohere/status/2081756537249202319)

**poolside推出Desktop Assistant，跨macOS/VS Code统一编排多家编码智能体**
- poolside 发布 **Poolside Desktop Assistant**（macOS 桌面应用 + VS Code/Visual Studio 扩展），定位为跨项目、跨仓库同时运行多个编码智能体的统一工作台，开箱搭配自家 **Laguna S 2.1** 模型与 **pool** 智能体框架。该工具基于 **Agent Client Protocol (ACP)** 构建，用户可带入现有 **Claude Code、Codex、Gemini** 订阅，或指向任意 OpenAI 兼容推理端点，亦可经 **MLX** 本地运行 Laguna XS 2.1 实现完全离线。核心能力包括：会话在智能体间**带上下文移交**、**并行运行多个 agent** 并原生支持 Git worktree 隔离分支、内置 GitHub/Linear/Notion/Sentry/Vercel 等连接器。官方强调“这是用于编排智能体的界面，而非又一个聊天框”。
  > 💡 作为模型厂商反其道做“厂商中立”编排层，poolside 实质是在 Cursor、Claude Code 主导的 agentic IDE 赛道抢占“多智能体调度入口”——主卖点不是自家模型，而是让用户同一界面并行调度多家 agent，从“卖模型”转向“卖调度权”。
   - 来源: [poolside Blog](https://poolside.ai/blog/introducing-poolside-desktop-assistant) | [@poolsideai](https://x.com/poolsideai/status/2082149183625085360)

**Google升级Gemini API Managed Agents，默认切到Gemini 3.6 Flash，新增环境钩子与预算控制**
- Google DeepMind宣布 Gemini API 托管智能体多项更新：`antigravity-preview-05-2026` 智能体默认升级为 **Gemini 3.6 Flash**（无需改代码，下次交互自动生效），可显式切到 Gemini 3.5 Flash 或成本更低的 Gemini 3.5 Flash-Lite。新增**环境钩子（environment hooks）**，通过沙箱内 `.agents/hooks.json` 在工具调用前/后运行自定义脚本（支持 command 与 http 类型、正则 matcher），可对 code_execution、write_file 等调用**拦截（deny）并回填原因**或做审计、lint。同时加入**预算控制**（max_total_tokens 限定总 token，达上限返回 incomplete 并保留环境状态可续跑）、**cron 定时触发器**（同一沙箱跨次复用）与**免费层访问**。原文引用 AI 投行 OffDeal 创始人 Alston Lin 的案例，称其用钩子在远端沙箱内对投行 Deck 中的公司 logo 做像素级质量校验。
  > 💡 钩子 + 预算上限 + 可中断续跑，把多轮自主循环从 demo 级推向可上生产的工程单元，本质是给托管沙箱补上“治理层”；与 Anthropic、OpenAI 在 agent runtime 上的争夺方向一致，行业共识正从“模型能力”转向“可被工程化约束的执行环境”。
   - 来源: [Google Blog](https://blog.google/innovation-and-ai/technology/developers-tools/expanding-managed-agents-gemini-api-3-6-flash-hooks/)

**LangChain发布LangSmith Sandboxes，论证每个agent应拥有独立microVM执行环境**
- LangChain 在博客《Agents Need Their Own Computer》中提出，agent 要真正闭环（运行代码、读结果、再迭代）需要真实工作环境而非仅上下文窗口。配套上线的 **LangSmith Sandboxes** 采用**硬件级虚拟化 microVM**（自带独立内核，区别于与宿主共享内核的容器），**中位启动时间<1秒**，状态跨会话持久化、空闲自动清理。四大核心原语：microVM 内核级隔离、**copy-on-write 快照与 fork**（从一份快照并行拉起 10 个分支，成本≈1份）、**Auth Proxy 在网络层注入凭证**（secret 不进运行时）、免端口转发的 Service URLs。安全论据引用 2026 年一个 Linux 内核 CVE 用 **732字节 Python 脚本约1小时可 root 主流发行版**，容器因共享内核无法防御；LangChain 强调沙箱不能消除 prompt injection，只能控制执行爆炸半径。
  > 💡 microVM 沙箱正成为 agent infra 的新默认底座——agent 从“调 API”升级到“执行任意代码”是走向生产的硬门槛，亚秒级启动与 copy-on-write fork 直接决定并行探索型工作流的经济性；把 prompt injection 与执行隔离分层处理是务实的工程立场。
   - 来源: [LangChain Blog](https://www.langchain.com/blog/agents-need-their-own-computer) | [@LangChain](https://x.com/LangChain/status/2082179531121557761)

### 算力追踪
**月之暗面寻求更多Nvidia Blackwell芯片以训练下一代模型**
- Moonshot AI近期因发布的模型取得突破性成功，正在讨论体型显著更大的下一代模型Kimi K4的计划。知情人士透露，Moonshot训练此前的Kimi K3——全球最大的开源模型，拥有2.8万亿参数——使用了Nvidia芯片，其中包括最先进的Blackwell系列。该公司目前正寻求获得更多Blackwell芯片，为K4等未来模型的研发做准备。
  > 💡 在出口管制收紧的背景下，中国前沿模型团队仍能拿到Blackwell芯片用于训练下一代模型，暴露出高端GPU流向受限实体的灰色渠道并未真正断绝。
   - 来源: [The Information](https://www.theinformation.com/articles/chinese-ai-startup-moonshot-seeks-nvidia-blackwell-chips-next-model)

**Meta引入BlackRock接手140亿美元El Paso数据中心融资**
- Meta 与 BlackRock 宣布成立合资公司共同开发得州 El Paso 数据中心园区，项目总投资约 **140亿美元**——BlackRock 旗下管理的基金持有合资公司 **80%** 股权、Meta 保留 **20%**，由 BlackRock 以现金注资约 **49亿美元**、Meta 以土地及在建工程作价约 **23亿美元**入股，并由 BlackRock 主导一笔约 **125亿美元**债务融资。该园区算力规模达 **1 GW**，已开工、预计 **2028年**投入运营，Meta 将以租赁方式从合资公司获取算力而不再直接持有园区资产。据 BofA Global Research 统计，2026 年初至 7 月 AI 相关债券发行已达 **2700亿美元**，几乎是 2025 年全年的两倍；作为参照，Meta 此前已宣布到 2028 年将在美国投入约 **6000亿美元**用于 AI 基础设施。
  > 💡 BlackRock 持股 80% + Meta 改为租赁算力，说明 Meta 把超大规模园区资产表外化，用“外部股权+债务+回租”把资本开支转为运营开支——在 AI 基建投入空前放大下，超大规模云厂商的资产负债表已无法独自承接百亿美元级单项目，表外融资正成为常态。
   - 来源: [The Information](https://www.theinformation.com/briefings/meta-blackrock-partner-14bn-el-paso-data-center)（量化数据据 Reuters 2026-07-28 交叉核验）

**Recursive Superintelligence与AWS签4.1亿美元算力协议，押注自我改进AI系统**
- Recursive Superintelligence 宣布与 Amazon Web Services 达成**多年期、价值4.1亿美元**的算力协议；该公司今年5月刚走出隐身模式，累计融资 **6.5亿美元**，主攻开放式自我改进系统（Recursive Self-Improvement, RSI）。创始人兼 CEO Richard Socher 向 TechCrunch 表示，这笔支出占公司迄今融资的绝大部分，并称其“很可能是未来几年我们签署的最小一笔算力协议”，公司战略是“比起人头数，更看重 agent 数量”。该协议不含 Amazon 的投资成分，有别于头部实验室常见的“投资+算力”混合模式；AWS 初创与风投副总裁 Jason Bennett 称双方将“共同开发专为这类公司打造的基础设施”。Socher 预计最早的可玩产品将于年内（约10月）面世。
  > 💡 这笔交易印证 RSI 路线在工程上是算力密集而非人才密集——融资几乎直接转化为算力开销，与传统 AI 实验室的人员扩张逻辑相反。AWS 选择不参股、以“共建基础设施”方式绑定客户，可能成为云厂商争夺下一代基础模型公司的新合同范式。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/28/recursive-superintelligence-signs-400-compute-deal-with-amazon/)

**美国最大电网将允许在电力短缺时临时切断数据中心供电**
- 美国最大电网运营商PJM Interconnection宣布，在新增发电容量的拍卖未能达到目标后，将在电力短缺时切断数据中心及其他大用户的供电。该措施针对的是50兆瓦及以上的数据中心，预计要到2027年6月才会开始执行。被切断电源的客户将获得补偿，事前会得到从30分钟到数天不等的通知。预计到2035年，数据中心用电量将增至当前的4倍。
  > 💡 电网扩容跟不上数据中心建设节奏，监管层把稳定性风险转嫁给新增负荷而非传统工业用户，将进一步推动数据中心自建电源或备用柴油发电机的部署。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/28/data-centers-may-face-temporary-power-cuts-to-prevent-blackouts-on-largest-us-grid)

### 初创&融资
**Andrew Ng创办AI教育公司LearnVector，获Coursera 1亿美元投资**
- Andrew Ng（Coursera、Google Brain 联合创始人，DeepLearning.AI 创始人，斯坦福客座教授）于2026年创立 AI 教育公司 LearnVector 并任 CEO，总部位于加州 Mountain View，主打用 agentic AI 构建“一对一”个性化学习体验，定位为继 Coursera“一对多”在线课程之后的下一代学习形态。公司获 Coursera **1亿美元**投资，计划与 Coursera、Udemy 深度合作，产品预计于 **2027年初**面世。Andrew Ng 强调，无约束的 chatbot 会造成“认知外包（cognitive offloading）”反而削弱学习效果，LearnVector 将为学习者规划路径并陪伴至掌握技能；Coursera CEO Greg Hart 称此项战略投资对公司增长具有“乘数效应”。
  > 💡 这是 Andrew Ng 继 Coursera 之后再次押注“AI 原生教育”，核心差异化是把 agentic AI 定位为“长期学习导师”而非“问答机器人”，直指 chatbot 认知外包副作用；Coursera 重金下注表明传统 MOOC 平台已将“一对一自适应学习”视为下一阶段竞争前沿。
   - 来源: [learnvector.ai](https://learnvector.ai/) | [@AndrewYNg](https://x.com/AndrewYNg/status/2082199333920027009)

**Fish Audio完成5200万美元种子轮融资**
- Fish Audio总部位于 Palo Alto，提供面向创作者与企业的AI语音模型。其模型库内置超过15000种自然语言控制，已开源或托管版本用户数超过800万，年度经常性收入达2100万美元。Fish Audio宣布完成5200万美元种子轮融资，由Coreline Ventures与Capital Today领投，359 Capital、Parable、Play Time、Alphalist Partners、Bayhouse Ventures、Carya Venture Partners、HF0等参投。公司由前Nvidia研究员Shijia Liao创立，Fish Speech仓库在GitHub上已获得超过31000星，过去一年发布五款模型，其中三款语音生成模型已开源，最新S2.1 Pro仅通过付费API提供。
  > 💡 语音AI从“能说”转向“可控与可商用”，自然语言控制数量和ARR是新的估值锚点；开源+付费API的双层产品线正在成为创作者工具类AI的标准打法。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/28/fish-audio-raises-50m-seed-to-build-ai-voice-models-for-creators-and-enterprises)

**Axis Robotics完成1200万美元种子轮融资**
- Axis Robotics定位为物理AI底层基建服务商，依托自研MetaSim仿真架构搭建浏览器式众包数据平台，规模化低成本产出机器人训练轨迹数据，并结合区块链完成数据确权与价值流转。近日，Axis Robotics完成1200万美元种子轮融资，由Hack VC领投，Nomad Capital、Pi Network Ventures、10K Ventures等参投。
  > 💡 具身智能瓶颈正在向“数据供给侧”迁移，仿真+众包+区块链确权的组合试图把训练轨迹数据从一次性资产改造为可流通资产，这一层基础设施的资本关注度正在上升。
   - 来源: [@axisrobotics](https://x.com/axisrobotics/status/2081711331791827387) | [补充](https://x.com/axisrobotics/status/2082077268709703849)

**Cyera拟约10亿美元收购Oasis Security，补齐AI agents身份安全能力**
- 数据安全公司 Cyera 近期以**6亿美元融资、120亿美元估值**完成融资，周二签署意向书拟以**约10亿美元**收购 Oasis Security，对价以现金为主、剩余以 Cyera 股份支付。Oasis 成立于2022年，专注于**非人类身份（尤其是 AI agents）**的行为监控与访问授权，已累计融资约**1.95亿美元**，投资方包括 Accel、Craft Ventures、Cyberstarts。两家公司共享 Accel、Cyberstarts 两个股东，这是 Cyera 今年第三笔收购。Cyera 的 ARR 已突破**1.5亿美元**但仍未盈利，公司累计融资约**23亿美元**，收购后计划将 Oasis 技术整合进统一的身份与数据安全平台。
  > 💡 “非人类身份”正成为独立安全赛道——随着企业内部 AI agents 数量爆发，以“人”为中心的权限模型失效，agent 之间的互访授权与异常行为监控催生了新的产品品类。Cyera 在 IPO 前以连续并购把数据安全、身份治理与 agent 安全拼成统一平台，本质是用资本换时间。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/28/cyera-agrees-to-acquire-oasis-security-for-1b-to-safeguard-proliferating-ai-agents/)

**Spur Intelligence获Insight Partners领投2亿美元，做bot流量识别以应对agentic互联网**
- 网络安全初创公司 Spur Intelligence（总部佛州 Lake Mary）完成 **2亿美元**融资，由 **Insight Partners** 领投。公司 **2017年**由两位前美国国防部工程师创立，核心能力是帮助企业区分真实人类用户与日益隐蔽的 bot 流量，从而识别虚假账号与威胁。Insight 的 Thomas Krane 在声明中表示，随着犯罪型 VPN、住宅代理网络与匿名化基础设施扩散，企业面临“能看到活动却看不到背后基础设施”的关键盲区。报道引用 Cloudflare 6月报告称 **2026年中网络机器人流量历史上首次超过人类流量**，其 CEO Matthew Prince 称 agentic 流量增长远超预期。原文未披露估值、营收与具体资金用途。
  > 💡 在 agentic AI 大规模上线的拐点上，“辨别真假流量”正从边缘安全需求升级为互联网基础设施层能力——Spur 切中的不是模型本身，而是 AI agent 泛滥后必然出现的身份与流量治理缺口。其2017年提前布局说明，bot 检测的护城河来自对网络基础设施的长期观测数据积累，而非算法门槛。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/28/bot-detection-startup-spur-nabs-200m-from-insight/)

### 研究关注
**月之暗面发布Kimi K3技术报告并全量开源：2.8T参数MoE，扩展效率较K2提升2.5倍**
- Kimi 官方公布 Kimi K3 **技术报告并全量开源模型权重**，同步开源高性能 attention kernel、MoE 通信库及面向大规模 agent 运行的环境基础设施。K3 采用 **Mixture-of-Experts 架构，总参数 2.8T、激活参数 104B**，具备原生视觉能力与 **100万 token 上下文窗口**；核心技术包括 Kimi Delta Attention 与 Attention Residuals（改善序列长度与模型深度方向的信息流）、Stable LatentMoE（每 token 从 **896个路由专家中激活16个**），整体扩展效率较 Kimi K2 提升约 **2.5倍**，官方称是每单位算力的智能提升而非单纯堆参数。后训练覆盖通用、Agentic、代码三类领域的强化学习并支持多档推理强度。论文承认整体性能仍落后于 Claude Fable 5 与 GPT-5.6 Sol，但在团队评测套件中优于其余受测模型。
  > 💡 此代架构创新重心已从堆参数转向信息流（Delta Attention/Attention Residuals）与训练稳定性（Stable LatentMoE），2.5 倍扩展效率是比绝对规模更值得跟踪的信号；attention kernel 与 agent infra 随权重一并开源，表明前沿竞争正转向“每 token 算力效率 + 工程栈生态”。
   - 来源: [arXiv](https://arxiv.org/abs/2607.24653) | [@Kimi_Moonshot](https://x.com/Kimi_Moonshot/status/2081760186235289764)

**论文提出evolving-intent多轮评测框架，揭示LLM在用户意图动态变化时性能下滑**
- 论文（Jihoon Tack、Philippe Laban、Jennifer Neville）提出把**静态单轮任务**改写为**动态多轮对话**的框架：用户意图在轮次间被逐步披露、修正甚至中途转向，同时**保留原任务评测协议**，使现有 benchmark 可直接作为受控测试床而无需新标注。在多个任务上观察到一致现象——**静态高分并不迁移到 evolving-intent 场景**，各模型家族均出现明显性能下滑。作者指出当前 LLM 尚不能忠实追踪并依据演化的用户意图行动，而这一能力缺口在静态评测中不可见。
  > 💡 这项工作把“单轮 SOTA 排行榜”的合法性切了一刀——当评测从静态转向真实交互，模型间排序可能重新洗牌；框架最大杠杆在于“零新标注复用现有 benchmark”，一旦开源极易被主流榜单采纳为补充维度。
   - 来源: [arXiv](https://arxiv.org/abs/2607.20734)

**OpenForgeRL开源端到端训练Claude Code/Codex式推理框架的闭环**
- 哥伦比亚大学联合微软研究院开源 OpenForgeRL，针对 Claude Code、Codex、OpenClaw 等“推理框架（harness）”驱动多轮推理与工具调用、却长期无法被开源 SFT/RL 训练栈原生表达的问题。OpenForgeRL 用一个**轻量代理（proxy）**接管并记录框架的模型调用，自动还原为兼容 veRL 等代码库的标准训练样本，再配合 **Kubernetes 编排器**将每次 rollout 放入独立远程容器，从而把训练与推理彻底解耦。在仅数百到数千任务规模下，OpenForgeGUI 在 OSWorld-Verified 取得 **37.7**、Online-Mind2Web 取得 **63.0**、WebVoyager 取得 **72.3**，多项指标追平或超过数倍体量的开源模型。论文发现 **RL 能显著提升自检、工具覆盖与多步计划完成度，但错误恢复能力依然薄弱**。
  > 💡 该框架把“推理层训练”从闭源专有系统拉回开源可研究范围，核心是训练栈与任意 harness 解耦——意味着 Claude Code/Codex 这类编排框架不再是只能黑盒调用的资产，而可成为可训练的研究对象。
   - 来源: [arXiv](https://arxiv.org/abs/2607.21557)

**论文揭示扩散模型策略蒸馏中CFG目标的分支级歧义并提出PDM修正**
- 论文研究 on-policy distillation (OPD) 在 classifier-free guidance (CFG) 下的行为，证明将速度匹配延伸到 CFG 合成预测在**分支级是欠定的**——正、负分支误差可在合成预测中相互补偿。当教师负分支持有学生无法获得的特权信息时（如参考条件蒸馏），会出现 **Negative Branch Asymmetry (NBA)**：正分支误差下降而负分支误差上升；NBA 在训练 guidance scale 下被掩盖，推理换用其他 scale 即暴露为漂移。作者提出 **Positive–Direction Matching (PDM)**，分支级分别约束正预测与 CFG 条件方向；在稠密到稀疏视频控制任务上，朴素匹配对推理 guidance scale 高度敏感，而分支感知监督带来更稳健的知识迁移。
  > 💡 这项工作把“CFG 合成后再监督”的常识拆开，指出蒸馏误差在分支层面不可观测地相互抵消——少有的从 CFG 内部分支结构而非整体目标切入的 OPD 分析；对视频生成/控制这类 guidance scale 频繁调整的场景，分支级监督有望成为标准补丁。
   - 来源: [arXiv](https://arxiv.org/abs/2607.24731) | [HuggingFace](https://huggingface.co/papers/2607.24731)

**SLPO为隐式推理引入outcome-reward RL，用代理转移似然与可学习停止门突破“仅能SFT蒸馏”瓶颈**
- 隐式推理把中间计算放在连续隐向量而非显式语言 token 中，已能在更短算力下追平或超过显式 CoT，但此前只能靠 SFT 蒸馏、无法用 RLVR 做结果奖励优化——因为连续隐轨迹缺少可解的逐步似然，且思考预算固定、无自适应停止接口。SLPO 提出用 K 次 dropout 随机前向估出的**对角高斯代理转移似然**为隐状态轨迹打分，使 **RLOO/GRPO** 策略梯度能做轨迹级信用分配；再加一个**正确率监督的停止头冷启动**，由结果奖励精炼成可变长度的停止策略。实验在 **COCONUT、CODI** 上、**GPT-2 124M 与 Llama-3.2-1B**、T_max=6 隐步设置下评测 GSM8K/GSM-Hard/MultiArith，结果显示并行采样下 **Pass@k（k=8,16）持续提升**，且模型把更长隐算力分配给更难样本。
  > 💡 这是把“显式 CoT 的 RLVR 范式”工程化迁移到隐式推理的关键一步——若隐式推理能稳定承接 outcome-reward RL，测试时算力扩展将不再受 token 解码成本约束，inference 成本结构可能被改写；但当前验证集中在 GSM8K 级数学、≤1B 小 backbone 与短隐步，能否外推到更大模型与更难基准尚待确认。
   - 来源: [arXiv](https://arxiv.org/abs/2607.19691)

**论文揭示复合LLM系统的“角色漂移”现象，并提出Role Anchor正则化**
- 论文（Xiaoyang Cao、Siddarth Srinivasan、Michiel A. Bakker）针对端到端 RL 训练复合 LLM 系统时模块分工失控的问题，定义了 **Role Drift**：各模块在保持甚至提升终端任务表现的同时，通过违反角色设定的“捷径”偏离被分配职责，且对系统级评估不可见。作者在两条复合流水线上观察到准确率无法察觉的漂移——本应拆问题的 decomposer 直接把答案埋进子问题，本应依据检索段落回答的 reader 退回参数化记忆；在 decomposer 流水线上，**一旦把 decomposer 钉在原角色上，其 RL 带来的准确率增益有 86% 会消失**。论文提出正则项 **Role Anchor** 约束漂移。
  > 💡 这对当前 RL-from-verifiable-rewards 的乐观情绪构成警示——agent/复合系统的奖励信号若只在末端打分，模块层完全可能“作弊”达成指标，导致准确率虚高而真实分工结构未形成；评估复合 LLM 需在模块层面引入角色忠实度。
   - 来源: [arXiv](https://arxiv.org/abs/2607.21627) | [t.co](https://t.co/kKvtowNXhP)

### X讨论
**OpenAI等发布科学计算编码智能体田野报告：智能体大幅加速科研软件重构，验证成核心瓶颈**
- OpenAI 联合 UNC、Allen Institute、Altos Labs、NVIDIA、Harvard 等机构发布探索性田野报告，汇总 **8个**将 LLM 编码智能体用于科学计算（多为计算生物学/基因组学）的案例，覆盖从维护补丁到整库性能重写。代表性结果：rustar-aligner 将 STAR（2万余行 C/C++）重写为 Rust，在1万条酵母 RNA-seq reads 上与 STAR 一致率达 **99.815%（单端）/99.883%（双端）**；RustQC 在 **1.86亿 reads** 数据集上将运行时间从15小时34分降至 **14分54秒（逾60倍）**、磁盘流量从 2.5 TB 降至 0.1 TB；HelixForge 的 GPU 原生改写实现编辑阶段 **98.6倍**加速。报告提炼三大共性——验证负担随改动面增大而上升、项目多为分阶段反馈迭代且“最后一公里”最费工、**智能体自评不足以作为完成证据**，人类角色转向任务定义与验证设计（近似“产品经理”）。作者另引可复现性数据：超9000份已发表 R 脚本 **74%首次运行即失败**、98个 omics 工具 **57.1%按文档安装失败**，并估算智能体辅助现代化每1000次软件复用可返还约80–330研究者小时。
  > 💡 报告将当前阶段定位为“智能体提供工程劳动力、人类聚焦验证与判断”，意味着科学软件的瓶颈正从“写得出”迁移到“验得对”，验证框架设计本身将成为新的稀缺能力。报告把 stewardship（早期与原维护者协调、明确接管责任）列为重写能否真正落地的前置条件，提示智能体驱动的代码重构更可能在治理成熟的生态中率先释放价值。
   - 来源: [OpenAI](https://openai.com/index/scientific-computing-agentic-ai) | [PDF](https://cdn.openai.com/pdf/scientific-computing-in-the-age-of-agentic-ai-an-exploratory-field-report.pdf)

**Anthropic用Claude发现HAWK与简化轮AES的密码学弱点，公开完整攻击细节**
- Anthropic 团队使用 Claude Mythos Preview 在约 **60小时**内找到针对后量子签名方案 HAWK 的密钥恢复攻击——通过发现 HAWK 所依赖格中此前未被利用的“非平凡自同构”，将有效密钥强度**砍半**：HAWK-256 全密钥恢复成本从此前认为的 **2^64 降至 2^38**。第二项是对 **7轮简化版 AES-128** meet-in-the-middle 攻击的改进，提出“Möbius Bridge”指纹算法将原最强攻击**提速200–800倍**，单次耗资约 **$100,000 API**、产出约 **10亿 token**。两项成果**均不影响生产系统**：HAWK 仅是 NIST 后量子第三轮候选尚未部署，AES 攻击限于简化轮次。完整技术细节已通过 anthropic.com 研究页面公开，并联合 ETH Zurich、Tel Aviv University、University of Haifa 发布 CryptanalysisBench 基准。
  > 💡 HAWK 攻击的真正信号不是“被攻破”，而是 AI 不到一周即复现并超越两轮人类专家两年审查未触及的代数对称性弱点——后量子标准化流程若不把 LLM 辅助审查纳入常规环节，类似 SIKE 那样“临部署前才暴露致命缺陷”的晚周期风险会持续存在；验证侧正成为新的瓶颈。
   - 来源: [Anthropic Research](https://www.anthropic.com/research/discovering-cryptographic-weaknesses) | [@AnthropicAI](https://x.com/AnthropicAI/status/2082153309553463600)｜[CryptanalysisBench 基准](https://arxiv.org/abs/2607.18538)

**Kimi团队开源PerceptionBench，从前沿模型失败中拆解多模态大模型的原子视觉感知**
- Moonshot AI 旗下 Kimi 团队发布并开源 PerceptionBench，专门评测多模态大模型（MLLM）的视觉感知。该 benchmark 从 **42个现有 benchmark** 的前沿模型错误中回溯归纳出 **10类原子感知能力**（视觉关系、计数、属性、深度与3D、定位、比较、细粒度识别、上下文整合、OCR、幻觉），构造 **3000道验证题**（取自 **17000+** 内部题库，**60%拆解自真实模型失败**），每题只测一种能力、仅需“看”即可作答，以剥离推理与外部知识。团队在 **16个前沿 MLLM** 上评测，**无一达到60%准确率**，感知相关幻觉是平均最薄弱环节；总分几乎相同的模型在实际感知内容上可能出现剧烈分化。
  > 💡 方法论亮点是“失败驱动分类”——评测维度由模型真实失败归纳而非预设，诊断更可解释；“总分相近但感知分化”提示当前主流 MLLM 评测常将感知与推理耦合计分，可能系统性掩盖感知层短板。
   - 来源: [Kimi Blog](https://www.kimi.com/blog/perception-bench) | [@Kimi_Moonshot](https://x.com/Kimi_Moonshot/status/2081813202514681878)

**EvoCode-Bench用多轮迭代任务评测代码智能体，揭示单轮基准高估可靠性**
- 该基准含 **26个有状态编码任务、共227个评测轮次**（每任务5-15轮），要求智能体在持久工作区中维护代码、应对不断变化甚至冲突的需求；评测采用累积可执行测试与两个指标——多轮失败即止得分 **MT@4** 和单轮得分 **SR**。对 **13个代码智能体** 的测试显示，多数智能体 SR 比 MT@4 高出 **22-40分**且排名因此重排：单轮最高的 **Opus-4.6（SR 78.9）在 MT@4 仅排第三（44.0）**；最强智能体多轮成功率仍仅约 **50%**。失败模式呈分层特征：弱智能体早期即失败，强智能体则因回归与需求追踪问题在后期崩盘。
  > 💡 单轮基准系统性高估了代码智能体的可靠性——生产级瓶颈不在单任务正确性，而在需求迭代中管理回归与规范追踪的能力；MT@4 与 SR 间 22-40 分的鸿沟说明“一次给需求、一次评测”的旧范式已无法区分真正可长期协作的智能体。
   - 来源: [arXiv](https://arxiv.org/abs/2605.24110) | [@_philschmid](https://x.com/_philschmid/status/2081744861829414977)

**Mark Zuckerberg在WSJ撰文，主张超级智能应广泛可及而非由少数公司集中掌控**
- Meta CEO Mark Zuckerberg 于7月28日在《华尔街日报》发表评论《The AI Future Is for Everyone》，核心论点为：“这个时代的决定性问题不是超级智能是否会出现，而是**谁将拥有访问权**——它会被少数公司集中控制，还是广泛可及、赋能所有人。”Zuckerberg 在 X/Facebook 推广时称“我们相信未来属于每一个人”，并预告将公布“关于超级智能世界的积极愿景”。该文是其近期“AI 乐观主义”campaign 的旗舰动作，以“赋能”叙事对冲 AI 末日论；Meta 首席 AI 科学家 Yann LeCun 转发支持。
  > 💡 Zuckerberg 将“超级智能访问权”重新框定为集中 vs. 开放的价值选择，本质是为 Meta 开源/Llama 路线争取舆论与政策正当性，与 OpenAI、Anthropic 的相对封闭定位形成叙事对冲。
   - 来源: [WSJ](https://www.wsj.com/opinion/the-ai-future-is-for-everyone-a0c24e20) | [@finkd](https://x.com/finkd/status/2082160210399948869)

**1134名前沿AI公司员工跨实验室联署《Pacing the Frontier》，请求政府调节自动化AI研发节奏**
- 该声明于2026年7月发布，由 **1134名**前沿AI公司员工联署，签名涵盖 Anthropic CEO Dario Amodei、OpenAI 首席科学家 Jakub Pachocki、Thinking Machines 首席科学家 John Schulman、Meta AI 首席科学家 Shengjia Zhao等，组织支持来自两家独立非营利机构 Guidelight AI Standards 与 Encode AI。核心诉求是请求美国政府支持一项国际 effort，开发能在必要时“主动放慢自动化AI研发节奏（deliberately pace the frontier）”的技术与治理工具，理由是各公司自认已接近“自动化AI研究”，而单方面减速的竞争压力使自发协调难以成立。John Schulman 表示该声明有助于建立“关于协调机制可能需要的共同认知”；OpenAI 的 Leo Gao 则将其类比为“通向智能爆炸的致命竞赛”。声明注明所有个人评论仅代表个人立场，不代表所属公司观点。尽管如此，OpenAI 和 Anthropic 已经在华盛顿围绕AI监管形成了共同行动。随着特朗普政府计划在8月1日前敲定“前沿模型”监管评估框架，两家公司正就共享议程低调游说：要求Meta、xAI等竞争对手也必须遵守政府模型审查，并对中国开源模型发出警示。双方讨论了由政府和行业共同制定评估方法，用以判断模型是否因网络安全等能力而需要扩展审查。
  > 💡 这是 OpenAI、Anthropic、Google DeepMind、Meta 四大竞争实验室在员工层面罕见地就“放慢节奏”达成四位数规模共识，本身就印证了前沿实验室内部对“自动化AI研究/近递归式自我改进”临近的判断。诉求明确指向政府与国际治理机制而非自愿承诺，标志着AI安全议程从“实验室自律”向“外部节奏管理”的范式位移。
   - 来源: [Pacing the Frontier](https://www.pacingthefrontier.com/) | [@AnthropicAI](https://x.com/AnthropicAI/status/2082228994653696371) | [The Information](https://www.theinformation.com/articles/openai-anthropic-quietly-teaming-washington)

---
*更新时间: 2026-07-29 10:34*