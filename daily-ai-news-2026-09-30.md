## 09月30日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 16 条

---

## 要点汇总

- 模型前沿：OpenAI 发布 GPT-6.1 Sol：智能指数距 Astra 仅 1 分，单任务成本约其四分之一
- 产业动态：微软撤回 Power BI 数据封锁加入 Ossie，Google 亦申请加入该联盟; OpenAI 发布 Dot：由 GPT-6 Astra 驱动的全天候主动型智能体; Meta 推出 Muse for Small Business：接入 15 款办公工具的个人 AI 智能体; Perplexity Computer 推出 Automations：事件触发或定时的持续型智能体; Claude 扩展 Preserved Thinking：思维块绑定账户与前缀，封堵蒸馏攻击
- 算力追踪：Anthropic 招股书披露：与 SpaceX 算力协议规模最高达 845 亿美元
- 初创&融资：OpenAI 据传洽谈 300 亿美元 Pre-IPO 融资，估值或达 1.4 万亿美元; a16z 投资的 EliseAI 完成 3.5 亿美元融资，估值翻倍至 40 亿美元; 前 Tesla 团队供应链智能体公司 Atomic 完成 1250 万美元 A 轮
- 研究关注：Active Taskless Distillation：仅靠单词级提示实现能力迁移; VisionHOPE：把视觉骨干网络重写为自修改学习系统; DN-MOPD：按领域方差归一化多教师反馈，找回被稀释的数学增益; GAGAR：用智能体评分器对代码 RL 的通过轨迹再分配优势
- X讨论：特朗普宣布《白宫超级智能协议》：Google、Anthropic、Meta、OpenAI、xAI 与英伟达签署; Anthropic 发起新一轮公众 AI 调查：8.1 万人研究后续，访谈可公开

---

## 📖 详细参考

