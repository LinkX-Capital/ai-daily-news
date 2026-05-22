## 05月22日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：Cohere发布Command A+：25B激活参数MoE模型
- 产业动态：Anthropic预计Q2运营盈利，Q2季度收入约109亿美元; 智谱ZCube训练速度提升3%-7%、网络成本降低26%-46%
- 算力追踪：Nvidia提出2000亿美元Agent CPU市场，Vera今年已售200亿美元; Epoch AI报告前沿实验室用不到全球50%算力; Anthropic与Microsoft洽谈使用自研AI芯片
- 初创&融资：AI搜索公司ExaExa完成2.5亿美元C轮融资; AI个人助理公司Hark完成7亿美元A轮融资，估值60亿美元
- 研究关注：中科大等提出EffOPD：参数动力学"预见"机制实现后训练3倍加速; 谢赛宁团队RAEv2收敛速度提升10倍; PlexRL：集群级RLVR训练调度，GPU成本降低最高37.58%

---

## 📖 详细参考

### 模型前沿
**Cohere发布Command A+：25B激活参数MoE模型，Apache 2.0开源**
- Cohere发布Command A+模型，采用MoE架构，**总参数218B、激活参数25B**，配备**128个专家（每token激活8个+1个共享专家）**，支持**128K上下文长度**。模型支持视觉输入、工具调用和推理能力，覆盖**48种语言**。采用**W4A4量化**后可部署在单张B200 GPU上。模型以**Apache 2.0协议开源**。
  > 💡 Command A+以Apache 2.0开源218B参数MoE模型，在开源权重的大模型中属于第一梯队，对Meta Llama系列和Mistral构成直接竞争压力。
   - 来源: [Cohere (X)](https://x.com/cohere/status/2057120818551734589) | [HuggingFace](https://huggingface.co/CohereLabs/command-a-plus-05-2026-w4a4)

### 产业动态
**Anthropic预计Q2实现运营盈利，Q2季度收入约109亿美元**
- Anthropic预计在6月底结束的第二季度实现**5.59亿美元运营利润**，这是公司首次实现运营层面的盈利。TechCrunch报道，Anthropic **Q2季度收入预计约109亿美元**，较上季度翻倍以上。作为参考，其2024年全年收入约为10亿美元。OpenAI Q1收入约**57亿美元**，领先Anthropic约10亿美元。Anthropic同时表示，由于后续训练前沿模型的大额算力支出，**全年可能不会持续保持盈利**。
  > 💡 Anthropic实现运营盈利表明AI基础模型公司的商业化路径开始跑通，但公司自身预计难以全年持续盈利，说明盈利与训练投入之间的拉锯仍是常态。与OpenAI的收入差距正在缩小，两家公司的竞争进入新阶段。
   - 来源: [The Information](https://www.theinformation.com/briefings/anthropic-projects-turning-operating-profit-second-quarter) | [TechCrunch](https://techcrunch.com/2026/05/20/anthropic-says-its-about-to-have-its-first-profitable-quarter/) | [The Information (OpenAI收入)](https://www.theinformation.com/articles/openai-held-1-billion-revenue-lead-anthropic-first-quarter)

**智谱ZCube：新型数据中心网络拓扑，LLM训练速度提升3%-7%，网络成本降低26%-46%**
- 智谱发布ZCube网络拓扑方案及自动化拓扑优化管道ATOP。论文将网络拓扑建模为超参数优化问题，在256至16384 GPU规模下优化LLM训练流量模式下的集合通信性能、容错能力和网络成本。仿真结果显示，ZCube相比此前最优拓扑（ROFT、Rail-only、HPN），**端到端LLM训练速度提升3%-7%**，**网络硬件成本降低26%-46%**。在真实测试环境中，ZCube在保持相同all-reduce和all-to-all性能的同时，硬件成本降低**25%**。
  > 💡 ZCube从网络拓扑层面而非GPU虚拟化层面优化训练效率，是算力紧缺背景下务实的系统创新。若在大规模生产环境中验证有效，可能成为大规模训练集群的标配方案。
   - 来源: [ACM](https://dl.acm.org/doi/epdf/10.1145/3718958.3750503) | [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651034260&idx=1&sn=79d1469b24b4a814ece601bcc00a5f95&chksm=8506215cd17a5b29218aca5f08f8e19029f27eedd0a76698c94be238d7e7487cf85bc9675e20&scene=0&xtrack=1#rd)

### 算力追踪
**Nvidia CEO Jensen Huang提出2000亿美元Agent CPU市场，Vera今年已售200亿美元**
- Nvidia发布2026财年Q1财报，**营收816亿美元**，再创纪录，下季度指引**910亿美元**。CEO Jensen Huang在财报电话会上提出，公司Vera CPU产品打开了**2000亿美元的新TAM（总可触达市场）**，定位为"全球首个专为Agentic AI设计的CPU"。Huang解释称，AI代理执行任务时主要运行在CPU上而非GPU上，Vera专为高速token处理设计，区别于传统云架构CPU的多核设计。Huang透露，**Vera CPU今年已售出200亿美元**（独立销售，不含与Rubin GPU捆绑的部分）。此前AWS与Meta签署了大规模自研AI CPU合同，显示CPU市场竞争正在加剧。
  > 💡 Huang将Agent时代的CPU定位为Nvidia的下一个增长引擎，且200亿美元已售数据表明这不是空谈。但AWS等云厂商正大力推进自研芯片，Nvidia能否在CPU市场复制GPU市场的统治地位仍有待观察。
   - 来源: [TechCrunch](https://techcrunch.com/2026/05/20/jensen-huang-says-hes-found-a-brand-new-200b-market-for-nvidia/)

**Epoch AI分析：前沿实验室仅使用全球不到50%AI算力**
- Epoch AI发布全球AI算力分析报告，估计全球已售出约**2000万张H100等效GPU**，其中约**1600万张正在运行**。按公司分布，OpenAI约**170万张H100e**（对应1.9 GW功耗），Anthropic约**100万张以上**，xAI约60-70万张。报告指出，**前沿实验室合计使用的算力不到全球总量的50%**，其余算力分布在其他科技公司、云服务商和学术机构中。
  > 💡 这组数据首次系统性地揭示了全球AI算力的分布格局。"前沿实验室用不到一半"意味着AI算力的需求方比想象中更加分散，非前沿实验室的AI应用正在成为算力消耗的重要力量。
   - 来源: [Epoch AI](https://epochai.substack.com/p/frontier-labs-dont-use-most-ai-compute)

**Anthropic正与Microsoft洽谈使用其自研AI芯片**
- Anthropic正在与Microsoft洽谈**租赁搭载Microsoft自研AI芯片的服务器**，以满足日益增长的算力需求。此前Microsoft的自研芯片主要通过Azure云服务供OpenAI使用。
  > 💡 Anthropic此前主要依赖Google TPU和AWS算力，若转向Microsoft自研芯片，说明AI公司正在积极多元化算力来源以降低对单一供应商的依赖，也反映出Microsoft自研芯片的竞争力正在被市场验证。
   - 来源: [The Information](https://www.theinformation.com/articles/anthropic-talks-use-microsofts-ai-chips)
   
### 初创&融资
**Hark完成7亿美元A轮融资，投后估值60亿美元**
- AI个人助理公司Hark宣布完成**7亿美元A轮融资**，**投后估值60亿美元**，由Parkway Venture Capital领投，Nvidia、AMD Ventures、Intel Capital、Qualcomm Ventures、Salesforce Ventures等跟投。创始人兼CEO Brett Adcock（此前创立Figure AI和Archer Aviation）于**2025年底**用**1亿美元自有资金**创办Hark，目前团队**70人**，运行配备Nvidia B200 GPU的数据中心。Hark计划今年夏天发布首批多模态模型，随后推出配套硬件设备。公司设计总监为前Apple产品高管Abidur Chowdhury。Hark定位为"通用AI接口"，但目前公开产品信息有限。
  > 💡 7亿美元A轮是年内AI硬件赛道最大融资之一，投资方涵盖Nvidia/AMD/Intel/Qualcomm四大芯片厂商极为罕见，显示行业对AI原生硬件+软件栈的押注。但Hark产品尚未面世，高额融资与有限信息公开之间的落差值得关注。
   - 来源: [TechCrunch](https://techcrunch.com/2026/05/21/hark-raises-700m-series-a-for-its-secretive-universal-ai-interface/)

**AI搜索公司Exa完成2.5亿美元C轮融资，投后估值22亿美元**
- AI搜索引擎研发商Exa宣布完成**2.5亿美元C轮融资**，**投后估值达22亿美元**，由a16z领投，a16z合伙人Sarah Wang主导本轮交易，Benchmark等跟投。Exa由Will Bryk和Jeffrey Wang于**2021年**创立（前身为Metaphor Systems），基于自监督学习模型，通过输入文本来预测网址，专为AI构建搜索引擎。该公司定位为Agent时代的搜索基础设施。2023年Exa曾完成1700万美元A轮融资。
  > 💡 这是年内AI搜索赛道最大规模融资之一，显示a16z对AI Agent工作流中原生搜索基础设施的看好，Exa需证明其能抢占Google搜索市场份额。
   - 来源: [DeepTech深科技](http://mp.weixin.qq.com/s?__biz=MzA3NTIyODUzNA==&mid=2649796907&idx=1&sn=2d2f41aecf2027b75a12d48f65843b7e&chksm=86839ea9d6080b6e6fa6d7d1c7857083b829c27dd04b23a094ffdd4fe09ce19a99d8ef12de22&scene=0&xtrack=1#rd)

### 研究关注
**中科大等提出EffOPD：参数动力学"预见"机制实现后训练3倍加速**
- 中国科学技术大学等机构研究团队发表论文"Learning to Foresee"，揭示On-Policy Distillation（OPD）高效的原因。研究发现OPD的效率源于一种"预见"能力：在训练早期就建立起指向最终模型的稳定更新轨迹。这种预见体现在两个层面——**模块分配层面**，OPD识别低边际效用区域并将更新集中在关键推理模块上；**更新方向层面**，OPD表现出更强的低秩集中性，其主导子空间在训练早期就与最终更新子空间对齐。基于这些发现，团队提出**EffOPD**方法，通过自适应选择外推步长沿当前更新方向前进，在无需额外可训练模块或复杂超参数调优的情况下，实现**平均3倍训练加速**，同时保持最终性能。
  > 💡 OPD效率的"预见"机制解释为后训练方法设计提供了参数动力学视角的理论基础，EffOPD作为即插即用的加速方案有较高的实用价值。
   - 来源: [arXiv](https://arxiv.org/abs/2605.11739) | [PaperWeekly](https://mp.weixin.qq.com/s?__biz=MzIwMTc4ODE0Mw==&mid=2247720422&idx=2&sn=c796e7fc0a37726acbfdd4f938096894)

**谢赛宁团队发布RAEv2：收敛速度较原版RAE提升10倍，ImageNet gFID 1.06**
- 谢赛宁团队发布RAEv2（Improved Baselines with Representation Autoencoders），对表征自编码器（RAE）的设计进行了系统性改进。研究发现三个关键洞察：将表征定义为编码器最后k层的求和而非仅最后一层，大幅提升重建质量；RAE与REPA（表征对齐）具有互补机制，可同时使用；通过对DiT输出的简单重参数化，实现无需额外训练模型的"免费"引导。RAEv2在ImageNet-256上以**仅80个epoch达到gFID 1.06**，较原版RAE的收敛速度提升**10倍以上**。在FDr^k指标上以80 epoch达到**2.17**，超越此前800 epoch的3.26最佳成绩。该方法在文生图和导航世界模型中也验证了一致性改进。
  > 💡 RAEv2的训练效率提升（35 epoch达到gFID≤2，原版需177 epoch）对图像生成领域有实际价值，大幅降低了表征自编码器的训练成本。论文已开源代码。
   - 来源: [arXiv](https://arxiv.org/abs/2605.18324v1) | [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651034260&idx=2&sn=3b6bb8eeaf3ee411d721c1981557b1f2&chksm=85060d508aae1012e0d98cda37bf0db9adefa1f71d4fc9514c7635194e8f00f6b0b5f13a797c&scene=0&xtrack=1#rd)

**PlexRL：集群级RLVR训练调度，GPU成本降低最高37.58%**
- 论文提出PlexRL，一种面向RLVR（可验证奖励强化学习）训练的集群级运行时系统。作者指出RLVR训练的低效是结构性的：长尾rollout、工具调用阻塞和rollout与训练之间的不对称资源需求在单个任务内无法消除。但不同任务之间的空闲时段呈**反相关性**，因此可在集群层面利用。PlexRL通过集中管理模型部署、状态转换和函数级调度，在严格的亲和性约束下跨任务时间切片执行LLM，填充空闲时段而无需昂贵的模型迁移。实验表明，PlexRL有效提升集群容量，**用户GPU小时成本最高降低37.58%**，同时保持算法灵活性。
  > 💡 RLVR是当前LLM后训练的核心范式，其训练效率直接制约推理能力的迭代速度。PlexRL从集群调度层面解决GPU闲置问题，对大规模RLVR训练有实际成本优化价值。
   - 来源: [arXiv](https://arxiv.org/abs/2605.20863)


---
*更新时间: 2026-05-22*
