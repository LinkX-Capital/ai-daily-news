## 07月09日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：OpenAI将于周四公开发布GPT-5.6模型家族; MiniMax研发2.7万亿参数模型M3 Pro，计划Q3发布并开源; xAI与Cursor联合发布Grok 4.5，主打编程与Agent的低成本与高token效率
- 产业动态：OpenAI发布GPT-Live全双工语音模型，ChatGPT语音升级为实时对话; NVIDIA Nemotron 3 Ultra搭配LangChain Deep Agents Harness取得benchmark领先性能; 法国ZML发布跨芯片推理服务器LLMD免费上线; Together AI推出Provisioned Throughput预留推理容量服务
- 算力追踪：NVIDIA与d-Matrix联合推出AI芯片系统; 英特尔公布XBM超高带宽内存专利对标HBM4; 中国计划允许头部AI公司限量采购NVIDIA H200芯片
- 初创&融资：SambaNova完成10亿美元F轮首关，估值110亿美元并获摩根大通推理基建订单
- 研究关注：智源研究院提出多模态表征世界模型Orca转向"下一世界状态"预测; RynnWorld-4D用RGB-深度-光流统一扩散生成4D具身世界模型; HiLS Attention让稀疏注意力端到端学习分块选择外推达训练上下文64倍
- X讨论：SemiAnalysis披露Anthropic 2026年Q3利润超10亿美元、赴IPO前财务预览; Liquid AI：Antidoom用末位token偏好优化将推理模型doom-loop率降至1.4%; Artificial Analysis独立评测Grok 4.5智能指数54分排第4、成本token效率突出; Cognition发布SWE-1.7编码模型在已RL过的Kimi K2.7基座上再获大幅提升

---

## 📖 详细参考

