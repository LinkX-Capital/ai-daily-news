## 05月26日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：GPT-5.6在Codex后台被曝光：1.5M上下文窗口，内部代号iris-alpha，预计6月发布; 通义千问3.7-Max上线隐式缓存：自动复用KV缓存，推理速度提升成本降低
- 产业动态：Anthropic准备推出Claude Memory Files：双模式记忆系统支持结构化持久存储; Google DeepMind发布AlphaProof Nexus：Agent自主解决9个Erdős开放问题，含两个56年未解难题; xAI推出Grok Build Beta版：SuperGrok和X Premium+用户可使用Plan Mode和多媒体生成; Salesforce与Snowflake本周发布财报，市场聚焦AI对企业软件的冲击程度; ClickUp大规模裁员用数千AI Agent替代员工，显示白领工作被AI快速取代
- 算力追踪：华为正式发表"韬定律"：以"时间缩微"替代"几何缩微"，目标2031年达1.4nm同等水平
- 研究关注：SaaS-Bench测试暴露Computer-Use Agent短板：最强Claude Opus 4.7端到端通过率仅3.8%; 中科大团队ICML 2026论文揭示：大模型终身编辑中"越改越稳"的归一化机制; 中科大等联合提出Flow-OPD：在线策略蒸馏解决Flow Matching模型多任务对齐冲突; Aholo.js实现10亿高斯点3D场景实时浏览器渲染，开源MIT协议; 港中文团队CUHK-X数据集：7模态58K样本人体动作数据集填补多模态模型短板
- X讨论：软件工程三个时代演进：1.0基础设施、2.0云服务、3.0 AI Agent; Cerebras晶圆级芯片实现单晶圆承载完整NVL72机架性能，绕过网络功耗瓶颈; 宇树科技展示WVLA 2.0模型：会议室清洁多任务全自主操作演示

---

## 📖 详细参考

