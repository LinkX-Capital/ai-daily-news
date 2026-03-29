# 📡 AI前沿动态 | 2026.03.28-29

**自动汇总** | 48h | 共 12 条新闻 + 重要X讨论

---

## 📌 要点速览

- **模型前沿**：硅心科技aiX-apply-4B单卡推理速度提升15倍；Meta SAM 3.1引入多目标追踪；GPT-5.4在USAMO数学基准达95%
- **产业动态**：智谱GLM-5.1登陆Coding Plan；钉钉CLI开源10项企业能力；谷歌TurboQuant论文被指造假；华为盘古负责人王云鹤投身Agent创业
- **算力追踪**：中兴发布AI超节点不依赖高端GPU；英伟达发布自进化AI Agent自主优化GPU算子；Sam Altman宣布Stargate工地开建
- **初创&融资**：Physical Intelligence洽谈10亿美元融资估值110亿美元；具身智能公司格松科技获超亿元A轮
- **研究关注**：哈工深补全Query Norm重构线性注意力；美团LongCat-Next统一文字图像语音为同源Token；南京大学提出仿真到现实迁移框架；LLM驱动工业机器人代码生成
- **关键X讨论**：vLLM 0.18.0提升Kimi推理18倍；LeCun转发自监督学习新方法；Sergey Levine谈pi模型形态；Percy Liang担忧训练稳定性

---

## 模型前沿

### aiX-apply-4B小模型实现单卡15倍推理加速，93.8%准确率超越DeepSeek-V3.2

aiX-apply-4B是北大系创企硅心科技（aiXcoder）推出的企业级小模型，在单张显卡上实现**15倍推理速度提升**。该模型准确率达到**93.8%**，超越DeepSeek-V3.2水平。企业AI落地通常受限于算力成本，高性价比小模型的突破使得更多场景能够本地部署，无需依赖云端API。这对于需要低延迟、高隐私的工业和商业场景意义重大。

> 💡 小模型加速推理正在成为企业AI落地的新瓶颈，谁能在边缘端跑出高性能，谁就掌握了下一波企业市场的入场券。

📌 来源：[量子位](https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247878293&idx=3&sn=d92f57deff1ab04556c05125580fe899)

**Meta 发布 SAM 3.1：引入 object multiplexing，单次前向传播可追踪16个目标**

Meta 发布 SAM 3.1，引入目标复用（object multiplexing）技术，使模型能在单次前向传播中追踪多达16个目标，显著提升视频处理效率，且无需牺牲精度。该更新可作为 SAM 3 的直接替代方案。**SAM系列持续迭代，多目标追踪能力已接近实用水平**。

