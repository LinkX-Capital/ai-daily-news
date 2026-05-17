# News Pipeline Feedback Log

Daily corrections accumulated from user reviews. Each entry is a structured training example for future prompt optimization (DSPy).

## Entry Format

```
### [DATE] #NN
- **file**: daily-ai-news-YYYY-MM-DD.md
- **field**: title | body | key_points | category | filter | source
- **before**: (原文)
- **after**: (修正后)
- **reason**: (为什么改)
- **rule_hint**: (可提炼的通用规则)
```

## Rule Index

| 类别 | 编号 | 关键词 |
|------|------|--------|
| **title** | #01 | 取最有影响力的动态 |
| **title** | #05 | 禁止感叹号/夸张口吻 |
| **title** | #18 | 模型名规模与正文交叉验证 |
| **title** | #38 | 标题动词匹配内容性质（禁止"发布"万能化） |
| **title** | #49 | 标题必须含"谁+做了什么+关键区分点"，禁止"论文提出""研究发现"万能开头 |
| **body — 核心原则** | #45 | ⭐ 来源里没有的信息不写，宁可短一句不编一词（反幻觉硬门槛） |
| **body — 事实密度** | #29 | 数据必须回答"为什么重要"，不是越多越好；禁止凑数（arXiv编号、作者人数、提交日期、版本号、页数等不影响理解的数字） |
| **body — 事实密度** | #30 | 融资/投资拆解资金构成 |
| **body — 事实密度** | #31 | 收购/M&A核心要素 |
| **body — 事实密度** | #36 | 来源归属：区分官方发布 vs hackathon/个人项目 |
| **body — body vs insight** | #17 | body只写事实，AI判断→insight |
| **body — body vs insight** | #35 | body自检黑名单：禁止"表明""反映""实验达到SOTA精度""大幅提升性能"等无具体数据的空洞句式 |
| **body — 绝对性判断** | #32 | 禁止无来源绝对性判断（首个/首次/首选/核心地位/迄今最…） |
| **body — 降级/截断** | #23 | 来源不可达时标注⚠️只写最小事实集 |
| **body — 降级/截断** | #37 | 截断检测：单字结尾/未闭合引号触发重新生成 |
| **body — 媒体与论文** | #22 | 写body前必须读原文，区分报道者和研究者 |
| **body — 媒体与论文** | #46 | 媒体原文事实性描述默认保留，仅当与一手来源矛盾时才修改；补充≠替换 |
| **body — 多源合并** | #15 | 同一事件多来源合并最丰富数据 |
| **body — 格式** | #47 | 链接只出现在来源行，body禁止inline markdown链接 |
| **key_points** | #04 | 每条新闻必须有≥1条insight |
| **key_points** | #07 | 要点速览只写关键事实，不写描述文字 |
| **category** | #10 | 企业合作→产业动态，非X讨论 |
| **category** | #21 | 分类由核心信号决定，非表面主题 |
| **category** | #27 | 研究博文→研究关注，非X讨论 |
| **filter** | #03 | 检查来源链接可用性（替换nitter.net） |
| **filter** | #11 | 同一条新闻只归属一个分类 |
| **filter** | #12 | 跨天去重需实体级匹配 |
| **filter** | #13 | "首次发布"需核实是否已更早发布 |
| **filter** | #19 | 同公司同日多条低权重动态合并 |
| **filter** | #20 | 同类benchmark结果合并为一条 |
| **filter** | #28 | 头部厂商官方账号覆盖检查 |
| **source** | #06 | 海外公司/人名保持英文 |
| **source** | #14 | 论文以arXiv为一手源，媒体为补充 |
| **source** | #26 | 交叉校验URL中的机构标识 |
| **source** | #34 | arXiv链接格式：`[arXiv](URL)` |
| **source** | #41 | 研究类新闻：主动查找arXiv是第一步，不是补充步骤 |
| **source** | #42 | 媒体来源body不足时：用标题/摘要反向搜索原始来源 |
| **pipeline** | #50 | 任何写入/覆盖文件的命令执行前，确认目标文件是否已被手动编辑 |

**图例：** 🔗 = 已合并至更新条目

---

## Corrections

