## 07月30日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 23 条

---

## 要点汇总

- 模型前沿：OpenAI披露GPT-5.6全栈效率优化，生产推理成本降低20%; 马斯克预告Grok 4.6于8月7日前后发布，Grok 4.7数周后跟进
- 产业动态：OpenAI开源Codex Security CLI与TypeScript SDK; Thinking Machines联合创始人Lilian Weng离职后重返OpenAI; OpenAI科研计划拟免费覆盖10万名研究者，ChatGPT周活逼近10亿; Unsloth发布Kimi K3 1-bit量化版本，权重体积由1.56TB缩至594GB; 美国禁止进口新款外国制造人形机器人、机器狗与逆变器; 微软季度营收900亿美元，Anthropic投资收益32亿美元、OpenAI减记约6亿美元; Meta二季度营收增28%但营业利润下滑8%，AI投入与一次性成本拖累盈利
- 算力追踪：SemiAnalysis追踪全球60GW以上模块化数据中心产能; SemiAnalysis估算2028年全球晶圆厂设备WFE市场或超2300亿美元，扩产与提价共同驱动
- 初创&融资：月之暗面融资超35亿美元，投后估值350亿美元并筹备Pre-IPO轮; Encore AI融资3000万美元，将客户沟通知识转化为销售Agent打法; Pangram融资900万美元并发布AI文本与图像检测模型
- 研究关注：Pigey以高层编排弥合机器人“会动不会想”的差距; WorldDiT统一动作生成与视觉世界建模; HiFi-UMI：用高保真便携数据采集系统支撑零真机后训练; ACM让Agent自主编辑上下文并按需调用外置长期记忆; RARG：用相关性排序引导Agent直接检索语料; Relay-OPD：让教师模型在错误推理前缀处短暂接棒
- X讨论：保留推理与上下文压缩令GPT-5.6 Sol的ARC-AGI-3得分提高近3倍; Dream-Cubed开源Minecraft体素生成数据、模型与代码; Grok Voice Think Fast 2.0以0.70秒首段音频延迟进入语音模型榜单第二

---

## 📖 详细参考

