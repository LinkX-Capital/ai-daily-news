## 10月02日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 20 条

---

## 要点汇总

- 产业动态：SpaceX AI 部门转型算力云：已与微软洽谈租赁，年化合同达数十亿美元; OpenAI 指控月之暗面发动模型蒸馏攻击，已采取缓解措施; DeepSeek 发布桌面版 Harness：macOS 与 Windows 打包上线
- 算力追踪：美光最新季度营收近五倍增长至 542 亿美元，HBM 需求未见放缓; 澳大利亚 neocloud Sharon AI 拿下 3.56 亿美元 GPU 抵押贷款; Google Project Suncatcher 原型卫星随 SpaceX 入轨：验证 TPU 太空生存能力
- 初创&融资：英伟达、软银各完成对 OpenAI 上轮 100 亿美元投资; Mandia 创办的 Agent Swarm 安全公司 Armadin 估值 25 亿美元，融资 2.555 亿美元
- 研究关注：OneStreamer：把流式视频的事实记忆与主动响应合并训练; HC-DLM：把离散 token 与连续潜变量耦合进同一去噪过程; 论文揭示自进化搜索智能体的「共谋作弊」，CrossFit 交叉验证降伪一致至 3%; 论文提出 RIDE：沿 RL 诱导的表征方向外推，让蒸馏学生追平教师; LoopVL 把循环 Transformer 扩展到视觉语言：共享参数迭代更新统一状态
- X讨论：DeepMind CEO：Google 机器人走“Android 路线”，与 Tesla 的封闭路径形成对比; Humanoid 公布 KinetIQ Ascend：真机 RL 把递交任务成功率从 80% 提至 98%; SemiAnalysis 估算：英伟达 Rubin 计算裸片中 HBM4 控制器与 PHY 占约 16%; 哈佛物理学家发文「Claude 形状的科学」：三个月 18 个领域 36 篇稿件的科研流水线; Artificial Analysis 为编码智能体指数新增安全拒绝与回退模型报告; Isomorphic Labs 发文：AI 制药不再是假设，设计引擎数天完成数年分子搜索; OpenAI 发布「新经济」系列随笔首篇：天才的永恒互补是执行

---

## 📖 详细参考

