# 科学智能（AI4S）日报采集 + 专题报告合并稿

*整理：2026-07-27 ｜ 合并范围：`daily-ai-news-2026-*.md` 相关采集 + `reports/onepager-ai4s-recent-progress-2026-07-23.md` 专题补查内容。*

## 0. 合并口径

- **日报素材池**：提供持续信号，覆盖科研 Agent/工作流、科学发现评测、生命科学/药物发现、材料/算力/国家科研平台等主线。
- **专题报告补查**：在日报基础上补齐了一手源、专题事实和结构化研判，尤其是 Genesis/DOE、ScienceOne、KrF 光刻胶、GridSFM、Aurora、SciAgentArena、FutureHouse、Molecule.one 等。
- **最终判断**：AI4S 正从“单点预测模型”进入“科研生产系统”竞争，关键不只是模型能力，而是模型、工具、数据、算力、实验和审计闭环的组织能力。

## 1. 日报已采集素材

### 科研工作流与自主科研 Agent

- **2026-03-14｜Paper Machine 自动化科研工作流**（`daily-ai-news-2026-03-14.md:55`）
  - 支持睡前设定研究方向、醒来生成初稿；工作流结合 Claude 研究与 GPT 审稿，指向“科研辅助从单点工具走向完整工作流”。
- **2026-03-16｜Stanford / Princeton LabClaw**（`daily-ai-news-2026-03-16.md:93`）
  - 一行命令启动 200+ 科研技能，结合 LabOS、XR 眼镜与实验机器人，让科研人员保留关键决策、其余环节交给 AI 执行。
- **2026-03-26｜“科研龙虾”AI 研究助手**（`daily-ai-news-2026-03-26.md:106`）
  - 覆盖文献综述、实验设计、论文撰写等流程；日报提醒科研诚信边界问题会随主导角色增强而凸显。
- **2026-03-26｜Sakana AI Scientist 登上 Nature**（`daily-ai-news-2026-03-26.md:154`）
  - 系统可自主探索科研假设的“可能性之树”，日报将其视为 AI 从科研工具向科研主体演进的信号。
- **2026-05-21｜Google Gemini for Science**（`daily-ai-news-2026-05-21.md:52`）
  - 包含 Hypothesis Generation、Computational Discovery、Literature Insights 三类工具；从 AlphaFold 式单点工具走向多 Agent 科学工作流编排。
- **2026-06-03｜Google DeepMind 开放 Co-Scientist**（`daily-ai-news-2026-06-03.md:115`）
  - 面向个人研究者开放，支持构思、文献检索、数值计算、定理证明和理论体系搭建，具备异步有状态工作空间。
- **2026-06-10｜Co-Scientist 四个科研案例**（`daily-ai-news-2026-06-10.md:42`）
  - 以“假设生成→虚拟同行评审/假设竞赛→精炼组合”的多 Agent 流程覆盖传染病、肝病、ALS、细胞衰老等场景。
- **2026-07-01｜Anthropic Claude Science + NVIDIA BioNeMo**（`daily-ai-news-2026-07-01.md:50`）
  - 科学家专属 AI 工作台，整合 Jupyter、R、PubMed、HPC/SSH 等工具，内置 60+ 科学技能/连接器，并通过 BioNeMo 封装 NVIDIA 生科能力。

### 科学发现评测与科研判断力

- **2026-04-24｜GIANTS / GiantsBench**（`daily-ai-news-2026-04-24.md:115`）
  - Stanford & NYU 定义 insight anticipation：给定两篇父论文摘要，预测下游论文核心洞察；日报强调这是对“组合式科学洞察”的测试。
- **2026-04-26｜SimpleTES 测试时扩展框架**（`daily-ai-news-2026-04-26.md:59`）
  - 把试错拆成并行 C、深度 L、候选 K 三维搜索空间，在 21 项科学任务刷新多项结果；日报判断评估器质量与搜索成本分配成为上限瓶颈。
- **2026-06-18｜OpenAI LifeSciBench**（`daily-ai-news-2026-06-18.md:21`）
  - 750 个生命科学专家任务、173 位 PhD 级专家编写/审核、19,020 条 rubric；GPT-Rosalind pass rate 达 36.1%。
