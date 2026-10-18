## 10月19日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 15 条

---

## 要点汇总

- 产业动态：vLLM v0.32.0 发布：合并 814 个 commit、新增 /v1/systemone 结构化决策端点; Anthropic 承诺将部分股份注入新设公益实体，起始 5% 并设增值阶梯追加机制
- 算力追踪：vLLM 展示 Kimi K3 在 GB300 NVL72 上的 DSpark 解码方案：batch 1 达 842 tokens/s; 报道称 Neocloud 行业洗牌临近，英伟达持仓面临较大风险敞口; 报道称微软退出 Nscale 英国数据中心项目，因电力接入延迟导致上线受阻
- 初创&融资：具身大脑研发商格物通智完成近亿元天使轮融资，绑定真实产业场景的灵巧操作路线; 企业 AI 平台 RapidCanvas 完成 2900 万美元 B 轮融资，祥峰投资领投
- 研究关注：CarryOn：用双循环 Harness 给冻结 VLA 补齐个性化与安全监督，把违规率压至 6.1%; MJev-Spatial：用原生注意力匹配重写空间推理，推理 Q12 跑出基座 5.6 倍速度并拿下 12 项基准 7 项第一; Waypoint-OPD：用 RL 早期与晚期策略漂移方向一致性，挑选性蒸馏 RL 教师前后的策略偏移; PAIR：在 VLA 内部搭一座"感知-动作"桥，把 LIBERO-Plus 成功率从 59.1% 抬到 64.2%; 浙大提出具身智能体长程记忆基准：看见不等于记住
- X讨论：SemiAnalysis 引述：GLM 5.3 全部由上一代后训练得到，后训练 GPU 效率高于从头预训练; The Information：Meta、Tesla、Netflix 三季度业绩本周集中发布，Meta 周三率先亮相

---

## 📖 详细参考

