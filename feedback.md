# News Pipeline Feedback Log

Daily corrections accumulated from user reviews. Each entry is a structured training example for future prompt optimization (DSPy).

## Entry Format

```
### [DATE] #NN
- **file**: daily-ai-news-YYYY-MM-DD.html
- **field**: title | body | key_points | category | filter
- **before**: (原文)
- **after**: (修正后)
- **reason**: (为什么改)
- **rule_hint**: (可提炼的通用规则，可选)
```

---

## Corrections

### [2026-04-24] #01
- **file**: daily-ai-news-2026-03-08.html
- **field**: title
- **before**: OpenAI再次推迟ChatGPT成人模式发布
- **after**: 谢赛宁团队开源多人游戏视角世界模型
- **reason**: 大标题应该抓最重要的动态，而非随机取第一条。谢赛宁团队开源世界模型比OpenAI推迟成人模式更重要。
- **rule_hint**: 标题应取当天最有影响力的动态，不是简单取第一条

### [2026-04-24] #02
- **field**: body
- **before**: (多条body缺少"为什么重要")
- **after**: (要求每条body必须有so what判断)
- **reason**: body写得像新闻聚合，没有判断和"意味着什么"
- **rule_hint**: body必须有so what，读完能跟人聊，关键判断加粗

### [2026-04-24] #03
- **field**: filter
- **before**: 多条新闻源链接为nitter.net开头，打不开
- **after**: 修复为正确的x.com链接
- **reason**: nitter.net是Twitter镜像服务，经常失效
- **rule_hint**: 检查来源链接可用性，nitter.net链接需替换

### [2026-04-24] #04
- **field**: filter
- **before**: (多条insight为空)
- **after**: (确保所有文章都有insight)
- **reason**: 30+个HTML文件缺失insight/key_points
- **rule_hint**: 每条新闻必须至少有1条key_point/insight

### [2026-04-24] #05
- **field**: title
- **before**: 标题带感叹号/夸张口吻
- **after**: 去掉感叹号和夸张表述
- **reason**: 新闻标题应客观准确，不用媒体夸张口吻
- **rule_hint**: 标题禁止感叹号、夸张词（彻底、硬核、重磅等）

### [2026-04-24] #06
- **field**: body
- **before**: 海外公司/人名翻译为中文（如"开放AI"、"奥特曼"）
- **after**: 保持英文原名（OpenAI、Sam Altman）
- **reason**: 行业通用英文名更易识别和搜索
- **rule_hint**: 海外公司/人名不翻译，保持英文原名

### [2026-04-24] #07
- **field**: key_points
- **before**: (summary要点速览中"展开阐释+关键细节+..."这行描述文字)
- **after**: 去掉，只保留关键事实
- **reason**: 描述性文字没有信息量
- **rule_hint**: 要点速览只写关键事实，不写描述文字

### [2026-04-24] #08
- **field**: key_points
- **before**: key_points写成核心判断
- **after**: key_points只写关键事实（是什么、关键突破、影响）
- **reason**: 核心判断应在body里，key_points只放事实
- **rule_hint**: key_points不重复标题已说的内容，不写核心判断，数据/细节优先

---

### [2026-04-28] #16
- **field**: body
- **before**: FedRAMP仅2句、Brev仅2句、天然气电厂仅2句、TPU仅2句，均未达3句下限
- **after**: body不足3句的条目要么从源补充更多信息，要么合并到相关条目
- **reason**: "3-6句话"是已有规则但从未被enforce，body不足3句的条目读完无法跟人聊
- **rule_hint**: **body硬性下限3句。不足3句时：(1) 去官方源挖更多数据补到3句；(2) 如果来源不可达，标注⚠️并只写已确认事实。注意：不足3句时禁止编造内容凑数（参见#22-#25）**

