## 09月26-27日 AI 前沿动态

> 自动汇总 | 时间窗口: 48h (09-26 ~ 09-27) | 两日合并精选 13 条

---

## 要点汇总

- 产业动态：OpenRouter：Jev 在分类请求中份额跃升至 27%，接近 DeepSeek V4 Flash 两倍; Tesla Optimus 量产爬坡受阻，手部与供应链成主要瓶颈; OpenRouter 推出 Jev Router：按难度路由模型，四个智能体基准多解 82% 任务; Muju Earth 推出 Aeropod：无需机械与机器人的土壤自动通气方案
- 算力追踪：SemiAnalysis 发布中国数据中心模型，覆盖千家设施与东数西算布局
- 初创&融资：英国 AI 算力新云 Nscale 拿下 33.6 亿美元可转债融资，瞄准美股 IPO; 推理需求上涨，Fireworks AI 与 Fal 据传洽谈新一轮融资; 前 Tesla Dojo 团队创立的 DensityAI 估值逼近 100 亿美元; BigHat Biosciences 完成 7500 万美元 C 轮融资，加速 AI 设计抗体疗法
- 研究关注：论文提出 WROP 数据集：评估与训练视频模型的物体恒存性
- X讨论：OpenAI Jalapeno 团队在 NVIDIA 首席科学家 YouTube 评论区反驳其对推理芯片的误解; SemiAnalysis 拆解 DeepSeek V4.1 Flash 的 Engram 记忆门; Ginkgo Bioworks 取消 "Mike Versus the Machines" 人机蛋白设计对决

---

## 📖 详细参考

