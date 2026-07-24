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

## TOP 10 硬性规则

> ⭐ 级规则的精简速查版，用于快速 reference。完整规则见下方 Rule Index 和 Corrections。

1. **#45** 写body前必须读原文，不编一词（反幻觉硬门槛）
2. **#64** 研究body三段：问题→方法+核心创新→数据；标题用量化/创新点不用会议归属
3. **#35** body禁止"意味着/标志着/反映出/表明"等判断句式→移至insight
4. **#32** 禁止无来源绝对性判断（首个/首选/最大/填补空白）
5. **#61** 发布前主动深抓一手来源，不等用户指出
6. **#42** body不足时用标题/摘要反向搜索arXiv/官方blog等原始来源
7. **#49** 标题含方法名+关键数据/创新点，禁止"论文提出""研究发现"万能开头
8. **#29** body必须有≥1个量化数据点（benchmark分数/金额/参数量）
9. **#17** body只写事实，AI判断/趋势预测→insight
10. **#62** [深抓补充]/[搜索补充]打开文件第一步自动清理，整合进body后删除

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
| **body — 媒体与论文** | #69 | 公司/机构不是研究者，归属表述用“机构研究人员/作者团队”或方法主体 |
| **body — 多源合并** | #15 | 同一事件多来源合并最丰富数据 |
| **body — 格式** | #47 | 链接只出现在来源行，body禁止inline markdown链接 |
| **key_points** | #04 | 每条新闻必须有≥1条insight |
| **key_points** | #07 | 要点速览只写关键事实，不写描述文字 |
| **category** | #10 | 企业合作→产业动态，非X讨论 |
| **category** | #21 | 分类由核心信号决定，非表面主题 |
| **category** | #27 | 研究博文→研究关注，非X讨论 |
| **category** | #66 | 新评测集→模型前沿；单模型评测结果→X讨论，除非与当天模型发布合并 |
| **category** | #67 | 分类模糊且主要来源是X时，默认归X讨论 |
| **category** | #68 | 官方公司/产品原型功能更新→产业动态，即使来源是X |
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
| **body — 媒体与论文** | #51 | ⭐ 缩写展开必须以论文原文为准（OPD≠One-step Diffusion） |
| **body — 多源合并** | #52 | 多来源财务数据必须标注维度（季度/年化/累计） |
| **body — 媒体与论文** | #53 | 论文命名以arXiv原文为准，不用媒体起的昵称（NeighbourhoodVAE→RAEv2） |
| **body — 媒体与论文** | #54 | 媒体技术描述与论文不符时，以论文为准重写body（ZCube GPU虚拟化→网络拓扑） |
| **title** | #55 | #49强化：多机构论文标题加"等"，标题包含方法名而非笼统描述 |
| **pipeline** | #50 | 任何写入/覆盖文件的命令执行前，确认目标文件是否已被手动编辑 |
| **filter** | #60 | 订阅推广/转发推广类推文一律过滤（is_ai_related: false） |
| **body — 媒体与论文** | #61 | ⭐ 深抓补充是发布前必做步骤，扫描二手来源主动补一手 |
| **body — 格式** | #62 | [深抓补充]/[搜索补充] 自动清理是硬性规则，打开文件第一步执行 |
| **body — 多源合并** | #63 | 同一事件多维度报道合并为一条，来源链接用\|分隔 |
| **body — 研究结构** | #64 | ⭐ 研究 body 三段结构：问题→方法+核心创新→数据；标题用量化/创新点不用会议归属 |
| **body — 结构完整性** | #70 | title/body/insight/source 必须同一事件；insight 跨条目错贴/字段错位缝合即判定损坏 |
| **filter — 汇总一致性** | #71 | 要点汇总 ↔ 详细参考 双向核对，汇总引用已删条目=留空头 |
| **filter — 金额/公司名核实** | #72 | 融资金额回溯一手、与传统行业矛盾即过滤；公司名（.ai 后缀臆造）回溯官网 |

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

---