### [2026-04-28] #17
- **field**: body
- **before**: body规则要求写"基于事实的so what"，导致AI每次往body里塞自己的判断
- **after**: body只写事实、数据、关键影响、具体人物/公司的评价观点；AI自己的so what/判断全部放insight
- **reason**: body和insight边界不清，AI的判断混入body降低了事实密度
- **rule_hint**: **body允许的内容：事实、数据、关键影响（市场反应/股价等）、具体人物或公司的评价观点（需注明谁说的）。body禁止的内容：AI自己的判断/so what/趋势预测，这些全部放insight**

---

### [2026-04-30] #18
- **field**: title
- **before**: Ling-2.6-1T 正文写"26B参数"
- **after**: 改为"万亿参数"（模型名1T=1 Trillion）
- **reason**: 模型名中的规模标识与正文参数量描述矛盾
- **rule_hint**: **模型名中的数字（如1T=万亿参数、7B=70亿参数）必须与正文参数量描述交叉验证，不能只看部分信息源**

### [2026-04-30] #19
- **field**: filter
- **before**: OpenAI网络安全方案和Codex决策对比各占一条独立条目
- **after**: 合并为一条"OpenAI发布网络安全方案+展示Codex决策辅助能力"
- **reason**: 同公司同日发布的低权重动态各自独立会稀释信息密度
- **rule_hint**: **同公司同日多条低权重动态（非核心产品发布/财报级）合并为一条，取"公司+多项动态"格式**

### [2026-04-30] #20
- **field**: filter
- **before**: GPT-5.5 Pro 159分和Gemini音频前7各占一条
- **after**: 合并为一条"本周评测动态：GPT-5.5 Pro创Epoch新高159分，Gemini包揽音频前7"
- **reason**: 同为benchmark评测结果，分开展示增加条目数但不增加信息密度
- **rule_hint**: **同类型benchmark/评测结果可合并为一条"本周评测动态"，将多个结果并列展示**

### [2026-04-30] #21
- **field**: category
- **before**: Google Cloud $200亿营收归入产业动态
- **after**: 移入算力追踪
- **reason**: 该条核心信号是"算力供给瓶颈限制增长"，不是一般的产业营收新闻
- **rule_hint**: **分类由内容的核心信号决定而非表面主题。财报中突出"算力瓶颈/供给限制"的归算力追踪，突出"用户增长/产品收入"的归产业动态**

---

<!-- Future corrections will be appended below -->
<!-- Format: copy the ### entry template above, fill in details -->

### [2026-04-25] #09
- **field**: body
- **before**: 多条body信息密度极低：DeepSeek-V4只有"支持百万token"、Grok Voice只有"快速响应和高精度"、Anthropic降智只有"三个Bug导致"、Workspaces只有"协作工作空间"
- **after**: 全部补充具体数据：V4参数量/benchmark/定价、Grok τ-voice Bench登顶/Starlink 20%转化率、Anthropic三个Bug具体内容、Workspaces API密钥/配额/路由
- **reason**: slogan级描述没有信息量，读者看完无法跟人聊，用户每次都要手动去官方源补充
- **rule_hint**: **body必须有可量化的具体数据（参数量、benchmark排名、价格、转化率等）。如果只能写出一句泛泛描述，必须去官方源（官网/blog/API docs/arxiv）挖具体数据，挖不到时在输出中标注「⚠️ 缺少具体数据，需人工补充」。禁止"具备XX特点""引发关注"等空洞表述**

### [2026-04-25] #10
- **field**: category
- **before**: "OpenAI与NVIDIA合作在公司范围内部署Codex" 分类为 X讨论
- **after**: 改为 产业动态
- **reason**: 企业级部署合作是产业动态
- **rule_hint**: 企业合作/部署案例归产业动态，不归X讨论，即使信息来源是推特

### [2026-04-25] #11
- **field**: filter
- **before**: 姚顺雨同时出现在「研究关注」和「X讨论」要点汇总中
- **after**: 只保留在 X讨论
- **reason**: 同一条新闻不应出现在两个分类中
- **rule_hint**: 同一条新闻只归属一个分类

