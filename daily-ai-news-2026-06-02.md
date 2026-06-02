## 06月02日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 模型前沿：NVIDIA Cosmos 3发布：物理AI开放世界基础模型; Qwen3.7-Plus发布：多模态智能体基座，编程Agent benchmark领先; MiniMax发布M3模型：编程能力接近Opus 4.7; JetBrains发布Mellum2：120亿参数稀疏MoE编程模型
- 产业动态：OpenAI引入Salesforce全球合作伙伴VP; Unitree发布H2+人形机器人：75 DOF灵巧操作; Luma成立OPAL Lab：开放物理AI研究; Meta AI支持聊天机器人被绕过：黑客借此劫持多个Instagram账户; OpenRouter Auto Router新增成本-质量权衡调参功能
- 算力追踪：OpenAI密歇根破土动工1GW数据中心，系Stargate项目最大单点投资; NVIDIA AI Cloud生态扩张至六大洲，合作伙伴加速AI工厂部署
- 初创&融资：Anthropic向SEC秘密提交S-1草案：$965B估值IPO进程启动; The Mall发布AI驱动的通用购物feed应用
- 研究关注：LLM teams在间接推理和文化知识任务上仍存局限; LinTree：显式树结构搜索历史提升LLM推理效率; S2L-PO：小模型作为GRPO自然探索器; Materials Property Axiom：三阶段材料属性预测; DisjunctiveNet：可微分凸化优化层实现神经符号学习新突破
- X 讨论：xAI Grok Build上线Composer 2.5：长任务推理优化; Xiaomi MiMo-V2.5全链路推理优化：Hybrid SWA将KVCache降至1/7

---

## 📖 详细参考

