## 04月12日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

#要点汇总#

- 产业动态：OpenAI星门计划三位核心负责人离职; Anthropic暂时封禁OpenClaw创始人Claude账号; Claude AI推出Word集成beta版本; 阿里Qwen Code推出定时任务功能; Google更新Gemini App集成NotebookLM功能
- 算力追踪：Anthropic租用CoreWeave算力支持Claude; 光通信龙头Lumentum称2028年产能即将售罄
- 研究关注：Meta押注Neural Computers：下一代计算机就是模型本身
- 初创&融资：生数科技融资2.93亿美元阿里云领投，布局通用世界模型
- X讨论：阿里Qwen发布子代理模型选择策略; SemiAnalysis展示用Claude同时运行8窗口控制agent swarm

---

## 📖 详细参考

### 产业动态
**OpenAI星门计划三位核心负责人离职**
- 曾参与启动OpenAI首个星门（Stargate）数据中心项目的三位高管集体离职，包括项目负责人Peter Herschler、算力战略负责人Shamez Hemani和算力部门负责人Anuj Saharan。星门是OpenAI首个超大规模数据中心项目，核心团队同时离开意味着算力基建战略可能面临方向性调整。
  > 💡 核心基建团队集体出走对星门项目推进构成重大风险，OpenAI算力战略不确定性增加
   - 来源: [36氪](https://36kr.com/newsflashes/3760818675565060)

**Anthropic暂时封禁OpenClaw创始人Claude账号**
- OpenClaw创始人Peter Steinberger（现就职OpenAI）的Claude账号被Anthropic以"可疑活动"为由暂时封禁，在X上引发热议后数小时内恢复。此前Anthropic刚宣布Claude订阅不再覆盖OpenClaw等第三方工具，改为API按量计费——本质上是对开源工具征收"claw tax"。Steinberger暗示Anthropic先在自家Cowork agent中复制热门功能，再封锁开源工具，并透露"一家欢迎我，一家发律师函"。
  > 💡 AI巨头通过定价策略和平台控制挤压第三方开源工具，平台锁定趋势值得关注
   - 来源: [TechCrunch](https://techcrunch.com/2026/04/10/anthropic-temporarily-banned-openclaws-creator-from-accessing-claude/)

**Claude AI推出Word集成beta版本**
- Claude for Word已开放beta测试，用户可直接从侧边栏起草、编辑和修订文档。Claude保留原有格式，编辑内容以追踪更改的形式呈现。
  > 💡 AI助手向传统办公软件渗透是商业化的重要路径
   - 来源: [@claudeai](https://x.com/claudeai/status/2042670341915295865#m)

**阿里Qwen Code推出定时任务功能**
- 用户可以告诉Qwen Code设置每30分钟检查测试是否通过的定时任务，系统会自动在项目环境中配置cron job。这扩展了AI编程助手的自动化能力。
  > 💡 AI编程助手向持续集成/自动化方向演进
   - 来源: [@alibaba_qwen](https://x.com/Alibaba_Qwen/status/2042551225795703290#m)

**Google更新Gemini App集成NotebookLM功能**
- Google本周更新了Gemini App，新增Notebooks功能，与NotebookLM集成使用户能够检索相关信息。这是Gemini生态系统的功能扩展。
  > 💡 产品功能整合提升用户粘性，Google在AI助手场景持续深耕
   - 来源: [@googleai](https://x.com/GoogleAI/status/2042671003570983299#m)

### 算力追踪
**Anthropic租用CoreWeave算力支持Claude**
- Anthropic向CoreWeave租用数据中心算力，涵盖美国数据中心多种英伟达芯片架构，用于构建和部署Claude模型。CoreWeave目前已将四大AI模型开发商纳入客户名单，意味着AI算力需求正从传统云厂商向专业GPU云服务商分流。
  > 💡 AI算力竞争从芯片延伸到云服务层，专业GPU云正成为大模型公司的新基建选择
   - 来源: [36氪](https://36kr.com/newsflashes/3760948716438017)

**光通信龙头Lumentum: 2028年产能即将售罄**
- Lumentum CEO表示，超大规模云厂商资本开支极其庞大且没有放缓迹象，按当前趋势再过两个季度2028年全年产能将彻底售罄。他判断本轮光通信景气周期至少持续5年。AI数据中心对高速光互联的需求已从短期爆发转为长期结构性增长。
  > 💡 光通信产能持续紧张印证AI基础设施投资进入长周期，不是短期泡沫
   - 来源: [36氪](https://36kr.com/newsflashes/3760888124146437)

### 研究关注
**Meta押注Neural Computers：下一代计算机就是模型本身**
- Meta提出Neural Computers概念，主张AI模型本身就是下一代计算平台，不再依赖传统软件栈。这一思路意味着未来应用开发可能从"编写代码"转向"训练和微调模型"，计算范式可能发生根本性转变。
  > 💡 模型即计算机的理念如果成真，将从底层重构软件产业，但距离实用仍有相当距离
   - 来源: [微信公众号](https://mp.weixin.qq.com/s?__biz=MzIwMTc4ODE0Mw==&mid=2247719459&idx=1&sn=e2c6f6e72e2e3f732d196c322d90c386)

### 初创&融资
**生数科技融资2.93亿美元，阿里云领投，布局通用世界模型**
- 由清华大学朱军教授创立的AI初创企业生数科技完成20亿元人民币融资，阿里云领投。资金将用于开发"通用世界模型"，通过处理感官信息模拟人类感知与交互。生数科技是中国首家发布视频生成模型（Vidu）的公司，近期还开源了面向机器人控制的Motus模型，正从视频生成向具身智能拓展。
  > 💡 生数科技从视频生成切入、逐步走向具身智能的技术路径清晰，阿里云领投显示国产大模型投资正从"卷模型"转向"卷落地"
   - 来源: [新浪财经](https://finance.sina.com.cn/videoroll/2026-04-10/doc-inhtyrwc5286201.shtml)

### X讨论
**阿里Qwen发布子代理模型选择策略**
- 阿里Qwen提出子代理模型选择方案：主代理使用Qwen3.6-Plus保证质量，但不同子任务可根据需求选择不同模型。这种分层模型架构可优化成本与性能的平衡。
  > 💡 模型路由和任务分配成为agent架构优化的关键方向
   - 来源: [@alibaba_qwen](https://x.com/Alibaba_Qwen/status/2042551230023762081#m)

**SemiAnalysis展示用Claude同时运行8窗口控制agent swarm**
- SemiAnalysis构建了一个系统，让intern同时运行8个Claude窗口来管理agent swarm。该系统实现了token mogging功能，展示了多代理协作的架构设计。这一实践体现了AI agent在工作流中的实际应用方式。
  > 💡 多窗口并发控制agent代表了一种新的AI协作架构，但实际效能和可靠性仍需验证
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2042719069397282992#m)

---
*更新时间: 2026-04-11 09:40*