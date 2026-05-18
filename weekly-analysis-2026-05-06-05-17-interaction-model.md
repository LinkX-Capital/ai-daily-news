# 交互原生模型深度研究 | 端到端 vs 管道架构的转折点？

> 周报 2026.05.06-05.17 补充研究 | 基于公开信息整理

---

## 一、Thinking Machines Lab 是谁？

**创始人：Mira Murati**（前OpenAI CTO）

这不是一个无名小公司。Murati离开OpenAI后创立Thinking Machines Lab，首个产品就是Interaction Model——直接挑战她前东家的Realtime API架构。

---

## 二、核心架构：交互原生 vs 外挂交互

### 当前主流方案：管道架构（Pipeline）

```
用户语音 → ASR(语音转文字) → LLM(推理) → TTS(文字转语音) → 输出
                                    ↑
                              VAD(语音活动检测)
                              Turn管理
                              中断处理
```

**代表产品：** OpenAI Realtime API、Gemini Live、大多数语音Agent

**问题：**
- 每个环节累加延迟（ASR 200-500ms + LLM 500-2000ms + TTS 200-500ms）
- VAD（语音活动检测）是外挂组件，无法理解语义——只能检测"有没有声音"，不能判断"该不该打断"
- Turn-based：必须等用户说完才能回应，无法实现真正的同时对话

### Thinking Machines Lab 方案：交互原生（End-to-End）

```
音频/视频/文本 → [Interaction Model] → 实时响应
                  200ms micro-turn
                  无VAD/无turn边界
                  encoder-free early fusion
```

**TML-Interaction-Small 技术细节（MarktechPost/Unite.AI/VentureBeat）：**
- **276B参数MoE**（12B活跃参数）
- **200ms micro-turn**：将时间tokenize为200ms块，持续处理并发输入输出
- **Encoder-free early fusion**：音频通过dMel嵌入层、图像通过40x40 patch + hMLP编码，所有组件从头联合训练
- **双层架构**：
  - Interaction Model：实时感知与响应（快）
  - Background Model：深度推理和工具调用（慢）
  - 两者共享上下文

**关键能力：**
- 自然打断（不依赖VAD）
- 同时说话和听（全双工）
- 视频+音频+文本并发处理
- 主动发起对话（不只是被动响应）

---

## 三、Pipeline vs Realtime vs Interaction Model 三方对比

| 维度 | Pipeline（管道） | Realtime（端到端语音） | Interaction Model（交互原生） |
|------|-----------------|---------------------|---------------------------|
| **代表** | 大多数语音Agent | OpenAI Realtime API | TML-Interaction-Small |
| **延迟** | 1-3秒（累加） | <600ms | **200ms** |
| **打断处理** | VAD外挂 | 模型内置 | **原生（无VAD）** |
| **多模态** | 需要多个模型拼接 | 语音为主 | **音频+视频+文本原生** |
| **全双工** | 否 | 部分 | **是** |
| **可控性** | 高（每个环节可调） | 中 | 低（黑盒） |
| **成本** | 低（各环节可选便宜模型） | 高 | 未知 |
| **部署复杂度** | 高（多组件编排） | 中 | 低（单模型） |

### LiveKit 的判断（行业基础设施提供商）

> "Neither architecture is universally the right answer. Realtime models excel at naturalness and emotional awareness, pipelines offer control, modularity, and cost efficiency."

**市场正在分裂为两个阵营：**
- Speech-to-speech（端到端）：追求自然度
- Orchestration（管道）：追求控制力和成本

Interaction Model是第三条路——不只是语音端到端，而是**多模态交互端到端**。

---

## 四、为什么这可能是转折点？

### 论据1：Bitter Lesson

Richard Sutton的"苦涩教训"：历史上，利用计算规模的通用方法最终总是胜过利用人类知识的特定方法。

- Pipeline = 人类设计的模块化架构（ASR→LLM→TTS）
- Interaction Model = 端到端学习

如果计算足够便宜，端到端路线最终会胜出。

### 论据2：现有方案的benchmark失败

TML提出了三个新benchmark：
- **TimeSpeak**：时间感知能力
- **CueSpeak**：同时语音能力
- **ProactiveVideoQA**：视觉主动性

**现有商业实时模型（GPT-Realtime、Gemini Flash Live）均无法有效完成这些任务。** 这说明当前方案在"真正的交互"上存在结构性缺陷。

### 论据3：Mira Murati的信号价值

前OpenAI CTO选择这个方向创业，本身就是一个强信号——她比大多数人更了解当前方案的局限性。

---

## 五、反面论据：为什么可能不是转折点

### 反面1：成本和规模化

- 276B MoE持续运行200ms micro-turn = 极高的推理成本
- 每个用户会话都需要持续占用GPU（不像Pipeline可以按需调用）
- 规模化部署的经济性未验证

### 反面2：可控性问题

- 企业场景需要精确控制AI说什么、不说什么
- 端到端模型是黑盒，难以做细粒度的行为控制
- 安全护栏更难实施

### 反面3：Pipeline在快速改进

- OpenAI Realtime API已经做到<600ms
- 管道架构的每个环节都在独立优化
- "足够好"的延迟+高可控性可能比"极致延迟+低可控性"更适合商业场景

### 反面4：验证周期长

- TML-Interaction-Small是"研究预览"，不是商业产品
- 从研究到大规模部署需要1-2年
- 这期间Pipeline方案会继续改进

---

## 六、判断

**短期（6-12个月）：** Pipeline仍是主流。OpenAI/Google/xAI的管道方案已经在大规模部署（OpenAI 9亿WAU、Vapi处理10亿+通话），Interaction Model还在研究阶段。

**中期（1-2年）：** 如果TML能证明200ms交互在商业场景中的价值（比如客服转化率显著提升），大厂会跟进。关键观察点：
- 是否有大厂（Google/Meta）发布类似的交互原生模型？
- TML是否能获得大规模商业部署？
- 成本是否能降到可接受水平？

**长期（2-3年+）：** 端到端路线大概率胜出（Bitter Lesson），但"交互原生"可能不是独立产品，而是被集成到下一代基础模型中（类似多模态从独立模型变成基础模型的标配）。

**对周报的补充：** 将Interaction Model列为P2（持续追踪）是正确的。它是重要的方向性信号，但验证周期长，不影响近期投资判断。关键追踪指标：大厂是否跟进、TML的商业化进展、成本下降速度。

---

*研究时间：2026-05-17 | 来源：Thinking Machines Lab Blog, MarktechPost, Unite.AI, VentureBeat, LiveKit Blog, Ultravox, Medium*