### [2026-04-24] #01
- **file**: daily-ai-news-2026-03-08.html
- **field**: title
- **before**: OpenAI再次推迟ChatGPT成人模式发布
- **after**: 谢赛宁团队开源多人游戏视角世界模型
- **reason**: 大标题应该抓最重要的动态，而非随机取第一条。谢赛宁团队开源世界模型比OpenAI推迟成人模式更重要。
- **rule_hint**: 标题应取当天最有影响力的动态，不是简单取第一条

### [2026-04-24] #03
- **file**: daily-ai-news-2026-03-08.html
- **field**: filter
- **before**: 多条新闻源链接为nitter.net开头，打不开
- **after**: 修复为正确的x.com链接
- **reason**: nitter.net是Twitter镜像服务，经常失效
- **rule_hint**: 检查来源链接可用性，nitter.net链接需替换

### [2026-04-24] #04
- **file**: daily-ai-news-2026-03-08.html
- **field**: key_points
- **before**: (多条insight为空)
- **after**: (确保所有文章都有insight)
- **reason**: 30+个HTML文件缺失insight/key_points
- **rule_hint**: 每条新闻必须至少有1条key_point/insight

### [2026-04-24] #05
- **file**: daily-ai-news-2026-03-08.html
- **field**: title
- **before**: 标题带感叹号/夸张口吻
- **after**: 去掉感叹号和夸张表述
- **reason**: 新闻标题应客观准确，不用媒体夸张口吻
- **rule_hint**: 标题禁止感叹号、夸张词（彻底、硬核、重磅等）

### [2026-04-24] #06
- **file**: daily-ai-news-2026-03-08.html
- **field**: source
- **before**: 海外公司/人名翻译为中文（如"开放AI"、"奥特曼"）
- **after**: 保持英文原名（OpenAI、Sam Altman）
- **reason**: 行业通用英文名更易识别和搜索
- **rule_hint**: 海外公司/人名不翻译，保持英文原名

### [2026-04-24] #07
- **file**: daily-ai-news-2026-03-08.html
- **field**: key_points
- **before**: (summary要点速览中"展开阐释+关键细节+..."这行描述文字)
- **after**: 去掉，只保留关键事实
- **reason**: 描述性文字没有信息量
- **rule_hint**: 要点速览只写关键事实，不写描述文字

---

### [2026-04-25] #09 🔗 已合并至 #29
> 统一规则：body事实密度。#09 建立"body必须有量化数据"，#29 细化为benchmark数据点要求。完整条目见 #29

### [2026-04-25] #10
- **file**: daily-ai-news-2026-04-25.md
- **field**: category
- **before**: "OpenAI与NVIDIA合作在公司范围内部署Codex" 分类为 X讨论
- **after**: 改为 产业动态
- **reason**: 企业级部署合作是产业动态
- **rule_hint**: 企业合作/部署案例归产业动态，不归X讨论，即使信息来源是推特

### [2026-04-25] #11
- **file**: daily-ai-news-2026-04-25.md
- **field**: filter
- **before**: 姚顺雨同时出现在「研究关注」和「X讨论」要点汇总中
- **after**: 只保留在 X讨论
- **reason**: 同一条新闻不应出现在两个分类中
- **rule_hint**: 同一条新闻只归属一个分类

### [2026-04-25] #12
- **file**: daily-ai-news-2026-04-25.md
- **field**: filter
- **before**: 来源链接只有机器之心，GPT-5.5等4/24新闻在4/25重复出现
- **after**: 补充官方一手来源（anthropic.com/x.ai blog/deepseek API docs）作为主来源，原有链接保留；跨天去重增加实体匹配层
- **reason**: 有官方一手源时应优先引用；Jaccard去重对"同一事件换种说法"失效（GPT-5.5 Jaccard仅0.18）
- **rule_hint**: 有官方一手来源时优先引用，新来源作为补充不替换原有链接。跨天去重不能只靠文字相似度，需要实体级匹配（公司+产品名）

---

### [2026-04-26] #13
- **file**: daily-ai-news-2026-04-26.md
- **field**: filter
- **before**: Chelsea Finn演讲"首次透露π0.7机器人模型"
- **after**: π0.7已于4/16发布，演讲中只是引用，删除"首次透露"
- **reason**: 模型/产品已在之前发布，后续演讲/报道中提及不等于首次公开
- **rule_hint**: 提到模型/产品发布时，必须核实是否已在更早时间点正式发布。不能因为首次在某人的演讲/推文中看到就标注"首次发布/透露"

