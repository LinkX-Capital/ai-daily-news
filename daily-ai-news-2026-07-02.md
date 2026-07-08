## 07月02日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：Anthropic 恢复 Claude Fable 5 全球部署：出口管制解除后 7 月 1 日重新上线; 智谱推出 GLM-5.2 官方开发环境 ZCode，支持插件管理与通用子智能体
- 产业动态：The Information 披露马斯克在特斯拉搭建 Terafab 芯片团队，系 550 亿美元 Tesla-SpaceX 协同制造项目; xAI发布Voice Agent Builder无代码语音Agent构建平台，定价0.05美元/分钟; 据报 SpaceX 向投资者展示「手机形态」AI 设备原型，Musk 否认该报道; Google 将 Gemini Spark 带上 macOS，并接入 Canva/Dropbox 等第三方应用与自定义 MCP; AWS CloudFormation推出Express模式，基础设施部署速度提升至4倍
- 算力追踪：NVIDIA 联合台积电等伙伴在美本土扩产：四年目标 5000 亿美元 AI 基础设施; Meta 据报筹建 AI 云基础设施业务，将富余 GPU 算力对外商业化对标 AWS/Azure
- 初创&融资：Venice AI 完成 6500 万美元 A 轮晋升独角兽，年化收入超 7000 万美元已盈利; 清华 AIR 孵化求之科技（星连被投）完成超 1 亿美元天使轮，创消费级具身机器人单笔纪录; MobAI 完成数百万元天使轮（赤子城独家投资），推出北美女性向 AI 互动叙事应用 Lunaverse Stories; Together AI 完成 8 亿美元 C 轮融资，估值跃升至 83 亿美元并锁定 500MW 算力; AI 芯片公司 Etched 累计融资 8 亿美元，投后估值 50 亿美元并已斩获 10 亿美元订单
- 研究关注：SARL（Berkeley）把 VLA 语言 prompt 当作 RL「语义动作」，100 episode 内适配真机; Dockerless：无需执行环境的编程 Agent 补丁验证器，SWE-bench Verified 解决率 62.0%; Orca：学习统一世界潜空间的通用世界基座模型，预训练 12.5 万小时视频; MIT 团队用 AI Agent 大规模黑盒审计推荐算法，1120 个 agent 在 X 上采集 20 万次曝光; 邢波团队《Critique of Agent Model》：区分 agentic/agentive 系统，提出 GIC 通用 Agent 架构; UniTac：首个面向跨传感器触觉理解与生成的统一多模态模型
- X讨论：Google DeepMind 披露 SynthID 进展：已为 1000 亿张图片/视频打水印，联合 OpenAI/NVIDIA/Apple 推广; SemiAnalysis 解析推理成本切割：每次推理被持续拆解推动智能成本下降; Peter Steinberger用 Codex 改进 OpenClaw iOS 应用，基于两条 X 反馈完成首轮迭代; Krea 2 技术报告：开权重文生图基座 K2 Raw / K2 Turbo，用 SAE 做数据策展

---

## 📖 详细参考