### [2026-05-20] #43
- **file**: daily-ai-news-2026-05-20.md
- **field**: body
- **before**: Trainium条目从旧报道补充数据（$1000亿承诺、5GW、Project Rainier），未用时间标记区分新旧信息
- **after**: 用户手动加"曾"区分："Anthropic曾承诺未来10年投入超1000亿美元"
- **reason**: 旧数据可以用来补充body，但必须用时间标记（曾、此前、早前、已于XX月）区分哪些是今天的新事件、哪些是背景信息。不加区分会误导读者对时间线的判断
- **rule_hint**: **【旧数据补充body需加时间标记】从旧报道/旧公告补充body数据时：(1) 必须使用时间标记词（曾、此前、早前、已于XX月、去年等）区分新旧信息；(2) 今天的新闻用"已宣布""已采用"等现在时态，旧背景用"曾承诺""此前已投入"等过去时态；(3) 如果无法确定某信息的时间归属，宁可不用或标注"具体时间待确认"**

### [2026-05-20] #44
- **file**: daily-ai-news-2026-05-20.md
- **field**: filter
- **before**: 管道抓取到Karpathy加入Anthropic的推文，但未收录进初始md输出
- **after**: 用户手动提供URL后由AI补充写入
- **reason**: Karpathy加入Anthropic是当天最有影响力的产业动态之一（OpenAI创始成员加入主要竞争对手），管道应将其标记为高优先级
- **rule_hint**: **【高优先级人物动态规则】以下类型的人物动态应自动标记为高优先级（不可被过滤）：(1) 头部AI公司创始人/核心成员的离职或加入（OpenAI/Anthropic/Google/Meta的founding team/C-level/VP）；(2) 知名AI研究者的机构变动（如Karpathy/LeCun/Sutskever等）；(3) 此类动态即使来源仅为一条推文也应收录。属于 #28 头部厂商覆盖检查的延伸**

---

### [2026-05-22] #51
- **file**: daily-ai-news-2026-05-22.md
- **field**: body
- **before**: "OPD（One-step Diffusion）" — 缩写展开完全错误，实际是 On-Policy Distillation（LLM后训练）
- **after**: "On-Policy Distillation（OPD）"
- **reason**: 媒体报道中"OPD"被错误展开为"One-step Diffusion"（扩散模型），实际论文是LLM后训练的"On-Policy Distillation"。整个body基于错误的技术方向展开，连研究领域都搞错了
- **rule_hint**: **⭐【缩写展开必须以论文原文为准】发现缩写/简称时，必须去arXiv/论文原文确认其完整含义，不以媒体报道的展开为准。媒体报道常将缩写错误展开（如把OPD误为One-step Diffusion），导致整个技术方向描述错误。这是 #22 "写body前必须读原文" 的最严重后果——连研究对象都搞错了。自检方法：body中任何带括号的缩写展开，必须与原文Abstract中的定义完全一致**

### [2026-05-22] #52
- **file**: daily-ai-news-2026-05-22.md
- **field**: body
- **before**: "Anthropic Q2收入预计约109亿美元"（未标注季度/年化）
- **after**: "Anthropic Q2季度收入预计约109亿美元"（明确标注"季度"）
- **reason**: 不同来源使用不同数据维度（TechCrunch报道Q2季度收入$10.9B，Epoch AI报道Q1年化运行率$30B），混在一起时"109亿美元"会被误解为年化数据
- **rule_hint**: **【多来源财务数据必须标注维度】合并多个来源的财务/数据信息时：(1) 每个数字必须标注其维度——季度收入/年化运行率/累计收入/单季度利润/合同总额等；(2) 同一主体在不同条目中出现不同维度的数据时，两个条目都应标注维度以防误解；(3) 当季度收入与年化数据同时出现时，读者会默认较大的数字是年化的，因此"109亿"如果实际是季度收入而旁边的Epoch AI写"$300亿"是年化的，不标注就会造成混淆。属于 #15 多源合并规则的维度层面**