### 模型前沿
**NVIDIA Cosmos 3发布：物理AI开放世界基础模型，GTC Taipei亮相**
- NVIDIA在GTC Taipei发布**Cosmos 3**世界基础模型，采用Mixture-of-Transformers架构，结合视觉推理和多模态生成（文本、视频、图像、环境音、动作）于单一模型。架构分为推理块（解析场景）和生成块（基于上下文生成物理仿真输出），支持原生动作生成（关节角度、夹爪位置、轨迹点等数值数据）。Agile Robots、NVIDIA GEAR团队等已在用Cosmos 3生成动作条件化机器人数据。Cosmos 3 Nano后训练策略在RoboLab和RoboArena上领先。
  > 💡 Cosmos 3将"看懂场景→预测→生成动作"闭环统一到单一模型，是物理AI从感知到控制端到端化的关键一步。
   - 来源: [NVIDIA Blog](https://blogs.nvidia.com/blog/cosmos-3-physical-ai-open-world-foundation-model/)

**Qwen3.7-Plus发布：多模态智能体基座，编程Agent benchmark领先**
- 通义千问发布Qwen3.7-Plus，定位为将视觉与语言统一的多模态智能体基座。纯文本方面，Coding Agent在**Terminal Bench 2.0达70.3**（超Opus-4.6 Max 65.4和DeepSeek-V4-Pro 67.9），**SWE-Pro 57.6**与头部模型持平。多模态方面，**ScreenSpot Pro 79.0**、**AndroidWorld 81.0**、**MathVision 90.3**显著超越Opus-4.6 Max和Gemini-3.1 Pro。模型在单一智能体循环中融合GUI操作、CLI工具调用和视觉推理，支持跨框架（Claude Code/OpenClaw/Qwen Code）部署。已通过阿里云百炼API提供服务。
  > 💡 Qwen3.7-Plus在多模态Agent能力上实现系统性突破，GUI操作和视觉编程benchmark全面领先同级别模型。
   - 来源: [Qwen Blog](https://qwen.ai/blog?id=qwen3.7-plus) | [@Alibaba_Qwen](https://x.com/Alibaba_Qwen/status/2061506644367069392#m)

**MiniMax发布M3模型：开源编程战场再加一员**
- 中国AI公司MiniMax发布M3大语言模型，编程能力接近**Anthropic Opus 4.7**水平。该模型特别适合编程和AI agent的复杂多步任务，支持文本、图像和视频多模态输入。MiniMax称M3可与头部闭源编程模型竞争，推动开源编程赛道进一步升温。
  > 💡 开源编程模型赛道继续升温，MiniMax M3加入后与CodeQwen、CodeLlama等形成正面竞争。
   - 来源: [The Information](https://www.theinformation.com/briefings/chinas-minimax-launches-new-model-open-source-ai-coding-battle-heats) | [@MiniMax_AI](https://x.com/MiniMax_AI/status/2061266317815296322)

**JetBrains发布Mellum2：120亿参数稀疏MoE编程模型**
- JetBrains发布Mellum2，120亿参数稀疏混合专家模型，专为代码场景优化。该模型采用稀疏激活机制降低推理成本，支持长上下文处理，已集成至JetBrains IDE生态。
  > 💡 JetBrains通过Mellum2将MoE架构引入IDE原生编程辅助，稀疏激活是成本敏感场景的关键。
   - 来源: [HuggingFace Blog](https://huggingface.co/blog/JetBrains/mellum2-launch)

### 产业动态
**OpenAI引入Salesforce全球合作伙伴VP，加速企业渠道布局**
- Salesforce前执行副总裁**Brian Landsman**在LinkedIn宣布加入OpenAI，担任全球合作伙伴VP，负责合作伙伴关系和应用商店业务。此前OpenAI已引入首席营收官**Denise Dresser**等多位Salesforce高管。Landsman此前在Salesforce任职14年，领导其全球合作伙伴和应用商店业务。此番引入销售渠道老将，OpenAI正从技术驱动转向企业生态和渠道驱动的商业化阶段。
  > 💡 OpenAI引入Salesforce背景高管表明AI商业化从技术竞争转向生态和渠道驱动。
   - 来源: [The Information](https://www.theinformation.com/briefings/openai-taps-salesforce-executive-lead-global-partnerships)

**Unitree发布H2+人形机器人：75 DOF灵巧操作，搭载NVIDIA Jetson Thor**
- Unitree发布H2+人形机器人，全身**75个自由度**（手部22个主动DOF），搭载**NVIDIA Jetson Thor**芯片（Blackwell GPU，FP4 2070 TFLOPS），配备128GB统一内存。机器人集成双SharpaWave触觉五指灵巧手，支持高级灵巧操作。额定臂部负载**7kg**，峰值**15kg**，配备15Ah电池（约3小时续航）。基于**NVIDIA Isaac GR00T**开放基础模型开发，支持人形推理、学习和多任务行为。
  > 💡 Unitree H2+的完整硬件规格和灵巧手配置表明国产人形机器人正从原型演示转向工业级操作能力。
   - 来源: [Unitree](https://www.unitree.com/H2plus/) | [@UnitreeRobotics](https://x.com/UnitreeRobotics/status/2061319330965475713#m)

**Luma成立OPAL Lab：开放物理AI研究，解决机器人泛化问题**
- Luma宣布成立Open Physical AI Lab（OPAL Lab），定位为开放科学实验室，解决物理AI的泛化危机。Luma指出当前机器人只能在特定环境重放特定任务，存在数据缺口和泛化瓶颈，而扩大遥操作采集在物理和经济上都不可行。Luma过去4年训练了3D、图像、视频和统一语言-视觉生成的frontier基础模型，积累了从原始多模态数据学习物理和交互的基础设施。OPAL Lab将研发World Models，与学术界和产业伙伴（芯片、硬件、物理agent系统）合作，所有成果开放可用。
  > 💡 Luma以开放科学路线切入物理AI，对抗少数公司垄断物理智能基础设施的趋势，是其从多模态生成向具身智能的战略延伸。
   - 来源: [@gravicle](https://x.com/gravicle/status/2061476460217737294#m)

**Meta AI支持聊天机器人被绕过：黑客借此劫持多个Instagram账户**
- 多名Instagram用户报告账户被劫持，黑客通过欺骗Meta AI支持聊天机器人获取账户访问权限。攻击者利用AI聊天机器人的指令遵循能力，绕过正常身份验证流程重置账户密码。TechCrunch详细披露了攻击手法。Meta尚未公开回应安全漏洞详情或修复时间表。该事件暴露了AI聊天机器人集成到用户支持场景时，缺乏权限边界控制的系统性安全风险。
  > 💡 AI聊天机器人集成到安全敏感产品暴露新型攻击面，AI安全不仅是模型层问题。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/01/hackers-hijacked-instagram-accounts-by-tricking-meta-ai-support-chatbot-into-granting-access/)

**OpenRouter Auto Router新增成本-质量权衡调参功能**
- OpenRouter为其Auto Router新增功能，允许用户自定义调整成本与质量的权重比例。新参数可精细控制路由策略，在成本敏感和质量优先场景间灵活切换。官方提供详细文档说明配置方法。
  > 💡 Auto Router的权衡参数将路由策略控制权交给用户，满足差异化需求是路由工具的核心竞争力。
   - 来源: [@openrouter](https://x.com/OpenRouter/status/2061476882470580329#m)

### 算力追踪
**OpenAI密歇根破土动工1GW数据中心，系Stargate项目最大单点投资**
- OpenAI在密歇根动工建设1GW数据中心，作为Stargate项目的重要组成部分。官方称该设施将支撑AI推理和训练需求，扩展AI访问范围并创造本地就业。这是Stargate框架下披露的规模最大的单点基础设施投资。
  > 💡 1GW级数据中心标志着AI基础设施进入GW时代，电力供应能力正成为AI扩张的核心约束。
   - 来源: [OpenAI News](https://openai.com/index/stargate-michigan-data-center)

**NVIDIA AI Cloud生态扩张至六大洲，合作伙伴加速AI工厂部署**
- NVIDIA宣布AI Cloud生态系统已扩展至**六大洲**，合作伙伴包括CoreWeave、Firmus、IREN、Nscale等，正在全球部署面向训练、推理和agentic AI的专用云基础设施。Jensen Huang表示"每家公司和每个国家都需要AI工厂基础设施将数据转化为智能"。区域扩展方面，东南亚、澳大利亚和美洲增长加速，新增非洲Cassava和南美Claro。合作伙伴采用NVIDIA DSX参考架构和液冷模块化设计，以降低单token成本并提升能效。
  > 💡 NVIDIA通过合作伙伴网络绕过自建产能瓶颈，生态扩展速度是决定其AI基础设施市场份额的关键。
   - 来源: [NVIDIA Blog](https://blogs.nvidia.com/blog/ai-cloud-ecosystem/)

### 初创&融资
**Anthropic已向SEC秘密提交S-1草案：$965B估值IPO进程启动**
- Anthropic确认已向美国证券交易委员会秘密提交S-1注册声明草案，等待SEC审查完成。此前Anthropic刚完成**$65B Series H融资**，由Altimeter Capital、Dragoneer、Greenoaks和Sequoia Capital领投，投后估值**$965B**。具体IPO时间表、发行股数和定价尚未披露。Anthropic为OpenAI主要竞争对手，此前已获Amazon数十亿美元投资。
  > 💡 Anthropic以近万亿美元估值启动IPO，代表AI公司进入资本市场新阶段，其与Amazon的合作关系后续动向值得关注。
   - 来源: [Anthropic News](https://www.anthropic.com/news/confidential-draft-s1-sec) | [@anthropicai](https://x.com/AnthropicAI/status/2061478052257841495#m)

**The Mall发布AI驱动的通用购物feed应用**
- 初创公司The Mall上线同名购物应用，通过爬取零售网站目录构建跨品牌商品数据库，当前覆盖**超10000个品牌**。后端使用LLM和自研模型对商品自动标注，支持按品类搜索和价格比对。用户关注品牌后可实时追踪促销、补货和新品推送，还可发现相似低价替代品。由Ellie Konsker（Tom Ford/Karla Otto背景）和Stanford CS的Sreya Halder于2025年10月创立，定位为"购物版的Spotify"。目前邀请制开放，预计夏末全面上线，商业模式为面向品牌的匿名数据分析工具和广告推荐位。
  > 💡 AI驱动的跨零售商商品聚合和自动标注，解决了碎片化电商时代的品牌发现和价格追踪痛点。
   - 来源: [TechCrunch](https://techcrunch.com/2026/06/01/a-new-app-the-mall-is-building-a-universal-feed-for-online-shopping/)

### 研究关注
**LLM teams在间接推理和文化知识任务上仍存局限**
- Anastasia Kotelnikova等人评估LLM teams在ChGK问答游戏（需要间接推理和文化知识）上的表现。使用572道2025年发布的题目，对比Voting、Silent Team和Talkative Team三种策略。六个开源模型实验显示团队策略准确率提升最高达**20个百分点**，最佳团队达**44.23%**，接近人类团队水平。分析发现模型间分歧强烈预示低准确率，但解释性沟通能缓解下降。研究结论指出LLM teams主要作为**答案选择和错误过滤机制**而非新解生成器。
  > 💡 LLM团队在复杂推理场景的局限性反映单模型能力的边界，多智能体协作尚需突破。
   - 来源: [arXiv cs.CL](https://arxiv.org/abs/2605.30459)

**LinTree：显式树结构搜索历史提升LLM推理效率**
- Liwei Kang、Yee Whye Teh和Wee Sun Lee发现LLM推理轨迹作为线性化搜索树，原始搜索历史不足以可靠超越仅观察局部状态的启发式搜索。原因是回溯时未显式标记回到哪个早期状态。通过添加父指针显式表示线性化树结构（LinTree），在Blocks World、Grid Navigation和Sokoban三个环境中同时提升了**任务性能和搜索效率**。结果表明搜索历史在树结构显式化时最有用。
  > 💡 LLM推理中的隐式回溯是效率瓶颈，显式结构化表示是提升推理搜索质量的有效方向。
   - 来源: [arXiv](https://arxiv.org/abs/2605.31492)

**S2L-PO：小模型作为GRPO自然探索器，提升数学推理准确率**
- Yiming Ren等人提出S2L-PO（Small-to-Large Policy Optimization），利用同族小模型作为天然探索器训练大模型。发现小模型在采样量增大时pass@k更高，其多样性具有时间相关性且保持逻辑一致性，优于token级随机噪声。通过渐进退火策略从小模型离线rollout过渡到大模型自身采样，避免小模型容量限制导致的中期性能下降。在AIME 24上使用1.7B模型引导8B模型，准确率提升**+8.8%**，同时减少rollout计算量。
  > 💡 同族小模型作为策略级探索源比token级噪声更有效，为高效RL训练提供了新范式。
   - 来源: [arXiv](https://arxiv.org/abs/2605.30789)

**Materials Property Axiom：三阶段训练框架提升材料属性预测**
- DeepPrinciple提出Materials Property Axiom（MPA），将LLM的三阶段训练范式（预训练→对齐→后训练）适配到材料属性预测。预训练基于约**6400万**优化材料几何的3D自监督，中间阶段按目标属性的物理相关性选择辅助数据，后训练针对具体实验端点微调。在**40个实验属性**上将MAE平均降低**10%**，单项OOD任务最高降低**51%**。最大提升出现在中间训练信号与目标属性物理机制匹配时。
  > 💡 材料属性预测的迁移效果取决于共享物理而非数据统计，按物理相关性选辅助数据是关键创新。
   - 来源: [DeepPrinciple Blog](https://blog.deepprinciple.com/introducing-materials-property-axiom/)

**DisjunctiveNet：可微分凸化优化层实现神经符号学习新突破**
- Shraman Pal和Can Li提出DisjunctiveNet，通过可微分凸化优化层在神经网络中强制执行硬性混合整数线性约束。方法将逻辑规则表示为析取约束，经层次化凸松弛获得凸包形式，生成可嵌入为可微分优化层的线性约束并实现精确规则满足。在真实数据集上实现**完美规则满足**和强预测性能，克服了现有方法仅能近似满足约束的局限。
  > 💡 神经符号学习正在从离散优化与梯度学习的对立走向融合，稀疏数据场景是其差异化应用方向。
   - 来源: [arXiv](https://arxiv.org/abs/2605.30456)

### X 讨论
**xAI Grok Build上线Composer 2.5：长任务推理优化**
- xAI在Grok Build平台发布Composer 2.5，定位为擅长长运行任务和遵循复杂指令的快速模型。该模型针对复杂推理场景优化，未披露具体技术架构或benchmark数据。
  > 💡 xAI通过Composer系列在Grok Build中建立长任务推理定位，与GPT-4.1-long等竞品形成差异化。
   - 来源: [@xai](https://x.com/xai/status/2061510464325206163#m)

**Xiaomi MiMo-V2.5全链路推理优化：Hybrid SWA将KVCache降至1/7**
- Xiaomi发布MiMo-V2.5系列全链路推理优化实践。该系列采用Hybrid Sliding Window Attention架构：70层中仅10层Full Attention、60层SWA，KVCache存储降至Full Attention的约**1/7**。团队基于SGLang构建了双池KVCache系统，SWA层实现严格O(W)存储约束，整体KVCache容量效率提升约7倍。此外覆盖分层缓存、SWA感知前缀缓存树、Prefill/Decode执行管线和多模态编码器吞吐优化。MiMo-V2.5-Pro在KVCache效率上仅次于DeepSeek-V4-Pro和DeepSeek-V4-Flash。
  > 💡 Hybrid SWA从架构理论到工程落地的完整实践，长上下文场景推理成本优势随序列长度递增。
   - 来源: [Xiaomi MIMO Blog](https://mimo.xiaomi.com/blog/mimo-v2-5-inference) | [@_LuoFuli](https://x.com/_LuoFuli/status/2060672928367497480)

---
*更新时间: 2026-06-02 06:45*