## 07月07日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：Hy3正式发布：Hunyuan团队半年内从Hy2迭代至Hy3，推理与Agent能力大幅跃升
- 产业动态：AI招聘平台Mercor年化毛收入突破20亿美元，较年初翻倍; Google调整隐私设置默认允许将用户数据用于AI训练; Reddit以LLM对抗LLM垃圾内容，2026 Q1用户垃圾曝光下降20%; Microsoft裁员4800人，Xbox部门1600人卷入重组，管理层级从14层压缩至3-5层
- 算力追踪：Anthropic与TeraWulf签署190亿美元算力租赁协议，后者股价大涨
- 初创&融资：前苹果团队创立的智能眼镜公司Even Realities以10亿美元估值完成$150M融资（美团、腾讯领投）
- 研究关注：Anthropic团队发现LLM中存在类"全局工作空间"的J-space表征，并与Dehaene团队合作完成外部评述; Sakana AI Sheaf-ADMM框架，多Agent分布式协调在Sudoku任务中达93%求解率; MIPU：腾讯/中科院等团队提出面向LLM RL的"推理侧单调策略提升"目标; PMD：跨episode"程序性记忆蒸馏"让LLM在RLVR训练中持续自改进; Embodied.cpp：跨异构机器人的统一C++推理运行时，VLA模型闭环任务成功率最高100%
- X讨论：Google DeepMind与Apptronik扩大人形机器人研究合作，Apollo 2平台将贡献真实世界数据; Anthropic 发布"The Making of Claude Code"幕后故事专题; 腾讯混元向vLLM贡献HPC-Ops高性能Attention与MoE推理后端

---

## 📖 详细参考

### 模型前沿
**Hy3正式发布：Hunyuan团队半年内从Hy2迭代至Hy3，推理与Agent能力大幅跃升**
- 腾讯混元（Hunyuan）团队在不到半年时间内完成Hy2 → Hy3 preview → Hy3的快速迭代。**Hy3 为 295B 总参 / 21B 激活 MoE 模型，含 3.8B MTP 层参数**，80 层 Transformer + 1 层 MTP，192 专家（top-8 激活），**上下文 256K**。内部 270 名专家盲评中，Hy3 在前端开发、数据存储、CI/CD 等生产力任务上得分 **2.67/4**，超过 GLM-5.1（2.51/4）。抗幻觉方面，**幻觉率从 12.5% 降至 5.4%**，常识错误率从 25.4% 降至 12.7%；多轮指令继承问题的失败率从 17.4% 降至 7.9%。Hy3 与 **Hy3-FP8** 量化版本同步开源（Apache 2.0），可通过 vLLM 与 SGLang 部署（推荐 H20-3e 等大显存 GPU × 8）。
  > 💡 混元以半年为周期迭代基础模型，重点强化推理与抗幻觉，反映国产大模型在Agent赛道的加速追赶；21B激活对标一线小尺寸MoE，配合vLLM/SGLang原生支持降低企业部署门槛。
   - 来源: [@shunyuyao12](https://x.com/ShunyuYao12/status/2074151389945827744#m) | [HuggingFace Model Card](https://huggingface.co/tencent/Hy3)

### 产业动态
**AI招聘平台Mercor年化毛收入突破20亿美元，较年初翻倍**
- 据The Information援引知情人士，AI招聘平台Mercor在6月年化毛收入跑率超过20亿美元，较今年早些时候翻倍。增长动力来自**AI 应用开发者**与**财富500强企业**两类客户——前者用 Mercor 招聘训练/微调模型所需的数据与技术人才，后者借此搭建自有 AI 模型。Mercor 创立三年，向全球签约工程师与标注人员按项目付费。
  > 💡 Mercor增长印证AI Recruiting赛道商业化跑通，垂直Agent类工具可快速突破传统招聘SaaS的天花板。
   - 来源: [The Information](https://www.theinformation.com/briefings/exclusive-mercor-hit-2-billion-gross-annualized-revenue)

**Google调整隐私设置默认允许将用户数据用于AI训练**
- Google近期更新隐私设置，允许公司将更多用户数据（包括媒体内容）用于AI训练。用户在Google账号设置中可手动关闭相关选项以退出数据共享。此次变更意味着默认状态下Google账户持有人的搜索记录、应用活动及部分媒体内容将进入AI训练数据流。
  > 💡 Google在用户隐私与AI训练数据需求之间倾向后者，用户需主动操作才能拒绝，监管和舆论压力可能随之上升。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/06/if-you-use-google-youre-training-its-ai-heres-how-to-opt-out/)

**Reddit以LLM对抗LLM垃圾内容，2026 Q1用户垃圾曝光下降20%**
- Reddit公布其反垃圾系统升级细节：每日拦截**2300万次**垃圾浏览、新增**25,000**条垃圾帖/评论的拦截。Reddit通过LLM识别传统系统难以发现的协同造假模式，使**2026年1-3月用户垃圾曝光较上季下降20%**。
  > 💡 LLM泛滥后平台转向"用AI对抗AI"，传统规则+ML过滤器在协调造假模式前失效，行业普遍面临新一轮军备竞赛。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/06/reddit-is-using-llms-to-solve-a-problem-llms-largely-created/)

