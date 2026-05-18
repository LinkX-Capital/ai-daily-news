# 深度研究：Thinking Machines Lab Interaction Models

> 2026-05-12 | 模型前沿 | L2a 基础模型 + L4 应用

---

## 一、事件概述

2026年5月11日，Thinking Machines Lab（TML）发布"Interaction Models"研究预览——一个将实时多模态交互作为模型原生能力（而非外挂组件）的新架构。首个模型 **TML-Interaction-Small** 为 276B MoE（12B活跃参数），在 FD-bench v1.5 交互质量上达到最优，Audio MultiChallenge 上超过所有非thinking模型。

这是 Mira Murati 离开 OpenAI 创办 TML 以来发布的**首个重大模型成果**。

---

## 二、Thinking Machines Lab 背景

### 2.1 公司概况

| 维度 | 信息 |
|------|------|
| 创立时间 | 2025年2月 |
| 总部 | 旧金山 |
| 法律结构 | Public Benefit Corporation |
| 员工数 | ~100人 |
| 创始人 | Mira Murati（前OpenAI CTO，主导ChatGPT/GPT-4/DALL-E） |
| 核心团队 | John Schulman（首席科学家，OpenAI联合创始人）、Lilian Weng |
| 顾问 | Bob McGrew（前OpenAI CRO）、Alec Radford（GPT-2/3作者） |

### 2.2 团队变动

值得注意的是，TML经历了显著的人才流失：
- **Barret Zoph**（联合创始人/CTO）：2026年1月被解雇，回到OpenAI
- **Andrew Tulloch**（联合创始人）：2025年10月被Meta Superintelligence Labs挖走
- **Luke Metz**（联合创始人）：2026年1月回到OpenAI

三位联合创始人离职，说明TML在人才争夺战中处于劣势。这次Interaction Models的发布，某种程度上是对外界"TML还在做什么"质疑的回答。

### 2.3 融资与算力

| 轮次 | 时间 | 金额 | 估值 |
|------|------|------|------|
| Seed | 2025年7月 | $20亿 | $120亿（a16z领投，Nvidia/AMD/Cisco跟投） |
| NVIDIA战略合作 | 2026年3月 | 未披露 | 1GW Vera Rubin算力部署 |
| 下一轮（传闻） | 2025年11月 | — | 目标$500亿估值 |

$120亿种子轮是历史最大，但对比Anthropic $900亿和OpenAI $3000亿估值，TML的资本密度并不突出。NVIDIA的1GW算力合作是关键——Interaction Models的实时推理对算力需求极高。

### 2.4 此前技术输出

| 时间 | 博文 | 核心贡献 |
|------|------|----------|
| 2025.09 | Defeating Nondeterminism in LLM Inference | Horace He；解决LLM推理服务中的非确定性问题 |
| 2025.09 | Modular Manifolds | Jeremy Bernstein；流形约束下的优化器设计 |
| 2025.10 | On-Policy Distillation | Kevin Lu / John Schulman；在线蒸馏，9-30x计算节省 |
| 2025.10 | Announcing Tinker | 首个产品——开源模型微调API |
| **2026.05** | **Interaction Models** | **首个模型架构发布** |

从优化器、蒸馏到推理确定性，TML的技术积累聚焦在**训练和推理基础设施**，这为Interaction Models的端到端训练和实时推理优化奠定了基础。

---

## 三、核心创新：Interaction Models架构

### 3.1 问题定义

当前AI交互的根本瓶颈：**turn-based（轮次制）接口**。

| 问题 | 说明 |
|------|------|
| 模型"冻结"感知 | 用户说话时模型等待，模型生成时感知冻结 |
| 外挂harness | VAD（语音活动检测）、对话管理等组件拼接在模型外部 |
| 单线程体验 | 无法同时听和说，无法在说话时处理视觉输入 |
| Human-out-of-loop | 自主Agent模式下用户被推出去 |

**核心主张**：交互性应该与智能同步扩展（"interactivity should scale alongside intelligence"）。当交互能力是模型原生的一部分时，scaling model = 更聪明 + 更好协作。

### 3.2 架构设计