### [2026-04-26] #14
- **file**: daily-ai-news-2026-04-26.md
- **field**: source
- **before**: "前馈式3D重建路线图发布"来源标注为机器之心
- **after**: 改为arXiv论文作为一手来源，机器之心为补充
- **reason**: 机器之心是报道媒体，不是论文作者。媒体转载≠原创
- **rule_hint**: 来源区分"报道媒体"和"原始出处"。论文/研究类新闻必须以arXiv/期刊/会议为第一来源，媒体链接作为补充。当body提到具体论文编号（如arXiv 2604.14025），必须以该论文为一手来源

### [2026-04-26] #15
- **file**: daily-ai-news-2026-04-26.md
- **field**: body
- **before**: Google/Anthropic body只有首期金额和估值，缺少后续条件、Amazon同期投资、循环交易争议
- **after**: 从深科技文章补充后续$300亿业绩目标、Amazon $50亿+$200亿、Anthropic营收$90亿→$300亿、哈佛PON质疑
- **reason**: 同一事件多条来源时，应合并最丰富的数据维度，而非取单条来源的子集
- **rule_hint**: 同一事件有多条来源时，合并所有来源的关键数据，取信息密度最高的版本。具体做法：以最早/最权威来源为骨架，从其他来源补充其缺少的数据（金额细节、对比数据、争议观点）

---

### [2026-04-28] #17
- **file**: daily-ai-news-2026-04-28.md
- **field**: body
- **before**: body规则要求写"基于事实的so what"，导致AI每次往body里塞自己的判断
- **after**: body只写事实、数据、关键影响、具体人物/公司的评价观点；AI自己的so what/判断全部放insight
- **reason**: body和insight边界不清，AI的判断混入body降低了事实密度
- **rule_hint**: **body允许的内容：事实、数据、关键影响（市场反应/股价等）、具体人物或公司的评价观点（需注明谁说的）。body禁止的内容：AI自己的判断/so what/趋势预测，这些全部放insight。具体违规句式见 #35**

---

### [2026-04-30] #18
- **file**: daily-ai-news-2026-04-30.md
- **field**: title
- **before**: Ling-2.6-1T 正文写"26B参数"
- **after**: 改为"万亿参数"（模型名1T=1 Trillion）
- **reason**: 模型名中的规模标识与正文参数量描述矛盾
- **rule_hint**: 模型名中的数字（如1T=万亿参数、7B=70亿参数）必须与正文参数量描述交叉验证，不能只看部分信息源

### [2026-04-30] #19
- **file**: daily-ai-news-2026-04-30.md
- **field**: filter
- **before**: OpenAI网络安全方案和Codex决策对比各占一条独立条目
- **after**: 合并为一条"OpenAI发布网络安全方案+展示Codex决策辅助能力"
- **reason**: 同公司同日发布的低权重动态各自独立会稀释信息密度
- **rule_hint**: 同公司同日多条低权重动态（非核心产品发布/财报级）合并为一条，取"公司+多项动态"格式

### [2026-04-30] #20
- **file**: daily-ai-news-2026-04-30.md
- **field**: filter
- **before**: GPT-5.5 Pro 159分和Gemini音频前7各占一条
- **after**: 合并为一条"本周评测动态：GPT-5.5 Pro创Epoch新高159分，Gemini包揽音频前7"
- **reason**: 同为benchmark评测结果，分开展示增加条目数但不增加信息密度
- **rule_hint**: 同类型benchmark/评测结果可合并为一条"本周评测动态"，将多个结果并列展示

### [2026-04-30] #21
- **file**: daily-ai-news-2026-04-30.md
- **field**: category
- **before**: Google Cloud $200亿营收归入产业动态
- **after**: 移入算力追踪
- **reason**: 该条核心信号是"算力供给瓶颈限制增长"，不是一般的产业营收新闻
- **rule_hint**: 分类由内容的核心信号决定而非表面主题。财报中突出"算力瓶颈/供给限制"的归算力追踪，突出"用户增长/产品收入"的归产业动态

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

### [2026-05-05] #24 🔗 已合并至 #32
> 统一规则：禁止无来源的绝对性判断。#24（首个）+ #25（首选/核心地位）+ 本条合并为 #32。完整条目见 #32

### [2026-05-05] #25 🔗 已合并至 #32
> 统一规则：禁止无来源的绝对性判断。完整条目见 #32

---

### [2026-05-09] #26
- **file**: daily-ai-news-2026-05-09.md
- **field**: source
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

---

