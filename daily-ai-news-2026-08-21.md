## 08月21日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 14 条

---

## 要点汇总

- 产业动态：Ramp 数据显示 OpenAI 在美企用户中缩小与 Anthropic 的份额差距; Binance 开放 AI agents 交易，但权限和风控主要交给用户; Claude 平台正式上线 computer use、Skills API 和 Files API，面向生产级 agents; Mistral 发布 Agentic Search：用多步检索提升复杂文档问答; AT&T 计划以开源模型压平对 Anthropic、OpenAI 的支出
- 算力追踪：英伟达计划年底前小批量交付面向中国客户的定制 AI 芯片; 阿里巴巴 CEO：AI 相关业务年化收入率本季度将达 100 亿美元
- 初创&融资：Veeda AI 完成超 9000 万美元种子轮融资，Sanja Fidler 领衔做物理 AI 世界模型; River AI 宣布 Cisco 加入其 $1.1B 融资轮
- 研究关注：Zetta ζ：面向自演化具身智能的闭环 Harness; OmniScientist：全模态全学科 AI Scientist; Co-RL：多智能体 RL 中涌现无监督推理; SPADE：自适应合成可执行环境中的自我博弈; Recirculation：推理时递归增强
- X讨论：Ramp 推出 Router：用模型路由器让客户在多家大模型间切换

---

## 📖 详细参考

### 产业动态
**Ramp 数据显示 OpenAI 在美企用户中缩小与 Anthropic 的份额差距**
- 企业支出管理平台 Ramp 公布的最新数据显示，OpenAI 在其覆盖的超过 7 万家美国企业用户中，正逐步缩小与 Anthropic 之间的市场份额差距。今年 5 月，Anthropic 在 Ramp 的付费企业用户中以 41% 对 39% 超过 OpenAI，ChatGPT 母公司此后未再夺回头名；至 7 月，Anthropic 份额接近 44%，OpenAI 接近 40%。Ramp 经济学家 Ara Kharazian 指出，按 2026 年第三季度迄今数据，OpenAI 在该群体中的增速已快于 Anthropic，但距离季度结束仍有约一个月时间，趋势仍可能再度变化。Ramp 仅披露市场份额百分比，未公布实际消费金额，且样本偏向使用其企业信用卡与账单支付产品的科技行业公司，并不包含使用 American Express 等其他支出管理工具的大型企业。
  > 💡 Ramp 数据是观察两家未上市公司相对表现的高频代理指标，但样本明显偏向硅谷科技客群，且不披露金额，份额 1–2 个百分点的波动并不足以证明粘性差距；更值得关注的是文中所提的企业随新模型发布而在两家公司之间来回切换这一行为本身，它意味着企业级 AI 支出在 IPO 之前仍缺乏结构性忠诚度。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/20/openai-is-gaining-on-anthropic-with-business-users-new-data-indicates)

**Binance 开放 AI agents 交易，但权限和风控主要交给用户**
- Binance 推出 Agent OS，让开发者把 AI 应用和 agents 接入其金融基础设施，直接使用 Binance API、Wallet Agentic Hub、x402 验证和 payment facilitator API，并支持与 ChatGPT、Claude Code、Cursor 等工具联动。用户可以把 agents 绑定到独立 subaccount，配置现货或期货权限，默认禁止提现；用户既可以要求每笔订单都审批，也可以授权 agent 自动执行交易。Binance 没有单独限制 AI agent 的盈亏上限，实质上由 subaccount 注资额充当风控边界。
  > 💡 这是把 agent 能力真正推到“动钱”的位置，但风控边界仍按用户自行配置，意味着交易安全责任从平台向终端用户和上层 agent 设计回流；一旦 agents 进入金融执行层，权限隔离会比模型能力本身更关键。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/20/binance-now-lets-ai-agents-trade-but-keeping-them-in-check-is-largely-up-to-users/)

