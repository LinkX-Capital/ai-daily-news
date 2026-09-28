## 09月28日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 全局精选 7 条

---

## 要点汇总

- 产业动态：MiniMax 发布 M3.1-Flash-Preview：登陆 MiniMax Code，面向日常开发; Microsoft 重做 Copilot：Home、Code 与 Autopilot 三套能力陆续上线; Sakana AI 聘请 Jürgen Schmidhuber 担任首席科学顾问，推进物理 AI 与世界模型; 智元与长隆部署超 300 台机器人，具身智能进入主题乐园常态化运营
- 算力追踪：中国或允许阿里、字节采购 NVIDIA RTX Pro 5500 芯片
- X讨论：SemiAnalysis AgentX 评测框架集成至 ModelScope; Epoch AI：华为 AI 芯片持续追赶，但到 2030 年仍可能落后 NVIDIA 约四年

---

## 📖 详细参考

### 产业动态
**MiniMax 发布 M3.1-Flash-Preview：登陆 MiniMax Code，面向日常开发**
- MiniMax 发布文本模型 **M3.1-Flash-Preview**，首先登陆 MiniMax Code，定位于从快速修复 bug 到开发完整功能的日常编程任务。官方同时宣布，9 月 28 日至 10 月 7 日（UTC+8）期间，MiniMax Code 每日签到可获得 **2 倍免费 credits**，新老用户均可参加，额度可用于 M3.1-Flash-Preview、H3 和 H3 Max；模型上线后 Token Plan 用户的额度将全部重置，后续还将继续安排重置。
  > 💡 MiniMax 将新模型、代码入口和限时额度激励绑定发布，实质上是在用产品分发和使用补贴推动开发者试用；M3.1-Flash-Preview 能否从预览版转化为稳定的日常开发工具，仍取决于真实任务中的可靠性与成本表现。
   - 来源: [@MiniMaxAgent](https://x.com/MiniMaxAgent/status/2104079819881517400) | [@minimax_ai](https://x.com/MiniMax_AI/status/2104256406786547800)

**Microsoft 重做 Copilot：Home、Code 与 Autopilot 三套能力陆续上线**
- Microsoft 对 Copilot 进行重新设计，新增 **Home、Code 和 Autopilot** 三项能力：Home 将 Chat、Cowork 以及 Copilot 内的 Word、Excel、PowerPoint 汇集到同一入口；Code 让用户利用与 GitHub Copilot 相同的底层技术构建并安全运行自己的解决方案；Autopilot 则是能够持续、主动运行的个人智能体。Home 与 Code 将在未来数周通过 Frontier 计划逐步推出，Autopilot 将于 9 月底进入 private preview。
  > 💡 Copilot 正从问答入口转向覆盖办公、编程和后台执行的统一工作界面；Autopilot 的持续运行能力如果能在权限与成本上得到控制，将直接改变企业对个人智能体的使用方式。
   - 来源: [Microsoft](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)

**Sakana AI 聘请 Jürgen Schmidhuber 担任首席科学顾问，推进物理 AI 与世界模型**
- Sakana AI 宣布 AI 先驱 **Jürgen Schmidhuber** 加入公司担任首席科学顾问，并参与其递归自我改进实验室（RSI Lab）的工作。Schmidhuber 将定期前往东京与团队交流，Sakana AI 希望借助其在世界模型、元学习和 Gödel Machine 等方向的研究积累，推进能够在行动前模拟物理后果的 Agent-Native World Models 与 Physical AI。
  > 💡 Sakana AI 引入世界模型领域的代表性研究者，说明其战略重点正从语言模型训练转向能模拟和执行现实行动的智能系统；日本的机器人与制造业基础也为这条路线提供了产业落点。
   - 来源: [Sakana AI](https://sakana.ai/schmidhuber/)

**智元与长隆部署超 300 台机器人，具身智能进入主题乐园常态化运营**
- 智元与横琴长隆飞船乐园联合部署 **超过 300 台**人形及其他具身智能机器人，覆盖文娱表演、科普研学、导览导购、零售、伴游、酒店和体育竞技等七类场景，并在园区 **100 余个交互点**常态化运行。智元当天向长隆交付第 **2 万台**具身智能机器人 A3 Ultra；以远征 A3 为例，针对园区场景优化后续航可达 **10 小时**，目前机器人与工作人员配比约为 **3:1**，未来目标是逐步提升至 10:1 乃至 20:1。
  > 💡 主题乐园提供了比工厂更开放、也更难标准化的真实环境，能同时检验机器人的多语言交互、安全避障和长期运营能力；当前仍需较高人工配比，说明具身智能已进入规模部署阶段，但距离低人力自主运营还有明显距离。
   - 来源: [智元官方](https://www.agibot.com.cn/article/315/detail/227.html) | [机器人前瞻](https://mp.weixin.qq.com/s/hizg-eyvPoAHAg0P8kcvRA)

### 算力追踪
**中国或允许阿里、字节采购 NVIDIA RTX Pro 5500 芯片**
- 据两位知情人士透露，中国政府已发出信号，可能允许部分国内公司采购 NVIDIA 本月新发布、面向高端专业计算的新芯片，以缓解本土 AI 企业运行聊天机器人与智能体所需的算力压力。工业和信息化部近期要求阿里巴巴、字节跳动等企业就采购 RTX Pro 5500 的数量与用途进行申报，并已告知部分中国企业政府有意批准相关采购。即使批准落地，具体的批准时间、可购数量与审批标准仍不明确。
  > 💡 工信部主动摸底芯片需求并暗示放行，表明中国 AI 算力缺口已大到无法仅靠国产替代满足，但也意味着审批口径仍由政府掌握，NVIDIA 在中国市场的实际放量节奏取决于监管尺度。
   - 来源: [The Information](https://www.theinformation.com/articles/china-weighs-allowing-purchases-new-nvidia-chips-bytedance-alibaba)

### X讨论
**SemiAnalysis AgentX 评测框架集成至 ModelScope**
- SemiAnalysis 宣布其 AgentX 评测框架已集成至 ModelScope，ModelScope 是中国广泛使用的评测框架。SemiAnalysis 表示 AgentX 已成为行业标准，并在全球被 OpenAI、Meta、Inferact、RadixArk、MiniMax、Alibaba Qwen、Moonshot、ZipHu GLM、Oracle 等机构采用。
  > 💡 AgentX 同时被中美头部模型厂商与云服务商接入，显示 SemiAnalysis 正在把单点拆解能力转化为跨厂商通用的评测基础设施。
   - 来源: [@semianalysis_](https://x.com/SemiAnalysis_/status/2104043521699119320)

**Epoch AI：华为 AI 芯片持续追赶，但到 2030 年仍可能落后 NVIDIA 约四年**
- Epoch AI 估算，2026 年华为旗舰 AI 芯片 Ascend 950 的单芯片计算吞吐约为 NVIDIA B300 的 **七分之一**，约为 2022 年 H100 的一半；华为预计生产约 **150 万颗**芯片，NVIDIA 约 **600 万颗**，综合产出算力约低 **25 倍**。报告认为，出口管制限制了华为提升单芯片性能和芯片产量两项关键规模化杠杆，到 2030 年华为在芯片性能和总产量上都可能仍落后 NVIDIA 约 **四年**。
  > 💡 中国 AI 芯片的追赶难点不仅是单颗芯片性能，更是先进制造、互联和规模化生产的乘数效应；即使架构和软件持续改进，产量与供应链约束仍会把总算力差距拉大。
   - 来源: [Epoch AI](https://epochai.substack.com/p/how-far-behind-nvidia-is-huawei)

---
*更新时间: 2026-09-28 06:45*