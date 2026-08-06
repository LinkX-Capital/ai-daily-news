## 08月06日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 20 条

---

## 要点汇总

- 模型前沿：NVIDIA开源Alpamayo 2 Super，LingoQA自动驾驶推理benchmark第一; Meta发布Muse Code终端编程agent与Muse Spark 1.2编程模型; Liquid AI发布LFM2.5-2.6B：2.6B端侧agentic模型; Pokee AI发布Isaac 28B：10M token上下文的非decoder-only agentic模型
- 产业动态：Google AI顶层人事震荡：Hassabis转任GDM董事长兼Alphabet首席科学家，Jeff Dean离职创办Discovery Loop; 字节跳动张一鸣在内部会议明确拒绝用蒸馏推进AI模型; Cursor开源Mixture-of-Kittens：NVL72 MoE训练megakernel，端到端tokens/s提升1.41x; PrimeIntellect开源Prime Agent：RLM + Continual Harness，Opus 5在ARC-AGI-3达95.5%超人类基线; Shopify：AI搜索Q2驱动流量与订单同比三倍，传统搜索仍增长; Sakana AI与大和证券合作进入财富管理本番开发阶段
- 算力追踪：Anthropic组建自研AI芯片团队，与三星谈判合作
- 研究关注：腾讯开源Hunyuan3D-Buffalo 1.0，统一3D理解、生成、编辑与部件生成; AURORA-LM:在连续潜在空间中直接做扩散的文本生成模型; Speculative Correction:面向扩散语言模型的先草稿再修订解码框架; JoyAI-Video-Edit:16B参数实时开放视频编辑自回归扩散框架; 基础模型博弈论：通过相似性推断通向理性合作的新路径; 动态分配评估预算：多臂赌博机视角的模型排名
- X讨论：ArtificialAnalysis发布Endpoint Accuracy Index v1.0，量化同模型不同provider的精度损耗; ZhihuFrontier：自演化AI分三层，只有一层真正通向RSI; steipete：用codex + 视频KVM让agent自验证OpenClaw的iMessage集成

---

## 📖 详细参考