```
用户 ←→ 交互模型（实时，200ms micro-turn）
              ↕ 共享上下文
         后台模型（异步，深度推理/工具调用）
```

**双模型协同**：
- **交互模型**：持续在线，200ms粒度处理音频+视频+文本的并发输入输出
- **后台模型**：处理需要深度推理的任务（工具调用、搜索、长链推理），结果异步注入对话
- 两者共享完整上下文，交互模型始终"在场"

**关键设计决策**：

| 设计 | 选择 | 理由 |
|------|------|------|
| 时间粒度 | 200ms micro-turn | 接近人类感知阈值，支持实时并发 |
| 多模态融合 | Encoder-free early fusion | 不依赖Whisper等外部编码器，端到端训练 |
| 音频编码 | dMel嵌入层 | 轻量化，与transformer co-trained |
| 视觉编码 | 40x40 patch + hMLP | 无需大型视觉编码器 |
| 音频解码 | Flow head | 流式语音生成 |
| MoE策略 | 276B总参/12B活跃 | 推理效率与能力的平衡 |
| 推理优化 | Streaming sessions | 已upstream至SGLang，避免频繁内存重分配 |

### 3.3 新能力

| 能力 | 说明 | 传统turn-based能否实现 |
|------|------|----------------------|
| 无缝对话管理 | 模型隐式追踪用户是在思考/让步/自我纠正/邀请回应 | 需要外部VAD+对话管理器 |
| 口头/视觉插话 | 模型在适当时机主动插话，不等用户说完 | 否 |
| 同时语音 | 用户和模型同时说话（如实时翻译） | 否 |
| 时间感知 | 模型有直接的时间流逝感 | 否 |
| 并发工具调用 | 边说话边搜索/生成UI | 需要harness编排 |

### 3.4 Trainer-Sampler Alignment

一个值得关注的技术细节：TML实现了**bitwise trainer-sampler对齐**——训练和推理的数值结果完全一致。这在LLM中极为罕见（通常不同batch size会导致浮点累积顺序差异），对调试和稳定性有重要价值。实现方式包括：
- NVLS实现的低延迟确定性通信内核（Blackwell架构）
- Split-KV注意力中一致的累积顺序

---

## 四、Benchmark分析

### 4.1 现有基准

| 基准 | TML表现 | 对比 |
|------|---------|------|
| **FD-bench v1.5**（交互质量） | **最优** | 超过GPT-Realtime-2.0、Gemini-3.1-flash-live |
| **Audio MultiChallenge**（智能+指令遵循） | **超过所有非thinking模型** | 包括GPT-Realtime-2.0 (minimal/xhigh)、Gemini-3.1-flash (minimal/high) |

关键点：TML-Interaction-Small在**交互质量和智能同时领先**，这是一个新的前沿——此前没有模型能同时做到。

### 4.2 TML提出的新基准

| 基准 | 测什么 | 现有模型表现 |
|------|--------|-------------|
| **TimeSpeak** | 定时语音触发（如"每4秒提醒我呼吸"） | 无法完成 |
| **CueSpeak** | 语义线索触发（如"每次我切换语言，纠正我"） | 无法完成 |
| **ProactiveVideoQA** | 视频内容变化时主动回答 | 无法完成 |
| **RepCount-A** | 视频中数俯卧撑/动作次数 | 无法完成 |
| **Charades** | 视频动作定位（说start/stop） | 无法完成 |

**GPT-Realtime-2.0和Gemini Flash Live在这些任务上"保持沉默或给出错误答案"**。这意味着TML不仅在已有赛道上领先，还在定义新赛道。

### 4.3 局限性

- **模型规模**：276B/12B是"Small"，更大的预训练模型"太慢无法在实时设置中服务"
- **长对话**：持续音视频积累上下文快，长会话的上下文管理仍是未解决问题
- **网络依赖**：低延迟流式需要可靠连接
- **安全**：实时交互对安全的挑战不同于turn-based，仍在探索

---

## 五、竞品对比

### 5.1 三条技术路线

当前实时多模态交互领域存在三条不同的技术路线：

```
路线A：Harness拼装（Turn-based模型 + 外挂组件）
路线B：原生交互（从头训练交互能力进模型）
路线C：角色表演（视频生成 + 实时驱动）
```