### 模型前沿
**OpenAI 发布 GPT-6.1 Sol：智能指数距 Astra 仅 1 分，单任务成本约其四分之一**
- OpenAI 发布 GPT-6.1 Sol，以 Astra 约五分之一的 token 价格提供接近其智能水平：定价与 GPT-6 Sol 持平（每百万 token 输入 2 美元、输出 10 美元），缓存输入降至 **0.10 美元**。DeepSWE v1.1 上与 Astra 持平、超 GPT-6 Sol 最佳分 **6.4 个百分点**；Terminal-Bench Science 0.1 分数较 GPT-6 Sol 翻倍，单任务成本 **5.47 美元**（Opus 5.5 为 23.21 美元）；低推理档下事实错误率从 11.4% 降至 **7.7%**。Artificial Analysis 评测称其发布即替代上市仅 7 天的 GPT-6 Sol，智能指数低于 Astra 1 分、每智能指数任务成本 **0.72 美元 vs Astra 的 3.26 美元**。Ultrafast 版即将上线，最高提速 **8 倍**。
  > 💡 「二代型号一个月内替换一代」的节奏加上对齐评测同步升级，说明 OpenAI 正在把中端型号当作成本效率的快消品迭代；0.72 美元逼近 Astra 智能的定价，会把行业锚点从「旗舰能力」继续压向「单位智能成本」。
   - 来源: [OpenAI](https://openai.com/index/introducing-gpt-6-1-sol) | [@ArtificialAnlys](https://x.com/ArtificialAnlys/status/2105025585332605357) | [@OpenAI](https://x.com/OpenAI/status/2104986129686741046)

### 产业动态
**微软撤回 Power BI 数据封锁加入 Ossie，Google 亦申请加入该联盟**
- 微软宣布加入成立一年的 Apache Ossie 联盟，该组织旨在让 AI 工具更方便地访问各类应用与数据库中的数据；四个月前微软曾阻止合作伙伴将其数据管理工具接入 Power BI，被外界解读为保护自有 Fabric 产品，Salesforce 此前也经历过类似转向。据公司发言人透露，Google 也正在申请加入该联盟——其现有成员包括 Snowflake 和英伟达，Google 搜索与云业务将因此成为最新加入的主要软件厂商。
  > 💡 微软的转向呼应了 CEO Satya Nadella 一贯的"与竞品兼容"策略，意味着它放弃以 Fabric 数据栈直接对抗 Databricks 与 Snowflake，转而参与通用互操作标准保住平台层；云厂商相继入局一个由数据库与硬件厂商牵头的组织，说明数据可访问性正成为模型以外新一轮云服务竞争的底层筹码，Google 更多是补齐生态短板而非单纯做贡献。
   - 来源: [The Information](https://www.theinformation.com/articles/microsoft-tears-ai-data-wall) | [The Information](https://www.theinformation.com/briefings/google-joins-industry-group-working-help-ai-better-understand-data)

**OpenAI 发布 Dot：由 GPT-6 Astra 驱动的全天候主动型智能体**
- OpenAI 推出全天候在线的主动型智能体 Dot，由 GPT-6 Astra 驱动，拥有独立身份、独立云端电脑与浏览器，可在需要时编写测试代码，通过插件生态连接 **4,000 多款应用**，并在长期使用中从反馈学习。用户可通过 ChatGPT、短信、Slack、Teams 随时联系它；它也会以只读工具在后台「主动研究」能帮上忙的地方，敏感操作经自动审核、重要操作需用户批准。OpenAI 同时面向少量企业开放「专职 Dot」预览——在组织内拥有独立身份与职责，覆盖采购、发票、客服等场景，并与微软合作集成进 Agent 365。当天起向符合条件的市场的 Pro 与 Business Premium 用户推出，套餐已含首个 Dot；官方设想未来由多个 Dot 组成团队。
  > 💡 从「对话模型」到「有名有姓、有自己电脑的数字员工」，Dot 把 agent 的单位从会话变成持续存在的实体；专职 Dot 进企业并与 Agent 365 治理集成，说明 OpenAI 直接瞄准的是组织编制内的智能体席位而非个人助手。
   - 来源: [OpenAI](https://openai.com/zh-Hans-CN/index/introducing-dots/) | [@OpenAI](https://x.com/OpenAI/status/2104984504133918973)

**Meta 推出 Muse for Small Business：接入 15 款办公工具的个人 AI 智能体**
- Meta 为 9 月初在美国和加拿大上线的个人 AI 智能体 Muse 推出 Small Business 版本：给 Muse 一个目标（如经营业务、寻找新客户），它就会推进完成；新增 Asana、Box、Canva、Dropbox、Figma、Notion、Intuit QuickBooks、Shopify、Slack、Stripe、Zoom 等 **15 款工具连接器**及 Facebook/Instagram 商业账户接入，几步点击即可让 Muse「一开始就理解你的生意」。任何发布、发送、支出操作都需用户批准。Meta 的 Vishal Shah 称，在此次发布前已有约**三分之一**的 Muse 用户连接了商业账户。基础功能免费，更高能力以订阅提供。
  > 💡 Meta 把 Muse 的能力面从个人生活直接扩展到经营侧，等于用免费策略把「个人超级智能」叙事延伸进小企业后台；对 Shopify、QuickBooks 等工具的一键连接，正面切入 Instinct 等创业公司押注的 agent 商务入口。
   - 来源: [Meta Newsroom](https://about.fb.com/news/2026/09/introducing-muse-small-business/) | [@MetaNewsroom](https://x.com/MetaNewsroom/status/2104884886318321905) | [@vishalshahis](https://x.com/vishalshahis/status/2104920530000425123)

**Perplexity Computer 推出 Automations：事件触发或定时的持续型智能体**
- Perplexity 为其 Computer 产品推出 Automations，取代原 Scheduled Tasks：任务可按时间表或在 Slack、Gmail、Outlook、Linear、GitHub 中出现指定事件时触发，可设条件（如「某发件人来信要求决策时」）缩小触发范围。与一次性任务不同，每次运行会记住先前工作并从上次进度继续——例如周度竞品价格报告会与上周对比并标出变化，也可反向标记「该发的更新没发」「逾期未行动」。用户可指定哪些动作自主执行、哪些需人工审核；监听触发不消耗积分，运行任务时才计费。所有 Computer 用户可用。
  > 💡 「记住上次跑到哪」把自动化从无状态脚本变成有连续记忆的常驻智能体，事件触发+记忆的组合是对 Zapier 式工作流自动化的一次代际替换；按运行计费的定价也呼应了 agent 经济「按结果付费」的方向。
   - 来源: [Perplexity](https://www.perplexity.ai/hub/blog/computer-adds-automations-for-ongoing-work) | [@perplexity_ai](https://x.com/perplexity_ai/status/2104976036274552963)

**Claude 扩展 Preserved Thinking：思维块绑定账户与前缀，封堵蒸馏攻击**
- Anthropic 平台文档披露 Preserved Thinking 机制：自 Claude Fable 5.1 起，思维块携带签名校验，只有产生它的模型或指定早期模型可以读取，其余被 API 静默丢弃；思维块的有效性还依赖对话前缀（system prompt、tools 与此前全部消息）保持不变，2026 年 8 月 31 日后新建的账户默认强制校验。Sonnet 5.5 的思维块进一步**绑定产生它的账户**——跨账户发送会被直接丢弃。ClaudeDevs 表示此举旨在封堵通过切换账户实施的蒸馏攻击：中途切换账户后，Claude 会重读会话并生成全新思维。官方同步提供 mid-conversation system message、tool_addition 等不破坏前缀的开发模式。
  > 💡 把思维链与「模型+前缀+账户」三元组绑定，等于给推理过程加了不可移植的数字指纹——这既是防蒸馏的护城河，也意味着多账户协作、网关代理等常见工程模式需要重写；推理过程正在从「可自由搬运的文本」变成「受控资产」。
   - 来源: [Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking) | [@ClaudeDevs](https://x.com/ClaudeDevs/status/2104641322137293209)

### 算力追踪
**Anthropic 招股书披露：与 SpaceX 算力协议规模最高达 845 亿美元**
- 据路透社援引 Anthropic 保密 IPO 招股书报道，公司与 SpaceX 达成最多 845 亿美元的算力协议，用于在 2029 年前使用其搭载英伟达芯片的计算资源。上述协议大多可在提前 90 天通知后终止。报道同时指出，该金额远超 SpaceX 此前对外披露的相关规模。
  > 💡 在 AMD 收购 World Labs、英伟达追加回购等近期事件之后，这笔潜在交易再次把"算力供给协议规模"拉到接近百亿美元级，反映出前沿模型厂商在自有算力之外的容量对冲正在加速形成长期契约；90 天可终止条款则提示该规模属于上限而非确定支出。
   - 来源: [The Information](https://www.theinformation.com/briefings/anthropic-discloses-84-5-billion-spacex-compute-agreements)

### 初创&融资
**OpenAI 据传洽谈 300 亿美元 Pre-IPO 融资，估值或达 1.4 万亿美元**
- 据知情人士透露，OpenAI 正与投资人就一轮至少 **300 亿美元**的 Pre-IPO 融资进行早期洽谈，对应估值约 **1.4 万亿美元**，目前尚未签署投资条款书；该轮被视为推迟至 2027 年的 IPO 之前的最后一轮私募融资。OpenAI 今年 3 月曾按 8520 亿美元估值募集 122 亿美元；公司随后放弃 2026 年上市计划，称将 AI 安全放在更优先位置。
  > 💡 在尚未签署 term sheet 的阶段释放 1.4 万亿美元估值信号，意味着 OpenAI 正在测试一级市场对头部 AI 公司估值天花板的承受力；估值一年内从 8520 亿美元跳升的同时主动叫停年内 IPO，体现出对现金缓冲与监管叙事的双重需求，但 300 亿美元的体量也会放大 IPO 时的解禁压力。
   - 来源: [The Information](https://www.theinformation.com/briefings/openai-early-talks-raise-30-billion-ipo) | [TechCrunch](https://techcrunch.com/2026/09/29/openai-repotedly-in-talks-to-raise-30b-round-at-1-4t-valuation)

**a16z 投资的 EliseAI 完成 3.5 亿美元融资，估值翻倍至 40 亿美元**
- AI 初创公司 EliseAI 于本周二宣布完成 3.5 亿美元融资，估值达到 40 亿美元，约为去年 8 月 E 轮估值的两倍。本轮由 Andreessen Horowitz 与 Bessemer Ventures 联合领投。公司成立于 2017 年，主要为住房与医疗企业提供行政与运营自动化软件，覆盖租赁、维护、续约等环节，并服务专科医生集团的患者文书全流程。其软件已被美国六分之一的公寓使用，年化经常性收入今年夏天突破 2 亿美元。本月初，EliseAI 还发布了名为 Apollo 的 AI 同事，用于在平台内协同执行任务。
  > 💡 EliseAI 在“住房+医疗”两条美国家庭支出最大的赛道上同时跑通 ARR 与估值翻倍，证明垂直行业 AI 代理只要能嵌进现有工作流，就可以用 SaaS 的财务逻辑扩张；Apollo 的发布也显示其正从工具向“数字员工”叙事迁移。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/29/a16z-backed-eliseai-raises-350m-doubles-valuation-to-4b)

**前 Tesla 团队供应链智能体公司 Atomic 完成 1250 万美元 A 轮**
- 波士顿供应链智能体公司 Atomic 完成 **1250 万美元 A 轮融资**，由 Klass Capital 与 Madrona Venture Group 领投，总融资额超过 1500 万美元。创始人曾在 Tesla 2018 年 Model 3 爬产期搭建库存模拟系统；产品通过模拟场景决定企业库存的数量与位置，并可直接自动执行决策——据前 Tesla 总裁、孵化方 DVx Ventures 创始人 Jon McNeill 称，DoorDash 约 **90% 的采购**跨数百站点由其运行，客户还包括 HelloFresh，年初至今年化经常性收入**增长五倍**。
  > 💡 从「给推荐」走到「直接做采购决策」并承接九成采购流量，说明供应链这类高价值、可仿真的运营场景已经跨过智能体自主执行的信任门槛；「决策速度复利」的 Tesla 方法论正被输出成通用软件。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/29/ex-tesla-team-raises-12-5m-to-put-supply-chains-on-autopilot/)

### 研究关注
**Active Taskless Distillation：仅靠单词级提示实现能力迁移**
- 论文发现语言模型可以通过与任务无关的文本实现能力迁移。作者提出 Active Taskless Distillation（ATD），在师生共享公共祖先模型对两个普通单词近乎无差别时挑选提示，让学生仅从这些提示-单词对中学习，无需目标任务示例、教师 logit 或教师参数。在以 Qwen2.5-1.5B 为主的编码实验中，5,664 条样本相对严格匹配的对照组使 HumanEval+ 提升 5.34 个百分点。论文称该效应在科学知识、常识推理和阅读理解任务上也成立，并跨越不同的模型世代、规模与家族。功能分析表明学习到的能力可组合，且其强度与教师的更新强度同步。
  > 💡 ATD 把能力迁移压缩到单词选择层面，意味着即使不暴露教师 logit、参数或任务数据，仅凭提示层级的微妙信号也可能被蒸馏出可观察的能力增量，对模型血缘与后训练资产的边界划定提出新的审计问题。
   - 来源: [arXiv](https://arxiv.org/abs/2609.29233) | [HuggingFace Daily Papers](https://huggingface.co/papers/2609.29233)

**VisionHOPE：把视觉骨干网络重写为自修改学习系统**
- 论文把视觉骨干网络的演进归纳为从 CNN 的局部聚合，到 ViT 的全局交互、SSM 的输入相关状态转移，再到 Test-Time Training 层在处理图像时适配内部学习器的过程。论文提出 VisionHOPE，采用 Nested Learning 的自引用结构，由五个耦合记忆分别承载内容、生成键与值表示、并管理学习率与保留度，这些记忆会随图像内的视觉上下文沿扫描线联合演化。论文还推导出稳定性匹配的步长控制方案，结合对自引用注入的软上限与对保留记忆转移的谱夹紧，并证明得到的记忆动态在每次扫描中是非扩张的。论文报告在 ImageNet-1K、COCO 与 ADE20K 上取得具有竞争力的结果，代码已在 GitHub 公开。
  > 💡 视觉骨干网络长期被定位为固定规则的提取器，VisionHOPE 的关键不在于又一个新架构，而在于把「记什么」与「怎么学」放进同一个图像内的反馈回路——若稳定性证明和跨任务成绩可被复现，它将把骨干网络的竞争维度从参数规模推向在线自适应能力，对视觉预训练范式是一次底层改写。
   - 来源: [arXiv](https://arxiv.org/abs/2609.33325) | [HuggingFace Daily Papers](https://huggingface.co/papers/2609.33325)

**论文提出 DN-MOPD：按领域方差归一化多教师反馈，找回被稀释的数学增益**
- 强化学习能把一个模型训成数学、编码、指令遵循等多个单科技能专家，多教师 on-policy 蒸馏（MOPD）让学生按 prompt 领域路由给对应专家教师学习。论文在 Qwen3.5 三个规模上发现 MOPD 的学生打不过最佳单专家教出的学生：指令遵循反馈的离散度是数学反馈的数倍，主导了共享学生的参数更新，数学增益所剩无几。DN-MOPD 保留路由、按各领域实测离散度重缩放反馈强度；在**六个公开基准、三种随机种子、两种答案长度限制**下平均分全面超过 MOPD，并找回大部分数学增益。对照实验显示，增益主要来自调低指令遵循反馈，而非单独调高数学反馈。
  > 💡 多教师融合的瓶颈不在「谁来教」而在「谁的声音大」——反馈尺度未经归一化时，宽松领域的教师会淹没严格领域的信号；这一诊断对任何多源奖励或多元数据配比的训练管线都成立。
   - 来源: [arXiv](https://arxiv.org/abs/2609.35347)

**论文提出 GAGAR：用智能体评分器对代码 RL 的通过轨迹再分配优势**
- 代码智能体 RL 通常以可执行测试给出二元奖励，GRPO 会给组内所有通过测试的轨迹相同的 advantage，模型因此学不到「干净、克制的实现优于夹带多余改动的实现」。GAGAR 把同组全部轨迹放进共享工作区，由 SFT 训练的智能体评分器联合检查并对通过的候选排序，据此降权低质轨迹、再等比例重缩放全部通过轨迹以保持 advantage 总和不变。在 MiMo-V2.6-Flash（**310B**）与 MiMo-V2.6-Pro（**1.02T**）的工业规模 RL 实验中，该方法提升代码智能体表现、减缓轨迹长度增长并使训练更稳定。
  > 💡 把「测试通过」这一布尔信号细化为组内质量排序，相当于给 RLVR 补了一条实现质量的梯度；在千亿到万亿参数的生产模型上验证，说明这类信用分配修补已经进入工业训练主流程。
   - 来源: [arXiv](https://arxiv.org/abs/2609.32577)

### X讨论
**特朗普宣布《白宫超级智能协议》：Google、Anthropic、Meta、OpenAI、xAI 与英伟达签署**
- 美国总统特朗普周二宣布，多家头部 AI 公司已就 AI 安全条款达成不具约束力的承诺，内容涵盖模型对齐的内部控制与外部审计。特朗普在 Truth Social 发布的《White House Accord on Super Intelligence》由 Google、Anthropic、Meta、OpenAI、xAI 与英伟达的高管签署。
  > 💡 在 Anthropic CEO 即将赴白宫与特朗普会面的背景下，该协议把"自愿性安全承诺"升级为白宫背书的多方联合声明，意味着美国行政当局开始以政治姿态框定 AI 安全的对外口径，但因条款本身不具约束力，实际效力仍取决于各家后续落地节奏。
   - 来源: [The Information](https://www.theinformation.com/briefings/president-trump-announces-white-house-ai-accord)

**Anthropic 发起新一轮公众 AI 调查：8.1 万人研究后续，访谈可公开**
- Anthropic 用 Anthropic Interviewer 发起新一轮公众研究（9 月 29 日至 10 月 6 日，面向 Claude 与 Claude Code 的 Free/Pro/Max 用户），主题是与 AI 的重要经历、希望 AI 改变世界的哪些部分、以及对 AI 公司的期待。去年 12 月的同类研究有 **8.1 万人**参与，是迄今规模最大的 AI 公众定性研究，其结果塑造了 Anthropic Institute 的研究议程并在达沃斯向各国决策者发布。本轮新增选项：参与者可让完整访谈公开，任何人都能阅读和引用——官方称如果很多人认为 Anthropic 这类公司应当改变做法，「白纸黑字留在公共记录里」。
  > 💡 把定性访谈整体公开、主动接受外部引用监督，是在用开放性换公信力：公众意见从「实验室内部数据」变成可被监管者、研究者直接引用的公共记录，这一姿态本身也与其安全叙事形成绑定。
   - 来源: [Anthropic](https://www.anthropic.com/research/your-thoughts-on-ai) | [@AnthropicAI](https://x.com/AnthropicAI/status/2104982629884063840)

---
*更新时间: 2026-09-30 06:46*