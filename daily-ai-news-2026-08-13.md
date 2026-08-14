## 08月13日 AI 前沿动态

> 自动汇总 | 近 24h 为主 | 全局精选 21 条

---

## 要点汇总

- 模型前沿：xAI 发布 Grok 4.6，强化长链路 agent 与 coding benchmark; DeepSeek V4 Pro 0813 上线，四项智能体基准较预览版大幅提升
- 产业动态：Anthropic 将 Claude in Chrome 扩至所有付费计划; Sakana Chat 接入 Fugu 与新一代 Namazu，支持代码执行和成果物预览; Northrop Grumman 的 MEV 从 Optus 卫星脱离，为后续机器人延寿任务让位; Google 发布 Pixel 11 系列并扩大 Gemini 硬件集成; 腾讯二季度资本开支同比增长 176% 至 528 亿元
- 初创&融资：Lovable 完成 4 亿美元 C 轮，估值升至 133 亿美元; Cognition 据报洽谈 400 亿美元估值新融资; Blacksmith 估值升至 5.5 亿美元，AI 编程带动软件验证需求; Form Energy 融资 7.5 亿美元扩产铁-空气 100 小时长时储能; OpenAI 参股的 Thrive Holdings 获得超 20 亿美元新资本，估值 120 亿美元
- 研究关注：U-OPSD：无需外部监督的在线策略自蒸馏方法; ComBodied Agents 提出以人的状态轨迹为核心的人本智能体框架; Latent-to-4D 绕过 RGB，直接从视频潜变量生成 4D 世界; Stealing Reasoning Traces 揭示专有 LLM API 加密推理块泄漏风险; OEO 重新检验自演化 Agent 是否需要预设优化管线
- X讨论：Dyna 自报在 100 万小时人类视频训练中观察到 world-action model scaling 趋势; Peter Walker 称 OpenRouter 7 月平均每 10 小时上线一个新模型; Unitree 称仿生双足人形机器人累计生产下线约 1.8 万台; Jonathan Hurst：机械硬件是实现物理 AI 的关键前提

---

## 📖 详细参考

