## 03月10日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

#要点汇总#

- 模型前沿：港科大提出音频生成统一模型AudioX
- 产业动态：智谱正式上线AutoClaw推动AI平权; 企业微信正式支持接入OpenClaw; IBM推出Granite 4.0 1B语音模型：面向边缘设备的紧凑多语; World Labs举办黑客松活动聚焦世界模型与空间智能; Anthropic与Mozilla合作测试Claude安全漏洞发现能力
- 算力追踪：ABB Robotics联合NVIDIA Omniverse实现工业级; OpenAI和Google员工支持Anthropic起诉国防部; AI驱动的行业变革：2026年收入增长与生产力提升; xAI承诺部署改善人类生活的AI并增加数据中心电力供应
- 初创&融资：OpenAI收购AI安全平台Promptfoo强化企业AI安全
- 研究关注：Yann LeCun团队揭示Transformer内部计算机制; OpenAI发布Chain-of-Thought可控性评估套件与研究论; 研究者发起红队对抗模型误用、控制与对齐研究项目; 研究证明数据回放既能减少遗忘又能帮助学习新数据
- X讨论：Karpathy提出自动化研究需要大规模异步协作; Karpathy发布自包含的autoresearch最小化代码库; Karpathy透露nanochat生产环境运行更大模型及8倍H100

---

## 📖 详细参考

