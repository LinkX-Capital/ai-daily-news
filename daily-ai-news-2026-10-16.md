## 10月16日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 15 条

---

## 要点汇总

- 模型前沿：Meta 与 Apple 联手发布 Muse Spark Open：8160 亿参数开源权重模型，本地运行需至少 1TB 内存
- 产业动态：Agility Robotics 拉票：Digit 5 入围 Material Handling 2026 年度移动机器人读者选择; Agility Robotics：Digit 5 电池由 Nyobolt 提供，主打 90 分钟工作 / 9 分钟充电的 10:1 配比
- 算力追踪：台积电宣布在台南再建一座 3nm 工厂，目标 2028 年上半年投产; SK Hynix 旗下 Solidigm 拟以美国建厂换取向大连工厂增运芯片设备
- 初创&融资：报道称数据中心机柜设计初创 Mueon 融资 6500 万美元，主打同功耗下十倍算力; Ramp 完成 18.5 亿美元新融资估值 600 亿美元，四个月内估值由 440 亿跃升并全面押注 AI; 超导输电公司 Veir 完成 2490 万美元 A+ 轮融资，主打蒸发式低温冷却技术平台
- 研究关注：Glance Forcing：把双向扩散蒸馏改写成单样本单卡 1 小时可行，VBench 总分 84.04→84.22; Vela：用样条参数化把 VLA 动作输出从固定帧率改成连续轨迹，适配多构型与长程操作; Cortex：把上下文收益内化为参数更新，14B 模型在 50 次顺序编辑后恢复 88.9% 增益
- X讨论：Anthropic 据报披露第三季度营收 168 亿美元，环比增长约 45%; The Information：Anthropic 增速放缓可能压制其 IPO 估值预期; Artificial Analysis：英伟达 Nemotron 3.5 Super VL 成美国开源权重榜首，智能指数 26 分; SemiAnalysis：Google 首次提交 TPUv7 FP8 vLLM 推理成绩，每美元性能超 GB300 NVL72 FP4 达 1.67 倍

---

## 📖 详细参考

