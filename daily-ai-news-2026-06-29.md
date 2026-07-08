## 06月29日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 产业动态：福特重新雇佣资深工程师，承认 AI 未能替代制造环节经验; 印度国家支付公司 CEO：AI 将深度参与下一代数字支付增长; OpenRouter 持续运行 GPQA 与 TAU-Bench 对开源模型进行实时评测; Google因算力限制缩减Meta对Gemini模型的调用额度
- 算力追踪：华尔街押注美光成为下一个英伟达，AI驱动内存需求成核心逻辑; 光本位科技联合东方天算启动全球首颗天基光计算卫星：单卡300 TOPS载荷已开展在轨试验
- 初创&融资：百度旗下 AI 芯片公司昆仑芯 IPO 路演中要求投资人购买其半导体产品
- 研究关注：SciAtlas：浙大开源4300万论文级科研知识图谱，配套 CLI 与 Agent Skill 服务自动化科研; Red Queen Gödel Machine：让自我改进 Agent 与评估器协同进化，论文写作接受率提升至1.78-1.86倍; OmniAct：分层异步架构统一具身Agent的网-物动作调度，百k交互下token消耗近平稳
- X讨论：SemiAnalysis：LeptonAI 创始人收购一年后离职，7 亿美元押注的 DGX Lepton 远未达预期; SemiAnalysis 警告 neocloud 商业模式脆弱，非 NVIDIA 客户难以为继; 百度 Unlimited-OCR 接入 vLLM，Reference Sliding Window 实现整书一次性解析; VLX-Seek视觉感知模型发布：3B参数在细粒度视觉理解基准上超越Google Gemini

---

## 📖 详细参考
### 产业动态
**福特重新雇佣资深工程师，承认 AI 未能替代制造环节经验**
- TechCrunch 报道，福特在引入 AI 与自动化质检系统后产品质量未达预期，决定**重新雇佣 350 名资深工程师**（"gray beard"）回归产线，部分为前员工、部分来自供应商。总裁 Kumar Galhotra 承认福特此前"越来越依赖自动化质检系统"却收效不佳，并指出生产制造中的隐性知识（tribal knowledge）难以被 AI 替代。
  > 💡 传统制造场景中AI落地的核心瓶颈是工艺know-how的隐性结构化，而非模型能力——车企需要建设'AI+老师傅'的混合工作流，而非纯AI替代。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/28/ford-rehires-gray-beard-engineers-after-ai-falls-short/)

**印度国家支付公司 CEO：AI 将深度参与下一代数字支付增长**
- TechCrunch 报道，印度国家支付公司（NPCI）CEO Dilip Asbe 表示，印度统一支付接口（UPI）日交易量已超 **7.5 亿笔**，目标是突破 **10 亿笔/日**，AI 将在下一阶段深度参与用户增长、反欺诈与信贷分发。他认为新一代 UPI 应用可借 AI 形成更具竞争力的商业模式。
  > 💡 新兴市场支付基础设施进入'AI增值'阶段，UPI的开放架构+AI能力可能成为印度本土支付公司对标Visa/Apple Pay的差异化抓手。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/27/indian-payments-chief-thinks-ai-will-be-heavily-involved-in-next-era-of-digital-payment-growth/)

