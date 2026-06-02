# 前沿模型周报 | 2026.05.19 — 06.02

> 基于 05.19-06.02 前沿动态的全栈信号分析
> 置信度标注：**高** = 多源交叉验证 | **中** = 有数据支撑但需持续观察 | **低** = 单一信号

---

## 信号矩阵

> 模型层 × 两条主线：能力跃迁（突破天花板）vs 效率革命（压低成本/延迟）

```
              Thread A                                Thread B
           能力跃迁                                 效率革命
        （突破天花板）                            （压低成本/延迟）
 ──────┬──────────────────────────────────────────────────────────────
       │  Qwen3.7-Max Code Arena #2 编程         GLM-5.1-highspeed 400 tok/s
       │  Gemini 3.5 Flash I/O 编程旗舰          MiniCPM5-1B 端侧 1B 超越 2B
       │  Gemini Omni 世界模型                    BitCPM-CANN 昇腾 1.58-bit 全栈
       │  AlphaProof Nexus 攻克 56 年 Erdős      Nemotron Diffusion 4× Qwen3
 模型  │  OpenAI 通用模型解 80 年单位距离         腾讯 Hy-MT2 1.25-bit/440MB
       │  Cursor Composer 2.5 长程 Agent           LongCat-Video-Avatar 8 步推理
       │  Cohere Command A+ 218B Apache 2.0       昆仑 SkyClaw-v1.0 1M 上下文极低价
       │  快手 Keye-VL-2.0 首个 DSA 多模态       Qwen3.7-Max 隐式缓存上线
       │  Grok V9-Medium 1.5T 完成训练            网易子曰4 27B 教育全栈开源
       │  Claude Opus 4.8 缺陷漏检降4×           EAGLE 3.1 接受长度提升2×
       │  Step-3.7-Flash 198B MoE 多模态         MAI-Image-2.5 Arena 文生图#3
       │  Qwen3.7-Plus TerminalBench2.0 70.3     Mellum2 10B MoE IDE 原生编程
       │  NVIDIA Cosmos 3 物理AI世界模型          MiniMax M3 编程接近 Opus 4.7
       │  Wall-OSS-0.5 开源 VLA 精密操作 39.6%   MiMo-V2.5 Hybrid SWA KVCache 1/7
       │  GPT-5.6 1.5M 上下文（泄露）
       │  Mythos 1 进入 Claude Code / Security
       │  SaaS-Bench：Opus 4.7 端到端仅 3.8%
       │  Stanford ABA：25.7% benchmark 有缺陷
       │  Qwen CUA-Gym：OSWorld 72.6%
       │  ★★★ 极强                               ★★★ 极强
 ──────┴──────────────────────────────────────────────────────────────
```

**开源反超、数学破壁——三周 24 模型释放的拐点信号：前沿竞争从能力竞赛转向效率博弈。** 能力跃迁侧，Google 终结 96 天沉寂在 I/O 一次性放出 Gemini 3.5 Flash（编程旗舰）和 Gemini Omni（世界模型）；阿里 Qwen3.7-Max 以 Code Arena 1541 分坐稳编程模型 #2；OpenAI 通用模型与 Google AlphaProof Nexus 在同一周分别攻克 80 年 / 56 年 Erdős 难题，AI 数学推理出现双线突破；Anthropic Mythos 1 进入 Claude Code/Security 产品线，标志最强内部模型开始下沉到生产应用。效率革命侧，智谱 GLM-5.1-highspeed 以 400 tok/s 刷新全球 API 速度纪录、打破"高速即轻量"定律；面壁 MiniCPM5-1B 用 1B 参数超越所有 2B 以下模型；NVIDIA Nemotron-Diffusion 用三模统一架构把 8B 吞吐推到 Qwen3-8B 的 4 倍。同时 SaaS-Bench 揭示当前最强 Claude Opus 4.7 在真实跨应用任务上端到端通过率仅 3.8%，Stanford ABA 发现 25.7% benchmark 任务存在缺陷——**模型 benchmark 时代正进入"自审与重估"阶段**。周末 Anthropic 发布 Claude Opus 4.8，距前代仅 41 天，代码缺陷漏检率降低 4 倍，同步推出 Dynamic Workflows 并行 Agent 架构；阶跃星辰 Step-3.7-Flash 以 198B 稀疏 MoE 架构登陆 OpenRouter。**6 月初更新：** Qwen3.7-Plus 在 Terminal Bench 2.0 达 70.3 超越 Opus 4.6 Max，多模态 Agent benchmark 系统性领先；NVIDIA GTC Taipei 发布 Cosmos 3 物理AI世界模型，将视觉推理与动作生成闭环统一；MiniMax M3 正式发布，编程能力接近 Opus 4.7；JetBrains Mellum2 以 10B MoE 进入 IDE 原生编程赛道；自变量机器人 Wall-OSS-0.5 开源 VLA 在精密操作上以 39.6% 显著领先 π0.5 的 4.0%。

---

## 模型发布

### 1. Qwen3.7-Max（5/21）——全球第二大 AI 编程模型

