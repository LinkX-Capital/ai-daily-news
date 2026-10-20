## 10月20日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 15 条

---

## 要点汇总

- 模型前沿：MiniMax 发布 M3.1 Flash：兼顾空间能力与快速推理; Inception AI 推出 Mercury 3：扩散模型支持 1M 上下文，上线即降半价; OpenAI 公布最新模型进展，主打 COBOL、Fortran 等小语种代码的构建与迁移能力
- 产业动态：MiniMax 在 OpenRouter 上线 M3.1 Flash 正式版，免费开放 72 小时; Agility Robotics 宣布前 UPS 总裁 Mark Vale 将在与 Churchill Capital XI 合并完成后加入董事会
- 算力追踪：SemiAnalysis：英伟达 GB300 FP4 单位成本性能落后 TPUv7; SemiAnalysis：2027 年数据中心单年增量或达 50GW，在建规模达 60GW; Meta：Prometheus 万卡级超集群支撑 Muse 基础模型训练
- 研究关注：EvoSkill v2：把指令改写做成有状态单智能体，SpreadsheetBench v2 通过率领先 SkillOpt 与 SkillBoost 7.7 个百分点; Maestro 以全局协调处理 Lean 证明失败：PutnamBench 解出 669/672，arXivLean 自证 34/48; PSSE：用条件状态空间探索缓解多轮强化学习无效动作与循环陷阱
- X讨论：DeepSeek 上线 V4.1 Flash 1017 更新，AA 智能指数 45 分位列开源权重并列第二; fal 发布 FLUX 3 Max：FLUX 3 后训练版，AA 视频图生视频榜并列第一、文生视频榜第四; Cognition 发布 Devin Fusion：拿 AA 编码智能体指数 68 分，单任务成本较 Claude Code 低 31%; Agility Robotics 联合创始人解释 Digit 5 无法运行的原因

---

## 📖 详细参考