### [2026-05-22] #53
- **file**: daily-ai-news-2026-05-22.md
- **field**: body/title
- **before**: "谢赛宁团队发布第二代表征自编码器NeighbourhoodVAE" — 媒体起名，论文实际名称为 RAEv2
- **after**: "谢赛宁团队发布RAEv2：收敛速度较原版RAE提升10倍" — 使用论文原始名称
- **reason**: 机器之心报道中将论文称为"NeighbourhoodVAE"，但arXiv原文标题为"Improved Baselines with Representation Autoencoders"，论文内部称RAEv2。标题和body使用了媒体的命名而非论文的实际名称
- **rule_hint**: **【论文命名以arXiv原文为准，不用媒体起的昵称】论文/模型的正式名称以arXiv标题和论文正文为准，不以媒体报道使用的通俗化名称为准。媒体报道常为论文起新名字（如把RAEv2称为NeighbourhoodVAE），但这不是论文的实际名称。处理方法：(1) 读到arXiv后使用论文自身定义的名称；(2) 如果媒体名称更广为人知，可在首次提及时注明"（媒体称NeighbourhoodVAE）"，但标题和正文以论文名为准。属于 #14 "arXiv为一手源"的命名层面执行**

### [2026-05-22] #54
- **file**: daily-ai-news-2026-05-22.md
- **field**: body
- **before**: 智谱ZCube body基于机器之心报道描述为"GPU虚拟化方案"，"将一张GPU虚拟成多个小GPU"
- **after**: 基于ACM论文原文重写——ATOP自动化拓扑优化管道+ZCube网络拓扑，核心是数据中心网络拓扑优化而非GPU虚拟化
- **reason**: 机器之心报道的"推翻传统二十年组网逻辑""GPU虚拟化"等描述与论文实际内容偏差大。论文提出的是ATOP自动化拓扑优化管道和ZCube网络拓扑，优化的是集群网络结构而非GPU层面的虚拟化。"15%利用率提升"在论文中无对应数据，实际结论是训练速度提升3%-7%、网络成本降低26%-46%
- **rule_hint**: **【媒体技术描述与论文原文不符时以论文为准重写body】当媒体对技术方案的描述模糊/夸张/与常识不符时（如"推翻二十年组网逻辑""GPU虚拟化"），必须回溯论文原文确认实际技术方向。媒体报道为通俗化常简化甚至歪曲技术内容（如把网络拓扑优化描述为GPU虚拟化）。处理流程：(1) 读到媒体描述感觉模糊时，立即查论文原文；(2) 以论文的实际技术描述为准重写body；(3) 媒体报道的数据如果无法在论文中找到对应，应替换为论文中的实际数据。属于 #42 "反向搜索补body"的深化执行——不仅是补数据，更是验证技术方向**

### [2026-05-22] #55
- **file**: daily-ai-news-2026-05-22.md
- **field**: title
- **before**: "中科大揭示OPD高效密码，提出EffOPD实现后训练速度提升3倍"
- **after**: "中科大等提出EffOPD：参数动力学'预见'机制实现后训练3倍加速"
- **reason**: (1) "揭示XX高效密码"属 #49 禁止的万能开头（类似"研究发现""论文提出"）；(2) 仅写"中科大"但论文12位作者来自多个机构；(3) 标题应体现核心贡献（方法名+关键机制）而非笼统描述问题
- **rule_hint**: **【#49强化：多机构论文标题精度】(1) 当论文作者来自多个机构时，标题中的机构名应加"等"（如"中科大等"），不能仅写一个机构——否则是事实不完整；(2) "揭示XX密码/机制/秘密""解锁XX"属万能开头，与"研究发现"同构，标题必须体现具体的核心贡献（方法名+关键机制+量化效果）；(3) 标题中应包含论文提出的方法名（如EffOPD），而非仅描述问题（如"揭示OPD高效密码"）。判断标准：删掉方法名后标题是否仍成立——如果成立，说明方法名是关键区分点不应省略**

### [2026-05-30] #56
- **file**: daily-ai-news-2026-05-30.md
- **field**: pipeline/fetcher
- **before**: feed_v5.py 对所有站点用 `Mozilla/5.0` UA，The Information 文章正文被 Cloudflare 拦截，pipeline 只能拿到 RSS 摘要前 200 字，导致 Meta AI Pendant / Lowe's / ByteDance 三条都降级为「⚠️ 来源未验证」最小事实
- **after**: 在 `_fetch_via_curl` 和 `fetch_source` 中根据域名切换 UA：付费墙站点（theinformation.com / wsj.com / ft.com / nytimes.com / bloomberg.com / economist.com）改用 Googlebot UA `Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)`
- **reason**: 实测 Googlebot UA 对 The Information 返回 200 OK 且能拿到 og:description 完整版（约 300 字）+ JSON-LD keywords 字段（含核心实体），足够写一条合格 body
- **rule_hint**: **【付费墙站点 UA 路由规则】feed_v5.py 已通过 `_ua_for_url(url)` 根据域名自动切换 UA。若未来新增 The Information 类付费媒体（subscription-only journalism），应加入 `PAYWALL_DOMAINS` 元组。除 og:description 外，可从 JSON-LD `<script type="application/ld+json">` 中的 NewsArticle 提取 keywords 字段获取核心实体列表用于 body 补充**