### 产业动态
**OpenRouter：Jev 在分类请求中份额跃升至 27%，接近 DeepSeek V4 Flash 两倍**
- OpenRouter 官方账号发文称，Jev 正在快速成为该平台分类请求的首选模型。该模型在该品类一周请求量中占据 27% 份额，约为此前居首的 DeepSeek V4 Flash 的两倍。
  > 💡 Jev 在分类这一轻量高频场景里占据近三成份额，意味着其低延迟与定价优势已经跑通了可观测的商业化用例，但能否外推到生成场景仍待验证。
   - 来源: [@openrouter](https://x.com/OpenRouter/status/2103915026205806610)

**Tesla Optimus 量产爬坡受阻，手部与供应链成主要瓶颈**
- Tesla 的人形机器人 Optimus 近期月产量较第二季度的小批量试产扩大约十倍，上月已能每周生产数百台，但产线在灵巧手部、自动化设备和供应商交付上持续遇到可靠性问题。管理层已向员工传达目标，要在年底前建成可周产千台以上的连续自动化产线，这一节奏仍远低于最终约周产 2 万台的长期规划。
  > 💡 十倍爬坡卡在灵巧手而非整体组装，提示人形机器人量产的真正瓶颈已从整机集成转向高自由度末端执行器与配套供应链；Tesla 能否在年底跨越千台/周门槛，是判断其能否在 2027 年逼近 2 万台/周目标的关键观察点。
   - 来源: [The Information](https://www.theinformation.com/articles/teslas-optimus-hits-snags-hands-suppliers-scale-up-begins)

**OpenRouter 推出 Jev Router：按难度路由模型，四个智能体基准多解 82% 任务**
- OpenRouter 发布 Jev Router，由 TypeSafe 首个决策模型 Jev 驱动：每轮对话前读取 prompt 并评估难度与精度需求，判断换更大模型、提高努力档位或用更便宜模型是否划算，只在预期收益大于成本（包括丢掉已缓存对话的代价）时才切换模型，会话内尽量保持同一模型。官方数据：在四个智能体基准上比自家 Auto Router **多解决 82% 的任务（423 题中 237 vs 130）**，在五个智能体基准上首 token 中位延迟快于所有参测路由器。Jev 以零数据保留（ZDR）条款运行，不存储不训练，附件不发送给 Jev，每次响应附带路由决策的理由与评分元数据。
  > 💡 路由器从「按消息挑模型」升级为「按难度与缓存成本做经济决策」，模型选择本身成了一个决策模型的活；把缓存丢失计入切换成本，说明推理经济学已精细到上下文复用层面。
   - 来源: [@openrouter](https://x.com/OpenRouter/status/2103610898690855161)

**Muju Earth 推出 Aeropod：无需机械与机器人的土壤自动通气方案**
- Muju Earth Technologies 推出 Aeropod，一种指甲盖大小、随种子一起播入土壤的通气装置，无需预先翻土或机器人作业。在温度、压力与湿度共同作用下，Aeropod 会裂开并疏松土壤、形成细小通道供空气、水与根系通过。公司称该方案可将农户翻土成本降低一半以上。公司已完成实验室测试，今年秋季将在英国启动付费田间试验，已招募九位农户并将三十余位列入候补名单，首批目标客户为英国的洋葱种植者。
  > 💡 Aeropod 走的是"无机器人替代农艺"路线，把传统依赖重机的环节压缩到一次性种子形态投放物，对小农户与单季作物敏感场景的减成本价值明显；但其长期效果与土壤修复回报仍依赖英国田间试验的后续披露。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/25/the-aeropod-automates-soil-aeration-without-robotics-see-it-at-techcrunch-disrupt)

### 算力追踪
**SemiAnalysis 发布中国数据中心模型，覆盖千家设施与东数西算布局**
- SemiAnalysis 上线中国数据中心模型，映射出 60 多家运营商运营的 1000 余座设施。文章强调国内算力以零售为先、由 AI 需求翻转，最大超大规模租户的租用量已达全国容量的五分之一，并实现 12 个月内 100MW 的快速部署，呼应东数西算框架。
  > 💡 该模型把分散的中国算力版图拼成统一坐标系，让全球投资者首次能按运营商、租户和电力时序对比中美算力增长；东数西算叠加 AI 需求，使得中国数据中心正从零售型 IDC 走向超大规模租赁市场。
   - 来源: [SemiAnalysis Newsletter](https://newsletter.semianalysis.com/p/the-chinese-ai-infrastructure-boom)

### 初创&融资
**英国 AI 算力新云 Nscale 拿下 33.6 亿美元可转债融资，瞄准美股 IPO**
- 英国新云厂商 Nscale 宣布在美股 IPO 前完成 33.6 亿美元可转债融资，由对冲基金 Third Point 领投。其中 23.6 亿美元立即到账，另有 10 亿美元来自现有投资人 NVIDIA，将于 11 月中旬到账。票据将在 IPO 完成时转换为股权。据《金融时报》报道，Nscale 在 NYSE 的 IPO 估值预计为 350 亿美元；据彭博报道，公司拟在发行中募集 30 亿美元。Nscale 已从澳大利亚加密矿企 Arkon Energy 分拆两年，IPO 文件显示其合同总额超过 1030 亿美元，目前在挪威与西弗吉尼亚等地建设多个大型数据中心园区。
  > 💡 可转债先于 IPO 入账，配合 NVIDIA 持续注资，体现 AI 算力新云仍极度依赖资本市场与上游芯片厂输血；巨额合同总额与估值落差也提示，IPO 定价将是检验 AI 算力赛道估值成色的关键节点。
   - 来源: [TechCrunch](https://techcrunch.com/2026/09/25/ahead-of-u-s-ipo-british-ai-neocloud-nscale-secures-3-36b-in-convertible-finacing)

**推理需求上涨，Fireworks AI 与 Fal 据传洽谈新一轮融资**
- 据报道，面向开发者提供 AI 模型与服务器访问的初创公司 Fal 与 Fireworks AI 因推理服务销售强劲，正在吸引新一轮投资。Fal 主营视频与图像生成模型的推理服务，已与投资人就新一轮融资进行洽谈，据三位知情人士透露，公司估值口径包括 150 亿美元，以及可能进一步上调至 170 亿至 200 亿美元。
  > 💡 推理基础设施正在取代训练侧成为新的资本焦点，Fal 与 Fireworks 的估值跳升说明视频/图像生成 API 已被视为继大模型 API 之后的下一个平台型入口，这对 vLLM、SGLang 等推理框架与 NVIDIA、AMD 的算力销售都具有二阶拉动效应。
   - 来源: [The Information](https://www.theinformation.com/articles/fireworks-fal-consider-new-rounds-inference-demand-soars)

**前 Tesla Dojo 团队创立的 DensityAI 估值逼近 100 亿美元**
- DensityAI 由 Tesla Dojo 超算项目前负责人创立，成立仅一年，估值已接近 100 亿美元，融资进入后期谈判阶段。公司方面已告诉潜在投资人，AWS 同意在芯片达到特定性能要求后采购其产品。报道同时指出公司芯片仍处于早期开发，距离大规模量产可能还需数年。
  > 💡 芯片未量产、客户承诺附带性能条件，估值却直接冲到 100 亿美元量级，典型靠团队履历与 AWS 兜底预期定价；但 AWS 这一有条件的采购协议能否真正落地，决定了这轮高估值是否会在两三年内被打折。
   - 来源: [The Information](https://www.theinformation.com/articles/startup-founded-ex-tesla-dojo-leaders-nears-10-billion-valuation)

**BigHat Biosciences 完成 7500 万美元 C 轮融资，加速 AI 设计抗体疗法**
- BigHat Biosciences 提供集成抗体表征实验室与机器学习的 AI 蛋白治疗设计平台，用于工程化改造具备更复杂功能与生物物理特性的分子。公司瞄准当下最难治疾病的安全、有效疗法开发。本轮 7500 万美元 C 轮融资由 PremjiInvest 与 DFJ 德丰杰（全球）联合领投，Section 32、Quadrille Capital、Intermountain Healthcare、GRIDS Capital、Discovery Ventures、Andreessen Horowitz-a16z、Alexandria Venture Investments、8VC、LG Technology Ventures、Catalio Capital Management、Merck Global Health Innovation Fund、礼来亚洲基金、Amgen Ventures 等机构参投。
  > 💡 本轮投资方同时覆盖一线科技 VC 与 Merck、Amgen、礼来亚洲基金、Intermountain Healthcare 等产业与医疗战略资本，说明 AI 抗体设计平台的下一道关卡不再是模型本身，而是与药企/医院在管线与临床数据上的深度对接。
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14705243)

### 研究关注
**论文提出 WROP 数据集：评估与训练视频模型的物体恒存性**
- 论文提出 WROP 数据基础设施，包含 150 个受认知科学启发的任务，划分为六个认知类目。论文同时发布 150 万样本训练语料与 300 题考试，并在考试上评测 14 个视频模型，其中 PWM-WROP 为 160 亿参数的世界模型。在盲测两两 Elo 对比中，PWM-WROP 在续写模型中排名第一、总排名第三，仅次于两个参考到视频模型。论文开源数据、考试、模型答卷、分数、权重以及基于 AWS Trainium2 的原生 PyTorch 训练栈 PWM。
  > 💡 把物体恒存性拆成可量化考试题，并开放权重与训练栈，相当于把"类人物理先验"做成可复现的基准，为后续视频世界模型在长时一致性与物理合理性上的比拼提供一个可对照的小型评测场。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2609.28654)

### X讨论
**OpenAI Jalapeno 团队在 NVIDIA 首席科学家 YouTube 评论区反驳其对推理芯片的误解**
- SemiAnalysis 注意到，OpenAI Jalapeno 负责人在 NVIDIA 首席科学家“计算机博物馆”对谈节目的 YouTube 评论区公开回应，针对 NVIDIA 首席科学家对 Jalapeno 项目的误解做出澄清。该回应指出，Jalapeno 已在 SemiAnalysis InferenceX 基准测试中完成演示，结果显示 Jalapeno 在非 OpenAI 模型上的推理速度已经超越 NVIDIA 的部分芯片产品（如 July Rubin），并以此反驳 NVIDIA 首席科学家对项目进度与定位的判断。
  > 💡 此次公开反驳把原本只面向技术圈的基准对比升级成 OpenAI 与 NVIDIA 双方在公开场合的“芯片性能口径”之争，InferenceX 被打造成可对外引用的第三方基准，使两家的推理硬件竞争从内部测试走向可被公众与客户直接对照的赛道。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2103922839812272220)

**SemiAnalysis 拆解 DeepSeek V4.1 Flash 的 Engram 记忆门**
- SemiAnalysis 在 X 平台发布对 DeepSeek V4.1 Flash 的探测结果。研究人员通过 Engram 门控观察该模型在不同文本模式上的激活情况，并以'逆转裁判：Wright'作为示例。初步结论显示模型调用的记忆模式远超人名与事实层面。
  > 💡 把 Engram 门控作为可解释性探针，意味着 DeepSeek 的稀疏记忆架构已经具备'外部可观测的路由信号'，这类信号对模型蒸馏、推理加速和对抗样本检测都有直接价值，也是少数能在工程层复现的'模型机理研究'。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2103681005261345264)

**Ginkgo Bioworks 取消 "Mike Versus the Machines" 人机蛋白设计对决**
- Ginkgo Bioworks CEO Jason Kelly 数月来筹划一场由顶级科学家对阵 OpenAI 模型的蛋白设计比赛，地点设在其波士顿总部一座 1.5 万平方英尺、配有机器人的自主实验室。比赛原定 9 月 14 日开战，对阵双方为斯坦福大学教授 Michael Jewett 与 OpenAI 的 AI 智能体，规则允许人类选手使用任意商用 AI 模型，OpenAI 则可调用尚未发布的更先进模型。赛事已被延期，原始的 "Mike Versus the Machines" 概念在恢复后被弃用。
  > 💡 这场被定位为 “生物学界 Kasparov 对 Deep Blue” 的公开对决在临近启动时被悄悄改写，反映出 AI 在真实生物学实验中替代人力仍存在不可控风险，主办方对外部传播叙事与赛事结果稳定性的权衡开始压过营销价值。
   - 来源: [The Information](https://www.theinformation.com/articles/inside-drama-behind-biology-contest-pits-openai-agents-humans)

---
*更新时间: 2026-09-27 21:30*