### 模型前沿
**Anthropic 恢复 Claude Fable 5 全球部署：出口管制解除后 7 月 1 日重新上线**
- Anthropic 公告，**Claude Fable 5** 于 **7 月 1 日** 面向全球用户重新开放，接入 Claude Platform、Claude.ai、Claude Code 与 Claude Cowork。时间线：**6 月 12 日** 美国政府对其最新模型 Fable 5 与 **Mythos 5** 实施出口管制，因指令即时生效且无法实时核验国籍，Anthropic 一度面向所有用户暂停两款模型；**6 月 30 日 出口管制解除**。Pro、Max、Team 及部分 Enterprise 套餐下，Fable 5 在 7 月 7 日前可占用每周用量上限的 **50%**，之后转为按用量额度使用；AWS、Google Cloud、Microsoft Foundry 上的可用性将尽快恢复。**Mythos 5** 已在 6 月 26 日获美政府批准后向部分美国组织恢复，并通过 **Glasswing 计划** 扩展。Anthropic 另联合 Amazon、Microsoft、Google 等 Glasswing 合作方推动统一的 jailbreak 严重性评估框架；OpenRouter 同步上线 Fable 5 并指出 Anthropic 为其新增**网络安全滥用防护分类器**，分类器完善期间部分编程与调试请求会**临时回退至 Opus 4.8**。
  > 💡 Fable 5 事件是 AI 出口管制首次直接干预前沿模型全球分发的标志性案例，Anthropic 从「全面暂停 → 分阶段恢复 → 跨云重新上架」的处置路径，将成为其他前沿模型厂商应对同类管制时的操作模板；Mythos 5 与 Glasswing 计划则暗示其多品牌 + 政企协同的全球分发链路正在制度化。
   - 来源: [Anthropic](https://www.anthropic.com/news/redeploying-fable-5) | [@anthropicai](https://x.com/AnthropicAI/status/2072163884430229756) | [@openrouter](https://x.com/OpenRouter/status/2072405997289877846#m)

**智谱推出 GLM-5.2 官方开发环境 ZCode，支持插件管理与通用子智能体**
- 智谱发布 GLM-5.2 模型的官方开发环境 **ZCode**，定位为配套 AI 编程智能体。功能上支持**插件管理与自定义插件（beta）**、**通用子智能体**（可自定义读写权限与模型）、文件回滚、知识库与远程工作区。
  > 💡 大模型厂商将 IDE/编程 Agent 作为模型生态延伸已成趋势（对标 Claude Code、Cursor），ZCode 的插件 + 子智能体 + MCP 式扩展反映智谱在 GLM-5.2 生态上从模型层向开发体验层的纵深投入。
   - 来源: [@zai_org](https://x.com/Zai_org/status/2072349457866265054#m) | [ZCode Changelog](http://zcode.z.ai/en/changelog)

### 产业动态
**The Information 披露马斯克在特斯拉搭建 Terafab 芯片团队，系 550 亿美元 Tesla-SpaceX 协同制造项目**
- The Information报道，特斯拉内部正组建名为 **Terafab** 的芯片团队，由 Elon Musk 主导；该项目是一个**总值约 550 亿美元的半导体制造项目，由 Tesla 与 SpaceX 协同推进**。报道通过梳理特斯拉组织架构指出，在 SpaceX 与 Tesla 合并预期升温的背景下，两家公司实则已在芯片、人形机器人等方向上以「单一实体」方式运作，Terafab 团队专注特斯拉自研 AI 芯片。
  > 💡 Terafab 团队组建意味着特斯拉自研算力的决心超越汽车范畴，叠加近期 SpaceX 与特斯拉合并预期，Musk 正在构建覆盖车、机器人和发射的垂直算力帝国。
   - 来源: [The Information](https://www.theinformation.com/articles/elon-musk-building-terafab-team-inside-tesla)

**xAI发布Voice Agent Builder无代码语音Agent构建平台，定价0.05美元/分钟**
- xAI 发布 Voice Agent Builder，一款基于 Grok Voice 的无代码语音 Agent 构建平台。用户无需编程即可创建类人语音 Agent，平台即日起上线，定价 0.05 美元/分钟。
  > 💡 Voice Agent Builder 把语音 Agent 推向无代码化，与近期 OpenAI、Google 抢占语音赛道的节奏一致，xAI 通过低价切入企业客服与电话自动化场景，是 Grok 商业化路径的重要补充。
   - 来源: [@xai](https://x.com/xai/status/2072342803787702422#m)

**据报 SpaceX 向投资者展示「手机形态」AI 设备原型，Musk 否认该报道**
- 据《华尔街日报》报道，SpaceX 向投资者展示了一款「手机形态」（handset-like）AI 设备原型，比 iPhone 更薄更小巧，定位介于小型触屏手机与 Rabbit R1 之间，仍处早期阶段、设计可能调整。**Elon Musk 否认该报道，称其「完全失实」**。SpaceX 具备与 Tesla 协同的量产制造能力与芯片资源，并已通过 Starlink Mobile 布局无线业务，被视为 Verizon、AT&T 的潜在竞争者。参照系：OpenAI 正与 Jony Ive 合作开发 AI 设备，Sam Altman 称其将「比 iPhone 更宁静」。
  > 💡 若报道属实，Musk 将在与 OpenAI 的 AI 设备竞赛中再开一条消费硬件战线，叠加 Starlink Mobile 的无线底座，形成「设备 + 网络 + 模型」闭环想象；但 Musk 已否认，真实性待进一步验证。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/01/spacex-has-an-ai-device-prototype-and-it-sure-sounds-phone-ish/)

**Google 将 Gemini Spark 带上 macOS，并接入 Canva/Dropbox 等第三方应用与自定义 MCP**
- Google 向 Gemini macOS 应用推送 **Gemini Spark** 更新，使其可跨桌面文件与应用执行任务（如整理下载目录 PDF、依据发票在 Workspace 生成预算表），仅访问用户授权文件；近期还将支持**由手机远程向 Mac 下发多步任务**（如找到销售报告→提取总收入→发邮件）。同步扩展至 Google Tasks/Keep、Canva、Dropbox 等，并上线**自定义 MCP** 接入；新增实时话题追踪（比赛结束、股价阈值等主动推送）。macOS 版 Beta，面向美国 18 岁以上 AI Ultra 订阅用户。
  > 💡 Gemini Spark 从聊天窗口走向操作系统级 Agent，「手机远程指挥桌面执行多步任务」是消费端通用 Agent 落地的标志性能力；自定义 MCP 接入则让 Google 在 Agent 生态标准之争中与 Anthropic（Claude）同台。
   - 来源: [Google Blog](https://blog.google/innovation-and-ai/products/gemini-app/gemini-spark-updates-june-2026/)

**AWS CloudFormation推出Express模式，基础设施部署速度提升至4倍**
- AWS宣布CloudFormation新增Express模式，将基础设施即代码（IaC）部署速度提升至最高4倍。该模式针对AI Agent与开发者的快速反馈场景设计，可在秒级返回部署确认结果，缩短从代码提交到资源可用的等待时间。
  > 💡 AI Agent自动化运维需要亚分钟级的云资源响应，传统CloudFormation堆栈在复杂场景下需数分钟，Express模式是AWS针对Agentic AI基础设施需求做的工程优化，也预示主流云厂商正在把AI Agent视为新的API调用主体。
   - 来源: [AWS Blog](https://aws.amazon.com/blogs/aws/accelerate-your-infrastructure-deployments-by-up-to-4x-with-aws-cloudformation-express-mode/)

### 算力追踪
**NVIDIA 联合台积电等伙伴在美本土扩产：四年目标 5000 亿美元 AI 基础设施**
- NVIDIA 官方博客《NVIDIA and Partners Build in America, for America》披露美国本土制造计划：联合**台积电、富士康、纬创、安靠、矽品精密**等伙伴，在**亚利桑那州凤凰城台积电工厂生产 Blackwell AI 芯片**，在**德州休斯顿与达拉斯分别建超级计算机制造工厂**，并在亚利桑那与安靠、矽品精密合作芯片封装与测试；休斯顿、达拉斯工厂将在**未来 12-15 个月内量产**。NVIDIA 目标**四年内在美国生产价值最高 5000 亿美元的 AI 基础设施**，以增强供应链韧性与安全，满足 AI 芯片与超算需求。
  > 💡 NVIDIA 从芯片设计向制造、能源、劳动力纵深布局，反映 AI 算力竞争已从芯片单点扩展至产业链与电力基建的国家级比拼。
   - 来源: [NVIDIA Blog](https://blogs.nvidia.com/blog/nvidia-and-partners-build-in-america-for-america/)

**Meta 据报筹建 AI 云基础设施业务，将富余 GPU 算力对外商业化对标 AWS/Azure**
- 据 Bloomberg/The Information 与 TechCrunch 报道，Meta Platforms 正筹建面向外部客户的 **AI 云基础设施业务**，直接对标 AWS、Microsoft Azure、Google Cloud。Meta 此前主要自用其大规模 GPU 集群（服务于 Llama 系列训练与社交平台 AI 功能部署），如今算力出现富余，转向对外销售 AI 算力与模型访问权限。业务规模、定价与上线时间均未披露。
  > 💡 Meta 若正式进入 AI 云市场，将打破其「仅供内部训练」的传统定位，超大规模自研 GPU 集群的剩余算力可能成为关键差异化资源；但对外售卖算力也可能与其既有广告/社交客户及云合作伙伴产生竞争冲突。
   - 来源: [The Information](https://www.theinformation.com/briefings/meta-plans-ai-cloud-business-push) | [TechCrunch](https://techcrunch.com/2026/07/01/meta-like-spacex-looks-to-turn-excess-ai-compute-into-cash/)

### 初创&融资
**Venice AI 完成 6500 万美元 A 轮晋升独角兽，年化收入超 7000 万美元已盈利**
- 隐私优先 AI 平台 Venice AI 完成 **6500 万美元** A 轮融资，估值 **10 亿美元**，为首轮外部融资，由加密赛道 VC 领投。公司由 Erik Voorhees 创立，提供 200+ 模型访问：在自有数据中心托管「无审查」开源模型，并将查询路由至 OpenAI、Anthropic 等闭源模型；用户输入经客户端加密后通过外部代理处理，Venice 自身不存储数据，部分模型提供端到端加密（需订阅）。公司**已盈利**，**年化收入运行率超 7000 万美元**，月活用户超 **300 万**，日均 API 调用 **170 万次**。
  > 💡 在主流 AI 产品依赖数据飞轮的格局下，Venice 以隐私 + 无审查为差异化并实现盈利，证明细分定位可跑通商业化；但 10 亿美元估值对应 7000 万美元年化收入倍数偏高，后续增长是关键考验。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/01/venice-ai-becomes-a-unicorn-with-65m-series-a-as-its-privacy-first-ai-platform-takes-off/)

**清华 AIR 孵化求之科技（星连被投）完成超 1 亿美元天使轮，创消费级具身机器人单笔纪录**
- 清华系消费级具身机器人公司求之科技（DISCOVER Robotics）完成**超 1 亿美元天使轮**，创下消费级具身机器人赛道单笔天使轮融资最高纪录，参投方含**君联资本、信产投资、联想创投、沄柏资本、普华资本、临港科创投、琥珀资本、庚辛资本**等。公司 2023 年自清华大学智能产业研究院（AIR）孵化，创始人兼首席科学家**周谷越**任清华水木书院具身工程机器人主题首席教授、DISCOVER Lab 主任，并曾是大疆核心成员、主导掌上无人机「晓」。团队含前华为天才少年（世界模型方向）、多名前消费级机器人企业智能一号位与清华特奖得主。公司主攻消费级具身机器人，目标「走进千家万户」，量产计划已在推进。
  > 💡 资金体量把消费级具身机器人天使轮门槛推至亿美元级，反映 2025 年具身智能赛道头部项目已进入资本密集阶段；周谷越「学术 + 大疆消费品」双重背景是连接具身前沿研究与消费量产的关键人选，但「走进千家万户」仍取决于成本与场景定义。
   - 来源: [雷峰网](https://mp.weixin.qq.com/s/bG0Wllp2cO6arJm6WaZ9PA) | [IT桔子](https://www.itjuzi.com/investevent/14699592)

**MobAI 完成数百万元天使轮（赤子城独家投资），推出北美女性向 AI 互动叙事应用 Lunaverse Stories**
- AI 创业公司 MobAI 完成 **数百万元** 天使轮，由港股上市公司 **赤子城科技独家投资**。核心产品为面向北美 18-24 岁年轻女性的 AI 互动叙事应用 **Lunaverse Stories**：以互动 Feed 流为载体、跑团骰子机制决定剧情分支，并融入体感操作与场景小游戏，支持多人多视角模式。团队仅 4 人——创始人钟文鼎（Vito，原头部 VC 从业者）、CPO 王博（Kaito，原头部 AI UGC 平台早期核心，曾 3 个月推动产品日活破百万）、CTO 张奥多（August，中科大 AI 方向博士）。底层为两套 AI 系统：**「Remix Anywhere」** 在任意剧情节点插入玩家想法、实时生成支线；**「Dream Universe」** 追踪偏好生成个性化支线并进入推荐池分发。MobAI 还将推出面向创作者的 **Lunaverse IDE**（AI 辅助编剧、资产一键生成、自动发布）。Lunaverse Stories 7-8 月内测，二季度中旬正式上线，IDE 已向外部创作者试运营。
  > 💡 4 人团队数月完成产品雏形本身即 AI 压缩内容生产管线的注脚；用 AI 把「互动叙事」旧品类重做一遍并自建 IDE 双端供给，是 AI 娱乐出海的典型打法，但 Z 世代女性留存与变现仍待验证。
   - 来源: [36氪](https://mp.weixin.qq.com/s/HqWh7DQfn0E9WYNm6oL4Xg) | [IT桔子](https://www.itjuzi.com/investevent/14699612)

**Together AI 完成 8 亿美元 C 轮融资，估值跃升至 83 亿美元并锁定 500MW 算力**
- AI neocloud Together AI 完成 **8 亿美元** C 轮融资，估值 **83 亿美元**，由 **Aramco Ventures** 领投，NVIDIA、Vista Equity、General Catalyst、Salesforce Ventures 等参投；新投资方另独立承诺**超 500MW 算力产能**。公司主营开源模型推理 API 与 GPU 集群租赁，客户含 Cognition、Decagon、ElevenLabs、Cursor、Suno。官方称基于 DeepSeek/Nemotron/MiniMax/Kimi/GLM 等模型，企业可实现 **6-20 倍** 成本下降（Decagon 降至**六分之一**）。研发侧近期发布面向 Blackwell 的 **FlashAttention-4**、Megakernel 与 together.compile，并自称已成「全球最大 AI token 生产者之一」。
  > 💡 估值较 16 个月前 B 轮翻倍有余、Aramco 领投标志中东资本继续加注 AI 基础设施；500MW 独立资本化算力承诺 + 开源模型 6-20 倍成本优势，是 Together AI 押注「闭源前沿模型在生产场景经济性不可持续」的核心筹码，也印证开源推理正在挤压闭源 API 利润空间。
   - 来源: [Together AI Blog](https://www.together.ai/blog/announcing-our-series-c) | [TechCrunch](https://techcrunch.com/2026/07/01/neocloud-together-ai-raises-800m-leaps-to-8-3b-valuation/)

**AI 芯片公司 Etched 累计融资 8 亿美元，投后估值 50 亿美元并已斩获 10 亿美元订单**
- AI 芯片公司 Etched 公布进展：台积电今年早些时候已成功制造其芯片，公司已累计获得 **10 亿美元** 合同订单。产品形态为「前沿推理集群」——芯片连同定制机架与软件整套出售，主打以更低成本、更高能效运行前沿模型推理。Etched 成立于 2022 年，累计融资 **8 亿美元**（最新一轮去年 12 月闭市 5 亿美元，**投后估值 50 亿美元**），由 Stripes 领投；天使投资人包括 **Andrej Karpathy、Geoffrey Hinton、Fei-Fei Li、Arthur Mensch、Scott Wu** 等。
  > 💡 Etched 是「专用推理芯片吞噬 GPU 通用算力」叙事的代表标的，10 亿美元订单（合同额而非已确认收入）与 Karpathy/Hinton 等顶级研究者站台，使其成为继 Cerebras、Groq 之后又一家冲击 NVIDIA 推理垄断的百亿美元级玩家。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/30/nvidia-competitor-etched-hits-5b-valuation-1b-in-sales-for-ai-chip/)

### 研究关注
**SARL（Berkeley）：把 VLA 语言 prompt 当作 RL「语义动作」，100 episode 内适配真机**
- 论文《Adapting Generalist Robot Policies with Semantic Reinforcement Learning》（作者 Jagdeep Singh Bhatia、Andrew Wagenmaker、William Chen、Sergey Levine，UC Berkeley，CoRL 2026）提出 **SARL**：不直接对机器人动作做 RL，而是**把 VLA 的语言 prompt 当作 RL「语义动作」**来优化。动机：标准动作空间 RL 要求基础策略分布接近目标，对 OOD 长程任务失效；而通用策略的语言接口本身已编码大量技能。SARL 学习把任务分解为接地技能、搜索能取得进展的 prompt，组合已有技能完成零样本做不到的长程行为，在真实 **WidowX 上不到 100 episode** 完成适配，解决了动作空间 RL 与 VLM prompting 都搞不定的任务。
  > 💡 「在语言上做 RL 而非在动作上做 RL」是对通用机器人策略下游适配的一条新路径——把语言接口当作可学习的规划层，绕开动作空间 RL 的分布假设瓶颈，也呼应「VLA 作为技能库 + 外挂轻量决策头」的整体趋势。
   - 来源: [项目页](https://semantic-action-rl.github.io/)

**Dockerless：无需执行环境的编程 Agent 补丁验证器，SWE-bench Verified 解决率 62.0%**
- 论文《Dockerless: Environment-Free Program Verifier for Coding Agents》（作者 Wenhao Zeng、Yuling Shi、Xiaodong Gu 等）提出**无需执行环境**的 Agent 代码补丁验证器。程序验证器在 Agent 训练中关键（为 SFT 选轨迹、为 RL 提供奖励），而标准执行式需 Docker 跑单测、搭建成本高。Dockerless 不执行代码，而是通过 **Agent 式仓库探索** 判断补丁正确性，在验证基准上较最强开源验证器高 **14.3 AUC**。以其作为 SFT 轨迹过滤与 RL 奖励可构成全流程无环境 post-training，所得模型在 **SWE-bench Verified / Multilingual / Pro 上分别 62.0% / 50.0% / 35.2%**，较 Qwen3.5-9B 基线提升 2.4 / 8.7 / 2.9 个点，追平依赖环境的 post-training。
  > 💡 去除 Docker/执行依赖可大幅降低编程 Agent 训练与评估的部署门槛，尤其利于企业内网与受限环境；把「验证」从执行式转为 Agent 探索式，也呼应了 Agent 评估方法本身 Agent 化的趋势。
   - 来源: [arXiv](https://arxiv.org/abs/2606.28436) | [HuggingFace Daily Papers](https://huggingface.co/papers/2606.28436)

**Orca：学习统一世界潜空间的通用世界基座模型，预训练 12.5 万小时视频**
- 论文《Orca: The World is in Your Mind》（作者 Yihao Wang、Yuheng Ji、Mingyu Cao 等）提出通用世界基座模型 **Orca**，从多模态世界信号中学习**统一的世界潜空间**，再通过多模态读出接口对外暴露。核心设计是以 **Next-State-Prediction（下一状态预测）** 统一替代孤立的 next-token / next-frame / next-action 建模。训练分两个范式：**无意识学习**从连续视频中捕捉密集自然状态转移，**有意识学习**以语言描述的事件与 VQA 监督建模稀疏关键转移；预训练数据含 **12.5 万小时视频与 1.6 亿条事件标注**。主干冻结、仅训练轻量模态解码器，在文本生成、图像预测、具身动作生成三类下游读出上验证「更强的世界潜空间 → 更强的下游能力」，并超越同等规模的专用基线。
  > 💡 把 next-state-prediction 作为统一建模路线，是绕开「语言/视频/动作各自预测」割裂、走向统一世界模型的一条技术路径；冻结主干 + 可训练解码器的设计也利于多任务复用。
   - 来源: [arXiv](https://arxiv.org/abs/2606.30534) | [HuggingFace Daily Papers](https://huggingface.co/papers/2606.30534)

**MIT 团队用 AI Agent 大规模黑盒审计推荐算法，1120 个 agent 在 X 上采集 20 万次曝光**
- 论文《Using AI Agents to Automate Black-Box Audits of Personalization Algorithms at Scale》（作者 Alessandro Morosini、Sarah H. Cen、Andrew Ilyas、Aleksander Mądry、Chara Podimata 等，MIT）提出用生成式 AI Agent 做合成账号的「行为引擎」来黑盒审计平台推荐算法。传统审计两难：真实用户成本高难控制，马甲号可扩展但行为脚本化失真，且都难把属性与行为解耦 → 限制因果推断。该框架给每个 Agent 设固定 persona（基于人口统计与政治倾向数据）、像真人一样推理选择行为，在保持 persona 不变的同时扰动年龄/性别/地域等可见信号，实现反事实审计。案例：**2024 年大选后在 X 部署 1120 个 agent、14 类 persona × 3 种反事实条件、采集超 20 万次内容曝光**，发现 X 推荐流较时间线放大有毒/极化/政治化/右倾内容，且放大程度随用户意识形态显著变化。
  > 💡 把 AI Agent 当作「可控合成用户」打破了几十年来推荐算法审计的样本与因果瓶颈，使大规模、可重复、可归因的平台算法稽查成为可能；其方法学与对 X 推荐流的实证结论，对平台监管与算法问责都具有直接工具价值。
   - 来源: [arXiv](https://arxiv.org/abs/2606.30801)

**邢波团队《Critique of Agent Model》：区分 agentic/agentive 系统，提出 GIC 通用 Agent 架构**
- MBZUAI 校长、CMU 教授 Eric Xing（邢波）与 Mingkai Deng、Jinyu Hou 等发表论文《Critique of Agent Model》，从「何为 agent、何为 agency」的根本问题切入，回应 LLM 类「coding agent / AI co-scientist」被泛化营销与「机器 agency 失控」的担忧。论文援引 Descartes 将 agency 根植于独立思考的论述，沿**目标、身份、决策、自我调节、学习**五个维度分析现有 Agent 架构，核心论点是：真正的 agency 要求这些结构**内生于系统本身**，而非靠外部脚手架拼装。据此区分两类系统——**agentic**（能力来自工程化工作流）与 **agentive**（能力内生涌现、含社会交互），前者只完成预设任务，后者才能在开放世界真正自主。基于此，论文提出面向通用 Agent 的 **GIC（Goal-Identity-Configurator）架构**，结合层次化目标分解与身份机制。
  > 💡 这是对当前「把带工具调用的 LLM 流水线称作 agent」这一泛化叙事的正面反驳，agentic / agentive 二分可为 Agent 能力评估与监管讨论提供更清晰的语言；GIC 架构若可工程化，将影响通用 Agent 的设计基准。
   - 来源: [arXiv](https://arxiv.org/abs/2606.23991) | [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651042107&idx=2&sn=455937649735c225e976b085ef82100c&chksm=85c3b4409b012ae160eb099d7b2b1b93d4d37c65a4cb43396aa0d4eb103c87a9225482dd43fa&scene=0&xtrack=1#rd)

**UniTac：首个面向跨传感器触觉理解与生成的统一多模态模型**
- 论文《UniTac: A Unified Multimodal Model for Cross-Sensor Tactile Understanding and Generation》（作者 Jiahang Tu、Fengyu Yang、Chenyang Ma、Xihang Yu、Ziyao Zeng、Shaokai Wu、Hanbin Zhao、Zhi Tao）提出首个面向触觉的统一多模态模型 **UniTac**。针对统一多模态模型很少延伸到触觉、且触觉意义由「物体语义」与「传感器配置」共同决定的问题，UniTac 将触觉过程建模为「非接触→接触」的转移，用**双层表征同时编码传感器与物体属性**。理解侧设两项任务（物体属性描述、传感器识别）以强化对物理与跨传感器信息的推理；生成侧采用「重建 + 对齐」两阶段训练范式，并设计基于传感器先验的采样策略以模拟真实触觉接触。在大规模多传感器数据上训练后，UniTac 在触觉理解上达到 SOTA，并能跨传感器生成真实触觉信号。
  > 💡 触觉是大模型多模态版图里相对被忽视的一维，UniTac 把「统一理解 + 生成」范式扩展到触觉并提出跨传感器表征，是补齐具身智能感知侧的关键一步，价值主要在机器人触觉反馈与材料/抓取建模。
   - 来源: [arXiv](https://arxiv.org/abs/2606.31451)

### X讨论
**Google DeepMind 披露 SynthID 进展：已为 1000 亿张图片/视频打水印，联合 OpenAI/NVIDIA/Apple 推广**
- Google DeepMind 回顾其 2023 年推出的 AI 内容水印技术 **SynthID** 进展：该技术在 AI 生成内容中嵌入隐藏数字水印，最初面向图像，现已扩展至视频、音频与文本。截至目前已为**超 1000 亿张图片与视频**、以及**约 6 万年时长的音频**打上水印；用户可在 Google Search、Chrome 内的 Gemini 及 Gemini App 中直接用 SynthID 验证内容，累计使用**超 5000 万次**。DeepMind 另在 Gemini App 等生成式工具中采用 **C2PA Content Credentials** 标准，水印之外可显示图像/视频的来源与修改痕迹；文本水印技术已**开源**，并正与 **OpenAI、NVIDIA、Apple** 合作将 SynthID 推广至更多生成式媒体。
  > 💡 内容标识正从「合规要求」升级为 AI 生成内容的基础信任设施；1000 亿级水印存量 + 三大入口内置核验，意味着 SynthID 事实上正成为 AI 内容溯源的行业标准，拉拢 OpenAI/NVIDIA/Apple 入局是抢占 provenance 标准的关键一步。
   - 来源: [@googleai](https://x.com/GoogleAI/status/2072318809277390940#m)

**SemiAnalysis 解析推理成本切割：每次推理被持续拆解推动智能成本下降**
- SemiAnalysis 梳理推理服务中被持续拆解的三层切割，并点出 MLSys 2026 的核心叙事即「每一切片都让智能更便宜」：**Phase（阶段）**——prefill 读 prompt 放一组芯片、decode 逐 token 写回答放另一组芯片，各跑各自最优的硬件；**Layer（层）**——attention 需要 HBM 高内存带宽跑 token 共享上下文，feed-forward 计算密集则放 SRAM 芯片；**Time（时间）**——最新切法，用 interleave 将任务切碎成执行窗口在不同 machine 间快速切换，什么都不让闲着。根本模式：**找到空闲算力并填满它**。每填一分，单位智能成本降一分；更便宜的 token 不会缩小需求，而是放大它。
  > 💡 推理经济正从「单阶段/单芯片计价」转向「阶段/层/时间多维度拆分工况计价」，这种微观经济层面的持续切分将不断降低智能成本门槛，使推理需求加速膨胀而非饱和。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2072417511987978298#m)

**Peter Steinberger用 Codex 改进 OpenClaw iOS 应用，基于两条 X 反馈完成首轮迭代**
- Peter Steinberger将用户在 X 上的反馈输入 Codex，由 Codex 对 iOS 应用进行了第一轮自动改进。开发者评价「仍然不够好，但就两个 prompt 而言不算差」，并特别提到 Codex 使用 **computer use** 自动生成了改前/改后截图对比（GitHub 无此 API），令改进结果更直观。
  > 💡 Codex 等编程 Agent 正嵌入到「收集 X 反馈 → 自动改版 → computer use 自动加截图证据」的轻量闭环中，截图补上了可视化说服力这一关键环节。
   - 来源: [@steipete](https://x.com/steipete/status/2072439279520039380#m)

**Krea 2 技术报告：开权重文生图基座 K2 Raw / K2 Turbo，用 SAE 做数据策展**
- Krea 发布 Krea 2（K2）技术报告——面向**创意探索**的开权重文生图基座，放出 **K2 Raw 与 K2 Turbo** 两套开权重。报告指出现今文生图系统普遍收敛到单一默认美学、不利创意探索，K2 从零自建大规模数据基础设施与分布式训练框架，预训练数据强调广世界知识与风格覆盖，训练采用**预训练 → midtraining → SFT → 偏好优化 → RL** 多阶段流水线。数据策展上，除常规质量过滤外，还**在 SigLIP-2 嵌入上训练稀疏自编码器（SAE）**对预训练语料做策展与探索——即可解释性工具被用于数据侧而非仅模型侧。
  > 💡 K2 把「创意探索」而非「单一精美默认输出」作为产品定位，差异化于主流 T2I；SAE 用于数据策展则代表可解释性研究从「解释模型」反哺到「解释与筛选数据」，是数据工程的新工具。
   - 来源: [Krea Blog](https://www.krea.ai/blog/krea-2-technical-report) | [@thesephist](https://x.com/thesephist/status/2072439816503820379#m)

**波士顿动力Spot机器人参与2026世界杯安保工作**
- 波士顿动力宣布Spot四足机器人已分配新任务，用于协助覆盖16座主办城市、3个国家的2026 FIFA世界杯安保工作。这是该赛事史上规模最大的安保部署之一。Spot将承担巡逻、监控等具体职责，具体功能与部署规模需参考官方公告进一步确认。
  > 💡 Spot进入世界杯级公共安全场景验证了商用机器人在大型活动中的实用性，但具体任务边界（是否涉及AI自主决策）尚不明确，需关注后续技术披露。
   - 来源: [@bostondynamics](https://x.com/BostonDynamics/status/2072314808251162822#m)

---
*更新时间: 2026-07-02 07:44*