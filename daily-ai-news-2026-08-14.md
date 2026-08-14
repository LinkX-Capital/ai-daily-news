## 08月14日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 16 条

---

## 要点汇总

- 模型前沿：OpenAI 预览 GPT-5.6 Sol 极速模式，速度最高 14 倍、每秒 750 tokens; Google 推出 Gemini 3.7 Flash，编程与文档任务全面超越 3.6 Flash
- 产业动态：DeepSeek 开源 Harness v0.1，以"一切皆插件"理念构建 agent 框架; OpenAI 上线 Computer History，把本机交互事件流变成记忆与时间线; Artificial Analysis 推出 Optima，让企业用自有任务自建可复用 benchmark; Luma 与 Dumbstruck 联合推出 Creative Intelligence 广告闭环; OpenAI、Anthropic 数据需求让初创公司 Slack 旧帖变成抢手资产; Microsoft 合并消费与商业 Copilot App，砍掉 AI Podcasts、Group Chats 等多项功能; Writer 推出 Palmyra X6，基于 GLM-5.2 后训练，客户任务成本降 50%
- 初创&融资：Databricks 原计划仅融 10 亿美元，最终以 1900 亿美元估值落地 50 亿美元
- 研究关注：OpenART：用 1 万+ stateful 场景做 Agent 红队，EMHA 攻击成功率 85.0%; Spark-to-Paper：把论文生成做成 13 个可组合 skill，引用有效率 99.5%; AI4AI at Test-Time：强模型建 harness，弱模型 ToM 性能从 0.49 提到 0.91; SHAPER：让具身 Agent 不训练参数、只进化 skill 与 harness
- X讨论：OpenAI 企业调研：前沿企业人均 token 8.3× 典型企业，Codex 占企业 token 64%; Perplexity 优化 Search as Code，执行可靠性 81.9%->92.6%、每任务成本降近 10%

---

## 📖 详细参考

