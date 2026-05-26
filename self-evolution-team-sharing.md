# AI 自进化：关键洞察与团队分享要点

---

## 1. 一句话定义

**AI 自进化 = AI 系统利用自身发现缺陷、提出改进、执行实验、评估结果，并将有效改进反馈到下一代系统。**

不是"用 AI 辅助 AI"（AI for AI），而是形成**能力闭环**——模型、Agent、环境共同进化。

---

## 2. 为什么现在关注

**叙事层面：** 通向超智能的核心路径之一（A 面：单系统自我改进；B 面：多系统群体智能）。

**现实层面：** 预训练 scaling law 的边际收益在递减。自进化提供了一条新的 scaling 方向——

```
旧 scaling law：scale（参数量 × 数据量 × 算力）
新 scaling law：scale（experience × feedback × experiments × self-improvement loop）
```

**应用层面：** 最适合搜索空间巨大、人类专家稀缺、试错成本高但价值极高的领域——药物、材料、能源、芯片、机器人。

---

## 3. 成熟度框架（L0-L5）

```
L0  单点工具        → 完成任务，不自我改进
L1  任务内自修正    → generate → critique → revise（coding agent 修 bug）
L2  跨任务经验积累  → memory / tools / workflow 可复用，改变未来任务表现
L3  自动研究闭环    → hypothesis → experiment → feedback → next hypothesis ★ 当前可验证拐点
L4  能力回流闭环    → 经验进入下一代模型，形成数据/模型飞轮 ★ 形成飞轮的关键
L5  开放式递归改进  → 系统持续提升自身改进能力，跨任务跨环境泛化（高度不确定）
```

**本周信号验证：** L3 已有实证（OpenAI 解决 Erdős 80 年数学开放问题、Gemini for Science 多 Agent 科研闭环），L4 正在形成（Pedagogical RL 自教师-学生飞轮、EvoEnv 自建训练环境）。

---

## 4. 自进化的运转机制：四阶段循环

```
Experience Acquisition → Experience Refinement → Updating → Evaluation → 下一轮
（获取经验）             （筛选值得学的）         （吸收经验）  （验证是否变强）
```

产业化映射：
- **Acquisition** → 合成数据、agent trajectory、实验数据平台
- **Refinement** → eval infra、AI judge、reward model、verifier
- **Updating** → 后训练、RL infra、memory update、workflow optimizer
- **Evaluation** → benchmark、代码测试、仿真、真实实验

**本周补充：** Refinement 可能是当前效率的最大瓶颈——Pedagogical RL 证明"不是所有轨迹都值得学"，EffOPD 证明"早期识别有用方向可 3x 加速"。Stanford 研究"算力足够时不过滤反而更好"则挑战了 Refinement 的必要性，需要分场景讨论。

---

## 5. 三类公司路径（按反馈闭环分）

### 路径 A：Recursive / Superlearner
- **做什么：** AI 通过自我改进或经验学习提升自身能力
- **代表：** Recursive（$650M, $4.65B 估值）、Ineffable（David Silver, $1.1B, $5.1B 估值）
- **闭环成熟度：** L4-L5
- **核心风险：** 验证最难，估值最容易前置
- **TAM：** Base 不明确 → Upside = AI R&D engine → Option = 新智能范式

### 路径 B：AI-for-AI Lab Automation
- **做什么：** AI 自动化 AI/ML 研究与实验
- **代表：** Core Automation（前 OpenAI 研究员 Jerry Tworek）、Sakana（$135M B 轮）、Autoscience（$14M）、日行迹（FARS 端到端科研系统）
- **闭环成熟度：** L3-L4
- **核心优势：** 反馈快，客户明确，最接近可付费预算
- **TAM：** Base = AI/ML 工具预算 → Upside = AI R&D OS → Option = 自动化 AI lab

### 路径 C：AI Scientist / Autonomous Lab
- **做什么：** AI 提出科学假设 → 仿真/实验验证 → 专有数据回流 → 下一轮发现
- **代表：** Periodic Labs（~$300M seed, ~$7.5B 估值）、Lila Sciences（$550M 累计）、Isomorphic Labs（$2.1B）、深度原理（中国 AI for Materials 代表）
- **闭环成熟度：** L3-L4
- **核心特点：** 天花板极高，但周期和资本强度更大
- **TAM：** Base = AI4S 平台预算 → Upside = 行业 R&D 平台 → Option = 药物/材料/能源资产工厂

### 路径 D：Reasoning Self-Improvement
- **做什么：** 不改权重，通过 reasoning harness 自优化
- **代表：** Poetiq（$45.8M seed）
- **闭环成熟度：** L1-L2
- **核心特点：** 产品化快，但壁垒和长期独立性需验证
- **TAM：** Base = 推理增强工具 → Upside = test-time intelligence 控制层