### 产业动态
**vLLM v0.32.0 发布：合并 814 个 commit、新增 /v1/systemone 结构化决策端点**
- vLLM 正式发布 v0.32.0 版本，共合并 814 个 commit，由 363 位贡献者参与，其中 121 位为首次贡献者。新版本新增 /v1/systemone 结构化决策端点与通用 hf tool/reasoning 解析器，并全面铺开低精度 KV 缓存（SM8x/90/12x 上的 NVFP4、GLM-5.x 默认 FP8 KV、ROCm 上的 4-bit KV）。Model Runner V2 在 ROCm 上成为默认，包含 GPU n-gram 推测解码、Elastic EP 与 PP+CP for MLA 等能力，同时引入预编译 kernel 下载以加快启动与服务部署。
  > 💡 低精度 KV 从单一模型选项升级为跨硬件默认，意味着开源推理栈正在把显存压缩变成新基线；/v1/systemone 端点把 agent 决策路径标准化进推理服务本身，对智能体框架接入方式也会产生连锁影响。
   - 来源: [@vllm_project](https://x.com/vllm_project/status/2111814711956168760)

**Anthropic 承诺将部分股份注入新设公益实体，起始 5% 并设增值阶梯追加机制**
- Anthropic 宣布将把公司部分股份投入新成立的 Anthropic Public Benefit Fund，后者为 Anthropic 全资拥有、专门服务公共利益的实体。公告指出，基金初始将持有 Anthropic 5% 的股份，并约定在 Anthropic 价值较既定基线每增长 50% 时，可经董事会裁量再追加最多 2%。按上述机制累算，Anthropic 最终可能向该基金投入约 20% 的股份。
  > 💡 采用「股份承诺 + 增值阶梯」结构而非一次性捐赠，意味着 Anthropic 将长期估值上行的一部分让渡给公益基金；20% 的累计上限为公司增长保留了显著弹性，同时把公益承诺与未来市值表现绑定，区别于传统科技公司的固定捐赠做法。
   - 来源: [@anthropicai](https://x.com/AnthropicAI/status/2111881963657412903)

### 算力追踪
**vLLM 展示 Kimi K3 在 GB300 NVL72 上的 DSpark 解码方案：batch 1 达 842 tokens/s**
- vLLM 项目在 NVIDIA GB300 NVL72 上为月之暗面 Kimi K3 decode 提供了一条统一的 CuTe DSL 解码路径，在多个测试配置下 decode 吞吐提升 1.5–2 倍。Kimi K3 在 batch 1 下达到 842 tokens/s。该路径同时融合 attention、MoE 与通信 collective，并在 SemiAnalysis AgentX 负载上将 P90 交互性最高提升 1.8 倍。
  > 💡 同一条 fused kernel 同时吃下 attention、MoE 通信与低延迟交互三项指标，意味着 K3 在 GB300 上的解码瓶颈已经从显存带宽移到调度与集合通信，对后续 Blackwell 平台上的长上下文 MoE 推理具备复用价值。
   - 来源: [@vllm_project](https://x.com/vllm_project/status/2111637219647840611)

**报道称 Neocloud 行业洗牌临近，英伟达持仓面临较大风险敞口**
- The Information 报道指出，AI 数据中心建设引发投资者对初创云厂商（neocloud）风险的担忧，相关风险包括 CoreWeave 等公司的高债务杠杆，以及 Firmus、Nscale 在缺乏业绩记录时仍尝试推进 IPO。Firmus 已在上周撤回上市计划，CoreWeave 及同业公司股价当周下跌约 20%，连 Oracle 等体量更大的 AI 云厂商也受到波及。数据中心与 neocloud 高管向 The Information 表示，即便英伟达提供资金或回购承诺，AI 云厂商的市场容量依然有限。
  > 💡 这是首次把英伟达的潜在损失放到标题层处理，意味着 Neocloud 的杠杆不只是这些公司自己的问题，也开始反向冲击英伟达的资本策略与估值叙事。
   - 来源: [The Information](https://www.theinformation.com/articles/neocloud-shakeout-looms-nvidia-lot-lose)

**报道称微软退出 Nscale 英国数据中心项目，因电力接入延迟导致上线受阻**
- The Information 报道称，Nscale 的一位发言人确认，微软已退出 Nscale 在英国为其承建的一座拟建数据中心，原因是该云厂商在获取电力以使站点上线方面遭遇延期。报道指出，这一取消很可能影响 Nscale 原定本月推进的 IPO 计划，眼下投资者正担心 AI 云厂商能否足够快地形成营收以偿还债务，Firmus 上周也已撤回上市。
  > 💡 在‘Anthropic 增速放缓’与 Neocloud 洗牌叙事之外，这是首个具体到某一笔订单被砍的案例，说明电力瓶颈正直接传导到 Neocloud 与其大客户之间的合同关系上。
   - 来源: [The Information](https://www.theinformation.com/briefings/microsoft-pulls-nscale-u-k-data-center-following-delays)

### 初创&融资
**具身大脑研发商格物通智完成近亿元天使轮融资，绑定真实产业场景的灵巧操作路线**
- 格物通智是一家具身大脑研发商，面向真实产业场景研发自进化的灵巧操作智能，依托触觉-视觉为主的多模态数据真实闭环构建"物理反演世界模型+PSI物理自进化"技术体系。格物通智近日已完成近亿元天使轮融资，投资方包括匹克投资、鸿富资产、杭州资本、杭州人才集团、某省级具身产投及多家头部上市公司。
  > 💡 天使轮就引入省级具身产投与多家上市公司，融资背景偏产业资本而非纯财务 VC，说明格物通智切入具身大脑的路径是从工厂/产线真实工况出发；后续能否在公开 benchmark 或真实产线数据上兑现"越用越适配"的进化叙事，是验证这套技术体系的关键。
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14706175)

**企业 AI 平台 RapidCanvas 完成 2900 万美元 B 轮融资，祥峰投资领投**
- IT 桔子报道，企业 AI 平台提供商 RapidCanvas 近日完成 2900 万美元 B 轮融资。本轮由祥峰投资 Vertex Ventures 领投，钛 Ventures Titanium Ventures、Valley Capital Partners、Peak XV Partners、Accel Partners、Hitachi 参投。RapidCanvas 面向企业用户提供 AutoAI 平台，主打无需专业数据科学或编码能力即可从原始数据走到可解释、可操作的预测。
  > 💡 AutoAI / 无代码建模平台的赛道正进入 B 轮整合阶段，老牌 VC 与 Hitachi 等产业资本同时出现，说明该方向被同时视为财务投资和「低门槛企业数据资产化」的入口；多轮老股东跟投也表明此前轮次的商业化验证已获认可。
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14706176)

### 研究关注
**CarryOn：用双循环 Harness 给冻结 VLA 补齐个性化与安全监督，把违规率压至 6.1%**
- 论文提出 CarryOn，一个围绕冻结 VLA 策略构建的双循环 harness。规划循环维护用户级与场景级持久上下文，并基于新观测持续落地、通过交互修订；执行循环主动监督策略推演，屏蔽预测到的危险接触，并在执行失败时调用可复用控制恢复技能。在真实机器人与仿真中，CarryOn 可在不同用户与场景之间分派偏好一致的子任务，把已做安全微调的 VLA 违规率由 52.6% 降至 6.1%，并在恢复技能被复用时把恢复成功率从 13% 提升到 80%。
  > 💡 CarryOn 的核心思路是把"个性化 + 安全恢复"做成外挂式 harness，而不是改动 VLA 本身权重，这让任何冻结的通用 VLA 都能即插即用升级到家庭助手级别的可靠性；恢复技能池的复用机制是关键工程杠杆，意味着每次失败都会反向沉淀技能库，长期来看比单纯强化学习更接近可部署的家庭服务方案。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.21453)

**MJev-Spatial：用原生注意力匹配重写空间推理，推理 Q12 跑出基座 5.6 倍速度并拿下 12 项基准 7 项第一**
- 论文提出 MJev-Spatial，一个用统一分类框架处理三类空间理解任务的 System 1 多模态决策模型，把候选选项当作类、用 backbone 预训练的 query/key 投影打分，不新增参数；推理时每条分类决策只需一次前向、不生成回答 token。基于 Qwen3.5-4B、用 1230 万条空间问答对训练后，MJev-Spatial 在 8 个模型中取得 65.64% 的最高总分，在 12 项基准中的 7 项排名第一，并全面超越其自回归基座，推理速度为最快自回归基线的 2.5 倍、基座的 5.6 倍。
  > 💡 把空间推理从自回归文本生成改造成分类任务，等于把"输出空间紧凑、计算却花在逐 token 解码"的低效环节直接砍掉；该方法证明 VLM 骨干的注意力本身就能做"分类式推理"，对需要在毫秒级交互中回答距离/方位/放置点的具身与机器人场景，是比堆参数更划算的工程方向。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.22276)

**Waypoint-OPD：用 RL 早期与晚期策略漂移方向一致性，挑选性蒸馏 RL 教师前后的策略偏移**
- 论文提出 Waypoint-OPD，一种引导学生蒸馏的策略偏移蒸馏方法。该方法通过同一 RL 训练中一份教师中间 checkpoint，比较早期与晚期相对动作偏好的方向一致性；当两者方向不一致时，抑制端点偏移的传递；相比仅用端点偏移的方案，仅多一次冻结教师打分前向。论文以 RL 训练后的 Qwen3-4B 为教师，用 Qwen3-8B/14B/30B-A3B 做学生，在数学与代码推理 6 个领域-学生设置上，Waypoint-OPD 都取得蒸馏方法中最高的领域平均分。
  > 💡 该工作把"RL 是否真的进步"从单点比较扩展为过程性诊断——同一份端点偏移可能来自方向相反的早期/晚期漂移叠加；用一致性门控过滤掉互相抵消的"伪进步"，相当于给学生一个更干净的 RL 监督信号，这对把 RL 收益稳定迁移到更大体量模型具有直接工程价值。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.21601)

