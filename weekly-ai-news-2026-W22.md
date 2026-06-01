## 【Weekly 简报】0525-0530（2026 W22）

> 数据来源：daily-ai-news 6 天 + smol.ai/latent.space + 联网补充 | 【OP】= Own Perspective

---

## 重点矩阵（30 秒全景）

| Layer | 能力跃迁 | 效率革命 |
|---|---|---|
| **L0 能源** | Focused Energy €240M A 轮（激光聚变，落地旧 RWE 核电厂） | Anthropic 一次签 10 GW（AWS 5GW + Google/Broadcom TPU 5GW + SpaceX Colossus） |
| **L1 计算范式** | 华为韬定律（时间缩微，2031 年 1.4nm 同等密度） | NVIDIA Vera CPU $200B 市场 / Snowflake×AWS Graviton $6B / 字节 capex $70B + 高通 ASIC + 自研类 LPU / XCENA CXL near-memory / Groq $650M 转推理云 |
| **L2 模型与认知** | Opus 4.8（41 天迭代）/ GPT-5.6 1.5M ctx 曝光 / Grok V9-1.5T / AlphaProof Nexus 解 9 个 Erdős / ESMFold2 蛋白质世界模型 / Step-3.7-Flash 196B / Keye-VL-2.0 DSA 多模态 | OSCAR 2-bit KV（358B 与 BF16 持平）/ DeepSeek V4-Pro 1M KV cache 降到 V3.2 的 10% / Delta Weight Sync 130× / ForgeTrain 比 Megatron 快 10% / UltraData-SFT 1500 万样本 |
| **L3 系统与平台** | Dynamic Workflows（百级并行子 Agent）/ Memory Files + Dreams / 三档安全隔离 / Trajectory $15M post-deployment learning 平台 | vLLM 五连发（RL 同步 / Rust 前端 / EAGLE 3.1 +2× / Dynamo 集成 / fastokens）/ LangChain Deep Agents v0.6 Delta Channels（5.3 GB→129 MB）/ AWS OpenSearch -60% |
| **L4 应用与智能体经济** | Cognition $26B（Devin 89% 内部代码）/ Tax AI 97% / Replit×Visa Agent 支付 / Figure×Catalyst 部署 | SkyClaw 价格 1/27-1/43 / Mercedes 8 月→8 天 / 单人 180h→15h / ClickUp 裁员由 Agent 替代 |

---

## 趋势 A：前沿模型里有大量 Latent Capability，Harness 的作用是「释放」而非「增加」

### 核心命题

模型能力不是被 harness「增加」的，而是被 vanilla chat UX「锁住」的。正确的 harness 释放已有能力。

### 本周证据

| 证据 | 来源 | 数据 |
|---|---|---|
| 冻结权重仅改 harness | Life-Harness（北大） | 18 模型 / 126 配置 / **+88.5%** 平均相对提升 |
| 同一模型 + appropriate harness 可复现内部模型 one-shot 结果 | Sébastien Bubeck | 「large amount of latent capability not exposed by vanilla chat UX」 |
| Harness 质量的独立度量 | EFC（Effective Feedback Compute） | **R²=0.99**（raw token/tool counts 解释力很弱） |
| Harness 与模型能力非单调 | arXiv 2605.26731（本周发表） | 中等模型获益最大，最强模型在过度结构化 harness 下反而下降 |
| 同一模型在自定义 vs 他人定义环境 | Cognition 89% vs Harvey LAB 7.1% | 差 **12 倍** |
| Opus 4.8 benchmark 评价分裂 | smol.ai 汇总 | CursorBench「效率更好但略低于 4.7」/ 真实使用「meaningful quality-of-life」 |
| 不同模型需要不同 harness | LangChain Deep Agents v0.6 | Qwen/Kimi/DeepSeek 在 **20×+ 更低成本**下达到强性能 |

### 反直觉推论【OP】

1. **Cognition 的 89% 不是「Devin 很强」，是「Cognition 的代码库已经与 Devin 共生进化」。** 换一个代码库会断崖下降。这不是通用能力，是环境适配。