📌 来源：[@AIatMeta](https://x.com/AIatMeta/status/2037582117375553924#m)


**GPT-5.4 在 USAMO 2026 达到95%，近乎SAT基准**

据转发，GPT-5.4 在 USAMO 2026 取得了惊人的95%得分，几乎达到基准饱和。去年模型在该测试中表现惨淡。**LLM数学能力持续飙升，USAMO 或已无法区分最强模型**。

📌 来源：[@hyhieu226](https://x.com/j_dekoninck/status/2037862663649460366#m)

## 产业动态

**GLM-5.1 登陆 GLM Coding Plan，所有用户可用**

GLM-5.1 现已向所有 GLM Coding Plan 用户开放。智谱同时发布了在 Coding Agents 中使用 GLM-5.1 的完整指南。有用户指出中国开源模型正在"碾压" Anthropic 和 OpenAI。**国产开源模型正在加速追赶闭源巨头，Coding Agent赛道已成中美AI竞争新战场**。

> 💡 智谱以Coding Plan切入差异化竞争，低价策略吸引开发者迁移，OpenAI和Anthropic面临压力。

📌 来源：[@Zai_org](https://x.com/Zai_org/status/2037490078126084514#m)

**钉钉CLI开源：首批开放10项核心产品能力，让AI Agent直接调用企业工作流**

钉钉CLI开源项目上架Github，以Apache-2.0协议开源，首批开放AI表格、日历、待办、机器人、通讯录等10项核心产品能力，原生支持Claude Code、Cursor等主流AI编程环境。**过去开发者若要调用企业软件能力，需要研读数百页API文档、编写鉴权代码，对接周期长达数周——这道高门槛严重制约了AI Agent在企业场景的落地。钉钉CLI让AI Agent能用自然语言指令直接调用企业工作流能力，大幅降低企业AI化门槛**。这是阿里巴巴争夺AI时代企业基础设施定义权的战略动作。

> 💡 阿里以开源CLI争夺企业AI基础设施定义权，当AI Agent成为企业生产力标配，平台入口价值将重塑。

📌 来源：[量子位](https://www.qbitai.com/2026/03/392828.html)

### 谷歌TurboQuant被指涉嫌学术造假，曾导致内存板块市值蒸发900亿美元

苏黎世联邦理工学院（ETH Zurich）博士后高健扬发布文章指控谷歌某AI研究存在学术不端行为。该论文曾因声称能大幅优化内存使用而引发市场震动，导致内存股单日蒸发约900亿美元市值。目前尚不清楚具体指控内容和谷歌回应，但此事已引发学术界和产业界广泛关注。

> 💡 AI研究的市场影响力已达能左右资本市场的程度，学术透明度与市场信心紧密挂钩。

📌 来源：[机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651024408&idx=1&sn=2e5b870868e54c10ba4fa75339f1d577&chksm=8552af8f87ed54665d88609ff10bac9b681edc3392fe814758929c2efa23ed0a060bc94b64f5&scene=0&xtrack=1#rd)

**华为盘古大模型负责人王云鹤离职，被曝投身Agent创业**

华为诺亚方舟实验室主任、盘古大模型负责人王云鹤宣布离职。王云鹤91年生，北大博士，2018年入职华为，2025年接任诺亚方舟实验室主任。他曾获华为"十大发明"奖，Google Scholar被引数达33109次，h-index为68。其代表作包括GhostNet（被引17000+）和Image Processing GNN。

> 💡 王云鹤的离职正值华为盘古大模型关键发展期，其下一步投身Agent创业，表明大厂核心人才正在加速流向AI应用赛道。目前水下融资已启动。

📌 来源：[量子位](https://www.qbitai.com/2026/03/392903.html)

## 算力追踪

### 中兴发布AI超节点基础设施，剑指推理成本大幅下降

中兴推出AI超节点产品，主打不依赖高端GPU的推理方案。该节点旨在降低企业部署AI的硬件门槛，通过架构优化提升单位算力效率。推理成本的下降将直接影响AI应用的商业可行性，特别是在需要大量token消耗的场景（如客服、代码生成）中。

> 💡 国产算力基础设施正在以差异化路线挑战英伟达生态，成本竞争将成为下一阶段主旋律。

📌 来源：[新智元](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA==&mid=2652687171&idx=2&sn=5f6d2ae6ae03f527e8b1aa80a860fcb1)

### 英伟达发布自进化AI Agent，7天内自主优化GPU算子性能超越FlashAttention-4

英伟达展示了一款自主进化的AI Agent，在连续7天的自主进化过程中，不断优化GPU算子性能，最终实现对FlashAttention-4的超越。该Agent被内部称为「GPU编码的AlphaGo时刻」，能够在无人干预的情况下持续改进底层计算性能。这标志着AI系统开始具备自动化优化硬件级代码的能力。

> 💡 AI Agent从软件层向硬件层渗透，底层代码优化进入「无人驾驶」阶段，Nvidia正在重新定义GPU编程边界。

📌 来源：[量子位](https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247878478&idx=3&sn=31ea9fbd473b6b758f68126c7a7351dc)

**Sam Altman：Michigan Stargate 网站开建，OpenAI+Oracle+Related Digital 合作落地**

Sam Altman 宣布，Michigan Stargate 站点首批钢梁已架设完成，合作方包括 Oracle 和 Related Digital。这是 OpenAI 基础设施扩张的重要里程碑。

> 💡 Stargate 项目进入实质性建设阶段。

📌 来源：[@sama](https://x.com/sama/status/2037610000122839116#m)

## 初创&融资

### Physical Intelligence洽谈10亿美元新融资，估值将翻倍至110亿美元

据TechCrunch报道，机器人AI公司Physical Intelligence正在洽谈新一轮约10亿美元融资。该公司成立于2024年，专注于为机器人开发通用基础模型。若交易完成，其估值将在短短四个月内从56亿美元翻倍至超过110亿美元，成为具身智能领域估值最高的公司之一。投资人正积极寻找能实现通用机器人智能的标的。

> 💡 具身智能成AI投资最热赛道，PI四个月内估值翻倍表明资本对通用机器人基础模型的持续押注。

📌 来源：[TechCrunch](https://techcrunch.com/2026/03/27/physical-intelligence-is-reportedly-in-talks-to-raise-1-billion-again/)

### 具身智能公司格松科技完成超亿元A轮融资，深创投连续两轮加注

格松科技宣布完成**超亿元A轮融资**，投资方包括深创投、祥峰投资、前海方舟等。深创投连续两轮加注，显示资本对具身智能赛道的持续看好。格松科技专注于具身智能研发与量产，3个月内连续获得两轮融资，印证了该领域的投资热度。

> 💡 具身智能成为资本新宠，深创投连续加注表明头部机构已将该领域列入核心布局。

📌 来源：[IT桔子](https://www.itjuzi.com/investevent/14694759)

## 研究关注

### 哈工深团队重构线性注意力：补全Query Norm后显存降低92.3%

哈工深圳团队在Transformer注意力机制上取得突破，通过补全Query Norm缺失，重构线性注意力架构。该改进使视觉任务精度提升的同时，**显存消耗降低92.3%**。线性注意力因可处理长序列且计算复杂度低而备受关注，此次改进解决了其训练不稳定的核心问题，为大视觉模型提供了新的高效架构选择。

> 💡 架构细节的完善往往是通往SOTA的最后一步，Query Norm的补全打开了线性注意力实用化的大门。

📌 来源：[PaperWeekly](https://mp.weixin.qq.com/s?__biz=MzIwMTc4ODE0Mw==&mid=2247718984&idx=2&sn=a2030ead6510be1126d4b569e5922068)

### 美团发布LongCat-Next：离散原生架构统一文字、图像、语音为同源Token

美团发布并开源原生多模态大模型 LongCat-Next，核心是 DiNA（Discrete Native Autoregressive）离散原生自回归架构。其核心创新在于将图像、语音、文字统一映射为离散 Token，通过统一的「下一个 Token 预测」范式建模所有模态，**打破了传统「语言基座+外挂视觉/语音模块」拼凑式架构的局限**。实验表明，LongCat-Next 在视觉理解上超越 Qwen3-VL，在图像生成上超越专用生成模型，工具调用大幅领先 Qwen3-Next。**这意味着多模态模型正在从「拼凑」走向「原生」，视觉和语音有望成为AI的「母语」而非副科**。

📌 来源：[IT之家](https://www.ithome.com/0/933/245.htm)

### 南京大学提出仿真到现实的迁移框架，机器人可在虚拟环境中完成全部训练

南京大学研究团队提出新框架，解决机器人从仿真环境到真实世界的迁移难题。该方法让机器人完全在虚拟环境中进行训练和调试，无需昂贵的真实机器人「肉身排雷」，大幅降低机器人开发成本。实验表明该方法在多个任务上实现了有效的zero-shot迁移。这对资源有限的学术团队尤为重要。

> 💡 仿真训练技术成熟度提升，机器人研发正从「实物试错」转向「低成本虚拟迭代」，加速学术与工业落地。

📌 来源：[新智元](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA==&mid=2652687225&idx=1&sn=cbb2aea5ee7a925c6ebbf2976c3c51d6)

### 卡内基梅隆大学提出安全AutoGEO方法，破解地理优化投毒攻击

卡内基梅隆大学研究团队提出「无毒合作式AutoGEO」，旨在解决地理优化任务中的数据投毒攻击问题。在315曝光相关产业链后，该研究提供了一种防御思路，允许系统在不信任环境中进行安全优化。该方法通过设计对抗性鲁棒的机制，降低投毒攻击对优化结果的影响。

> 💡 AI安全研究正在回应真实世界的攻击威胁，防御性研究需求随攻击曝光而激增。

📌 来源：[新智元](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA==&mid=2652687225&idx=3&sn=bcbedf7b2151686e391d88df299720a3)


### LLM驱动工业机器人控制代码生成，研究展示多智能体协同新范式

大语言模型正被用于工业机器人控制软件的自动化生成。传统上需要专业工程师手动编写的多机器人协同控制代码，现在可以通过自然语言指令自动生成，大幅降低开发门槛。这项研究发表于机器人领域顶会ICRA 2026，展示了将LLM与运筹优化结合应用于真实工业产线的可行路径。随着具身智能发展，代码生成能力正从数字世界延伸至物理世界的工业场景。

> 💡 LLM从聊天对话走向工业产线，代码生成能力正成为机器人落地的重要基础设施。

📌 来源：[机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651024408&idx=3&sn=9500bbb79d4a97484c102284e8ebd5e3&chksm=8572044724e73349142a91a79738d8584741ed8fa4682601e59b5749b1a2dc222e0d2009465e&scene=0&xtrack=1#rd)

## X讨论

**vLLM 0.18.0 发布：Kimi K2.5 1T MXFP4 在 AMD GPU 上实现18倍交互提升**

vLLM 发布 0.18.0 版本，在 AMD GPU 上对 Kimi K2.5 1T MXFP4 模型实现了高达18倍的交互性能提升。所有修复和 GEMM 调优已合并到主线。**vLLM 正在成为国产模型出海的重要推理底座**。

📌 来源：[@vllm_project](https://x.com/vllm_project/status/2037366264256168165#m)

**LeCun 转发 Bootleg：自监督表示学习新方法**

LeCun 转发了一篇新论文"Bootleg"，介绍了一种自监督表示学习的新方法。有评论指出，LeCun的团队训练出了第一个不会崩溃的世界模型。**自监督学习是LeCun的核心研究主线**，相关突破值得持续关注。

📌 来源：[@ylecun](https://x.com/scottclowe/status/2037535817871065365)

**Sergey Levine：pi 模型可能采用"带抓取器的无人机"形态**

Sergey Levine 表示，他原以为"带抓取器的无人机"不在 pi 模型的候选形态中，但现在看来这就是实际情况——这是一个"飞行抓取器"。**具身智能的物理形态仍在探索中，飞行平台可能是一类被低估的方案**。

📌 来源：[@svlevine](https://x.com/svlevine/status/2037954541283602519#m)

**Neel Nanda：推理模型的可解释性评估很困难**

Neel Nanda（Google DeepMind）指出，评估推理模型的可解释性进展出人意料地困难。需要设计那些无法通过思维链提示解决的任务来真正测试。**推理模型的可解释性研究正在成为一个独立方向**。

📌 来源：[@neelnanda5](https://x.com/NeelNanda5/status/2037617329450991817#m)

**Sam Altman：用户用 ChatGPT 为狗开发 mRNA 疫苗协议**

Sam Altman 分享了一个案例：一位用户 Paul 使用 ChatGPT 和其他 LLM 为其狗创建了 mRNA 疫苗协议，最终拯救了狗的生命。Altman 称这是他本周最酷的会议。**AI 在生物医药领域的个人化应用正在突破想象**。

📌 来源：[@sama](https://x.com/sama/status/2037396826060673188#m)

**Jeff Dean 发布与 Bill Dally 在 GTC 的对谈视频**

Jeff Dean 发布了与 NVIDIA 首席科学家 Bill Dally 在 GTC 上的对话视频，讨论了计算机体系结构的未来发展趋势。**两位顶级计算领域领袖的对话，指向GPU与AI系统的深度融合趋势**。

📌 来源：[@jeffdean](https://x.com/JeffDean/status/2037363016770191539#m)