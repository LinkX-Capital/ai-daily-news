## 07月04日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 产业动态：阿里巴巴禁止员工在工作电脑使用Claude; Dune键盘设备可充当会议控制器，支持Claude生成自定义脚本
- 初创&融资：Kling AI完成约19B元融资，投前估值达150亿美元
- 研究关注：SARL：在语言提示空间做强化学习，VLA机器人任务成功率提升至约80%; WLA-0：统一世界建模、语言推理与动作生成，2B参数实现40ms推理; 量化推理模型过度思考研究：CoT长度降低12-23%，错误最高减少58%; 异构PD推理设计空间：拆解跨硬件KV缓存的表示、放置与归属

---

## 📖 详细参考

### 产业动态
**阿里巴巴禁止员工在工作电脑使用Claude**
- 第一财经援引阿里内部人士称，因近期 **Claude Code 被曝存在植入后门的安全风险**，Alibaba 已将其列入高风险软件名单，并将自 **7 月 10 日**起全面禁止内部员工在办公环境下使用 Claude Code，同时推荐使用自研智能体编程平台 **Qoder** 作为替代方案。文中称，阿里此前鼓励员工使用海内外 AI 工具并报销外部模型成本，Claude Code 是程序员高频编码工具；但 Anthropic 单方面指控阿里开展模型蒸馏攻击、针对性标记和封禁中国用户，以及退款和申诉渠道问题，让研发数据面临泄露与溯源风险。第一财经还援引 Forrester 副总裁兼首席分析师戴鲲观点称，该事件会加速国产 AI Coding 工具在大型企业中的渗透；阿里公布 Qoder 截至 2026 年 5 月全球用户超过 **500 万**，已覆盖从需求分析到代码部署的端到端自主开发流程。
  > 💡 这不是单一工具替换，而是海外 AI coding 工具从“员工自选效率工具”进入集团级风控清单的信号：安全合规、模型供应链和云厂商 token 收入会同时推动国产编码 Agent 在大厂内部获得默认分发位。
   - 来源: [The Information](https://www.theinformation.com/briefings/alibaba-bans-employees-using-claude) | [第一财经](https://mp.weixin.qq.com/s/PPkiVjKCPMZRQQuwAJRFPQ)

**Dune键盘设备可充当会议控制器，支持Claude生成自定义脚本**
- Project Mirage 推出的 **Dune** 是一款插入 MacBook USB-C 口的三键铝制键盘，可按当前应用自动切换按键语义：在会议应用中控制麦克风、摄像头和窗口置顶，在 Excel / Sheets 中执行复制、粘贴、撤销，在 Chrome 中刷新、跳转地址栏和粘贴；开发者也可在 VS Code 或 GitHub 中绑定合并、批准、关闭 PR 等操作。设备支持 **M2 Air 或更新机型、M1 Pro 或更新机型**，系统要求 **macOS 15 Sequoia 或更高版本**，无电池、由 MacBook 供电；配套 App 可同步日历并在会议前提供加入、忽略或发送迟到消息。Dune 支持按应用或全局配置快捷键、命令、链接和 **Python 脚本**，并集成 Claude Desktop：用户用自然语言描述想要的快捷操作，Claude 可生成脚本并分配到对应按键。TechCrunch 称其当前售价 **119 美元**，intro 结束后标准零售价 **149 美元**。
  > 💡 Dune 的 AI 相关性不在三键硬件本身，而在把 Claude 生成脚本、应用上下文和实体快捷键绑定起来：Agent 工作流正在从屏幕内的软件按钮，延伸到可编程的物理输入设备。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/03/the-dune-keypad-device-can-be-your-meeting-controller-and-more/)