2. **Opus 4.8「不是 benchmark 刷新」恰恰证明了这个框架。** 模型本身的提升是 incremental（CursorBench 误差范围内），但 Dynamic Workflows + Memory Files + effort control 释放了更多已有能力，所以真实使用体验「meaningful」。smol.ai 的社区第四阵营说得最准：**the model matters less than the harness。**

3. **非单调性意味着不存在「一个最优 harness 适配所有模型」。** 这解释了为什么 LangChain 要把 harness profiles 做成一等公民——不同模型需要不同的释放方式。也意味着 Life-Harness 的 +88.5% 在最强模型上可能只有 +20-30%。

### 与前两周联动

前两周趋势四「Model + Harness 叙事强化」是假说阶段（Artificial Analysis Coding Agent Index 显示 harness 有独立价值）。本周拿到了**决定性验证**：Life-Harness +88.5%、EFC R²=0.99、Bubeck 的 latent capability 表述。从「harness 有价值」升级为「能力本来就在那里，harness 只是释放它」。

### 值得深挖的问题

1. Life-Harness 的 +88.5% 按模型能力分层后是什么分布？（验证非单调性）
2. 如果能力是 latent 的，那 Anthropic 的安全对齐是否在**故意压制**公开版本的能力？（smol.ai 第三阵营的怀疑）
3. EFC 作为 harness 质量度量，能否成为新的行业标准？（替代 token count / tool call count）

---

## 趋势 B：自进化从研究方向变成可购买的基础设施——L2 到 L4 本周同时成型

### 核心命题

前两周的 L1-L5 自进化框架本周第一次变成了**可追踪的产业进度条**——每一层都有了产品/组织行为/论文对应物，且「post-deployment learning」从愿景变成了可购买的 infra。

### 本周证据

| 层级 | 对应物 | 性质 | 关键数据 |
|---|---|---|---|
| L2 产品 | Anthropic Memory Files + Dreams | 已上线测试 | 双模式记忆 / REM-style 后台巩固 |
| L2 方法论 | Echo（用户修正→学习信号） | 论文 | 代码补全接受率 25.7%→**35.7%** |
| L2 方法论 | DenoiseRL（从错误推理链学习） | 论文 | 不依赖强教师模型 |
| L2-L3 平台 | **Trajectory**（$15M 融资） | **产品**（可购买） | 用 agent traces 持续 post-train；Harvey/Clay/Mercor 为设计合作伙伴 |
| L2-L3 企业 | **Fujitsu 自进化多 Agent**（5/25） | **产品**（企业 IT） | 多 Agent 团队从日常运营中持续安全学习 |
| L3 验证 | AlphaProof Nexus（Google DeepMind） | 已部署到实际数学研究 | 9 个 Erdős 开放问题（含 56 年未解 2 题）/ 单题约几百美元 |
| L3→L4 | BES 双向进化搜索（Harvard） | 论文 | 突破自回归探索的熵壳限制 |
| **L4 组织行为** | **Karpathy autoresearch 团队**（5/19 入职 Anthropic） | 组织 | mandate = 用 Claude 自动化预训练研究 |
| L4 baseline | Karpathy Loop（3 月） | 实验 | 2 天 700 个训练实验 / 11% 训练加速 |
| 训练 bug 修复 | HuggingFace 多轮 RL tokenization bug | 基础设施 | Token-In, Token-Out 规则（自进化的前提是训练循环不能 broken） |

### 反直觉推论【OP】

1. **Anthropic 的 Memory Files + Dreams + Karpathy autoresearch 是同一条线的三层。** Memory Files 是 L2（跨任务经验积累的产品化），Dreams 是 L2→L3 的桥（离线巩固 = 经验整理），Karpathy 的 autoresearch 是 L4（用 Claude 改进 Claude 的预训练）。这不是三个独立产品决策，是一个**自进化栈**。

2. **HuggingFace 的多轮 RL bug 说明当前大部分 Agent RL 训练可能是「静默 broken」的。** 如果 tokenization 不匹配导致梯度应用到模型从未采样的序列上，那过去几个月所有基于多轮 RL 的 Agent 改进都需要重新审视。这是自进化的「地基问题」。

