## 08月02日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 15 条

---

## 要点汇总

- 模型前沿：字节跳动Seed团队发布Seedance 2.5
- 产业动态：Perplexity将Spaces升级为Projects
- 研究关注：Explorative Modeling; 腾讯Hyra研究代理辅助解决50年数学难题; ALIGN; CG-World
- X讨论：追求预训练数据质量的尽头是自建私有搜索引擎

---

## 📖 详细参考

### 模型前沿
**字节跳动Seed团队发布Seedance 2.5：单次生成30秒视频，支持多模态参考与精准编辑**
- Seedance 2.5延续2.0的多模态音视频联合生成架构，重点突破长叙事、多模态参考和编辑能力。**单次生成时长从15秒提升至30秒**，支持多轮延长以生成数分钟连贯内容，模型优化了镜头衔接和场景过渡。多模态参考方面支持单次输入**最多30张图片、10段视频、10段音频**作为参考素材，综合理解构图、场景、风格、人物等元素，并提升**白模参考**、运动参考、创意参考能力。编辑方面支持时间戳精准控制、绿幕编辑、视角编辑、参考编辑等。模型系统优化了视频生成中常见的"油腻感"问题，减少字幕与背景音乐不受控的情况。产业应用方面，模型已进入**教育领域**（豆包爱学App「豆包课堂」将课文历史背景转化为沉浸式视频、辅助教师制作教学视频）、**工业制造**（生成合成数据训练机器人感知与操作能力、工业仿真与设备演示）及**自动驾驶**（模拟极端天气与复杂路况等低频场景）等场景。已在即梦AI、豆包专业版上线，API将近期上线火山方舟。
  > 💡 30秒单次生成+多轮延长是当前消费级视频模型的领先规格，多模态参考让视频生成从"片段输出"走向完整创作流程；但复杂运动物理合理性与极多主体交互场景的稳定性仍有提升空间，说明模型对物理世界规律的理解仍是下一阶段瓶颈。
   - 来源: [Seed](https://seed.bytedance.com/zh/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5)

### 产业动态
**Perplexity将Spaces升级为Projects：共享文件系统+持久记忆**
- Perplexity推出Projects，作为Spaces的演进版本。每个Project拥有**持久化层级文件系统**，Computer（Perplexity的代理）可跨会话读写、编辑、保存文件，工作成果逐任务累积。Projects接入**Brain自我改进记忆系统**，在任务间自动回顾文件和会话以更新上下文，使每个新任务从已有理解出发。支持团队协作，所有人基于同一文件源工作；可连接Google Drive、Notion、Linear、Snowflake等**400+工具**。支持Slack和Microsoft Teams集成，在频道中输入/project即可绑定。原有Spaces自动迁移，已向所有用户开放。
  > 💡 Perplexity正从搜索引擎向AI工作平台转型，持久文件系统+Brain记忆直接对标Claude Code的项目管理能力；AI代理的"工作连续性"正成为产品差异化核心。
   - 来源: [@perplexity_ai](https://x.com/perplexity_ai/status/2082866707438415932) | [Perplexity Blog](https://www.perplexity.ai/hub/blog/spaces-are-now-projects)

### 研究关注
**Explorative Modeling：提出预训练"第三轴"探索，6.2×数据效率与1.43 FID**
- Alexi Gladstone、Heng Ji、Yilun Du提出Explorative Modeling (XM)，将"探索"作为继参数和数据之后的第三个预训练轴。核心思想是因式分解训练而非生成：在训练时探索K个候选输出并选择最优进行训练，使预测commit到真实mode而非模糊均值。加入探索后实现**6.2×数据效率、4.1× FLOP效率、47%参数效率提升**，ImageNet无引导FID达到**1.43**，较标准SiT recipe收敛快约**300×**。最关键的是探索的收益随规模增长而非饱和--数据规模增大时收益从7%升至36%，参数增大时从13%升至23%。在机器人操作任务中，Explorative Policy以**单次前向传播**匹配Diffusion Policy（100步）的性能；在Maze2D规划任务中以平均**80×更少步数**超越Diffuser。
  > 💡 如果探索确实是一个新的缩放轴，暗示当前模型在生成表达能力上存在系统性瓶颈，仅靠堆数据和参数无法解决；端到端生成（训练和推理方式相同）可能大幅降低推理成本，对扩散模型"多步去噪"范式构成根本性挑战。
   - 来源: [项目主页](https://explorative-modeling.github.io) | [@AlexiGlad](https://x.com/AlexiGlad/status/2083230922196107288) | [arXiv](https://arxiv.org/abs/2607.27372)

**腾讯Hyra研究代理辅助解决50年数学难题：和集与差集最优指数确认为2**
- 腾讯混元团队宣布，其研究代理Hyra和Hy3模型帮助解决了一个50年悬而未决的组合数学问题。对于有限整数集A，|A+A|相对|A-A|的增长最优指数--1969年定理给出上界2，但此前最佳构造仅略超1.1。论文构造了显式集合族A_K使得log σ(A_K)/log δ(A_K) -> 2，证明指数1/2同样是最优的，并附带形式化证明。论文作者为Haowei Lin、Shanda Li，明确标注构造与证明在Hyra（基于开源Hy3模型的AI研究代理）辅助下完成。
  > 💡 AI研究代理在纯数学前沿问题上取得实质性贡献，标志着AI辅助研究从"文献整理"进入"构造性证明"阶段；腾讯Hyra的定位类似于DeepMind的FunSearch/AlphaProof路线，国内大厂开始在"AI做数学研究"方向投入。
   - 来源: [arXiv](https://arxiv.org/abs/2607.27199) | [@TencentHunyuan](https://x.com/TencentHunyuan/status/2082655737541726636) | [Hyra 博客](https://hy.tencent.ai/research/hyra)

**ALIGN：自动生成对齐接口修复Agent-环境失配，ALFWorld成功率提升45.67%**
- OpenBMB团队提出ALIGN框架，解决LLM Agent与环境之间的接口失配问题。论文指出Agent失败往往不是推理错误，而是对动作效果的预期与环境实际状态转移不一致。典型案例：在ALFWorld中Agent试图examine shelf 1但环境要求先go to，返回"Nothing happens"后Agent误判货架为空。ALIGN通过INFERRULES模块提取环境静态规则（前置条件、动作排序）、WRAPSTEP模块增强逐步观察（补充成功/失败条件），作为轻量级Python包装器运行，不修改Agent逻辑或环境代码。在ALFWorld上仅优化接口反馈就将Qwen2.5-7B从**13.4%提升至31.3%**，四个基准测试中最高提升**45.67%**，连续无效动作减少65%。接口可跨Agent架构（ReAct、Self-Consistency、Planning）和LLM骨干即插即用迁移，无需重新生成。作者为Kaiming Liu等。
  > 💡 Agent-环境接口失配被识别为系统性瓶颈，意味着当前大量Agent性能损失可能被误归因为模型推理能力不足；轻量级接口优化不改模型和环境即可获得大幅提升，对工业界Agent部署有直接实用价值。
   - 来源: [arXiv](https://arxiv.org/abs/2505.21055) | [@OpenBMB](https://x.com/OpenBMB/status/2083175856563003724)

**CG-World：85万段CG对齐数据集，带反事实分支面向世界模型**
- CG-World提出基于工业计算机图形学生成管线的大规模世界状态数据集，v1包含约**85万段**1-5秒的时间对齐片段。每段片段对齐RGB、物体、几何、骨骼与控制器状态、运动曲线、相机与光照参数、物理缓存、接触事件和多通道渲染。数据集定义分支谱系，包含**5000条动作干预和5000条机制干预**的反事实分支--改变动作、质量、摩擦力或粘度，保持其余固定，观察替代结果。论文在几何条件视频生成、动作预测和闭环VLA策略迁移上验证了数据集的有效性。作者为Yiming Cai、Fangjie Yu等。
  > 💡 CG-World将世界模型训练焦点从"预测下一帧"转向"识别底层状态及其在干预下的变化"，反事实分支结构为因果推理和干预学习提供了稀缺的结构化监督信号；但CG记录非物理真值且完整数据集尚未公开，其转化为实际世界模型增益的程度仍待验证。
   - 来源: [arXiv](https://arxiv.org/abs/2607.26452)

### X讨论
**追求预训练数据质量的尽头是自建私有搜索引擎，Anthropic新增TurboPuffer暗示自建索引**
- swyx指出：当AI实验室对预训练数据质量要求足够高（CommonCrawl不再够用），就需要自建全网页爬虫和索引系统以保持时效性，最终等于在预训练的副产品中建了一个"低频私有版Google"，还可复用于Agent推理侧；自建1P搜索既是竞争优势也是对抗AEO Batesian Mimicry的对抗性目标。Simon Willison补充披露：OpenAI曾与Bing合作但也在运行自研爬虫与索引基础设施；Anthropic除Brave外于**2026年5月**在子处理者列表中新增**TurboPuffer**，后者为除Claude for Government外所有Anthropic产品提供网页搜索，暗示Anthropic已开始自建搜索索引。Willison强调，作为付费用户，了解搜索机制对评估结果可信度至关重要。
  > 💡 AI实验室自建搜索索引是垂直整合的必然趋势，搜索能力正从外部采购转向核心基础设施；搜索索引透明度的缺失对用户信任构成挑战，尤其在AI生成内容引用可信度方面。
   - 来源: [@swyx](https://x.com/swyx/status/2083016652032188669) | [@simonw](https://x.com/simonw/status/2082835952939200939)

---
*更新时间: 2026-08-02*