#### 路线A：Harness拼装 — 在turn-based模型上外挂实时交互

**代表**：GPT-Realtime（OpenAI）、Gemini Live（Google）、Qwen-Omni

**技术方案**：
- 底层仍是传统turn-based LLM
- 外接VAD（语音活动检测）判断用户是否说完
- 对话管理器（Dialog Manager）编排多轮交互
- ASR→LLM→TTS管线串联，各环节独立

**优势**：
- 复用已有大模型能力，工程化成熟
- 可插拔替换组件（升级LLM不影响交互层）
- 已有商用产品，用户基数大

**劣势**：
- VAD判断不智能（无法区分"用户在思考"和"用户说完"）
- 模型在说话时感知冻结（无法同时听和说）
- 无法做视觉主动性（只能响应语音，不能主动看屏幕说话）
- harness组件的能力天花板低于模型自身能力

**当前状态**：商用主流，但TML论文明确引用Anthropic自己的研究预览版模型卡："when used in an interactive, synchronous, 'hands-on-keyboard' pattern, the benefits of the model were less clear"——连模型厂商自己都承认turn-based在交互场景下效果打折。

#### 路线B：原生交互 — 交互能力作为模型原生组成部分

**代表**：TML Interaction Models、Moshi（Kyutai）、MiniCPM-o 4.5（面壁智能）、InternLM-OmniLive（上海AI Lab）

**技术方案**：
- 从头训练，音频/视频/文本作为统一的token流
- 持续双向流（非轮次），200ms粒度
- 无需外部VAD/Dialog Manager
- encoder-free early fusion（TML特有）

**优势**：
- 交互质量上限高——scaling law同时提升智能和交互
- 支持同时语音、视觉主动性、时间感知等harness无法实现的能力
- 端到端训练，组件间无信息损失

**劣势**：
- 训练成本极高（需要大规模音视频+文本配对数据）
- 推理延迟约束强（276B模型已是"Small"，更大模型"太慢"）
- 尚无成熟商用产品

**学术-产业光谱**：

| 模型 | 规模 | 原生交互 | 视觉 | 智能水平 | Thinking | 状态 |
|------|------|----------|------|----------|----------|------|
| **TML-Interaction-Small** | 276B/12B MoE | 是（200ms） | 是 | 接近非thinking前沿 | 后台模型 | 研究预览 |
| Moshi | 7B | 是 | 否 | 低 | 否 | 开源 |
| MiniCPM-o 4.5 | 8B | 是 | 是 | 低 | 否 | 开源 |
| InternLM-OmniLive | 未公开 | 是（长视频流） | 是 | 中 | 否 | 研究 |
| ROMA | 未公开 | 是 | 是 | 中 | 否 | 研究 |

**关键观察**：TML是唯一在"原生交互 + 前沿智能"交集处的玩家。Moshi/MiniCPM-o证明了原生交互方向正确，但7-8B规模离实用差两个数量级。

#### 路线C：角色表演 — 视频生成模型驱动实时交互

**代表**：LPM 1.0（Anuttacon/蔡浩宇）、MIDAS、LiveTalk

**技术方案**：
- 基于视频生成模型（非LLM架构）
- 输入：图像/音频 → 输出：视频帧流
- 实时生成角色表演（说话、唱歌、倾听、表情）
- 全双工对话、身份一致性

**与TML的差异**：
- LPM的目标是"表演"（生成逼真视频），TML的目标是"交互智能"
- LPM不追求高智能推理/工具调用，追求视觉逼真度
- LPM是L4应用层产品，TML是L2a基础架构

**Anuttacon/LPM 1.0**（用户补充）：
- 蔡浩宇AI公司成员（据传团队已被裁）发布
- 基于视频的角色表演模型，实时说话/唱歌/倾听/反应/表达情绪
- 关键优势：性能质量、情感对话、精确口型同步、身份保留
- 目标场景：对话代理、直播角色、游戏NPC的视觉引擎
- 来源：arXiv 2604.07823

### 5.2 下游应用延伸

#### 有明确信号的场景

**AI编程助手** — TML论文中明确提到的场景