**Claude 平台正式上线 computer use、Skills API 和 Files API，面向生产级 agents**
- Anthropic 在 Claude 平台正式发布面向生产环境 agent 的三项能力：computer use、Skills API 和 Files API。此外，Computer Use 还新增了一项浏览器使用工具，专为在网页应用中运行的智能体设计。该公告把 Claude 的 agent 工作流进一步推向可调用工具、文件处理和计算机操作的生产场景，目标是让 agents 更稳定地执行多步任务。
  > 💡 Anthropic 在把“会聊天”继续往“能干活”推进，且把文件和桌面操作纳入同一套 API 叙事，说明 agent 平台竞争已经从模型对话转向工作流执行和外部系统整合。
   - 来源: [Claude](https://claude.com/blog/computer-use-skills-api-files-api)

**Mistral 发布 Agentic Search：用多步检索提升复杂文档问答**
- Mistral 发布 Agentic Search，强调它不是一次性 RAG，而是一个检索层：模型可以通过 `search`、`open`、`navigate`、`read`、`grep` 等工具多步查找、阅读和核验复杂文档。官方给出的基准结果显示，它在 FinanceBench 上把正确率从 26.7% 提升到 86%，在 OfficeQA Pro 上提升 45.6 个百分点，同时将 p90 延迟最多降低 39.6%，token 消耗最多减少三分之一。
  > 💡 Mistral 把检索从“召回一段文本”升级成“带推理的阅读系统”，这对企业文档智能很重要：真正的瓶颈往往不是找不找得到，而是能不能沿着证据链自己把答案走出来。
   - 来源: [Mistral](https://mistral.ai/news/agentic-search)

**AT&T 计划以开源模型压平对 Anthropic、OpenAI 的支出**
- 电信运营商 AT&T 副总裁 Mark Austin 表示，公司计划在未来几年通过更多使用 Nvidia Nemotron 等开源模型，把员工在 Anthropic 与 OpenAI 模型上的支出保持在现有水平。该策略意在遏制闭源 API 账单持续膨胀。
  > 💡 大型企业级客户用开源模型替代部分闭源 API 调用，是模型层“去依赖”的重要信号；Nemotron 等企业友好型开源权重正成为企业 IT 预算对冲闭源涨价的现实选项。
   - 来源: [The Information](https://www.theinformation.com/articles/t-using-open-source-models-curb-anthropic-bills)

### 算力追踪
**英伟达计划年底前小批量交付面向中国客户的定制 AI 芯片**
- 据两位员工透露，英伟达计划在今年年底前开始小批量出货一款为中国客户量身定制的 AI 芯片。该芯片为英伟达语言处理单元（LPU）的变体，多家中国客户已下达订单。LPU 由英伟达基于 Groq 授权技术开发，与 GPU 协同用于加速 AI 聊天机器人的响应速度。
  > 💡 在出口管制约束下，英伟达用 LPU 这一新品类绕开 GPU 限制，为中国市场保留一条有限但可控的供给通道；Groq 的低延迟推理 IP 也由此获得进入中国客户的间接路径。
   - 来源: [The Information](https://www.theinformation.com/articles/nvidia-plots-china-comeback-new-ai-chip)

**阿里巴巴 CEO：AI 相关业务年化收入率本季度将达 100 亿美元**
- 阿里巴巴集团 CEO 吴泳铭在周四的财报电话会上表示，截至 9 月的当前季度，公司 AI 相关产品的年化收入运行率有望达到 100 亿美元，高于上一季度的 73 亿美元。截至 6 月的当季，阿里营收增长 9%，主要来自“AI 云和算力服务”业务 45% 的增长。
  > 💡 在整体营收个位数增长的背景下，AI 云与算力服务以 45% 的增速成为阿里增长主引擎，100 亿美元年化收入率意味着国内云厂商的 AI 商业化已进入真金白银的兑现阶段。
   - 来源: [The Information](https://www.theinformation.com/briefings/alibaba-ceo-expects-ai-related-arr-reach-10-billion-september)

### 初创&融资
**Veeda AI 完成超 9000 万美元种子轮融资，Sanja Fidler 领衔做物理 AI 世界模型**
- 由前 Nvidia AI 研究员、Toronto 大学教授 Sanja Fidler 领衔的 Veeda AI 已完成超过 9000 万美元种子轮融资，投资方包括 Radical Ventures 与 Khosla Ventures。公司由 Fidler、Huan Ling 和 Zan Gojcic 共同创办，目标是为 physical AI / embodied intelligence 构建多模态世界模型和高保真模拟环境；The Logic 还披露，Veeda 早在 6 月就完成公司注册，并在随后补充了来自 Radical 和 Khosla 的董事。
  > 💡 这不是普通的“world model 创业”，而是把 Nvidia 系世界模型研究线直接搬到创业层并拿到重金下注，说明 physical AI 的资本门槛正在迅速抬高。
   - 来源: [The Logic](https://thelogic.co/news/exclusive/veeda-ai-sanja-fidler-nvidia/)

**River AI 宣布 Cisco 加入 $1.1B 融资轮**
- River AI 宣布，Cisco Investments 将作为战略投资者加入其 11 亿美元融资轮。该公司强调个人化、用户自有的 AI 需要更强的产品和基础设施支撑，并表示很期待与 Cisco 团队合作。
  > 💡 这类“硬件/网络巨头做战略投资人”的信号，通常意味着 personal AI 的竞争不只在模型，而是开始往分发、设备与基础设施层扩展。
   - 来源: [@River](https://x.com/river_ai_inc/status/2090495631668519045)

### 研究关注
**Zetta ζ：面向自演化具身智能的闭环 Harness**
- 论文指出，当前具身智能 Agent 多采用开环 Harness，在回合结束后才进行反思，难以实时管控物理执行过程。作者提出 Zetta 这一闭环具身 Harness，可在保持基础策略冻结的前提下，在线演化基于代码的运行时评判器与恢复技能。该系统通过三个时间尺度分离的循环分别提供动作级治理、回放级评判—恢复提议，以及校验门控的技能更新，并配合将智能体逻辑与异构执行资源解耦的 Z-Infra 基础设施。论文报告称，在 LIBERO-Pro 与 RoboCasa 上分别取得 90.8% 与 93.6% 的成功率，并实现 11.1 倍推理加速。
  > 💡 Zetta 把具身智能的训练—执行关系从“训完再用”转向“边用边演化”，通过三时间尺度闭环把动作频率对齐到机器人—环境状态变化节奏，是把 Agent harness scaling 思路落到物理执行层的一次系统性推进。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2608.16590) | [arXiv](https://arxiv.org/abs/2608.16590)

**OmniScientist：全模态全学科 AI Scientist**
- 论文提出 OmniScientist，由感知层和 ideation、experiment、writeup 三个自治 agent 组成，在确定性流水线中直接处理图像、信号、音频、视频、3D 结构、轨迹、表格、公式和图等原始证据。系统在 36 个真实数据案例中均完成了从原始数据到可编译论文稿件的完整流程；与只接收预计算标量特征的盲版系统相比，直接感知原始证据在配对比较中赢得 85% 的判断。
  > 💡 AI Scientist 的竞争焦点正从自动写作转向能否直接处理多模态证据，并让实验过程和最终结论可追溯。
   - 来源: [arXiv](https://arxiv.org/abs/2608.13558)

**Co-RL：多智能体 RL 中涌现无监督推理**
- 论文提出 Co-RL，让多个不共享参数的模型互相提供 reward，减少对 ground-truth label 的依赖。作者指出，单模型自奖励容易放大相关错误并导致训练坍塌；通过混合模型家族、参数规模和改写样本提高 cohort diversity 后，Co-RL 在 7 个文本基准上平均提升 3.0%–8.6%，在 4 个多模态基准上平均提升 2.3%–7.2%。
  > 💡 这项工作把无监督推理的关键从单模型自我评价转向多模型协同去偏，群体多样性成为训练稳定性的新变量。
   - 来源: [arXiv](https://arxiv.org/abs/2608.17253)

**SPADE：自适应合成可执行环境中的自我博弈**
- 论文提出 SPADE，让同一个 LLM 分别扮演 Environment Designer 和 Reasoning Agent，自动生成带状态转移、奖励函数和验证代码的长时程训练环境。环境设计器根据 agent 在有无特权提示时的 reward 差距调整任务难度；在 30B 模型规模下，SPADE 比最强固定环境基线平均高 5.3 分，在 BFCL-v4 multi-turn 和 ACEBench-Agent 上分别提升 5.7 和 13.9 分。
  > 💡 该方法把训练环境本身变成可优化对象，为 agent 的持续自我改进提供了比固定 benchmark 更开放的路径。
   - 来源: [arXiv](https://arxiv.org/abs/2608.19197)

**Recirculation：推理时递归增强机制**
- 论文提出 recirculation，通过在 prefill 阶段对现成基础模型加入递归式处理，使模型能够追踪 belief states，同时基本不增加生成阶段延迟。adaptive recirculation 在 Gemma3 系列上使 perplexity 降低 23%，GSM8k 准确率提高 21%，并在其他下游任务上持续改善。
  > 💡 这条路线把推理收益放在状态更新机制而非继续扩大训练规模上，提供了利用现有模型权重获得额外能力的架构方向。
   - 来源: [arXiv](https://arxiv.org/abs/2608.17981)

### X讨论
**Ramp 推出 Router：用模型路由器让客户在多家大模型间切换**
- Ramp 发布名为 Router 的 AI 模型路由服务，允许用户和企业通过 API 在 OpenAI、Anthropic、DeepSeek、Moonshot、Minimax、Nvidia、xAI 和 Z.ai 等模型之间切换。Ramp 表示，这套系统已在内部使用了三年；目前仅面向美国用户开放，2026 年内免费，用户仍需承担模型推理成本，另外还附带 26 美元的启动信用额度。Router 还提供按模型供应商、基准分数或难度分级的路由策略，以及 token 花费、延迟、fallback 尝试等仪表盘；默认数据保留期为一年。
  > 💡 Ramp 把企业支出管理、token 监控和模型路由揉成一体，说明“模型入口”正在从纯 API 市场变成预算控制层；这类产品的竞争点不是单一模型能力，而是企业能否把多模型调用编排成可计费、可审计的基础设施。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/20/ramp-launches-its-own-ai-model-router-called-router/) | [@Ramp](https://x.com/tryramp/status/2090146780512227825)

---
*更新时间: 2026-08-21 06:47*