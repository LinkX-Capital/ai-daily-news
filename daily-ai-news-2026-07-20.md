## 07月20日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：阿里通义千问Qwen3.8即将开源，参数规模达2.4万亿；OpenBMB开源MiniCPM-Robot具身模型家族，1.5B通用VLA在多项基准超越π0.5等更大模型
- 产业动态：黄仁勋访日推进物理AI，日本组建Noetra主权AI与Cosmos机器人联盟、五年投入62亿美元
- 初创&融资：Netflix以5.87亿美元现金收购Ben Affleck联合创办的AI影视公司InterPositive
- 研究关注：REAL：上海AI实验室InternRobotics开源具身智能框架，真实双臂机器人端到端成功率78.3%; VideoChat3：南京大学联合上海AI实验室开源4B视频多模态模型，以更高效率超越更大参数开源模型; SearchOS：人民大学提出多智能体开放域搜索框架，将搜索进度外化为共享状态并全面领先WideSearch/GISA; LOTAPO：基于留一回合归因的自生成过程奖励方法，多轮搜索推理平均EM达0.326
- X讨论：Schema：不改模型权重的推理框架，使Claude Opus 4.8+Fable 5在ARC-AGI-3公开集自报98.98%; Nathan Lambert走访中国AI实验室，归纳fast-follow文化与开发者Claude依赖

---

## 📖 详细参考

### 模型前沿
**阿里通义千问Qwen3.8即将开源，参数规模达2.4万亿**
- 阿里通义千问宣布Qwen3.8即将上线，将以开源权重形式发布，模型参数规模达**2.4万亿**。
  > 💡 2.4T参数级别直接对标Meta Llama 4 Behemoth等超大模型竞品，阿里选择在开源权重路线上继续加大投入，意味着头部开源阵营的规模军备竞赛仍在加速。
   - 来源: [@alibaba_qwen](https://x.com/Alibaba_Qwen/status/2078759124914098291#m)

**MiniCPM-Robot：OpenBMB开源具身智能模型家族，1.5B通用VLA在多项基准超越π0.5、Qwen-VLA等更大模型**
- OpenBMB（面壁智能）开源MiniCPM首个具身智能模型家族MiniCPM-Robot，包含通用机器人操作模型MiniCPM-RobotManip与具身目标跟踪模型MiniCPM-RobotTrack。RobotManip为**1.5B**参数的通用VLA，单套权重覆盖全部下游任务，在LIBERO、RoboTwin2、RMBench等代表性评测上以更小体量超过π0.5（3B）、Qwen-VLA（5B+）等更大模型；借助流式推理与继承自MiniCPM-V 4.6的视觉token压缩（每帧256→64），支持最长1分钟视觉上下文记忆且在线成本接近单帧反应式推理。RobotTrack为**0.9B**的全本地具身目标跟踪模型，官方称其为首个完全端侧的具身跟踪器，在EVT-Bench上为开源SOTA，在Unitree Go2 EDU上以纯视觉本地运行达**5+ FPS（约180ms）**。
  > 💡 1.5B通用VLA在多项操作基准上反超3B~5B+模型，配合0.9B纯端侧跟踪器，显示具身大模型正沿"小参数+高效率+端侧部署"路线快速逼近乃至超越大参数方案，对机器人本体厂商的算力与成本门槛是直接利好。
   - 来源: [GitHub](https://github.com/OpenBMB/MiniCPM-Robot) | [@OpenBMB](https://x.com/OpenBMB/status/2078839529591759025)

### 产业动态
**黄仁勋访日推进物理AI：日本组建Noetra主权AI与Cosmos机器人联盟，五年投入62亿美元**
- TechCrunch报道，NVIDIA CEO黄仁勋7月15-16日访问东京，与日本政商界敲定一系列覆盖AI算力、机器人与芯片供应链的合作。主权AI方面，日本政府牵头约44家本土企业（SoftBank、Sony、NEC、Honda等为核心）组建Noetra，建设自主"物理AI"基础模型，东京承诺五年内投入最高**1万亿日元（约62亿美元）**；NVIDIA将为其建设"Vera Rubin AI工厂"数据中心，计划2028年投运，配备**1.375万颗Vera CPU与2.75万颗Rubin GPU**、规模140MW。机器人方面，Fanuc、Yaskawa、川崎重工、Fujitsu、Hitachi、Sony、SoftBank、Kubota及AIRoA等宣布基于NVIDIA Cosmos模型构建应用，NVIDIA同步发布可运行于Jetson Thor芯片的**Cosmos 3 Edge**版本。丰田则将合作延伸至制造仿真、车载软件与交通感知系统。日本AI机器人战略目标是2040年前在18个行业部署**1000万台**AI机器人，公共与私人物理AI投资规模达**650亿美元**。
  > 💡 日本以"主权AI+物理AI"为框架，把国家级算力工厂、Cosmos机器人联盟与制造业数据捆绑在一起，本质是用美国芯片换本土物理AI主权——对NVIDIA是锁定下一个万亿级产业场景，对日本是对冲中美AI差距的产业政策押注。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/19/what-to-watch-for-after-jensen-huangs-japan-visit/)

### 初创&融资
**Netflix以5.87亿美元现金收购Ben Affleck联合创办的AI影视公司InterPositive**
- Netflix最新监管文件披露，其以**5.87亿美元全现金**收购AI影视制作初创InterPositive（Bloomberg此前估值最高6亿美元），该公司由演员兼导演Ben Affleck联合创办，Affleck将作为高级顾问加入、原团队整体并入。InterPositive的AI工具用于后期制作，帮电影人弥补漏拍、背景替换、灯光失误等实拍难题；Netflix最新财报披露已有约**300部**自家作品使用了生成式AI。
  > 💡 Netflix愿意为一家AI影视初创付出近6亿美元现金，表明头部流媒体已将生成式AI视为影视制作降本提效的核心基础设施，相关资产估值正在快速重估。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/19/netflix-paid-587m-for-ben-afflecks-ai-filmmaking-startup/)