### 模型前沿
**港科大提出音频生成统一模型AudioX**
- 港科大郭毅可院士团队提出AudioX音频生成统一模型，基于Diffusion Transformer架构，支持多模态输入生成音效和音乐，在多项基准上达到SOTA。
   - **港科大提出音频生成统一模型AudioX**
   - **支持文本、视频、图像等多模态输入生成音频**
   - **论文被ICLR 2026接收**
   - 来源: [新智元](https://mp.weixin.qq.com/s/xxx)

### 产业动态
**智谱正式上线AutoClaw推动AI平权**
- 智谱正式上线AutoClaw（中文名：澳龙），这是国内首个真·一键安装的本地版OpenClaw，预置50+热门Skills，支持一键接入飞书等即时通讯工具。
   - **智谱上线国内首个一键安装的本地版OpenClaw**
   - **预置50+热门Skills，支持一键接入飞书**
   - 来源: [量子位](https://mp.weixin.qq.com/s/ksLlPO58gnHgm2W-zVi4Rw)

**企业微信正式支持接入OpenClaw**
- 企业微信正式支持接入OpenClaw，企业成员可与AI助手直接对话，让AI主动处理业务、写入智能表格。管理员无需配置域名即可使用。
   - **企业微信正式支持接入OpenClaw**
   - **管理员无需配置域名，选择API模式即可接入**
   - 来源: [机器之心](https://mp.weixin.qq.com/s/nvtED-ELdGiWCpEDWpfZnQ)

**IBM推出Granite 4.0 1B语音模型：面向边缘设备的紧凑多语言方案**
- IBM在HuggingFace发布Granite 4.0 1B语音模型，这是一款紧凑、多语言、专为边缘设备设计的语音模型，支持多种语言的语音处理任务。
   - **IBM发布Granite 4.0 1B语音模型**
   - **模型专为边缘设备设计，支持多语言**
   - 来源: [HuggingFace Blog](https://huggingface.co/blog/ibm-granite/granite-4-speech)

**World Labs举办黑客松活动聚焦世界模型与空间智能**
- World Labs举办WL-HACK 01黑客松活动，汇聚了对世界模型和空间智能未来感兴趣的开发者，共同探索前沿AI技术。
   - **World Labs举办世界模型黑客松活动**
   - **活动聚焦空间智能和世界模型**
   - 来源: [@theworldlabs](https://x.com/theworldlabs/status/2029633878743470442#m)

**Anthropic与Mozilla合作测试Claude安全漏洞发现能力**
- Anthropic与Mozilla合作测试Claude在Firefox中发现安全漏洞的能力，Opus 4.6在两周内发现22个安全漏洞，展现了AI在网络安全领域的应用潜力。
   - **Anthropic与Mozilla合作测试Claude安全检测能力**
   - **Opus 4.6两周内发现22个漏洞**
   - 来源: [@AnthropicAI](https://x.com/AnthropicAI/status/2029978909207617634#m)

### 算力追踪
**ABB Robotics联合NVIDIA Omniverse实现工业级物理AI规模化部署**
- ABB Robotics宣布采用NVIDIA Omniverse平台来交付工业级物理AI解决方案，vLLM为Jetson上的完全本地化AI助手提供支持，OpenClaw教程展示了如何在NVIDIA Jetson上服务Nemotron 3 Nano等MoE模型。
   - **ABB Robotics采用NVIDIA Omniverse实现工业级物理AI规模化部署**
   - **vLLM为Jetson本地AI助手提供支持**
   - **展示了在边缘设备上部署MoE模型的技术方案**
   - 来源: [NVIDIA Blog](https://blogs.nvidia.com/blog/abb-robotics-omniverse/)

**OpenAI和Google员工支持Anthropic起诉国防部**
- 超过30名OpenAI和Google DeepMind员工签署声明，支持Anthropic起诉国防部的诉讼，回应了政府对AI军事应用的监管争议。
   - **超过30名OpenAI和Google DeepMind员工支持Anthropic**
   - **涉及对国防部AI军事应用政策的争议**
   - 来源: [TechCrunch](https://techcrunch.com/2026/03/09/openai-and-google-employees-rush-to-anthropics-defense-in-dod-lawsuit/)

**AI驱动的行业变革：2026年收入增长与生产力提升**
- NVIDIA博客探讨AI如何为各行业推动收入增长、降低成本并提升生产力，指出当前模型并非'够用'，智能竞赛远未结束，更高阶的智能仍是追求目标。
   - **AI正在为各行业带来实际收入增长和成本降低**
   - **更高阶智能仍是AI发展的未来方向**
   - 来源: [NVIDIA Blog](https://blogs.nvidia.com/blog/state-of-ai-report-2026/)

**xAI承诺部署改善人类生活的AI并增加数据中心电力供应**
- xAI承诺部署改善人类生活的AI技术，同时将在数据中心附近增加更多电力供应以支持AI系统的运行需求。
   - **xAI承诺部署改善生活的AI技术**
   - **计划增加数据中心附近电力供应**
   - 来源: [@xai](https://x.com/xai/status/2029294509230874896#m)

### 初创&融资
**OpenAI收购AI安全平台Promptfoo强化企业AI安全**
- OpenAI宣布收购Promptfoo，这是一家AI安全平台，帮助企业在开发过程中识别和修复AI系统漏洞。Promptfoo被超过25%的财富500强企业使用。
   - **OpenAI收购AI安全平台Promptfoo**
   - **Promptfoo被超过25%财富500强企业使用**
   - **将整合到OpenAI Frontier平台**
   - 来源: [OpenAI](https://openai.com/index/openai-to-acquire-promptfoo)

### 研究关注
**Yann LeCun团队揭示Transformer内部计算机制**
- 纽约大学Yann LeCun团队发表论文，研究Transformer中大值激活和Attention Sink现象，证明共并非必然，为量化部署提供优化思路。
   - **Yann LeCun团队揭示Transformer内部计算机制**
   - **大值激活与Attention Sink共并非必然**
   - **为量化部署和长上下文推理提供优化思路**
   - 来源: 机器之心

**OpenAI发布Chain-of-Thought可控性评估套件与研究论文**
- OpenAI发布了新的思维链（CoT）可控性评估套件和研究论文，发现GPT-5.4 Thinking在思维链可控性方面表现较弱，为模型推理能力评估提供新基准。
   - **OpenAI发布思维链可控性评估套件**
   - **GPT-5.4 Thinking在CoT可控性上表现不足**
   - 来源: @OpenAI

**研究者发起红队对抗模型误用、控制与对齐研究项目**
- NeelNanda发起一个关于红队测试模型误用、控制和对齐的研究机会，呼吁研究者参与AI安全领域的红队研究工作。
   - **NeelNanda发起红队研究项目**
   - **聚焦模型误用、控制和对齐问题**
   - 来源: @NeelNanda5

**研究证明数据回放既能减少遗忘又能帮助学习新数据**
- Percy Liang团队研究发现，数据回放技术不仅能减少知识遗忘，还能帮助模型在学习新数据时取得更好效果，相关论文已发布在arXiv。
   - **数据回放可减少知识遗忘**
   - **数据回放同时有助于新数据学习**
   - 来源: @percyliang


---
*更新时间: 2026-03-10 10:04*