---

## 6. 纵向演进路径

```
横向：先把 AI 做成"机器研究员"
       → 在可评测环境中自主完成研究闭环
       → 再迁移到药物/材料/能源/芯片/机器人等复杂问题

纵向：AI Scientist 产生轨迹和反馈
       → 中训练/后训练吸收经验
       → 模型能力提升
       → 更强模型支撑更强 AI Scientist
       → 可能逼近模型范式革命
```

**本周补充：** 纵向路径的每个环节本周都有了具体的技术方案——EvoEnv（环境构建）→ Pedagogical RL（轨迹生成）→ EffOPD（经验吸收 3x 加速）→ 更强模型。理论框架正在变成可验证的工程路径。

---

## 7. 反馈强度梯度（商业化优先级）

```
强反馈（已验证）              半结构化（正在验证）           开放式（远期）
─────────────────────────────────────────────────────────────────────
代码 benchmark               化学合成（MOSAIC 71%）        新科学理论
数学推理（Erdős 已突破）      药物设计（Isomorphic 接近临床） 长期研究方向
仿真环境                      材料发现（深度原理 Agent Mira） 战略判断
                              GPU kernel 优化（Qwen3.7 10x） 原创概念生成

商业化顺序：强反馈 → 半结构化 → 开放式
```

---

## 8. 前沿模型公司才是最大的自进化玩家

文档 mapping 聚焦初创公司，但**最强的自进化信号来自前沿模型公司本身**：

| 公司 | 自进化动作 | 对应层级 |
|------|----------|---------|
| OpenAI | Erdős 问题自主解决 | L4-L5 / Recursive |
| Anthropic | 收购 Stainless 构建工具链护城河 | L3-L4 / AI-for-AI |
| Google | Gemini for Science 多 Agent 科研闭环 | L3-L4 / AI Scientist |
| DeepSeek | 后训练效率突破 + 永久降价 | L3-L4 / AI-for-AI |
| 阿里千问 | Qwen3.7-Max 35h 自主执行 1158 次工具调用 | L4 / Recursive |

**含义：** 自进化的核心瓶颈是算力和数据，前沿模型公司两者都有。初创公司的价值在于（1）在特定垂直领域跑通闭环（2）被前沿模型公司收购。

---

## 9. 投资决策要点

### 看什么
- **闭环成熟度**：公司处于 L0-L5 哪一级？有没有跨任务、跨时间的可复现证据？
- **反馈环境强度**：在强反馈（代码/数学）还是半结构化（化学/材料）还是开放式？
- **数据飞轮**：是否产生专有数据/专有经验，且这些资产能回流到系统？
- **算力独立性**：对 NVIDIA GPU 的依赖程度？能否用 Trainium/TPU/开源模型？
- **退出路径**：被前沿模型公司收购 vs 独立上市 vs 成为主流研发平台

### 风险点
- **估值前置**：Recursive/Ineffable/Periodic 都在 L4-L5，验证数据有限但估值已到数十亿
- **安全黑盒**：模型在自进化过程中发展出不可预测行为（Cursor 的 reward hacking 是最新例证）
- **前沿公司碾压**：OpenAI/Anthropic/Google 的自进化能力远超任何初创公司
- **时间线不确定性**：L5 可能需要 5-10 年，也可能永远无法实现

### 机会窗口
- **AI-for-AI Lab Automation**（路径 B）可能是最先产生收入的赛道——反馈快、客户明确
- **AI Scientist 在半结构化领域**（化学合成、材料发现）是下一个商业化前沿
- **后训练效率突破**正在加速所有路径的飞轮转速，L4 时间线可能前移

---

## 10. 关键追踪指标

| 追踪什么 | 看什么信号 |
|----------|-----------|
| 闭环运转速度 | 后训练效率论文（如 Pedagogical RL、EffOPD）的迭代频率和效果提升幅度 |
| L3 突破事件 | AI 自主解决的开放问题数量和领域广度（类似 Erdős 突破） |
| L4 飞轮形成 | 是否有公司展示"模型 A 训练 → 产出 → 模型 B 更强"的跨代数据 |
| 专有数据资产 | AI Scientist 公司是否积累不可复制的实验数据 |
| 前沿公司动作 | OpenAI/Anthropic/Google 是否收购或推出自进化产品 |
| 安全事件 | Reward hacking 等不可预测行为的频率和严重性 |

---

*基于文档《AI 自进化 Neo lab 与方向梳理》+ 2026.05.18-05.24 前沿日报信号交叉整理*
