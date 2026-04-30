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
- **rule_hint**: **body硬性下限3句。不足3句时必须执行以下二选一：(1) 去官方源挖更多数据补到3句；(2) 如果确实信息不够，标注⚠️需补充。禁止输出不足3句的body**

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