### [2026-05-30] #57
- **file**: daily-ai-news-2026-05-30.md
- **field**: pipeline/coverage
- **before**: vLLM RL 升级 / StepFun Step-3.7-Flash 详细 benchmark / Together AI OSCAR 论文等内容只能从推文片段或机器之心二手报道获得，body 信息密度不足，需用户手动提供官方 blog/arXiv 链接后再补
- **after**: OPML 增订阅 4 个 feed：vLLM Blog (`https://vllm.ai/blog/rss.xml`)、Together AI Blog (`https://www.together.ai/blog/rss.xml`)、arXiv cs.CL、arXiv cs.LG
- **reason**: 这些都是当天信息密度最高的一手源，原 OPML 只覆盖了大型媒体和顶级公司博客，**vLLM/Together 等中型项目和 arXiv 论文流**没收
- **rule_hint**: **【一手源覆盖规则】对于以下类别应优先订阅一手 RSS 而非依赖推文/二手报道：(1) 主流推理框架官方 blog（vLLM、SGLang、LMDeploy）；(2) 重要研究机构/初创官方 blog（Together AI、Anthropic、Mistral）；(3) arXiv 分类 RSS（cs.CL、cs.LG）作为当天论文兜底覆盖。验证方法：候选 RSS 必须返回 `application/xml` 或 `application/rss+xml` 且 200 状态码**

### [2026-05-30] #58
- **file**: daily-ai-news-2026-05-30.md
- **field**: body
- **before**: SemiAnalysis Dark Output / StepFun Step-3.7-Flash / OSCAR 论文等条目，pipeline 抓到了源（推文或 RSS 标题）但只用 RSS 摘要文本，没有顺着推文/媒体里的 `arxiv.org/abs/*`、`*.stepfun.com/blog/`、`newsletter.semianalysis.com/p/*` 等链接抓官方页面
- **after**: 用户提供链接后由 AI 主动抓正文（StepFun blog 拿到完整 benchmark 表、SemiAnalysis Substack 拿到 Solow 类比和 3.6 万亿 GDP 修订案例、arXiv 拿到 OSCAR/BES/Adam's Law/Life-Harness 摘要）
- **reason**: feed_v5.py 的 `_fetch_arxiv` 函数已存在但只在 article 字段含 "arxiv" 字符串时触发；对于「机器之心报道某 arXiv 论文」这种二手报道，pipeline 不会反查 arXiv。同理对官方 blog/Substack 链接也无深抓
- **rule_hint**: **【深抓触发规则】未来计划在 `post_validate_and_enrich` 中实现按域名的二级深抓：当 body < 3 句或 < 80 字且 link 含以下域名时强制抓正文：`arxiv.org/abs/`（用现有 `_fetch_arxiv` 扩展）、`*.stepfun.com/blog/`、`vllm.ai/blog/`、`newsletter.semianalysis.com`、`techcrunch.com`（抓全文而非只用 RSS description）、`huggingface.co`（抓 model card）。每个域名一个轻量提取函数**