### [2026-05-10] #29
- **file**: daily-ai-news-2026-05-10.md
- **field**: body
- **before**: "谷歌DeepMind Pushmeet Kohli发布AI for Math最新成果，刷新数学AI基准SOTA。牛津教授使用该工具解开群论悬案。"（2句，无具体benchmark数据，slogan级描述）
- **after**: 补充AI co-mathematician是多Agent系统、FrontierMath Tier 4得分**48%**（创AI最高分）、测试领域（群论/哈密顿系统/代数组合）、对比GPT-5.5 Pro 39.6%、Gemini Deep Think IMO金牌、AlphaEvolve具体成果
- **reason**: 原body完全无量化数据，"刷新SOTA""群论悬案"均为空洞表述。从Pushmeet LinkedIn帖子和Google Blog补充具体数据后信息密度显著提升
- **rule_hint**: **【统一规则：body事实密度】模型/系统发布类新闻必须包含至少1个具体benchmark数据点（分数/排名/对比）。"刷新SOTA"本身不是数据，必须写明在哪个benchmark上、具体多少分。缺乏数据时优先搜索官方博客/LinkedIn帖子/技术论文。融资/投资类必须拆解资金构成（#30），收购/M&A类必须包含交易核心要素（#31）**

### [2026-05-10] #30
- **file**: daily-ai-news-2026-05-10.md
- **field**: body
- **before**: "英伟达2026年内已承诺$400亿用于AI相关股权投资交易。英伟达在传统GPU销售商业模式之外，通过资本投资深入参与AI产业链，扩展其在AI领域的影响力。"（2句，第2句纯filler）
- **after**: 补充$300亿投向OpenAI、Corning $32亿、IREN $21亿、2025年67笔VC、2026年24轮私募、Wedbush分析师"circular investment theme"评价
- **reason**: 第2句"深入参与产业链扩展影响力"是零信息增量的filler。TechCrunch原文有丰富数据（OpenAI $300亿等），未读取就写body
- **rule_hint**: **融资/投资类新闻必须拆解资金构成（最大单笔→谁→多少钱、其他投资→几笔→总额多少），不能只写一个总数。对比数据（同比/上期）和第三方评价（分析师观点）是信息密度的关键增量。属于 #29 body事实密度统一规则**

### [2026-05-10] #31
- **file**: daily-ai-news-2026-05-10.md
- **field**: body
- **before**: "Robo.ai宣布收购Neurovia AI，后者是一家AI数据处理与压缩技术研发商...产品广泛赋能自动驾驶、智慧城市、无人设备及智能制造等场景。本次收购将强化Robo.ai在机器人数据基础设施方面的能力。"（营销稿体，无交易金额/结构）
- **after**: 补充$1亿全股票、Class B股、8年锁定期、NASDAQ: AIIO、股价飙升70%、具体应用场景
- **reason**: 原body直接复制IT桔子摘录，含"广泛赋能"等marketing fluff，缺少交易金额/结构/市场反应等核心事实。PRNewswire官方新闻稿有完整数据
- **rule_hint**: **收购/M&A类新闻的核心要素：交易金额、支付方式（现金/股票/混合）、锁定期/earn-out、卖方核心资产、市场反应（股价变动）。来源优先级：PRNewswire官方稿 > 财经媒体 > IT桔子。禁止使用"广泛赋能""致力于"等营销稿措辞。属于 #29 body事实密度统一规则**

### [2026-05-10] #32
- **file**: daily-ai-news-2026-05-10.md
- **field**: body
- **before**: 多个条目含无来源绝对性判断："首个"（#24）、"首选引擎/核心地位"（#25）、"填补技术空白"（本条）
- **after**: 全部删除，或移至insight并标注为AI分析
- **reason**: "首个""首选""核心地位""填补空白"等均为AI自行添加的拔高表述，原文无支撑。三条规则（#24/#25/本条）合并为统一规则
- **rule_hint**: **【统一规则：禁止无来源绝对性判断】body中禁止以下类型的无来源判断：(1) "首个/首次/首创/填补空白"——除非原文明确支撑且无prior work；(2) "首选/核心地位/领先"——竞争格局判断放insight；(3) "最大/最强/最具影响力"——必须有可验证的排名/数据来源。合并自 #24（首个）和 #25（首选/核心地位）**

