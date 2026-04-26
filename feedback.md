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