### 研究关注
**REAL：上海AI实验室InternRobotics开源具身智能框架，真实双臂机器人端到端成功率78.3%**
- 上海人工智能实验室InternRobotics团队提出REAL，一个面向开放世界移动操作的具身智能体框架，不依赖仿真器特权状态，仅从原始RGB观测进行视觉探索，并通过模拟用户完成人在环的意图澄清。团队构建了覆盖主动探索、视觉干扰、铰接操作、交互澄清四类任务的REAL-Bench基准，共**241个任务**，并采用分层SFT与在线RL的训练管线。在交互任务上，训练后的智能体以**56.9%成功率**超过主流商用闭源VLM；在物理双臂移动机器人上完成60轮真实世界测试，端到端成功率**78.3%**，并展现对未见家庭场景的零样本迁移能力。该工作已被**ECCV 2026**收录，代码与241任务基准已开源。
  > 💡 REAL用不依赖特权感知的纯视觉方案在真实机器人上拿到78.3%端到端成功率并开源241任务基准，为VLA/具身智能的sim-to-real与可复现评测提供了具体落点，也呼应了行业对具身智能拐点临近的预期。
   - 来源: [arXiv](https://arxiv.org/abs/2607.13653) | [GitHub](https://github.com/InternRobotics/REAL)

**VideoChat3：南京大学联合上海AI实验室开源4B视频多模态模型，以更高效率超越更大参数开源模型**
- 南京大学王利民团队联合上海人工智能实验室、南洋理工大学等提出VideoChat3，一个完全开源、高效、通用的视频多模态大模型。效率侧引入I3D-ViT（膨胀3D视觉Transformer）与面向流式视频感知的自适应帧分辨率策略，降低训练与推理的视频处理成本；效果侧构建可扩展视频数据合成管线，产出Academic2M、LV116K、OL617K三套分别覆盖通用、长视频、流式场景的高质量数据集。在通用、长视频、流式三类基准上，VideoChat3仅以**4B参数**和更高效率超越同等或更大参数的既有开源模型，并完整开放训练代码、策略与数据。
  > 💡 在多数开源视频MLLM仅部分开放（训练代码/数据缺失）的背景下，VideoChat3的完全开源（代码+策略+三套数据集）加上4B即超越更大模型，对视频理解的可复现研究与端侧/高效部署有直接价值。
   - 来源: [arXiv](https://arxiv.org/abs/2607.14935) | [HuggingFace](https://huggingface.co/papers/2607.14935)

**SearchOS：人民大学提出多智能体开放域搜索框架，将搜索进度外化为共享状态并全面领先WideSearch/GISA**
- 中国人民大学高瓴人工智能学院窦志成、文继荣团队提出SearchOS，一个系统级多智能体框架，针对工具增强LLM信息检索Agent在交互历史增长后陷入重复循环、浪费搜索预算的问题。SearchOS将开放域信息检索建模为带溯源引用的关系模式补全（实体-属性-链接表），并通过搜索导向上下文管理SOCM把演化状态外化为前沿任务、证据图、覆盖图与失败记忆四类持久共享结构；配合流水线并行调度与搜索工具中间件Harness，避免重复失败搜索模式。在WideSearch和GISA基准上，SearchOS在评估的全部单/多智能体基线中所有指标领先。
  > 💡 把Agent搜索过程中易丢失的隐式进度显式外化为可共享的持久状态（证据图/覆盖图/失败记忆），是从"单次检索"走向"长程、鲁棒信息搜集Agent"的关键工程方向，对Deep Research类产品的稳定性有直接参考价值。
   - 来源: [arXiv](https://arxiv.org/abs/2607.15257) | [HuggingFace](https://huggingface.co/papers/2607.15257)

**LOTAPO：基于留一回合归因的自生成过程奖励方法，多轮搜索推理平均EM达0.326**
- 针对多轮搜索推理强化学习只能依赖终局奖励、无法区分有用/冗余/有害中间交互的问题，LOTAPO提出一种基于反向留一回合归因的自生成过程监督方法：对每个搜索回合，将其与检索观测替换为固定[DELETE]占位符，测量当前策略对金标准答案平均对数似然的变化作为该回合贡献估计，并保留全部下游交互；再通过符号一致性门控只保留方向一致的归因。该方法无需额外奖励模型、教师、验证器或LLM-as-Judge。在7个带本地检索的知识密集型问答数据集上，LOTAPO平均精确匹配（EM）达**0.326**，较最强步级奖励基线IGPO高**0.053**。
  > 💡 LOTAPO用策略自身的似然变化来"回溯打分"每一轮搜索交互，绕开了训练额外过程奖励模型的开销，为多轮搜索/Agent的RL提供了更细粒度、低成本的过程监督信号。
   - 来源: [arXiv](https://arxiv.org/abs/2607.13501)

### X讨论
**Schema：不改模型权重的推理框架，使Claude Opus 4.8+Fable 5在ARC-AGI-3公开集自报98.98%**
- Impossible Research团队（作者包括Angjoo Kanazawa、Andrea Zanette、Haiwen Feng等）提出Schema，一个不修改底层模型权重、而是重构模型使用流程的推理框架，在ARC-AGI-3公开集上自报**98.98%**（Claude Opus 4.8 + Fable 5配对）与**95.35%**（GPT-5.6 Sol）。ARC-AGI-3只给智能体64×64彩色网格与合法动作集合，不提供物体清单、规则、目标或奖励，官方指标RHAE对比人类首次通关动作数。Schema将潜在世界表示建模为可读、可验证、可搜索的可编辑程序，把"状态接地"（从原始观测发明物体/变量/关系）与"机制发现"（写出可执行的step()转移规则）两个问题联合求解：当观测与预测矛盾时，智能体可修订状态表示或转移规则中的任一层。在固定Opus+Fable配对的对照实验中，Schema相比Claude Code基线的42.83%提升至98.98%（+56.15个百分点）。需要说明的是，上述成绩均为**公开集自报结果、尚未经ARC Prize独立验证**，而GPT-5.6 Sol在更具区分度的Semi-private集官方仅7.78%，公开集近满分能映射到Semi-private多少仍未知。
  > 💡 ARC-AGI-3从3月发布时的0.51%到7月官方13.33%，再到Schema自报98.98%，量级跃升主要来自"怎么用模型"而非模型本身——把世界模型做成可验证、可搜索的程序而非隐式向量上下文，提示抽象推理的红利正从"堆参数"转向"推理流程工程"；但自报+公开集的成绩仍需Semi-private独立验证才能定性。
   - 来源: [项目主页](https://schema-harness.github.io/) | [@HavenFeng](https://x.com/HavenFeng/status/2077770348876247502)

**Nathan Lambert走访中国头部AI实验室：归纳fast-follow文化、开发者普遍"Claude-pilled"、渴求更多Nvidia芯片**
- AI评论人Nathan Lambert（Interconnects作者）撰文记录其走访Moonshot（Kimi）、智谱Z.ai、美团、小米、通义千问、蚂蚁、零一万物等中国头部AI实验室的见闻。他认为中国实验室在文化上天然适配**fast-follow**——愿意做不显眼的精细工作、自我意识更少、学生作为同级深度参与（类似Ai2，区别于OpenAI/Anthropic/Cursor基本不招实习生）。行业层面他归纳：中国企业端AI付费或更接近云市场而非历史上较小的SaaS市场；多数开发者**"Claude-pilled"**、重度使用Claude而较少提Codex；美团、小米、蚂蚁等非典型厂商自研通用大模型以掌控技术栈，开源更多出于实用主义；数据产业较不成熟、倾向自建RL环境；各实验室普遍**渴求更多Nvidia芯片**用于训练、华为等国产加速器多用于推理。格局上，各实验室普遍忌惮字节跳动（豆包，国内唯一前沿闭源实验室），并尊重DeepSeek的研究品味。
  > 💡 Lambert的走访提供了一个相对平衡的"内部视角"：中国AI的竞争力被归因于工程文化（精细、低自我、学生深度参与）与"掌控技术栈"的实用主义，而非单纯举国体制或复制；其中"开发者对Claude的统治级依赖"和"Nvidia训练芯片的稀缺性"是两个对中美AI格局可操作的判断。
   - 来源: [Interconnects](https://www.interconnects.ai/p/notes-from-inside-chinas-ai-labs) | [@natolambert](https://x.com/natolambert/status/2052415630062879098)

---
*更新时间: 2026-07-20 06:50*