### [2026-04-25] #12
- **field**: filter
- **before**: 来源链接只有机器之心，GPT-5.5等4/24新闻在4/25重复出现
- **after**: 补充官方一手来源（anthropic.com/x.ai blog/deepseek API docs）作为主来源，原有链接保留；跨天去重增加实体匹配层
- **reason**: 有官方一手源时应优先引用；Jaccard去重对"同一事件换种说法"失效（GPT-5.5 Jaccard仅0.18）
- **rule_hint**: 有官方一手来源时优先引用，新来源作为补充不替换原有链接。跨天去重不能只靠文字相似度，需要实体级匹配（公司+产品名）

### [2026-04-26] #13
- **field**: body
- **before**: Chelsea Finn演讲"首次透露π0.7机器人模型"
- **after**: π0.7已于4/16发布，演讲中只是引用，删除"首次透露"
- **reason**: 模型/产品已在之前发布，后续演讲/报道中提及不等于首次公开
- **rule_hint**: 提到模型/产品发布时，必须核实是否已在更早时间点正式发布。不能因为首次在某人的演讲/推文中看到就标注"首次发布/透露"

### [2026-04-26] #14
- **field**: filter
- **before**: "前馈式3D重建路线图发布"来源标注为机器之心
- **after**: 改为arXiv论文作为一手来源，机器之心为补充
- **reason**: 机器之心是报道媒体，不是论文作者。媒体转载≠原创
- **rule_hint**: 来源区分"报道媒体"和"原始出处"。论文/研究类新闻必须以arXiv/期刊/会议为第一来源，媒体链接作为补充。当body提到具体论文编号（如arXiv 2604.14025），必须以该论文为一手来源

### [2026-04-26] #15
- **field**: body
- **before**: Google/Anthropic body只有首期金额和估值，缺少后续条件、Amazon同期投资、循环交易争议
- **after**: 从深科技文章补充后续$300亿业绩目标、Amazon $50亿+$200亿、Anthropic营收$90亿→$300亿、哈佛PON质疑
- **reason**: 同一事件多条来源时，应合并最丰富的数据维度，而非取单条来源的子集
- **rule_hint**: 同一事件有多条来源时，合并所有来源的关键数据，取信息密度最高的版本。具体做法：以最早/最权威来源为骨架，从其他来源补充其缺少的数据（金额细节、对比数据、争议观点）

---

### [2026-05-05] #22
- **file**: daily-ai-news-2026-05-03.md
- **field**: body
- **before**: "DeepTech深科技发表分析文章，提出'神经计算机'概念框架。文章将此类比为从'使用工具'到'成为工具'的跃迁，认为这是Agent从tool-use走向tool-creation的理论基础。"
- **after**: 从arXiv 2604.06425读取准确信息：Meta田渊栋+KAUST诸葛鸣晨+Schmidhuber等提出Neural Computers，将计算/内存/I/O统一到学习的运行时状态中，用视频模型在CLI/GUI环境验证接口原语学习
- **reason**: 原body存在严重幻觉：(1) 把媒体DeepTech当成概念提出者，实际是Meta+KAUST的论文；(2) "从使用工具到成为工具""tool-use走向tool-creation"等具体表述完全编造，原文无此内容
- **rule_hint**: **写body前必须读原文。禁止凭pipeline摘要扩写/润色。如果来源是媒体报道研究成果，必须区分"报道者"和"研究者"，去找论文原文确认具体内容。编造具体表述/类比是最严重的质量事故。**

### [2026-05-05] #23
- **file**: daily-ai-news-2026-05-03.md
- **field**: body
- **before**: "北大博士休学创业，自研异构计算架构，通过CPU/GPU/专用加速器协同调度优化Agent推理效率"
- **after**: 2000年出生的林修醇休学创办荆华密算，联合清华任炬教授实验室推进密态计算商业化，已完成种子轮+天使轮数千万融资
- **reason**: 原body完全跑偏——实际是密态计算（同态加密），不是异构计算架构。人名、公司名、技术方向全部错误，属于未读原文凭标题臆测内容
- **rule_hint**: **当来源不可达（如微信反爬）且无法验证内容时，禁止凭标题/摘要臆测body细节。应标注"⚠️ 来源未验证"并只写已确认的最小事实集，或请用户提供更多信息**