**Microsoft裁员4800人，Xbox部门1600人卷入重组，管理层级从14层压缩至3-5层**
- Microsoft宣布裁员约**4,800人**，其中**1,600人来自Xbox部门**，全部裁员将在2027财年前累计达3,200人。Xbox CEO Asha Sharma在内部备忘录中称这是"Xbox历史上最重大的重组"，承认Xbox"业务不健康、毛利比同行低3-10倍"。同时微软新成立聚焦企业AI部署的"Frontier Company"业务单元并配套**25亿美元投资**。
  > 💡 微软同时推进裁员与AI业务加码（Frontier Company + $2.5B），印证AI CapEx持续挤占传统业务预算，游戏和内容板块首当其冲。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/06/microsoft-lays-off-nearly-5000-employees-across-xbox-commercial-sales/)

### 算力追踪
**Anthropic与TeraWulf签署190亿美元算力租赁协议，后者股价大涨**
- 比特币矿企兼数据中心运营商TeraWulf宣布与Anthropic签订20年租约，提供190亿美元算力容量。消息公布后TeraWulf股价周一大涨。
  > 💡 190亿美元为近期头部AI公司单笔算力承诺的量级新高，矿企转型AI算力供应商趋势加速，Anthropic持续推进非NVIDIA自有算力布局。
   - 来源: [The Information](https://www.theinformation.com/briefings/terawulf-shares-soar-19-billion-anthropic-data-center-deal)

### 初创&融资
**前苹果团队创立的智能眼镜公司Even Realities以10亿美元估值完成1.5亿美元融资**
- 智能眼镜公司Even Realities完成**1.5亿美元** pre-Series B 融资，估值达**10亿美元**，由美团和腾讯领投。Even Realities 总部位于深圳，成立于**2023年**，由前 Apple 工程师创立（CEO Will Wang 曾负责 Apple Watch 与 iPhone），早期投资人包括红杉中国（HSG）。公司主打"显示优先"的智能眼镜——**不配摄像头**，通过镜框内置 HUD 显示信息，配合 Even R1 指环实现输入。首代产品 Even G1 于 2024 年发布，**销量突破 1 万副**（首发品类首家），团队从 30-40 人扩张至 300-400 人。核心技术为自研的 **Even HAO（Holistic Adaptive Optics）** 端到端光学方案，自研微芯片、波导与处方支持。
  > 💡 无摄像头 + 欧洲隐私标准设计避开智能眼镜最大争议点，"指环+显示"组合区别于 Meta/Ray-Ban 的"摄像头+AI"路线，腾讯+美团组合背书中国硬件出海能力。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/06/smart-glasses-maker-even-realities-hits-1b-valuation-with-150m-funding-led-by-meituan-tencent/)

