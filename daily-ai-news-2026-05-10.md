## 05月10日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 产业动态：谷歌DeepMind发布AI联合数学家，FrontierMath Tier 4达48%创AI最高分; OpenRouter推出Pareto Code免费编程路由器; 英伟达2026年内已承诺$400亿股权投资AI生态，其中$300亿投向OpenAI
- 算力追踪：AMD发布vLLM-ATOM插件，AMD Instinct GPU原生推理性能直通vLLM
- 初创&融资：Robo.ai以$1亿全股票收购Neurovia AI，构建物理AI视频数据基础设施
- 研究关注：Sakana AI与NVIDIA开源TwELL稀疏格式，重塑稀疏性适配GPU，推理加速30%训练加速24%; OpenAI翁家翌提出Heuristic Learning，Codex写纯代码在Atari/MuJoCo媲美Deep RL; 港科大开源StarVLA框架，模块化架构统一VLM与世界模型两大VLA范式; 浙大联合上海AI Lab发布SciGraph-SCP，覆盖8大学科3.7亿实体的AI原生科学知识图谱; Claude Code源码逆向分析，核心循环仅while-loop，7模式权限+5层上下文压缩构成主要复杂度
- X讨论：Claude Code团队成员倡导HTML替代Markdown作为Agent输出格式; SGL Project与Radixark团队合作优化DeepSeek V4推理，提升B200/B300性能

---

## 📖 详细参考