- **2026-07-01｜OpenAI GeneBench-Pro**（`daily-ai-news-2026-07-01.md:97`）
  - 从“能否执行分析”升级到“能否做科学判断”：判断数据模式是信号还是噪声、数据是否支持研究问题、下一步如何调整。

### 生命科学、药物发现与医疗 AI

- **2026-06-04｜OpenAI GPT-Rosalind 引入 GPT-5.5 能力**（`daily-ai-news-2026-06-04.md:32`）
  - 面向生命科学企业级应用，强化分子生物学、药物发现等场景，体现前沿通用模型向垂直科学领域下放。
- **2026-06-25｜Microsoft Talos 罕见病基因组重分析**（`daily-ai-news-2026-06-25.md:105`）
  - 4,735 名未确诊罕见病患者中新增 241 例诊断，额外诊断率 5.1%；把基因组重分析从一次性事件变成持续自动程序。
- **2026-07-16｜OpenAI 研究员 Miles Wang 创办 AI 药物发现公司**（`daily-ai-news-2026-07-16.md:74`）
  - 据报以约 20 亿美元估值融资约 2 亿美元；日报判断药物发现是 AI for Science 中人才与资本最集中的落点。
- **2026-07-23｜Dimension Capital 三期 8 亿美元基金**（`daily-ai-news-2026-07-23.md:89`）
  - 押注 science × compute；曾投 Chai Discovery 等，显示 AI 制药、抗衰、推理等交叉方向资本配置加速。

### 材料、算力与国家科研平台

- **2026-05-01｜中科大“灵境造物”智能科研云平台**（`daily-ai-news-2026-05-01.md:42`）
  - 整合科学大模型、垂类小模型、科研机器人、自动计算、自动实验和技能库；华为 openJiuwen / MindSpore 提供全栈国产化支撑。
- **2026-05-13｜Microsoft MatterSim / MatterSim-MT**（`daily-ai-news-2026-05-13.md:58`）
  - 实验验证版仅需 3% 原始数据达实验精度；MatterSim-MT 学统一原子表征并预测多种物理性质，用于加速计算材料发现。
- **2026-07-12｜中国首个十万卡国产算力集群**（`daily-ai-news-2026-07-12.md:35`）
  - 已承载 300+ 应用，涉及大模型、机器人、量子计算、新材料等 20+ 前沿领域，是国内 AI4S 算力底座信号。
- **2026-07-23｜Google 向 DOE Genesis Mission 承诺 4000 万美元额度**（`daily-ai-news-2026-07-23.md:32`）
  - 向 DOE 研究者开放 AlphaEvolve、AlphaFold 3、AlphaGenome、WeatherNext、AlphaEarth 等工具；日报判断 Genesis 正成为头部 AI 公司切入国家算力/数据的共同通道。

### OpenAI / 科研组织线索

- **2026-04-18/19｜OpenAI for Science / Prism 组织线索**（`daily-ai-news-2026-04-18-19-orig.md:21`）
  - Kevin Weil 曾负责 OpenAI for Science 项目；日报将其与 OpenAI 战略收缩、聚焦企业 AI 和核心模型放在一起观察。

## 2. 专题报告已补齐的关键事实

专题报告文件：`reports/onepager-ai4s-recent-progress-2026-07-23.md`。其中代表性发布表如下：