### [2026-05-30] #59
- **file**: daily-ai-news-2026-05-30.md
- **field**: body/translation
- **before**: 「美国清洁能源创业公司 Focused Energy 宣布获得 2.4 亿美元 A 轮融资，投资方包括联邦突破能源机构（Federal Agency for Breakthrough Energy）」——国籍错（实为德国公司）、机构名错译（Federal Agency for Breakthrough **Innovation** 即 SPRIND，不是 Energy）
- **after**: 「Darmstadt 总部的激光核聚变公司 Focused Energy ... 投资方包括德国联邦突破创新署 SPRIND（Federal Agency for Breakthrough Innovation）、RWE（战略+工业合作伙伴）、欧洲创新理事会基金、原领投方 Prime Movers Lab」
- **reason**: 公司原 press release 明确表述为德国 Darmstadt 公司、欧洲最具价值聚变公司，主要投资方 SPRIND 是德国联邦机构（Federal Agency for Breakthrough Innovation 创新署，非 Energy 能源署）。pipeline 只用 IT桔子 二手摘要导致两处事实错误
- **rule_hint**: **【机构名/国籍核实规则】(1) 涉及非中国公司/机构时，国籍以官方网站 / press release 为准，不以中文媒体的「美国/欧洲」笼统描述为准；(2) 外文机构缩写（如 SPRIND、ARPA-H、DARPA）必须保留缩写并在括号中给出完整官方英文名，不要凭直觉翻译完整名（Innovation 易被错译为 Energy）；(3) 当条目的唯一来源是 IT桔子等中文二手聚合时，应去公司官网/press release 抓一手核对。属于 #54 "媒体技术描述与论文原文不符时以论文为准重写 body" 的国别/机构维度延伸**

---

### [2026-06-15] #60
- **file**: daily-ai-news-2026-06-15.md
- **field**: filter
- **before**: Turing Post 发布的订阅引导推文（"关注我们获取AI深度分析"）被收录进 X讨论，body 自身已标注"纯账号推广内容，无实质AI行业信息"但仍通过 `is_ai_related: true`
- **after**: 删除该条目
- **reason**: LLM 识别到这是推广内容（body 写了"纯账号推广内容"），但未执行过滤，仍然收录
- **rule_hint**: **【订阅推广/转发推广类推文过滤】pipeline LLM prompt 需增加规则：账号自我推广、订阅引导、转发无增量信息的推文一律标 `is_ai_related: false`。判断标准：推文核心目的是引导关注/订阅/点击链接，而非传递具体AI行业事实。即使发布者是AI领域账号（如 Turing Post），其自我推广推文也不应收录**

### [2026-06-15] #61
- **file**: daily-ai-news-2026-06-15.md
- **field**: body — 媒体与论文
- **before**: 多条新闻 body 信息不足，来源停留在二手媒体（IT桔子摘录、HuggingFace 摘要、X推文片段），缺少一手来源的关键数据
- **after**: 逐一深抓官方/一手来源补充：弘火智能从高瓴官方公众号补充创始人背景+产品细节+上市时间；FTP-1/1D Token/LabVLA/LU-KV/GaussianDWM 从 arXiv 原文+ICML会议页补充方法细节和实验数据；Turing Post 向量数据库从官网全文补充市场规模和四层分类
- **reason**: #42 要求"媒体body不足时反向搜索原始来源"，但 pipeline 只从 RSS 摘要/推文片段写 body，未触发深抓
- **rule_hint**: **【深抓补充是发布前必做步骤】打开日报文件时，第一步扫描所有 body，检查是否有以下信号：(1) 来源仅为微信/IT桔子等二手聚合，缺官方一手；(2) 研究类条目来源仅为 HuggingFace 摘要而非 arXiv 原文；(3) X推文类条目 body 仅为标题复述无实质内容。命中则手动深抓官方来源/arXiv 补充。此步骤在 QA 前执行，不等用户指出。属于 #42 的执行层面强化——不仅 pipeline 要做，人工审核也要主动做**

### [2026-06-15] #62
- **file**: daily-ai-news-2026-06-15.md
- **field**: body — 格式
- **before**: 文件中大量 `[深抓补充]` 和 `[搜索补充]` 段落残留：英文原文片段、关键词列表（`关键词: ai, policy, x, anthropic...`）、作者元数据（`作者: Jul...`）未整合进 body
- **after**: 全部整合进中文 body 后删除原始英文块
- **reason**: MEMORY.md 已有规则"[深抓补充]必须自动处理"，但执行时仍遗漏
- **rule_hint**: **【[深抓补充]/[搜索补充] 自动清理是硬性规则】打开日报文件的第一步就是扫描所有 `[深抓补充]` 和 `[搜索补充]` 段落，将有用信息整合进中文 body，然后删除原始英文文本、关键词列表、作者元数据。这不是可选步骤——残留这些标记等于半成品。此规则已在 MEMORY.md 中记录，但需再次强调：不要等用户指出**

