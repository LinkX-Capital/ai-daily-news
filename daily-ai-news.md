## 04月20日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

## 要点汇总

- 产业动态：Meta从Thinking Machines Lab挖走第5位创始成员; 高德发布全栈具身技术体系及ABot-Claw机器人
- 算力追踪：Nikkei称全球DRAM供应缺口将持续到2030年; Epoch AI调查Stargate全部7个站点正在建设; Google与Marvell洽谈合作开发AI推理芯片; 三星停产LPDDR4/LPDDR4X
- 初创&融资：OpenAI收购AI教育科技公司Chalkie，全球50万+教师用户; 半导体工艺公司AlixLabs获1410万欧元A轮开发原子层蚀刻工艺; Anthropic收到8000亿美元估值投资意向
- 研究关注：Berkeley RDI审计8大AI Agent基准测试，全部可被零能力Agent刷满分
- X讨论：SemiAnalysis对话ChipBook团队探讨芯片制造; Luma提出AI系统联邦模型与mega模型两种路线

---

## 📖 详细参考

### 产业动态
**Meta从Mira Murati的Thinking Machines Lab挖走第5位创始成员**
- Thinking Machines Lab由前OpenAI CTO Mira Murati创立，估值120亿美元。最新加入Meta的是Joshua Gross，他从零构建并交付了该公司的旗舰产品Tinker，现加入Meta Superintelligence Labs领导工程团队。**Meta已挖走5位创始成员**（包括联合创始人Andrew Tulloch），OpenAI也挖走了其前CTO Barret Zoph。Thinking Machines Lab则反向引入了PyTorch创建者Soumith Chintala担任CTO，团队已扩张至约130人。
  > 💡 Thinking Machines Lab同时面临Meta和OpenAI的双向挖角，但它也在从大厂吸引顶尖人才，AI人才流动已呈双向竞争态势
   - 来源: [新智元](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA==&mid=2652693322&idx=2&sn=33e2bc903b986938996d63f66bf56e2a) | [Business Insider](https://www.businessinsider.com/thinking-machines-lab-loses-another-founding-member-to-meta-2026-4)

**高德发布全栈具身技术体系及ABot-Claw机器人，参加北京亦庄人形机器人半马**
- 高德发布首个面向AGI的全栈具身技术体系，涵盖感知、规划、控制全链路，**在15项基准测试中达到SOTA性能**。同步发布ABot-Claw具身智能机器人，专注于打造世界记忆系统，解决机器人对环境的感知和记忆问题。在北京亦庄举行的2026人形机器人半程马拉松中，300余台机器人参赛，高德全自主具身机器人在城市主干道和复杂路段完成长距离导航和导盲任务。
  > 💡 高德同时推进技术体系、产品落地和真实场景验证，具身智能从实验室走向城市道路的节奏在加快
   - 来源: [量子位](https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247884586&idx=1&sn=9bf96cc00105a72306c125f3513f7d07) | [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651028576&idx=1&sn=322ec19f119345c917c1a803e2c26905&chksm=8571c5a85201ce119154cd58233d0d08e2ed0d1fc3e5456790bb2f6e8b1f5aa3403dc30e0e52&scene=0&xtrack=1#rd) | [新智元](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA==&mid=2652693322&idx=1&sn=a049b38295b61ad6ad8b23151cb82fcd)

### 算力追踪
**Nikkei：全球DRAM供应缺口将持续到2030年**
- 根据Nikkei Asia的最新报告，尽管各大供应商试图提升DRAM产量，预计到2027年底全球DRAM供应只能满足约60%的需求。内存短缺问题可能持续到2030年。
  > 💡 DRAM供应缺口持续至2030年，AI算力供应链的瓶颈不止在GPU，存储也是关键约束
   - 来源: [机器之心](http://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2651028576&idx=2&sn=b359daa45a3e8e72dc99d2ac26d966b6&chksm=85352c6fff3b477cfcf077a47974f42c4f0d83d2c140f6799d53e5cc322a7026b5b51d14f735&scene=0&xtrack=1#rd)

**Epoch AI调查OpenAI Stargate：全部7个数据中心站点正在建设，预计2029年达9+ GW**
- Epoch AI实地调查了OpenAI $5000亿Stargate数据中心的全部7个美国站点，**均发现可见的建设进展**。项目预计到2029年达到9+ GW电力容量，相当于纽约市峰值电力需求。
  > 💡 Stargate是目前最大的AI基础设施项目，9 GW的电力规模意味着算力供给正在加速集中
   - 来源: [@EpochAIResearch](https://x.com/EpochAIResearch/status/2045258390147088764)

**Google与Marvell洽谈合作开发AI推理芯片**
- The Information报道，Google正与芯片公司Marvell洽谈合作开发新的AI推理专用芯片。这是Google在自研TPU之外的又一次芯片合作尝试，**专门面向推理场景**。
  > 💡 大厂纷纷布局推理芯片，Google+Marvell组合是继Amazon Trainium、Microsoft Maia之后的又一玩家
   - 来源: [The Information](https://www.theinformation.com/articles/google-talks-marvell-build-new-ai-chips-inference)

**三星正式停产LPDDR4和LPDDR4X，十年主流内存产品进入EOL**
- 据The Elec报道，三星电子已正式停止接收LPDDR4和LPDDR4X的新增订单，**标志着这两款量产逾十年的主流内存产品进入生命周期终结阶段**。LPDDR4/4X自2017年大规模量产后成为数十亿移动设备的标准配置，停产反映出行业向LPDDR5/5X加速迁移。
  > 💡 三星停产LPDDR4/4X将加速行业向新一代内存迁移，DRAM产能结构变化可能加剧AI用HBM的供应紧张
   - 来源: [36氪](https://36kr.com/newsflashes/3773244803236354)

### 初创&融资

**OpenAI收购AI教育科技公司Chalkie，全球50万+教师和1000万+学生用户**
- OpenAI收购AI教育科技公司Chalkie。Chalkie的核心产品为AI驱动的教师备课工具，能自动生成教案和备课内容，**全球已有50万+教师和1000万+学生使用**。公司2026年3月刚从TriplePoint Ventures完成$4M融资，CEO Phil Daneshyar为前YC创始人。这是OpenAI在教育垂直场景的首次收购布局。
  > 💡 OpenAI通过收购进入AI教育场景，Chalkie的用户规模验证了AI备课工具的产品市场契合度
   - 来源: [IT桔子](https://www.itjuzi.com/merger/13981) | [EdTech Innovation Hub](https://www.edtechinnovationhub.com/news/milestone-for-ai-powered-edtech-startup-chalkie-as-it-is-snapped-up-by-openai)

**半导体工艺公司AlixLabs获1410万欧元A轮开发原子层蚀刻工艺**
- AlixLabs是一家原子层蚀刻工艺服务商，专注于半导体纳米结构制造。其技术将40纳米宽的特征分割成两个10纳米的中间距特征，可扩展到10纳米以下。该工艺减少了光刻设备的使用。
  > 💡 AlixLabs的原子层蚀刻技术可减少光刻设备依赖，为10纳米以下制程提供新路径
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14695945)

**Anthropic收到投资者以8000亿美元估值投资的意向**
- The Information报道，Anthropic已收到多家投资者以**8000亿美元估值**注资的意向，但公司目前没有融资计划。报道来自Anthropic CFO Krishna Rao的人物专访，**融资决定预计要等到5月董事会之后**。
  > 💡 8000亿美元估值反映出市场对Anthropic的高度认可，与OpenAI的估值竞争正在白热化
   - 来源: [The Information](https://www.theinformation.com/briefings/anthropic-received-investor-interest-800-billion-valuation)

### 研究关注
**Berkeley RDI系统性审计8大AI Agent基准测试：全部可被零能力Agent刷到满分**
- UC Berkeley RDI团队（Dawn Song等）构建自动化扫描Agent，系统审计了SWE-bench、WebArena、OSWorld、GAIA、Terminal-Bench等8个主流AI Agent基准测试，**发现全部可被零能力Agent刷到近满分**。SWE-bench只需10行conftest.py即可100%通过；WebArena通过`file://` URL直接读取标准答案；FieldWorkArena的validate函数完全不检查答案正确性。团队总结了7大漏洞模式（评估与Agent未隔离、答案泄露、eval()注入、LLM Judge未过滤输入等），并提出Agent-Eval Checklist和开源工具BenchJack用于基准测试漏洞扫描。
  > 💡 主流AI基准测试的系统脆弱性比预想严重，benchmark分数正在驱动模型选择和投资决策，但评估方法论本身需要对抗性测试
   - 来源: [Berkeley RDI Blog](https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/)

### X讨论
**SemiAnalysis对话ChipBook团队：探讨芯片制造难题的解决方案**
- SemiAnalysis与ChipBook团队进行了完整对谈，探讨他们如何解决芯片制造中的关键问题。视频内容涉及半导体制造工艺的技术细节和解决方案。该播客持续约1小时，展示了ChipBook在芯片领域的专业见解。
  > 💡 ChipBook聚焦芯片制造数据与工艺优化，半导体制造的数据化工具是产业链的重要环节
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2045970772070445521#m)

**Luma提出AI系统构建两种路线：联邦模型与 mega 模型**
- Luma AI提出了构建AI系统的两种思路：一是联邦模型加法官编排器（judge orchestrating），二是 mega 模型通过深度连接组织（deep connective tissue）实现推理。两种路线代表了当前AI架构的不同发展方向。
  > 💡 Luma提出AI系统的两条架构路线，代表了当前行业在模型设计上的根本分歧
   - 来源: [@lumalabsai](https://x.com/LumaLabsAI/status/2045925400371773870#m)


---
*更新时间: 2026-04-20 06:06*