3. **Trajectory 的出现意味着「post-deployment learning」不再需要自建。** 以前只有 Anthropic / OpenAI / DeepSeek 这种有自己训练栈的公司能做 continual learning，现在 Harvey / Clay 这种垂直 Agent 公司可以通过 Trajectory 直接购买这个能力。门槛从「自建训练栈」降到「接入 API」。

### 与前两周联动

前两周判断「L4 是真正的分水岭」。本周 Karpathy 入职 Anthropic 意味着 L4 已经从「研究方向」变成了「组织行为」——一个 OpenAI 联合创始人 + 一个专门团队 + 一个明确 mandate。结合他 3 月的 Karpathy Loop（11% 训练加速），如果这个加速可以 compound（每轮 11%，10 轮后 2.8×），这就是 RSI 的 adequacy 阶段。Ajeya Cotra 预计 adequacy 在 1-2 年内实现——Karpathy 的团队可能就是验证这个时间线的关键变量。

### 值得深挖的问题

1. Karpathy Loop 的 11% 能否 compound？如果能，多少轮后到 Ajeya Cotra 的 adequacy？
2. HuggingFace 的 Token-In, Token-Out 修复后，哪些已发表的 Agent RL 结果需要重新跑？
3. Trajectory 的商业模式是什么？按 trace 量收费？按模型改进幅度收费？这决定了 post-deployment learning 的经济学。

---

## 趋势 C：Inference Inflection——推理层从附属变成独立十亿美元级赛道

### 核心命题

推理经济学正在被 **attention design + cache hierarchy + routing** 三层同时推动，不只是更便宜的硬件。中国实验室的价格战是架构创新驱动的真实成本下降，不是补贴。HBM 涨价是这次栈位分裂的根本驱动。

### 本周证据

| 维度 | 事件 | 数据 |
|---|---|---|
| **推理层独立融资** | Baseten $1B 洽谈 / OpenRouter $113M / Groq $650M / General Compute $15M | Baseten 估值 3 个月翻倍至 $11B；OpenRouter 半年用量 5×（5T→25T tokens/week） |
| **内存层独立融资** | XCENA $135M | CXL near-memory / 宣称 10 台压 1 台 / 2027 年才有收入 |
| **HBM 涨价** | TrendForce 5/27 | Q1 **+95%** / Q2 预计 **+58-63%**（十年最陡峭） |
| **架构驱动降本（中国）** | DeepSeek V4-Pro | 1M-token KV cache 降到 V3.2 的 **~10%** / 单 token FLOPs 降到 **27%** |
| **架构驱动降本（中国）** | MiMo（小米） | 5× cached token capacity / **80%** lower caching cost / 1:7 Full:SWA |
| **量化** | Together AI OSCAR | 2-bit KV / GLM-4.7（358B）与 BF16 持平 |
| **推测解码** | EAGLE 3.1 | 长上下文接受长度 **+2×** / Kimi K2.6 实测 +2.03× |
| **训练通信** | HuggingFace Delta Weight Sync | 每步 1.2 GB→20-35 MB（**130×** 缩减） |
| **推理框架** | vLLM 一周五连发 | RL 同步 API / Rust 前端 / EAGLE 3.1 / Dynamo 集成 / fastokens |
| **供应链锁定** | Anthropic 入股 Micron + Samsung + SK hynix | 三大 HBM 厂商战略入股 |

### 因果链【OP】

```
HBM Q1 涨 95% / Q2 +58-63%
    ↓
KV cache 绑在 HBM 上不再经济
    ↓
两条逃逸路径：
  A. 把 KV cache 挤出 HBM → XCENA CXL / OSCAR 2-bit / DeepSeek V4-Pro 稀疏注意力
  B. 把推理从 GPU 上挤走 → 字节类 LPU / SambaNova SN50 / Groq 转推理云
    ↓
推理层独立成市（Baseten $11B / OpenRouter $1.3B）
    ↓
Agent 编排层因吃 token 数最大成为新成本中心（63% 会话无子 Agent = 成本约束）
    ↓
模型公司反过来锁供应链（Anthropic 入股三大 HBM 厂商）
```

