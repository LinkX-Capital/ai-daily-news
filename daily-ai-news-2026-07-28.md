## 07月28日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 15 条

---

## 要点汇总

- 模型前沿：Kimi K3开源发布：2.8T参数MoE模型主打长上下文与原生视觉; NVIDIA 发布 Cosmos-H-Dreams 用于手术机器人实时生成式仿真
- 产业动态：特朗普政府接近敲定AI自愿框架，要求头部公司在发布前沿模型前提交政府审阅
- 算力追踪：长鑫存储科创板首日股价飙升472%，市值跻身A股最大; 中国国资背景企业开始量产浸没式DUV光刻机; 云厂商测试显示Nvidia Rubin服务器部署难度低于上代Blackwell; Nvidia向韩国Naver投资10亿美元，扩建AI数据中心; SemiAnalysis称其深度报告早已预判长鑫存储崛起
- 初创&融资：Nvidia对Ilya Sutskever联合创办的Safe Superintelligence进行数十亿美元投资; Antares融资4.7亿美元为美国空军基地建设小型模块化核反应堆; 铭镓半导体完成超1.5亿元Pre-B轮融资，押注磷化铟与氧化镓产线; Thea Energy获ARPA-E 2000万美元资助，扩大高温超导磁体产能; 机器人初创公司 Tacta 展示灵巧手与数据采集手套
- 研究关注：论文提出 JarvisHub：面向长时程多模态创作的画布原生 Agent 框架; 论文重新审视在线策略扩散蒸馏中的免分类器引导

---

## 📖 详细参考

### 模型前沿
**Kimi K3开源发布：2.8T参数MoE模型主打长上下文与原生视觉**
- Kimi K3是一套总参数2.8万亿、激活1040亿参数的Mixture-of-Experts模型，原生支持视觉能力与百万token上下文窗口。该模型基于Kimi Delta Attention与Attention Residuals两项结构改造，叠加Stable LatentMoE（每个token从896个路由专家中激活16个）以及训练与数据流程优化，整体Scaling Efficiency较K2提升约2.5倍。后训练阶段覆盖通用、Agent与编程三类强化学习，并设置多档推理强度。论文指出，尽管Kimi K3总体表现仍落后于Claude Fable 5与GPT-5.6 Sol，但在该团队评测范围内一致优于其他开源与闭源模型；团队同时开源了Kimi K3完整模型权重。
  > 💡 K3在2.8T规模下以更低激活量逼近前沿闭源模型，配合开源权重，对中美前沿模型竞争与开源生态都是一次显著拉扯；其SMR+长上下文Agent RL的工程叙述也指向Kimi在系统级协同设计上的延伸。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2607.24653)