### [2026-05-10] #33
- **file**: daily-ai-news-2026-05-10.md
- **field**: body
- **before**: 多个⚠️来源不可达条目的body仍包含无法验证的具体细节（如通义千问眼镜"支持主动提醒用户并帮忙叫车"）
- **after**: 通义千问眼镜降级为"据报发布，具体参数无法验证"；浙大知识图谱删除"覆盖学科最多、规模最大"的绝对性判断；Claude Code源码解析标注"二次解读非一手源"；SGL/Radixark标注"具体benchmark数据待补充"
- **reason**: 来源不可达时，body中的具体细节同样不可验证，应一并降级。按规则"只写已确认的最小事实集"
- **rule_hint**: **⚠️标注的降级规则应覆盖body中所有具体声明，不只加标签但保留细节。如果来源不可达，body中任何"支持XX功能""实现XX效果"的描述都是不可验证的，应缩减为"据报XX，细节待验证"**

### [2026-05-10] #34
- **file**: daily-ai-news-2026-05-10.md
- **field**: source
- **before**: `[arXiv:2604.05014](https://arxiv.org/abs/2604.05014)`, `[arXiv:2604.14228](https://arxiv.org/abs/2604.14228)`
- **after**: `[arXiv](https://arxiv.org/abs/2604.05014)`, `[arXiv](https://arxiv.org/abs/2604.14228)`
- **reason**: arXiv来源链接无需在方括号内注明编码，链接本身已包含完整信息
- **rule_hint**: **arXiv来源链接统一使用 `[arXiv](URL)` 格式，不在方括号内加编码**

---