### 模型前沿
**NVIDIA开源Alpamayo 2 Super，LingoQA自动驾驶推理benchmark第一**
- NVIDIA发布Alpamayo 2 Super并开放商业许可，基于Cosmos 3 Super Reasoner、用RL后训练，参数规模约30B（为Alpamayo 1.5的3倍），在LingoQA上以Lingo-Judge衡量超过Qwen2.5-VL 72B **17.0分**、Gemini 2.5 Pro **15.1分**、GPT-4o **23.2分**。模型同时产出轨迹、因果链（CoC）trace、meta-action、推理自动标注和带2D grounding的VQA五个耦合输出，并与Halos安全验证流程对齐ISO/PAS 8800。Alpamayo家族在Hugging Face下载量已超**50万**，许可证为Linux基金会的OpenMDW-1.1，允许商业 Redistribution。
  > 💡 把因果链trace和meta-action做进同一个foundation model，让自动驾驶决策从"黑盒运动预测"走向可被安全工程师审计的对象；OpenMDW商业许可补齐了"R&D权重→上路部署"的最后一公里，是端到端方案对封闭栈的再一次挤压。
   - 来源: [NVIDIA Blog](https://blogs.nvidia.com/blog/alpamayo-2-super-open-model-now-available/) | [@JensenHuang](https://x.com/JensenHuang/status/2084656303046332747)

**Meta发布Muse Code终端编程agent与Muse Spark 1.2编程模型**
- Meta旗下MSL发布Muse Code（beta）终端编程agent，以及驱动它的编程模型Muse Spark 1.2。Muse Code的核心结构是"主agent循环 + 常驻后台子agent"：后台子agent在session内持续累积上下文，需要时并行扇出多个子agent到隔离worktree；每个model call、tool run、edit都追加到本地事件日志，崩溃后可精准续跑。Muse Spark 1.2训练算力显著扩展、环境多样性提升，与Muse Code协同训练（包含harness轨迹rejection sampling）。在案例研究中，模型在NVIDIA Hopper上跑了**1000+ tool calls / 24小时**持续优化KDA和MLA kernel，远超baseline。Muse Spark 1.2在Artificial Analysis Intelligence Index得分**54**。
  > 💡 把"agent runtime即事件日志"和"持续子agent"绑定在一起，让agent能在长任务上保持状态而不退化；1.2代已把训练数据从"代码片段"扩展到"harness轨迹"，这是模型-工具协同收敛路径上的明确信号。
   - 来源: [Meta Research Blog](https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2) | [@AIatMeta](https://x.com/AIatMeta/status/2085084709277565213) | [@finkd](https://x.com/finkd/status/2085080750034940201) | [@ArtificialAnlys](https://x.com/ArtificialAnlys/status/2085116732231028882)

**Liquid AI发布LFM2.5-2.6B：2.6B端侧agentic模型**
- Liquid AI发布LFM2.5-2.6B，目标是把agentic工作流跑到端侧：M5 Max上CPU推理**220 tok/s**、Rygon AI Max+ 395上113 tok/s、手机上30 tok/s，内存占用**<2.5GB**。模型在**34T tokens**上预训练，词表扩展到128K，4阶段post-training包含SFT、Teacher Specialization、Multi-Domain On-Policy Distillation（MOPD）、Agentic RL（GRPO + LLM-as-judge + 程序校验 + 安全硬门）。在指令遵循与工具调用benchmark上多数超过Gemma-4 E2B/E4B和Qwen3.5-4B，τ³-Bench Banking达到**5.67**。RL阶段直接跑在Hermes Agent、OpenClaw等真实harness里。
  > 💡 Liquid把on-policy蒸馏 + 真实harness RL做进2.6B，把"agent"从云端API拉到本地常驻进程；一旦边际token成本归零，长时背景agent的商业模型就会和云端方案分化。
   - 来源: [Liquid AI Blog](https://www.liquid.ai/blog/lfm2-5-2-6b) | [@liquidai](https://x.com/liquidai/status/2084640749862236227)

**Pokee AI发布Isaac 28B：10M token上下文的非decoder-only agentic模型**
- Pokee AI发布Isaac 28B Technical Report。模型是non-decoder-only架构，上下文窗口最高**10M tokens**，在单张NVIDIA B200上prefill可达**137K tokens/s**、decode 335 tok/s，可以部署在客户端工作站。论文核心论点：长上下文+agentic能力此前几乎只能从云端获取，使得合规/主权/端侧场景无解；Isaac在function calling、多轮交互执行、tool orchestration和terminal工作上达到或超过cost-optimized云端系统。
  > 💡 把"10M上下文 agentic"和"单GPU本地部署"绑在一起，把regulated/sovereign场景从"无法享受长上下文agent"的困境里拉出来；non-decoder-only架构也提供了一个不同于主流Token混音的工程样本。
   - 来源: [Pokee AI Technical Report](https://console.pokee.ai/pokee-isaac-28b-v0-technical-report.pdf) | [@Pokee_AI](https://x.com/Pokee_AI/status/2084682445648216383) | [arXiv](https://arxiv.org/abs/2608.03958)

### 产业动态
**Google AI顶层人事震荡：Hassabis转任GDM董事长兼Alphabet首席科学家，Jeff Dean离职创办Discovery Loop**
- Google CEO Sundar Pichai与Demis Hassabis同步发出内部信：Hassabis不再担任Google DeepMind CEO，转任GDM董事长兼Alphabet首席科学家，继续领导Isomorphic Labs；现任GDM CTO兼Google首席AI架构师Koray Kavukcuoglu晋升SVP of Google DeepMind，统管Gemini模型、前沿研究和Gemini app/开发者团队。同日，Jeff Dean在X上发布告别邮件正式公开：他与Sanjay Ghemawat、Oriol Vinyals、Quoc Le联合创办**Discovery Loop**——一家public benefit corporation，使命是用自动化ML/科学/工程循环加速发现，目标对齐NAE Grand Challenges；Sundar表示Alphabet是创始投资人和Cloud partner，并建立ML系统研究合作框架。Jeff Dean在Google工作27年，参与了TensorFlow、TPU、Gemini等关键项目。
  > 💡 这是Google AI历史上罕见的双线顶层变动：Hassabis从运营角色切到战略/AGI shaping角色，叠加Isomorphic的药物研发；Jeff Dean带着三位长期合作者集体出走创业，意味着Google基础研究体系最重要的"基础设施大脑"开始独立运行；Alphabet选择做Discovery Loop的创始投资人而不是收购锁死，反映出AI人才外溢已无法用旧式竞业方式留住，资本绑定+合作框架是新均衡。
   - 来源: [Google Blog (Sundar + Demis 内部信)](https://blog.google/company-news/inside-google/message-ceo/next-chapter-ai-momentum/) | [@JeffDean](https://x.com/JeffDean/status/2085083442669318443) | [The Information](https://www.theinformation.com/briefings/jeff-dean-leaves-google-demis-hassabis-steps-aside-google-deepmind-ceo)

**字节跳动张一鸣在内部会议明确拒绝用蒸馏推进AI模型**
- 据报道，字节跳动创始人张一鸣在上月一次内部会议上向员工表示，公司不会通过蒸馏来作为推进AI模型能力的捷径，即便这意味着短期内会落后于国内对手。报道援引接近公司人士指出，作出该判断的原因之一是字节跳动与美国政府围绕TikTok的复杂历史。会议在内部称为Seed的字节AI团队全员会上召开，时间点紧接Moonshot AI的Kimi K3模型发布之后。
  > 💡 字节在监管与合规压力下把"训练方法选择"与"企业政治风险"绑定，会影响其后续在大模型版本节奏上的相对位次。
   - 来源: [The Information](https://www.theinformation.com/articles/bytedances-founder-rules-distillation-ai-models)

**Cursor开源Mixture-of-Kittens：NVL72 MoE训练megakernel，端到端tokens/s提升1.41x**
- Cursor Research开源Mixture-of-Kittens（MoK），一个为GB300 NVL72从零设计的DSV3-style MoE训练megakernel。核心设计：把所有dispatch/combine通信和expert FFN计算fuse进单个kernel；通过pull-based forward dispatch + push-based forward combine + 反向对称布局，消除跨GPU signaling，单机dispatch latency比push-based降**5.8x**；引入ring token buffer（macrobatch）彻底消除CPU-GPU同步，规避GB300 Grace CPU慢的问题；MXFP8训练稳定，fully deterministic。在Kimi K2.7 / GLM-5.2 / Qwen3.5-397B-A17B / DeepSeek-V4-Pro四种模型shape的MoE层benchmark上，MoK比最快baseline快**1.58x-2.37x**；Cursor内部生产stack在512 GPU上端到端tokens/s从760.9提升到**1070.2（1.41x）**。
  > 💡 MoK把"通信是MoE瓶颈"这个问题用pull/push方向选择 + megakernel fusion + ring buffer三个层次同时治掉；开源意味着GB300 NVL72上的MoE训练效率天花板被拉到社区可复现水平，对DeepEP/HybridEP构成直接竞争。
   - 来源: [Cursor Blog](https://cursor.com/cn/blog/mixture-of-kittens) | [@cursor_ai](https://x.com/cursor_ai/status/2084670806613737919)

**PrimeIntellect开源Prime Agent：RLM + Continual Harness，Opus 5在ARC-AGI-3达95.5%超人类基线**
- PrimeIntellect发布开源agent harness——Prime Agent，围绕两个核心抽象：Recursive Language Model（RLM）把context作为变量、子agent调用作为REPL里的函数调用；Continual Harness把prompt/skill/memory/subagent视为agent可CRUD的对象，并由`/refine`从自身轨迹中提炼最小可行的harness改进。在ARC-AGI-3上，配Opus 5三次run得分**95.0/95.2/95.5%**，超过报告的人类专家基线**95.4%**，Best@3达99.97%。在长上下文/长任务套件上，Prime Agent + GLM-5.2在OOLONG-Pairs、LongBenchPro、ManyIH Coding等任务上多数超过Pi-mono + 子agent或Claude Code + Opus 5。
  > 💡 "harness本身是agent可改的对象"是近期agent设计的关键转变——Prime Agent把它形式化为CRUD + /refine循环并开源，意味着harness自演化不再是少数lab的私有配方；ARC-AGI-3超过人类基线不是模型变强，而是harness-模型协同达到的。
   - 来源: [PrimeIntellect Blog](https://www.primeintellect.ai/blog/prime-agent) | [@PrimeIntellect](https://x.com/PrimeIntellect/status/2085086999267144083)

**Shopify：AI搜索Q2驱动流量与订单同比三倍，传统搜索仍增长**
- Shopify在Q2财报电话会上披露：AI驱动的流量和订单同比**三倍**，传统搜索sessions过去两年增长1.3x、仍占门店约1/3流量，AI未侵蚀搜索而是补充。Q2营收同比+36%至**$3.6B**，毛运营利润+31%至$1.71B，双双超预期。President Harley Finkelstein解释，AI agent能跨多维度（意图、尺寸、车型、约束）匹配结构化catalog，半数AI-referred sessions直接落到商品详情页（传统搜索的2.5x），**75%**的AI归因购买发生在Top 100品类之外。Shopify已建立Claude、ChatGPT、Perplexity、Lovable等主流AI agent平台connector。
  > 💡 Shopify用数据反驳"AI杀死搜索流量"的叙事：对出版业是失血，对电商长尾则是更精确的需求匹配；AI agent接入catalog的connector层正在成为新的"SEO"。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/05/shopify-says-ai-search-is-driving-more-traffic-and-sales-not-replacing-google/)

**Sakana AI与大和证券合作进入财富管理本番开发阶段**
- Sakana AI与大和证券集团宣布，2025年9月签订的合作协议在市场信息收集与分析的技术验证阶段取得结果，确认Sakana AI的"AI Scientist"、AB-MCTS等agent技术对证券咨询业务有效；**2026年8月1日**起进入财富管理领域的本番开发phase，目标是将技术验证阶段建立的基盘发展为面向客户提案业务的AI产品，分阶段在大和证券内部部署。
  > 💡 这是日本头部券商把agent从PoC推到production的明确信号；Sakana AI的合作路径从"技术研究"→"基盘建立"→"产品化"逐步收敛，为日本金融行业AI落地提供了一个可参照的模板。
   - 来源: [Sakana AI Blog](https://sakana.ai/daiwa-shoken-full-scale/) | [@hardmaru](https://x.com/hardmaru/status/2085017735000465694)

### 算力追踪
**Anthropic组建自研AI芯片团队，与三星谈判合作**
- Anthropic首次公开确认正在组建in-house silicon团队，为Claude设计定制芯片，让模型"在客户所需规模上"跑得更快更高效。Business Insider独家披露岗位年薪**$320K-$485K**，要求工程师有"direct personal contribution to shipping silicon"。Anthropic同步声明将继续multi-chip策略，硬件来自AWS、Google、Nvidia、AMD；The Information上月已报道Anthropic与Samsung谈判代工合作。OpenAI 6月已发布Broadcom代工的Jalapeño推理芯片，Meta MTIA即将量产。
  > 💡 Anthropic进入自研硅子赛道时间晚于OpenAI和Meta，但走的是相同的"模型-硬件协同设计"路径；岗位要求"shipped silicon"意味着首批交付周期将以年计，短期仍靠AWS/Google算力支撑。
   - 来源: [TechCrunch](https://techcrunch.com/2026/08/05/anthropic-is-hiring-an-ai-chip-design-team/) | [Business Insider](https://www.businessinsider.com/anthropic-in-house-silicon-chip-team-claude-2026-8)

### 研究关注
**腾讯开源Hunyuan3D-Buffalo 1.0，统一3D理解、生成、编辑与部件生成**
- Hunyuan3D-Buffalo 1.0是一个统一多模态框架，在同一架构下支持3D理解、文生3D、指令引导3D编辑以及文本约束的部件生成。论文披露团队构建了**8700万**规模3D多模态语料，其中理解样本2500万、文生3D对5000万、编辑对1200万。架构上由Hunyuan3D-VLM负责语义结构与空间理解，与Hunyuan3D DiT联合完成高保真3D合成，编辑与部件生成额外将源物体表示作为扩散条件以保持整体结构。论文称在文生3D与3D编辑基准上取得SOTA或领先成绩。
  > 💡 把3D理解与编辑放进同一训练回路后，编辑质量反向帮助生成质量收敛，说明3D多模态已走到"统一数据—统一模型"的临界点。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2608.02711) | [arXiv](https://arxiv.org/abs/2608.02711)

**AURORA-LM:在连续潜在空间中直接做扩散的文本生成模型**
- AURORA-LM 把文本潜在表示的构建与分布建模解耦开来,采用基于 Query 的编解码器把文本组织成前缀对齐的高容量潜在序列,再用块因果扩散 Transformer 通过 flow matching 学习该分布,在块内并行去噪的同时逐块从左到右生成。该模型在 OpenWebText 自由生成和 XSum 摘要任务上取得了当前连续与扩散类语言模型中的最强成绩,扩展到**10亿参数**、约**1500 EFLOPs** 算力后还超越了更大的同类潜在扩散语言模型。所有实验均在 Ascend NPU 上完成。
  > 💡 离散 token 一直让文本难以复用图像/音频/视频的连续扩散范式,AURORA-LM 不压缩潜在空间,而是让扩散模型去适配高容量可解码 latent,这为文本生成脱离自回归路线提供了一条新路径。
   - 来源: [HuggingFace Daily Papers](https://huggingface.co/papers/2608.02602) | [arXiv](https://arxiv.org/abs/2608.02602)

**Speculative Correction:面向扩散语言模型的先草稿再修订解码框架**
- 论文针对扩散语言模型(DLM)的解码过程,提出"先一次性生成完整草稿、再用双向扩散整体修订"的推理模式,并在 LLaDA2.1-Flash 与 LLaDA2.1-Mini 上分别测试 Flash-Flash(同模型自修订)与 Mini-Flash(小模型草稿、大模型修订)两种配置。Flash-Flash 把 GSM8K-384 准确率从**0.848**提升到**0.899**,同时比同等 Flash 块自回归基线快**1.20倍**,并把 MBPP-384 从**0.545**提升到**0.693**。Mini-Flash 在 MATH-384 上达到**0.294**,而运行速度比 Flash 快**2.17倍**。
  > 💡 DLM 的核心价值在于双向修订能力,但常规解码只让它退化为块自回归,本文用"草稿+全局修订"把这份能力重新激活,并由此得到一种无需训练的快速生成路径,这是把双向扩散从理论优势落到工程指标的典型方法。
   - 来源: [arXiv cs.CL](https://arxiv.org/abs/2608.02625)

**JoyAI-Video-Edit:16B参数实时开放视频编辑自回归扩散框架**
- JoyAI-Video-Edit是一个**16B参数**自回归扩散框架，面向实时、开放视频编辑，不访问未来帧、不预设视频时长。方法上结合自回归适配与蒸馏，降低train-inference mismatch，并在两步生成中保持源视频保真度与长时序一致性。
  > 💡 把"因果生成"和"两步蒸馏"绑进同一个autoregressive diffusion框架，意味着流媒体实时编辑可以不再依赖完整视频预处理；这种"边生成边编辑"路线对短视频和直播工作流更具落地价值。
   - 来源: [arXiv](https://arxiv.org/abs/2608.03974) | [HuggingFace Daily Papers](https://huggingface.co/papers/2608.03974)

**基础模型博弈论：通过相似性推断通向理性合作的新路径**
- 论文针对自动agent在社会与经济系统中的集体行为，提出区别于经典"decoupled agency"的新博弈论框架。核心发现：当基础模型agent把自身未来行动与外部观测联合预测时，会自然涌现一种基于相似性推断的合作理性，开辟与经典纳什博弈不同的合作路径。
  > 💡 经典博弈论假设agent把自身决策与外界隔离，FM-based agent天然不做这种切分——本文把这种"耦合agency"形式化为可分析的对象，为多agent协作与合作失败的预测提供了新的理论基础。
   - 来源: [arXiv](https://arxiv.org/abs/2608.03958)

**动态分配评估预算：多臂赌博机视角的模型排名**
- 论文把多模型人工评估形式化为correlated arms下的best-arm identification问题，根据中间排名自适应采样，避免穷尽式评估所有模型的所有benchmark题目。方法在保留排名质量的前提下显著降低人工评估成本。
  > 💡 人工评估是LLM排行榜的"金标准"但昂贵到不可扩展，把它建模为bandit问题是评估经济学上的实在进步；这套思路对HLE、BFCL等大型benchmark的直接成本控制有可落地价值。
   - 来源: [arXiv](https://arxiv.org/abs/2608.03437)

### X讨论
**ArtificialAnalysis发布Endpoint Accuracy Index v1.0，量化同模型不同provider的精度损耗**
- ArtificialAnalysis发布Endpoint Accuracy Index v1.0方法学。Index测量"同一个模型由不同provider提供时，能力保留百分比"，benchmark套件包含BFCL v4-500（工具调用，500任务，权重33%）、HLE-250（硬推理，250题，权重33%）、AA-LCR-25（长上下文recall，25题，权重33%）；以self-hosted部署为基线，结果带95%置信区间与统计显著性标记。当前覆盖DeepSeek V4 Pro、GLM-5.2、gpt-oss-120b三个模型。
  > 💡 同一权重不同provider的精度差异长期是行业"公开秘密"但缺乏系统度量；Index把provider差异量化为可对比的统计对象，把采购决策从品牌信任拉到证据层。
   - 来源: [ArtificialAnalysis Methodology](https://artificialanalysis.ai/methodology/endpoint-accuracy-index) | [@ArtificialAnlys](https://x.com/ArtificialAnlys/status/2084702191466725669)

**ZhihuFrontier：自演化AI分三层，只有一层真正通向RSI**
- 知乎前线援引知乎作者周星星的长文，把self-evolving AI按"被改进的对象"分成三层：**Artifact evolution**（改单次输出：代码/算法/模型config，例：Karpathy Autoresearch在700次尝试中保留20次改进，GPT-2 level训练时间从2.02h压到1.80h；AlphaEvolve已为Google基础设施和Gemini训练做出生产级改进）；**Harness evolution**（改agent的"操作系统"：prompt/memory/tool/skill/multi-agent routing，例：Hermes把失败转为SKILL.md，MiniMax M2.7做了100+轮harness分析+重写使内部harness提升30%，Apodex-1.0协调~150个子agent）；**Model evolution**（改权重：自训练/self-play/RL/distillation/test-time training，RSI严格定义要求跨代改进自身的改进过程）。文章给出RSI的5条判定标准：持久改动、外部verifier、compute预算守恒、可迁移到held-out任务、改进过程自身可改进。结论：当前大多数系统只满足前2-3条，真正的RSI尚未到来，但Artifact→Harness→Model的渐进闭环正在闭合。
  > 💡 这个三层框架为RSI的营销泡沫提供了一个去伪存真的工具：很多"self-improving agent"其实是artifact evolution，改harness不等于改模型；文章引用的Ai2研究（Harness evolution在Terminal-Bench上未超过parallel sampling）是重要的反例数据，说明搜索预算必须先被控制才能归因到evolution本身。
   - 来源: [@ZhihuFrontier](https://x.com/ZhihuFrontier/status/2084525505878073466) | [周星星知乎原文](https://zhuanlan.zhihu.com/p/206522731397)

**steipete：用codex + 视频KVM让agent自验证OpenClaw的iMessage集成**
- Peter Steinberger（@steipete，OpenClaw核心开发者）分享了一个让codex agent自己完成e2e测试的case study：因为iMessage在VM里不可靠、且已读回执等功能需要SIP被禁用（在VM中做不到），他给codex配置了一个带视频输入的远程KVM，agent通过KVM直接操作一台真实Mac，端到端自动化测试OpenClaw的iMessage集成。推文引发大量讨论，被评论称为"迄今为止看到最干净的agent自验证方案"。
  > 💡 这是agent突破"沙盒无法触达真实状态"限制的一个具体案例：当被测系统无法虚拟化时，最直接的方案是给agent一双"眼睛"和真实硬件操作权；本质上把verify-the-work从agent自己的output loop里外化到物理世界上。
   - 来源: [@steipete](https://x.com/steipete/status/2084988316324397312)

---
*更新时间: 2026-08-06 09:30*