**OpenRouter 持续运行 GPQA 与 TAU-Bench 对开源模型进行实时评测，据此动态调整 provider 路由**
- OpenRouter 推出 **Auto Exacto** 自适应质量路由，对带工具调用的请求默认开启：每约 **5 分钟**依据三类信号重新评估平台各 provider——生产流量吞吐量、工具调用遥测（自 2025 年 8 月累计数十亿次）与周期运行的 **TauBench Verified Airline / GPQA-Diamond** 两项基准，仅把统计离群的低质 provider 降权到队尾、保留原价格/延迟排序。相较旧的价格加权路由，头部模型工具调用错误率大幅下降：**GLM-5、GLM-4.7 分别降 88%、80%**（约 8% → 约 1%），gpt-oss-120b、DeepSeek V3.2 也有 16–36% 改善、TauBench 得分提升。OpenRouter 还发现 provider 间质量差异主要源于推理引擎的**工具调用解析器而非量化精度**（Novita 的 FP4 方案甚至跑赢部分 FP8 provider）。
  > 💡 第三方模型路由平台开始承担'持续 benchmark'职能——同一模型在不同 provider 上能力差异巨大，且主要源于推理引擎实现而非模型本身，意味着选 provider 比选模型更影响生产环境的 Agent 稳定性。
   - 来源: [@openrouter](https://x.com/OpenRouter/status/2071283228908896655#m) | [OpenRouter Blog](https://openrouter.ai/blog/announcements/auto-exacto/)

**Google因算力限制缩减Meta对Gemini模型的调用额度**
- The Information报道，Google数月前开始限制Meta对其Gemini AI模型的使用量，称无法满足这家社交媒体巨头所请求的全部算力。Meta此前在内部AI产品中接入Gemini API以补充自研模型的不足，此次额度收紧意味着Meta需要重新评估外部模型依赖度，并加快Llama系列自研投入。Google方面未公开受影响的调用规模与具体产品线。
  > 💡 Meta在自研模型之外仍重度依赖外部闭源API，反映出头部互联网公司在大模型供给端尚未完全自给，Google的算力配额成为行业博弈筹码。
   - 来源: [The Information](https://www.theinformation.com/briefings/google-put-limits-metas-use-gemini-due-capacity-constraints)

### 算力追踪
**华尔街押注美光成为下一个英伟达，AI驱动内存需求成核心逻辑**
- TechCrunch 报道，华尔街投资者认为总部位于爱达荷州博伊西的存储厂商美光（Micron）有望复制英伟达的股价表现，核心驱动力来自 AI 算力扩张对 HBM 等高带宽内存的强劲需求与内存芯片的供应紧缺。美光承诺已为长期布局以应对潜在的需求下滑或产能过剩，华尔街对此买账。报道未给出具体股价目标或估值数据。
  > 💡 市场叙事从'GPU稀缺'转向'HBM稀缺'，美光是否能真正复制英伟达取决于其HBM3E/HBM4在NVIDIA与AMD下一代GPU的导入份额，而非单纯的AI故事溢价。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/28/why-wall-street-thinks-us-memory-maker-micron-is-the-next-nvidia/)

**光本位科技联合东方天算启动全球首颗天基光计算卫星：单卡300 TOPS载荷已开展在轨试验**
- **光本位科技与东方天算**联合启动**全球首颗天基光计算卫星与全球首个天基光计算载荷研制**。光子不带电荷天然免疫宇宙高能粒子的单粒子翻转，光在波导传播几乎不产热，静态功耗趋近零——直接绕开传统电芯片在太空的辐射、散热、功耗三道工程坎。光本位科技是**全球唯一同时实现光子存内计算与玻璃基光计算**的公司，存内计算把模型参数直存芯片，计算延迟降至传统光计算方案的 **1/10**。双方联合研制的光电融合计算卡**单卡算力达 300 TOPS**，支持 INT8/FP8 多精度推理，已开展在轨环境试验验证；第二代卡计划今年内推出。宏观背景是 Musk 判断 **2032 年**太阳能驱动的太空 AI 卫星将成为全球成本最优算力方案，SpaceX 同期也正考虑收购光模块公司 **Mesh**。
  > 💡 电芯片在制程极限触顶、太空环境又把散热/功耗推到极致时，光计算从"实验室概念"切到"商业卫星载荷"是一次差异化突围；但天基光计算还需穿越火箭震动、太空辐射环境与在轨系统级三重工程验证，距规模商业部署仍很远。
   - 来源: [量子位](https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247900104&idx=1&sn=3b0889c74d995686a0a178fe84cebbb4)

### 初创&融资
**百度旗下 AI 芯片公司昆仑芯 IPO 路演中要求投资人购买其半导体产品**
- The Information 报道，由百度控股的 AI 芯片公司昆仑芯（Kunlunxin Technology）计划在**香港上市，目标估值约 500 亿美元**。路演期间，昆仑芯向潜在投资人推介其半导体产品，暗示希望 IPO 投资人在投资之外也成为芯片客户。昆仑芯是中国本土 AI 加速器厂商，主要对标 NVIDIA 推理芯片。
  > 💡 国内AI芯片公司IPO正演变为'资本绑定客户'的圈地运动——通过股东身份锁定出货量，以应对英伟达在推理侧的份额挤压。
   - 来源: [The Information](https://www.theinformation.com/articles/baidus-chip-unit-asked-ipo-investors-buy-semiconductors)

### 研究关注
**SciAtlas：浙大开源4300万论文级科研知识图谱，配套 CLI 与 Agent Skill 服务自动化科研**
- 浙大 zjunlp 团队开源 SciAtlas——面向自动化科研的大规模科学知识图谱（**4300 万篇论文与 30 亿知识三元组**），节点覆盖论文/作者/机构/会议/关键词/引用，并构建"领域→学科→子领域→主题"四级分类。团队同步发布 pip 可装的 CLI 客户端与托管 API，支持图感知检索、idea 生成/评估、综述、趋势分析等科研工作流，配套 Agent Skill 包可把检索能力迁移进 Codex、Claude Code，让知识图谱直接服务于科研 Agent 的"生成—评估"闭环。
  > 💡 把评估环节纳入科研Agent能力图谱，使AI科研能力从'能否生成像样论文'推进到'能否判断思路是否真正新颖'，这对未来AI辅助科研工作流的可靠性是更关键的指标。
   - 来源: [PaperWeekly](https://mp.weixin.qq.com/s?__biz=MzIwMTc4ODE0Mw==&mid=2247721282&idx=2&sn=a907e3a5c8bd8d81cb70c74713128f66) | [GitHub](https://github.com/zjunlp/SciAtlas) | [arXiv](https://arxiv.org/abs/2605.22878)

**Red Queen Gödel Machine：让自我改进 Agent 与评估器协同进化，论文写作接受率提升至1.78-1.86倍**
- 论文提出 Red Queen Gödel Machine（RQGM）递归自我改进框架，核心突破是把**评估器**纳入自我改进回路——以往自我改进 Agent 假设评估标准固定，RQGM 改用"受控效用进化"（epoch 内标准固定、epoch 之间可更新效用），在目标动态演化时仍保持自我改进保证。实验上：代码任务仅靠补充一个 agent-as-a-judge 评审信号就超过此前 SOTA 且更省 token；论文写作/评审与奥赛级证明写作/评分上，协同进化的写作者接受率达 **1.78–1.86 倍**提升、评分者 ground-truth 准确率高 **9%**；它还修正了最强基线评审对 AI 生成论文高达人类 **1.91 倍**的过度接受。第一作者 Alex Iacob，资深作者 Nicholas D. Lane。
  > 💡 把"评估器进化"与"Agent 进化"绑定，触及递归自我改进的核心难题——能力越强，静态基准越快失效；让评判标准与 Agent 同步演化是通向真正自我改进系统的关键一步，但也放大了"评估器与 Agent 共谋"的安全风险。
   - 来源: [arXiv](https://arxiv.org/abs/2606.26294)

**OmniAct：分层异步架构统一具身Agent的网-物动作调度，百k交互下token消耗近平稳**
- 复旦大学（邱锡鹏、姜育刚团队，第一作者 Junhao Shi）提出 OmniAct 框架，解决持续具身 Agent 统一调度"网络域"（API、IoT）与"物理域"（操作、导航）异构工具、并从长时物理故障自主恢复的问题。论文主张持久自主不需要单体大模型，而需**规划/记忆/验证分离的分层异步架构**：多模态语义规划器（统一动作空间内的技能路由）、基于事件边界压缩的分层记忆（**亚线性上下文增长**）、异步视觉抢占引擎（执行中闭合语义环）。在双机器人平台协同四个 IoT 设备的 **40 项真实长程任务**上，端到端成功率全复杂度级别均提升，累积 **10 万+** token 下消耗近平稳，并把中等规模开源模型提升到闭源专有水平。
  > 💡 "持久自主"被拆解为规划/记忆/验证解耦的工程架构而非堆叠更大模型——事件边界压缩让长程任务的上下文成本可控，异步视觉抢占补上开环 VLA 缺失的失败检测，是把具身 Agent 从"孤立技能演示"推向"日常物理自主"的关键拼图。
   - 来源: [arXiv](https://arxiv.org/abs/2606.27251)

### X讨论
**SemiAnalysis：LeptonAI 创始人收购一年后离职，7 亿美元押注的 DGX Lepton 远未达预期**
- SemiAnalysis 报道，LeptonAI 创始人兼 CEO（Caffe / ONNX / PyTorch 联合创作者贾扬清）在 NVIDIA 收购仅**一年后**离职。据悉 Jensen 当年斥资约 **7 亿美元**收购 LeptonAI，但整合产品 **DGX Lepton** 远未达预期、基本宣告失败。NVIDIA 曾承诺**到 2026 年开源 Lepton 核心软件平台**至今未兑现，SemiAnalysis 推测是 Jensen 改主意否决了开源——按惯常多期 vesting，CEO 一年后即走意味着放弃大量未归属股权（或当初谈下了特殊条款）。SemiAnalysis 指出这仅是 NVIDIA 一年来收购后被其文化"拖垮"的多家 ML 平台公司之一；背景是 agentic coding 兴起，可能直接取代这类平台原本要填补的位置。
  > 💡 收购 ≠ 能力整合：NVIDIA 的硬件公司文化与开源软件平台基因冲突，导致重金买下的人才与产品双双流失；而 agentic coding 的兴起又在需求侧挤压这类 ML 平台的生存空间。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2071337894321512734#m)

**SemiAnalysis 警告 neocloud 商业模式脆弱，非 NVIDIA 客户难以为继**
- SemiAnalysis 援引多位 neocloud 高管称，若其集群使用非 NVIDIA 网络设备、或对外提供 AMD GPU / TPU 算力，会感到遭到 NVIDIA 报复，报复手段包括**不给予早期 GPU 配额**以及**不再为其 IPO / VC 融资提供支持**。高管们认为 NVIDIA 借高压手段迫使 neocloud 保持 NVIDIA-only；该压力**不适用于 hyperscaler**（超大规模云厂商），因其议价能力更强、客户基础更多元。部分 neocloud 高管已开始考虑**悄悄上线 TPU 或 AMD GPU**，以规避 NVIDIA 的施压与报复感。
  > 💡 neocloud 的护城河本质是 NVIDIA 分销渠道而非独立算力供给——NVIDIA 以'早期配额 + 融资背书'作为绑定筹码，把非 NVIDIA 路线逼入灰色地带，CoreWeave、Lambda 等的估值与其对 NVIDIA 生态的绑定深度直接挂钩。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2071005688134881647#m)

**百度 Unlimited-OCR 接入 vLLM，Reference Sliding Window 实现整书一次性解析**
- vLLM 官方账号宣布百度 Unlimited-OCR 模型已可在 vLLM 推理框架运行，核心特性为通过 Reference Sliding Window（R-SWA）Attention 实现整本书籍一次性解析，并保持恒定 KV cache 占用。该模型总参数 **3B**、推理时激活参数约 **570M**，在 OmniDocBench v1.6 基准上取得 **93.92%** 的综合成绩。
  > 💡 长文档OCR的关键瓶颈从'模型能不能读'转移到'推理能不能省内存'——Reference Sliding Window类方法正在成为长上下文推理的事实标配。
   - 来源: [@vllm_project](https://x.com/vllm_project/status/2071116236591948227#m)

**VLX-Seek视觉感知模型发布：3B参数在细粒度视觉理解基准上超越Google Gemini**
- @OmAI_lab 在 X 上介绍 VLX 系列的 Day 2 模型 **VLX-Seek**，针对 VLM"看得懂图中有什么、却定位不准在哪"的短板：传统坐标生成（输出 [x1,y1,x2,y2]）脆弱、易出错与幻觉，VLX-Seek 改走**区域指代（region reference）**——检索候选区域转为语言可寻址 token（如 `<region_i>`），让模型直接选择区域而非生成坐标，任务覆盖检测、指代表达、计数、OCR 与具身交互。该系列 Day 1 的 **VLX-Flow**（HF blog）则面向流式视频理解，用双层记忆 + Linear Attention 增量维护状态、把视频从"请求式 API"变为端侧常驻感知。据 PaperWeekly，VLX-Seek 参数量 **3B**、在细粒度视觉感知基准上超过 Google Gemini 系列（此数据仅见于二手聚合，待核实）。
  > 💡 "区域指代替代坐标生成"与"流式持续理解"代表 VLM 演进的两条务实路径——前者把空间定位从"生成数字"改成"选择离散区域"绕开数值幻觉，后者把视频从"离线问答"改成"常驻状态"适配端侧，都是工程友好型的小模型打法。
   - 来源: [@OmAI_lab](https://x.com/OmAI_lab/status/2070755221295579402) | [HuggingFace Blog](https://huggingface.co/blog/omlab/vlx-flow) | [PaperWeekly](https://mp.weixin.qq.com/s?__biz=MzIwMTc4ODE0Mw==&mid=2247721282&idx=1&sn=743a9f0e74e36d8dc33f091018efe187)

---
*更新时间: 2026-06-29 06:47*