### 模型前沿
**OpenAI披露GPT-5.6全栈效率优化，生产推理成本降低20%**
- OpenAI表示，GPT-5.6模型家族从训练、推理到Agent编排层共同优化“每单位成本的智能”。其中GPT-5.6 Sol协助分析生产流量、改写GPU内核并优化推测解码：内核等优化使端到端服务成本降低20%，改进后的草稿模型又将token生成效率提升15%以上；在产品层，Terra以GPT-5.5级别能力实现约一半价格，Luna价格则比Sol低80%。
  > 💡 这次披露的重点不是单一模型分数，而是模型开始反过来优化承载自己的推理栈；当负载均衡、内核、缓存与上下文管理的收益叠加，前沿能力的竞争会越来越转向“智能/美元”而非只看榜单峰值。
   - 来源: [@OpenAI](https://x.com/OpenAI/status/2082577278450676080)、[OpenAI](https://openai.com/index/gpt-5-6-frontier-intelligence-efficiency/)

**马斯克预告Grok 4.6于8月7日前后发布，Grok 4.7数周后跟进**
- Elon Musk表示，Grok 4.6预计于8月7日前后发布，规模为1.5T参数，并将显著改进监督微调（SFT）与强化学习（RL）；随后数周发布的Grok 4.7预计为2.1T参数，除服务速度略慢外将全面优于4.6，并具备更高token效率。该帖未给出独立技术报告或评测结果，具体规格仍待xAI正式发布确认。
  > 💡 在同一代内快速推出两个不同规模版本，显示xAI可能以“更快服务”和“更强能力”分层覆盖需求；但参数规模与宣称的token效率不能直接等同于真实任务性价比，仍需等待API价格和第三方评测。
   - 来源: [@elonmusk](https://x.com/elonmusk/status/2082123925283041545)

### 产业动态
**OpenAI开源Codex Security CLI与TypeScript SDK**
- OpenAI发布开源Codex Security，可用于扫描代码仓库、跨运行跟踪漏洞发现、验证修复，并把安全检查接入CI/CD。项目提供CLI和TypeScript SDK，支持ChatGPT登录或API Key认证；当前属于早期版本，要求Node.js 22及以上、Python 3.10及以上并具备Codex Security访问权限。
  > 💡 把“发现—验证—修复—持续集成”放进同一套Agent工作流，比只生成一次性安全报告更接近真实DevSecOps；开源CLI也降低了团队在现有流水线中试用和审计的门槛。
   - 来源: [@OpenAI](https://x.com/OpenAI/status/2082263717916586117)、[GitHub：openai/codex-security](https://github.com/openai/codex-security)

**Thinking Machines联合创始人Lilian Weng离职后重返OpenAI**
- TechCrunch报道称，Thinking Machines Lab联合创始人Lilian Weng此前以健康原因为由离开公司，随后加入OpenAI。据OpenAI发言人向TechCrunch透露，Weng将领导一个高层团队，专注于加速OpenAI内部研究，支持跨研究工作在**递归自我改进**方向的合作。Weng在加入Thinking Machines前曾于OpenAI工作七年，并担任安全系统研究副总裁。
  > 💡 联合创始人从新实验室回流原公司并不常见，尤其Weng兼具Agent研究与安全体系经验；她此次领导内部研究加速团队，聚焦递归自我改进，说明OpenAI正把这一方向作为长期竞争力重点布局。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/29/thinking-machines-co-founder-lilian-weng-left-the-company-citing-health-reasons-then-joined-openai/)

**OpenAI科研计划拟免费覆盖10万名研究者，ChatGPT周活逼近10亿**
- OpenAI推出ChatGPT for Academic Researchers，首批面向1万名科学家、数学家和工程师，并计划在2027年扩展至10万人；参与者可免费使用包括GPT-5.6 Sol Pro在内的前沿模型、ChatGPT Work、Codex及更高额度的深度研究能力，工作区默认不使用研究者数据训练模型。该计划属于OpenAI截至2027年投入超过2.5亿美元支持外部科研的承诺。另外，The Information援引OpenAI内部消息称，ChatGPT周活跃用户正逼近10亿；这一目标原计划在去年年底达成，目前比预期晚约七个月。
  > 💡 该计划的核心是降低外部研究者使用前沿模型和Agent工具的门槛；接近10亿的周活数据说明其依托的平台覆盖面较大，但现有信息不足以判断科研计划的实际使用效果，或它对用户增长和模型研发反馈的贡献。
   - 来源: [The Information](https://www.theinformation.com/articles/openais-chatgpt-nears-1-billion-weekly-active-users-seven-months-target)、[@OpenAI](https://x.com/OpenAI/status/2082516370949062989)、[OpenAI](https://openai.com/index/chatgpt-for-academic-researchers/)

**Unsloth发布Kimi K3 1-bit量化版本，权重体积由1.56TB缩至594GB**
- Unsloth发布Kimi K3本地运行指南与GGUF量化权重，将其Q8版本的1.56TB体积压缩至1-bit版本的594GB，减少约62%；Unsloth按自身量化评测口径称，1-bit版本保留约78.9%的准确率，并可通过内存与磁盘卸载，在Mac Studio连接一台128GB内存设备的配置上运行。Kimi K3共有2.8万亿参数，支持100万token上下文与原生多模态；594GB仅为权重体积，实际运行仍需要额外内存和存储空间。
  > 💡 594GB仍远非普通个人电脑可轻松承载，但1-bit量化把超大MoE模型从“只能在集群运行”推进到高端工作站可实验的范围；真正可用性仍取决于内存带宽、磁盘卸载速度与量化后的具体任务损失。
   - 来源: [@Unsloth](https://x.com/UnslothAI/status/2082463988953367031)、[Unsloth](https://unsloth.ai/docs/models/kimi-k3)

**美国禁止进口新款外国制造人形机器人、机器狗与逆变器**
- 特朗普政府以“不可接受”的国家安全威胁为由，禁止进口新款外国制造的人形机器人、机器狗和电力逆变器。报道称该措施主要影响占据全球大部分市场份额的中国供应商。美国联邦通信委员会（FCC）称，海外制造设备可能被外国政府远程控制、用于监视或参与网络攻击；若政府认定具体设备不构成国家安全风险，可给予例外。2025年全球人形机器人出货量约1.5万台，中国两家最大机器人厂商分别占其中相当大比例；已安装在家庭及其他设施中的现有逆变器不受此次禁令影响。
  > 💡 人形机器人、机器狗与逆变器被同时纳入限制，显示监管范围已从单一机器人产品扩大到可感知、联网或影响关键基础设施的智能硬件；中国厂商进入美国市场将更依赖逐项风险认定与个案豁免。
   - 来源: [The Information](https://www.theinformation.com/briefings/trump-administration-bans-new-humanoid-robots-china)、[TechCrunch](https://techcrunch.com/2026/07/29/us-government-bans-new-foreign-made-humanoids-robot-dogs-and-solar-inverters-citing-risks-to-national-security)

**微软季度营收900亿美元，Anthropic投资收益32亿美元、OpenAI减记约6亿美元**
- 微软2026财年第四季度营收同比增长18%至900亿美元，增速与上一季度持平；AI相关销售增长被Xbox和Windows设备业务下滑部分抵消。Office 365 Copilot付费订阅已超过3000万，高于此前披露的2000万。投资方面，微软当季确认Anthropic投资收益32亿美元，使摊薄每股收益增加0.33美元；同期对OpenAI投资减记约6亿美元、每股收益减少约0.07美元，但OpenAI投资全年仍贡献约50亿美元收益。微软曾于2025年11月投资Anthropic 50亿美元，Anthropic同时承诺采购300亿美元Azure服务；微软目前持有OpenAI约27%股份。
  > 💡 微软的季度数据同时呈现三条AI变现路径：Copilot订阅继续增长，Anthropic投资带来显著账面收益，OpenAI投资则出现单季波动；但AI增量尚未完全抵消部分传统业务下滑，产品收入、云服务采购与股权投资正共同影响其AI回报。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/29/microsoft-logs-3-2b-from-anthropic-investment-but-openai-was-a-mixed-bag/)、[The Information](https://www.theinformation.com/briefings/microsofts-rising-ai-sales-fail-boost-overall-growth-june-quarter)

**Meta二季度营收增28%但营业利润下滑8%，AI投入与一次性成本拖累盈利**
- Meta Platforms二季度营收同比增长28%，但营业利润同比下滑8%。盈利下降被归因于AI投资相关的成本显著上升以及部分一次性费用。CEO Mark Zuckerberg在电话会上表示，公司正在评估对外出租多余算力的可能性，并指出已收到大量以溢价求购算力的报价。
  > 💡 Meta算力出现过剩信号是个关键拐点：自建集群通常按峰值训练需求设计，一旦训练峰值回落就会出现冗余；对外租算力既能摊销折旧，也使Meta有机会从纯AI消费者变成算力供应商。
   - 来源: [The Information](https://www.theinformation.com/briefings/meta-shares-fall-profits-drop)

### 算力追踪
**SemiAnalysis追踪全球60GW以上模块化数据中心产能**
- SemiAnalysis的模块化数据中心追踪器覆盖超过61GW产能和1000多个采用模块化或预制策略的站点，并估算这类方案到2028年底将覆盖全球已投运数据中心容量的30%以上。其自下而上测算显示，将墙板、电力房、冷却撬块等重复性工作移至工厂，可令整体建设周期缩短约36%（7至9个月）、单位MW资本开支降低约8%；仅将约占项目内容26%的电力系统模块化，就可把机房达到IT-ready状态的时间由约16.7个月缩至13个月，单位MW成本降低约5%。文章将熟练电工和管道工短缺列为主要推动因素，并区分了具体环节：AWS Project Houdini把白区安装由数月压缩至数周，Meta的织物外壳设施只加快建筑围护，并不缩短并网、供电、冷却和调试流程；在供应商侧，SemiAnalysis估算Vertiv提供全栈模块化方案后，每MW可获取的设备内容价值由约350万美元升至700万美元。
  > 💡 AI集群建设开始从“一座座定制工程”转向可复制的标准模块，交付速度和供应链集成能力由此成为新瓶颈；但“模块化”口径混乱，供应商宣称仍需用实际交付周期、功率密度和每兆瓦成本验证。
   - 来源: [@SemiAnalysis](https://x.com/SemiAnalysis_/status/2082590316268294179)、[SemiAnalysis](https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters)

**SemiAnalysis估算2028年全球晶圆厂设备WFE市场或超2300亿美元，扩产与提价共同驱动**
- SemiAnalysis称，华尔街对2028年全球晶圆厂设备（WFE）市场的预测约为1900亿至2000亿美元；若前五大设备厂商按当前价格售罄已规划产能，其测算的市场规模将**超过2300亿美元**。价格方面，SemiAnalysis援引ASML财报、台积电指引及渠道信息称，同类设备提价已经开始讨论：中国客户据报接受DUV设备约**10%**的涨价，Tokyo Electron被指正讨论约**30%**的涨幅；台积电也将设备价格上涨列为资本开支指引增加**15%**的重要原因。SemiAnalysis判断设备商具备更强议价能力，并估算同类设备价格若提高10%，头部设备商毛利率可能比历史峰值高**1至5个百分点**。
  > 💡 超过2300亿美元是建立在头部厂商规划产能全部售出、现有价格维持的情景测算，并非市场共识预测；更高的收入和毛利率还取决于提价能否落地、需求能否消化新增产能。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2082519754426757434)

### 初创&融资
**月之暗面融资超35亿美元，投后估值350亿美元并筹备Pre-IPO轮**
- 据报道，月之暗面最新一轮融资超过35亿美元，投后估值达到350亿美元；公司已接触潜在投资者，拟以500亿美元投前估值启动Pre-IPO融资，并为年内赴港上市做准备，此前还被曝就上市事宜与中金公司和高盛接洽。报道同时称，其年化收入（ARR）从2026年4月的2亿美元升至6月的3亿美元，收入来源包括Kimi个人订阅、企业API和6月推出的Kimi Work；公司在2025年末完成5亿美元C轮融资、投后估值43亿美元，2026年5月又完成估值200亿美元的D轮融资。Kimi K3于7月16日发布，模型规模为2.8万亿参数，随后被Cursor集成；Artificial Analysis披露，完成其全套评测约消耗1.3亿输出token、总成本2709.75美元。上述融资、估值、ARR与上市安排均来自媒体援引的知情人士或第三方数据，月之暗面尚未逐项公开确认。
  > 💡 月之暗面的估值上升同时依赖模型突破、收入增长与上市预期：ARR快速增长提供基本面支撑，Kimi K3扩大海外技术影响力，而500亿美元Pre-IPO目标则把市场对开源模型的认可提前计入资本定价；后续关键是把模型热度转化为可持续毛利与企业客户留存。
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14701580)、[腾讯科技](https://mp.weixin.qq.com/s/RmMsCT-JbwhSFjIGOzwAQA)

**Encore AI融资3000万美元，将客户沟通知识转化为销售Agent打法**
- Encore AI完成3000万美元融资。公司称其产品会分析客户电话、消息与CRM数据，从中识别表现较好的销售做法，再将这些模式整理成可供AI Agent执行的销售手册；报道未披露其识别方法、客户部署规模或相对现有销售工具的量化效果。
  > 💡 与通用销售助手相比，Encore把企业自身对话数据变成可执行策略，价值更接近“持续学习的销售操作系统”；其护城河取决于能否区分相关性与真实因果，并避免把少数优秀销售的偶然做法固化为自动化偏差。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/29/encore-ai-raises-30m-to-build-ai-agents-that-learn-from-customer-calls/)

**Pangram融资900万美元并发布AI文本与图像检测模型**
- AI内容检测公司Pangram融资900万美元，用于扩展其检测软件；公司同时发布新一代文本检测模型Pangram 4，并以研究预览形式推出AI图像检测模型。产品面向AI内容快速涌入互联网后产生的来源识别与真实性验证需求。
  > 💡 检测赛道正从单一文本分类扩展到多模态来源验证，但生成模型与检测模型之间仍是持续对抗；商业落地的核心不只是准确率，还包括跨模型泛化、误伤人类作者的成本以及可解释证据链。
   - 来源: [TechCrunch](https://techcrunch.com/2026/07/29/as-ai-content-floods-the-internet-pangram-raises-9m-to-detect-it/)

### 研究关注
**Pigey以高层编排弥合机器人“会动不会想”的差距**
- 论文将通用机器人能力拆分为语言条件控制策略与高层Agent编排器，提出闭环Physical Agency编排器Pigey。它可规划、分解子目标、调用VLA策略或参数化技能、验证结果并从失败中恢复，无需额外采集数据或后训练；在LIBERO-PRO上将成功率从12.8%提升至53.3%，真实机器人推理受限任务则从接近零提升到90%以上。
  > 💡 结果表明，机器人策略的瓶颈未必都要靠更大规模端到端预训练解决；在冻结运动策略之上增加能观察、验证和恢复的Agent循环，就可能释放已有技能中被编排缺陷掩盖的能力。
   - 来源: [@Liane Galanti](https://x.com/lianegalanti/status/2082146266461405552)、[arXiv](https://arxiv.org/abs/2607.21725)

**WorldDiT统一动作生成与视觉世界建模**
- WorldDiT使用单一扩散Transformer同时生成连续动作块，并预测未来相机画面的归一化RGB patch，无需大型预训练VLM充当动作骨干。在四个LIBERO仿真套件上，它在公开报告全部四套结果的方法中处于“总参数量—平均成功率”帕累托前沿，形成一个十亿参数以下的世界模型与控制统一基线。
  > 💡 同一网络同时学习“接下来会看到什么”和“接下来该怎么动”，使世界预测成为动作学习的内在监督；若小模型也能维持竞争力，机器人控制可能不必完全依赖越来越大的通用VLM。
   - 来源: [@Bagel](https://x.com/bageldotcom/status/2082179134336512366)、[arXiv](https://arxiv.org/abs/2607.23909)

**HiFi-UMI：用高保真便携数据采集系统支撑零真机后训练**
- HiFi-UMI是一套无需外部追踪设施的便携式机器人示范采集系统：它结合头戴式离线立体惯性SLAM、双手夹爪相对位姿的直接测量、共享微秒级GPIO触发器，以及每只手两台、总视场约200°的广角相机；作者报告末端执行器在工作空间内的定位精度为3毫米。仅用HiFi-UMI示范后训练的策略可直接部署到真机，在StarVLA-QwenPI、OpenPI-pi_0.5和LingBot-VA三种基干上，与场景内遥操作数据训练的基线相比，成功率分别相差-2.5、+3.1和-0.6个百分点；最强策略在精密插入任务上达到85%成功率。进一步使用同一采集体系的4000小时数据预训练后，模型在10个未见任务上的动作误差降低41%，StarVLA-QwenPI的真机成功率提升18.1个百分点。团队还开源了包含2000小时演示的HiFi-UMI-2K；以上结果均为论文在其所选任务、机器人平台和评测设置下的报告。
  > 💡 把“保真度”做高而非缩减“真机比例”，使通用UMI数据从预训练语料升级为可直接支撑后训练和部署的数据源；如果结果可跨更多硬件复现，机器人团队对昂贵遥操作设备与目标场景采集的依赖将明显下降。
   - 来源: [Hugging Face Papers](https://huggingface.co/papers/2607.25895)、[arXiv](https://arxiv.org/abs/2607.25895)

**ACM让Agent自主编辑上下文并按需调用外置长期记忆**
- 论文提出Agentic Context Management（ACM），为长时程Agent提供专用上下文编辑工具：Agent可自主决定何时压缩，把被移出的内容存入外部记忆，并在后续按需检索。作者还构建后训练流程生成高质量上下文管理示范，在Agent搜索与编码任务上提升表现，同时降低峰值token压力并提高多次独立运行的一致性。
  > 💡 ACM把上下文压缩从固定阈值触发的系统操作变成Agent可学习的行为，并通过外置记忆降低不可逆信息损失；这与OpenAI在ARC-AGI-3上的发现共同表明，“如何记忆”正成为长时程Agent能力的一部分。
   - 来源: [arXiv](https://arxiv.org/abs/2607.23809)

**RARG：用相关性排序引导Agent直接检索语料**
- 论文指出，传统检索Agent通常只用相关性选择top-k文档，难以对复杂问题所需证据进行定位、组合和验证；grep式直接语料交互虽能进行更细粒度的探索，却可能因不考虑相关性而较晚发现关键线索。作者提出Relevance-Aware RipGrep Search Agent（RARG），先按相关性安排文档遍历顺序，再用查询相关段落初始化入口，并重排grep匹配片段。在论文选取的高难浏览问答与推理密集型检索任务上，作者报告RARG相较检索型和直接交互型Agent改善了准确率—效率前沿，并称搜索收敛更快、更稳定；论文未在摘要中给出统一的绝对提升幅度，代码已开放。
  > 💡 RARG没有把检索和Agent式浏览视作二选一，而是用检索分数决定“先搜索哪里、先看哪些匹配”；这类混合策略尤其适合代码库、论文集和企业文档等既大又需要精确证据拼接的语料。
   - 来源: [Hugging Face Papers](https://huggingface.co/papers/2607.24223)、[arXiv](https://arxiv.org/abs/2607.24223)

**Relay-OPD：让教师模型在错误推理前缀处短暂接棒**
- 论文聚焦在线策略蒸馏（OPD）的“前缀失败”问题：学生模型早期走错方向后，后续生成会沿错误轨迹继续延伸，使监督信号失真并浪费计算。Relay On-Policy Distillation（Relay-OPD）利用教师与学生在失败前缀上的续写差异作为无标签触发信号，由教师在触发点短暂接管生成，再交还学生继续完成并学习。实验以Qwen3-4B-Instruct-2507为教师、Qwen3-0.6B和1.7B非思考模型为学生，在8个数学推理基准上均取得最佳或次佳结果；其中1.7B学生的平均成绩比标准OPD高5.73%，比FastOPD高1.49%，训练轨迹长度减少50%以上。
  > 💡 相比让教师全程代写高质量答案，Relay-OPD只在学生即将“越走越偏”时介入，因此既保留学生自身分布，又把昂贵教师算力用在关键转折点；这一思路也可扩展到长链Agent轨迹的局部纠偏。
   - 来源: [Hugging Face Papers](https://huggingface.co/papers/2607.26057)、[arXiv](https://arxiv.org/abs/2607.26057)

### X讨论
**保留推理与上下文压缩令GPT-5.6 Sol的ARC-AGI-3得分提高近3倍**
- OpenAI发现，ARC-AGI-3官方评测框架会在每次动作后丢弃私有推理，并通过滚动截断移除较早历史，导致Agent反复重新理解游戏。改用Responses API并开启“保留推理”和上下文压缩后，GPT-5.6 Sol在公开任务集上的RHAE得分从13.3%升至38.3%，同时输出token减少约6倍；OpenAI估算人类测试者平均得分约48%。
  > 💡 结果说明Agent评测不只测模型，也在测上下文与编排框架；当长期任务依赖跨步骤学习时，丢弃推理状态可能系统性低估模型能力，也让不同评测框架之间的横向比较更难成立。
   - 来源: [@OpenAI](https://x.com/OpenAI/status/2082616636989952217)、[OpenAI研究](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/)

**Dream-Cubed开源Minecraft体素生成数据、模型与代码**
- Sakana AI与纽约大学合作发布Dream-Cubed：包含**数百亿token**的Minecraft体素世界数据集，以及直接在方块空间生成交互式3D环境的扩散模型家族。数据混合程序化生物群系地形与高质量玩家地图，模型支持连续和离散两种扩散训练目标，可实现基于用户方块的局部重绘、向外扩展与用户条件生成；团队开源完整数据集、代码与预训练模型，并以适配后的FID指标和人类偏好研究评估生成质量。据作者介绍，这是**首个**针对体素生成的大规模3D扩散模型研究。
  > 💡 直接在离散方块空间建模，比先生成视频或网格再转换更适合可编辑、可交互的世界；开放的大规模结构化3D数据也可成为研究世界模型、游戏内容生成与具身Agent环境的公共底座。
   - 来源: [Sakana AI](https://sakana.ai/dream-cubed/)、[arXiv](https://arxiv.org/abs/2604.22847)、[交互项目页](https://pub.sakana.ai/dream-cubed)

**Grok Voice Think Fast 2.0以0.70秒首段音频延迟进入语音模型榜单第二**
- 据Artificial Analysis，Grok Voice Think Fast 2.0 High在Speech-to-Speech Index以82.9%位列第二，仅次于Qwen Audio 3.0 Realtime Plus的84.1%，较上一代的75.7%提升7.3个百分点；它在衡量Agent语音能力的Tau Voice上以56.5%排名第一，在Full Duplex Bench子集上由上一代的77.8%升至95.1%。模型平均首段音频时间为0.70秒，是榜单前五中唯一低于1秒的模型；输入音频价格为每小时4.80美元，高于上一代的3美元，但约为GPT-Realtime-2.1 High价格的45%。
  > 💡 实时语音模型需要同时平衡理解、Agent执行、双工打断、延迟与价格，单一综合分数难以覆盖全部体验；Grok此次最明显的优势是把前沿档能力和亚秒级响应结合，但价格已高于部分直接竞品。
   - 来源: [Artificial Analysis](https://x.com/ArtificialAnlys/status/2082528987272957960)

---
*更新时间: 2026-07-30 09:14*