> "tell me when I've written a bug in my code" — TML视觉主动性示例

当前编程助手（Claude Code、Cursor、Gemini Code Assist）都是turn-based。Anthropic computer use用截图→分析的方式做视觉理解，但仍需要用户主动触发。Interaction Models的视觉主动性可以让编程助手**持续看屏幕并主动插话**。

但工程化门槛高：需要IDE深度集成、屏幕流处理、代码语义理解的联合优化。这是方向正确但短期难以落地的场景。

**通用语音助手** — 最直接的应用

ChatGPT/Gemini/Claude的voice mode是"语音版chatbot"。Interaction Models能实现：
- 同时听和说（无需等用户说完）
- 自然中断和纠正（不用从头来）
- 多模态协作（指着屏幕讨论）

Google Project Astra已在追求"proactive responses"和"no interrupt or time lag"，但实现方式仍是harness方案。这是最大的商业赛道，也是竞争最激烈的。

**游戏NPC** — 与角色表演模型的互补

Interaction Models提供"交互智能"，LPM等视频生成模型提供"视觉表演"。两者结合可以实现：
- NPC能看玩家动作、听语调、做出情感反应
- 实时全双工对话，不再是预设脚本

但注意：这是两个不同系统的组合，不是单一架构能解决的。

#### 推测性场景（无市场信号）

- **具身智能**：理论上持续感知比"拍照→分析→行动"更优，但需要物理世界可靠性验证，且当前无团队在使用类似架构。与冯瑶/刘淼的"human-in-the-loop"概念不同——后者指训练数据引入人类行为，不是实时交互。
- **客服/销售、教育**：理论上可行，但无任何来自TML或市场的定向信号，暂不展开。

### 5.3 竞争格局判断

| 玩家 | 威胁程度 | 路线 | 优势 | 弱点 |
|------|----------|------|------|------|
| OpenAI | 高 | A（harness） | GPT-Realtime商用产品、用户基数、算力 | harness路线的技术天花板 |
| Google | **最高** | A（harness） | Astra愿景、Gemini Live API、TPU算力、工程化能力最强 | 同样受harness限制；COSMO是端侧小模型，与原生交互架构量级不同 |
| Anthropic | 中 | A | Claude Code/Cowork多模态、computer use | 未公开进入实时交互赛道 |
| Kyutai | 中 | B | Moshi是开源先驱 | 规模小、无视觉、商业化弱 |
| 中国团队 | 中低 | A+B | MiniCPM-o/Qwen-Omni有技术基础 | 实时交互产品化差距大 |

**注意**：目前没有证据表明OpenAI或Google在研发路线B（原生交互）架构。所有公开产品都是路线A（harness）。Google的威胁主要来自资源优势和Astra愿景，而非技术路线的一致。

### 5.4 关键学术论文

| 论文 | 团队 | 与TML的关系 |
|------|------|-------------|
| Moshi (2024) | Kyutai（Defossez等） | 全双工语音的先驱，TML引用为prior work |
| dMel (Bai等 2024) | — | TML的音频token化方案基础 |
| MoshiRAG (2026) | Kyutai | 异步知识检索用于全双工模型，类似TML的后台模型思路 |
| On-Policy Distillation | TML（Kevin Lu/Schulman） | TML自己的训练方法论，9-30x计算节省 |
| MiniCPM-o 4.5 (2026) | 面壁智能 | 路线B的开源代表，实时全双工omni-modal |

**相关但不同方向**：

| 论文 | 团队 | 说明 |
|------|------|------|
| LPM 1.0 (2026) | Anuttacon（蔡浩宇） | 视频驱动的角色表演模型，解决"逼真视觉"而非"交互智能"，是不同问题 |
| Artic (2026) | — | MLLM视频助手的实时通信优化 |
| PhoStream (2026) | — | 移动端omnimodal助手流式benchmark |

---

## 六、投资与商业意义

### 6.1 在L2a/L4框架中的定位

```
L1 计算范式：TML依赖NVIDIA 1GW Vera Rubin算力，无自研芯片
L2a 基础模型：Interaction Models是新架构范式（交互原生），非传统LLM
L3 AI Infra：SGLang upstream、streaming sessions、推理优化是Infra贡献
L4 应用：语音助手和编程助手有明确信号，其他场景为推测
```