| 日期 | 产品/技术 | 关键信号 |
|---|---|---|
| 04‑16 | OpenAI GPT‑Rosalind | 生命科学专用前沿推理模型，接入 50+ 数据库与工具，受控访问 |
| 04‑25 | Google Decoupled DiLoCo | 跨数据中心异步训练：带宽 198→0.84 Gbps，高故障率下有效产出 88% |
| 04‑29 | 中科院 ScienceOne 100 | 1 科学基础模型 + 8 学科大模型 + 智能体工厂，覆盖 50+ 院所、100+ 场景 |
| 05‑12 | 上海 AI Lab KrF 光刻胶闭环 | 「书生」+ 自动化合成，PDI<1.3、金属杂质<10ppb，批次稳定 |
| 05‑12 | Microsoft MatterSim‑MT | 多任务材料基础模型；3500 万+ 第一性原理标注结构，89 种元素 |
| 05‑13 | Microsoft GridSFM | 面向交流最优潮流的离散神经算子；150+ 网架、约 50 万场景训练 |
| 05‑19 | Google Gemini for Science / Co‑Scientist | 多智能体「假设锦标赛」、并行计算发现、文献洞察；30+ 科学技能 |
| 05‑19 | FutureHouse Robin（Nature） | 多智能体贯通假设→实验→洞察，原代人 RPE 细胞验证 |
| 06‑02 | Microsoft Discovery GA | 面向科研与工程的企业级智能体平台正式商用，含桌面 App 预览 |
| 06‑03 | Google Gemma 4 12B | 无编码器统一多模态，16GB 内存可运行 |
| 06‑04 | GPT‑Rosalind 引入 GPT‑5.5 | 强通用底座 + 领域增量训练；发布 LifeSciBench（750 专家任务） |
| 06‑17 | OpenAI × Molecule.one 化学家 | GPT‑5.4 + Maria 实验室，10080 次反应，Chan–Lam 产率 16.6%→25.2% |
| 06‑23 | NVIDIA BioNeMo Agent Toolkit | 将生科模型/库/算力封装为可被任意智能体调用的技能；50+ 机构采用 |
| 06‑23 | DOE Quantum Genesis | Genesis 核心组成，目标 2028 年部署全球首台科研级容错量子计算机 |
| 06‑24 | Genesis / NNSA Aires Tide | AI+HPC+增材制造的飞行试验体，成本低 15×、快 7× |
| 06‑30 | Anthropic Claude Science | 60+ 技能/连接器、HPC/SSH、审稿智能体、可审计工件 |
| 07‑09 | Microsoft Aurora 1.5 | +22 天气变量、逐小时、概率集合预报；开放代码与权重，88.9% 指标超 ECMWF 集合 |
| 07‑12 | 首个十万卡国产算力集群 | 承载 300+ 应用、量子计算/新材料等 20+ 前沿领域 |

日报精确关键词未直接命中、但专题报告已作为正文事实纳入的重点包括：

- ScienceOne 100
- 上海 AI Lab KrF 光刻胶闭环
- GridSFM
- Aurora 1.5
- SciAgentArena
- FutureHouse Robin
- OpenAI × Molecule.one 化学家
- Quantum Genesis
- NNSA Aires Tide
- 文曲星元训练场

## 3. 合并后的主题研判

### 3.1 从科研助手到科研工作台
Claude Science、Gemini for Science、Co-Scientist、LabClaw、Paper Machine 等共同说明，产品形态正在从“问答/写作助手”升级为“科研工作台”：连接文献、数据库、代码、HPC、实验工具和可审计工件。

### 3.2 从静态基准到科学判断力
GIANTS、LifeSciBench、GeneBench-Pro、SciAgentArena 代表评测口径变化：不再只看模型能否答题，而看能否组合洞察、处理专家级任务、区分信号与噪声、规划下一步研究。

### 3.3 生命科学/药物发现最先形成资本与人才密度
GPT-Rosalind、LifeSciBench、GeneBench-Pro、Talos、OpenAI 研究员创业、Chai Discovery/Dimension Capital 等构成连续信号，说明生命科学是 AI4S 商业化和资本配置最活跃的入口。

### 3.4 长期壁垒来自物理闭环和数据回流
MatterSim、KrF 光刻胶、Molecule.one、Aires Tide 等显示，AI4S 的价值不止于“给建议”，而在于通过仿真、实验、中试或真实系统验证，把结果回流为独特数据资产。

### 3.5 国家科研平台化正在成为主战场
Genesis Mission、Quantum Genesis、中国十万卡国产算力集群、灵境造物等说明，AI4S 正从公司产品竞争上升到国家实验室、算力网络、科学数据和重大挑战清单的体系竞争。

## 4. 后续建议

- 建议为 AI4S 建一个专题索引文件，把日报条目、官方源、补查源统一挂进去，避免后续追溯困难。
- 中国侧条目（ScienceOne、KrF、文曲星元、十万卡）应优先回填官方/机构源，减少二手媒体口径偏差。
- Genesis 相关金额要拆分企业额度、预算申请、资金机会、已拨款四类口径，避免混用。