### [2026-06-15] #63
- **file**: daily-ai-news-2026-06-15.md
- **field**: body — 多源合并
- **before**: SpaceX 相关内容散布在 3 条独立条目（The Information 分析Anthropic矛盾、TechCrunch Mobility SpaceX超越特斯拉、TechCrunch AI公司IPO受益方），要点汇总出现 3 条 SpaceX，信息碎片化
- **after**: 合并为一条「SpaceX完成史上最大IPO，市值2.1万亿美元超越特斯拉」，4 个来源交叉引用，IPO财务数据+Anthropic分析+市场溢出效应整合在一个 body 中
- **reason**: 同一事件（SpaceX IPO）的多个维度分散在不同条目中，违反 #19 同公司同日多条合并规则
- **rule_hint**: **【同一事件多维度合并】当同一核心事件（如某公司IPO/收购/发布）在多条来源中出现不同侧面的报道时，应合并为一条：(1) 取事件本身（IPO完成+市值数据）为 body 骨架；(2) 从其他来源补充关联影响（AI赛道溢出效应、竞品分析、关联公司动态）；(3) 所有来源链接用 `|` 分隔保留在来源行。属于 #15 多源合并和 #19 同公司合并的交叉执行**

### [2026-06-15] #64
- **file**: daily-ai-news-2026-06-15.md
- **field**: body — 研究关注 body 结构
- **before**: 5 条研究关注 body 存在多个结构问题：(1) 缺"解决了什么问题"——直接跳到方法描述，读者不知道现有方法有什么不足；(2) 方法细节过长——作者全名列举（"Yuchen Xian、Yunqiu Xu、Yang He等"）、工程中间链路冗余（"离线profiling协议支持实际部署"）；(3) 标题用会议归属（"ICML 2026入选"）代替核心区分点
- **after**: 统一为三段结构：**问题（现有方法的不足）→ 方法+核心创新（保留关键技术链路，砍冗余）→ 数据/结果**。标题补充量化数据或核心创新点（LU-KV补"压缩至20%性能损失仅0.52%"，GaussianDWM补"语言特征嵌入3D高斯基元"）
- **reason**: 研究 body 规则（MEMORY.md）要求"先一句话讲清楚论文做了什么"，但"做了什么"应包含"解决了什么问题"——读者需要知道现有方法的不足才能理解新方法的价值。同时方法细节要区分"核心创新"（保留）和"工程冗余"（砍掉）
- **rule_hint**: **【研究关注 body 三段结构】每条研究 body 统一为：(1) **问题**：一句话说现有方法/技术的不足（如"现有触觉策略绑定固定传感器，跨传感器泛化困难"）——这是理解论文价值的前提，不能省略；(2) **方法+核心创新**：谁提出了什么方法，保留关键技术创新链路（如"异构编码器→latent token→Transformer Expert"），但砍掉作者全名列举（只写"第一作者+等"）、工程实现细节（如"离线profiling协议"）、冗余修饰；(3) **数据/结果**：硬数据加粗。**标题规则**：标题的核心区分点必须是量化数据或技术创新点，不能用会议归属（"ICML/CVPR 2026入选"）代替——会议归属放来源行即可。判断标准：删掉会议归属后标题是否仍能区分该论文与其他论文**

### [2026-07-05] #65
- **file**: daily-ai-news-2026-07-05.md
- **field**: filter
- **before**: 7月5日再次收录“阿里巴巴据报禁止员工使用Anthropic的Claude Code”
- **after**: 删除该条，因7月4日已以“阿里巴巴禁止员工在工作电脑使用Claude”完整收录，并保留更丰富的第一财经/The Information来源版本
- **reason**: 同一实体+同一事件跨天重复，后一天 TechCrunch 简讯信息量更低，不应重复进入日报
- **rule_hint**: 跨天去重需按实体+事件匹配；同一事件后续低信息量简讯重复出现时删除，保留信息密度最高且来源更完整的旧条

