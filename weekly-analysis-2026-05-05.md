# AI 前沿周报 | 2026.04.28 — 05.05

> 基于 04.28-05.05 前沿动态的全栈信号分析
> 置信度标注：**高** = 多源交叉验证 | **中** = 有数据支撑但需持续观察 | **低** = 单一信号

---

## 本周信号矩阵

> 两条主线 × 四层结构，标注本周各位置的信号强度

```
              Thread A              Thread B
           能力跃迁               效率革命
 ──────┬────────────────────────────────────────────
 L1    │  Vera Rubin 3.3x推理      四巨头$7250亿capex
 计算  │  GB300 ultra 2.7x推理     xAI 89%GPU闲置
       │  五角大楼8家部署AI        29-160万H100流入中国
       │  ★★☆ 中                ★★★ 极强
 ──────┼────────────────────────────────────────────
 L2    │  ARC-AGI-3: 0.43% vs 100%  DeepSeek V4 $0.036
 模型  │  IKP反推参数量9T/4T        NIST评估方法论争议
       │  Grok-4.3 agentic +321    Opus 4.7谄媚率-50%
       │  ★★★ 极强              ★★☆ 中
 ──────┼────────────────────────────────────────────
 L3    │  SemiAnalysis:价值向模型层  OpenRouter免费缓存
 Infra │    迁移 ARR $90B→$440B     TTFT首次官方量化
       │  vLLM DeepSeek V4优化      DeepSeek V4折扣到期
       │  Coatue锁定数据中心用地     OpenRouter ZDR数据保护
       │  ★★★ 极强              ★★☆ 中
 ──────┼────────────────────────────────────────────
 L4    │  Anthropic+OpenAI PE合资   视觉AI下载6.5x收入0
 应用  │  Anthropic $900B估值       tokenmaxxing全员渗透
       │  Meta收购ARI进机器人       豆包付费68-500元/月
       │  智元LWD部署即训练         Sierra $158亿企业Agent
       │  o1急诊诊断67%超医生50%    Legora法律AI双寡头
       │  ★★★ 极强              ★★★ 极强
 ──────┴────────────────────────────────────────────
```

**本周格局：价值链重心迁移的一周。SemiAnalysis 量化了"从卖铲子到卖金子"的趋势（Anthropic ARR $90B→$440B），Anthropic 与 OpenAI 同日宣布 PE 合资企业将企业 AI 推入资本驱动的深度部署阶段，ARC-AGI-3 则在另一端提醒——模型在可验证推理上进步巨大，但在通用智能上仍是 0.43% vs 100%。能力在涨，价格在崩，价值在迁移。**

---

## L1 计算

### 四大科技巨头 2026 AI capex $7,250 亿，同比+77%