### 模型前沿
**OpenAI 预览 GPT-5.6 Sol 极速模式，速度最高 14 倍、每秒 750 tokens**
- OpenAI 发布 Ultrafast 服务档位，**让 GPT-5.6 Sol 比标准档快最高 14 倍**，由 Cerebras 提供算力，**每秒生成最高 750 个输出 token**。官方定位"不再以放弃智能换速度"，让最智能模型进入对延迟敏感的业务。Ultrafast 在 OpenAI API 中向少数客户开启预览，并随算力逐步扩展。OpenAI 内部已用 Ultrafast 做事故响应（读日志、查 trace、梳理工程师报告）和把"过夜批量实验"压缩为"工作日内多次迭代"。Cerebras 同时为 OpenAI 最智能模型提供推理后端。
  > 💡 把推理速度做成独立可售卖服务档位、并由 Cerebras 这类推理芯片提供后端，等同于把"速度/成本"从模型能力中拆出作为单独差异化指标，可能动摇"小模型才够快"的旧分工。
   - 来源: [@openai](https://x.com/OpenAI/status/2087947721936359705) | [OpenAI Blog](https://openai.com/index/previewing-ultrafast/)

**Google 推出 Gemini 3.7 Flash，编程与文档任务全面超越 3.6 Flash**
- Google 发布 Gemini 3.7 Flash，定位"面向编码与 Agent 的工作模型"。相比 3.6 Flash（三周前发布），**3.7 Flash 在 FrontierCode 1.1 Main 拿到 43.6% 对 34.4%**，**在 DeepSWE v1.1 拿到 65.3% 对 49.0%**；Web 开发在 Arena.ai WebDev Arena Elo 拿到 **1588 对 1538**；知识密集文档 GDP.pdf 拿到 **34.0% 对 22.0%**；AutomationBench **30.4% 对 17.0%**。**年底前以入门价 $0.75/1M 输入、$3.75/1M 输出 token 销售**，相当于 3.6 Flash 原价的一半。
  > 💡 沿用"Flash 为工作模型、Pro/Ultra 为前沿模型"的双层产品线，Google 把价格更低、响应更快的版本与 Agent 场景绑定，三周迭代一轮，意在抢占高调用量的开发者入口。
   - 来源: [@GoogleAI](https://x.com/GoogleAI/status/2087949045407035766) | [Google Blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-3-7-flash/)

### 产业动态
**DeepSeek 开源 Harness v0.1，以"一切皆插件"理念构建 agent 框架**
- DeepSeek 上线 Harness v0.1 开发者预览版，**以 MIT 协议开源核心代码**，面向全球构建 agent harness 的开发者开放。Harness 基于 **Cordis meta-framework**，核心设计理念是"Everything is a plugin"：模型、工具、技能、会话、沙盒、文件系统、循环、编排、UI 全部以插件实现，可混合、替换、扩展。该版本定位 agent harness 框架的早期形态，供外部在其基础上做二次适配。
  > 💡 把 agent harness 作为可被开发者二次定制的框架开源，并在架构层声明"一切皆插件"，意在把 agent 运行时骨架开放成生态入口，呼应 DeepSeek 在 Agent 方向的产品化与社区化动作。
   - 来源: [@deepseek_ai](https://x.com/deepseek_ai/status/2087887408440164663)

**OpenAI 上线 Computer History，把本机交互事件流变成记忆与时间线**
- OpenAI 在 ChatGPT 桌面端（macOS）推出 Computer History 功能，**Pro/Business/Enterprise 用户默认关闭，需手动开启**，EEA、瑞士与英国暂不开放。Computer History 把用户在允许 App 与网站上的交互事件流（点击、键入、快捷键、App 切换等通过 macOS accessibility 系统获取的事件）周期性转成文本摘要与本地记忆文件，供 ChatGPT 和 Codex 跨对话引用。**与早期 Chronicle 研究预览不同，Computer History 不截屏、不录屏、不录音**；原始事件文件保留不超过 48 小时，记忆文件以纯 Markdown 存于本地。用户可按 App/网站过滤并一键删除历史。OpenAI 处理事件文件以生成记忆但训练不使用事件，除非用户开启相应数据控制。文档明确指出"Computer History 增加 prompt 注入风险"。
  > 💡 这是 OpenAI 第一次把"本机行为流"做成跨 Chat 持久上下文，不靠截屏而靠交互事件摘要。路径与 Anthropic 的 Skills、Microsoft 的 Recall 同出一源，但工程边界更克制（本地存储+分明权限+不训练），主战场正在向"系统级 agent"延伸。
   - 来源: [@openai](https://x.com/OpenAI/status/2087996499263369267) | [ChatGPT Learn](https://learn.chatgpt.com/docs/customization/computer-history)

**Artificial Analysis 推出 Optima，让企业用自有任务自建可复用 benchmark**
- Artificial Analysis 发布 Optima 平台，让企业用自有数据/任务/agent 轨迹自定义 benchmark，跨前沿模型对比性能、成本与时间效率。支持上传自有数据集、导入 agent traces（Arize/Braintrust/Langfuse）、或仅描述用例让 Optima 自动建 benchmark。评分复用 Artificial Analysis 在 GDPval-AA 和 AA-Briefcase 的 rubric 与 pairwise judging，可显示"质量/每任务成本/每任务时间"的 tradeoff。VP Product Graham Cameron 引用内部数据："90% 头部 AI 组织知道自己需要自定义 benchmark，但只有不到 5% 实际建过"。Optima 今日可用。
  > 💡 "通用榜单不能告诉你哪个模型最适合你的活"——把自家任务做成 benchmark 一直贵到只有头部实验室做得起；Optima 把这套工程封装成 SaaS，瞄准的是企业评估内化的入口。
   - 来源: [@ArtificialAnlys](https://x.com/ArtificialAnlys/status/2087930781050322977) | [Artificial Analysis Optima](https://artificialanalysis.ai/optima) | [@grmcameron](https://x.com/grmcameron/status/2087981252683223522)

**Luma 与 Dumbstruck 联合推出 Creative Intelligence 广告闭环**
- Luma 与情绪分析公司 Dumbstruck 联合提出"Creative Intelligence"广告品类：**Dumbstruck 用面部编码测受众情绪/行为/认知反应→定位需要改的片段→Luma Agents 用现成素材逐帧重做，不需要重拍→Dumbstruck 在投流前验收益**。Dumbstruck CEO Jeff Tetrault 称"瓶颈不再是产出更多，而是判断哪条值得做"。Wayfair 已在探索这套闭环做高影响个性化和本地化。
  > 💡 创意生产成本塌缩后，品牌侧战场正在从"会不会拍"转移到"哪条值得被投"——情绪 analytics + 逐帧 AI 重做组合的闭环，等于把 post-production 做成可双向循环的优化系统；行情性是 Luma 继统一多模态模型之后又一个产品锚定。
   - 来源: [@LumaLabsAI](https://x.com/LumaLabsAI/status/2087916837736497459) | [Luma News](https://lumalabs.ai/news/luma-and-dumbstruck-launch-creative-intelligence-for-advertising)

**OpenAI、Anthropic 数据需求让初创公司 Slack 旧帖变成抢手资产**
- 据报道，AI agent 创业公司 Warmly 在 6 月底同意被 HubSpot 收购八天后，CEO Maximus Greenwald 收到一封不寻常邮件：**Mercor（为 OpenAI/Anthropic/Google 等实验室训练 AI 而付钱给外包标注员）主动询价购买 Warmly 存量的 Slack 历史帖和工单**。Mercor 的逻辑是把这些企业内部 Slack 历史、helpdesk tickets 当作真实工作流语料来训练模型。
  > 💡 当公开网爬接近上限，模型训练数据的下一个高地转向企业内部工单与协作历史——被收购前的 startup 恰好是含金量最高的语料；价格信号出现了，但归并、版权与隐私边界尚未定形。
   - 来源: [The Information](https://www.theinformation.com/articles/startups-find-old-slack-threads-tickets-suddenly-high-demand)

**Microsoft 合并消费与商业 Copilot App，砍掉 AI Podcasts、Group Chats 等多项功能**
- Microsoft 把消费向 Copilot App 与 Microsoft 365 Copilot App 合并成一个统一 App，用户可用个人账户、工作/学校账户或两者同时登录，账户数据隔离保留。**消费用户将在 2026 年 8 月 18 日失去 Group Chats、AI 生成 Podcasts、Copilot Labs 实验性功能与 Deep Research**，付费专业用户可改用 Researcher 替代 Deep Research；趣味浮动角色 Mico 下线。Microsoft 自身确认 Copilot 已"lost its way"：The Information 7 月曾报道负责 Copilot 的 EVP Jacob Andreou 内部备忘录称该 App 需要"赢得 exist 的权利"。
  > 💡 "敢于砍掉"是 AI App 经过一年无序扩张后回到产品收敛的信号；对 Microsoft 是承认 Copilot 没有靠捆绑取得入口，对行业则意味着 AI 助手竞争从"功能多少"转向"重复使用深度"。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/13/microsoft-kills-off-unsuccessful-ai-features-while-merging-its-separate-copilot-apps/) | [Microsoft Support](https://support.microsoft.com/en-us/microsoft-365-copilot/learning/changes-microsoft-copilot-app)

**Writer 推出 Palmyra X6，基于 GLM-5.2 后训练，客户任务成本降 50%**
- 面向营销的企业 AI 平台 Writer 发布新旗舰模型 **Palmyra X6**，作为 **Z.ai 开源模型 GLM-5.2 的后训练变体**，定位部署就绪、单价更低。配合新升级的 agentic harness，Writer 估计对客户基础任务成本最多降 50%。公司近期一份论文显示："harness 改造跨模型平均可降成本 40%"，并称"harness 是唯一能跨当前和未来所有模型复利增效的组件"。CEO May Habib 称"企业绝对厌倦了追逐下一个 benchmark"。
  > 💡 "harness 复利 + 后训练开源底座"是中立路线 —— 对 Writer 自身是把推理成本做成可控杠杆；对大模型实验室则是一种契约化的成本约束，等于把"用谁的底座"的决定权从厂商迁移到企业。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/13/writer-introduces-new-ai-model-and-upgraded-harness-to-contain-token-costs/)

### 初创&融资
**Databricks 原计划仅融 10 亿美元，最终以 1900 亿美元估值落地 50 亿美元**
- 据报道，Databricks 联合创始人兼 CEO Ali Ghodsi 透露本轮最初只打算筹集 10 亿美元。**The Information 6 月在 Databricks 大会期间爆出融资消息后，"select group of investors"表达的总认购意向达到 150 亿美元**；为避免冷落长期股东，公司增发股票。**7 月官宣在 1880 亿美元估值完成，8 月 13 日披露实际融资额 50 亿、估值上修为 1900 亿美元**。本轮由 Coatue 领投，约 24 家 VC 参与。Databricks 当前 **年化 run rate 收入 70 亿美元，增长 80%，现金流为正**；云数据仓库核心产品 15 亿美元 run rate、同比 100% 增长；**面向 agent 数据库的 Lakebase（2025 年 6 月上线）已达 1 亿美元 run rate**。Ghodsi 表示公司过去 20 个月累计融资 200 亿美元，与三大 hyperscaler 都有数十亿美元云承诺。
  > 💡 融资规模 5 倍于计划、估值较上一轮显著抬升，说明数据/AI 基础设施需求拉动下二级基金仍在抢配头部；Lakebase 已达 1 亿美元 run rate，是 Databricks 第一次把"agent 即时数据库"做成可计价的轮廓，估值锚从数据仓库切向 agent 基础设施。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/13/databricks-wanted-to-raise-1b-investors-wanted-15b-it-settled-on-5b-at-a-190b-valuation/)

### 研究关注
**OpenART：用 1 万+ stateful 场景做 Agent 红队，EMHA 攻击成功率 85.0%**
- 论文提出 OpenART，一个面向长程 Agent 安全的开源红队 arena，包含 **50 个领域、超过 1 万条经验证的 stateful 场景**，背后可调用 50 万+ 工具与技能。可跨 75 种 agent-model 配置统一评测。作者提出 Evolutionary Markov Hypergraph Attack（EMHA）——一类黑盒 policy，通过协调 authorized 状态转移做"环境进化"，无需更新参数；任务目标不变、只改环境状态。**在所有配置中，EMHA 的 pooled Attack Success Rate 达 85.0%**，相比 instruction-only 进化在简单环境中优势约 2%，复杂环境扩大到 17% 以上，说明**安全漏洞随任务复杂度增加被暴露更多**。论文进一步发现：**agent 的 runtime 实现，而非底座模型本身，是安全差异的重要来源**。第一作者 Yunhao Chen，通讯作者 Yu-Gang Jiang（复旦大学）。
  > 💡 "安全评测改 benchmark 的同时要改 agent 实现"——这套结果把"harness 是新的模型"这句话做了量化，也说明现有对单模型进行的安全评测已经无法回答 agent 系统在生产中的实际攻击面。
   - 来源: [arXiv](https://arxiv.org/abs/2608.00677) | [HuggingFace](https://huggingface.co/papers/2608.00677)

**Spark-to-Paper：把论文生成做成 13 个可组合 skill，引用有效率 99.5%**
- 论文提出 Spark-to-Paper，把从研究想法到完整论文的端到端流程做成**现有 coding assistant 内 13 个可组合 skill**，不需要单独的 agent 平台或编排服务。系统把基于模型判断的操作与可确定性执行/检查的操作分开，再进一步把"实验规划"与"结果汇报"分开——要求证据在观察到结果前就被列出、论文 claim 根据实测结果回头修订。为防止"Self-Refutation Loop"（重复实验持续否定原研究目标），系统用确定性完整性检查 + 自批判。在 8 个受控研究选题上：**Citation 有效性 99.5%，figure 可编辑率 96.4%**；完整 integrity + review stack 把 fabrication 检测从 14% 提到 92%。**单篇论文平均 1190 万 token、8.1 美元、3.2 小时**。第一作者 Zhuoyang Qian，通讯作者 Wenhao Wang。
  > 💡 这种把研究做工程化的方式：不换底座模型、不堆 agent 编排框架，靠把"做事的步骤"和"判断的步骤"分隔开、再用 deterministic check 兜底——把"全自动化研究论文"的质量瓶颈推进到可控的工程成本范畴。
   - 来源: [arXiv](https://arxiv.org/abs/2608.11924) | [HuggingFace](https://huggingface.co/papers/2608.11924)

**AI4AI at Test-Time：强模型建 harness，弱模型 ToM 性能从 0.49 提到 0.91**
- 论文研究 strong-to-weak scaffolding：**强 builder 模型构建 inference-time harness，帮弱 target 模型在不更新参数的情况下更可靠地完成任务**，以 4 个 Theory-of-Mind benchmark 为载体。builder 用 5% 数据作 validation 多轮 refine harness，然后在完整测试集上评估。**平均 target 模型性能从 0.49 提到 0.91，接近翻倍**。分析表明增益主要来自把不稳定的模型推理 offload 到确定性 code、benchmark-specific routing 与严格 answer-format 强制——而非鼓励弱模型多推理或多采样。进一步发现：越弱的 target 模型收益越大。作者 Cheng Qian、Shelby Heinecke（Salesforce AI Research）、Silvio Savarese、Huan Wang。
  > 💡 "强模型教弱模型"传统做训练时蒸馏，这里把它搬到测试时——结论是强模型可直接用 harness transfer 认知结构给弱模型；与近期 DeepSeek Harness v0.1 的开源共享同一组假设，即 harness 正在成为与模型权重并列的能力载体。
   - 来源: [arXiv](https://arxiv.org/abs/2608.12307) | [HuggingFace](https://huggingface.co/papers/2608.12307)

**SHAPER：让具身 Agent 不训练参数、只进化 skill 与 harness**
- 论文提出 SHAPER，一个 train-free 自演化框架，用**冻结参数的底座模型**做规划器与优化器，通过目标环境的 rollout 演化可复用 skill 与 context-code harness，提升非参数 agent 系统的能力。相比纯执行、SFT 与 verifier-free selection 这类 test-time scaling baseline，SHAPER 在 VLABench 和 ESI-Bench 两类具身任务上、跨不同底层 action 接口有效。结论：当模型训练贵、不可得或不可取时，**skill + harness 联合优化是具身 Agent 自演化的可行路径**。第一作者 Peidong Wang，机构关联 Dongsheng Li。
  > 💡 与 test-time harness transfer 把"训练时蒸馏"搬到推理时类似，SHAPER 把"训练适配环境"搬到"agent 代码层进化"，且不要求可编程 API——把机器人侧模型训练成本曲线再往下压一档。
   - 来源: [arXiv](https://arxiv.org/abs/2608.11350)

### X讨论
**OpenAI 企业调研：前沿企业人均 token 8.3× 典型企业，Codex 占企业 token 64%**
- OpenAI 发布两份研究--Enterprise Signals 与工作论文《How Organizations Use AI: Evidence from ChatGPT》--基于超 1000 万条消息。截至 6 月，**企业 Codex 已生成全部 Codex+ChatGPT 输出 token 的 64%**。**前沿企业（每月 AI 用量前 10%）人均每周输出 token 是典型企业的 8.3 倍**，1 月份该倍数还只有 2.6×。前沿企业每周活跃用户 21% 用 Plugins、19% 用 skills，典型企业分别只有 9% 和 3%。Codex 周活自 2 月起在法律职能增长 108×、销售 41×、营销 26×，工程仅 5×。**初阶员工半年后比高管每周多发 13 条消息**，与此前高管用得多的调查结论相反。
  > 💡 "前沿差距"在半年内从 2.6× 扩到 8.3×，且非工程职能 Codex 月内增长数十倍，说明 Agent 化扩散的瓶颈不再是模型，而是企业有没有把工具接到业务上下文、并把成功用例沉淀为可复用实践。
   - 来源: [@openai](https://x.com/OpenAI/status/2087912623883051300) | [OpenAI Blog](https://openai.com/index/how-enterprises-put-ai-to-work/)

**Perplexity 优化 Search as Code，执行可靠性 81.9%→92.6%、每任务成本降近 10%**
- Perplexity 6 月发布的 Search as Code（SaC）在 wide & deep research 上达到 SOTA。本周正在滚出 SaC 优化：**在 Computer Search SDK 两批更新内，把执行可靠性从 81.9% 提升到 92.6%**，同时把单任务成本压低近 10%。Perplexity 指出"SDK 形态决定模型能不能用好它"，并举例 SaC 优化在 Computer 内多类真实工作流上带来更高用户满意度。成本降低伴随每任务可靠性上升，被官方定位为"orchestration 越可靠，能力越强"。
  > 💡 把搜索能力做成 SDK 形态给模型调用，并通过 SDK 形状优化来抬高执行可靠性——成本与可靠性同向下降，意味着 agent harness 里的工具侧正在成为可被工程化提升的独立变量。
   - 来源: [@perplexity_ai](https://x.com/perplexity_ai/status/2087950343841915046)

---
*更新时间: 2026-08-14 06:46*