### 研究关注
**Anthropic团队发现LLM中存在类"全局工作空间"的J-space表征，并与Dehaene团队合作完成外部评述**
- Anthropic 团队在 Transformer Circuits 发表论文 **"Verbalizable Representations Form a Global Workspace in Language Models"**（Jack Lindsey 团队）。研究发现 LLM 中存在与人类"全局神经工作空间"（GNW）功能相似的稀疏子空间 **J-space**（使用 Jacobian lens 工具识别），位于中间层、容量有限、约占每层方差的 <10%。**Claude Sonnet 4.5** 的 J-space 中包含模型"不愿外显"的内部思考（潜在欺骗意图、对自身诚实性的元认知等）；同时该论文邀请 **Stanislas Dehaene、Neel Nanda** 等专家独立评述，Dehaene 评述称这是 GNW 假设的"里程碑式验证"，但强调 Claude 缺乏身体、持续记忆与自发动态。Neel Nanda（Google DeepMind）在 **Qwen 3.6 27B** 上独立复现了核心结论，并在处理歧义句时发现可激活并起因果作用的"interpretative meta-tokens"（如中文"这是什么意思"对应的 token）。Anthropic 与 **Neuronpedia** 合作发布开源权重模型的可交互 demo。
  > 💡 Anthropic 把 LLM interpretability 与神经科学意识理论直接对接，J-space 既是对齐工具（识别隐性意图）也是"意识"争论的实证战场；Neel Nanda 在不同模型上的独立复现 + 跨模型泛化（meta-tokens）显著提高结论可信度。
   - 来源: [Transformer Circuits](http://transformer-circuits.pub/2026/workspace/index.html) | [External Commentary PDF](https://www-cdn.anthropic.com/files/4zrzovbb/website/cc4be2488d65e54a6ed06492f8968398ddc18ebe.pdf) | [@AnthropicAI](https://x.com/AnthropicAI/status/2074185348142280912) | [@NeelNanda5](https://x.com/NeelNanda5/status/2074193936588148891)

**Sakana AI Sheaf-ADMM框架，多Agent分布式协调在Sudoku任务中达93%求解率**
- Sakana AI 论文 **"Learning Multi-Agent Coordination via Sheaf-ADMM"**（Jeffrey Seely、Bartłomiej Cupiał、Llion Jones；ICML 2026）将多Agent协调建模为基于 cellular sheaf 的可微 ADMM 优化：每个 Agent 只见局部视图，通过 primal / consensus / dual 状态变量进行邻居协调。在多Agent Sudoku 上**求解率 93%**（同等参数 MPNN baseline 仅 11%），MNIST 在 canvas-size domain shift 下保留 **86%** 精度（CNN baseline 仅 11%）。
  > 💡 Sakana 把分布式优化经典方法（ADMM）与拓扑学（sheaf）嫁接到多Agent LLM 协同，相比黑盒消息传递可显式审计协调过程，对分布式 AI 系统设计提供新工具。
   - 来源: [Sakana Blog](https://sakana.ai/sheaf-admm/) | [arXiv](https://arxiv.org/abs/2605.31005)

**MIPU：腾讯/中科院等团队提出面向LLM RL的"推理侧单调策略提升"目标**
- 论文 **"The Mirage of Optimizing Training Policies: Monotonic Inference Policies as the Real Objective for LLM Reinforcement Learning"**（Jing Liang 等 12 人，含腾讯/中科院作者）指出 LLM RL 中的"训练-推理 mismatch"导致离线策略偏移使训练脆弱甚至崩溃，现有方法只稳定训练策略而非真正改善部署用的推理策略。论文提出新目标 **MIPI（Monotonic Inference Policy Improvement）** 和两阶段框架 **MIPU**，通过推理侧 gap proxy 挑选同步候选更新。实验在两个模型规模的高 mismatch 设置下，MIPU 提升平均推理性能与训练稳定性。
  > 💡 把 RL 目标从"训练侧策略改进"重新定义为"推理侧单调提升"，直击 LLM RL 训练常崩溃的根因，对所有走 RLHF/RLVR 后训练路线的团队有方法论价值。
   - 来源: [arXiv](https://arxiv.org/abs/2606.29526)

**PMD：跨episode"程序性记忆蒸馏"让LLM在RLVR训练中持续自改进**
- 论文 **"Procedural Memory Distillation: Online Reflection for Self-Improving Language Models"**（Ye Liu 等 9 人）针对 RLVR 与 SDPO 等自蒸馏方法只使用 episode 级 verifier 信号而忽略 rollout 中更丰富程序性信息的问题，提出 **PMD**：将跨 episode 信号（哪些策略反复通过、哪些失败模式持续存在）转化为可复用的"程序性记忆"，在线蒸馏到策略权重中（推理时无需记忆）。在 Qwen3-8B 与 OLMo3-Instruct-7B 上，PMD 相对 SDPO 在 **SciKnowEval 上提升 3.8-5.5%、LiveCodeBench 上提升 7.9-13.6%**；冻结记忆或策略任一方都会导致 SciKnowEval 各域下降超 10%。
  > 💡 "co-evolution of policy & memory"是 RLVR 自改进的关键设计点，对 RL 后训练长期稳定增益有借鉴意义；不依赖外部记忆即可内部化跨 episode 经验，对部署侧无额外开销。
   - 来源: [arXiv](https://arxiv.org/abs/2607.01480)

**Embodied.cpp：跨异构机器人的统一C++推理运行时，VLA模型闭环任务成功率最高100%**
- 论文 **"Embodied.cpp: A Portable Inference Runtime of Embodied AI Models on Heterogeneous Robots"**（Ling Xu 等 9 人）指出 VLA（vision-language-action）与 WAM（world-action）模型部署分散在不同 Python 栈与机器人胶水代码中，现有推理运行时多为请求-响应服务模式，无法满足具身场景的多速率闭环控制、batch-1 延迟优先与可扩展 I/O。Embodied.cpp 把 VLA / WAM 的共享执行路径抽象为 **5 层架构**（input adapters / sequence builders / backbone execution / head plugins / deployment adapters），在 VLA 模型 HY-VLA 上闭环任务成功率 **100%**、pi0.5 上 91%，WAM benchmark 块显存从 312.2 MiB 降至 88.1 MiB。
  > 💡 把"具身模型跨硬件部署"统一到单一 C++ 运行时抽象，类似大模型推理侧的 vLLM/TensorRT 之于 LLM；对 VLA / WAM 走向工业级部署有底层基建意义。
   - 来源: [arXiv](https://arxiv.org/abs/2607.02501)

### X讨论
**Google DeepMind与Apptronik扩大人形机器人研究合作，Apollo 2平台将贡献真实世界数据**
- Google DeepMind宣布与Apptronik扩大研究合作。Apptronik位于德州奥斯汀的 **Robot Park** 数据采集与训练设施已扩展至约**90,000 平方英尺**，同步发布 **Apollo 2** 人形机器人平台（双足与轮式两种构型）。Apollo 2 机器人在 Robot Park 及 DeepMind、客户站点执行物流、制造、零售等任务，**收集的真实数据反哺 Gemini Robotics 基础模型**。Apptronik CEO Jeff Cardenas 表示该机制是"持续学习闭环"：工作-采集-改进循环。
  > 💡 DeepMind通过真实硬件平台合作补齐具身智能数据缺口，Apollo 2成为DeepMind人形机器人研究的核心数据源；多场地分布式数据采集正在取代单一实验室内演示。
   - 来源: [@googledeepmind](https://x.com/GoogleDeepMind/status/2074157282477154597#m) | [Apptronik Press Release](https://apptronik.com/news-collection/welcome-to-robot-park-where-apptroniks-apollo-goes-to-work)

**Anthropic 发布"The Making of Claude Code"幕后故事专题**
- Anthropic 上线专题 **"The Making of Claude Code"**，由研究员、工程师与早期用户共同讲述。Claude Code 的雏形是 Anthropic Labs 团队负责人 **Ben Mann** 与 RL 负责人 **Shauna Kravec** 在 2021-2022 年间做的内部 VS Code 扩展；2022 年底 **Dawn Drain** 团队做出了支持 bash 与持久 shell 的"clide"命令行原型。**Boris Cherny**（Claude Code 现任负责人）2024 年初在 Labs 内部 demo 一个能在 Apple Music 上读屏的 **Claude CLI**，当时仅拿到两三个 Slack 点赞。Labs 经理 **Adam Wolff**（前 React 核心团队、电影专业出身）受 Boris 多次邀请出任经理，从工程经理 **Raphael Lee**、设计师 **Meaghan Choi**、产品负责人 **Cat Wu** 到工程师 **Sid Bidasaria、Robert Boyce、Igor Kofman** 陆续加入。**2025 年 2 月**正式以 **Claude Code** 名称对外发布研究预览；**Claude 4 系列模型** + 订阅制（"业务模式创新 + 模型创新"）共同推动起飞。**Boris Cherny 自述**：2025 年 2 月 Claude Code 写约 **10%** 的代码，5 月升至 30-40%，**Sonnet 4** 发布后他自己 **100% 代码由 Claude Code 撰写**；Shauna 提到自己同时跑 12 个 Claude 在不同任务上的"集群"。早期外部用户包括 **Ramp** 的 AI DevX 负责人 Austin Ray（5 分钟内认定"将根本改变一切"）、**Bun** 创始人 Jarred Sumner（曾因团队讨论禁用 Claude Code 而坚持反对）、为阿拉斯加残障青年非营利组织做应用的顾问 Kyle Easterly 等。团队文化上，**Boris** 坚持"模型能力达到 20-30% 可用就发布，等下一代模型达 80-90%"的高容错节奏；**Sid** 提到内部"无 PR 限制、无审核限制"，修复可几分钟推到用户。
  > 💡 Claude Code 走的是"模型能力 + 工具链 + 小团队 + 快速迭代"路线，与 GitHub Copilot 类"插件式助手"路径迥异；官方公开整段研发历程，是少数把"Agent 产品如何炼成"透明化的头部案例，对国内 IDE/Agent 产品团队有方法论价值。
   - 来源: [Anthropic](https://www.anthropic.com/features/making-of-claude-code) | [@claudeai](https://x.com/claudeai/status/2074244664199115201)

**腾讯混元向vLLM贡献HPC-Ops高性能Attention与MoE推理后端**
- 腾讯混元团队向开源推理框架vLLM贡献了HPC-Ops后端，针对Hopper架构优化Attention与FP8 MoE算子，专为混元Hy3模型设计。该方案在变长Decode与MoE延迟场景下提升吞吐性能，集成至vLLM后可在生产环境直接部署混元大模型。
  > 💡 腾讯混元从单纯发布模型转向推理基础设施共建，进一步绑定vLLM生态，为开源大模型降低部署门槛并强化自身在大模型推理栈的存在感。
   - 来源: [vLLM Blog](https://vllm.ai/blog/2026-07-06-vllm-hpc-ops)

---
*更新时间: 2026-07-07 07:35*