### 模型前沿
**GPT-5.6在Codex后台被曝光：1.5M上下文窗口，内部代号iris-alpha，预计6月发布**
- 多名开发者在OpenAI Codex后台日志中发现尚未公布的**gpt-5.6模型**，内部开发代号为**iris-alpha**，另有ember-alpha和beacon-alpha两个测试标签。通过ChatGPT Pro的OAuth认证在Codex环境中成功调用后，探针测试显示上下文窗口达到**150万tokens**，较GPT-5.5的API上限（1.05M）提升约43%。开发者在OpenCode中实测90万tokens输入时模型仍正常运行。泄露信息显示GPT-5.6将采取双版本策略：标准版主攻多步推理，Pro版强化Agent工作流。OpenAI研究人员透露，支撑近期重大数学突破的底层模型已在内部广泛用作日常调试和技术工作的主力。Polymarket预测GPT-5.6在6月30日前发布概率超过85%。
  > 💡 OpenAI将主力模型迭代周期压缩至30-45天，6月将迎来GPT-5.6、Anthropic Sonnet 4.8（代号Conway）和Google Gemini 3.5 Pro的集中发布，大模型竞争进入高频迭代阶段。
   - 来源: [新智元](https://mp.weixin.qq.com/s/T8x357cWij8VKsTlm868Qg) | [@pankajkumar_dev](https://x.com/pankajkumar_dev/status/2058194939264307638) | [@0xLogicrw](https://x.com/0xLogicrw/status/2054785297452314671)

**通义千问3.7-Max上线隐式缓存：自动复用KV缓存，推理速度提升成本降低**
- 阿里巴巴通义千问3.7-Max正式上线隐式缓存功能，系统自动在推理过程中复用已计算的键值对，用户无需任何配置即可获得更快的响应速度和更低的推理成本。该功能对于长序列和重复调用场景效果尤为显著。
  > 💡 隐式缓存正在成为大模型推理优化的标配，通义千问的跟进显示各厂商在该领域的竞争日趋激烈。
   - 来源: [@alibaba_qwen](https://x.com/Alibaba_Qwen/status/2058932656797368619#m)

### 产业动态
**Anthropic准备推出Claude Memory Files：双模式记忆系统支持结构化持久存储**
- Anthropic正在测试Claude的双模式记忆系统：现有的"Classic"模式将用户信息压缩为单条摘要，新方案"Memory Files"将记忆分散为多个按主题、项目或场景组织的结构化文档，用户可随时浏览和编辑。该架构可在不占用上下文窗口的情况下为Claude提供更大量、更持久的用户记录。同步推进的还有"Dreams"功能——一种异步记忆整理机制，可合并重复、更新过期条目、解决矛盾，Anthropic将其类比为REM睡眠记忆巩固，目前已在Opus 4.7和Sonnet 4.6上有限测试。此外，代号"Conway"的Claude后台持久化Agent也预计即将上线。
  > 💡 从单条摘要到结构化文件记忆的升级，标志着AI助手从"对话记忆"向"个人知识库"演进，是Agent长程自主工作的基础设施前提。
   - 来源: [TestingCatalog](https://www.testingcatalog.com/anthropic-plans-claude-memory-update-with-new-memory-files/)

**Google DeepMind发布AlphaProof Nexus：Agent自主解决9个Erdős开放问题，含两个56年未解难题**
- Google DeepMind发布AlphaProof Nexus，一个基于Gemini的形式化证明搜索Agent框架。该框架在353个开放Erdős问题中自主解决了**9个**（包括两个悬而未决56年的问题），在492个OEIS猜想中证明了**44个**，还解决了一个代数几何领域开放15年的问题和一个最小最大优化领域开放7年的问题。研究表明，即使最基本的Agent——交替使用LLM生成和Lean形式化验证——也能复现Erdős问题的成功，但在最困难的问题上成本更高，每个问题约花费几百美元。该Agent已部署至组合数学、优化、图论、代数几何和量子光学等方向的实际数学研究合作中。
  > 💡 AI驱动的形式化证明正从辅助工具演进为数学研究的生产力工具，Gemini+Lean的Agent架构展示了LLM在严格推理场景的实用性，单题几百美元的成本已具备研究级实用价值。
   - 来源: [arXiv](https://arxiv.org/abs/2605.22763v1) | [@pushmeet](https://x.com/pushmeet/status/2058936037754224998)
   
**xAI推出Grok Build Beta版：SuperGrok和X Premium+用户可使用Plan Mode和多媒体生成**
- xAI向所有SuperGrok和X Premium+用户推出Grok Build Beta版。用户可以使用Plan Mode功能、Imagine工具创建图像和视频，以及构建自动化工作流。该功能集成在X平台内，为创作者和企业用户提供端到端的AI Agent开发能力。
  > 💡 Grok Build的发布标志着xAI在AI Agent平台领域的正式入局，与OpenAI、Anthropic等展开直接竞争。
   - 来源: [@xai](https://x.com/xai/status/2058973760708091907#m)

**Salesforce与Snowflake本周发布财报，市场聚焦AI对企业软件的冲击程度**
- 过去半年，华尔街用「SaaS 末日」形容一场惨烈杀跌，Salesforce、ServiceNow、Snowflake股价均从高点**腰斩**。有分析指出，市场过度悲观导致这些龙头股被错杀，但AI并未消灭软件行业，而是带来了结构性分化。与此同时，AI复杂度与合规风险上升反而催生了对相关软件的新需求。本周财报季，两家公司的AI功能商业化进展及传统软件许可证收入变化将成为市场焦点。
  > 💡 企业软件公司的AI转型速度将决定其未来估值，Salesforce和Snowflake的财报是观察AI软件商业化进程的重要窗口。
   - 来源: [The Information](https://www.theinformation.com/articles/salesforce-snowflake-earnings-focus-attention-ais-software-impact)

**ClickUp大规模裁员用数千AI Agent替代员工，显示白领工作被AI快速取代**
- 成立九年的创业公司ClickUp宣布大规模裁员，用数千个AI Agent替代数百名员工。该公司CEO表示AI正在重塑知识工作的本质，裁员是转型的一部分。此举引发业界对AI取代白领工作的广泛讨论。
  > 💡 ClickUp案例是AI替代白领工作的典型案例，显示软件行业的结构性变革正在加速，劳动力市场面临深刻调整。
   - 来源: [TechCrunch](https://techcrunch.com/2026/05/25/what-clickups-mass-layoff-tells-us-about-the-future-of-work/)

### 算力追踪
**华为正式发表"韬定律"：以"时间缩微"替代"几何缩微"，目标2031年达1.4nm同等水平**
- 华为公司董事、半导体业务部总裁何庭波在2026国际电路与系统研讨会上正式发表**"韬（τ）定律"**，提出以**"时间缩微"**替代摩尔定律的"几何缩微"路线。该定律以系统性降低时间常数（韬τ）为目标，通过逻辑折叠等创新技术压缩信号传播时延、提升晶体管密度。华为过去六年已成功设计并量产**381款芯片**，**预计到2031年基于该定律的高端芯片晶体管密度将达到1.4纳米制程的同等水平**。何庭波宣布，**今年秋季华为将发布新的麒麟手机芯片，完整采用逻辑折叠技术**。值得注意的是，该路线本质上是在美国制裁限制先进制程设备获取的背景下，试图通过架构创新绕开制造端约束。
  > 💡 "韬定律"是中国首次在全球半导体领域提出指导产业发展的新原则，逻辑折叠路线试图绕开EUV光刻机限制来缩小与台积电的差距，但实际芯片性能、量产能力和供应链稳定性仍需今年秋季新麒麟芯片的产品验证。
   - 来源: [智东西](https://mp.weixin.qq.com/s/3dEiVhs8gs7vY7H3gorDVw) | [The Information](https://www.theinformation.com/briefings/huawei-moves-narrow-chip-gap-tsmc-despite-u-s-sanctions)

### 研究关注
**SaaS-Bench测试暴露Computer-Use Agent短板：最强Claude Opus 4.7端到端通过率仅3.8%**
- UniPat AI发布SaaS-Bench，在23个真实SaaS系统、106个跨应用长程任务上测试Computer-Use Agent能力。最强模型**Claude Opus 4.7检查点得分43.9%，端到端完全通过率仅3.8%**（106个任务仅完整通过4个），**Kimi K2.5和Gemini 3.1 Pro完全通过率为零**。93.4%的任务跨至少两个应用，97.3%的文本任务操作超过100步。SaaS-Bench揭示了Agent的四种结构性失败：任务越长通过率越低、一步错误导致链式失败、执行后不验证结果、同一任务多次运行分数差异巨大（Claude Sonnet 4.6同一任务三次运行分数从0.00到0.68）。
  > 💡 当前Agent在长程真实工作流中的能力远低于Benchmark成绩，核心瓶颈不是单步操作能力，而是对持久状态的有效推理和闭环验证机制的缺失。面向人类的SaaS界面可能需要为Agent重新设计。
   - 来源: [机器之心](https://mp.weixin.qq.com/s/DZIzuzR7W0jZH0QFoBKQAA) | [UniPat AI](https://unipat.ai)

**中科大团队ICML 2026论文揭示：大模型终身编辑中"越改越稳"的归一化机制**
- 中科大马鑫等人在ICML 2026发表论文"More Edits, More Stable"，揭示终身模型编辑（Lifelong Model Editing）中「越改越稳」的反直觉现象。研究聚焦于终身归一化（Lifelong Normalization, LN），发现移除LN会导致性能立即崩溃，而早期的编辑反而能促进后续编辑的成功。论文首次给出了LN的理论解释，证明其结合岭回归时参数更新具有渐近正交性和有界范数，直接缓解灾难性遗忘和模型崩溃。基于此提出StableEdit方法，通过显式预热阶段和全白化强化稳定性循环。
  > 💡 终身归一化研究为理解LLM持续更新中的稳定性提供了理论框架，StableEdit的实际训练效率提升仍需在大规模模型上进一步验证。
   - 来源: [arXiv](https://arxiv.org/abs/2605.11836) | [PaperWeekly](https://mp.weixin.qq.com/s?__biz=MzIwMTc4ODE0Mw==&mid=2247720489&idx=2&sn=74ab49af6c3fa2c39c528c98ca4d3a84)

**中科大等联合提出Flow-OPD：在线策略蒸馏解决Flow Matching模型多任务对齐冲突**
- 方振等人联合提出Flow-OPD，将LLM后训练中的在线策略蒸馏（OPD）引入Flow Matching文本生成图像模型。该方法采用两阶段策略：先通过单奖励GRPO微调培养领域专精教师模型，再通过在线采样、任务路由标注和轨迹级密集监督将多个教师的专业知识蒸馏到单一学生模型中。还引入流形锚定正则化（MAR），利用任务无关教师提供全数据监督，缓解纯RL对齐常见的审美退化问题。基于**Stable Diffusion 3.5 Medium**，Flow-OPD将**GenEval得分从63提升至92，OCR准确率从59提升至94**，较vanilla GRPO整体提升约10个点，且出现了"学生超越教师"的涌现效应。
  > 💡 Flow-OPD将LLM后训练的OPD范式成功迁移到图像生成领域，解决了多奖励信号"跷跷板效应"和奖励作弊问题，为构建通用文本生成图像模型提供了可扩展的对齐方案。
   - 来源: [arXiv](https://arxiv.org/abs/2605.08063) | [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651034802&idx=2&sn=8073f8f1de5678cc24a4b43a269766f2&chksm=852fd1f268d756956986565e47c70a58ea19b9064c0aa697e4e1d89bea4a9f87ab7c54381a62&scene=0&xtrack=1#rd)

**Aholo.js实现10亿高斯点3D场景实时浏览器渲染，开源MIT协议**
- 开源3D Gaussian Splatting渲染引擎**Aholo.js**实现了将10亿高斯点3D世界实时渲染到浏览器的突破，性能指标超越李飞飞团队此前的方法。该引擎通过chunk-level LoD与流式调度，支持10亿级高斯点场景秒级加载，首屏10秒内进入；提供效果优先、性能优先和极限性能多档渲染配置；支持物理碰撞体生成和云端混合渲染。项目采用**MIT开源协议**，支持ply/spz/sog/splat等主流格式，适合SDK接入和二次开发。
  > 💡 3DGS浏览器渲染引擎的开源化将降低空间计算和数字孪生的技术门槛，Aholo.js的LoD+流式方案在工程上具有实用价值。
   - 来源: [Aholo.js](https://aholojs.dev/zh-CN/) | [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651034802&idx=1&sn=aca7d8c47e9a0e86138d845b09d9e70a&chksm=85efa726dff6d75b1a26f0afde495559630d2e045dd2ecf1e18ed0f3262bb4240187b32f3296&scene=0&xtrack=1#rd)

**港中文团队CUHK-X数据集：7模态58K样本人体动作数据集，填补多模态模型短板**
- 香港中文大学邢国良教授团队发布CUHK-X大型多模态人体动作数据集。该数据集包含**58,445个样本**，覆盖**40种动作**、**30名参与者**、两个室内环境，涵盖7种模态（视觉、深度、姿态、音频、IMU、mmWave等）。团队提出了三个基准任务：动作识别（HAR，平均准确率76.52%）、动作理解（HAU，40.76%）和动作推理（HARn，70.25%），包含6个评估子任务。研究指出当前大视觉语言模型在非RGB模态上表现薄弱，主要原因是缺乏大规模数据-描述配对资源。
  > 💡 CUHK-X的数据-描述配对方式解决了传统动作数据集标注粗糙的问题，为具身智能和多模态推理研究提供了标准化评测基准。
   - 来源: [arXiv](https://arxiv.org/abs/2512.07136) | [DeepTech深科技](http://mp.weixin.qq.com/s?__biz=MzA3NTIyODUzNA==&mid=2649797156&idx=2&sn=11ccc50b5924ba280b0e08f8720ab867&chksm=861a5a63398458e6019f16aa16a46afb9760530771b9a1e133c314aa63176db73dfcf1a32741&scene=0&xtrack=1#rd)

### X讨论
**软件工程三个时代演进：1.0基础设施、2.0云服务、3.0 AI Agent**
- 资深工程师指出，同时精通软件工程三个时代的工程师极为稀缺：1.0时代专注构建基础设施，2.0时代聚焦云服务和分布式系统，3.0时代以AI Agent为核心。每个时代需要不同的技术思维和工作模式，从底层系统设计到云原生架构，再到AI Agent的自主决策逻辑，要求工程师具备跨越多个技术栈的能力。
  > 💡 AI Agent时代对工程师提出了更高要求，但「全能工程师」的稀缺性也意味着团队协作和专精化仍是现实路径。
   - 来源: [@denny_zhou](https://x.com/denny_zhou/status/2058994840327881010#m)

**Cerebras晶圆级芯片实现单晶圆承载完整NVL72机架性能，绕过网络功耗瓶颈**
- Cerebras的晶圆级芯片在单个晶圆上实现了完整计算集群的性能。通过绕过缺陷并保持片内路由，Cerebras实现了机架级算力而无需传统AI服务器之间的网络互联功耗瓶颈。该技术将整个NVL72机架的计算资源集成在单一晶圆上，大幅降低了系统功耗和通信延迟。
  > 💡 Cerebras晶圆级方案在特定AI负载下具有能效优势，但软件生态和通用性仍是其进入主流市场的关键障碍。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2058714944313450805#m)

**宇树科技展示WVLA 2.0模型：会议室清洁多任务全自主操作演示**
- 宇树科技展示WVLA 2.0模型，展示了会议室清洁测试的多任务全自主操作能力。该视频为单次连续拍摄，机器人完成了多个清洁任务，展现了强泛化能力。
  > 💡 宇树机器人展示了具身智能的实际进展，但实验室演示与真实复杂场景的差距仍是挑战。
   - 来源: [@unitreerobotics](https://x.com/UnitreeRobotics/status/2058809948650484130#m)


---
*更新时间: 2026-05-26 18:30*