### 初创&融资
**Kling AI完成约19B元融资，投前估值达150亿美元**
- Kuaishou Technology 旗下 AI 视频业务主体北京可灵完成新一轮增资，初始融资约 **138 亿元人民币（约 20 亿美元）**，并与 **15 家额外投资方**签约追加 **52.24 亿元**，认购总上限为 **204.47 亿元（约 30 亿美元）**；交易前估值 **150 亿美元**，若全部资金到位，投后估值约 **180 亿美元**。融资完成后，Kuaishou 仍持有北京可灵约 **68.33%** 股权并继续并表，同时落地资产重组、独立员工股权激励计划、同股不同权治理结构和长期上市预期。极客公园援引公告称，可灵 2025 年全年收入约 **11 亿元人民币**，2025 年 12 月单月收入突破 **2000 万美元**，到 2026 年 3 月年化收入运行率升至 **5 亿美元**；但 2024 年净亏损 **5 亿元**、2025 年亏损扩大至 **19 亿元**，独立融资也承担了分担算力、研发和全球化投入压力的功能。投资方包括腾讯、Alibaba、Baidu 相关主体、地方国资、CPE、中信金石、红杉等；股权激励池合计占股 **15%**，CEO 盖坤个人获 **3%** 股权激励，且其股份最多可享受 **10 倍投票权**。
  > 💡 这轮融资不只是给 Kling AI 补充算力弹药，更是快手把 AI 视频业务从集团内部成本中心拆成独立估值主体：收入增长、亏损压力、股权激励和同股不同权同时出现，说明 AI 视频竞争正在从模型演示进入资本结构与组织机制的下半场。
   - 来源: [The Information](https://www.theinformation.com/briefings/kuaishou-announces-kling-ai-video-units-fundraising-15-billion-valuation) | [极客公园](https://mp.weixin.qq.com/s/pmvl7WPoSgKmGTseD8Egqg)

### 研究关注
**SARL：在语言提示空间做强化学习，VLA机器人任务成功率提升至约80%**
- UC Berkeley 的 Jagdeep Singh Bhatia、Andrew Wagenmaker、William Chen、**Sergey Levine** 提出 **Semantic Action Reinforcement Learning（SARL）**，解决通用 VLA 机器人策略在复杂长程任务中无法靠单一 prompt 激活正确技能组合的问题。传统 action-space RL 只能在固定 prompt 诱导出的动作分布附近微调，遇到预训练分布外任务时难以组合已有技能；SARL 将强化学习空间提升到 **language prompt space**，由 VLM 生成候选语义动作，再学习 semantic Q-function 选择能推进任务的 prompt。在 **4 个真实 WidowX 长程任务**和 **10 个 LIBERO-10 仿真任务**中，base policy 在多数任务接近 **0%** 成功率，SARL 经过 **60-100 个 online episodes** 后提升到约 **80%**。
  > 💡 把 VLA 的部署期学习从动作层迁移到语义提示层，说明机器人 foundation model 的在线适配可能更多依赖“选择和组合已有技能”，而不是重新学习底层控制。
   - 来源: [arXiv](https://arxiv.org/abs/2606.31958) | [@svlevine](https://x.com/svlevine/status/2073076767292813579#m) | [项目页](https://semantic-action-rl.github.io/)

**WLA-0：统一世界建模、语言推理与动作生成，2B参数实现40ms推理**
- 上海交通大学 DENG Lab 等提出 **World-Language-Action（WLA）** 模型，解决 WAM 推理慢、语义规划弱，而 VLA 缺少物理动态建模的问题。WLA 用自回归 Transformer 统一预测文本子任务、未来视觉状态和机器人动作，将未来状态拆成 **semantic-level textual intention** 与 **fine-grained physical dynamics**；World Expert 在训练阶段提供物理动态监督，推理时可关闭以避免显式生成未来图像带来的延迟。WLA-0 激活 **2B 参数**，在 RTX 5090 上单次推理约 **40ms**，RoboTwin 2.0 Clean 成功率 **92.94%**、LIBERO 平均 **98.6%**、RMBench **56.5%**；跨本体无动作标注视频也能让 unseen task Clean/Rand. 平均成功率从 **13.0/11.6** 提升到 **28.8/27.4**。
  > 💡 这条路线把世界模型从“推理时生成未来视频”改为“训练期注入物理先验”，为低延迟机器人控制提供了比重型视频生成模型更实用的架构方向。
   - 来源: [arXiv](https://arxiv.org/abs/2606.05979) | [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651042515&idx=3&sn=8e62ba2c7572de45d20993e9c8d2271f&chksm=85a518c8f35c22352275c27c4a675d97dd2d33b29bbbc5c3baedae44be4f3624ceb09fc532ec&scene=0&xtrack=1#rd)

**量化推理模型过度思考研究：CoT长度降低12-23%，错误最高减少58%**
- Sanae Lotfi、Polina Kirichenko、Steven Li、Zechun Liu 研究 **post-training quantization（PTQ）** 对 reasoning model 的影响，解释量化后模型为什么会“想更久但答得更差”。论文发现 PTQ 会改变 token-level 输出分布，在高 KL divergence / 高 next-token entropy 位置更容易采样 “wait”“but”“alternatively” 等 overthinking markers，导致最高 **52%** 的量化失败样本已经在中间步骤得到正确答案却没有作为最终答案输出。作者提出无需训练的 logit penalty 直接压制过度思考标记，在 **5 个模型（1.5B-32B）、3 种量化方法、5 个 benchmark** 上将 CoT 长度降低 **12-23%**，并使过度思考错误最高减少 **58%**。
  > 💡 量化 reasoning model 的风险不只是最终精度下降，还会改变模型的停止与修正行为；推理成本优化需要同时控制数值误差和生成轨迹偏移。
   - 来源: [arXiv](https://arxiv.org/abs/2606.00206) | [@TheTuringPost](https://x.com/TheTuringPost/status/2072868677872157078#m)

**异构PD推理设计空间：拆解跨硬件KV缓存的表示、放置与归属**
- 上海创智学院、上海交通大学、复旦大学、MetaX Integrated Circuits、Infrawaves 等提出异构 **Prefill-Decode（PD）** 推理设计空间，解决跨硬件 LLM serving 中 KV cache 如何表示、传输和归属的问题。论文将生产部署中的异构 PD 推理拆成 **accelerator、precision、interconnect、KV residency** 四个设计轴，并指出真正需要联合决策的是 PD 边界上的 **compute placement、KV representation、KV ownership**。作者强调精度策略应跟随 runtime role 而非全局统一，KV transfer engine 只搬运字节而不理解 tensor 语义，因此跨硬件/跨数值格式的 KV 表示兼容、reservation、release 和 failure recovery 必须显式管理。
  > 💡 这不是模型能力突破，而是异构算力进入生产后的系统设计信号：多供应商推理成本优势能否释放，关键会落在 PD 边界契约和 KV 生命周期管理上。
   - 来源: [arXiv](https://arxiv.org/abs/2606.29708) [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651042515&idx=2&sn=6994427190f016869ee92b7a2fab085a&chksm=8517678b634635e3d0bdb2e4c4efa3ea7a93106a8512f15d994c8b8d728f677aa89b23afe7a2&scene=0&xtrack=1#rd)

---
*更新时间: 2026-07-04 13:15*