### [2026-05-11] #35
- **file**: daily-ai-news-2026-05-11.md
- **field**: body
- **before**: 3条body混入AI判断：(1) Anthropic OpenRouter"是API市场竞争力的直接指标"；(2) 拉姆齐数"标志着AI辅助数学推理进入新阶段"；(3) TechCrunch语音"趋势显示语音交互正从个人习惯蔓延到职场"
- **after**: 全部删除AI判断句，保留纯事实
- **reason**: body/insight分离规则(#17)已明确，但pipeline仍频繁混入。需要更具体的违规模式识别而非仅靠原则性规则
- **rule_hint**: **【#17 操作化：body自检黑名单】以下句式出现在body中时必须移至insight："意味着...""说明...""标志着...""趋势显示...""这表明...""反映出...""是...的直接指标/重要里程碑""展示了...的能力/潜力"。自检方法：写完body后搜索这些关键词，命中则移至insight**

### [2026-05-11] #36
- **file**: daily-ai-news-2026-05-11.md
- **field**: body
- **before**: MachinaCheck标题"AMD发布MachinaCheck多Agent系统"，body写"AMD在HuggingFace Blog发布"
- **after**: 改为"AMD Developer Hackathon项目MachinaCheck"，补充hackathon背景、开发者姓名、参赛性质
- **reason**: MachinaCheck是lablab.ai主办的AMD开发者黑客松参赛项目，非AMD官方产品发布。pipeline将"公司名+技术"默认写成公司发布，混淆了平台提供方和项目开发方
- **rule_hint**: **【来源归属规则】区分"公司官方发布"和"第三方基于公司平台开发"：(1) Hackathon/devpost项目 → 标注开发者姓名+"参赛项目"，非公司发布；(2) 开发者个人GitHub项目 → 标注开发者名，非公司行为；(3) arXiv论文 → 标注机构（大学/研究部门），非产品发布；(4) 只有公司官方blog/新闻稿/官宣推文才可写"XX公司发布/推出"**

### [2026-05-11] #37
- **file**: daily-ai-news-2026-05-11.md
- **field**: body
- **before**: TechCrunch语音文章body以"他"字截断结尾
- **after**: 补全完整内容
- **reason**: body截断说明pipeline在LLM生成或feed处理环节存在文本截断问题，可能是token限制或摘要生成时的长度截断
- **rule_hint**: **pipeline输出后需加截断检测：(1) body以单个汉字或不完整句子结尾时标记为截断；(2) body包含未闭合引号时标记为截断。截断的body应触发重新生成而非原样输出**

### [2026-05-11] #38
- **file**: daily-ai-news-2026-05-11.md
- **field**: title
- **before**: 多条标题使用"发布/推出"作为万能动词：Databricks**发布**Genie技术解析、Nous Research**发布**Pareto Code文档、浙大联合腾讯优图**发布**AdaMARP
- **after**: 按实际性质选择精确动词：博客→"详解/解析"、论文→"提出/发表"、文档→"开源/公开"、数据→"报告/显示"
- **reason**: "发布/推出"暗示产品级动作，但实际内容可能是博客文章、论文、配置文档、研究报告等。动词不精确会误导读者对事件重要性的判断
- **rule_hint**: **标题动词必须匹配内容实际性质，禁止"发布/推出"万能化：(1) 博客/技术文章 → 详解、解析、介绍；(2) 论文/学术研究 → 提出、发表、验证；(3) 配置文档/工具 → 开源、公开、提供；(4) 数据/报告 → 报告显示、数据显示；(5) 产品/模型 → 才用发布、推出；(6) 分析/观点 → 分析、复盘、探讨**

---

### [2026-05-13] #39
- **file**: daily-ai-news-2026-05-13.md
- **field**: category
- **before**: Perceptron Mk1视觉语言模型归入"算力追踪"
- **after**: 移入"模型前沿"
- **reason**: Perceptron Mk1是视觉语言模型，有明确的模型能力描述（视频理解、具身推理、时间推理），不是算力基础设施
- **rule_hint**: **模型能力类新闻（视觉语言模型/多模态模型/coding agent benchmark等）归"模型前沿"。算力追踪仅用于：芯片/硬件、云服务定价/实例、推理部署优化、数据中心基础设施。判断标准：描述"模型能做什么"→模型前沿；描述"跑模型的硬件/服务多少钱"→算力追踪**

### [2026-05-13] #40
- **file**: daily-ai-news-2026-05-13.md
- **field**: body
- **before**: Bengio团队TBA条目body写"RL训练提速50倍"
- **after**: 读取arXiv原文后纠正为"训练时间缩短4倍以上"
- **reason**: 50倍来自媒体摘要（PaperWeekly），与arXiv原文严重不符（原文是"4x or more"）
- **rule_hint**: **媒体摘要中的倍数/百分比/绝对数值必须回溯arXiv/官方博客确认。媒体转述论文时常夸大数字（如把4x说成50倍）。属于 #22 "写body前必须读原文"的硬性执行**

### [2026-05-13] #41
- **file**: daily-ai-news-2026-05-13.md
- **field**: body
- **before**: 多次从媒体报道（PaperWeekly/机器之心/DeepTech）直接写body，未主动查找arXiv原文
- **after**: 看到媒体报道论文时，第一步查找并读取arXiv原文，基于原文写body
- **reason**: #14要求"arXiv为一手源"，#22要求"写body前必须读原文"，但执行时仍然先读媒体再写body。根本原因是规则表述为"偏好"而非"必做"。应改为：处理研究类新闻时，**主动查找arXiv**是第一步，不是补充步骤
- **rule_hint**: **【研究类新闻处理流程】看到媒体报道论文时：(1) 从标题/摘要提取arXiv编号或论文标题；(2) 用arXiv搜索或Google找原文；(3) 读arXiv abstract+intro+results；(4) 基于原文写body，媒体只作为补充来源。这是流程起点而非补充步骤，违反此规则等同于凭媒体摘要扩写（#22）。适用于所有"研究关注"类条目和X讨论中的论文解读**

### [2026-05-15] #42
- **file**: daily-ai-news-2026-05-15.md
- **field**: body
- **before**: 量子位报道国产GPU/SGLang、PaperWeekly报道Nous Research TST，管道只从微信抓到标题/摘要级内容，body只有1-2句slogan描述，未主动搜索原始来源
- **after**: 用标题关键词（如"Nous Research Token Superposition"）反向搜索arXiv/GitHub/官网，找到原文后基于原文重写body
- **reason**: #41针对"研究类新闻找arXiv"，但问题更广泛：**任何来源（不仅论文）如果body信息不足，都应基于标题/摘要反向搜索原始来源**。微信/媒体报道是二手信息，原始来源（arXiv/GitHub/官方blog/公司官网）信息密度远高于媒体
- **rule_hint**: **【反向搜索补body】当管道抓到的来源是媒体（量子位/PaperWeekly/机器之心/DeepTech等）且body不足时：(1) 从标题提取关键实体和关键词（模型名/公司名/技术名）；(2) 用web_search搜索原始来源（arXiv/GitHub/HuggingFace/官方blog）；(3) 读到原文后重写body。此规则是#41的泛化——不仅论文要找arXiv，任何媒体报道都应追溯到一手来源**