**为什么不可逆**：四象的优化目标互相矛盾——训练要高 FLOPs 密度，推理要高 token/s/watt，Agent 要低延迟调度，内存要高容量低成本。没有一种硬件能同时优化四个。

### 反直觉推论【OP】

1. **中国实验室的价格战不是烧钱补贴，是架构创新。** DeepSeek V4-Pro 把 1M KV cache 降到 10%、MiMo 降 80% caching cost——这些是 attention design 层面的真实成本下降。smol.ai 的判断：「recent API price cuts look sustainable because they reflect lower serving cost per token, not temporary subsidy.」

2. **vLLM 一周五连发的节奏不是巧合，是在「抢在硬件分裂之前」建立统一抽象层。** 如果推理硬件碎片化（GPU / LPU / CXL / ASIC），谁控制了软件抽象层谁就是新的 CUDA。vLLM 正在抢这个位置。

3. **latent.space 把这叫「Inference Inflection」——上周 unicorns（Exa/Modal/TurboPuffer），本周 decacorns（Fireworks $15B / Baseten $11B / OpenRouter on the way）。** 推理层的估值增速已经超过模型层。

### 与前两周联动

前两周的「推理效率优化」信号（Kimi PrfaaS 跨数据中心 PD 分离 / MORI-IO 单节点 PD 分离）是技术层面的观察。本周升级为**资本层面的确认**——当 Baseten 3 个月估值翻倍、OpenRouter 半年用量 5×、Groq 拿到 $650M 转型推理云，推理层已经不是「模型公司的附属」，是独立赛道。

### 值得深挖的问题

1. 如果 CXL 内存层独立成市（2028 年 $15B），XCENA vs Astera Labs vs Marvell 谁赢？
2. HBM 涨价什么时候见顶？CoWoS 从 75K 扩到 120K wafers/month（Lisa Su 预期 2026 年底）是否足够？
3. vLLM 能否成为推理层的「CUDA」？还是会被 NVIDIA Dynamo 吞掉？

---

## 趋势 D：Anthropic 从 model lab 转型为 capital-intensive agent platform company

### 核心命题（来自 smol.ai）

> Anthropic is no longer just a model lab; it is a capital-intensive agent platform company. Safety gating is becoming product segmentation. The capital raise is inference capacity for token-hungry agent workflows.

### 本周证据

| 维度 | 动作 | 解读 |
|---|---|---|
| 模型 | Opus 4.8（incremental benchmark, meaningful UX） | 模型本身不是重点，harness 释放能力才是 |
| 资本 | H 轮 $6.5B / $965B 估值 / $47B ARR | 不是训练 fuel，是 inference capacity |
| 算力 | 10 GW 签约 + 三大存储入股 | 锁住推理毛利率的供应链前提 |
| Agent 编排 | Dynamic Workflows（百级并行子 Agent） | 平台基础设施，不是产品功能 |
| 记忆 | Memory Files + Dreams + Conway | 自进化栈的 L2 层 |
| 安全 | 三档隔离 + Mythos 只给审查通过的客户 | **Safety gating = product segmentation** |
| 自进化 | Karpathy autoresearch 团队 | 自进化栈的 L4 层 |
| 利润结构 | 推理毛利率 -94%→mid-60s / Bedrock EBIT 55% | 从亏损到盈利的拐点 |

### 三个结构性判断【OP】

**1. 安全分级 = 产品分级**

Anthropic 的安全对齐可能在**故意压制**公开版本的能力（smol.ai 第三阵营：「alignment and caution may be suppressing some performance」）。Mythos 级别模型只给通过安全审查的客户——这不是「安全限制了商业化」，是「安全成为了商业化的分层工具」。越高安全等级 = 越强能力 = 越贵的客户。

**2. $65B 融资和 10 GW 签约是同一件事**

$47B ARR 意味着每月需要消耗对应数量级的推理算力。10 GW 是 ARR 兑现的物理前提。三大存储入股是推理毛利率的供应链保障（HBM 涨 95% 的环境下）。**三件事互为前置条件，不是三条独立新闻。**

**3. 竞争已经从「单次回复质量」转向「长程工作流执行」**