### 模型前沿
**MiniMax 发布 M3.1 Flash：兼顾空间能力与快速推理**
- MiniMax 发布 M3.1 Flash，并将 Space Bunny 称为该模型的早期版本。MiniMax 称 Space Bunny 曾以超过 200T tokens 的规模登顶全球榜单。M3.1 Flash 在 Automation-Bench、ALE、DeepSWE 和 BabyVision 上分别取得 62%、30%、74% 和 91% 的结果。
  > 💡 M3.1 Flash 将智能、编码与视觉推理能力集中到快速推理模型中，但相关成绩来自厂商披露。
   - 来源: [@minimax_ai](https://x.com/MiniMax_AI/status/2112150867868541221)

**Inception AI 推出 Mercury 3：扩散模型支持 1M 上下文，上线即降半价**
- OpenRouter 上线 Inception AI 的 Mercury 3 扩散模型，支持 1M 上下文，生成速度超过 1,000 tokens/s。Inception 表示，该速度是 Mercury 2.5 的 4 倍，并在 IFBench、GPQA Diamond 和 SWE-Bench Atlas 上超过 GPT-6 Luna 与 Haiku 5.5。上线期间价格为每百万输入 tokens 0.10 美元、每百万输出 tokens 0.35 美元，优惠幅度为 50%。
  > 💡 Mercury 3 将高速生成、百万级上下文与 OpenRouter 的渠道分发结合，但领先结论仍需结合第三方实测审视。
   - 来源: [@openrouter](https://x.com/OpenRouter/status/2112225779782398131)

**OpenAI 公布最新模型进展，主打 COBOL、Fortran 等小语种代码的构建与迁移能力**
- OpenAI 在官方账号宣布，最新模型进展将强化 COBOL、Fortran 与 Visual Basic 等低资源编程语言上的代码构建与迁移能力。这些语言支撑着银行、政府与企业长期依赖的业务系统，进展意味着模型需要理解数十年沉淀的业务逻辑，并在保留原有功能的前提下协助开发者完成现代化改造。OpenAI 表示将继续围绕该方向投入相关能力建设。
  > 💡 把 COBOL、Fortran 这类承载关键基础设施但被新生态边缘化的语言列为改进方向，意味着 OpenAI 在意的不只是开发者圈层的基准名次，更在押注企业级遗留系统改造这块高粘性、强付费意愿的市场。
   - 来源: [@openai](https://x.com/OpenAI/status/2112310345863930168)

### 产业动态
**MiniMax 在 OpenRouter 上线 M3.1 Flash 正式版，免费开放 72 小时**
- MiniMax 发布 M3.1 Flash 正式版本，并在 OpenRouter 平台免费开放 72 小时。官方账号透露在 M3.1 正式版之前曾经有过一个被开发者连续十天上榜到第一的早期版本，并戏称 OpenRouter 为其保守了秘密。
  > 💡 用 72 小时免费窗口跟进此前的早期试用热度，是把开发者社区的尝鲜流量转化为正式版第一波使用数据的标准动作；限时免费的强度决定了其能否在 OpenRouter 与 Hugging Face 等聚合渠道上跑出口碑。
   - 来源: [@minimax_ai](https://x.com/MiniMax_AI/status/2112287025361801272)

**Agility Robotics 宣布前 UPS 总裁 Mark Vale 将在与 Churchill Capital XI 合并完成后加入董事会**
- Agility Robotics 在社交平台宣布，前 UPS 总裁 Mark Vale 预计将在公司 与 Churchill Capital Corp XI（NASDAQ: CCXI）合并完成后加入董事会，并担任审计委员会主席一职。公告中提供了相关链接以供查阅更多细节。
  > 💡 在 SPAC 合并的关键节点引入具有大型上市公司运营背景的高管出任审计委员会主席，体现出 Agility Robotics 为公开市场合规与公司治理标准做准备的动作；这也是其商业化进入资本市场的常规前置安排。
   - 来源: [@agilityrobotics](https://x.com/agilityrobotics/status/2112140452531220643)

### 算力追踪
**SemiAnalysis：英伟达 GB300 FP4 单位成本性能落后 TPUv7**
- SemiAnalysis 表示，上周 TPUv7 FP8 提交结果展现出更优的每美元性能后，英伟达已投入额外时间应对竞争。英伟达提交的 GB300 FP4 首次对比结果在多数端到端性能区间内，面向外部客户的每美元性能仍比 TPUv7 低 1.64 倍。
  > 💡 该对比显示，AI 基础设施竞争除峰值算力外，单位成本性能和外部客户可用性已成为关键衡量维度。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2112258243372146742)

**SemiAnalysis：2027 年数据中心单年增量或达 50GW，在建规模达 60GW**
- SemiAnalysis 将 2027 年称为数据中心加速之年，预计该年将新增 50GW 容量。当前处于建设阶段的数据中心规模达到 60GW，年初至今已签署 1.3T 的租赁合同。该机构认为，短缺压力可能进一步传导至芯片。
  > 💡 数据中心建设与长期租赁合同同步扩张，意味着算力需求仍在增长，但新增容量也可能把供应瓶颈推向芯片环节。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2112069964131713517)

**Meta：Prometheus 万卡级超集群支撑 Muse 基础模型训练**
- Meta 表示，Muse 基础模型均在俄亥俄州 New Albany 的 Prometheus 超集群上训练，其中包括 Muse Wonder。Prometheus 由数十万块 GPU 构成，Meta 称其预训练 goodput 超过 85%，强化学习 goodput 超过 90%，平均故障时间为约 47K GPU 小时。
  > 💡 超大规模训练的关键不只是 GPU 数量，Meta 将重点放在降低单个故障主机对整体训练进度的影响。
   - 来源: [@aiatmeta](https://x.com/AIatMeta/status/2112245968750145561)

### 研究关注
**EvoSkill v2：把指令改写做成有状态单智能体，SpreadsheetBench v2 通过率领先 SkillOpt 与 SkillBoost 7.7 个百分点**
- 论文提出 EvoSkill v2，把智能体优化「指令（skills）」的过程拆成三智能体系统：用户在运行时描述基准并提供评分器，由基准适配器生成基准插件，求解器完成任务，进化器读取求解器训练 rollout 后在每个 epoch 改写指令。论文将进化器实现为带 bash 工具的有状态编码智能体，而非 SkillOpt 的多次单次模型调用或 SkillBoost 每轮重新启动智能体的常见设计。论文同时测量求解器 rollout 的逐次波动、为每个训练任务提供多次尝试，并接受每个 epoch 改写出的全部指令而非按噪声分数筛选。在 SpreadsheetBench v2 与 τ³-bench 银行两个基准、两种反馈设置下，EvoSkill v2 改写后的指令将留出测试通过率较 SkillOpt 与 SkillBoost 中较强基线分别提升 7.7 与 5.4 个百分点，且每提升一个百分点通过率的进化器成本低于两个基线优化器。在 τ³-bench 银行实验里，由 Claude Haiku 5.5 同时驱动求解器与进化器时仍可获得最高 21.5 个百分点的提升。
  > 💡 EvoSkill v2 的真正区别不在三智能体框架，而在把「进化器」从一次性脚本改写为带工具的有状态智能体：保留历史 rollout、接受噪声、对每次任务允许多次尝试，三件事一起做才能让小模型也能编辑自己的指令。这条技术路径的产业意义是：指令/系统提示调优不必依赖更大模型自审，用一台带 bash 的小模型长期维护即可逐步逼近更强基线，对成本敏感的部署方是直接利好。
   - 来源: [arXiv cs.LG](https://arxiv.org/abs/2610.25931v1)

**Maestro 以全局协调处理 Lean 证明失败：PutnamBench 解出 669/672，arXivLean 自证 34/48**
- 论文提出面向 Lean 的证明器框架 Maestro，让各个证明器报告失败原因，并由可查看完整证明过程的协调器选择引导、修正错误引理、撤回错误子树或重新规划等响应。该框架也扩展到经过验证的代码生成，代码经检查发现反例后会返回修复。论文使用四个前沿 LLM，在七项数学和三项软件验证基准上开展评测；在代理尚未饱和的每项基准上，Maestro 证明的目标数均超过 Claude Code 或 Codex 原生代理，其中 Claude Opus 5 在 2026 年 6 月版 arXivLean 中自行证明了 48 个定理中的 34 个，原生代理为 19 个。Maestro 还超过所有共同覆盖的已发表证明器系统，取得 PutnamBench 669/672、Lean-IMO-Bench 59/60 和 IMO 2026 6/6 的结果。
  > 💡 Maestro 的关键价值不是单纯增加分解层级，而是让失败反馈进入全局规划，避免系统沿错误证明方向持续消耗预算；其结果也显示，针对形式化证明的代理能力不能只由底层模型衡量。
   - 来源: [arXiv cs.LG](https://arxiv.org/abs/2610.25920v1)

**PSSE：用条件状态空间探索缓解多轮强化学习无效动作与循环陷阱**
- 论文指出，大语言模型智能体在多轮、长周期环境的强化学习中常陷入高置信但低产出行为，反复执行无效动作或进入动作循环，进而违反环境前置条件，暴露出智能体内部状态表征与底层环境动态之间的失配。论文提出一种条件状态空间探索框架，通过引入惩罚观察与历史状态记忆重复的内禀奖励，在不依赖通用信息论度量的前提下抑制冗余行为并鼓励状态空间覆盖。在多轮环境中的结果显示，该方法在策略学习上取得明显提升，并能缓解无效动作与重复循环问题。
  > 💡 该工作把多轮 RL 中的循环陷阱归因于状态表征与环境的失配，并通过去重式内禀奖励直接施压而非增加信息论开销，对长周期智能体训练的实用价值较高；但摘要未给出具体基准名称与提升幅度，需结合原文进一步核验。
   - 来源: [arXiv cs.LG](https://arxiv.org/abs/2610.25957v1)

### X讨论
**DeepSeek 上线 V4.1 Flash 1017 更新，AA 智能指数 45 分位列开源权重并列第二**
- DeepSeek 发布 V4.1 Flash 1017，是旗舰模型 V4.1 Flash 的迭代版本。在 Artificial Analysis 智能指数上，该版本拿到 45 分，比上一版 V4.1 Flash 提高 6 分，并列开源权重模型第二名。官方 API 方面，V4.1 Flash 1017 每百万输入 token 定价 0.30 美元、每百万输出 token 定价 1.20 美元。
  > 💡 作为非旗舰的小版本更新，6 分的智能指数涨幅与对标并列开源第二的排位，显示出 DeepSeek 在轻量档位上仍有明确的分数提升空间，开源权重阵营的位次竞争也由此进一步加剧。
   - 来源: [@artificialanlys](https://x.com/ArtificialAnlys/status/2112218661432000694)

**fal 发布 FLUX 3 Max：FLUX 3 后训练版，AA 视频图生视频榜并列第一、文生视频榜第四**
- fal 发布 FLUX 3 Max，作为 Black Forest Labs FLUX 3 的后训练版本。在 Artificial Analysis 评测中，FLUX 3 Max 在 AA-Video-I2V v1.1 榜单上位列第二（与第一统计学意义上并列），在 AA-Video-T2V v2.1 榜单上位列第四，均高于基础版 FLUX 3。该模型可由文本提示词或起始图像生成长度 5 到 20 秒、720p 分辨率并带原生音轨的视频，fal 宣称 10 秒视频生成耗时低于 12 秒。
  > 💡 第三方在开源基底上做后训练就能在一图/文生视频榜单挤进前两名，说明视频生成赛道的产品-模型分工开始清晰化：基础模型提供能力上限，后训练服务厂商则在细分榜单与生成速度上做差异化变现。
   - 来源: [@artificialanlys](https://x.com/ArtificialAnlys/status/2112266414593827110)

**Cognition 发布 Devin Fusion：拿 AA 编码智能体指数 68 分，单任务成本较 Claude Code 低 31%**
- Cognition 推出 Devin Fusion，在 Artificial Analysis 编码智能体指数上以 68 分拿下榜首。系统采用 Opus 5.5 担任主模型，GPT-6 Luna 担任辅助角色。Cognition 表示，Devin Fusion 在同跑 Opus 5.5 的条件下，性能与价格均优于 Claude Code，在达成 68 分的同时单任务成本较后者低 31%。
  > 💡 用双模型分工组合（前沿旗舰做主、较新一代做副）跑出更低的单任务成本，体现了编码智能体的竞争已经从单模型榜单过渡到「调度 + 模型组合」阶段；这也使得同一基座在不同 agent 产品中的相对优势，会更多被工程编排放大或抵消。
   - 来源: [@cognition](https://x.com/cognition/status/2112290148205436979)

**Agility Robotics 联合创始人解释 Digit 5 无法运行的原因**
- Agility Robotics 在 X 平台表示，其联合创始人 Jonathan Hurst 探讨了 Digit 5 无法运行的原因。相关内容由 IEEE Spectrum 刊载，Agility Robotics 官方账号随后分享了该链接，并标注 Digit 5。
  > 💡 现有信息仅说明 Agility Robotics 分享了联合创始人对 Digit 5 运行问题的解读，尚未披露具体技术原因或改进方案。
   - 来源: [@agilityrobotics](https://x.com/agilityrobotics/status/2112286284236640320)


---
*更新时间: 2026-10-20 11:12*