**PAIR：在 VLA 内部搭一座"感知-动作"桥，把 LIBERO-Plus 成功率从 59.1% 抬到 64.2%**
- 论文提出 PAIR，一个面向连续动作 VLA 的感知-动作表示桥接框架。训练时由 Masked Action Autoencoder 将专家动作块编码为与 horizon 对齐的 Action Latent Tokens，Bridge Module 从当前视觉-语言表征抽取任务相关特征并对齐到这些 Token，形成 Bridge Tokens，再投入 Action Expert 精炼；推理时去掉 autoencoder，仅由当前观测与指令生成 Bridge Tokens。论文在 LIBERO、LIBERO-Plus 与 CALVIN ABC-D 上验证，PAIR 使 VLA-Adapter 在 LIBERO-Plus 成功率从 59.1% 升至 64.2%，在 CALVIN 把平均完成序列长度由 4.42 提升到 4.53；在 7 项真实任务中使 OpenVLA-OFT 成功率从 51.4% 升至 65.0%。
  > 💡 PAIR 的关键是把"从描述场景到生成动作"的过渡显式化为一个共享中间表示，让 VLA 不必只靠最终动作损失来间接对齐两种空间；这种中间表征对长 horizon、连续动作的家用/工业操作尤其重要，因为这类任务的成败往往取决于第一步动作分布是否落在可执行区域。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.09016)