### [2026-05-05] #24
- **file**: daily-ai-news-2026-05-03.md
- **field**: body
- **before**: "这是首个针对'Agent网络'而非单个Agent的安全评估框架"
- **after**: 删除"首个"判断。原文Prior work段明确提到Prompt Infection、ClawWorm、Agents of Chaos等先行工作
- **reason**: 原文自己列举了prior work，说明不是"首个"。AI编造了"首个"这一绝对性判断
- **rule_hint**: **禁止无来源的绝对性判断（"首个""首次""最大""首选"等）。这类表述必须有原文明确支撑。如果原文自己提到了prior work/竞品，则绝对不能称"首个"**

### [2026-05-05] #25
- **file**: daily-ai-news-2026-05-03.md
- **field**: body
- **before**: "此前vLLM已是DeepSeek V4推理的首选引擎，本次更新进一步巩固了其在开源推理栈中的核心地位"
- **after**: 删除该句。vLLM推文只说了"10+ bug fixes and optimizations"，未声称自己是"首选引擎"或"核心地位"
- **reason**: 无来源的市场地位判断，属于AI自行添加的"拔高"表述
- **rule_hint**: **body中禁止无来源的市场地位/竞争格局判断（"首选""核心地位""领先"等）。这类判断如果要写，必须放insight且标注是AI分析，不能混入body伪装成事实**

---

### [2026-05-09] #26
- **file**: daily-ai-news-2026-05-09.md
- **field**: body
- **before**: EMO条目中机构归属错误——来源链接明确为 huggingface.co/blog/allenai/emo，body中也写了"Allen AI的Ryan Wang..."，但管线处理阶段曾将其错误归属为Meta
- **after**: 确认为Allen AI (AI2)的工作，非Meta
- **reason**: 来源链接已明确标注allenai，QA环节未交叉校验机构归属
- **rule_hint**: **QA必须交叉校验：来源链接中的机构标识（如URL路径中的allenai/google/meta）必须与body中提到的机构名一致。发现不一致时立即标记为事实错误。这是最高优先级的校验项——机构归属错误比分类错误严重得多**

### [2026-05-09] #27
- **file**: daily-ai-news-2026-05-09.md
- **field**: category
- **before**: Anthropic安全干预方法研究、OpenAI CoT优化压力研究被归入"X讨论"
- **after**: 移入"研究关注"
- **reason**: 内容是正式研究博文/论文，不是X平台讨论。来源虽含X推文链接，但核心内容是研究成果
- **rule_hint**: **分类以内容语义为准，不以来源渠道为准。官方研究博文/论文即使通过X推文传播，仍归"研究关注"。"X讨论"仅用于：(1)纯社区讨论/观点；(2)产品演示视频/动态；(3)无正式博文/论文支撑的碎片信息**

### [2026-05-09] #28
- **file**: daily-ai-news-2026-05-09.md
- **field**: filter
- **before**: OpenAI Codex Chrome插件推文未被管线自动收录
- **after**: 手动补充为产业动态条目
- **reason**: 采集窗口或关键词匹配遗漏了OpenAI官方推文
- **rule_hint**: **OpenAI/Anthropic/Google等头部厂商的官方产品更新推文不应被遗漏。采集后应有一轮"头部厂商官方账号覆盖检查"**

### [2026-05-10] #29
- **file**: daily-ai-news-2026-05-10.md
- **field**: body
- **before**: "谷歌DeepMind Pushmeet Kohli发布AI for Math最新成果，刷新数学AI基准SOTA。牛津教授使用该工具解开群论悬案。"（2句，无具体benchmark数据，slogan级描述）
- **after**: 补充AI co-mathematician是多Agent系统、FrontierMath Tier 4得分**48%**（创AI最高分）、测试领域（群论/哈密顿系统/代数组合）、对比GPT-5.5 Pro 39.6%、Gemini Deep Think IMO金牌、AlphaEvolve具体成果
- **reason**: 原body完全无量化数据，"刷新SOTA""群论悬案"均为空洞表述。从Pushmeet LinkedIn帖子和Google Blog补充具体数据后信息密度显著提升
- **rule_hint**: **模型/系统发布类新闻必须包含至少1个具体benchmark数据点（分数/排名/对比）。"刷新SOTA"本身不是数据，必须写明在哪个benchmark上、具体多少分。缺乏数据时优先搜索官方博客/LinkedIn帖子/技术论文**