### 模型前沿
**Meta 与 Apple 联手发布 Muse Spark Open：8160 亿参数开源权重模型，本地运行需至少 1TB 内存**
- Meta 发布开源权重模型 Muse Spark Open，与 Apple 合作使其可在 Apple silicon 上本地运行。该模型采用 8160 亿参数与 100 万 token 上下文窗口，原生多模态，面向复杂编程与智能体任务。本地运行至少需要 1TB 内存，在搭载 M5 Ultra 芯片的 Mac Studio 上表现最佳。Meta 将该模型与自家 AI 编程终端 Muse Code 配对，用于修复 Mastodon 客户端 bug、添加新功能并完成完整构建，还在 DaVinci Resolve 中执行视频审阅与裁剪。
  > 💡 Muse Spark Open 进一步把前端旗舰的开源权重版推向桌面端，强调本地推理与硬件协同，是 Meta 在终端侧 AI 与开发者工作流上的双线推进。
   - 来源: [TechCrunch](https://techcrunch.com/2026/10/15/meta-launches-an-open-weight-model-that-runs-on-macs)

### 产业动态
**Agility Robotics 拉票：Digit 5 入围 Material Handling 2026 年度移动机器人读者选择**
- Agility Robotics 官方账号发文称 Material Handling 2026 年度移动机器人读者选择投票仍在进行，Digit 5 进入候选名单。Digit 5 以协作安全为设计核心，被定位为可在人员近旁工作的产品。官方同时附上投票入口与介绍链接。
  > 💡 投票本身不构成销量或客户承诺，但与 Agility 同步推进的借壳上市进程放在一起看，是把 Digit 5 持续推向工业采购视野的市场动作。
   - 来源: [@agilityrobotics](https://x.com/agilityrobotics/status/2110789047677509854)

**Agility Robotics：Digit 5 电池由 Nyobolt 提供，主打 90 分钟工作 / 9 分钟充电的 10:1 配比**
- Agility Robotics 官方账号发文介绍 Digit 5 的电池来自 Nyobolt 的超快充技术，设计目标为 10:1 工作与充电比，每天可工作超过 20 小时。官方同时放出 90 分钟工作与 9 分钟充电的对比数字，并附上详细介绍链接。
  > 💡 把运行/充电比拉到 10:1 并把 24 小时内可工作小时数作为卖点，本质是把人形机器人从「演示设备」推进到「班次化运行设备」；这类规格只有在真实客户现场跑过班次才会被验证，硬件演示与落地效果之间仍存在距离。
   - 来源: [@agilityrobotics](https://x.com/agilityrobotics/status/2110800374793699601)

### 算力追踪
**台积电宣布在台南再建一座 3nm 工厂，目标 2028 年上半年投产**
- 台积电于周四宣布将在台湾台南新建一座 3nm 芯片工厂，量产时间定在 2028 年上半年。首席执行官魏哲家表示，强劲的客户需求是公司在已规划 3nm 工厂之外再添新厂的原因。此举释放出对 AI 芯片需求将持续多年的信心信号。
  > 💡 在 3nm 节点上再加产能，意味着台积电把 AI 加速器的长期需求作为既定前提来投资，同时也在用新增产能锁定头部客户的设计订单。
   - 来源: [The Information](https://www.theinformation.com/briefings/tsmc-add-new-3nm-fab-ai-orders-pile)

**SK Hynix 旗下 Solidigm 拟以美国建厂换取向大连工厂增运芯片设备**
- 据 Reuters 报道，SK Hynix 旗下闪存子公司 Solidigm 正寻求美国批准，向其中国大连工厂运送更多芯片制造设备，条件是继续在美国建设新的 NAND 闪存工厂，潜在选址包括纽约州北部。SK Hynix 向 TechCrunch 表示，公司并未寻求扩大 2023 年完工的大连 Mod B 工厂产能，相关设备安装是在美国政府授权与协商下进行的。美国自 2022 年 10 月起以国家安全为由对先进芯片及制造设备对华出口实施限制，并在此后多次收紧。受 AI 数据中心需求激增影响，TrendForce 预计第四季度 NAND 价格将上涨 15% 至 20%。
  > 💡 Solidigm 用美国本土产能投资换取对华设备许可，是在中美出口管制框架下把扩产与合规做交易的典型样本，也反映出 NAND 紧缺使企业更有筹码推动政策松动。
   - 来源: [TechCrunch](https://techcrunch.com/2026/10/15/sk-hynix-bargains-for-chip-equipment-exports-to-its-china-facility-in-return-for-building-a-factory-in-us)

### 初创&融资
**报道称数据中心机柜设计初创 Mueon 融资 6500 万美元，主打同功耗下十倍算力**
- 据报道，位于波特兰的初创公司 Mueon 融资 6500 万美元，用于开发一种新的 AI 服务器机柜组件布局方式。公司表示，其设计可在同等功耗下将计算容量提升至现有数据中心方案的十倍。此轮融资由 Maverick Silicon 领投，Intel Capital 与 Wellington 参投。
  > 💡 电力已成为 AI 数据中心的硬约束，围绕机柜层面的物理与散热创新开始成为缓解这一瓶颈的高价值赛道。
   - 来源: [The Information](https://www.theinformation.com/briefings/exclusive-mueon-raises-65-million-rework-data-centers-put-together)

**Ramp 完成 18.5 亿美元新融资估值 600 亿美元，四个月内估值由 440 亿跃升并全面押注 AI**
- 支出管理公司 Ramp 周四宣布完成 18.5 亿美元新融资，估值达 600 亿美元，由 Dragoneer、Thrive Capital、Founders Fund、Sands Capital 与 Avenir Growth 联合领投。公司年化收入已突破 20 亿美元，年化采购处理量超过 2750 亿美元，客户数从 6 月的 7 万家增至 8.5 万家，包括 Visa、Uber、Shopify、Robinhood、Anduril、Notion、Cursor 和 Figma。Ramp 已从支出管理扩展至支付、反欺诈、采购、供应商管理乃至会计，近期还在产品中嵌入 AI 智能体，并推出面向 AI 智能体使用的企业信用卡，8 月进入模型路由业务。本月早些时候，Ramp 上线 Glass 工作空间，用于沉淀员工构建的 AI 自动化与提示词。
  > 💡 Ramp 把金融 SaaS 升级为 AI 原生操作平台，从支出管理延伸至 token 监控、模型路由与智能体信用卡，意在抢占企业 AI 工作流的钱包入口。
   - 来源: [TechCrunch](https://techcrunch.com/2026/10/15/ramp-reaches-60b-valuation-as-it-pushes-deeper-into-ai)

**超导输电公司 Veir 完成 2490 万美元 A+ 轮融资，主打蒸发式低温冷却技术平台**
- 美国蒸发式低温冷却技术平台 Veir 完成 2490 万美元 A+ 轮融资，投资方包括 VXI Capital、Galvanize Climate Solutions、Fidelity Investments、Congruent Ventures、The Engine 与 Breakthrough Energy Ventures。Veir 开发了基于高温超导体（HTS）的电力传输方法，能够以较小通行权在较低电压下传输更多电力，把成本最低的可再生资源连接到负荷中心。
  > 💡 Veir 用 HTS 把可再生能源输电瓶颈下移到低压低成本侧，是 AI 数据中心选址与绿电长距离输送的关键基础设施型创新。
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14706069)

### 研究关注
**Glance Forcing：把双向扩散蒸馏改写成单样本单卡 1 小时可行，VBench 总分 84.04→84.22**
- 论文指出当前自回归视频生成的主流方案是把双向扩散模型蒸馏成少步学生，但离线 PF-ODE 轨迹代价动辄数万 GPU 小时与 TB 级存储。论文提出 Glance Forcing，把去噪轨迹拆分成慢专家与快专家两条互补分支并配以分阶段目标，教师模型全程冻结。论文显示仅用一条 PF-ODE 轨迹即可把 VBench 总分从 84.04 提到 84.22，轨迹采集开销从数千 GPU 小时降到约 1 个 A100-GPU 小时。论文同时指出 PF-ODE 蒸馏主要负责把少步轨迹拉直，分布匹配阶段独立决定最终分布质量。
  > 💡 把高噪声语义布局与低噪声纹理细节交给不同专家解耦，相当于承认双向扩散向自回归蒸馏的损失景观不是单一可优化问题；这一拆分让「单轨迹 + 极少 GPU」成为可行起点，但语义与纹理的解耦是否会被极端压缩或长视频时序反向冲击，仍需后续验证。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.20220)

**Vela：用样条参数化把 VLA 动作输出从固定帧率改成连续轨迹，适配多构型与长程操作**
- 论文指出多数视觉-语言-动作模型把未来动作表示成固定帧率的动作块，时间分辨率与预测长度被同一输出预算绑死。论文提出 Vela，把机器人未来行为表示为连续轨迹，由紧凑样条动作表征与随运动变化的时间支撑组成，并配合多构型共享动作接口。论文在 LIBERO-X、EBench 与蛋饼烹饪、土豆切丝两项真实长程任务上验证，取得了仿真与真实操作的初步结果。论文认为连续动作表征可作为未来具身基础模型的基础。
  > 💡 把动作空间从离散帧重写成样条，本质上是把「时间分辨率与覆盖长度」的耦合砍掉，让同一输出预算在不同任务里自动调节粒度；该路径对接触密集型操作更友好，但也意味着评估体系与基线都得换一套可比口径。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.05230)

**Cortex：把上下文收益内化为参数更新，14B 模型在 50 次顺序编辑后恢复 88.9% 增益**
- 论文指出大语言模型从上下文中获得的性能增益往往在上下文移除后随之消失，并把这一现象形式化为 Memory Consolidation，目标是在保留非目标能力的前提下把上下文指定编辑、技能学习与行为引导统一起来。论文提出 Cortex，会先生成前瞻查询来预判上下文用途，再把上下文条件输出蒸馏为可合并的低秩或结构化 FFN 更新。论文覆盖 4B–120B 的稠密与 MoE 主干，并同时测试纯文本与多模态模型。在 14B 模型上完成 50 次顺序事实编辑后，Cortex-Structural 恢复了 88.9% 的上下文诱导增益，同时保留 99.8% 的原始非目标性能。
  > 💡 用前瞻查询 + 结构化 FFN 更新替代 RAG 等外挂手段，相当于把「即时上下文」折算成「可合并的参数补丁」，对顺序编辑与技能累积场景尤其有价值，但批量与顺序设置下的增益稳定性仍要看更长链条与更大模型的复现。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2610.20399)

### X讨论
**Anthropic 据报披露第三季度营收 168 亿美元，环比增长约 45%**
- 据知情人士透露，Anthropic 周三在 IPO 前路演中向潜在投资者披露，公司第三季度营收达 168 亿美元，环比增长约 45%。这一数字是 Anthropic 2025 年全年营收的 3.6 倍以上，但增速较第二季度有所放缓。
  > 💡 营收仍在高速增长，但环比增速从第二季度的 140% 级大幅回落，意味着 Claude Code 带来的爆发性需求开始回归到更可持续但更平淡的轨道上。
   - 来源: [The Information](https://www.theinformation.com/briefings/anthropic-reports-16-8-billion-third-quarter-revenue)

**The Information：Anthropic 增速放缓可能压制其 IPO 估值预期**
- 据报道，Anthropic 周三在旧金山与潜在投资者会面时透露，第三季度营收 168 亿美元、环比增长约 45%，但增速已低于第二季度由 Claude Code 需求拉动的 140% 以上水平。部分到场投资者预计，估值目标可能因此需要有所控制。
  > 💡 市场对前沿模型公司的估值越来越依赖增速曲线，Anthropic 仍能讲规模故事，但要维持超高估值，增速放缓本身就会成为定价的阻力。
   - 来源: [The Information](https://www.theinformation.com/articles/anthropics-rapid-slowing-growth-weigh-ipo-valuation)

**Artificial Analysis：英伟达 Nemotron 3.5 Super VL 成美国开源权重榜首，智能指数 26 分**
- Artificial Analysis 表示，英伟达的 Nemotron 3.5 Super VL 以 26 分登顶该机构智能指数，成为当前最强的美国开源权重模型。相较前代 Nemotron 3 Super 的 13 分，新模型智能翻倍，且每任务输出 tokens 量减少约 60%。同期发布的 Nemotron 3.5 Bolt 74B-A9B 24GB 是 Bolt 系列首款模型，智能指数为 21 分。
  > 💡 Nemotron 3.5 Super VL 用更少输出换更高智能，是推理效率路线的一次集中展示，但领先位置需要持续更新才能稳住美国开源榜首的叙事。
   - 来源: [@artificialanlys](https://x.com/ArtificialAnlys/status/2110760441240752399)

**SemiAnalysis：Google 首次提交 TPUv7 FP8 vLLM 推理成绩，每美元性能超 GB300 NVL72 FP4 达 1.67 倍**
- SemiAnalysis 称 Google 已向其智能体推理基准（Agentic Inference Benchmark）提交首批 TPUv7 FP8 vLLM 成绩。结果显示，TPUv7 FP8 每美元性能较 GB300 NVL72 FP4 高出 1.67 倍。SemiAnalysis 认为这表明 Google 正加速把 TPU 的能力对外开放。
  > 💡 TPU 首次在外部基准上以 FP8 精度跑出优于英伟达旗舰 FP4 的性价比，标志 Google 自研加速器开始正式进入外部推理市场的竞争视野。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2110560412907262343)


---
*更新时间: 2026-10-16 06:47*