smol.ai 的判断：「Frontier competition has shifted from single-response quality to long-horizon workflow execution.」Dynamic Workflows（百级并行子 Agent）、Memory Files（跨会话持久化）、effort control（成本精细控制）——这些都是长程工作流的基础设施，不是聊天体验的优化。

### 与前两周联动

前两周判断「OpenAI 下场自己做生产力 vs Anthropic 专注打磨终端用户体验+开渠道分发」。本周需要修正：Anthropic 不只是「开渠道分发」，它在建设**agent platform**——从模型到 harness 到记忆到安全到算力的全栈。区别在于：OpenAI 自己做垂直 Agent（Tax AI / Rosalind / Codex），Anthropic 建平台让别人做（Dynamic Workflows + Memory Files + Code Security + Trajectory 这类第三方）。

### 值得深挖的问题

1. 如果 Anthropic 推理毛利率已到 mid-60s，但 80-90% 通过 Bedrock 且 Bedrock EBIT 55% 归 AWS——Anthropic 自己的净利润率是多少？它可能是 AWS 的利润引擎而非独立盈利体。
2. Safety gating as product segmentation 的终局是什么？是否会形成「安全等级越高 = 能力越强 = 价格越贵」的三级市场？
3. Dynamic Workflows 的 token 消耗量级是多少？百级并行子 Agent 的单次任务成本？这决定了它是「所有人都能用」还是「只有企业客户用得起」。

---

## 数据附录

### 本周融资汇总

| 公司 | 栈位 | 融资 | 估值 | 关键指标 |
|---|---|---|---|---|
| Anthropic | 模型+平台 | $6.5B H轮 | $965B | $47B ARR / 10 GW 签约 |
| Cognition | Agent 编排 | $1B+ | $26B | $492M ARR / 89% 内部代码 |
| Baseten | 推理云 | $1B 洽谈 | $11B | Q1 $200M→季末 $600M ARR |
| Groq | 推理云 | $650M | — | NVIDIA $20B「非收购」后转型 |
| Focused Energy | 能源 | €240M A轮 | — | 全球聚变 A 轮纪录 |
| XCENA | 内存层 | $135M | $570M | CXL near-memory / 2027 年收入 |
| OpenRouter | 路由 | $113M B轮 | $1.3B | 半年 5T→25T tokens/week |
| General Compute | 推理芯片 | $15M 种子 | $60M | 已下单 SambaNova $300M |
| Trajectory | Post-deployment learning | $15M | — | Harvey/Clay/Mercor 设计合作伙伴 |

### HBM / DRAM 价格（TrendForce 2026-05-27）

- DRAM 合同价 Q1 2026：**+95%** QoQ
- Q2 2026 预计：**+58-63%**（十年最陡峭单季涨幅）
- HBM 占 DRAM 总产值：2025 年底已超 **30%**
- CoWoS 产能：2025 年 ~75K wafers/month → 2026 年底预计 120K（Lisa Su）

### 风投集中度（Crunchbase Q1 2026）

- 全球 VC ~$300B（季度历史新高）
- AI 占比 **~80%**（首次单季突破）
- 4 家公司拿走 $188B（全球 VC **65%**）：OpenAI $122B / Anthropic $30B / xAI $20B / Waymo $16B
- 北美投资金额同比 +190%，交易笔数 -26%

### Agent 使用结构（SemiAnalysis）

- **63%** 会话不使用子 Agent
- **25.9%** 使用 1-5 个并行子 Agent
- **9.8%** 使用 5 个以上
- Meta **70%** 新毕业生工程师转 RL 任务

### 开源追赶速度（Epoch AI + LangChain）

- 开源权重模型落后前沿专有模型约 **4 个月**
- 2026 年 4 月 **1/3** AI 团队跑过开源权重模型（9 个月前 1/5）

---

*汇总时间：2026-05-31 | 参考源：daily-ai-news 6 天 + smol.ai (05/27-05/29) + latent.space (ESMFold2 / AI Infra Decacorns) + 联网补充（Crunchbase / TrendForce / Epoch AI / CXL 论文 / arXiv 2605.26731）*