### 模型前沿
**xAI 发布 Grok 4.6，强化长链路 agent 与 coding benchmark**
- xAI 发布 Grok 4.6，称该模型在 Grok 4.5 基础上强化长时间运行的 agent、交互式工作和视觉任务，可跨多个步骤进行研究、信息分析、代码库操作和应用生成。xAI 在发布页列出的评测结果显示，Grok 4.6 在 AA Intelligence Index 得分 **61**，GDPVal-AA v2 为 **1753**，CursorBench v3.2 为 **69.9%**，DeepSWE v1.1 为 **65.9%**，FrontierCode v1.1 Extended 为 **61.3%**。模型已在 Cursor、Grok Build、xAI API 以及 OpenRouter、Vercel、Cloudflare 等合作方开放，API 起价为每百万输入 token **2 美元**、输出 token **6 美元**。
  > 💡 Grok 4.6 的发布重点不是单纯聊天能力，而是把 coding、知识工作和长链路 agent 任务作为 xAI 模型竞争的主战场。
   - 来源: [@SpaceXAI](https://x.com/SpaceXAI/status/2087562800982077492) | [xAI](https://x.ai/news/grok-4-6)

**DeepSeek V4 Pro 0813 上线，四项智能体基准较预览版大幅提升**
- OpenRouter 上线 DeepSeek V4 Pro 0813，并在发布帖中转述 DeepSeek 厂商自报、尚未独立验证的测试结果：相较 V4 Pro Preview，新版在 **DeepSWE** 得分 **62.7（+49.9）**、**CyberGym** 得分 **83.3（+30.6）**、**NL2Repo** 得分 **61.5（+23.0）**、**Terminal Bench 2.1** 得分 **87.9（+15.8）**，括号内为较预览版增加的绝对分值。OpenRouter 页面将其列为 DeepSeek V4 Pro 的正式版本，支持 **100 万 token** 上下文窗口，标注的输入/输出价格为每百万 token **0.435 美元 / 0.87 美元**。
  > 💡 四项 Agent 任务同步提升，显示 V4 Pro 0813 的升级重点在 coding、网络安全、代码库生成与终端操作等可执行任务；不过这些数据由 DeepSeek 报告并经 OpenRouter 转述，仍待独立评测验证。
   - 来源: [@OpenRouter](https://x.com/OpenRouter/status/2087579472380018792) | [OpenRouter](https://openrouter.ai/deepseek/deepseek-v4-pro-0813)

### 产业动态
**Anthropic 将 Claude in Chrome 扩至所有付费计划**
- Anthropic 扩大 Claude in Chrome 的开放范围，目前面向所有付费计划提供，Chrome 扩展本身仍处于 beta。它可以读取用户已登录的网页，并执行点击、输入和表单填写。官方展示的能力包括从分析仪表盘提取指标、整理 Google Drive 文件、基于日历和邮件准备会议、抓取竞品网站并生成对比材料，以及将销售电话记录到 CRM。用户可按站点授权，Team 和 Enterprise 管理员可设置组织级开关、allowlist 与 blocklist；Anthropic 也建议避免将其用于银行、健康记录和密码管理等敏感流程。
  > 💡 浏览器代理把“可登录网页”纳入 AI 自动化范围，但产品能否规模化取决于权限、确认机制和 prompt injection 防护是否足够可靠。
   - 来源: [@Claude](https://x.com/claudeai/status/2087635262390026525) | [Claude](https://claude.com/claude-in-chrome)

**Sakana Chat 接入 Fugu 与新一代 Namazu，支持代码执行和成果物预览**
- Sakana AI 更新 Sakana Chat，新增 orchestrator 模型 Sakana Fugu，并把 Sakana Namazu 升级到新一代；官方称 Fugu 在复杂指令理解和多步骤任务上可发挥作用，Namazu 则提升了日语响应质量和 agentic execution 能力。Sakana Chat 同时加入沙盒 Python 代码执行，支持计算、数据处理和文件生成，生成的 HTML、Word、幻灯片等成果物可在右侧面板预览并下载。更新还支持图片、PDF 和 Office 文档附件，用户可从本地文件开始进行总结、分析或重组。
  > 💡 Sakana Chat 正从“模型试用入口”升级为面向日本语境的轻量 agent 工作台，代码执行和文件附件是从聊天走向交付物的关键一步。
   - 来源: [Sakana AI](https://sakana.ai/chat-update/)

**Northrop 的 MEV 脱离 Optus 卫星，为机器人延寿任务让位**
- Northrop Grumman 建造并运行的 Mission Extension Vehicle（MEV）本周从澳大利亚 Optus 运营的通信卫星上脱离；此前它已驻留一年多并帮助卫星维持轨道。7 月 21 日，Mission Robotic Vehicle（MRV）和三个模块化推进舱 Mission Extension Pod（MEP）随 SpaceX Falcon 9 入轨。MRV 搭载 DARPA 主导开发的双机械臂机器人载荷，计划于 2027 年把一枚 MEP 安装到这颗 2009 年发射、设计寿命 15 年的 Optus 卫星上，预计再延寿约六年。
  > 💡 通过机器人安装模块化推进舱，可把一次性延寿服务扩展为可重复的在轨服务模式。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/12/northrops-robot-space-mechanic-is-a-new-way-to-keep-satellites-at-work-longer/) | [DARPA](https://www.darpa.mil/news/2026/robotic-servicing-geosynchronous-satellites-lifts-off) | [Northrop Grumman](https://www.northropgrumman.com/what-we-do/space/space-logistics-services)

**Google 发布 Pixel 11 系列并扩大 Gemini 硬件集成**
- Made by Google 2026 汇总了新一代 Pixel 设备动态，覆盖 Pixel 11、Pixel 11 Pro Fold、Pixel Watch 5、Pixel Tag 和 Pixel Buds 等硬件，并把 Gemini app 的更多集成列为本次更新的一部分。Pixel Buds 相关内容主要涉及既有 Buds Pro 2 和 Buds 2a 的新配色及功能更新，并非发布全新一代耳机。
  > 💡 Google 的 AI 分发正在从 app 和搜索框继续下沉到手机、手表、耳机与配件，硬件入口成为 Gemini 日常使用频次的放大器。
   - 来源: [Google Blog](https://blog.google/products-and-platforms/devices/pixel/made-by-google-2026/)

**腾讯二季度资本开支同比增长 176% 至 528 亿元**
- 腾讯控股第二季度资本开支达 528 亿元人民币（约 78 亿美元），同比增长 **176%**，即约为上年同期的 2.76 倍。公司披露，资本开支主要包括 IT 基础设施、数据中心等投资；另有计入经营现金流的 AI 相关预付款，用于支持 Hy 模型升级、WorkBuddy 和 CodeBuddy 推理、微信 AI 项目，以及外部云服务需求。
  > 💡 腾讯正在同时加大模型、应用和云端算力投入，但这些投入的回报结构仍需后续业绩验证。
   - 来源: [The Information](https://www.theinformation.com/briefings/tencents-capex-nearly-triples-compute-ai-models-tools)

### 初创&融资
**Lovable 完成 4 亿美元 C 轮，估值升至 133 亿美元**
- 欧洲 vibe-coding 创业公司 Lovable 宣布完成 4 亿美元 C 轮融资，估值 133 亿美元，由 Menlo Ventures 领投、Scaleup Europe Fund 共同领投。Lovable 自述 6 月年化营收运行率达到 5 亿美元，平台已托管 6000 万个项目，Lovable 所建应用月访问量超过 9 亿次。公司 6 月与 Google Cloud 签订多年合作；据 TechCrunch 此前援引知情人士，相关云端使用规模拟增至此前五倍。
  > 💡 融资与使用规模显示资本仍看好 AI 应用开发平台，但估值能否持续仍取决于收入质量和留存表现。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/12/lovable-confirms-new-13-3b-valuation-raises-another-400m/)

**Cognition 据报洽谈 400 亿美元估值新融资**
- 据 TechCrunch 转述 Bloomberg 援引的知情人士，AI 编程公司 Cognition 正初步洽谈新一轮融资；若年化营收运行率达到 10 亿美元，估值可能至少为 **400 亿美元**，但条款仍可能变化。公司今年 5 月刚完成逾 **10 亿美元** 融资，当时投后估值约 **260 亿美元**。
  > 💡 若新融资落地，Cognition 的估值将在数月内再次上调；目前仍应把它视为融资洽谈，而非已完成交易。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/12/ai-coding-startup-cognition-reportedly-already-in-talks-to-raise-at-40b-valuation/)

**Blacksmith 估值升至 5.5 亿美元，AI 编程带动软件验证需求**
- AI 代码测试创业公司 Blacksmith 完成 **4500 万美元 B 轮融资**，估值达到 **5.5 亿美元**；估值由上一轮约 6000 万美元升至 5.5 亿美元，约为此前的 9.2 倍。公司从 CI 工作负载扩展到自动修复失败代码检查的工具，押注 AI coding 增加代码产出后带来的验证需求。
  > 💡 当 AI coding 提高代码产出速度后，验证、测试和发布前质量控制会成为新的瓶颈，Blacksmith 的融资热度反映了这一配套层的价值重估。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/12/blacksmiths-valuation-jumps-10x-to-550m-as-ai-coding-fuels-software-validation/)

**Form Energy 融资 7.5 亿美元扩产铁-空气 100 小时长时储能**
- Form Energy 宣布完成 **7.5 亿美元 G 轮融资**，用于扩大其位于西弗吉尼亚州的 100 小时铁-空气电池制造能力并推进商业部署。与 Google 明尼苏达州数据中心相关的 Xcel Energy 供电方案拟纳入 **300MW/30GWh** 的 Form Energy 电池；Crusoe 3 月签署了 **12GWh** 战略产能协议；FuturEnergy Ireland 另与 Form Energy 签署了联合部署 **10MW/1GWh** 系统的协议。
  > 💡 这些项目显示，AI 数据中心的连续供电需求正在拉动长时储能订单，但项目审批、交付和实际部署仍需持续观察。
   - 来源: [Form Energy](https://formenergy.com/form-energy-secures-750m-in-series-g-financing/) | [Xcel Energy](https://newsroom.xcelenergy.com/news/xcel-energy-to-power-new-google-data-center-in-minnesota) | [Crusoe 协议](https://formenergy.com/form-energy-crusoe-announce-agreement-for-12-gigawatt-hours-of-iron-air-batteries-for-ai-data-centers/) | [FuturEnergy Ireland 协议](https://formenergy.com/form-energy-and-futurenergy-ireland-announce-agreement-to-deploy-first-iron-air-battery-storage-project-in-ireland/)

**OpenAI 参股的 Thrive Holdings 获得超 20 亿美元新资本，估值 120 亿美元**
- Thrive Holdings 宣布获得超过 20 亿美元新资本，估值 120 亿美元，新增外部投资者包括 D1 Capital Partners、Altimeter Capital 和 SoftBank Group。公司将自身定义为长期收购并运营企业的永久资本载体，重点把 AI 引入会计和 IT 服务等行业。公司称其目前拥有并运营 70 余家企业；据 TechCrunch，旗下 Current 会计业务包含 50 多家公司和 2000 多名专业人士，另有 IT 服务业务 Shield。
  > 💡 私募资本与模型厂商合作实施 AI 正成为一种新模式，但其规模化效果仍取决于被投企业的实际效率改善。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/12/openai-backed-thrive-holdings-raises-2b-to-bring-ai-to-the-enterprise)

### 研究关注
**U-OPSD：无需外部监督的在线策略自蒸馏方法**
- 论文提出无监督在线策略自蒸馏方法 U-OPSD，仅依赖模型自身生成结果，通过自一致性阈值进行多数投票构造伪解，并对与多数伪答案不一致的完成项进行蒸馏。在 AIME24、AIME25、HMMT25、MATH500、AMC23 五个数学推理基准上，作者报告 U-OPSD 在 Qwen3 non-thinking 模式的 4B 与 8B 规模下，五项平均分较基座分别提高 8.5 与 10.7 分，较 OPSD 分别高 3.2 与 2.3 分；thinking 模式下较 GRPO 分别高 0.7 与 1.1 分。
  > 💡 U-OPSD 减少了对 ground truth、外部反馈或更大模型的依赖，但论文仅在 Qwen3 与竞赛数学任务上验证，扩展性仍待更多实验确认。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2608.06296) | [arXiv](https://arxiv.org/abs/2608.06296)

**ComBodied Agents 提出以人的状态轨迹为核心的人本智能体框架**
- 论文提出 Combodied Agents，认为 Digital Agents 主要围绕数字状态转换组织，Embodied Agents 主要围绕物理状态转换组织，但两类范式均未将人的演变状态与自主性作为建模、干预和评估的首要对象。作者将 personal assistants、health agents、AI companions 与 adaptive human-AI systems 的分散能力归纳为一个闭环。多模态感知重构有关个人事件的证据，长期可校正记忆提供时间上下文，Personal World Models 估计不同决策和干预下的未来个人状态，再由 consent、uncertainty、safety、reversibility 和 user control 约束下的 intervention policy 选择支持方式。
  > 💡 这篇论文把 agent 叙事从“替人执行任务”推进到“围绕人的状态轨迹做闭环支持”，对 health agent、personal assistant 和 companion AI 的定义都更往前了一步。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2608.10915) | [arXiv](https://arxiv.org/abs/2608.10915)

**Latent-to-4D 绕过 RGB，直接从视频潜变量生成 4D 世界**
- 论文提出 direct latent-to-4D generation，利用共享 VAE 的视频模型最终去噪 latent 作为可复用接口，直接对接预训练 4D decoder 的 token grid，并通过 frame-wise 和 global spatiotemporal attention 进行 refinement。在预训练 4RC 初始化和多阶段几何监督基础上，Latent-to-4D 的最终训练阶段使用 **1,143** 个现有 reconstruction clips；单一 checkpoint 可在共享同一 VAE 的两个文生视频 DiT 和一个图生视频 DiT 上无需再调优即可使用。在 Text4D-200 与 I4D-200 上，相比同 latent 的 Wan+4RC cascade，projection-based DINO-F1 分别提升 **2.88-3.45** 和 **5.81** 分；该指标是投影层面的几何一致性与完整性代理，并非 4D 几何精度测量。
  > 💡 4D 生成的关键可能不再是从 RGB 重新回推，而是把 video latent 直接变成可迁移的几何接口。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2608.10744) | [arXiv](https://arxiv.org/abs/2608.10744)

**Stealing Reasoning Traces 揭示专有 LLM API 加密推理块泄漏风险**
- 论文指出，部分大模型服务会把隐藏的 chain-of-thought 作为加密文本块返回客户端，并在后续请求中由客户端回传。作者测试 2026 年 7 月初的 API 后报告，这些加密块当时可在同一提供商生态内跨会话、用户和模型互换，并可借较弱模型解码更强模型的 reasoning trace；测试覆盖 Anthropic、OpenAI 和 Google。作者还报告从公开仓库的 **315,320** 个 reasoning blocks 中识别出 **367** 个 PII artifacts 和 **182** 个 credentials，但同时说明无法取得隐藏推理的明文真值，因此不能完全验证全部解码内容，这次公开轨迹扫描也并非穷尽审计。论文注明，负责任披露后厂商已采取缓解措施，截至 8 月原攻击已不可复现。
  > 💡 推理过程不只是模型质量资产，也会变成隐私、蒸馏和隐形 prompt injection 的攻击面；API 协议层设计比单次输出审查更关键。
   - 来源: [arXiv](https://arxiv.org/abs/2608.09867)

**OEO 重新检验自演化 Agent 是否需要预设优化管线**
- Hui Xue 和 Fan Yang 在 arXiv 论文中提出 Open-Ended Optimization（OEO），在目标、允许交互、资源预算、数据边界和评测固定的前提下，让 frontier model 在线组合优化流程，而不是使用预设 pipeline。在该次预印本实验中，三种方法的优化器侧调用均使用 GPT-5.5；OEO 在 8 组对 SkillOpt 和 6 组对 GEPA 的 confirmatory head-to-head 比较中取得 **12 胜、1 平、1 负**，唯一一次落后 **0.21 个百分点**，且每个报告分数仅对应一次完整优化运行。OEO 的中位目标模型交互 token 为 SkillOpt 设定预算的 **34.3%**，这不等同于总 token 或总成本；论文还在 SearchQA 和 LiveMath 两个能力阶梯任务上发现，中等优化器下 SkillOpt 优于 OEO，弱优化器无法通过未改动的 OEO 接口运作。
  > 💡 自演化 Agent 的流程设计可能从“人工写死优化管线”转向“强模型自行组织改进路径”，但这种转变依赖优化器模型本身的能力阈值。
   - 来源: [arXiv](https://arxiv.org/abs/2608.09629)

### X讨论
**Dyna 自报在 100 万小时人类视频训练中观察到 world-action model scaling 趋势**
- Dyna Robotics 发布机构研究文章，称 Dyna-2 预训练于 **100 万小时以上**、主要为头戴式第一视角的人类操作视频；数据规模按 **1,000 / 10,000 / 100,000 / 1,000,000 小时**构造嵌套子集，并用固定 **100 小时**人类视频验证集评估 scaling 趋势。团队还称在预训练未见过的机器人数据上观察到 human-to-robot transfer scaling，并给出用 **10 分钟**遥操作数据微调双五指机械手开瓶盖的案例。相关结果尚未独立复现。
  > 💡 Dyna-2 把具身智能 scaling 的主变量从昂贵机器人遥操作数据转向大规模人类视频，若跨 embodiment transfer 可持续成立，视频数据会成为机器人基础模型的新算力燃料。
   - 来源: [@DynaRobotics](https://x.com/DynaRobotics/status/2086856327150858298) | [DYNA](https://www.dyna.co/dyna-2)

**Peter Walker：OpenRouter 7 月平均每 10 小时上线一个新模型**
- Peter Walker 称 7 月平均每 **10 小时**就有一个新模型上线 OpenRouter。这一频率是 2025 年 7 月的 2.6 倍，也是 2024 年 7 月的 5.8 倍。
  > 💡 模型数量快速增长，会进一步强化聚合平台在发现、比较和路由模型方面的作用。
   - 来源: [@PeterJ_Walker](https://x.com/PeterJ_Walker/status/2087646545755963620)

**Unitree 称仿生双足人形机器人累计生产下线约 1.8 万台**
- Unitree 发帖称，其仿生双足人形机器人累计生产下线约 **18,000 台**。该统计仅包含仿生双足人形机器人，不包含轮式人形平台及其他类型的人形机器人。
  > 💡 累计生产规模提供了观察人形机器人制造能力的一个厂商侧指标，但商业化程度仍需结合交付与实际部署数据判断。
   - 来源: [@UnitreeRobotics](https://x.com/UnitreeRobotics/status/2087475885658210719)

**Jonathan Hurst：机械硬件是实现物理 AI 的关键前提**
- Agility Robotics 联合创始人兼首席机器人官 Jonathan Hurst 在 Science Robotics 发文指出，AI 正推动多用途应用，但机器人进入物理世界后，机械硬件必须设计到位。Agility Robotics 在 X 上将这一观点概括为：AI 可以让机器人更聪明，却无法改变物理规律。公开摘要未给出具体硬件指标或实验数据，文章的核心主张是物理 AI 的能力不仅取决于模型，也取决于承载智能的机械系统。
  > 💡 该文将机械硬件视为物理 AI 的能力组成，而非模型之外的配套；公开摘要未提供具体硬件指标或实验数据，适合按行业观点而非研究突破解读。
   - 来源: [@Agility Robotics](https://x.com/agilityrobotics/status/2087668588866122043) | [Science Robotics](https://www.science.org/doi/10.1126/scirobotics.aee2921) | [DOI](https://doi.org/10.1126/scirobotics.aee2921)

---
*更新时间: 2026-08-13 11:18*