### [2026-07-11] #66
- **file**: daily-ai-news-2026-07-11.md
- **field**: category
- **before**: 「Artificial Analysis评测：Meta Muse Spark 1.1 Intelligence Index得51分」归入「模型前沿」
- **after**: 移入「X讨论」
- **reason**: 这不是新的重要评测集发布，也不是当天模型发布的合并动态，而是第三方对具体模型的单条评测结果。具体模型评测结果更适合作为X平台讨论/数据点收录，避免模型前沿被单模型分数榜单稀释。
- **rule_hint**: **【评测类动态分类规则】新的重要benchmark/评测集/评测框架发布可归「模型前沿」；具体模型的第三方评测结果、榜单分数、单模型对比，如果不是与当天模型发布合并成同一动态，一律归「X讨论」。判断标准：核心新闻是“评测体系本身新增”→模型前沿；核心新闻是“某已有模型拿了多少分”→X讨论。**

### [2026-07-11] #67
- **file**: daily-ai-news-2026-07-11.md
- **field**: category
- **before**: 「Google DeepMind与Google Labs在Project Genie中推出Street View地理接地功能」归入「模型前沿」
- **after**: 移入「X讨论」
- **reason**: 该条主要来源是X动态，且内容介于生成式3D、空间智能演示、产品原型更新之间，分类边界不清晰。对于这类模糊条目，放入X讨论比硬归入模型前沿更稳妥。
- **rule_hint**: **【X来源模糊分类兜底规则】当条目分类边界模糊，且主要来源是X推文/账号动态时，默认归入「X讨论」。但如果条目有明确一手论文、官方研究博客、企业合作/融资/算力基础设施等强语义信号，仍按核心信号归入对应栏目。**

### [2026-07-11] #68
- **file**: daily-ai-news-2026-07-11.md
- **field**: category
- **before**: 「Google DeepMind与Google Labs在Project Genie中推出Street View地理接地功能」按模型/空间智能或X来源模糊处理
- **after**: 移入「产业动态」
- **reason**: 该条虽然来源是X，但主体是Google DeepMind与Google Labs，动作是Project Genie产品原型的具体功能更新。它不是新模型/benchmark/论文，也不是纯社区讨论；官方产品/平台/实验原型功能更新应归产业动态。
- **rule_hint**: **【官方产品/原型更新分类规则】当X来源条目有明确公司/官方账号主体，且内容是产品、平台、实验原型、功能、API、集成能力更新时，优先归「产业动态」。#67 的X讨论兜底只适用于主体或事件性质不清的模糊条目，不能覆盖明确的官方产品动态。**

### [2026-07-11] #69
- **file**: daily-ai-news-2026-07-11.md
- **field**: body — 媒体与论文
- **before**: 「Meta等研究者在arXiv发布《Remember When It Matters: Proactive Memory Agent for Long-Horizon Agents》」
- **after**: 「长时程Agent容易让任务事实、既有诊断和未完成子目标在不断增长的轨迹中失效，论文将这一问题称为behavioral state decay。Proactive Memory Agent把记忆作为主动干预机制……」
- **reason**: Meta是公司/机构，不是“研究者”。即使作者机构归属已核实，也不能把机构写成研究者主体；此外“在arXiv发布”是低信息量模板句，不如直接写问题、方法和数据。
- **rule_hint**: **【研究归属表述规则】论文/研究类条目中，公司、大学、实验室等机构不是“研究者”。需要归属时写“Meta等机构的研究人员/作者团队”或“某机构团队”，更推荐以论文方法/项目名为主体开头。禁止“Meta等研究者”“Google等研究者”这类机构人格化表达；“在arXiv发布/论文提出”模板句也应尽量替换为问题→方法→数据结构。**

### [2026-07-22] #70
- **file**: daily-ai-news-2026-07-22.md
- **field**: body/structural
- **before**: 「具身智能模型实现27000台真实机器人跨50国部署」条目是三段不相关内容拼接——标题讲睿尔曼+机器人部署，正文残缺到「工业和信息化部、国务院国资委」就截断，insight 讲 OpenAI 中小企业项目，来源却是 OpenAI SMB 链接。同期「阿里平头哥 SAIL」条目的 insight 写的是「a16z 和 Bessemer 押注 Agent 安全赛道」（实为 Neo 融资的 insight，错贴到 SAIL）。
- **after**: 删除 27000 机器人拼接条目；SAIL insight 重写为「平头哥开源软件栈切入推理部署层、对标 CUDA 生态」。Neo 融资作为独立条目在初创&融资补全。
- **reason**: 同一条目的 title/body/insight/source 来自不同事件，是 pipeline 在合并/截断/落库环节把多条记录的字段错位缝合；insight 跨条目错贴说明 key_points 与 body 的绑定关系在处理中丢失
- **rule_hint**: **【结构完整性自检】QA 必须对每条新闻做字段一致性校验：(1) title 主体 == body 主体 == source 链接指向的主体（三者必须同一事件/公司）；(2) insight 讨论的对象必须与 body 一致，禁止 insight 谈 A 公司而 body 谈 B 公司；(3) body 以单字/未闭合引号/部门名截断时标记为损坏并重生成（#37 的延伸）。任一不一致即判定为拼接/错位损坏，删除或整条重写，不做局部修补**