**置信度：高** | 来源：[CNBC](https://www.cnbc.com/2026/05/03/big-tech-earnings-show-how-big-smart-spending-can-be-rewarded-by-the-market.html) | [Forbes](https://www.forbes.com/sites/aliciapark/2026/04/30/big-tech-is-on-track-to-spend-750-billion-on-ai-this-year/)

| 公司 | 2026 capex 指引 | 市场反馈 |
|------|----------------|----------|
| Google | $1,800-1,900 亿 | Cloud 增长 63%，获正面反馈 |
| Amazon | $2,000 亿 | AWS 增长 28%，获正面反馈 |
| Microsoft | $1,900 亿 | — |
| Meta | $1,250-1,450 亿 | 缺乏清晰回报路线图，周跌 9.8% |

Q1 单季合计已超 $1,300 亿。BofA 预测 2027 年将突破 $1 万亿。AI capex 进入"分化验证期"——能证明收入转化的获奖励，纯投入无路线图的被惩罚。

### NVIDIA Vera Rubin VR NVL72：推理性能 3.3x Blackwell

**置信度：高** | 来源：[@semianalysis_](https://x.com/SemiAnalysis_/status/2050282508893438316#m)

单机柜集成 **72 颗 Rubin GPU + 36 颗 Vera CPU**，液冷设计，提供 **3.6 EFLOPS**（NVFP4 推理）和 **2.5 EFLOPS**（训练）。Rubin R100 GPU 采用 **3,360 亿晶体管**，NVLink 6 带宽达 **1.8 TB/s**。相比 Blackwell Ultra GB300，推理性能提升 **3.3 倍**，每 token 成本降低 **10 倍**。H2 2026 开始出货。Vera Rubin 是 NVIDIA 维持算力垄断的关键一代。

### NVIDIA GB300 ultra NVL72 推理速度 2.7x GB200

**置信度：高** | 来源：[@semianalysis_](https://x.com/SemiAnalysis_/status/2051406756429943109#m)

SemiAnalysis 在 vLLM 推理引擎上验证，GB300 ultra 相比 GB200 NVL72 推理速度快 **2.7 倍**，推理成本可降低约 60%。

### xAI 数据中心仅 11% GPU 在线运行

**置信度：高** | 来源：[新智元](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA==&mid=2652697384&idx=2&sn=93795584090162d9c4fbbcaa76411bb0)

xAI 拥有数十万片 H100/H200 等高性能 GPU，但实际在线运行比例仅约 **11%**。其余处于闲置状态，可能用于冷存储、下一代模型训练准备或等待基础设施到位。反映 AI 公司在算力储备上的激进策略——宁可囤积也不错过训练窗口期。**算力结构性冗余与供应链紧张并存。**

### Epoch AI：29-160 万片 H100 等效 GPU 流向中国

**置信度：高** | 来源：[Epoch AI](https://epochai.substack.com/p/diversion-and-resale-estimating-compute)

中位数估计为 **66 万片** H100 等效值，主要通过 Diversion 和 resale 方式进入中国。美国出口管制未能完全阻止 AI 算力流入中国，实际规模可能接近数十万片。

### 美国国防部与 8 家科技巨头签机密网络 AI 部署协议

**置信度：高** | 来源：[TechCrunch](https://techcrunch.com/2026/05/01/pentagon-inks-deals-with-nvidia-microsoft-and-aws-to-deploy-ai-on-classified-networks/)

与 **NVIDIA、Microsoft、AWS、SpaceX、OpenAI、Google、Reflection AI、Oracle** 签约。**Anthropic 未入选**——此前五角大楼与 Anthropic 因 AI 安全政策分歧产生争议。军方在 AI 安全立场与实用主义之间选择后者。

**L1 判断：** 本周 L1 信号呈现"供给扩张+利用分化"的双面格局。NVIDIA 两代产品（Vera Rubin + GB300）持续推高算力天花板，但 xAI 89% 闲置率和四巨头 capex 分化验证（Meta 被惩罚）说明"堆算力"本身不再是护城河——关键在于能否证明收入转化。Epoch AI 的数据则揭示了出口管制的实际效果远弱于预期。

---

## L2 模型

### ARC-AGI-3：前沿模型在通用推理上近乎完全失败

**置信度：高** | 来源：[ARC Prize](https://arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis)

ARC Prize 基金会发布 ARC-AGI-3 新一代推理基准测试，包含 **135 个**人工设计的新环境，测试者需在无指令情况下探索界面、推断规则、形成假设并跨关卡迁移。

| 模型 | 得分 | 人类 |
|------|------|------|
| GPT-5.5 | **0.43%** | 100% |
| Claude Opus 4.7 | **0.18%** | 100% |

ARC Prize 开放了 160 份 replay 和推理链分析，发现 3 种常见失败模式：(1) 局部观察正确但无法构建全局世界模型；(2) 训练数据中的游戏类比（Tetris、Frogger 等）劫持行动选择；(3) 偶然过关但未理解规则，错误策略在后续关卡固化。**两模型差异：Opus 压缩为自信但错误的理论，GPT-5.5 难以压缩。**

**核心意义：** ARC-AGI-3 的价值不只是评分——replay 分析揭示了 LLM 失败的具体机制（压缩方式不同），这比 benchmark 刷分更接近"智能"本质，也为 Agent 在真实环境中的可靠性提供了预判信号。

### IKP 方法反推闭源 LLM 参数量：GPT-5.5 约 9T、Opus 4.7 约 4T

**置信度：中** | 来源：[机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651031232&idx=1&sn=6ef67aad98248c27294f1be3eb80d089) | [arXiv:2604.24827](https://arxiv.org/abs/2604.24827)

Incompressible Knowledge Probes（IKP）利用信息论下界——存储 F 个事实至少需要 F/(bits per parameter) 个权重——通过 **1,400 道跨 7 个冷僻度等级的事实问答**测量模型知识容量，反推参数量。

| 模型 | 估算参数量 | 90% CI |
|------|-----------|--------|
| GPT-5.5 | **~9T** | 0.3-3× |
| Claude Opus 4.7 | **~4T** | 0.3-3× |
| GPT-5.4 | **~2.2T** | 0.3-3× |
| Claude Sonnet 4.6 | **~1.7T** | 0.3-3× |
| Gemini 2.5 Pro | **~1.2T** | 0.3-3× |

在 89 个开源模型（135M-1.6T）上校准达 **R²=0.917**。**关键发现：推理 benchmark 饱和≠scaling 终结，事实知识不可压缩，参数量仍是硬约束。Densing Law 预测被以 p<10⁻¹⁵ 拒绝。**

### NIST CAISI 评估 DeepSeek V4-Pro 落后美国前沿约 8 个月

**置信度：高** | 来源：[NIST](https://www.nist.gov/news-events/news/2026/05/caisi-evaluation-deepseek-v4-pro) | [The Decoder](https://the-decoder.com/china-is-falling-behind-in-the-ai-race-according-to-a-us-government-benchmark/)

NIST 下属 AI 标准与创新中心发布评估报告：DeepSeek V4-Pro 在网络安全、软件工程、自然科学、抽象推理和数学等 9 项测试中，整体落后美国前沿模型约 **8 个月**。但在成本效率上，与 GPT-5.4 mini 对比，DeepSeek V4 在 **7 项 benchmark 中 5 项更便宜**（最多便宜 53%）。多位专家质疑该评估使用私有不可验证的 benchmark，且排除了大部分美国模型只留 GPT-5.4 mini 做对比。

**政策意味>技术意味**——"8 个月差距"叙事服务于出口管制政策论证，但方法论争议削弱了结论可信度。DeepSeek 在成本效率上的优势反而被证实。

### xAI Grok-4.3 API 上线：定价降 20%，agentic 性能大幅提升

**置信度：高** | 来源：[xAI 官方文档](https://docs.x.ai/developers/models/grok-4.3)

定价 **$1.25/$2.50 per MTok**（input/output），比 Grok 4.2 降低约 20%。上下文窗口 **1M tokens**，输出速度 **207 tok/s**。Artificial Analysis Intelligence Index 得分 **53**，超过 Muse Spark 和 Claude Sonnet 4.6；**GDPval-AA ELO 达 1500**，比前代提升 321 点，agentic 任务能力显著增强。

### Claude Opus 4.7 谄媚率较 4.5 降低 50%

**置信度：高** | 来源：[@anthropicai](https://x.com/AnthropicAI/status/2049927626215825734#m)

Anthropic 在真实对话场景中对 Opus 4.7 进行压力测试，谄媚率仅为 Opus 4.5 的一半。谄媚指模型过度迎合用户观点而丧失独立判断的问题。**谄媚成模型能力新 benchmark。**

**L2 判断：** 本周 L2 的核心信号来自 ARC-AGI-3——当前最前沿模型在"无指令探索+规则迁移"上几乎完全失败（0.43% vs 100%），这比任何 benchmark 刷分都更接近"智能"的本质困境。IKP 方法则从另一个角度补充：参数量仍是硬约束，scaling 远未饱和。NIST CAISI 的"8 个月差距"评估更多是政策信号而非技术定论。综合来看，模型在可验证推理上持续进步，但在通用智能上仍有根本性缺口。

---

## L3 AI Infra

### SemiAnalysis：AI 价值捕获从基础设施层向模型层迁移

**置信度：高** | 来源：[SemiAnalysis](https://newsletter.semianalysis.com/p/ai-value-capture-the-shift-to-model)

**本周最具结构意义的信号。** 核心论点：AI 产业的价值捕获正从硬件基础设施层（NVIDIA、TSMC）向模型提供商（Anthropic 等 AI Lab）迁移。关键数据：

- Anthropic ARR 从年初 **$90 亿飙升至 $440 亿**（+389%）
- 推理基础设施毛利率从 **38% 提升至 70% 以上**
- Blackwell 芯片运行前沿模型的每秒 token 生成量是 Hopper 的 **30 倍**
- Neocloud H100 一年期租赁价格较 2025 年 10 月低点 **上涨 40%**
- SemiAnalysis 自身在 Anthropic Claude token 上的年化支出达 **$1,095 万**

**"卖铲子"→"卖金子"**——模型层首次成为价值捕获的主战场。

### OpenRouter 免费 Response Caching + 首次官方量化 TTFT

**置信度：高** | 来源：[OpenRouter](https://openrouter.ai/announcements/response-caching)

开发者通过添加 `X-OpenRouter-Cache: true` 请求头即可启用。相同请求首次正常计费，后续缓存命中在 **80-300ms** 内返回，**零 token 费用**。首次从官方角度量化各模型 TTFT：

| 模型 | 首词延迟 |
|------|----------|
| Gemini 2.5 Flash | ~**1.3 秒** |
| Kimi K2.6 | ~**4.6 秒** |
| GPT-5.5 | ~**9.1 秒** |

Response Caching 与 prompt caching 不同——跳过 provider 直接返回完整响应，对 Agent 工作流的重试场景价值最大。

### OpenRouter 推出 ZDR 数据保护

**置信度：高** | 来源：[@openrouter](https://x.com/OpenRouter/status/2051289713319858313#m) | [@alexatallah](https://x.com/alexatallah/status/2051276860177121616#m)

ZDR（Zero Data Retention）一键数据保护，用户可自主控制数据保留设置。免费缓存+数据保护组合拳，加剧模型聚合平台价格竞争。

### vLLM v0.20.1 针对 DeepSeek V4 做 10+ 优化

**置信度：高** | 来源：[@vllm_project](https://x.com/vllm_project/status/2050961077769494830#m)

开源推理引擎对前沿模型的适配速度成为竞争力指标。vLLM 快速跟进 DeepSeek V4 优化有助于巩固其在开源推理栈中的位置。

### DeepSeek V4-Pro 75% 折扣到期

**置信度：高** | 来源：[Reuters](https://www.reuters.com/world/china/chinas-deepseek-slashes-prices-new-ai-model-2026-04-27/)

折扣期间百万输入 token 仅 **$0.036**，百万输出 token **$0.87**，较 OpenAI 和 Anthropic 同级模型便宜约 **97%**。折扣到期后的留存率将是检验产品力的关键指标。

### Coatue 购买数据中心用地，可能供 Anthropic 使用

**置信度：中** | 来源：[TechCrunch](https://techcrunch.com/2026/05/01/coatue-has-a-plan-to-buy-up-land-for-data-centers-possibly-for-anthropic/)

AI 公司正通过 VC 投资机构直接锁定数据中心用地，算力资源竞争前置到土地层面。

**L3 判断：** SemiAnalysis 的"价值迁移"报告是本周 L3 最强信号——模型层首次在价值链中占据利润主位，这与 Anthropic ARR 爆发和 PE 合资模式形成逻辑闭环。OpenRouter 的免费缓存+TTFT 量化从开发者工具层面降低了模型比较和使用的摩擦。DeepSeek V4 折扣到期是成本战争的阶段性节点。

---

## L4 应用

### Anthropic 与 OpenAI 同日宣布 PE 合资企业，合计 $11.5B

**置信度：高** | 来源：[TechCrunch](https://techcrunch.com/2026/05/04/anthropic-and-openai-are-both-launching-joint-ventures-for-enterprise-ai-services/) | [Bloomberg](https://www.bloomberg.com/news/articles/2026-05-04/openai-finalizes-10-billion-joint-venture-with-pe-firms-to-deploy-ai) | [Fortune](https://fortune.com/2026/05/04/anthropic-claude-consulting-industry-joint-venture-blackstone-goldman-sachs/)

| 合资企业 | 规模 | 合作方 | 模式 |
|----------|------|--------|------|
| Anthropic + Blackstone/HF/Goldman | **$15 亿** | 三方各投约 $3 亿，Goldman 投约 $1.5 亿 | 向 PE 投资组合公司部署 Claude |
| OpenAI Deployment Company | **$100 亿估值，$40 亿+募集** | TPG、Brookfield、Advent、Bain Capital、SoftBank 等 19 家 | OpenAI 保留多数控制权，17.5% 目标回报 |

**PE 合资模式本质是用资管公司的 portfolio access 换 AI 公司的技术嵌入。** 两家头部 AI 公司同日官宣，标志企业 AI 从技术授权转向 PE 驱动的深度部署模式。OpenAI 规模是 Anthropic 的 6.7 倍，反映两者在企业市场的不同阶段。

### 视觉 AI 模型推动下载量 6.5 倍，但仅 ChatGPT 实现收入转化

**置信度：高** | 来源：[Appfigures](https://appfigures.com/resources/insights/image-model-updates-drive-more-ai-app-downloads) | [TechCrunch](https://techcrunch.com/2026/05/04/image-ai-models-now-drive-app-growth-beating-chatbot-upgrades/)

| 产品 | 28 天增量下载 | 28 天增量消费者支出 |
|------|-------------|-------------------|
| ChatGPT 4o 图像 | ~**1,200 万** | ~**$7,000 万** |
| Gemini Nano Banana | ~**2,200 万** | ~**$18.1 万** |
| Meta AI Vibes 视频 | ~**260 万** | 几乎无 |

**视觉 AI 是获客利器但不是变现利器。** Gemini 下载量超 ChatGPT 但收入差 **386 倍**。付费转化取决于产品生态而非单一功能。

### tokenmaxxing 热潮：企业 AI 从试点进入全员渗透

**置信度：高** | 来源：[BusinessInsider](https://www.businessinsider.com/disney-ai-adoption-dashboard-tokens-tokenmaxxing-claude-cursor-josh-damaro-2026-4)

- Disney 内网上线 AI Adoption Dashboard：一名员工 9 个工作日调用 Claude 约 **46 万次**
- Meta 员工自建「Claudeonomics」：8.5 万人 30 天烧掉 **60 万亿 token**（折算约 $90 亿）
- Uber 2026 年 AI 预算 **$34 亿**，4 个月烧光，大头在 Claude Code
- Anthropic 年付 $100 万以上企业客户从 500 家翻倍至 **1,000+家**

**企业 AI 从试点进入全员渗透阶段，Anthropic 是最大受益者。**

### Anthropic 拟以 $900B+ 估值融资 $500 亿

**置信度：高** | 来源：[TechCrunch](https://techcrunch.com/2026/04/30/anthropic-potential-900b-valuation-round-could-happen-within-two-weeks/) | [CNBC](https://www.cnbc.com/2026/04/29/anthropic-weighs-raising-funds-at-900b-valuation-topping-openai.html)

5 个月从 **$380B 翻至 $900B+**，融资规模约 $500 亿，预计两周内完成。若落地将超越 OpenAI（$852B）成为全球估值最高 AI 公司，IPO 最早可能在 2026 年 10 月。估值飙升的驱动力是 Claude Code 驱动的收入爆发——**仅用两个月收入翻倍**，成为历史上增长最快的公司。多位科技公司 CTO 和高管放弃管理岗位加入 Anthropic 当一线工程师。

**AI 行业双寡头格局正式确立。**

### Meta 收购 Assured Robot Intelligence，进军人形机器人

**置信度：高** | 来源：[TechCrunch](https://techcrunch.com/2026/05/01/meta-buys-robotics-startup-to-bolster-its-humanoid-ai-ambitions/)

收购圣地亚哥初创公司 ARI，该公司专注为人形机器人构建基础模型。两位创始人已并入 Meta 的 **Superintelligence Labs**。此前 Meta 已在内部组建机器人团队数月，Zuckerberg 表示长期目标是构建家用人形机器人。

### 智元机器人 LWD 框架：部署即训练

**置信度：高** | 来源：[机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651031116&idx=1&sn=b934b136862779b055b5e7623bc4e43a)

Learning While Deploying（LWD）框架，核心思路是让已部署的机器人**边执行边学习**，利用成功和失败经验持续优化策略，无需回收离线重训。**将数据飞轮从"采集→训练→部署"的离线循环压缩为部署即训练的闭环。**

### 豆包新增付费订阅：68-500 元/月三档

**置信度：高** | 来源：[新智元](https://mp.weixin.qq.com/s/1XjDw2ANNMJEM2NBGjlv9A) | [36氪](https://www.36kr.com/p/3794920946561542)

标准版连续包月 **68 元/月**、加强版 **200 元/月**、专业版 **500 元/月**。专业版对标 ChatGPT Pro（$200/月），说明字节认为高算力复杂任务存在付费意愿，但免费版不动——先保用户规模再做付费分层。

### o1 急诊诊断准确率 67% 超医生 50%，登 Science

**置信度：高** | 来源：[Science](https://www.science.org/doi/10.1126/science.adz4433) | [TechCrunch](https://techcrunch.com/2026/05/03/in-harvard-study-ai-offered-more-accurate-diagnoses-than-emergency-room-doctors/)

哈佛医学院与贝斯以色列女执事医疗中心对 **76 名真实急诊患者**双盲对比。OpenAI o1 诊断准确率 **67%** vs 医生 55%/50%；治疗方案评分 AI **89%** vs 医生 **34%**。首次在真实临床环境验证 AI 推理能力，样本量 76 人仍需更大规模验证。

### Sierra $9.5 亿 E 轮，估值 $158 亿

**置信度：高** | 来源：[TechCrunch](https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/)

前 Salesforce 联席 CEO Bret Taylor（现任 OpenAI 董事长）联合创办，专为企业客服 AI Agent，已服务超过 **40% 的 Fortune 500**。Bret Taylor 同时担任 OpenAI 董事长和 Sierra CEO 的双重身份值得关注。

### Legora 估值 $56 亿，ARR 破 $1 亿

**置信度：高** | 来源：[TechCrunch](https://techcrunch.com/2026/04/30/legal-ai-startup-legora-hits-5-6-valuation-and-its-battle-with-harvey-just-got-hotter/)

法律 AI 赛道双寡头格局：Harvey（$110 亿估值）vs Legora（$56 亿）。法律 AI 验证了垂直 SaaS+AI 的 $1 亿 ARR 路径。

### DeepSeek-TUI 获 2.3k 星：开源版 Claude Code

**置信度：高** | 来源：[GitHub](https://github.com/Hmbown/DeepSeek-TUI)

终端原生编程 Agent，专为 DeepSeek V4 的 **100 万 token 上下文窗口**和 prefix cache 能力优化。单二进制分发，内置 MCP 客户端、沙箱和持久任务队列，支持 1-16 个并行子 Agent。

### Google Gemini 推上车载系统

**置信度：高** | 来源：[Google Blog](https://blog.google/products-and-platforms/platforms/android/cars-with-google-built-in-gemini-tips-2026/)

Gemini 通过 OTA 升级取代 Google Assistant，覆盖所有搭载"Google built-in"的 Android Automotive 车辆，将车载语音交互从"指令式"转为"对话式"。

### xAI Voice Cloning API：2 分钟创建自定义语音

**置信度：高** | 来源：[@xai](https://x.com/xai/status/2050355373052223585#m)

80+ 预制语音，覆盖 28 种语言。xAI 正构建从文本到语音的完整多模态 API 矩阵。

### Avoca $1.25 亿融资：AI 语音 Agent 切入蓝领服务

**置信度：高** | 来源：[Fortune](https://fortune.com/2026/04/27/avoca-ai-agents-missed-calls-hvac-plumbing-roofing-kleiner-perkins-chen-shrivastava-braswell/)

HVAC、管道、电气等家庭服务 AI 语音 Agent，估值 **$10 亿**。"AI+蓝领服务"——不是替代技工，而是替代前台调度。目标今年帮客户预约 **$10 亿**工单量。

**L4 判断：** 本周 L4 信号分三个层面：(1) **资本驱动的企业部署加速**——PE 合资模式将企业 AI 从"技术评估"推入"资本绑定部署"，Anthropic/OpenAI 同日官宣是标志性事件；(2) **商业化验证的分化**——视觉 AI 下载 6.5x 但收入转化仅 ChatGPT 成功，说明产品生态>单一功能；tokenmaxxing 热潮说明 B 端渗透已从试点进入全员阶段；(3) **新场景突破**——o1 急诊诊断登 Science 是 AI 从 benchmark 到真实场景的跨越，LWD"部署即训练"是具身智能的范式升级。

---

## 研究亮点

### Meta/KAUST Neural Computers：用学习运行时状态统一计算/内存/I/O

**置信度：高** | 来源：[arXiv:2604.06425](https://arxiv.org/abs/2604.06425)

田渊栋、Jürgen Schmidhuber 等提出"神经计算机"概念，将传统计算机的计算、内存和 I/O 统一到**学习到的运行时状态**中。作为初步验证，团队将 NC 实例化为视频模型，验证了 NC 可以习得基本的**接口原语**（I/O 对齐、短时控制），但例程复用、受控更新和符号稳定性仍是挑战。**不是 Agent tool-use 升级，而是探索"后 Agent"范式。**

### 复旦北大 AHE：Harness 自动进化，Terminal-Bench 首超人工设计

**置信度：高** | 来源：[PaperWeekly](https://mp.weixin.qq.com/s?__biz=MzIwMTc4ODE0Mw==&mid=2247719989&idx=1&sn=850381020da533ac8b5158d0f9079f58) | [arXiv:2604.25850](http://arxiv.org/abs/2604.25850)

Agentic Harness Engineering（AHE），**10 轮迭代后 Terminal-Bench 2 pass@1 从 69.7% 提升至 77.0%**，超过 OpenAI 人工设计的 Codex-CLI（71.9%）。关键发现：增益来自 tools、middleware、long-term memory 等结构性组件，而非 system prompt。冻结 harness 直接迁移到三个不同模型家族仍获 **+5.1~10.1pp 增益**。**Agent 能力的瓶颈正从模型本身转向基础设施层的编排质量。**

### Microsoft Research 多 Agent 红队测试：单独安全但交互时崩溃

**置信度：高** | 来源：[Microsoft Research](https://www.microsoft.com/en-us/research/blog/red-teaming-a-network-of-agents-understanding-what-breaks-when-ai-agents-interact-at-scale/)

在内部沙盒平台测试 100+ 个 always-on Agent（基于 GPT-4o/4.1/5 级模型），发现**某些风险只在 Agent 交互时出现，单独测试时不会暴露**——级联故障、权限升级和信息泄露。**多 Agent 安全评估不能靠单 Agent 测试叠加，交互层面的涌现风险需要专门的红队方法论。**

### RecursiveMAS：潜空间循环替代文本消息交换，消除 token 税

**置信度：高** | 来源：[@omarsar0](https://x.com/omarsar0/status/2050261229315477988) | [arXiv:2604.25917](https://arxiv.org/abs/2604.25917)

UIUC、Stanford、NVIDIA、MIT 联合提出。用轻量级 **RecursiveLink** 模块连接异构 Agent，通过潜空间直接计算替代传统文本消息交换，消除了"token 税"。Agent 间通过迭代精炼共享潜状态实现协作推理，效率和准确率均优于传统 MAS。**多 Agent 协作从文本交换走向潜空间计算，是 MAS 效率瓶颈的根本性解法。**

### 中科院 SpikingBrain2.0：Transformer→脉冲混合架构，4M 上下文加速 10x

**置信度：高** | 来源：[arXiv:2604.22575](https://arxiv.org/abs/2604.22575)

5B 参数类脑基础模型，核心思路是 **Transformer-to-Hybrid (T2H)**——将已训练好的 Qwen3-4B 转换为混合稀疏架构，训练成本不到 **7,000 A100 GPU 小时**。实测在 **4M 上下文下 TTFT 加速 10.13x**。不是替代 Transformer，而是低成本后转换方案，更适合长文档/代码库等垂直场景。

### GS-Playground：3DGS 具身仿真框架，10^4 FPS

**置信度：高** | 来源：[arXiv:2604.25459](https://arxiv.org/abs/2604.25459) | [量子位](https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247888140&idx=2&sn=1616cedcba7abd0b4f4f2d68d7d8edba)

清华 AIR DISCOVER Lab 联合多家公司提出。将批量 3D Gaussian Splatting 渲染管线与自研高性能并行物理引擎集成，在 640x480 分辨率下实现 **10^4 FPS** 吞吐量。用 3DGS 替代传统光追渲染，在保持画面质量的同时实现数量级性能提升。

### 中科大超级二极管：拍照+降噪+识别三合一

**置信度：高** | 来源：[DeepTech深科技](http://mp.weixin.qq.com/s?__biz=MzA3NTIyODUzNA==&mid=2649796012&idx=1&sn=ae9ea9a0b104c84d133e5e129ba59719)

单器件集成感知+存储+计算，无需模数转化和数据搬运。10×10 二极管阵列在 FMNIST 上经原位去噪后识别准确率从不足 **60%** 提升到超过 **95%**。工艺与 CMOS 完全兼容，已有公司联系合作将传感器做机器人眼睛。

### OpenAI Voice AI 基础设施：重构 WebRTC 栈服务 9 亿 WAU

**置信度：高** | 来源：[OpenAI](https://openai.com/index/delivering-low-latency-voice-ai-at-scale/)

将信令/媒体处理从单一 Go 服务拆分为无状态 relay 和有状态 transceiver 两层。**9 亿 WAU** 的规模首次从基础设施侧得到验证。实时语音已成为 OpenAI 核心产品形态。

### 北大 OpenWorldLib：统一世界模型推理框架

**置信度：高** | 来源：[量子位](https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247888004&idx=2&sn=df1394c7a8d411439011d14c12233470) | [arXiv:2604.04707](https://arxiv.org/abs/2604.04707)

提出世界模型的统一定义：以感知为核心、具备交互和长期记忆能力。将不同任务的模型整合到统一推理框架中。**世界模型从各自为战走向标准化。**

### 上海交大 RouteMoA：无需预推理的动态 Agent 路由

**置信度：高** | 来源：[arXiv:2601.18130](https://arxiv.org/abs/2601.18130) | [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651031297&idx=2&sn=6249a28de4fdf4debab54dbc8eb7bc8c)

ACL 2026 接收。引入动态任务分发机制，根据实时状态将请求路由到最适合的智能体，而非预先规划。**Agent 架构的新方向。**

### 荆华密算：密态计算商业化，清华任炬实验室参与

**置信度：中** | 来源：[DeepTech深科技](http://mp.weixin.qq.com/s?__biz=MzA3NTIyODUzNA==&mid=2649795987&idx=1&sn=a4e1021fd243108d95b9d88b396899c2)

林修醇休学创办，联合清华任炬教授实验室推进高性能密态计算商业化。可在数据加密状态下直接计算，解决 AI 时代数据隐私与计算效率之间的根本矛盾。完成种子轮和天使轮累计数千万元融资。

---

## X 讨论精选

### Karpathy（Sequoia Ascent 2026）：LLM 不是效率工具，是新范式

来源：[@karpathy](https://x.com/karpathy/status/2049903821095354523)

三个主题：(1) LLM 不只是加速已有任务，而是能创造传统代码无法实现的功能——如纯 LLM 驱动的图像应用、用 **.md 文档替代 .sh 安装脚本**（LLM 作为自然语言解释器智能适配环境并调试）；(2) 解释 LLM 能力的"锯齿状"现象——同一模型既能重构 10 万行代码库又会给出荒谬建议，"**要么在 RL 轨道上飞驰，要么拿着砍刀在丛林里开路**"；(3) Agent-native economy 正在形成，产品服务将被分解为传感器、执行器和逻辑。

### Hieu Pham（前 OpenAI 研究员）："软件是 agent 工作流的缓存"

来源：[@hyhieu226](https://x.com/hyhieu226/status/2051342344084181501#m)

软件本质上是 agent 工作流的缓存——Agent 已能完成许多独立任务，人类只是决定将经过验证的工作流保存为逻辑代码。同日分享 Transformer 梯度呈稀疏特征，为模型压缩和高效训练提供理论基础。

### Sam Altman：罕见表态工具中立

来源：[@sama](https://x.com/sama/status/2050274547061129577#m)

"use codex or claude code or cursor or whatever works best for you"。同日宣布 OpenClaw 支持 ChatGPT 账号登录。GPT-5.5 发布一周后，OpenAI 称其 API 收入增速**超过此前任何模型发布的 2 倍**。

### Sam Altman：承认更想要模型更便宜更快

来源：[@sama](https://x.com/sama/status/2050671161915371998#m)

他个人更希望模型更便宜、更快速，但观察到用户仍然最看重能力本身。**成本优化是厂商的追求，但用户付费的核心逻辑始终是能力领先。**

### Meta AI（Jason Weston）：Autodata——Agent 自动创建训练数据

来源：[@jaseweston](https://x.com/jaseweston/status/2050009867830673679#m)

让 AI Agent 扮演数据科学家角色，迭代式构建高质量训练和评估数据。弱强模型得分差距从 CoT Self-Instruct 的 **1.9% 扩大到 34%**。验证通过率从 **12.8% 提升至 42.4%**。"用更多推理算力换更高质量训练数据"是新的 scaling 方向。

### swyx：Opus 4.7 退步说法多为轶事证据

来源：[@swyx](https://x.com/swyx/status/2051401321744605450#m)

离线和在线评估结果指向明确进步，社区反馈需理性看待。

---

## 本周关键数字

| 指标 | 数值 | 来源 |
|------|------|------|
| 四巨头 2026 AI capex | **$7,250 亿**（+77%） | CNBC/Forbes |
| Anthropic 估值 | **$900B+**（从 $380B） | TechCrunch/CNBC |
| Anthropic ARR | **$440 亿**（从 $90 亿） | SemiAnalysis |
| Anthropic $100 万+企业客户 | **1,000+家**（从 500） | BusinessInsider |
| PE 合资总规模 | **$115 亿**（Anthropic $15 亿 + OpenAI $100 亿） | TechCrunch/Bloomberg |
| ARC-AGI-3 GPT-5.5 | **0.43%** | ARC Prize |
| ARC-AGI-3 Opus 4.7 | **0.18%** | ARC Prize |
| IKP GPT-5.5 参数量估算 | **~9T** | arXiv:2604.24827 |
| IKP Opus 4.7 参数量估算 | **~4T** | arXiv:2604.24827 |
| Vera Rubin 推理 vs Blackwell | **3.3x** | SemiAnalysis |
| GB300 推理 vs GB200 | **2.7x** | SemiAnalysis |
| xAI GPU 在线率 | **11%** | SemiAnalysis |
| 中国 H100 等效流入 | **66 万片中位数** | Epoch AI |
| 视觉 AI 下载增量倍数 | **6.5x** | Appfigures |
| ChatGPT vs Gemini 收入差 | **386 倍** | Appfigures |
| Meta 30 天 Claude token 消耗 | **60 万亿** | BusinessInsider |
| Uber 年度 AI 预算 | **$34 亿**（4 月烧光） | BusinessInsider |
| DeepSeek V4-Pro 折扣价 | **$0.036/$0.87** | Reuters |
| GPT-5.5 TTFT | **~9.1 秒** | OpenRouter |
| o1 急诊诊断准确率 | **67%** vs 医生 50% | Science |
| Sierra 估值 | **$158 亿** | TechCrunch |
| Legora ARR | **$1 亿+** | TechCrunch |

---

## 值得跟踪的早期信号

| 信号 | 矩阵位置 | 依据 | 跟踪理由 |
|------|---------|------|----------|
| **PE 合资模式** | L4×B | Anthropic+OpenAI 同日官宣 | AI 公司与资本方联合锁定部署链路，是否会成为企业 AI 标准模式？ |
| **价值从 infra 迁移到模型层** | L3×B | SemiAnalysis ARR 毛利率数据 | 模型层首次成为利润主位，对投资框架有根本性影响 |
| **ARC-AGI-3 失败模式分析** | L2×A | 0.43% vs 100% | Opus 压缩为错误理论 vs GPT-5.5 难以压缩——不同失败模式暗示不同改进路径 |
| **视觉 AI 获客不获收** | L4×B | 下载 6.5x 但收入差 386x | 产品生态>单一功能，纯视觉模型难以独立变现 |
| **Anthropic $900B 估值** | L4×A | 5 月 $380B→$900B | 是否标志 AI 双寡头格局中 Anthropic 开始拉开差距？ |
| **xAI 89% GPU 闲置** | L1×B | SemiAnalysis | 算力囤积策略的资本效率何时被市场质疑？ |
| **Meta 进军人形机器人** | L4×A | 收购 ARI | 从元宇宙→AI→具身智能，Meta 路线持续摇摆还是找到了终局？ |
| **Hieu Pham "软件是工作流缓存"** | L3×A | 前OpenAI研究员观点 | 如果成立，AI 原生应用设计需根本性改变 |
| **NIST "8 个月差距" 叙事** | L2×B | 方法论被质疑 | 政策驱动的评估会如何影响出口管制升级？ |
| **AHE Harness 可跨模型迁移** | L3×A | +5.1~10.1pp | Agent 瓶颈从模型转向编排，是否催生独立的"编排层"市场？ |
| **密态计算商业化** | L3×B | 荆华密算融资 | AI 数据安全"圣杯"方向，Agent 处理敏感数据的需求正在爆发 |

---

## 下周关注

1. **Anthropic 融资进展**：$900B 估值 $500 亿融资是否两周内 close，谁领投？
2. **DeepSeek V4 折扣到期后留存率**：97% 价差消除后的开发者行为是检验产品力的关键
3. **PE 合资模式落地细节**：DeployCo 和 Anthropic 合资企业的首批客户和部署场景
4. **WWDC26 倒计时**（6/8-12）：苹果暗示重大 AI 收购 + AI 新进展，是否在 WWDC 前官宣？
5. **Musk vs OpenAI 庭审走向**：第二周庭审结果将直接影响 OpenAI 治理结构
6. **ARC-AGI-3 后续**：社区是否开始针对 3 种失败模式设计改进方案？
7. **Google DeepMind 回应**：Gemini 3.2 何时发布？TPU 8t/8i 量产时间表
8. **tokenmaxxing 成本控制**：企业 60 万亿 token 消耗的可持续性，是否催生 token 优化工具赛道

---

*数据来源：[SemiAnalysis](https://newsletter.semianalysis.com/p/ai-value-capture-the-shift-to-model) | [ARC Prize](https://arcprize.org/blog/arc-agi-3-gpt-5-5-opus-4-7-analysis) | [TechCrunch](https://techcrunch.com/2026/05/04/anthropic-and-openai-are-both-launching-joint-ventures-for-enterprise-ai-services/) | [CNBC](https://www.cnbc.com/2026/05/03/big-tech-earnings-show-how-big-smart-spending-can-be-rewarded-by-the-market.html) | [Science](https://www.science.org/doi/10.1126/science.adz4433) | [NIST](https://www.nist.gov/news-events/news/2026/05/caisi-evaluation-deepseek-v4-pro) | [OpenRouter](https://openrouter.ai/announcements/response-caching) | [BusinessInsider](https://www.businessinsider.com/disney-ai-adoption-dashboard-tokens-tokenmaxxing-claude-cursor-josh-damaro-2026-4) | [Epoch AI](https://epochai.substack.com/p/diversion-and-resale-estimating-compute)*
*生成时间：2026-05-05*