### 模型前沿
**OpenAI将于周四公开发布GPT-5.6模型家族**
- OpenAI 宣布将于**周四**公开发布 GPT-5.6 系列模型。GPT-5.6 是 GPT-5 系列的迭代版本，发布前特朗普政府曾因网络安全顾虑要求 OpenAI 限量发布新模型；据 Axios 报道，政府已放行 GPT-5.6 的 **Sol、Terra** 等版本。
  > 💡 GPT-5.6属于GPT-5系列的小版本迭代，发布节奏密集反映OpenAI在头部模型市场的迭代压力加大。
   - 来源: [The Information](https://www.theinformation.com/briefings/openai-publicly-launch-gpt-5-6-family-models-thursday) | [@OpenAI](https://x.com/OpenAI/status/2074704958419792299)

**xAI与Cursor联合发布Grok 4.5，主打编程与Agent的低成本与高token效率**
- xAI（SpaceXAI）联合 Cursor 发布 Grok 4.5，定位编码、Agent 与知识工作，在数万张 NVIDIA GB300 上训练，RL 覆盖数十万任务。工程类评测中 DeepSWE 1.0 得 **62.0%**、Terminal Bench 2.1 **83.3%**、SWE Bench Pro resolve **64.7%**，均落后于 Fable（max），与 GPT 5.5 接近，在 DeepSWE 与 Terminal Bench 上超过 Opus 4.8。核心卖点是 token 效率——SWE Bench Pro 平均输出 **15,954 tokens，约为 Opus 4.8（67,020）的 1/4.2**，推理速度 80 TPS，定价 **$2/百万输入、$6/百万输出**。已在 Grok Build、Cursor 全套餐及 SpaceXAI 控制台上线，欧盟暂不可用。
  > 💡 Grok 4.5 工程评测并未超过 Fable，真正差异化是 token 效率与价格：以约 1/4 的输出 token 和极低单价切入编码市场，叠加 Cursor 分发争夺开发者，对 Opus/GPT 编码模型构成单位成本压力。
   - 来源: [xAI](https://x.ai/news/grok-4-5) | [@SpaceXAI](https://x.com/SpaceXAI/status/2074915721684086811) | [The Information](https://www.theinformation.com/briefings/spacexai-cursor-launch-grok-4-5-tout-lower-costs-rivals)

**MiniMax研发2.7万亿参数模型M3 Pro，计划Q3发布并开源**
- 据 The Information 报道，MiniMax 正在研发一款 **2.7 万亿参数**的大语言模型，内部代号暂定 **M3 Pro**，相较现有旗舰 M3 的 **4280 亿参数**实现数量级跃升，最快 **今年第三季度**发布并计划**同步开源**，定位复杂推理、多步骤任务与长上下文理解。其商业化已跑通：MiniMax M3 混合定价为 **每百万 token 0.22 美元**，美银披露上一代模型 M2.7 最终实现 **超 40% 推理利润率**，同期高盛、美银、花旗均给予"买入"评级。
  > 💡 2.7 万亿参数（代号 M3 Pro、Q3 开源）让 MiniMax 在规模上对标海外万亿模型，但更值得注意的是"规模+效率"双线叙事——M3 以 $0.22/百万 token 定价与 40% 推理利润率证明其高效架构已跑通，规模化与毛利率兼得正成为国产头部厂商竞争的新焦点。
   - 来源: [The Information](https://www.theinformation.com/briefings/exclusive-chinas-minimax-plans-launch-2-7-trillion-parameter-model) | [Z Potentials](https://mp.weixin.qq.com/s/4kQrhboy6s06QtYclHftGw)

### 产业动态
**OpenAI发布GPT-Live全双工语音模型，ChatGPT语音升级为实时对话**
- OpenAI 发布 GPT-Live 语音模型系列，采用**全双工架构**，可同时听与说，能用"mhmm""yeah"等回应表示在听，并支持打断与停顿。遇到需搜索或深度推理的问题时，会委托给后台前沿模型（首发为 GPT-5.5）处理，对话不中断。首发 GPT-Live-1 与 GPT-Live-1 mini 两版，替代此前的级联式（ASR→LLM→TTS）与轮次式（Advanced Voice Mode）方案，在 GPQA、BrowseComp、τ³-Voice Telecom 上优于 Advanced Voice Mode。每周超 **1.5 亿人**使用 ChatGPT 语音与听写；GPT-Live-1 成为 Go/Plus/Pro 默认，mini 为免费版默认，暂不支持视频与屏幕共享。
  > 💡 全双工把语音交互从"轮流说话"推向"实时对话"，是交互形态的代际升级；把重活委托给后台前沿模型的解耦设计，让语音层可持续跟随最新模型迭代而不被冻结。
   - 来源: [OpenAI](https://openai.com/index/introducing-gpt-live)

**NVIDIA Nemotron 3 Ultra搭配LangChain Deep Agents Harness取得benchmark领先性能**
- NVIDIA官方博客披露，Nemotron 3 Ultra模型在结合LangChain生态中应用最广泛的Deep Agents编排框架后，于多项Agent编排benchmark上以更低成本达到领先成绩，覆盖编码、工具调用、多步推理等任务。NVIDIA强调这是当前采用率最高的Agent编排栈与Nemotron模型的协同优化结果。
  > 💡 NVIDIA把Nemotron与LangChain生态绑定，本质是用推理软件栈协同放大模型竞争力，对冲开源模型在Agent场景下对闭源模型的替代风险。
   - 来源: [NVIDIA Blog](https://blogs.nvidia.com/blog/nemotron-langchain-agents-open-stack/)

**法国推理创业公司ZML发布跨芯片推理服务器LLMD，免费上线以打破厂商锁定**
- 法国 AI 推理创业公司 ZML（图灵奖得主 Yann LeCun 背书，创始人 Steeve Morin 曾任 Zenly 工程副总裁）发布 LLM 推理服务器 **ZML/LLMD**，支持各类开源大模型在 NVIDIA、AMD、Google TPU、Apple Metal、Intel Arc 等多种芯片上以峰值速度运行，目标是打破硬件厂商锁定、让用户混用更便宜或更省电的芯片。产品**免费**上线（非开源），用于收集使用数据；团队仅 20 人，已融资 2000 万美元，投资方含 Hugging Face 创始人 Clément Delangue、Julien Chaumond 及 Docker 创始人 Solomon Hykes。竞品包括估值 130 亿美元的 Baseten、Inferact 与 RadixArk。
  > 💡 推理成本焦虑催生"推理淘金热"，跨芯片推理中间件瞄准的是 NVIDIA 之外的存量算力池；免费策略意在先占开发者心智，但与 vLLM、SGLang 等开源栈的差异化能否持续是关键。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/08/hot-french-startup-zml-releases-free-product-to-speed-inference-across-lots-of-ai-chips/)

**Together AI推出Provisioned Throughput预留推理容量服务**
- Together AI 上线 Provisioned Throughput 服务，为 MiniMax-M3、GLM-5.2 等前沿开源模型提供预留推理容量，首发即支持这两款模型，覆盖北美、EMEA 等地、最低一个月起订。计费按 Provisioned Throughput Unit（PTU，**$0.05/分钟**）购买，输入、缓存输入与输出 token 以不同速率消耗 PTU；MiniMax M3 满负载下单 PTU 约合 **$0.36/百万输入、$2.16/百万输出 token**，并提供 **99% 正常运行时间 SLA**。Together AI 称该方案成本比 Claude Opus 4.8 列表价低最多 **90%**，并援引客户数据称开源模型推理成本较闭源低 6–20 倍；其 API 月 token 量九个月内从 300 亿增至逾 400 万亿。
  > 💡 Together AI从按需推理转向预留容量，反映开源推理服务商向企业级SLA市场延伸的趋势，对标云厂商Reserved Instance模式。
   - 来源: [Together AI Blog](https://www.together.ai/blog/provisioned-throughput)

### 算力追踪
**NVIDIA与d-Matrix联合推出AI芯片系统，以合纵连横对冲芯片竞争**
- NVIDIA 与 AI 服务器芯片创业公司 d-Matrix 将把双方硬件组合成一套新的 AI 芯片系统用于驱动大模型。The Information 指出这是 NVIDIA 整体策略的一部分——通过与更多竞争对手合作，对冲其成功或从中获利。
  > 💡 NVIDIA 从独占转向合纵连横，把潜在芯片竞争者纳入自家系统，是其在 AMD 与各家自研芯片浪潮下维持生态主导权的防御性布局。
   - 来源: [The Information](https://www.theinformation.com/briefings/nvidia-d-matrix-announce-joint-ai-chip-system)

**英特尔公布XBM超高带宽内存专利，对标HBM4但商业化在2030年之后**
- 据 wccftech 报道，英特尔公布名为 XBM（eXtended Bandwidth Memory）的超高带宽内存专利，定位 HBM4 替代方案：封装尺寸与 HBM4 一致，单芯片容量 **0.5–5GB**，搭载 **32GT/s** 的 UCIe 芯粒互联接口。核心革新是把 1T1C 存储单元从 FEOL 前段制程转移到 BEOL 后段，用薄膜晶体管堆叠在晶体管上方，以容纳更多硅通孔、提升集成密度与带宽上限，专利重点在定制化封装（封装集成内存 MoP 与反向悬垂结构）压低 Z 轴堆叠高度。商业化预计在 **2030 年之后**；同期英特尔还与软银子公司 SAIMEMORY 联合开发 ZAM 方案，带宽密度约为 HBM4 的两倍，目标 2029 年商业化。
  > 💡 AI 算力增速远超内存读写，"内存墙"正成为整体性能瓶颈，HBM 替代路线是下一代算力竞争的关键变量；但 XBM 距量产仍有数年，短期 HBM 格局难以撼动。
   - 来源: [wccftech](https://wccftech.com/intel-xbm-memory-takes-aim-at-hbm4-32-gt-s-speeds-lower-costs-through-ucie-links/) | [财联社](https://mp.weixin.qq.com/s/0H7K9keOgH76LuIOKu2UgA)

**中国计划允许头部AI公司限量采购NVIDIA H200芯片**
- 据The Information援引两位知情人士，中国计划允许部分头部AI公司采购少量NVIDIA H200芯片，旨在缓解AI芯片需求激增导致的短缺。H200是H100的下一代产品，HBM3e显存容量与带宽较H100提升显著。报道未披露具体配额数量与首批获准企业名单。
  > 💡 在H20被禁、自研芯片尚未完全补位的窗口期，限量放行H200是中美技术管制下的折中方案，对国内头部厂商的下一代模型训练计划构成关键供给补充。
   - 来源: [The Information](https://www.theinformation.com/articles/china-plans-let-top-ai-firms-buy-limited-amount-nvidia-h200-chips)

### 初创&融资
**SambaNova完成10亿美元F轮首关，估值110亿美元并获摩根大通推理基建订单**
- AI 芯片公司 SambaNova 完成 **10 亿美元** F 轮首关，估值 **110 亿美元**，由 General Atlantic 领投，后续仍有投资者加入。本轮距其 2 月的 3.5 亿美元 E 轮及 SN50 芯片发布仅约 5 个月；此前彭博曾报道 Intel 洽谈以约 **16 亿美元**估值收购该公司。融资同期，SambaNova 被摩根大通选为"推理基础设施合作伙伴"，SN40L 与 SN50 系统将为其部署安全、本地化的 AI 推理；下一代 SN50 计划 2026 下半年出货，软银为首个部署伙伴，其卖点是把万亿参数模型塞进单个机柜快速运行，客户还包括沙特阿美、Intel 及多家日本企业。
  > 💡 摩根大通这类顶级金融机构自建本地推理基建，是"去云化"推理需求从互联网向金融等强监管行业扩散的信号；SambaNova 以单机柜承载万亿参数模型的定位，正卡位这块私有化推理市场。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/08/sambanova-draws-1b-at-11b-valuation-in-series-f-first-close/)

### 研究关注
**智源研究院提出多模态表征世界模型Orca，转向"下一世界状态"预测**
- 智源研究院悟界·RoboBrain Orca，定位为多模态表征世界模型（Multimodal Latent World Model）。其核心转向是不再绑定 Next Token / Next Frame / Next Action 的单一模态预测，而是先在统一的 World Latent Representation 空间学习世界状态转移（Next State Prediction），再以冻结 backbone + 轻量 readout 读出文本、图像、动作。学习分两条路径：从连续视频学稠密自然状态转移（无意识学习），从语言事件、任务指令与 VQA 学稀疏但有语义意义的状态转移（有意识学习）。预训练数据含 **12.5 万小时视频、1.6 亿条事件标注、1150 万条 VQA**，当前仅用约十分之一且损失仍在下降。下游 zero-shot OOD 结果：文本读出在 4B 规模多项综合评测取得同规模最高平均分，提升集中在状态转移与事件演化维度；图像读出在 PRICE 上比 FLUX 2、OmniGen2 更好保持场景与物体一致性、符合物理常识；动作读出在预训练未用任何动作标签的情况下，仅用每任务 200 条域内轨迹即完成多个 OOD 双臂操作，整体达到经大规模机器人数据预训练的 π0.5 水平。
  > 💡 把"预测下一个模态输出"统一为"预测下一个世界状态"，是用一个潜空间同时支撑语言、视觉、具身三类任务的范式尝试；最值得关注的是预训练完全不用动作标签，却靠世界表征迁移在少量机器人数据上接近 π0.5，直击具身智能的数据稀缺与泛化难题。
   - 来源: [智源研究院](https://mp.weixin.qq.com/s/j20nOnm0hajH5jy_lStHug) | [arXiv](https://arxiv.org/abs/2606.30534)

**HiLS Attention让稀疏注意力端到端学习分块选择，外推达训练上下文的64倍**
- 论文提出 HiLS Attention（Hierarchical Landmark Sparse），针对现有稀疏注意力方法因分块选择不准而跑不赢全注意力的痛点。核心是把注意力分层：每个 query 先与每个被检索分块独立做注意力抽取分块信息，再按分块检索得分融合；由于检索得分直接进入前向计算，可与语言建模损失一起端到端优化，实现原生稀疏训练。实验上 HiLS 在域内上下文长度达到与全注意力相当甚至更优的表现，并能外推到训练上下文长度的 **64 倍以上、检索准确率 90%**，远超全注意力；已有全注意力模型可用轻量继续预训练转换为 HiLS，域内性能不降。
  > 💡 长上下文的真正瓶颈是注意力二次开销与外推能力差，HiLS 把"选哪些块"从启发式规则变成可学习目标，是稀疏注意力走向端到端的关键一步，对超长上下文落地与推理成本都有直接价值。
   - 来源: [arXiv](https://arxiv.org/abs/2607.02980) | [HuggingFace Papers](https://huggingface.co/papers/2607.02980)

**RynnWorld-4D用RGB-深度-光流统一扩散生成4D具身世界模型，服务机器人操作**
- 论文提出 RynnWorld-4D，面向机器人操作的 4D 具身世界模型，核心是用同步的 RGB、深度与光流（RGB-DF）作为物理接地表征刻画场景 4D 动力学，相比 2D 像素视频更贴近末端执行器的低层动作，缩小世界预测与策略学习的差距。模型采用三分支架构（跨模态注意力 + 逐帧 3D RoPE），在统一扩散过程中从单张 RGB-D 图像与语言指令同时生成未来 RGB 帧、深度图与光流；配套构建 Rynn4DDataset 1.0（**2.544 亿帧**第一视角人与机器人操作视频，含深度与光流伪标签），并设计 RynnWorld-4D-Policy 逆动力学头消费内部 4D 表征用于动作生成。
  > 💡 给世界模型补上"深度+运动"的 4D 几何维度，用物理接地而非纯像素桥接"预测世界"与"控制机器人"，与纯表征路线（智源 Orca）形成互补的具身世界模型路径。
   - 来源: [arXiv](https://arxiv.org/abs/2607.06559) | [HuggingFace Papers](https://huggingface.co/papers/2607.06559)

### X讨论
**SemiAnalysis：Anthropic 2026年Q3利润超10亿美元，赴IPO前财务预览**
- 据 SemiAnalysis（其 Tokenomics 团队按 SKU、层级与客户类型自下而上建模，并被 WSJ 报道验证准确）披露，Anthropic **2026 年第三季度利润超 10 亿美元**。Anthropic 已于 **6 月 1 日秘密提交 IPO**，将成为此规模首家上市的 AI 实验室（中国的智谱、MiniMax 已先行上市）；同期 OpenAI 据报道将自身 IPO 推迟至 2027，引发市场对 labs 融资能力的疑虑。SemiAnalysis 指出 Anthropic 与 OpenAI 合计约 **1000 亿美元 ARR**，2026 年 Claude Code 席卷软件开发，使 Anthropic 成为 AI 模型盈利化的明确赢家——在 B2B 市场以盈利姿态领先于“目标分散、持续烧钱”的 OpenAI；其 base case 甚至给出 Anthropic 在持续执行下有望成为首家 **6 万亿美元**市值公司的可能性。
  > 💡 Anthropic 单季盈利破 10 亿美元并抢先 IPO，把“谁先证明 AI 能赚钱”的叙事牢牢握住，并倒逼 OpenAI 公开财务、融资应战；但 6 万亿美元市值是条件化的激进预测，能否兑现取决于 Claude Code 的护城河、定价权与对开源/Grok 的防御。
   - 来源: [SemiAnalysis](https://newsletter.semianalysis.com/p/anthropic-3q26-profit-over-1b-the) | [@SemiAnalysis](https://x.com/SemiAnalysis_/status/2074803351728869865)

**Liquid AI：Antidoom用末位token偏好优化将推理模型doom-loop率降至1.4%**
- Liquid AI 发布方法 Antidoom，针对推理模型推理时反复生成同一片段（"doom loop"，如重复"Wait, let me reconsider…"）直至耗尽上下文的退化问题。方法定位到循环起始的单一 token，用 Final Token Preference Optimization（FTPO，改编自 Antislop）在该位置训练模型偏好连贯替代项，其余分布基本不动。在 LFM2.5-2.6B 早期 checkpoint 上，难题与编码 prompt 的循环率从 **10.2% 降至 1.4%**，各项评测分数随之提升，博客称整体 doom-loop 率降幅最高达 **90%**。
  > 💡 相比通用的 repetition_penalty 或需在线滚动的 RL，定位到单一 token 做偏好优化是一种更外科手术式的退化修复，对模型整体行为扰动小；小型推理模型的循环退化是落地痛点，这类低成本后训练修复有明确工程价值。
   - 来源: [Liquid AI](https://www.liquid.ai/blog/antidoom) | [@liquidai](https://x.com/liquidai/status/2074494130126811473)

**Artificial Analysis独立评测Grok 4.5：智能指数54分排第4，成本与token效率突出**
- 独立评测机构 Artificial Analysis 发布 Grok 4.5 评测：在其 Intelligence Index v4.1（含 GDPval-AA、Terminal-Bench 2.1、GPQA Diamond、SciCode、Humanity's Last Exam 等 9 项）上得 **54 分、排第 4**，仅落后 Fable 5、GPT-5.5、Opus 4.8，较 Grok 4.3 提升 16 分，称已把 SpaceXAI 带到仅次于 OpenAI/Anthropic 的智能前沿并超过所有开源权重模型及 Google Gemini。编程智能体指数上 Grok 4.5（Grok Build）得 **76**，与 GPT-5.5（Codex）持平、仅次于 Fable 5（Claude Code）；GDPval-AA v2 以 Elo **1543** 排第 4（介于 Opus 4.8 的 1600 与 GLM-5.2 的 1513 之间），𝜏³-Banking 以 **33%** 居首。成本上每任务约 **$0.31**（智能指数）/ **$2.49**（编程智能体），远低于 Fable 5 的 $11.80 与 GPT-5.5 的 $5.07，因定价较 Opus 4.8/GPT-5.5 低逾 60% 且每任务仅用约 **1.9M token**（对比 Fable 5 的 7.2M、GPT-5.5 的 6.2M）。另披露 Grok 4.5 为 **1.5T 参数**（Musk 称为 Grok 4.3 的 3 倍）、上下文窗口 **500k**（较 Grok 4.3 的 1M 收窄）。
  > 💡 第三方独立评测印证了 xAI 自报的“成本与 token 效率”叙事，但把 Grok 4.5 明确定位在 Fable/GPT/Opus 之后的第二梯队——靠价格与效率逼近前沿，而非智能领先。
   - 来源: [Artificial Analysis](https://artificialanalysis.ai/models/grok-4-5) | [@ArtificialAnlys](https://x.com/ArtificialAnlys/status/2074956932289282087)

**Cognition发布SWE-1.7编码模型，在已RL过的Kimi K2.7基座上再获大幅提升**
- Cognition 发布 SWE-1.7，称其训练过的最强模型，在 Kimi K2.7 基座（已历经大量 RL 后训练）之上仍取得大幅提升，挑战“后训练天花板”假设。FrontierCode 1.1 Main 得 **42.3%**（接近 GPT-5.5 的 43.0%、低于 Opus 4.8 的 46.5%，远高于基座 Kimi K2.7 Code 的 30.1% 与 GLM-5.2 的 24.5%），Terminal-Bench 2.1 **81.5%**、SWE-Bench Multilingual **77.8%**；已在 Devin（Web/桌面/CLI）经 Cerebras 以 **1000 TPS** 提供。技术亮点包括：用 top-p 采样 + 采样分布重放抑制熵崩溃与训练-推理失配、跨三大洲四数据中心的多集群训练（1T 参数跨洲权重更新压缩 >99%、1–2 分钟完成）、长程任务的自我压缩（rollout 最长 6 小时）与交替长度惩罚；行为上形成更凝练的思维链与“先充分探索代码库再动手”的倾向。
  > 💡 SWE-1.7 的价值不在绝对分数（仍逊于 Opus 4.8），而在两点：一是证明强 RL 基座仍可被进一步拉开，二是把多集群、长程自我压缩等工程能力沉淀进编码模型训练——这是编码 Agent 厂商把“模型 + Agent harness”协同优化的典型路径。
   - 来源: [Cognition](https://cognition.com/blog/swe-1-7) | [@cognition](https://x.com/cognition/status/2074882968770728416)

---
*更新时间: 2026-07-09 08:19*