**核心判断**：TML在L2a开创了"交互原生模型"子赛道，但目前是架构创新，离商业化还有距离。

### 6.2 市场信号

- **$120亿估值 + $20亿种子轮**：市场给予足够信任，但对比Anthropic/OpenAI仍属早期
- **NVIDIA 1GW合作**：算力保障是必要条件，实时推理的算力成本将是关键
- **产品Tinker（微调API）**：与Interaction Models方向不同，说明TML在探索多个产品方向
- **人才流失**：3位联合创始人离开是负面信号，技术团队的稳定性值得关注

### 6.3 竞争格局判断

| 玩家 | 威胁程度 | 理由 |
|------|----------|------|
| OpenAI | 高 | GPT-Realtime已有商用产品，用户基数大；未知是否在研发原生交互架构 |
| Google | 高 | Gemini Live有视觉能力，工程化优势，TPU算力；Astra愿景方向一致但实现路线不同 |
| Kyutai | 中 | Moshi是开源先驱，但规模小、无视觉 |
| 中国团队 | 中低 | MiniCPM-o/Qwen-Omni有技术基础，但实时交互产品化差距大 |

---

## 七、风险与不确定因素

1. **技术风险**：276B模型的实时推理成本极高，"Small"版已挑战极限，更大模型"太慢"
2. **产品化风险**：从研究预览到商用产品的路径不明确，Tinker和Interaction Models是两条不同的路
3. **人才风险**：3位联合创始人已离开，团队稳定性是持续隐忧
4. **竞争风险**：OpenAI/Google的资源优势可能让他们在原生交互方向快速跟进，但时间线不确定
5. **安全风险**：实时交互的安全边界与传统turn-based完全不同，红队测试经验不足
6. **需求验证**：原生交互能力是否有足够强的PMF？多数用户可能对harness方案"够用就好"

---

## 八、结论

### 核心判断

1. **技术方向正确**：从turn-based + harness → 原生交互，符合"bitter lesson"端到端学习路线。这是AI交互的长期演进方向。

2. **当前领先但窗口有限**：TML在交互质量+智能的联合前沿上是唯一的玩家，但OpenAI/Google的资源优势可能在未来抹平这一差距，具体时间线不确定。

3. **276B/12B是妥协而非终点**：更大的预训练模型"太慢"，说明实时交互对推理速度的约束正在倒逼架构创新——这可能催生新的模型设计范式（如专门为micro-turn优化的稀疏架构）。

4. **商业化路径不明**：编程助手和语音助手是有明确信号的场景，但都需要大量工程化工作。L4应用层的价值需要PMF验证。

### 关注节点

- [ ] 研究预览开放时间及用户反馈（预计未来几个月）
- [ ] 更大模型发布时间线（"later this year"）
- [ ] OpenAI/Google的回应产品（GPT-Realtime-3.0? Gemini Live 2.0?）
- [ ] TML下一轮融资动态（$500亿估值传闻）
- [ ] 开源社区对Interaction Models架构的复现进展

---

*研究基于：[Thinking Machines Lab Blog](https://thinkingmachines.ai/blog/interaction-models/)、[Semantic Scholar](https://semanticscholar.org)、公开报道*

关联延伸：蔡浩宇AI公司Anuttacon成员 （据说这个团队已经被裁）分享的LPM 1.0——一个基于视频的角色表演模型，能够实时说话、唱歌、倾听、反应和表达情绪。

- 生成全双工对话、身份一致的无限长度生成以及细腻逼真的人类般表演。
- 基于共同设计的数据管道、基础模型、在线模型和流式推理优化进行构建。
- 相比其他视频生成模型的关键优势：性能质量、情感对话、精确口型同步、身份保留和逼真的自然度。

将图像转化为表演视频，LPM 1.0 作为对话代理、直播角色和游戏 NPC 的视觉引擎。
来源：[@AilingZeng81332](https://x.com/AilingZeng81332/status/2042464987529298244) 
Page: http://large-performance-model.github.io
Arxiv: https://huggingface.co/papers/2604.07823