**置信度：高** | 来源：[Facebook@alibabacloud](https://www.facebook.com/alibabacloud/posts/qwen37-max-is-officially-the-2-ai-coding-model-globallyin-the-latest-code-arena-/1434941022011319/) | [VentureBeat](https://venturebeat.com/technology/alibabas-proprietary-qwen3-7-max-can-run-for-35-hours-autonomously-and-supports-external-harnesses-like-anthropics-claude-code) | [OpenRouter](https://openrouter.ai/qwen/qwen3.7-max)

阿里通义千问发布 Qwen3.7-Max，在 Code Arena 盲测中得分 **1541**，正式成为全球第二大 AI 编程模型，仅次于 Claude。另有测试显示 Qwen3.7-Max 超越 GPT-5.5、Gemini-3.5-Flash、GLM-5.1 和 Kimi K2.6。

**核心参数：**

| 维度 | 数值 |
|------|------|
| Code Arena 得分 | **1541**（全球第二） |
| 上下文窗口 | **1M tokens** |
| API 定价 | $2.50 / $7.50 per 1M tokens |
| 可运行时长 | **35 小时**（支持长时间自主任务） |
| 工具调用 | **1000+ 次** |

**关键解读：**

- **不是"更聪明"而是"更自主"**：35 小时运行 + 1000+ 工具调用，专为生产级长时任务设计
- **隐式缓存上线（5/25）**：自动启用无需配置，开箱即用更便宜更快
- **Code Arena 的意义**：盲测排除了 prompt engineering 优势，结果更接近真实能力差距
- **定价信号**：$2.50/$7.50 是阿里旗舰模型历史最高价，说明能力溢价已获市场认可

---

### 2. 智谱 GLM-5.1 高速版（5/22）——刷新全球 API 速度纪录

**置信度：高** | 来源：[证券时报](https://www.stcn.com/article/detail/3921913.html) | [IT之家](https://www.ithome.com/0/953/717.htm) | [智谱文档](https://docs.bigmodel.cn/cn/guide/models/text/glm-5.1-highspeed)

智谱面向部分企业客户推出 GLM-5.1 高速版 API，输出速度达 **400 tokens/s**，刷新全球大模型 API 速度上限。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 输出速度 | **400 tokens/s**（全球最快 API） |
| 推理引擎 | **TileRT**（自研系统级推理优化） |
| 能力保留 | 旗舰级（非轻量裁剪版） |
| 适用场景 | AI 编程、实时语音、商业决策、3D 建模 |
| 可用性 | 企业客户灰度（5/22 启动） |

**关键解读：**

- **打破"高速即轻量"定律**：首次在国产大模型中实现旗舰级能力与低延迟的结合
- **TileRT 推理引擎**：通过系统级优化（推理引擎 + 调度系统 + 底层基础设施）重构 GPU 推理
- **国产首次**：智谱官方称这是国产大模型首次将旗舰级模型速度提升至这个量级

---

### 3. 面壁智能 MiniCPM5-1B（5/26）——端侧模型超越所有 2B 以下模型

**置信度：高** | 来源：[IT之家](https://www.ithome.com) | [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651035127&idx=1&sn=1699c9c08063a1f8faf96f5b49fa8c65) | [面壁智能](https://mp.weixin.qq.com/s/vLBxru7RYPp-V8cPpTMMCA)

面壁智能开源新一代端侧大模型 MiniCPM5-1B，仅 1B 参数在 AA-Index 榜单上得分 **17.9**，超越所有 2B 参数以下模型。基于自研 **ForgeTrain** AI 训练框架完成预训练。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 参数量 | **1B** |
| AA-Index 得分 | **17.9**（超越所有 2B 以下模型） |
| 训练框架 | **ForgeTrain**（AI 自动编写训练代码） |
| 训练加速 | 较 NVIDIA Megatron **+10%** |
| 训练硬件 | H100 GPU |
| INT4 量化后权重 | **0.5GB** |
| 运行平台 | 手机、浏览器 |

**关键解读：**

- **"高密度"能力再突破**：延续面壁"以小博大"传统，1B 模型在 AA-Index 上压制所有 2B 以下竞品
- **ForgeTrain 是更深的信号**：训练框架由 AI 自动编写训练代码，相对 Megatron 提速 10%——这意味着模型训练自动化进入实操阶段
- **开源全栈**：模型权重、训练数据集、部署方案全部开源

---

### 4. 谷歌 AlphaProof Nexus（5/26）——攻克悬置 56 年数学难题

**置信度：高** | 来源：[IT之家](https://www.ithome.com) | [@pushmeet](https://x.com/pushmeet/status/2058936037754224998) | [arXiv](https://arxiv.org/abs/2605.22763v1)

Google DeepMind 发布 AlphaProof Nexus 系统，结合大语言模型（Gemini）与 Lean 形式化验证工具构建形式化证明搜索 Agent。在 353 个开放 Erdős 问题中自主解决 9 个（含两个悬置 56 年的问题），在 492 个 OEIS 猜想中证明 44 个，还解决了代数几何领域开放 15 年的问题和最小最大优化领域开放 7 年的问题。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 架构 | Gemini + Lean 形式化验证 Agent |
| Erdős 问题解决 | **9 / 353**（含两道悬置 56 年问题） |
| OEIS 猜想证明 | **44 / 492** |
| 跨域突破 | 代数几何 15 年 + 最小最大优化 7 年开放问题 |
| 单题成本 | 最困难问题约几百美元 |
| 部署场景 | 组合数学、优化、图论、代数几何、量子光学 |

**关键解读：**

- **形式化验证是关键**：将每一步逻辑转化为可编译、可验证的代码，将模型从"令人信服的叙述者"转变为"候选方案生成器"
- **与 OpenAI Erdős 突破呼应**：同周 OpenAI 通用模型解决 1946 年单位距离问题——AI 数学推理出现双线突破
- **单题几百美元已具研究价值**：成本结构允许学者像调用工具一样调用 AI 证明 Agent

---

### 5. Google Gemini 3.5 Flash（5/19）——I/O 2026 旗舰发布，编程能力飙升

**置信度：高** | 来源：[Google I/O 2026](https://io.google) | [Google Blog](https://blog.google)

Google 在 I/O 2026 大会发布 Gemini 3.5 Flash，在编程和 Agent benchmark 上大幅超越前代 Gemini 3.1 Pro，速度提升 4 倍。

**核心参数：**

| 维度 | 数值 |
|------|------|
| Terminal-Bench | **76.2%**（超越 GPT-5.4 的 75.1%） |
| GDPval-AA Elo | **1656**（编程能力新标杆） |
| MCP Atlas | **83.6%**（Agent 工具使用） |
| 速度 | 较 Gemini 3.1 Pro **提升 4 倍** |
| 可用性 | GA 已上线 |

**关键解读：**

- **Google 终结 96 天沉寂**：Gemini 3.1 Pro 发布 96 天后，Google 终于在 I/O 大会放出新一代旗舰 Flash 模型
- **Flash 先行，Pro 在后**：Gemini 3.5 Flash 已 GA，更强的 Gemini 3.5 Pro 预计 6 月发布
- **编程能力质变**：Terminal-Bench 76.2% 和 GDPval-AA Elo 1656 均大幅超越前代，进入第一梯队

---

### 6. Google Gemini Omni（5/19）——世界模型：多模态视频生成与编辑

**置信度：高** | 来源：[Google I/O 2026](https://io.google) | [Google Blog](https://blog.google)

Google 在 I/O 2026 发布 Gemini Omni 世界模型，支持多模态视频生成与编辑，标志着 Google 正式进入物理世界模拟领域。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 定位 | 物理**世界模型**（理解/生成/编辑视频） |
| 能力 | 多模态视频生成、物理世界模拟、视频编辑 |
| 与 I/O 其他发布关系 | 与 Gemini 3.5 Flash（编程）+ AlphaProof Nexus（数学）同日发布 |

**关键解读：**

- **世界模型新赛道**：Gemini Omni 定位为理解物理世界、生成和编辑视频的基础模型，与 Mistral 收购 Emmi AI（数字孪生）形成竞争
- **Google I/O 三线齐发**：同一大会同时推出编程旗舰（3.5 Flash）、数学推理（AlphaProof Nexus）、物理世界模拟（Omni），展示模型层多维推进能力

---

### 7. 腾讯 Hy-MT2 开源翻译模型（5/21）——33 种语言互译，1.8B 登顶 HuggingFace

**置信度：高** | 来源：[Tencent Hunyuan@X](https://x.com/TencentHunyuan) | [arxiv](https://arxiv.org/html/2605.22064v1) | [Medium](https://medium.com/data-science-in-your-pocket/tencent-just-dropped-a-1-8b-translation-model-that-beats-commercial-apis-f1a1860a501c)

腾讯混元发布 Hy-MT2 多语言翻译模型系列，包含 1.8B / 7B / 30B-A3B 三个尺寸，支持 33 种语言互译。

**核心参数：**

| 维度 | 1.8B | 7B | 30B-A3B |
|------|------|-----|---------|
| HuggingFace 排名 | **#1** | 开源 SOTA | 开源 SOTA |
| vs 商业 API | 超越微软等主流 | - | - |
| 存储需求（1.25-bit 量化） | **440MB** | - | - |
| 推理速度提升 | 较前代 **+1.5 倍** | - | - |

**关键解读：**

- **开源阵营持续扩大**：继 DeepSeek V4（MIT）后，腾讯加入开源阵营
- **极量化技术**：腾讯 AngelSlim 1.25-bit 量化，仅需 440MB 即可在主流手机芯片本地运行
- **小程序发布**："腾讯混译"微信小程序支持语音输入和离线翻译

---

### 8. 面壁智能 BitCPM-CANN（5/25）——全球首个昇腾全栈训练 1.58-bit 开源大模型

**置信度：高** | 来源：[新浪财经](https://finance.sina.com.cn/roll/2026-05-25/doc-inhzawmm5162548.shtml) | [Rohan Paul@X](https://x.com/rohanpaul_ai)

面壁智能联合清华大学和 OpenBMB 社区发布 BitCPM-CANN，全球首个完全基于华为昇腾 910B NPU 训练的开源 1.58 比特三元大模型。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 训练平台 | 华为昇腾 910B NPU（全栈） |
| 比特数 | **1.58-bit**（仅 3 种权重状态） |
| 内存降低 | 相比 BF16 降低约 **6 倍** |
| 性能保持率 | 全精度模型 **95-97%** |
| 参数范围 | 0.5B - 8B |

**关键解读：**

- **国产算力全栈训练**：从量化算子到框架全部在昇腾上原生构建，非简单移植
- **极低比特量化**：三种权重状态的极低比特量化，内存占用降至原来的 1/6
- **边缘部署**：可高效部署于手机、电脑、车载设备等边缘端

---

### 9. Cursor Composer 2.5（5/19）——基于 Kimi K2.5 训练，长程 Agent 任务大幅提升

**置信度：高** | 来源：[Cursor Blog](https://cursor.com/cn/blog/composer-2-5) | [@cursor_ai](https://x.com/cursor_ai/status/2056415413077233983)

Cursor 发布 Composer 2.5，基于 Moonshot 的 Kimi K2.5 开源 checkpoint 训练，在长程 Agent 任务上的智能和行为均有显著提升。引入 targeted RL with textual feedback——在轨迹中错误位置直接插入文本提示作为教师信号，结合 on-policy 蒸馏 KL loss 进行局部行为修正。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 基础模型 | Kimi K2.5 开源 checkpoint |
| 合成任务数量 | Composer 2 的 **25 倍** |
| API 定价 | $0.50 / $2.50 per 1M tokens |
| 训练算力（与 SpaceXAI 合作） | Colossus 2 百万级 H100，**10倍 计算量** |

**关键解读：**

- **targeted textual feedback 是关键创新**：为长上下文 RL 的 credit assignment 提供了新解法
- **基于开源 checkpoint**：Cursor 直接基于 Moonshot Kimi K2.5 训练，开源模型在前沿应用中扮演基础设施角色
- **Cursor + SpaceXAI**：联合训练 10 倍算力的更大模型，Coding Agent 赛道加码

---

### 10. Cohere Command A+（5/21）——218B/25B 激活参数 MoE 模型，Apache 2.0 开源

**置信度：高** | 来源：[Cohere@X](https://x.com/cohere/status/2057120818551734589) | [HuggingFace](https://huggingface.co/CohereLabs/command-a-plus-05-2026-w4a4)

Cohere 发布 Command A+ 模型，采用 MoE 架构，**总参数 218B、激活参数 25B**，配备 128 个专家（每 token 激活 8 个 + 1 个共享专家），支持 128K 上下文长度，覆盖 48 种语言。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 总参数 / 激活参数 | **218B / 25B** |
| 专家数 | 128（每 token 激活 8 + 1 共享） |
| 上下文 | 128K |
| 语言支持 | 48 种 |
| 量化部署 | W4A4 量化后单张 B200 GPU 可部署 |
| 许可证 | **Apache 2.0** |

**关键解读：**

- **开源阵营再添重磅**：218B 参数 Apache 2.0，对 Meta Llama 系列和 Mistral 构成直接竞争压力
- **企业级开源新选择**：Cohere 此前主打闭源企业 API，转向 Apache 2.0 是策略转向信号

---

### 11. NVIDIA Nemotron-Labs-Diffusion（5/23）——AR/扩散/自推测三模统一，8B 吞吐 4× Qwen3

**置信度：高** | 来源：[HuggingFace Blog](https://huggingface.co/blog/nvidia/nemotron-labs-diffusion) | [NVIDIA Research](https://research.nvidia.com/publication/2026-05_nemotron-labs-diffusion-tri-mode-language-model-unifying-autoregressive)

Nemotron-Labs-Diffusion 在单一架构内统一三种解码模式：**AR**（传统串行）、**Diffusion**（32-token block 并行起草+多步精修）、**Self-Speculation**（扩散并行起草 + AR 因果验证，输出与纯 AR 完全相同）。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 模型尺寸 | 3B / 8B / 14B + 8B VLM |
| 训练数据 | 1.3T tokens 预训练 + 45B SFT |
| 8B 准确率 | 较 Qwen3-8B 高 **1.2%** |
| Diffusion 模式 TPF | AR 的 **2.6 倍** |
| Self-Speculation TPF | 6× 至 **6.4×** |
| SPEED-Bench GB200 吞吐 | **4× Qwen3-8B** |
| B200 实测速度 | 约 **865 tok/s** |

**关键解读：**

- **AR 与 Diffusion 不再是两个家族**：而是同一模型的不同模式，可灵活切换
- **Self-Speculation 新范式**：扩散起草 + AR 验证，无损质量但显著加速，可能成为推理加速主流
- **NVIDIA 模型实验室回归**：从硬件供应商扩展到模型创新主战场

---

### 12. 网易有道"子曰4"多模态模型全量开源（5/22）

**置信度：高** | 来源：[IT之家](https://www.ithome.com)

网易有道开源子曰大模型 4.0 的多模态模型（27B 参数）和语音合成模型，聚焦教育场景。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 多模态模型参数量 | **27B** |
| 专注场景 | 教育 |
| 纯文本中文数理准确率 | **81.4%** |
| 思维链压缩 | 输出长度压缩 **43.2%** |
| 语音合成 | 3 秒零样本克隆，**14 语种**，准确度超 **97%** |

**关键解读：**

- **教育垂直模型全栈开源**：27B 多模态 + 语音合成完整开源，教育场景的中文数理能力 81.4% 已具实用性
- **思维链压缩 43.2%**：在不损失准确率前提下大幅减少推理 token，是教育实时交互场景的关键优化

### 13. 美团 LongCat-Video-Avatar-1.5（5/21）——音频驱动数字人视频生成

**置信度：高** | 来源：[HuggingFace](https://huggingface.co)

美团 LongCat 团队发布音频驱动数字人视频生成框架，升级至 Whisper-Large 音频编码器。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 音频编码器 | Whisper-Large（升级） |
| 推理步数 | 仅需 **8 步**（DMD2 步蒸馏） |
| 能力 | 精准唇形同步、全身时序一致性、身份一致性 |

**关键解读：**

- **8 步推理是关键效率突破**：DMD2 步蒸馏让数字人视频生成进入接近实时区间
- **数字人方向竞争加剧**：与字节、阿里同类工作并行推进，模型质量从"可用"向"商用"过渡

---

### 14. xAI Grok V9-Medium（5/27）——1.5T 参数完成训练，2-3 周内公开发布

**置信度：高** | 来源：[@elonmusk](https://x.com/elonmusk/status/2058787384364265734)

Elon Musk 宣布 xAI 的 Grok 基础模型 **V9-Medium**（**1.5T 参数**）已完成训练，评测结果表现良好。训练中加入了大量 Cursor 编程数据进行补充训练。目前正在进行微调，强化学习将在几天内开始。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 参数量 | **1.5T** |
| 当前生产模型 | Grok V8-small **0.5T**（升级 3×） |
| 训练补充 | 大量 **Cursor 编程数据** |
| 微调状态 | RL 几天内开始 |
| 预计发布 | **2-3 周内**公开发布 |

**关键解读：**

- **从 0.5T 跃升至 1.5T**：参数量级 3× 跳跃，结合 Cursor 数据，xAI 在编程能力上明显加码
- **Grok 4.3 之后下一代主力**：当前 Grok 4.3 仅 26 天前发布，迭代节奏继续加速
- **Cursor 编程数据训练**：暗示 xAI 在 Coding Agent 赛道与 Anthropic Claude Code、阿里 Qwen3.7-Max 直接竞争

---

### 15. 快手 Keye-VL-2.0-30B-A3B（5/27）——首个 DSA 多模态，长视频理解开源 SOTA

**置信度：高** | 来源：[Hugging Face](https://huggingface.co/Kwai-Keye/Keye-VL-2.0-30B-A3B) | [量子位](https://mp.weixin.qq.com/s/gomgqFAZrdbJFQlOfSJxpQ)

快手发布 Keye-VL-2.0-30B-A3B，**首个将 DeepSeek Sparse Attention（DSA）成功落地多模态理解场景的模型**，支持 **256K 超长上下文**，长视频理解登顶开源 SOTA。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 参数量 / 激活参数 | 30B-A3B（MoE） |
| 上下文 | **256K** |
| 架构亮点 | **首个 DSA 多模态**（DeepSeek Sparse Attention） |
| VideoMME V2（输入 64→512 帧） | **35.3% → 42.4%**（不降反升） |
| LongVideoBench | **74.1**（超越 Qwen3-VL-235B-A22B） |
| LiveCodeBench v6 | **77.1** |
| SWE-bench Verified | **62.0** |

**关键解读：**

- **DSA 在多模态首次成功落地**：DeepSeek 的稀疏注意力架构跨域到视觉理解，证明架构通用性
- **以 30B 跨级超 200B+ 开源模型**：在 LongVideoBench 上压过 Qwen3-VL-235B-A22B，参数效率显著
- **长上下文不衰减**：512 帧准确率反而高于 64 帧，对长视频理解有重大实际价值
- **首次解锁 Agent 协作机制**：编程类 benchmark 大幅提升，多模态模型开始具备 Agent 能力

---

### 16. 昆仑万维 SkyClaw-v1.0（5/27）——Agent 原生模型，1M 上下文极低价

**置信度：高** | 来源：[新智元](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA==&mid=2652702909&idx=1&sn=242761d18907f204339ead4777ce72b4)

昆仑万维旗下 Skywork（天工 AI）发布 Agent 专用模型 **SkyClaw-v1.0** 及轻量版 **SkyClaw-v1.0-lite**，专为工具调用、多轮任务执行、代码生成等 Agent 场景优化。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 上下文窗口 | **1M tokens** |
| 训练范式 | 三阶段 Agent-native（mid-train + 合成任务 SFT + 端到端 RL） |
| OpenClaw Agent 任务 | 超 Minimax 2.7、DeepSeek V4 Flash，**接近 Claude Opus 4.6** |
| API 定价 | 输入 **¥0.5/M tokens**，输出 **¥4/M tokens** |
| 与 Claude Sonnet 4.6 价差 | **1/43 ~ 1/27** |
| 限免试用 | 发布后 **2-4 周** |

**关键解读：**

- **极低定价切入 Agent 市场**：输出端 ¥4/M tokens 约为 Claude Sonnet 4.6 的 1/27，直击成本敏感的 Agent 场景
- **Agent-native 训练**：三阶段管道明确为工具调用与多轮任务设计，非通用对话模型外延
- **评测范围有限**："接近 Opus 4.6" 仅在 OpenClaw 任务上成立，通用能力待验证

---

### 17. Anthropic Claude Opus 4.8（5/29）——距前代仅 41 天，代码缺陷漏检率降低 4 倍

**置信度：高** | 来源：[Anthropic Blog](https://www.anthropic.com/news/claude-opus-4-8) | [TechCrunch](https://techcrunch.com/2026/05/28/anthropic-releases-opus-4-8-with-new-dynamic-workflow-tool/)

Anthropic 发布新旗舰模型 Claude Opus 4.8，距 Opus 4.7 仅 **41 天**，远快于常规升级周期。相比前代代码缺陷漏检率降低 **4 倍**，新模型更倾向于主动标记输入输出中的问题。同步推出 **Dynamic Workflows** 功能，支持数十到上百个并行子 Agent 同时工作、交叉验证后汇报结果。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 距前代间隔 | **41 天**（Opus 4.6→4.7 为 70 天） |
| 代码缺陷漏检率 | 较 Opus 4.7 **降低 4 倍** |
| LAB 基准 | **首个突破 10%** 的模型 |
| Databricks token 成本 | 降低 **61%** |
| API 定价 | $5/$25（不变） |
| 新增功能 | effort control（low/extra/max/xhigh）+ 快速模式（**3 倍便宜**） |
| Dynamic Workflows | **数十到上百个并行子 Agent** 交叉验证 |

**关键解读：**

- **41 天迭代周期**：Anthropic 加速发版节奏，从模型能力、成本效率和 Agent 架构三线同步推进
- **主动标记而非被动回答**：Bridgewater 反馈最大改进是"其他模型通常遗漏的问题，Opus 4.8 会主动标记"
- **Dynamic Workflows**：并行子 Agent 验证模式直指企业级复杂任务场景（代码库级 bug 搜索、大规模迁移）
- **Bun 团队实战**：用 Opus 4.8 将 **75 万行 Zig 代码重写为 Rust，11 天完成，99.8% 测试通过**

---

### 18. 阶跃星辰 Step-3.7-Flash（5/30）——198B 稀疏 MoE 多模态模型登陆 OpenRouter

**置信度：高** | 来源：[@openrouter](https://x.com/OpenRouter/status/2060195234756370768) | [@vllm_project](https://x.com/vllm_project/status/2060155953715323288)

阶跃星辰（StepFun-ai）的多模态模型 Step-3.7-Flash 在 OpenRouter 上线，支持图像和视频处理。vLLM 在发布首日即宣布原生支持。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 总参数 | **198B**（稀疏 MoE） |
| 激活参数 | 约 **11B** / 每次前向传播 |
| 多模态 | 图像 + 视频 |
| 推理框架 | **vLLM 首日支持** |
| 分发平台 | OpenRouter |

**关键解读：**

- **中国多模态模型加速出海**：Step-3.7-Flash 快速登陆 OpenRouter 和 vLLM，反映中国模型厂商正加速抢占全球分发渠道
- **198B/11B MoE 架构**：与 Cohere Command A+（218B/25B）类似的"大模型小激活"范式，推理成本可控
- **vLLM 首日支持**：开源推理框架对中国模型的快速适配，反映生态认可度提升

---

### 19. MiniMax M3 开源发布（6/2）——编程能力接近 Opus 4.7，#MSA 新注意力架构

**置信度：高** | 来源：[@MiniMax_AI](https://x.com/MiniMax_AI/status/2061266317815296322) | [The Information](https://www.theinformation.com/briefings/chinas-minimax-launches-new-model-open-source-ai-coding-battle-heats)

MiniMax 正式发布 M3 大语言模型，编程能力接近 **Anthropic Opus 4.7** 水平。该模型特别适合编程和 AI Agent 的复杂多步任务，支持文本、图像和视频多模态输入。此前 5/28 预告标签为 **#MSA #OpenSource #M3**。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 编程能力 | 接近 **Opus 4.7** 水平 |
| 多模态支持 | 文本 + 图像 + 视频输入 |
| 核心场景 | 编程、AI Agent 复杂多步任务 |
| 架构标签 | **#MSA**（新型注意力机制） |
| 开源状态 | 已开源 |

**关键解读：**

- **开源编程赛道持续升温**：MiniMax M3 加入后与 CodeQwen、DeepSeek V4 等形成正面竞争
- **#MSA 架构**：可能指向 Multi-Head Sparse Attention 或类似 DeepSeek DSA 的新型稀疏注意力机制
- **M2.7→M3 迭代速度**：上一代 M2.7 于 4/12 发布，距 M3 仅 51 天

---

### 20. Microsoft MAI-Image-2.5（5/28）——Arena 文生图第 3 名，文本渲染大幅提升

**置信度：高** | 来源：[Microsoft AI](https://microsoft.ai/news/mai-image-2-5-launches-at-no-3-on-arena-ai/)

Microsoft AI 超智能团队发布 MAI-Image-2.5，在 Arena 文生图排行榜位列 **第 3 名**。相较于上一代，在文本渲染、风格化插画和商业图像方面显著提升。预计两周内接入 MAI Playground 和 Foundry。

**核心参数：**

| 维度 | 数值 |
|------|------|
| Arena 文生图排名 | **第 3 名** |
| 提升领域 | 文本渲染、风格化插画、商业图像 |
| 可视推理 | 覆盖物体、场景结构、光影、比例、空间关系 |
| 接入时间 | 两周内接入 MAI Playground / Foundry |

**关键解读：**

- **Microsoft 模型层多维布局**：同一周自研编码模型预告 + 文生图模型升级，从依赖 OpenAI 转向"自研+合作"双轨
- **文生图赛道竞争加剧**：与 Google Imagen 4、Midjourney V7 竞争，文本渲染和商业图像是差异化方向

---

### 21. 通义 Qwen3.7-Plus（6/2）——Terminal Bench 2.0 超 Opus 4.6 Max，多模态 Agent 全面领先

**置信度：高** | 来源：[Qwen Blog](https://qwen.ai/blog?id=qwen3.7-plus) | [@Alibaba_Qwen](https://x.com/Alibaba_Qwen/status/2061506644367069392)

通义千问发布 Qwen3.7-Plus，定位为视觉与语言统一的多模态智能体基座。纯文本编程方面，Terminal Bench 2.0 达 **70.3**（超 Opus 4.6 Max 65.4 和 DeepSeek-V4-Pro 67.9），SWE-Pro 57.6 与头部模型持平。多模态方面，ScreenSpot Pro 79.0、AndroidWorld 81.0、MathVision 90.3 显著超越 Opus 4.6 Max 和 Gemini 3.1 Pro。模型在单一智能体循环中融合 GUI 操作、CLI 工具调用和视觉推理。

**核心参数：**

| 维度 | 数值 |
|------|------|
| Terminal Bench 2.0 | **70.3**（超 Opus 4.6 Max 65.4、DeepSeek-V4-Pro 67.9） |
| SWE-Pro | **57.6** |
| ScreenSpot Pro | **79.0** |
| AndroidWorld | **81.0** |
| MathVision | **90.3** |
| API | 阿里云百炼已上线 |
| 部署框架 | 支持 Claude Code / OpenClaw / Qwen Code |

**关键解读：**

- **编程 Agent 新标杆**：Terminal Bench 2.0 上首次超越 Anthropic 和 DeepSeek 头部模型
- **多模态 Agent 系统性突破**：GUI 操作 + 视觉推理 + CLI 工具调用的统一循环，是 Agent-native 模型的典型范式
- **Qwen3.7 系列双旗舰**：Max 专注 Code Arena 盲测，Plus 专注多模态 Agent 实操，覆盖互补

---

### 22. NVIDIA Cosmos 3（6/2）——物理AI开放世界基础模型，GTC Taipei 发布

**置信度：高** | 来源：[NVIDIA Blog](https://blogs.nvidia.com/blog/cosmos-3-physical-ai-open-world-foundation-model/)

NVIDIA 在 GTC Taipei 发布 Cosmos 3 世界基础模型，采用 **Mixture-of-Transformers** 架构，将视觉推理和多模态生成（文本、视频、图像、环境音、动作）统一于单一模型。架构分为推理块（解析场景）和生成块（基于上下文生成物理仿真输出），支持原生动作生成（关节角度、夹爪位置、轨迹点）。Agile Robots、NVIDIA GEAR 团队已在用 Cosmos 3 生成动作条件化机器人数据。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 架构 | **Mixture-of-Transformers** |
| 模态 | 文本 + 视频 + 图像 + 环境音 + 动作 |
| 核心能力 | 推理块解析场景 → 生成块输出物理仿真 |
| 原生动作生成 | 关节角度、夹爪位置、轨迹点等数值数据 |
| Nano 后训练 | RoboLab / RoboArena 领先 |

**关键解读：**

- **"看懂→预测→生成动作"闭环**：将感知与控制端到端统一到单一模型，是物理AI的关键一步
- **世界模型赛道新玩家**：与 Gemini Omni（Google）、Gemini Robotics 形成三足鼎立
- **开源 VLA 生态加速**：Cosmos 3 为开源 VLA 训练提供世界模型基座

---

### 23. JetBrains Mellum2（6/2）——10B 稀疏 MoE 编程模型，IDE 原生集成

**置信度：高** | 来源：[HuggingFace Blog](https://huggingface.co/blog/JetBrains/mellum2-launch)

JetBrains 发布 Mellum2，**120 亿参数稀疏混合专家模型**，专为代码场景优化。采用稀疏激活机制降低推理成本，支持长上下文处理，已集成至 JetBrains IDE 生态。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 总参数 | **12B**（稀疏 MoE） |
| 架构 | 稀疏激活混合专家 |
| 核心场景 | 代码补全、IDE 辅助编程 |
| 集成 | JetBrains IDE 全产品线 |

**关键解读：**

- **IDE 原生模型路线**：JetBrains 继续走"模型即 IDE 功能"路线，与 Cursor（Agent 嵌入）、GitHub Copilot（API 调用）形成差异化
- **MoE 降低推理成本**：稀疏激活让 12B 模型在本地/IDE 侧可接受范围内运行

---

### 24. 自变量机器人 Wall-OSS-0.5（5/29）——开源 VLA，精密操作领先 π0.5 近 10 倍

**置信度：高** | 来源：自变量机器人官方发布 | HuggingFace 开源仓库

自变量机器人开源发布 Wall-OSS-0.5 VLA 模型。在 RoboCaca 精密插入任务上达 **39.6%**，显著领先闭源 π0.5 的 **4.0%**。这是首个在精密操作任务上大幅超越闭源模型的开源 VLA。

**核心参数：**

| 维度 | 数值 |
|------|------|
| RoboCaca 精密插入 | **39.6%**（π0.5 仅 4.0%） |
| 开源状态 | **已开源**（HuggingFace） |
| 定位 | VLA（Vision-Language-Action）通用机器人模型 |
| 核心优势 | 精密操作任务 |

**关键解读：**

- **开源 VLA 首次在精密操作上大幅领先闭源**：39.6% vs 4.0%，差距近 10 倍
- **降低 VLA 赛道入场门槛**：开源模型让研究机构和中小团队可以参与物理AI研发
- **与 π0.5、Gemini Robotics 形成开源 vs 闭源对照**：开源 VLA 生态开始形成

---

## 模型能力评估与部署预告

> 本节聚焦模型本身的能力评估、benchmark 审计、部署落地预告，不包含融资、人事、算力等非模型信号。

### 1. OpenAI GPT-5.6 曝下月发布：150 万 token 上下文（泄露）

**置信度：中** | 来源：[IT之家](https://www.ithome.com) | [Instagram@GoogleAI](https://www.instagram.com/p/DYiFypSii9e/)

开发者在 OpenAI Codex 后端日志中发现未官宣的 **GPT-5.6** 模型（内部代号 iris-alpha）。

**泄露信息：**

| 维度 | GPT-5.6 | GPT-5.5 |
|------|---------|---------|
| 上下文窗口 | **150 万 tokens** | 105 万 |
| 提升幅度 | +43% | - |
| 测试状态 | 输入 90 万 token 时仍流畅响应 | - |

**关键解读：**

- **上下文窗口军备竞赛**：150 万 token 意味着单次对话可处理整本书籍级别的上下文
- **6 月发布窗口**：Anthropic、Google Gemini 和 xAI Grok 也可能瞄准同期发布
- **注意**：这是泄露信息，OpenAI 尚未官宣

---

### 2. OpenAI 通用模型解决 Erdős 平面单位距离问题——80 年开放数学难题首获突破

**置信度：高** | 来源：[@OpenAI](https://x.com/OpenAI/status/2057176201782075690) | [@sama](https://x.com/sama/status/2057203171198636251)

OpenAI 宣布其通用推理模型解决了 **平面单位距离问题（planar unit distance problem）**，该问题由数学家 Paul Erdős 于 **1946 年**提出，是组合几何领域的经典开放问题。近 80 年来数学界普遍认为最优解大致为方形网格结构，OpenAI 模型发现了**全新的构造族**，性能优于方形网格，从而推翻了这一假设。

**关键信号：**

- **首次由 AI 自主解决数学领域核心开放问题**（OpenAI 自评）
- 菲尔兹奖得主 Timothy Gowers 转发提醒数学同行"坐稳了再看"
- Sam Altman 表示这是重要里程碑
- 与 Google AlphaProof Nexus（5/26 解决 9 个 Erdős 问题）形成数学推理双线突破

---

### 3. SaaS-Bench 揭示 Computer-Use Agent 真实差距：Claude Opus 4.7 端到端通过率仅 3.8%

**置信度：高** | 来源：[UniPat AI](https://unipat.ai)

UniPat AI 发布 SaaS-Bench，在 23 个真实 SaaS 系统、106 个跨应用长程任务上测试 Computer-Use Agent 能力，结果远低于 benchmark 成绩预期。

**关键数字：**

| 模型 | 检查点得分 | 端到端通过率 |
|------|-----------|-------------|
| **Claude Opus 4.7** | 43.9% | **3.8%**（106 任务仅完整通过 4 个） |
| Kimi K2.5 / Gemini 3.1 Pro | - | **零** |

**关键解读：**

- **Agent 能力远低于 Benchmark 成绩**：核心瓶颈是对持久状态的有效推理和闭环验证机制的缺失
- **四种结构性失败**：任务越长通过率越低、一步错误链式失败、执行后不验证、运行间分数差异巨大
- **面向人类的 SaaS 界面可能需要为 Agent 重新设计**

---

### 4. Anthropic Mythos 1 即将引入 Claude Code 与 Claude Security

**置信度：高** | 来源：[TestingCatalog](https://www.testingcatalog.com/anthropic-prepares-mythos-1-for-claude-code-and-claude-security/)

Anthropic 正将 Mythos 1 引入 Claude Code 和 Claude Security 产品线，模型标签为 **claude-mythos-1-preview**。

**关键信息：**

- **Project Glasswing** 已发现 **10,000+ 个**高/危级别漏洞
- Sonnet 4.8 预计 **6 月中下旬**发布，视觉准确率提升至 **>98%**，新增"X high"推理层级
- token 输出量增加约 30%

**关键解读：**

- **Mythos 系列定位更高安全要求的 Agent 场景**：与 OpenAI Operator 形成直接竞争
- **从单一产品线向多产品矩阵扩展**

---

### 5. Stanford Auto Benchmark Audit（5/27）——25.7% AI 评测任务存在缺陷

**置信度：高** | 来源：[arXiv](https://arxiv.org/abs/2605.26079)

Stanford 团队（Junlin Wang、James Zou 等）提出 Auto Benchmark Audit（ABA）框架，系统审计 AI benchmark 任务质量。对 **168 个** benchmark、九个领域的审查发现，超过 **25.7%** 的评测任务存在歧义设计、环境冲突或错误基准答案等问题。

**核心参数：**

| 维度 | 数值 |
|------|------|
| 审查 benchmark 数 | **168 个**（覆盖 9 个领域） |
| 缺陷任务占比 | **25.7%** |
| SWE-bench Verified 移除问题任务后 | 平均性能 **+9.9%** |
| Terminal-Bench 2 移除问题任务后 | 平均性能 **+9.6%** |
| 排名变化 | 移除问题任务后模型排名发生改变 |

**关键解读：**

- **Benchmark 时代进入"自审"阶段**：四分之一任务存在缺陷意味着部分模型排名失真
- **9.9% / 9.6% 的差异足以改变排名**：模型 A vs B 的微弱优势可能完全来自有问题的题目
- **自动化审计将成为新基础设施**：benchmark 提供方需要内置 ABA 类工具来背书评测可信度

---

### 6. Qwen CUA-Gym（5/27）——计算机使用 Agent 训练数据规模化生成

**置信度：高** | 来源：[arXiv](https://arxiv.org/abs/2605.25624)

Qwen 团队（Bowen Wang、Tao Yu 等）提出 CUA-Gym 框架，通过 Generator-Discriminator 双 Agent 协作自动生成计算机使用 Agent（CUA）的训练数据。

**核心参数：**

| 维度 | 数值 |
|------|------|
| RLVR 训练数据 | **32,112 条**经验证 |
| 覆盖环境数 | **110 个** |
| A3B 模型 OSWorld-Verified | **62.1%** |
| A17B 模型 OSWorld-Verified | **72.6%**（超越同规模开源 CUA） |
| 跨环境泛化 | WebArena 上保持泛化能力 |

**关键解读：**

- **CUA 训练数据稀缺瓶颈被打破**：Generator-Discriminator 自动管道，可规模化扩展环境覆盖
- **与 SaaS-Bench 形成呼应**：SaaS-Bench 暴露端到端 3.8% 问题，CUA-Gym 给出训练侧解决思路
- **Agent 训练数据生产新范式**：从人工标注转向自动生成 + 自动验证，跟 ForgeTrain 思路一致

---

### 7. EAGLE 3.1 推测解码（5/28）——长上下文接受长度提升 2 倍

**置信度：高** | 来源：[vLLM Blog](https://vllm.ai/blog/2026-05-26-eagle-3-1) | [@vllm_project](https://x.com/vllm_project/status/2059420705834619104)

EAGLE 团队、vLLM 团队和 TorchSpec 团队联合发布 EAGLE 3.1 推测解码方案，解决"注意力漂移"问题。引入 FC normalization 和 post-norm hidden-state feedback，在长上下文场景中将接受长度较 EAGLE 3 提升 **2 倍**。基于 Kimi K2.6 的 benchmark 显示，并发 1 时每用户输出吞吐量提升 **2.03 倍**，并发 16 时仍有 **1.66 倍**加速。已合并至 vLLM main 分支。

**关键解读：**

- **推测解码走向生产级部署**：EAGLE 3.1 对注意力漂移的修复解决了长上下文部署中的核心痛点
- **2× 接受长度**对推理成本优化意义重大，与 GLM-5.1-highspeed 400 tok/s 形成推理效率双线推进

---

### 8. 苹果据称正使用定制版 1.2T 参数 Google 模型重塑下一代 Siri

**置信度：高** | 来源：[Kim@X](https://x.com/kimmonismus)

据报道，苹果为改造下一代 Siri，正使用定制版、参数规模达 **1.2T** 的 Google 大模型（显著大于预估约 300B 的 Gemini 3.5 Flash）。

**关键信息：**

- 简单查询预期在本地设备运行
- 下月重要发布：WWDC 上的 Apple Intelligence 与 Gemini 整合
- 同期可能发布：GPT-5.6、可能的 Sonnet 4.8/Opus 4.8、已确认的 Gemini 3.5 Pro

**关键解读：**

- **1.2T 参数的意义**：远超 Gemini 3.5 Flash 的 300B，说明顶级助手场景对模型能力要求持续提升
- **Google 顶级模型首次端侧+云协同部署**：6 月 WWDC 将是该产品形态的首次公开展示

---

## 其他趋势洞察

### 新范式：从"单模型 Scaling"到"多模型编排"

本周多条证据线显示，在 Agent 场景下，harness engineering（系统层 L3）的边际收益正在放大：

- Sakana Fugu 7B 编排器在 GPQA Diamond 上达到 95.1%，超越池中所有单个前沿模型
- AHE 论文通过自进化 harness 把 Terminal-Bench 从 69.7% 提到 77.0%（+7.3pp）
- Mason Drxy 仅通过 prompt 调优把 gpt-5.2-codex Terminal-Bench 从 52.8% 提到 66.5%（+13.7pp）

**信号：在 Agent 场景，训练更好的调度器可能比训练更强的模型更具性价比。**

### Benchmark 饱和与新前沿

| Benchmark | 状态 | 领先者 | 分数 | 含义 |
|-----------|------|--------|------|------|
| GPQA | **已饱和** | Claude Mythos | 94.6% | 前 4 差 <0.5% |
| AIME | **已饱和** | GPT-5.2/Gemini | 100% | 完全失去区分度 |
| ARC-AGI-3 | **新战场** | GPT-5.5 | 0.43% | 人类 100%，233x 差距 |
| τ-voice | **新战场** | Grok Voice | 67.3% | 语音 Agent 首个标准 benchmark |
| Code Arena | **新战场** | Qwen3.7-Max | **1541** | 盲测编程能力新基准 |

---

## 趋势深读

> 把散落在不同模型卡片里的信号串成主线，标注成熟度和待跟踪问题。本节是周报从"事实层"到"判断层"的桥梁。

### 趋势 A — Agent-native：从"通用 LLM + harness"到"专为 Agent 训练的模型"

**这是早就出现、本期变得明牌的趋势。** 历史脉络：

| 阶段 | 时间 | 范式 | 代表 |
|------|------|------|------|
| L0 补全 | 2021-2022 | 单文件代码补全 | Codex、Copilot v1 |
| L1 Chat | 2023 | 通用 LLM + Chat | GPT-4、Claude 2 |
| L2 IDE Agent | 2024 上半年 | 通用模型 + IDE harness | Cursor、Cline |
| L3 长程 Agent | 2024 下半年 | 通用模型 + 强化工具链 | Devin、Claude Code、Aider |
| **L4 Agent-native** | **2025-2026** | **专为 Agent 训练的模型** | **Composer 2.5、SkyClaw、Opus 4.8** |

**本期的关键观察：L4 训练管道在两周内被三家独立验证。**

| 厂商 | 训练管道 | 关键创新 |
|------|---------|---------|
| Cursor Composer 2.5 | 25× 合成任务 + targeted RL with textual feedback + on-policy 蒸馏 | 在错误轨迹位置直接插入文本提示作为教师信号 |
| 昆仑万维 SkyClaw-v1.0 | 三阶段：mid-train + 合成任务 SFT + 端到端 RL | Agent-native 全栈管道 |
| Anthropic Opus 4.8 | Dynamic Workflows（数十到上百并行子 Agent 交叉验证） | 推理时 Agent 化，主动标记错误 |

**学术对照（验证不是孤立现象）：**

- **HINT-SD**（2026）：targeted hindsight self-distillation，在 BFCL v3/AppWorld 上 +18.8%、训练步时 2.26× 加速——证实"选择性反馈"是当前学术活跃方向
- **LOOP**（2025）：32B 模型在 AppWorld 上超 OpenAI o1 9pp，证实小模型 + 环境内 RL 可击败大通用模型
- **LiteCoder-Terminal-RL**（2026）：仅用 602 个可验证环境的 DMPO 训练，32B 模型在 Terminal Bench 1.0/2.0/Pro 上达 29.06%/18.54%/34.00%

**深层判断：targeted textual feedback 解决了长程 RL 最难的 credit assignment 问题**——传统 reward shaping 难以归因 50 步前的错误，textual feedback 等于"用语言代替奖励信号、直接打在错误那一步"。如果该方法被广泛验证，未来 6 个月所有 Agent-native 模型的训练管道会向这个方向收敛。

**编程是最佳战场，但不是最终战场**：编程之所以成为所有头部 lab 的收敛维度，原因是 reward 易获得（测试通过=客观信号）、轨迹结构化、数据丰富。但 SaaS-Bench 端到端 3.8% 通过率证明：**当 reward 模糊、状态持久、跨应用时，当前 Agent-native 模型仍崩溃**。下一个 6 个月真正的挑战是把训练管道从编程迁移到 SaaS / CUA / 研究等无明确 reward 的场景。

**待跟踪：**
1. Cursor Composer 2.5 完整论文是否公开（仅 blog 还是有技术报告）
2. textual feedback 是否能扩展到非编程场景（Qwen CUA-Gym 已有早期信号）
3. Microsoft Build 自研编码模型的训练管道是否相似
4. Grok V9-Medium 加 Cursor 数据训练后的真实 benchmark

---

### 趋势 B — 推理效率 6 路径：从单点优化到组合叠加

本期周报里 6 条独立技术路径同时成熟，且大部分**正交可叠加**：

| 路径 | 优化点 | 量级 | 互斥性 |
|------|--------|------|--------|
| 1. 系统级推理引擎 | CPU/GPU 调度 + 内存布局 | GLM-5.1 **400 tok/s** | 与所有路径正交 |
| 2. 推测解码 | 草稿 + 验证 | EAGLE 3.1 接受长度 **2×** | 与量化、蒸馏正交 |
| 3. AR/Diffusion 架构统一 | 解码模式切换 | Nemotron Self-Spec **6.4× TPF** | 路径 2 的超集 |
| 4. 极低比特量化 | weight 精度 | BitCPM 1.58-bit、内存 **6×** | 与所有路径正交 |
| 5. 步蒸馏 | diffusion 步数 | LongCat DMD2 **8 步** | 仅适用扩散类 |
| 6. 训练-推理同步 | 异步 RL 工程 | HF Delta Sync **130×** 减传输 | 训练时优化 |

**理论上限测算**：路径 1+2+4 完全正交，TileRT 引擎 + EAGLE 3.1 + 1.58-bit 量化叠加，理论值 400 × 2 × 6 = **4800 tok/s**；考虑实际交互损失取 60-70%，**约 2900-3400 tok/s** 是工程上限。

**实际生产瓶颈**：EAGLE 3.1 在并发 1 时 2.03× vs 并发 16 时 1.66×，**批量推理时收益递减**——这意味着推理效率突破对**低延迟单用户场景**（如 IDE、语音 Agent）杠杆最大，对批量 API 场景杠杆较小。

**判断：未来 6 个月推理成本下降的主要来源不再是"模型变小"，而是"6 条路径组合"。** 含义：
- GPU 厂商护城河被削弱：系统级优化收益可能超过硬件升级
- vLLM/SGLang 战略地位上升：路径 1/2/3/6 都需要它们
- 小厂仍能追：路径 4/5 可在开源模型上实现

**待跟踪：**
1. 是否有真实模型同时使用 ≥3 条路径（Step-3.7-Flash 可能用了 1+2）
2. Nemotron Self-Speculation 在生产负载下的实际表现
3. 1.58-bit 量化在 100B+ 模型上是否仍保持 95-97% 性能

---

### 趋势 C — 物理世界模型 × VLA：被低估的下半年爆发点

本期被低估的赛道。三条独立技术路线同步推进：

| 路线 | 代表 | 当前状态 | 商业化距离 |
|------|------|---------|-----------|
| **路线 1**：World Model（生成式视频理解 + 模拟） | Gemini Omni（5/19）、**NVIDIA Cosmos 3**（6/2） | Cosmos 3 将推理+生成+动作统一于单一模型，支持原生动作生成 | 中（Cosmos 3 已被机器人团队采用） |
| **路线 2**：VLA（机器人专用） | Wall-OSS-0.5（5/29，开源）、π0/π0.5、Gemini Robotics | 开源 VLA 在 RoboCaca 精密插入达 39.6% vs π0.5 的 4.0%——**开源已显著领先闭源** | 近（工业落地最快） |
| **路线 3**：端云协同消费助手 | 苹果定制 1.2T Google 模型（WWDC 6 月）、子曰4 27B 端侧 | 即将公开形态 | 中（消费级最大单一市场） |

**学术对照**：
- **π0**（2024）：Internet-scale VLM + flow matching + 多机器人形态预训练，奠定 VLA 范式
- **villa-X**（2025）：Vision-Language-Latent-Action，未见 embodiment 上的零样本生成
- **GeoAware-VLA**（2025）：几何先验加入 VLA，未知视角成功率 +35pp（LIBERO）
- **VLAPS**（2025）：VLA + MCTS，特定任务成功率 +67pp

**深层判断：三条路线在 2026 下半年可能开始合流**——理想的端云助手需要 World Model 的物理理解 + VLA 的动作能力 + 大模型的语言理解。Wall-OSS-0.5 的开源比 Mistral / Sora 这类闭源更值得关注，因为它降低了整个赛道的入场门槛。

**待跟踪：**
1. WWDC 苹果 Siri 实际形态（端云比例、模型架构）
2. Gemini Omni 是否能预测物理交互结果（"球放斜坡上会怎样"）
3. Wall-OSS-0.5 vs π0.5 vs Gemini Robotics 的全面对比
4. VLA scaling law（参数量、机器人形态数、轨迹数的最优配比）

---

### 趋势 D — Benchmark 信任危机的 5 个维度

周报已有信号但深度不够。Benchmark 失信不是单一问题，是 **5 个独立维度**同时崩塌：

| 维度 | 表现 | 本期证据 | 影响 |
|------|------|---------|------|
| 1. **任务质量缺陷** | 25.7% 任务有歧义/错误 | Stanford ABA | 移除后 SWE-Verified +9.9%、Terminal-Bench 2 +9.6%——**模型排名重排** |
| 2. **benchmark vs 真实差距** | 检查点 43.9% → 端到端 3.8% | SaaS-Bench Opus 4.7 | 当前 Agent benchmark 高估真实能力 **10-20×** |
| 3. **饱和** | AIME 100%、GPQA 94.6% 前 4 差 <0.5% | 多模型刷顶 | 失去区分度，迫使新 benchmark 涌现 |
| 4. **训练数据泄露** | 闭源模型可能见过题 | LiveCodeBench v6 缓解但未根治 | 闭源模型的优异表现部分不可信 |
| 5. **评测方法本身** | 只能 nudge 测出欺骗能力 | Neel Nanda + DeepMind Gram | 安全 benchmark 系统性低估真实风险 |

**关键判断：Benchmark 报错率（25.7%）已接近模型性能差距（5-10pp）**——意味着**当前所有"模型 X 比 Y 强 5%"的论断都需要重新审视**。

**接下来 6-12 个月会出现的新事物**：
- **Benchmark v2 运动**：所有主流 benchmark 发布"经过 ABA 审计"版本
- **真实环境评估生态**：SaaS-Bench、OSWorld、WebArena 类工具成为新基础设施
- **第三方评测机构地位上升**：Artificial Analysis、Scale AI 等
- **学术-工业评估分化**：发论文用一套，工业部署用另一套

**待跟踪：**
1. Stanford ABA 论文（arXiv:2605.26079）的缺陷分布——是否所有领域都受影响
2. OSWorld、SaaS-Bench、GDPval-AA 的采纳率
3. 是否有厂商主动发布"自审过的内部 benchmark"

---

### 趋势 E — 自进化工具链：四层级成熟度

> "自进化"是本期信号最密集但散落在多处的主题。把它系统化呈现。

**四层级成熟度模型**：

| 层级 | 含义 | 本期证据 | 成熟度 |
|------|------|---------|--------|
| **L1 工程自动化** | AI 写训练代码 / 生成训练数据 | ForgeTrain（5/26）、CUA-Gym（5/27）、Composer 2.5（5/19）、HF Delta Weight Sync（5/28） | **生产级（已落地）** |
| **L2 评测自审** | AI 审计 benchmark / 发现自身错误 | Stanford ABA（5/27）、MemTrace（5/29）、DeepMind Gram（5/30） | **早期工程化** |
| **L3 自我修正** | 推理时主动标记错误 / 从错误学习 | Opus 4.8 主动标记（5/29）、DenoiseRL（5/29）、BES（5/30） | **能力初现** |
| **L4 闭环自进化** | 不需人类的完全自主迭代 | 无 | **未实现** |

**深层判断：本期展示 L1 和 L2 的成熟、L3 的能力初现，L4 没有任何证据。**

CSET Helen Toner 的反驳是对的——目前所有"自进化"都是**让 AI 加速人类研究员的某些环节**，而非真正的递归自我改进（RSI）。但这种加速本身有杠杆效应：当 ForgeTrain + CUA-Gym + DenoiseRL + ABA 四件套同时成熟，**L1/L2 实际已形成"AI-in-the-loop"训练循环**——人类只需定义目标和审核结果，中间环节 AI 化。

**METR Ajeya Cotra 三阶段框架**（5/29 TechCrunch）：
- **Adequacy**（无人也能产出研究）：预计 1-2 年内
- **Parity**（AI 等同人类研究员）：未给时间表
- **Supremacy**（AI 超越人机协作）：达到 parity 后 1 年内可能到来

**真正值得追踪的指标**不是单点能力，而是**L1+L2+L3 工具链何时形成闭环**：训练→数据→评测→推理是否能在没有人类介入下完成一次完整迭代。

**待跟踪：**
1. ForgeTrain 是端到端自动还是 in-the-loop
2. CUA-Gym Discriminator 是否需要人工标注 oracle
3. DenoiseRL 错误标签如何获得
4. Sangyun Lee "Language Models Need Sleep"（CMU 5/28）后续——这是少数真正涉及"模型自我修改权重"的工作
5. Karpathy Auto-Research、Recursive Superintelligence 这些 RSI 项目的工程进展

---

## 厂商演进视图

### OpenAI

| 模型 | 发布日期 | 间隔 | SWE-Pro | Terminal-Bench | GPQA | 定价 $/M | 备注 |
|------|----------|------|---------|---------------|------|---------|------|
| GPT-5.4 | 2026-03-05 | - | 57.7% | 75.1% | 92.8% | $2.5/$15 | 1M ctx |
| GPT-5.4 Pro | 2026-03-05 | 0天 | - | - | 94.4% | $30/$180 | |
| **GPT-5.5** | **2026-04-23** | **48天** | **58.6%** | **82.7%** | **93.6%** | **$5/$30** | **Spud** |
| **GPT-5.5 Pro** | **2026-04-23** | **0天** | - | - | - | **$30/$180** | **FrontierMath T4 39.6%** |
| *GPT-5.6* | 预期 6 月 | - | - | - | - | - | 泄露：150 万 token |

### Anthropic

| 模型 | 发布日期 | 间隔 | SWE-Pro | Terminal-Bench | GPQA | 定价 $/M | 备注 |
|------|----------|------|---------|---------------|------|---------|------|
| Claude Opus 4.6 | 2026-02-05 | - | 53.4% | 65.4% | 91.3% | $5/$25 | |
| Claude Sonnet 4.6 | 2026-02-17 | 12天 | - | 59.1% | 89.9% | $3/$15 | 性价比款 |
| Claude Opus 4.7 | 2026-04-16 | 2月 | **64.3%** | 69.4% | 94.2% | $5/$25 | 自验证 |
| Claude Mythos | 受限 | - | 77.8% | 82.0% | 94.6% | - | 不公开发布 |
| *Opus 4.8* | 预期 | - | - | - | - | - | WWDC? |

### xAI

| 模型 | 发布日期 | 间隔 | GPQA | GDPval-AA | 定价 $/M | 备注 |
|------|----------|------|------|-----------|---------|------|
| Grok 4.20 | 2026-02-17 | - | - | 1179 | $2/$6 | |
| **Grok 4.3** | **2026-04-30** | **2月** | **88.0%** | **ELO 1500** | **$1.25/$2.50** | **207 tok/s** |
| **Grok Build** | **2026-05-14** | - | - | - | - | **Beta 开放 SuperGrok** |
| *Grok 5* | 预期 | - | - | - | - | Musk 预告 |

### DeepSeek

| 模型 | 发布日期 | 间隔 | SWE-Verified | LiveCodeBench | 定价 $/M | 许可证 |
|------|----------|------|-------------|---------------|---------|--------|
| V3.2 | 2025-09 | - | - | - | $0.28/$0.42 | MIT |
| **V4-Pro** | **2026-04-27** | **~4月** | **80.6%** | **93.5** | **$1.74/$3.48** | **MIT** |
| **V4-Flash** | **2026-04-27** | **0天** | 79.0% | 91.6 | **$0.14/$0.28** | **MIT** |

### 其他厂商

| 厂商 | 最近模型 | 发布日期 | 状态 | 距今天数 |
|------|---------|---------|------|---------|
| **xAI** | **Grok V9-Medium 1.5T**（已训练完成） | **2026-05-27** | **训练完成** | **6天** |
| **快手** | **Keye-VL-2.0-30B-A3B**（首个 DSA 多模态） | **2026-05-27** | **新发布** | **6天** |
| **昆仑万维** | **SkyClaw-v1.0**（Agent-native, 1M ctx） | **2026-05-27** | **新发布** | **6天** |
| **面壁智能** | **MiniCPM5-1B**（端侧 1B AA-Index 17.9） | **2026-05-26** | **新发布** | **7天** |
| **面壁/华为** | **BitCPM-CANN**（昇腾 1.58-bit 全栈） | **2026-05-25** | **新发布** | **8天** |
| **NVIDIA** | **Cosmos 3**（物理AI世界基础模型） | **2026-06-02** | **新发布** | **0天** |
| **JetBrains** | **Mellum2**（12B MoE IDE 原生编程） | **2026-06-02** | **新发布** | **0天** |
| **Alibaba** | **Qwen3.7-Plus**（TerminalBench2.0 70.3） | **2026-06-02** | **新发布** | **0天** |
| **MiniMax** | **M3**（编程接近 Opus 4.7） | **2026-06-02** | **新发布** | **0天** |
| **自变量机器人** | **Wall-OSS-0.5**（开源 VLA，精密操作 39.6%） | **2026-05-29** | **新发布** | **4天** |
| **NVIDIA** | **Nemotron-Labs-Diffusion**（4× Qwen3-8B） | **2026-05-23** | **新发布** | **10天** |
| **智谱** | **GLM-5.1-highspeed**（400 tok/s） | **2026-05-22** | **新发布** | **11天** |
| **网易有道** | **子曰4 多模态 + 语音**（27B 教育全栈开源） | **2026-05-22** | **新发布** | **5天** |
| **腾讯** | **Hy-MT2 翻译模型**（HF #1，1.25-bit/440MB） | **2026-05-21** | **新发布** | **6天** |
| **Cohere** | **Command A+**（218B Apache 2.0） | **2026-05-21** | **新发布** | **6天** |
| **Alibaba** | **Qwen3.7-Max**（Code Arena #2） | **2026-05-21** | **新发布** | **6天** |
| **美团** | **LongCat-Video-Avatar-1.5**（8 步推理） | **2026-05-21** | **新发布** | **6天** |
| **Cursor** | **Composer 2.5**（基于 Kimi K2.5） | **2026-05-19** | **新发布** | **8天** |
| **Google DeepMind** | **Gemini 3.5 Flash / Gemini Omni / AlphaProof Nexus** | **2026-05-19** | **三线齐发** | **8天** |
| Grok 4.3（xAI 上一代主力） | - | 2026-04-30 | 活跃 | 27天 |
| DeepSeek | V4-Pro/Flash | 2026-04-27 | 活跃 | 30天 |
| Moonshot AI | Kimi K2.6 | 2026-04-20 | 活跃 | 37天 |
| **Anthropic** | **Claude Opus 4.8**（缺陷漏检降4×，Dynamic Workflows） | **2026-05-29** | **新发布** | **4天** |
| Anthropic | Claude Opus 4.7 | 2026-04-16 | 活跃 | 47天 |
| **MiniMax** | **M3**（编程接近 Opus 4.7，#MSA 架构） | **2026-06-02** | **新发布** | **0天** |
| **阶跃星辰** | **Step-3.7-Flash**（198B MoE 多模态） | **2026-05-30** | **新发布** | **3天** |
| Meta | Muse Spark | 2026-04-08 | 活跃 | 51天 |

---

## 迭代速度排名

| 排名 | 厂商 | 模型数 | 平均间隔 | 最近间隔 | 趋势 |
|------|------|--------|---------|---------|------|
| 1 | **OpenAI** | 12 | ~2.2 月 | **48天** | 加速 |
| 2 | **xAI** | 5 | ~3.0 月 | **2月** | **显著加速** |
| 3 | **Google DeepMind** | 8 | ~2.8 月 | **8天（I/O 发布）** | **爆发** |
| 4 | **Anthropic** | 10 | ~2.8 月 | **41天** | **加速** |
| 5 | Tencent | 1 | - | 首发即开源 | 新入局 |
| 6 | DeepSeek | 7 | ~4 月 | ~4月 | 回归 |
| 7 | Moonshot AI | 4 | ~4 月 | 3月 | 加速 |
| 8 | Alibaba | 7 | ~3.0 月 | **0天（Qwen3.7-Plus）** | **爆发** |
| 9 | MiniMax | 4 | ~6.5 月 | **0天（M3）** | **加速** |
| 10 | 智谱 | 3 | ~6 月 | **11天前新发** | **爆发** |

---

## Benchmark 横向对比

### 编程能力（真实代码库修复 vs 人工编写的测试用例）

| 模型 | SWE-Verified | SWE-Pro | Terminal-Bench | LiveCodeBench | Code Arena |
|------|-------------|---------|---------------|---------------|------------|
| Claude Mythos | **93.9%** | **77.8%** | 82.0% | - | - |
| **Claude Opus 4.8** | - | - | - | - | - |
| Claude Opus 4.7 | **87.6%** | **64.3%** | 69.4% | 88.8 | - |
| GPT-5.5 | 80.0% | 58.6% | **82.7%** | - | - |
| DeepSeek V4-Pro | 80.6% | 55.4% | 67.9% | **93.5** | - |
| Kimi K2.6 | 80.2% | 58.6% | 66.7% | 89.6 | - |
| **Gemini 3.5 Flash** | - | - | **76.2%** | - | - |
| GPT-5.4 | 78.2% | 57.7% | 75.1% | - | - |
| **Qwen3.7-Max** | - | - | - | - | **1541 (#2)** |
| Grok 4.3 | 70.0% | - | - | - | - |

### 推理 & 知识（无工具/静态问答 + ARC 系列 + 长程执行）

| 模型 | GPQA | ARC-AGI-1 | ARC-AGI-2 | ARC-AGI-3 | HLE (no tools) |
|------|------|-----------|-----------|-----------|----------------|
| Claude Mythos | **94.6%** | - | - | - | **64.7%** |
| Gemini 3.5 Flash | 94.3% | **98.0%** | 77.1% | 0.37% | 44.4% |
| Claude Opus 4.7 | 94.2% | 93.5% | 75.8% | **0.18%** | 46.9% |
| GPT-5.5 | 93.6% | 95.0% | **85.0%** | **0.43%** | 41.4% |
| DeepSeek V4-Pro | 90.1% | - | - | - | - |
| Grok 4.3 | 88.0% | - | - | - | - |
| **人类** | - | - | - | **100%** | - |

### API 定价对比（美元/百万 Token）

| 模型 | Input $/M | Output $/M | 上下文 | 许可证 | 本周变化 |
|------|----------|-----------|--------|--------|---------|
| DeepSeek V4-Flash | $0.14 | **$0.28** | 1M | MIT | - |
| DeepSeek V3.2 | $0.28 | $0.42 | 128K | MIT | 7月退役 |
| MiniMax 2.7 | $0.30 | $1.20 | 1M | 闭源 | - |
| Kimi K2.6 | $0.60 | $2.50 | 262K | Modified MIT | - |
| **Grok 4.3** | **$1.25** | **$2.50** | **1M** | 闭源 | 4/30 新发布 |
| DeepSeek V4-Pro | $1.74 | $3.48 | 1M | MIT | - |
| **Qwen3.7-Max** | **$2.50** | **$7.50** | **1M** | 闭源 | **5/21 新发布** |
| **Qwen3.7-Plus** | 未公开 | 未公开 | 未公开 | 闭源 | **6/2 新发布，百炼 API** |
| Gemini 3.5 Flash | $1.25 | $5.00 | 1M | 闭源 | **5/19 新发布** |
| Gemini 3.1 Pro | $2.00 | $12.00 | 10M | 闭源 | - |
| GPT-5.4 | $2.50 | $15.00 | 1M | 闭源 | - |
| Claude Sonnet 4.6 | $3.00 | $15.00 | 200K | 闭源 | - |
| **GPT-5.5** | **$5.00** | **$30.00** | **1M** | 闭源 | - |
| **Claude Opus 4.7** | **$5.00** | **$25.00** | **200K** | 闭源 | - |
| GPT-5.5 Pro | $30.00 | $180.00 | 1M | 闭源 | - |

---

## 突破方向检测

| 维度 | 状态 | 领先者 | 分数 | 含义 |
|------|------|--------|------|------|
| ARC-AGI-3 | **通用推理缺口** | GPT-5.5 | **0.43%** | 人类 100%，233x 差距，scaling 的硬上限 |
| Code Arena | **新战场** | Qwen3.7-Max | **1541 (#2)** | 盲测编程能力新基准 |
| API 速度 | **新突破** | GLM-5.1-highspeed | **400 tok/s** | 打破"高速即轻量"定律 |
| SWE-bench Pro | 分化加剧 | Claude Mythos | **77.8%** | 前 2 差 13.5% |
| τ-voice | **新战场** | Grok Voice | **67.3%** | 语音 Agent 首个标准 benchmark |
| GPQA | 饱和 | Claude Mythos | 94.6% | 前 4 差 <0.5% |
| AIME | 饱和 | GPT-5.2/Gemini | 100% | 完全失去区分度 |

---

## 本周关键数字

> 仅收录模型参数、benchmark、能力评估、推理效率等模型本身的数据点。

| 指标 | 数值 | 来源 |
|------|------|------|
| **Qwen3.7-Max Code Arena** | **1541**（全球第二大编程模型） | [alibabacloud](https://www.facebook.com/alibabacloud/posts/qwen37-max-is-officially-the-2-ai-coding-model-globallyin-the-latest-code-arena-/1434941022011319/) |
| Qwen3.7-Max 上下文 | **1M tokens** | [OpenRouter](https://openrouter.ai/qwen/qwen3.7-max) |
| Qwen3.7-Max 自主可运行 | **35 小时** + 1000+ 工具调用 | [VentureBeat](https://venturebeat.com/technology/alibabas-proprietary-qwen3-7-max-can-run-for-35-hours-autonomously-and-supports-external-harnesses-like-anthropics-claude-code) |
| **GLM-5.1-highspeed 速度** | **400 tok/s**（全球最快 API） | [智谱](https://docs.bigmodel.cn/cn/guide/models/text/glm-5.1-highspeed) |
| **MiniCPM5-1B AA-Index** | **17.9**（超越所有 2B 以下模型） | [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651035127) |
| MiniCPM5-1B ForgeTrain | 较 Megatron **+10%** 训练速度 | [面壁智能](https://mp.weixin.qq.com/s/vLBxru7RYPp-V8cPpTMMCA) |
| **BitCPM-CANN 内存降低** | **6×**（vs BF16，1.58-bit 三元） | [Rohan Paul](https://x.com/rohanpaul_ai) |
| **AlphaProof Nexus Erdős** | **9/353 解决 + 44/492 证明** | [@pushmeet](https://x.com/pushmeet/status/2058936037754224998) |
| AlphaProof 单题成本 | 约几百美元（最困难问题） | [arXiv](https://arxiv.org/abs/2605.22763v1) |
| **OpenAI 通用模型 Erdős** | 80 年开放问题首获 AI 突破 | [@OpenAI](https://x.com/OpenAI/status/2057176201782075690) |
| **Gemini 3.5 Flash Terminal-Bench** | **76.2%**（超 GPT-5.4 的 75.1%） | [Google Blog](https://blog.google) |
| Gemini 3.5 Flash GDPval-AA | **Elo 1656** | [Google Blog](https://blog.google) |
| Gemini 3.5 Flash 速度 | 较 Gemini 3.1 Pro **4×** | [Google I/O](https://io.google) |
| **Tencent Hy-MT2** | 1.8B 版本登顶 HuggingFace #1 | [Tencent Hunyuan](https://x.com/TencentHunyuan) |
| Hy-MT2 量化后大小 | **440MB**（1.25-bit，可手机本地运行） | [Medium](https://medium.com/data-science-in-your-pocket/tencent-just-dropped-a-1-8b-translation-model-that-beats-commercial-apis-f1a1860a501c) |
| **Cohere Command A+** | **218B / 25B 激活**（Apache 2.0） | [Cohere@X](https://x.com/cohere/status/2057120818551734589) |
| **NVIDIA Nemotron-Diffusion** | 8B 吞吐 **4× Qwen3-8B**（SPEED-Bench GB200） | [HuggingFace Blog](https://huggingface.co/blog/nvidia/nemotron-labs-diffusion) |
| 网易子曰4 多模态 | **27B**，中文数理 **81.4%** | [IT之家](https://www.ithome.com) |
| 网易子曰4 思维链压缩 | 输出长度压缩 **43.2%** | [IT之家](https://www.ithome.com) |
| 网易子曰4 语音克隆 | **3 秒**克隆，14 语种，>97% 准确度 | [IT之家](https://www.ithome.com) |
| LongCat-Video-Avatar 推理步数 | 仅需 **8 步**（DMD2 步蒸馏） | [HuggingFace](https://huggingface.co) |
| **Grok V9-Medium**（5/27） | **1.5T 参数**，2-3 周内发布 | [@elonmusk](https://x.com/elonmusk/status/2058787384364265734) |
| Grok V9-Medium 训练 | 大量 Cursor 编程数据补充 | [@elonmusk](https://x.com/elonmusk/status/2058787384364265734) |
| **Keye-VL-2.0**（5/27） | **256K 上下文 + 首个 DSA 多模态** | [Hugging Face](https://huggingface.co/Kwai-Keye/Keye-VL-2.0-30B-A3B) |
| Keye-VL-2.0 VideoMME V2 | 64→512 帧：**35.3% → 42.4%**（不降反升） | [量子位](https://mp.weixin.qq.com/s/gomgqFAZrdbJFQlOfSJxpQ) |
| Keye-VL-2.0 LongVideoBench | **74.1**（超 Qwen3-VL-235B-A22B） | [Hugging Face](https://huggingface.co/Kwai-Keye/Keye-VL-2.0-30B-A3B) |
| **SkyClaw-v1.0**（5/27） | **1M 上下文**，价格仅 Sonnet 4.6 的 1/43~1/27 | [新智元](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA==&mid=2652702909&idx=1&sn=242761d18907f204339ead4777ce72b4) |
| Cursor Composer 2.5 算力 | Colossus 2 百万级 H100，**10× 计算量** | [Cursor Blog](https://cursor.com/cn/blog/composer-2-5) |
| **GPT-5.6 上下文**（泄露） | **150 万 tokens**（+43% vs GPT-5.5） | [新智元](https://mp.weixin.qq.com/s/T8x357cWij8VKsTlm868Qg) |
| **SaaS-Bench Opus 4.7** | 端到端通过率 **3.8%**（106 任务 4 个通过） | [UniPat AI](https://unipat.ai) |
| **Stanford ABA**（5/27） | **25.7%** AI benchmark 任务存在缺陷 | [arXiv](https://arxiv.org/abs/2605.26079) |
| ABA 移除问题任务后 | SWE-bench Verified **+9.9%**、Terminal-Bench 2 **+9.6%** | [arXiv](https://arxiv.org/abs/2605.26079) |
| **Qwen CUA-Gym**（5/27） | OSWorld-Verified **A17B 72.6%**、32K 训练数据 | [arXiv](https://arxiv.org/abs/2605.25624) |
| Anthropic Mythos 1 | 进入 Claude Code / Claude Security 产品线 | [TestingCatalog](https://www.testingcatalog.com/anthropic-prepares-mythos-1-for-claude-code-and-claude-security/) |
| **Claude Opus 4.8**（5/29） | **缺陷漏检降 4×**，LAB 首个突破 10%，41 天迭代 | [Anthropic Blog](https://www.anthropic.com/news/claude-opus-4-8) |
| Opus 4.8 Dynamic Workflows | **数十到上百个并行子 Agent** 交叉验证 | [Anthropic Blog](https://www.anthropic.com/news/claude-opus-4-8) |
| Bun 团队 Opus 4.8 实战 | **75 万行 Zig → Rust，11 天，99.8% 通过** | [Anthropic Blog](https://www.anthropic.com/news/claude-opus-4-8) |
| **Step-3.7-Flash**（5/30） | **198B MoE / 11B 激活**，图像+视频多模态 | [OpenRouter](https://x.com/OpenRouter/status/2060195234756370768) |
| MAI-Image-2.5 Arena | 文生图 **第 3 名** | [Microsoft AI](https://microsoft.ai/news/mai-image-2-5-launches-at-no-3-on-arena-ai/) |
| EAGLE 3.1 接受长度 | 长上下文接受长度较 EAGLE 3 **提升 2×** | [vLLM Blog](https://vllm.ai/blog/2026-05-26-eagle-3-1) |
| **Qwen3.7-Plus**（6/2） | Terminal Bench 2.0 **70.3**（超 Opus 4.6 Max 65.4） | [Qwen Blog](https://qwen.ai/blog?id=qwen3.7-plus) |
| Qwen3.7-Plus 多模态 | ScreenSpot Pro **79.0**、AndroidWorld **81.0**、MathVision **90.3** | [Qwen Blog](https://qwen.ai/blog?id=qwen3.7-plus) |
| **MiniMax M3**（6/2） | 编程能力接近 **Opus 4.7**，#MSA 架构 | [The Information](https://www.theinformation.com/briefings/chinas-minimax-launches-new-model-open-source-ai-coding-battle-heats) |
| **NVIDIA Cosmos 3**（6/2） | Mixture-of-Transformers，5 模态统一（文本/视频/图像/音/动作） | [NVIDIA Blog](https://blogs.nvidia.com/blog/cosmos-3-physical-ai-open-world-foundation-model/) |
| **JetBrains Mellum2**（6/2） | **12B** 稀疏 MoE，IDE 原生编程模型 | [HuggingFace Blog](https://huggingface.co/blog/JetBrains/mellum2-launch) |
| **Wall-OSS-0.5**（5/29） | RoboCaca 精密插入 **39.6%**（π0.5 仅 4.0%） | 自变量机器人 |
| **MiMo-V2.5**（6/2） | Hybrid SWA KVCache 降至 Full Attention 的 **1/7** | [Xiaomi MIMO Blog](https://mimo.xiaomi.com/blog/mimo-v2-5-inference) |

---

## 前瞻预判

### 近期可能发布

| 厂商 | 预期模型 | 信号强度 | 预计时间 |
|------|---------|---------|---------|
| Google DeepMind | Gemini 3.5 Pro | 高（I/O 已发布 Flash，Pro 跟进） | **6 月** |
| OpenAI | GPT-5.6（iris-alpha） | 中（150 万 token 上下文泄露） | **6 月** |
| Anthropic | Sonnet 4.8（代号 Conway） | 中（视觉 >98%，新增 X-high 层级） | **6 月中下旬** |
| Anthropic | Mythos 新能力（预告数周内发布） | 高（Opus 4.8 已发布，Mythos 为下一阶梯） | **数周内** |
| **xAI** | **Grok V9-Medium 1.5T**（已训练完成） | **高（Musk 5/27 官宣）** | **2-3 周内** |
| 昆仑万维 | SkyClaw-v1.0 限免试用结束转付费 | 中（Agent-native 1M ctx） | 6 月 |

### 非共识判断

1. **API 速度竞争正在成为新战场**：GLM-5.1-highspeed 的 400 tok/s 刷新全球纪录，打破了"高速模型即轻量模型"的传统认知。这可能引发新一轮 API 速度竞赛——不是能力，而是延迟。

2. **Code Arena 盲测是比 SWE-Pro 更接近真实编程的信号**：Qwen3.7-Max 1541 排名 #2（仅次于 Claude），盲测消除了 prompt engineering 优势。但 Code Arena 上 GPT-5.5 的具体排名尚未公开，"超越 GPT-5.5"的判断需要第三方验证。

3. **Google I/O 一箭双雕——Gemini 3.5 Flash + Omni 同时发布**：Google 同时推出编程旗舰（Flash）和世界模型（Omni），展示在模型层多线推进能力。Flash 的 Terminal-Bench 76.2% 已超越 GPT-5.4，Gemini 3.5 Pro 6 月发布后可能改写编程能力排行榜。

4. **数学推理出现双线突破**：OpenAI 通用模型攻克 80 年单位距离问题、Google AlphaProof Nexus 解决 9 个 Erdős + 44 个 OEIS 猜想（含两道 56 年难题），同一周两条独立技术路线均取得突破。**这不再是"是否能解"的问题，而是"成本与规模"问题**——AlphaProof 单题约几百美元已具研究级实用价值。

5. **Benchmark 进入"自审"阶段**：Stanford ABA 揭示 25.7% benchmark 任务有缺陷，移除后 SWE-bench Verified 与 Terminal-Bench 2 平均分均上升约 10pp 且模型排名变化。叠加 SaaS-Bench 暴露 Opus 4.7 端到端仅 3.8% 通过率，**当前 benchmark 时代的可信度正被系统性重估**。

6. **xAI 加码编程模型**：Grok V9-Medium 从 0.5T 跃升至 1.5T 参数，训练中加入大量 Cursor 编程数据，2-3 周后公开发布。结合 Cursor Composer 2.5 基于 Kimi K2.5、Qwen3.7-Max Code Arena #2、Claude Mythos SWE-Pro 77.8% 等信号，**编程模型已成为各家旗舰能力的核心竞争维度**。

7. **DSA 跨模态成功**：快手 Keye-VL-2.0 首次将 DeepSeek Sparse Attention 落地多模态，**架构通用性获验证**——稀疏注意力不只是 LLM 加速技术，也能跨域到视觉理解，512 帧仍维持长上下文性能。

8. **Anthropic 41 天迭代 Opus 4.8 + Dynamic Workflows = Agent 基础设施化**：Opus 4.8 不仅是模型升级，更通过 Dynamic Workflows（数十到上百个并行子 Agent）将"模型能力"转化为"系统级 Agent 基础设施"。Bun 团队 75 万行 Zig→Rust 的实战案例证明，**编程模型的价值已从"写代码"升级为"重构整个代码库"**。

9. **Qwen3.7-Plus 在 Terminal Bench 2.0 上首次超越 Anthropic 头部模型**：70.3 > Opus 4.6 Max 65.4，结合 Qwen3.7-Max 在 Code Arena #2 的表现，阿里在编程模型赛道已从追赶者变为并跑者。多模态 Agent benchmark（ScreenSpot Pro 79.0、AndroidWorld 81.0）的系统性领先进一步巩固了这一判断。

10. **开源 VLA 开始超越闭源**：Wall-OSS-0.5 在 RoboCaca 精密插入达 39.6%，领先 π0.5 的 4.0% 近 10 倍。这打破了"闭源 VLA 碾压开源"的假设，开源 VLA 生态正在形成与闭源（π0.5、Gemini Robotics）的正面竞争。

### 下周关注

1. **Gemini 3.5 Pro 发布时间**：Flash 已 GA，更强的 Pro 版本何时跟进
2. **GPT-5.6 动向**：150 万 token 上下文是否得到官方确认
3. **Anthropic Sonnet 4.8（代号 Conway）**：6 月中下旬可能发布，视觉准确率提升至 >98%，新增 X-high 推理层级
4. **Grok V9-Medium 2-3 周后正式发布**：1.5T 参数、Cursor 编程数据训练，是否能与 Qwen3.7-Max / Claude 在编程上正面较量
5. **Mythos 1 灰度进度**：Claude Code / Claude Security 集成后是否会进一步开放给开发者
6. ~~**MiniMax M3 开源发布**~~ → **已发布**（6/2），编程接近 Opus 4.7，后续追踪 #MSA 架构细节和 benchmark 完整数据
7. **Microsoft Build 大会**：发布自研编码模型，强化 GitHub Copilot 竞争力
8. **Qwen3.7-Plus 后续**：Terminal Bench 2.0 新标杆能否在 Code Arena 盲测中同步验证
9. **NVIDIA Cosmos 3 生态**：开源程度、机器人团队接入进展、与 Gemini Robotics 对照

---

*数据来源：[阿里 Qwen](https://x.com/Alibaba_Qwen) | [Cursor Blog](https://cursor.com/cn/blog/composer-2-5) | [面壁智能](https://mp.weixin.qq.com/s/vLBxru7RYPp-V8cPpTMMCA) | [智谱文档](https://docs.bigmodel.cn) | [Hugging Face](https://huggingface.co) | [Google Blog](https://blog.google) | [@pushmeet](https://x.com/pushmeet) | [Cohere](https://cohere.com) | [NVIDIA Research](https://research.nvidia.com) | [@elonmusk](https://x.com/elonmusk) | [Tencent Hunyuan](https://x.com/TencentHunyuan) | [arXiv](https://arxiv.org) | [机器之心](https://mp.weixin.qq.com) | [量子位](https://mp.weixin.qq.com) | [新智元](https://mp.weixin.qq.com) | [TestingCatalog](https://www.testingcatalog.com) | [UniPat AI](https://unipat.ai) | [VentureBeat](https://venturebeat.com)*

*报告范围：仅聚焦模型本身的发布、能力、benchmark、推理效率、部署预告。融资、人事、算力基础设施、产品化等非模型信号请参阅日度 AI 简报。*

*生成时间：2026-06-02*