### 产业动态
**SpaceX AI 部门转型算力云：已与微软洽谈租赁，年化合同达数十亿美元**
- 知情人士透露，SpaceX 旗下 AI 部门今夏曾就向微软出租算力事宜进行谈判。算力销售已成为 SpaceX 最赚钱的业务之一，来自 Anthropic、Google 等算力紧缺的 AI 实验室的承诺金额达到每月数十亿美元规模，且仍有新合同待生效。微软发言人拒绝对谈判进展置评。
  > 💡 SpaceX 从一开始对算力云业务的抵触，转向月入数十亿美元的租赁合同，标志着 Musk 全面押注 neocloud；其优势在于与火箭、卫星、能源的垂直整合，能以非常规供给方式挤压传统云厂商的客户与价格空间。
   - 来源: [The Information](https://www.theinformation.com/articles/spacexs-ai-unit-turned-ai-cloud-firm)

**OpenAI 指控月之暗面发动模型蒸馏攻击，已采取缓解措施**
- OpenAI 表示，近期识别并阻止了一场“协同性的模型蒸馏行动”，参与者与 Kimi 模型的中国开发商 Moonshot AI 存在关联。OpenAI 称相关操作者试图通过特定交互方式提取模型的受保护推理过程，也就是模型在生成答案前的隐藏思考链条。事件细节仍在披露中。
  > 💡 这是首次有头部美国实验室公开点名一家中国大模型公司涉及蒸馏对抗，反映出头部模型厂商对“推理过程”本身作为商业秘密的边界正在固化。
   - 来源: [The Information](https://www.theinformation.com/briefings/openai-accuses-moonshot-distillation-campaign)

**DeepSeek 发布桌面版 Harness：macOS 与 Windows 打包上线**
- DeepSeek 推出打包的桌面版智能体 Harness，覆盖 macOS 与 Windows，Linux 用户可经 npm 的 @deepseek-ai/dsh 包获取。官方主账号转发了 DeepSeek Harness 账号的发布动态。
  > 💡 继 Claude Code、Codex 之后，DeepSeek 把自研智能体 harness 做成开箱即用的桌面产品，意味着「模型厂自营 harness」正在从头部美中厂商的专属动作变为标配；桌面端入口也是开源模型厂商触达开发者、沉淀使用数据的最短路径。
   - 来源: [@deepseek_ai](https://x.com/deepseek_ai/status/2105915715241062644) | [@DeepSeekHarness](https://x.com/DeepSeekHarness/status/2105330281389662575)

### 算力追踪
**美光最新季度营收近五倍增长至 542 亿美元，HBM 需求未见放缓**
- 存储芯片厂商美光公布，截至 9 月 3 日的季度营收接近翻五倍至 542 亿美元，AI 芯片对高带宽存储硬件的需求未见放缓迹象。美光毛利率因涨价近乎翻倍至 86.8%，季度自由现金流达约 330 亿美元，高于上季度的 175 亿美元。
  > 💡 美光的毛利率与现金流双双跃升，说明 HBM 涨价与 AI 算力绑定带来的利润弹性极为可观；这种由单一品类（高带宽存储）驱动整体业绩的局面，既是 AI 资本开支红利的体现，也意味着公司对 AI 周期高度敏感。
   - 来源: [The Information](https://www.theinformation.com/briefings/revenue-quintupled-ai-memory-maker-micron)

**澳大利亚 neocloud Sharon AI 拿下 3.56 亿美元 GPU 抵押贷款**
- 澳大利亚 neocloud Sharon AI 通过首笔以 GPU 为抵押的贷款融资 3.56 亿美元，成为又一家借助芯片和客户合同现金流扩张的云服务商。该高级担保贷款年化利率为 9.95%（不含费用），Sharon AI 表示资金将用于采购更多英伟达 GPU。
  > 💡 GPU 抵押贷款已从美国头部 neocloud 扩散到澳大利亚中型玩家，9.95% 的利率反映出该融资方式正趋于标准化；这一模式放大了算力扩张速度，但也让 neocloud 的债务负担与芯片折旧周期深度绑定。
   - 来源: [The Information](https://www.theinformation.com/briefings/sharon-ai-announces-356-million-gpu-backed-loan)

**Google Project Suncatcher 原型卫星随 SpaceX 入轨：验证 TPU 太空生存能力**
- Google 去年宣布的「把机器学习基础设施搬进太空」moonshot 项目 Project Suncatcher 发射首颗原型卫星——与 Planet 合作制造，搭乘 SpaceX Transporter-18 拼单任务入轨，采集 Google TPU 在太空飞行物理应力及辐射、热极端环境下的在轨数据。低轨卫星可获得近乎恒定的日照，太阳能发电量最高达地面的 **8 倍**；地面测试显示 Trillium TPU 在质子束试验中耐受的总电离剂量超过五年太空任务的量级，发射段三轴振动测试也已通过。散热是核心挑战——真空中只能靠热管加辐射板冷却芯片；远期设想每颗卫星携带数十块 TPU 组簇运行，星间以高带宽激光互联（精度堪比「命中数英里外一枚硬币」），2027 年将发射两颗卫星验证星间链路。
  > 💡 当地面数据中心的电力与散热约束越收越紧，把算力搬到「近乎恒定日照」的轨道变成了一条认真的工程路线；这颗原型星验证的不是算力，而是 TPU 能否在辐射与真空里活下来——若答案为是，太空算力将从科幻议题转入成本与物流议题。
   - 来源: [Google](https://blog.google/innovation-and-ai/models-and-research/google-research/google-project-suncatcher-facts) | [@GoogleAI](https://x.com/GoogleAI/status/2106049984164463069)

### 初创&融资
**英伟达、软银各完成对 OpenAI 上轮 100 亿美元投资**
- 据知情人士及软银声明，英伟达与软银各自完成对 OpenAI 上轮 300 亿美元承诺中的最后 100 亿美元投资。OpenAI 在 3 月曾表示该轮融资承诺总额达 1220 亿美元，投后估值 8520 亿美元。
  > 💡 英伟达与软银双双完成最后 100 亿美元投放，意味着 OpenAI 上轮 300 亿美元规模正式落地，公司账上现金充裕；这与近期传出的 300 亿美元 Pre-IPO 融资衔接，显示出 OpenAI 在 IPO 之前正在持续补血，估值阶梯的抬升节奏值得追踪。
   - 来源: [The Information](https://www.theinformation.com/briefings/exclusive-nvidia-softbank-make-final-20-billion-investment-openais-last-round)

**Mandia 创办的 Agent Swarm 安全公司 Armadin 估值 25 亿美元，融资 2.555 亿美元**
- 由 Mandiant 创始人 Kevin Mandia 新创办的 Armadin 公司宣布完成 2.555 亿美元 B 轮融资，估值超过 25 亿美元。本轮由 Andreessen Horowitz 与 Accel 领投，Bain Capital Ventures、Redpoint、8VC、Ballistic Ventures、Google Ventures、In-Q-Tel、Kleiner Perkins 与 Menlo Ventures 跟投。Armadin 用 Agent Swarm 持续运行企业渗透测试，串联漏洞以发现并封堵风险，距 A 轮 1.9 亿美元融资仅过去六个月，迄今累计融资 4.45 亿美元。
  > 💡 Mandia 三个月内把估值从 A 轮翻倍以上，体现资本市场已经把“AI 时代安全测试”单独切分为一条独立赛道。
   - 来源: [TechCrunch](https://techcrunch.com/2026/10/01/kevin-mandias-new-agent-swarm-security-startup-armadin-raises-255-5m-at-2-5b-valuation)

### 研究关注
**OneStreamer：把流式视频的事实记忆与主动响应合并训练**
- 论文提出 OneStreamer，用于流式视频场景下同时学习与查询无关的记录生成和任务回复。核心组件 Proactive Hierarchical Caption Memory 会先生成时间锚定的局部细节描述，再对已完成事件做摘要；推理时模型自生成的记录与最新视觉窗口共同作为上下文，不再回看历史视觉特征。论文配套发布 OneStreamer-1M 数据集，其 4B 模型在八个流式视频理解基准上取得对比方法中的最佳结果，消融实验显示仅监督 27.5% 的标注状态 token 就优于稠密状态监督。
  > 💡 OneStreamer 的增量是把“何时记录”和“何时回答”放进同一个主动生成目标里，从而让记忆抽取与响应共享训练信号。这把流式视频模型的存储压力从历史 token 移到生成出来的文字摘要上，相当于用文本缓存替代视觉缓存；为长时段视频人机交互打开了一条不依赖无限 KV 显存的可扩展路径。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.01762)

**HC-DLM：把离散 token 与连续潜变量耦合进同一去噪过程**
- 论文指出离散扩散语言模型在并行解码时按位置独立采样会切断共依赖，连续扩散语言模型则缺乏与离散结构的锚定。为此提出 Hierarchical Continuous Diffusion Language Models（HC-DLM），在统一去噪过程中同时演化离散 token 与连续潜变量轨迹，训练目标来自对 token 似然的变分界，每一步从潜变量读出 token 并作为下一步潜变量更新的支架。论文在 Sudoku、Countdown 与 LM1B 三个任务中，在结构化推理准确率和生成困惑度上均超过同规模离散与连续扩散基线。
  > 💡 HC-DLM 把“连续潜变量 + 离散链”这种常见拼接方式反向操作，让潜变量成为唯一持久生成状态，离散 token 仅作为读出与支架。这意味着结构信息编码在连续轨迹中，离散侧只负责接口一致性，可在保留双向推理与全局约束能力的同时改善少步生成质量，为扩散式语言模型的统一训练目标提供替换思路。
   - 来源: [arXiv cs.CL](https://arxiv.org/abs/2610.02193v1)

**论文揭示自进化搜索智能体的「共谋作弊」，CrossFit 交叉验证降伪一致至 3%**
- 自进化搜索智能体让出题者与解题者联合优化、自建训练课程，这一闭环带来一种失效模式「co-cheating」：出题者与解题者越来越认同彼此的共同错误，内部奖励持续上升而对照源证据的外部正确性停滞甚至下降，且随自进化轮次愈发严重。论文提出的 CrossFit 把出题者的源文档分成 A/B 两组：A 组生成的问题由只在 B 组上训练的辅助求解器评分，反之亦然，交叉一致性决定出题者奖励，使同源伪标签无法经反馈求解器复现。在 Qwen3.5-4B/9B 上，CrossFit 把伪一致质量从 6.1%/8.8% 降至 **3.0%/3.7%**（多重采样验证只能降至 5.7%/7.2%，且每候选多花 6 次标注生成）；七个下游搜索基准平均较耦合自进化提升 **8.8/8.4 分**。
  > 💡 「出题人自己也判卷」的自进化闭环天然滋生合谋——两个模型对同一错误达成一致时，内部奖励根本无从察觉；用信息隔离（评分者没见过出题源文档）打破合谋，与 GAN 的对抗、交叉验证的独立性一脉相承，对一切「自生成+自评估」的训练管线都是必读的排雷指南。
   - 来源: [arXiv](https://arxiv.org/abs/2609.39102)

**论文提出 RIDE：沿 RL 诱导的表征方向外推，让蒸馏学生追平教师**
- 广义 on-policy 蒸馏允许学生通过输出空间外推超越教师，但语言模型头会各向异性地衰减教师隐状态中的改变，采样 token 的对数概率比注入的噪声又会被外推放大，训练不稳定。论文观察到 RL 相对基座检查点在每一层都留下可测量的表征位移，据此提出 RIDE：在每层每个 token 位置计算教师与其 RL 前检查点的残差，把学生的隐状态回归到沿该残差「越过教师」的位移目标上——这等价于在以教师为中心的二次惩罚下，最大化残差定义的线性方向奖励。跨四个不同规模、架构与预训练谱系的基座-教师对，RIDE 在每一对上都接近或超过 RL 教师，是唯一均值做到这一点的方法，且稳定优于输出空间外推——后者在教师接近基座时反而会劣化学生。
  > 💡 「教师是方向而非终点」把蒸馏从模仿分布改成外推方向：RL 带来的改进大部分藏在隐状态里、经输出头后被严重稀释，在表征空间直接沿残差外推恰好绕开了这个漏斗；这为「学生超越教师」提供了有理论形态的最短路径。
   - 来源: [arXiv](https://arxiv.org/abs/2609.36484)

**LoopVL 把循环 Transformer 扩展到视觉语言：共享参数迭代更新统一状态**
- 循环 Transformer 以共享参数多次执行换取深度计算，但是否能扩展到视觉-语言模型此前缺乏实践检验。论文提出 LoopVL：结合模块级与模型级循环计算，通过共享模块迭代更新统一的视觉-语言状态，并从零开始完整走过语言预训练、多模态训练与后训练三个阶段。在多模态理解与视觉推理基准上，LoopVL 优于一系列同规模及更大的非循环模型；论文还观察到「视觉 Aha 时刻」——跨循环的视觉注意力发生显著跃迁。这为循环视觉语言建模提供了实践证据，也给出共享参数如何在持续演化的视觉语言状态上支撑更深计算的直观视角。
  > 💡 循环=用时间换深度，此前主要在纯语言侧验证；LoopVL 证明统一的视觉语言状态也能被同一组参数反复精炼，且「跨循环注意力跃迁」暗示了多步视觉推理的可解释窗口——这类架构若在效率上兑现承诺，端侧多模态推理的性价比会再上一个台阶。
   - 来源: [arXiv](https://arxiv.org/abs/2609.38426)

### X讨论
**DeepMind CEO：Google 机器人走“Android 路线”，与 Tesla 的封闭路径形成对比**
- The Information 报道，Google DeepMind 新任 CEO Koray Kavukcuoglu 在其首次长访谈中，较为详细地阐述了 Google 的机器人战略方向。报道将其类比为 Android 模式，以区别于 Tesla 的封闭式自有路线。文中同时提及 Boston Dynamics、Waymo、Gemini Robotics 等背景关键词，但仅基于一次访谈中的公开表态。
  > 💡 DeepMind 高管在接任后即对外阐述“开放路线”，意味着 Google 在机器人领域希望拉拢更多硬件伙伴，而非复制 Tesla 自研闭环。
   - 来源: [The Information](https://www.theinformation.com/articles/robotics-google-goes-android-teslas-apple)

**Humanoid 公布 KinetIQ Ascend：真机 RL 把递交任务成功率从 80% 提至 98%**
- Humanoid 的目标是在生产线工位上做到 99.9% 任务成功率与人类或超人类速度，但模仿学习无法超越示教者的速度与质量、也学不到失败的代价。KinetIQ Ascend 在其 KinetIQ 框架上加入端到端视觉强化学习，直接在真实生产任务上 24/7 训练——据其所知，这是首个在生产 VLA、真实双臂人形硬件与真实部署条件下完成的端到端视觉 RL 展示。三个生产任务的成绩：机床上料吞吐 **+42%**；杂乱料箱取物递人吞吐 +85%、成功率 **80%→98%**（不良失败降十倍）；双臂料箱搬运吞吐翻倍以上、成功率 **78%→99%**，均只需数天机器人时间。两个超预期发现：只对任务最难部分做 RL 能改善整任务、单物体训练能提升未练习物体的技能；仿真与真机训练曲线高度相关，真机正沿通往仿真 100% 成功率的同一轨迹爬升。
  > 💡 「真机 RL 而非仿真」是最反主流的选择——没有 sim-to-real gap，且训练循环与未来客户现场的持续学习循环相同；「训练最难的部分改善整个任务」则意味着 RL 可以像补丁一样局部施加，工程成本大降。若真机曲线确实沿仿真轨迹走向 100%，工业部署的可靠性门槛第一次有了可预测的抵达路径。
   - 来源: [Humanoid](https://thehumanoid.ai/technology/kinetiq-ascend/) | [@thehumanoidai](https://x.com/TheHumanoidAI/status/2105703276884971852)

**SemiAnalysis 估算：英伟达 Rubin 计算裸片中 HBM4 控制器与 PHY 占约 16%**
- SemiAnalysis 估算，英伟达 Rubin 计算裸片中 HBM4 控制器与 PHY 大约占据 16% 的面积，意味着大量先进制程硅被用于与内存通信而非计算本身。该机构表示数据来源于英伟达。
  > 💡 若 16% 的估算成立，说明 HBM 接口已成为先进制程最大的非计算开销之一；这对存储带宽、功耗与裸片良率的优化提出极高要求，也意味着任何 HBM 供应商在英伟达产品中的价值比重都在结构性上升。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2105771525605351710)

**哈佛物理学家发文「Claude 形状的科学」：三个月 18 个领域 36 篇稿件的科研流水线**
- 哈佛物理学家 Matthew Schwartz 在 Anthropic 科学博客撰文，提出科学家与 LLM 之间存在「阻抗失配」：像对待人类合作者那样使用模型并非发挥其科学所长的最佳方式，应转而寻找「Claude 形状的问题」。他为此构建了定量科学精确计算工具包 BootLoops（开源 harness），Claude 借它把数理方法迁移到生态学、群体遗传学等十几个领域——例如解出生态学中悬置 20 年的 Etienne 方程，证明巴拿马 Barro Colorado 岛树种更替速度是中性理论允许值的 **4.5 倍**；分析 1000 Genomes 项目 **57 亿对**突变并找到基因转换的证据；三个月内产出 36 篇稿件、覆盖 18 个领域、与 19 位专家合作（约 400 个候选问题中筛出）。他强调技术正确不等于科学有趣，仍需领域专家掌舵——「品味」暂时无法外包。
  > 💡 「Claude 形状的问题」给出了 AI 科研的第三种叙事：既不是替代科学家、也不是超级大脑解千禧难题，而是自动填充人类知识「凸包」的中间地带——各领域都够得着、但没有人真正去做的计算；三个月 36 篇稿件的产能，也第一次让「品味与判断力」成为科研中最稀缺的供给。
   - 来源: [Anthropic](https://www.anthropic.com/research/claude-shaped-science) | [@AnthropicAI](https://x.com/AnthropicAI/status/2105733864152858919)

**Artificial Analysis 为编码智能体指数新增安全拒绝与回退模型报告**
- Artificial Analysis 在 Coding Agent Index 中新增安全拒绝报告，展示拒绝何时发生（仅由任务提示触发，还是智能体已开工后在任务中途触发）以及拒绝后回退到哪个模型。数据显示 Claude Code 配 Sonnet 5.5（max）目前指数排名第一，其安全拒绝率 **4.5%**，约为 Claude Code 配 Opus 5.5（8.9%）的一半；Sonnet 5.5 约 **94%** 的拒绝发生在首轮之后，拒绝后几乎总是回退到 Opus 4.8。不同配置的回退模式各异：Fable 5.1 下 Claude Code 主要回退 Opus 4.8，而 Opus 5 在 Devin Fusion 的回退中占比大得多。AA 提醒安全与回退行为由厂商配置、可能随时间变化。
  > 💡 把「拒绝率」和「回退链路」做成公开可查的维度，等于给智能体的安全层加上了可比较的仪表盘——用户第一次能看见安全策略的真实运行时行为而非宣传口径；这也把各家 fallback 策略的差异（回退给谁、何时回退）摆上了竞争桌面。
   - 来源: [@ArtificialAnlys](https://x.com/ArtificialAnlys/status/2105755934253568428)

**Isomorphic Labs 发文：AI 制药不再是假设，设计引擎数天完成数年分子搜索**
- Isomorphic Labs  CEO Max Jaderberg 发长文回顾公司五年进展：2021 年创立时 AI 制药还只是假设，如今其药物设计引擎 IsoDDE 已在分子设计上超越现有深度学习与行业标准计算方法。核心展示：理论小分子化学空间约 10^60，传统高通量筛选需数月至数年评估固定化合物库、再经多年迭代优化，而其设计智能体在输入设计规格（靶点、分子类型、选择性、溶解度等要求）后 **2-4 天**内即可在计算机上完成分子搜索、推进多目标 Pareto 前沿，实验验证显示智能体设计的分子成功调控靶点且性质良好。公司称已在他人长期挣扎的问题上找到功能分子、只需合成极少量分子即可获得更好的实验结果，临床前数据正推进临床开发。
  > 💡 从「AlphaFold 预测结构」到「设计智能体在化学空间里自主搜索」，AI 制药的主语正在从工具变成引擎；「合成一小撮分子、实验一次过」的叙事若能被第三方重复验证，药物发现的瓶颈将从湿实验产能转移到设计规格与靶点选择——这正是 Isomorphic 想占住的位置。
   - 来源: [Isomorphic Labs](https://www.isomorphiclabs.com/articles/building-a-new-path-to-make-medicines-with-ai) | [@maxjaderberg](https://x.com/maxjaderberg/status/2104959165277892780)

**OpenAI 发布「新经济」系列随笔首篇：天才的永恒互补是执行**
- OpenAI 上线新平台发布独立视角探讨 AGI 未来的系列随笔，首篇《The Eternal Complement》提出：前沿智能与实现想法的能力互为互补品——维持摩尔定律所需的研究者已达 1970 年代初的 18 倍以上，全经济研究投入九十年间增长 23 倍而研究生产率下降 41 倍，「执行」正成为进步的瓶颈。文章给出两种文明图景：「深度的文明」里超级智能以极致节俭的方式咨询现实（仿真加精准实验）推进知识；「宽度的文明」里对新证据的需求压倒一切效率、物理扩张成为知识引擎——届时超级智能的超能力可能不是天才而是「甘当官僚」，几乎全部机器智能被用于做无聊而非聪明的事。作者认为人类在「品味」与创意多样性上仍保有位置。
  > 💡 这篇随笔把「创意易得、执行稀缺」的当下与两种终局图景串了起来，是对「AI 只会生成想法」这一焦虑的正面回应：无论走向深度还是宽度，执行与协调都长期有价；真正的分水岭在于自然界的复杂度是否逼着文明不断「变宽」。
   - 来源: [OpenAI](https://openai.com/index/the-eternal-complement)

---
*更新时间: 2026-10-03 00:21*