### [2026-07-22] #71
- **file**: daily-ai-news-2026-07-22.md
- **field**: filter/summary
- **before**: 要点汇总列着「产业动态」（Mercor、OpenAI 中小企业、LangChain 语音 Agent）和「初创&融资」（Sila、Neo.ai、Stenon）两类的条目，但详细参考里这两节整个缺失——汇总与正文脱节
- **after**: 抓一手来源把缺失条目补成完整详细条目（OpenAI blog、WSJ、LangChain Docs 等），重建两个章节；汇总与正文逐项对齐
- **reason**: 用户手动删低质量条目时只删正文、漏改汇总，或 pipeline 生成汇总与正文不在同一环节，导致汇总引用了已不存在的详细条目
- **rule_hint**: **【汇总↔正文一致性校验】发布前 QA 必须双向核对 要点汇总 与 详细参考：(1) 汇总里每个分类下的每个条目，在详细参考中必须有对应章节+条目（汇总→正文）；(2) 正文里每个条目，在汇总对应分类里至少有一条呼应（正文→汇总）；(3) 若某汇总条目无正文、且无法抓到一手来源补全，则从汇总删除而非留空头。校验顺序：先确保 6 个分类标题在汇总和正文都存在，再逐条比对**

### [2026-07-22] #72
- **field**: filter/source
- **before**: 「Sila raises $300M」融资条目——汇总金额 $300M，但可查证记录仅有 $375M Series G（2024年6月）+$1亿 DOE，无 2026 新轮；且电池材料属传统行业、非 AI。「Neo.ai」公司名实际为「Neo」（前 SentinelOne 团队），.ai 后缀为臆造
- **after**: 删除 Sila（金额不可核实 + 非 AI）；Neo 名称由「Neo.ai」更正为「Neo」，并补全前 SentinelOne 团队/a16z+Bessemer 领投/Agentic Software Control 等可核实事实
- **reason**: 融资金额/公司名是高事实密度字段，错误会直接误导；不可核实的金额即使加「据报」也有风险，且 Sila 非跨边界前沿科技，按非 AI 过滤
- **rule_hint**: **【融资金额与公司名核实】(1) 融资/投资类金额必须能回溯到一手（公司 press release/Crunchbase/权威财经媒体）；若搜到的记录与汇总金额矛盾（如汇总 $300M 但记录是 $375M 且无更新轮），不写不可核实金额，标注或删除该条；(2) 非 AI 的纯传统行业（电池材料/地产/食品/纯汽车）即使曾进 pipeline 也应过滤，前沿科技白名单仅量子/脑机/核聚变/半导体；(3) 公司名以后缀（.ai/.com）臆造时，回溯官网/新闻稿确认正式名称（Neo 而非 Neo.ai）。属于 #29 事实密度与 #32 绝对性判断的事实核实延伸**

### [2026-07-24] #73
- **file**: daily-ai-news-2026-07-24.md
- **field**: filter
- **before**: 精简日报时删除「Stripe据报洽购OpenRouter」和「Corgi据报8周内第三次融资」两条初创&融资动态
- **after**: 恢复两条，并同步补回要点汇总
- **reason**: OpenRouter潜在收购体现模型聚合与计费入口的战略价值；Corgi短期连续融资体现AI创业风险保障这一二阶基础设施信号，均有独立信息增量
- **rule_hint**: **【精简不只看条目数量】融资栏目精简时，应保留能反映AI产业二阶基础设施、分发/计费入口或异常资本节奏的事件；固定条目上限只能作为告警，不能替代编辑价值判断**