### [2026-05-10] #30
- **file**: daily-ai-news-2026-05-10.md
- **field**: body
- **before**: "英伟达2026年内已承诺$400亿用于AI相关股权投资交易。英伟达在传统GPU销售商业模式之外，通过资本投资深入参与AI产业链，扩展其在AI领域的影响力。"（2句，第2句纯filler）
- **after**: 补充$300亿投向OpenAI、Corning $32亿、IREN $21亿、2025年67笔VC、2026年24轮私募、Wedbush分析师"circular investment theme"评价
- **reason**: 第2句"深入参与产业链扩展影响力"是零信息增量的filler。TechCrunch原文有丰富数据（OpenAI $300亿等），未读取就写body
- **rule_hint**: **融资/投资类新闻必须拆解资金构成（最大单笔→谁→多少钱、其他投资→几笔→总额多少），不能只写一个总数。对比数据（同比/上期）和第三方评价（分析师观点）是信息密度的关键增量**

### [2026-05-10] #31
- **file**: daily-ai-news-2026-05-10.md
- **field**: body
- **before**: "Robo.ai宣布收购Neurovia AI，后者是一家AI数据处理与压缩技术研发商...产品广泛赋能自动驾驶、智慧城市、无人设备及智能制造等场景。本次收购将强化Robo.ai在机器人数据基础设施方面的能力。"（营销稿体，无交易金额/结构）
- **after**: 补充$1亿全股票、Class B股、8年锁定期、NASDAQ: AIIO、股价飙升70%、具体应用场景
- **reason**: 原body直接复制IT桔子摘录，含"广泛赋能"等marketing fluff，缺少交易金额/结构/市场反应等核心事实。PRNewswire官方新闻稿有完整数据
- **rule_hint**: **收购/M&A类新闻的核心要素：交易金额、支付方式（现金/股票/混合）、锁定期/earn-out、卖方核心资产、市场反应（股价变动）。来源优先级：PRNewswire官方稿 > 财经媒体 > IT桔子。禁止使用"广泛赋能""致力于"等营销稿措辞**

### [2026-05-10] #32
- **file**: daily-ai-news-2026-05-10.md
- **field**: body
- **before**: "该技术为AI Agent的安全性提供技术保障，填补Agent治理领域的技术空白。"
- **after**: 删除"填补Agent治理领域的技术空白"。Agent安全/Guardrails赛道已有NVIDIA NeMo Guardrails、Lakera等先行项目
- **reason**: "填补技术空白"是无来源的绝对性判断，违反"禁止无来源的绝对性判断"规则
- **rule_hint**: **"填补空白""首创""填补技术空白"与"首个""首次"同属绝对性判断，必须由原文明确支撑。Agent安全赛道已有多个开源项目，不能因为中文媒体报道未提竞品就称"填补空白"**

### [2026-05-10] #33
- **file**: daily-ai-news-2026-05-10.md
- **field**: body
- **before**: 多个⚠️来源不可达条目的body仍包含无法验证的具体细节（如通义千问眼镜"支持主动提醒用户并帮忙叫车"）
- **after**: 通义千问眼镜降级为"据报发布，具体参数无法验证"；浙大知识图谱删除"覆盖学科最多、规模最大"的绝对性判断；Claude Code源码解析标注"二次解读非一手源"；SGL/Radixark标注"具体benchmark数据待补充"
- **reason**: 来源不可达时，body中的具体细节同样不可验证，应一并降级。按规则"只写已确认的最小事实集"
- **rule_hint**: **⚠️标注的降级规则应覆盖body中所有具体声明，不只加标签但保留细节。如果来源不可达，body中任何"支持XX功能""实现XX效果"的描述都是不可验证的，应缩减为"据报XX，细节待验证"**