**浙大提出具身智能体长程记忆基准：看见不等于记住**
- 新智元报道，浙江大学团队提出面向具身智能体的长程记忆基准，指出视觉感知并不等同于长期记忆能力。该工作专门针对智能体在长程任务中需要调用与更新历史观测的场景构建评测。由于来源仅给出标题，相关方法细节、评测指标与具体得分数据无法核验。
  > 💡 长程记忆是当前具身智能体从短任务演示走向真实家庭/工厂部署的关键瓶颈之一；建立独立基准比单纯堆叠参数更能暴露现有模型的真实短板，但具体覆盖范围与可复现性仍需等论文披露后才能判断。
   - 来源: [新智元](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA%3D%3D&mid=2652735627&idx=3&sn=2195898b4588173b111e6ffc13732156)

**OneWM：把世界建模与动作生成统一在因果训练框架中，互训在 LIBERO 等基准上互相增益**
- 论文提出了 OneWM 框架，把动作同时当作世界预测的条件和策略学习的目标，在共享的视频-动作架构下做统一因果训练。论文在 LIBERO、LIBERO-Plus 和 RoboCasa365 等具身测试平台上评估了策略学习与世界建模，并补充了真实世界策略实验。结果显示，学习指定动作带来的视觉后果能提升策略在不同场景下的表现与泛化，而动作学习又在同一架构下提升了多视角世界预测的保真度。
  > 💡 世界模型与策略模型长期被视为两条独立路线，本工作在统一架构与因果训练下让二者互为监督信号，给数据紧缺的具身场景提供了一条「用动力学监督动作、用动作监督动力学」的可行路径；但增益幅度与对真实硬件的迁移效果仍取决于 LIBERO 系基准之外的真实落地表现。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.21095)

### X讨论
**SemiAnalysis 引述：GLM 5.3 全部由上一代后训练得到，后训练 GPU 效率高于从头预训练**
- SemiAnalysis 在 X 平台表示，GLM 5.3 全部由对前代模型进行后训练得到，这对团队是一次重要提醒。帖文进一步指出，后训练在 GPU 效率上远高于从零做预训练，许多公司无力从头训练模型，但拥有专有数据，因此可以通过自行后训练在效果上追平部分闭源模型。
  > 💡 SemiAnalysis 把这一次迭代作为案例对外表态，相当于把‘后训练即迭代主线’这一策略从厂商内部叙事升级到行业判断，会进一步压缩纯预训练玩家的差异化空间。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2111596468528087078)

**The Information：Meta、Tesla、Netflix 三季度业绩本周集中发布，Meta 周三率先亮相**
- The Information 报道，Meta Platforms 将在本周三率先公布 9 月季度业绩，领先 Google、Microsoft、Amazon 一周，Apple 更要等到 11 月 2 日。报道提到，Meta 此举意在争取更大的市场注意力，但上周五市场对 AI 扩张的担忧再次升温，多数科技股承压。截至上周，Meta 此前因自家 Muse 个人智能体与新发布的 Muse Wonder AI 模型获得华尔街积极情绪，本周业绩将再次考验投资者对其高额 AI 投入的态度。
  > 💡 Meta 把披露时间前移一周，本质上是在市场情绪转弱时抢先掌握叙事窗口；但 AI 支出规模已成为新的争议焦点，财报中关于资本开支与 AI 产品落地节奏的口径将直接决定短期股价是否能延续此前由 Muse 系列带动的乐观预期。
   - 来源: [The Information](https://www.theinformation.com/articles/meta-tesla-netflix-q3-updates-coming-week)


---
*更新时间: 2026-10-19 06:45*