### 产业动态
**谷歌DeepMind发布AI联合数学家，FrontierMath Tier 4达48%创AI最高分**
- Google DeepMind Pushmeet Kohli 分享 **AI co-mathematician**，一个多Agent系统，可主动与人类数学家协作解决开放式研究数学问题。在 FrontierMath Tier 4 自主模式评估中得分 **48%**，创所有AI系统最高分。数学家已在群论、哈密顿系统、代数组合等领域测试并报告显著成果。此前 Gemini Deep Think 在 IMO 达金牌水准（35分，6题解5题），AlphaEvolve 改进了50+开放问题中20%的最优解，包括打破Strassen 1969年保持的4×4矩阵乘法纪录（48次标量乘法）。
  > 💡 AI辅助数学从"工具"升级为"研究合作者"。FrontierMath Tier 4此前GPT-5.5 Pro为39.6%，AI co-mathematician以48%大幅刷新，多Agent协作模式可能在更多科学领域复制
   - 来源: [Pushmeet Kohli (LinkedIn)](https://www.linkedin.com/posts/pushmeet-kohli-4838994_the-future-of-math-is-mathematicians-and-activity-7458579385223245824-s4jx) | [Google Blog](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/ai-for-math/)
  
**OpenRouter推出Pareto Code免费编程路由器，按编码评分自动路由最便宜达标模型**
- OpenRouter推出Pareto Code免费实验性编程路由器。用户可设置 `min_coding_score` 参数，路由器自动选择达到该分数门槛的最便宜编程模型，模型评分由 **Artificial Analysis** 排名提供。该路由器将模型按编码能力映射到不同性能/价格档位，开发者可根据速度偏好或成本偏好灵活选择，Pareto前沿实时更新。
  > 💡 路由器的灵活定价/性能权衡满足不同开发者需求，Sakana Fugu的多模型编排思路正在被更多产品采用
   - 来源: [@OpenRouter](https://x.com/OpenRouter/status/2053170520087024109#m)

**英伟达2026年内已承诺$400亿股权投资AI生态，其中$300亿投向OpenAI**
- 据CNBC报道，英伟达2026年至今已承诺超过 **$400亿** 用于AI公司股权投资。其中最大一笔为向 OpenAI 投资 **$300亿**。此外还宣布7笔上市公司投资，包括 Corning **$32亿** 和数据中心运营商 IREN **$21亿**。英伟达2025年完成67笔VC投资，2026年已参与约24轮私募融资。Wedbush 分析师 Matthew Bryson 评价这些投资属于"circular investment theme"，但若成功可帮助英伟达建立"competitive moat"。
  > 💡 $400亿规模超过多数AI独角兽估值，英伟达正从芯片供应商转型为AI生态最大资本方。但"循环投资"争议持续——投资客户反过来采购自家GPU，实质是用资本锁定需求
   - 来源: [CNBC](https://www.cnbc.com/2026/05/09/nvidia-embraces-ai-investor-topping-40-billion-in-equity-bets-2026.html) | [TechCrunch](https://techcrunch.com/2026/05/09/nvidia-has-already-committed-40b-to-equity-ai-deals-this-year/)

### 算力追踪
**AMD发布vLLM-ATOM插件：AMD Instinct GPU原生推理性能直通vLLM**
- AMD发布vLLM-ATOM插件，以out-of-tree方式将ATOM推理引擎集成到vLLM，无需修改vLLM核心代码即可获得AMD硬件优化。支持**FP4/FP8精度**、AITER融合注意力、DeepSeek V2/V3 MLA架构、Kimi-K2.5多模态等。支持模型包括Qwen3-235B、DeepSeek-R1-0528、Kimi-K2/K2.5、GLM-4.7等。设计理念：ATOM快速验证新优化→成熟后上游合并到vLLM ROCm后端。
  > 💡 AMD通过插件模式绕过vLLM上游集成周期，直接向用户交付硬件优势。MI355X FP4和MI400机架级推理的提前支持将吸引大规模部署用户
   - 来源: [AMD ROCm Blog](https://rocm.blogs.amd.com/software-tools-optimization/vllm-atom/README.html)
   
### 初创&融资
**Robo.ai以$1亿全股票收购Neurovia AI，构建物理AI视频数据基础设施**
- Robo.ai（NASDAQ: AIIO）宣布以 **$1亿全股票** 收购 Neurovia AI Limited 100%股权。Neurovia 聚焦AI视频压缩、边缘计算与实时分析，解决物理AI时代海量视频数据的传输与计算瓶颈。交易采用Class B普通股支付，设 **8年锁定期**（前3年完全锁定，后5年逐步解禁）。收购完成后 Robo.ai 计划将业务从传统视频编码升级为全球AI视频数据基础设施平台，覆盖robotaxi、自动驾驶、无人机和人形机器人等场景。消息公布后 AIIO 股价 **飙升70%**。
  > 💡 全股票+8年锁定表明收购方以股权绑定团队而非现金收购。物理AI时代视频数据基础设施是新赛道，但Robo.ai作为小市值公司执行风险较高
   - 来源: [PRNewswire](https://www.prnewswire.com/news-releases/roboai-announces-acquisition-of-data-processing-and-compression-technology-company-neurovia-building-data-infrastructure-for-the-machine-economy-302766695.html) | [Yahoo Finance](https://finance.yahoo.com/sectors/technology/articles/100-million-neurovia-acquisition-expands-145546646.html)

### 研究关注
**Sakana AI与NVIDIA开源TwELL稀疏格式：重塑稀疏性适配GPU，推理加速30%训练加速24%**
- Sakana AI与NVIDIA合作发布ICML 2026论文"Sparser, Faster, Lighter Transformer Language Models"（作者包括Transformer论文共同作者**Llion Jones**），开源GPU kernel与数据格式。核心贡献两方面：提出**TwELL（Tile-wise ELLPACK）**稀疏打包格式，按tile对齐可直接嵌入优化tiled matmul kernel；开发**自定义CUDA kernel**，推理端融合up/down projection跳过中间activation物化，训练端压缩为稀疏+dense备份的混合表示。通过L1正则化诱导>**99%稀疏率**（对下游性能影响可忽略），在**H100**上推理加速最高**30%**，训练加速最高**24%**且峰值内存降低>**24%**。收益随规模增长：0.5B→2B时非零activation减少**38%**，2B模型推理加速**20.5%**、训练加速**21.9%**。
  > 💡 TwELL解决了"做更少运算反而更慢"的硬件悖论——tile对齐设计让稀疏性与现有GPU kernel管线无缝融合而非对抗。收益随模型规模增长是关键信号：若趋势持续，稀疏性可能成为量化/剪枝之外LLM效率的第三条主轴
   - 来源: [Sakana AI](https://sakana.ai/twell/) | [arXiv](https://arxiv.org/abs/2603.23198) | [GitHub](https://github.com/SakanaAI/sparser-faster-llms)

**OpenAI翁家翌提出Heuristic Learning：Codex写纯代码在Atari/MuJoCo媲美Deep RL**
- OpenAI研究者翁家翌（Jiayi Weng）发布博文"Learning Beyond Gradients"，提出**Heuristic Learning (HL)**范式：用Coding Agent（Codex/GPT-5.4）持续维护程序代码系统替代神经网络梯度更新。实验结果：Atari Breakout达到理论满分**864**分、MuJoCo Ant达**6146**（媲美Deep RL）、HalfCheetah达**11837**、Atari57中位HNS在1M步时已超过PPO基线。HL系统包含策略代码+状态检测+回归测试+失败回放+版本记忆，coding agent直接编辑代码而非反向传播。翁家翌认为这可能是pretraining→RLHF→RL/RLVR之后的下一个范式。
  > 💡 Heuristic Learning本质是"让AI写代码替代训练神经网络"，如果coding agent持续变强，大量传统RL任务可能被纯程序系统取代。对具身智能有直接启示：底层控制可分层为HL+浅层NN+LLM Agent
   - 来源: [翁家翌博客](https://trinkle23897.github.io/learning-beyond-gradients/) | [X](https://x.com/Trinkle23897/status/2052596837547495549)

**港科大开源StarVLA框架，模块化架构统一VLM与世界模型两大VLA范式**
- 港科大联合社区开源 **StarVLA**，采用模块化 backbone-action head 架构，支持 **VLM backbone**（如 Qwen-VL）和 **世界模型 backbone**（如 Cosmos）可独立互换。提供可复用训练策略（跨embodiment学习、多模态联合训练），集成 **LIBERO、SimplerEnv、RoboTwin 2.0、RoboCasa-GR1、BEHAVIOR-1K** 五大benchmark的统一评测接口，支持仿真和真机部署。论文称其单benchmark训练recipe在多个benchmark上已 **match or surpass** 先前方法。
  > 💡 StarVLA解决VLA领域"架构不兼容、代码库碎片化"的核心痛点。backbone与action head解耦设计使研究者可独立迭代，对标深度学习早期的PyTorch统一时刻
   - 来源: [arXiv:2604.05014](https://arxiv.org/abs/2604.05014) | [GitHub](https://github.com/starVLA/starVLA)

**浙大联合上海AI Lab发布SciGraph-SCP：覆盖8大学科、3.7亿实体的AI原生科学知识图谱**
- 浙江大学联合上海人工智能实验室、同济大学等发布 **SciGraph-SCP Server**，覆盖 **8个科学领域、3.7亿+实体、37亿+三元组**，集成科学智能上下文协议（SCP），为AI智能体提供原生调用接口。已基于 SkillNet 完成技能化封装，支持从 OpenClaw、华为 JiuwenClaw 等开源智能体框架直接调用。团队还展示了基于 SciGraph 构建的大模型知识维基 **SciLLM-Wiki**。前期工作已在《国家科学评论》发表综述论文。本项工作得到科技创新2030—"新一代人工智能"国家科技重大专项支持。
  > 💡 SciGraph从数据规模和智能体集成两个维度推进AI4Science基础设施：3.7亿实体+37亿三元组的开放图谱直接通过SCP协议供Agent调用，跳过传统API层
   - 来源: [SciGraph-SCP Server](https://scphub.intern-ai.org.cn/detail/37O) | [PaperWeekly](https://mp.weixin.qq.com/s?__biz=MzIwMTc4ODE0Mw==&mid=2247720111&idx=3&sn=f28a0eb6d50d31a3b4a84d5ff2197b35)

**Claude Code源码逆向分析：核心循环仅while-loop，7模式权限+5层上下文压缩构成主要复杂度**
- Jiacheng Liu 等人通过分析 Claude Code 公开 TypeScript 源码，识别出 **5大设计哲学**（人类决策权、安全与安保、可靠执行、能力放大、上下文适应性）并追踪至 **13条设计原则** 的具体实现。系统核心是简单的 while-loop（调用模型→运行工具→重复），但主要代码量围绕此循环：**7模式权限系统 + ML分类器**、**5层上下文压缩管线**、**4种扩展机制**（MCP/plugins/skills/hooks）、带 worktree 隔离的 **subagent委派**、append-only 会话存储。论文还与开源 Agent 系统 OpenClaw 对比，揭示同一设计问题在不同部署上下文中产生不同架构答案。
  > 💡 这是目前最系统的 Claude Code 架构逆向分析。5层上下文压缩管线和7模式权限系统值得所有 Agent 开发者参考——Agent的核心复杂度不在推理循环本身，而在周围的安全/上下文/扩展系统
   - 来源: [arXiv:2604.14228](https://arxiv.org/abs/2604.14228) | [量子位](https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247889444&idx=3&sn=db42e6bfd193cb5b0d2150a3ac90b64d)

### X讨论
**Claude Code团队成员倡导HTML替代Markdown作为Agent输出格式**
- Claude Code团队成员trq212发帖分享用HTML替代Markdown作为Claude Code输出格式的实践。理由：HTML可表达表格/SVG/交互/动画/空间数据，信息密度远高于Markdown；配合Opus 4.7的**1M上下文窗口**，token增长可忽略；HTML文件上传至S3即可直接分享链接。使用场景包括：方案探索（生成多方案HTML网格对比）、PR代码解释（内联diff标注）、设计原型（滑块/旋钮调参）、研究报告、可交互playground编辑器（拖拽排序、配置编辑后一键导出）。缺点是**HTML diff对版本控制不友好**，生成耗时比Markdown长2-4倍。
  > 💡 trq212的实践揭示了Agent输出从纯文本向富媒体演进的路径。HTML作为"通用画布"可能改变AI辅助工作的交互范式，但VC不友好是工程层面的硬伤
   - 来源: [@trq212](https://x.com/trq212/status/2052809885763747935)

**SGL Project与Radixark团队合作优化DeepSeek V4推理，提升B200/B300性能**
- SGL Project与Radixark团队合作优化DeepSeek V4在NVIDIA B200、B300及4x iso-interactive配置上的推理性能。SemiAnalysis评价这是"Amazing work"。
  > 💡 开源模型推理优化持续推进，SGL与Radixark合作为DeepSeek生态补强
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2052916556972065271#m)

---
*更新时间: 2026-05-10 (质量修正版)*