**NVIDIA 发布 Cosmos-H-Dreams 用于手术机器人实时生成式仿真**
- NVIDIA 在 HuggingFace Blog 发布 Cosmos-H-Dreams，将实时生成式仿真引入手术机器人方向。可用证据仅含标题，未提供方法、适用场景或支持硬件的进一步描述。
  > 💡 Cosmos 系列从自动驾驶与通用机器人扩展到手术机器人，反映 NVIDIA 在物理 AI 仿真层面正向高合规要求的医疗场景延伸，但具体技术细节仍待后续披露。
   - 来源: [HuggingFace Blog](https://huggingface.co/blog/nvidia/cosmos-h-dreams)

### 产业动态
**特朗普政府接近敲定AI自愿框架，要求头部公司在发布前沿模型前提交政府审阅**
- 据三位知情人士透露，特朗普政府即将敲定一份AI自愿框架，要求AI公司在向公众发布最强模型之前先提交给政府。白宫国家网络主任办公室约两周前将草案分发给OpenAI、Anthropic与Google，三家公司联合提交了修改意见。6月初由特朗普签署的AI行政命令设定了8月1日为框架落地期限，该框架目标是为能够快速发现网络漏洞的强AI建立更正式的发布流程。
  > 💡 若按行政命令时点8月1日落地，这是美国首次把"前沿模型发布前通报"从行业承诺抬升为可追溯的政府流程，配合OpenAI/Anthropic/Google联合提意见，三家头部公司在合规通道里的话语权也将进一步显化。
   - 来源: [The Information](https://www.theinformation.com/articles/trump-administration-nears-ai-framework-open-source-questions-loom)

### 算力追踪
**长鑫存储科创板首日股价飙升472%，市值跻身A股最大**
- 中国头部存储芯片厂商长鑫存储（CXMT）周一在上海上市首日股价上涨472%，市场押注其将受益于AI驱动的存储需求增长。开盘价对应市值约3.3万亿元人民币（约4870亿美元），使其成为A股最大上市公司，盘中涨幅一度扩大至535%。
  > 💡 存储芯片在AI推理与训练工作负载中的需求扩张，使CXMT获得与海外巨头并列的资本市场背书，A股估值锚点出现变化。
   - 来源: [The Information](https://www.theinformation.com/briefings/china-memory-chipmaker-cxmt-soars-472-shanghai-debut)

**中国国资背景企业开始量产浸没式DUV光刻机**
- 一家中国国资背景的上海企业开始量产芯片制造关键设备之一的浸没式深紫外（DUV）光刻机，这是北京推动降低对海外芯片制造技术依赖过程中的重要进展。知情人士透露，该设备与台积电等芯片厂商所用机型属同一类别。
  > 💡 DUV本地量产标志着中国半导体设备国产化从外围环节向核心光刻环节延伸，但能否达到先进制程量产良率仍需后续验证。
   - 来源: [The Information](https://www.theinformation.com/articles/china-starts-mass-producing-homegrown-duv-chipmaking-tools-advance-local-chip-industry)

**云厂商测试显示Nvidia Rubin服务器部署难度低于上代Blackwell**
- 据多家采购Nvidia AI服务器云厂商的高管透露，基于初步测试，他们预期即将推出的Vera Rubin服务器机架在安装上比2025年的Grace Blackwell机架容易得多。Grace Blackwell部署期间，Nvidia头部客户曾因多项新技术而遭遇严重困难，安装延迟直接影响AI算力上线与数据中心利润率。
  > 💡 Rubin若能兑现部署便利承诺，将缓解云厂商在Grace Blackwell周期中遭遇的算力上线瓶颈，影响后续订单节奏与机柜密度决策。
   - 来源: [The Information](https://www.theinformation.com/articles/nvidias-new-rubin-servers-offer-early-relief-cloud-providers)

**Nvidia向韩国Naver投资10亿美元，扩建AI数据中心**
- Nvidia宣布将向韩国互联网巨头Naver投资10亿美元，用于扩大该国数据中心基础设施。资金将支持Naver将其AI数据中心规划容量从55兆瓦提升至200兆瓦，加拿大投资公司Brookfield计划另投最多90亿美元。
  > 💡 Nvidia联合Brookfield以股权融资替代部分自建投入，锁定韩国主权云客户长期算力订单，亚太区域数据中心资本结构正变得复杂化。
   - 来源: [The Information](https://www.theinformation.com/briefings/nvidia-invest-1-billion-south-koreas-naver-ai-data-center-expansion)

**SemiAnalysis称其深度报告早已预判长鑫存储崛起**
- SemiAnalysis 在社交平台发文回应讨论，表示团队在上月的深度报告中已经拆解长鑫存储（CXMT）从奇梦达（Qimonda）遗产中成长为全球第四大 DRAM 厂商的技术路径，并强调「我们早预见到了这一点」。该推文重申了对长鑫存储技术演进的关注，但未给出新的事实数据。
  > 💡 SemiAnalysis 选择在公开讨论中以「早已预判」的方式重申上月长鑫存储报告，意在巩固其半导体产业深度研究的品牌定位，并非新事件本身。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2081749013339017391)

### 初创&融资
**Nvidia对Ilya Sutskever联合创办的Safe Superintelligence进行数十亿美元投资**
- Nvidia对由前OpenAI首席科学家Ilya Sutskever联合创办的AI实验室Safe Superintelligence进行了"实质性"投资。双方周一宣布，该笔投资将使这家初创公司在未来一年将算力资源扩大为原先的数倍（最高10倍）。双方未披露投资金额，但金额达到"数倍"美元量级。
  > 💡 算力供应商直接投资超智能对齐实验室，反映Nvidia通过资本绑定加深对前沿模型公司的算力供给关系，同时押注多路线研究生态。
   - 来源: [The Information](https://www.theinformation.com/briefings/nvidia-makes-multibillion-dollar-investment-ilya-sutskevers-safe-superintelligence)

**Antares融资4.7亿美元为美国空军基地建设小型模块化核反应堆**
- 核能初创公司Antares Nuclear宣布完成4.7亿美元C轮融资，用于为美国空军基地建设小型模块化反应堆（SMR），单机功率在100千瓦至1兆瓦之间。本轮由Paradigm与Caffeinated Capital领投，Industrious Ventures、Point72 Ventures与Shine Capital跟投，包含3.7亿美元股权和1亿美元债权。Antares的演示堆Mark-0已于6月4日在Idaho National Laboratory达到临界，并入围五角大楼Advanced Nuclear Power for Installations项目，将在科罗拉多州与蒙大拿州空军基地测试SMR。Antares计划明年上线首座发电反应堆，2028年部署至美国军事设施。
  > 💡 AI数据中心驱动的电力需求已开始把核能初创的资金量级推高到与传统能源初创相当的水平，且直接服务于军用负荷，标志前沿算力需求正向高密度、独立电源方向外溢。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/27/antares-raises-470m-to-build-nuclear-reactors-for-the-u-s-military)

**铭镓半导体完成超1.5亿元Pre-B轮融资，押注磷化铟与氧化镓产线**
- 铭镓半导体专注于第四代半导体材料氧化镓、高频磷化铟晶体及大尺寸掺杂光学晶体等人工晶体材料的研发与生产。本轮Pre-B1与Pre-B2累计融资超1.5亿元人民币，由千曦资本、芯禾资本、安阳经开集团、粤科资本、天鹰资本及洪泰基金联合投资。资金将主要用于磷化铟（InP）多晶材料产能扩张、氧化镓中试产线建设以及上市筹备工作。
  > 💡 资金明确指向InP多晶与氧化镓中试两条产线，并首次把"上市筹备"写入资金用途，铭镓在第四代半导体这条尚处早期国产化的赛道上已开始向二级市场靠拢。
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14701354)

**Thea Energy获ARPA-E 2000万美元资助，扩大高温超导磁体产能**
- 聚变能源初创公司Thea Energy宣布获得美国能源部ARPA-E 2000万美元资助，用于扩大其模块化高温超导（HTS）磁体的制造能力。HTS磁体是磁约束聚变堆的关键部件，强磁场用于约束并压缩等离子体以达到聚变条件。Thea采用仿星器（stellarator）设计，通过减少磁体变体来压低成本：12块主磁体来自4种模板，超过300块小型调谐磁体完全相同并由软件单独控制。公司是资金最充裕的聚变初创之一。
  > 💡 ARPA-E资助从概念走向制造环节，配合"软件控制磁体阵列"这种降本思路，HTS磁体这一聚变产业链最贵环节正在出现可量产路径，相关供应链值得后续跟踪。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/27/thea-energy-lands-20m-federal-grant-to-build-its-magnets-for-fusion-reactors)

**机器人初创公司 Tacta 展示灵巧手与数据采集手套**
- 成立于约三年前的 Tacta Systems 已累计融资 7500 万美元，长期保持低调。该公司将三指灵巧手安装在外采工业机械臂末端并置于可移动底座上，而把类人机器人本体的其他部分留给其他公司。Tacta 同时在开发面向真人的数据采集手套，由佩戴者在工作或居家执行任务时记录手部动作信息，用以训练人形机器人的物理 AI 模型。
  > 💡 Tacta 押注「人手即机器人最难替代的部分」，并将灵巧手与数据采集手套并列推进，意味着物理 AI 的竞争焦点正从整机系统转向高质量人类操作数据的获取渠道。
   - 来源: [The Information](https://www.theinformation.com/articles/robotics-startup-tacta-shows-hand-glove)

### 研究关注
**论文提出 JarvisHub：面向长时程多模态创作的画布原生 Agent 框架**
- 论文指出创意工作需要参考、草稿、替代方案、修改、失败尝试、版本关系、工具动作与人类反馈等持续演化的项目状态，而现有 prompt、对话或节点式生成系统往往丢弃中间上下文或依赖线性会话。作者提出 JarvisHub，将可编辑画布同时作为用户工作区、Agent 外部记忆、动作空间和共享项目状态，并以类型化画布节点与链接表示多模态资产及其依赖、版本与反馈。其三层架构由画布状态、协议桥接和 Agent 运行时分组成，使 Agent 能在可检视、可编辑的创意状态内执行操作。
  > 💡 JarvisHub 把「画布」提升为 Agent 的核心状态表征，呼应了工业界正在出现的 Agent 辅助创意系统走向，标志着多模态 Agent 研究从孤立工具调用迈向持续可监督的创作自动化。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2607.23588)

**论文重新审视在线策略扩散蒸馏中的免分类器引导**
- 论文分析在线策略蒸馏（OPD）在免分类器引导（CFG）下的行为，指出将引导速度直接对齐师生预测在分支层面存在欠定问题，正负分支误差可在引导预测中相互抵消。作者据此提出「负分支不对称（NBA）」失败模式：当教师负分支保留学生无法获取的特权信息时，联合误差下降不再成立，引导目标反而出现正分支误差下降、负分支误差上升的对抗性动态。为缓解 NBA，论文引入分支感知的「正方向匹配（PDM）」目标，分别约束正预测和 CFG 条件方向，并在密集到稀疏的视频控制任务中验证其对推理引导尺度更稳健。
  > 💡 PDM 把 CFG 的师生匹配拆解到正负分支层面，揭示了扩散蒸馏中常被忽视的负分支不对称问题，为后续视频控制等对引导尺度敏感的任务提供了更可靠的蒸馏目标。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2607.24731)


---
*更新时间: 2026-07-28 17:12*