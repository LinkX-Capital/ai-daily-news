## 03月27日 AI 前沿动态

> 自动汇总 | 时间窗口: 24h | 每类 Top 5

---

#要点汇总#

- 模型前沿：Cohere发布Transcribe语音识别模型，支持14种语言;Meta AI发布TRIBE v2三模态脑编码器，可预测大脑视觉响应；Google发布Gemini 3.1 Flash Live，支持实时对话式AI编程
- 产业动态： Google实时耳机翻译功能扩展至iOS和更多国家; Google Search Live全球上线，支持实时视觉搜索与对话
- 初创&融资：AI驱动的金融数据服务商讯兔科技完成近2亿元A轮融资; 它石智航发布OmniVTA视触觉世界模型，实现从被动感知到理解接触的跨越
- 研究关注：Sakana AI AI Scientist论文正式发表于Nature
- X讨论：研究者发现主流Scaling Laws拟合方法存在偏差，可能浪费数百万美元算力

---

## 📖 详细参考

### 模型前沿
**Cohere发布Transcribe语音识别模型，支持14种语言**
- Cohere发布Cohere Transcribe，这是一款2B参数的语音识别模型，采用Apache 2.0许可证，支持14种语言。**该模型获得vLLM的Day-0支持**，意味着开源社区可以立即在其推理框架中部署使用。2B参数规模使其适合在消费级GPU上运行推理。
  > 💡 语音识别开源模型再添重磅玩家，2B参数级别在端侧部署具有明显优势
   - 来源: [@vllm_project](https://x.com/vllm_project/status/2037197243111895066#m)

**Meta AI发布TRIBE v2三模态脑编码器，可预测大脑视觉响应**
- Meta AI发布TRIBE v2（Trimodal Brain Encoder），这是一个基础模型训练用于预测人脑对几乎任何视觉或听觉输入的响应。该模型整合了大脑的三模态信号，能够在不需要任何重新训练的情况下，可靠地预测从未见过的个体的脑响应。这解决了传统脑编码模型需要对每个新个体进行昂贵fMRI扫描和重新训练的痛点。**该模型达到了接近大脑fmri信号真实值解码的准确性**，为脑科学研究和脑机接口应用提供了强大的AI工具。
  > 💡 脑机接口的底层技术突破，AI解码大脑信号从实验走向可复用的基础模型阶段
   - 来源: [@aiatmeta](https://x.com/AIatMeta/status/2037153756346016207#m); (https://x.com/AIatMeta/status/2037153758455750717#m)

**Google发布Gemini 3.1 Flash Live，支持实时对话式AI编程**
- Google推出Gemini 3.1 Flash Live，允许用户通过实时语音对话与AI进行交互式编程（vibe coding）。用户可以在Google AI Studio中构建能够进行双向语音对话的实时对话代理，AI能够理解用户的语音指令并即时生成代码或应用。**这是Google首个支持实时语音交互的轻量级模型**，将大幅降低AI应用开发门槛。
  > 💡 实时语音交互是AI编程助手的下一代形态，轻量模型支持边缘部署将加速AI普惠
   - 来源: [@googleai](https://x.com/GoogleAI/status/2037190798609932671#m)

### 产业动态
**Google实时耳机翻译功能扩展至iOS和更多国家**
- Google实时耳机翻译功能现支持iOS设备和更多国家，该功能能够保持每位说话者的语调、重音和节奏，使对话更容易理解。该功能最初在Pixel Buds和Android设备上推出，现扩展至更广泛的生态。**这是Google将AI翻译能力推向终端设备的关键步骤**，进一步模糊了语言障碍。
  > 💡 AI翻译从云端走向端侧，实时耳机交互或将成为下一代人机交互形态
   - 来源: [TechCrunch](https://techcrunch.com/2026/03/26/google-translates-real-time-headphone-translations-feature-expands-to-ios-and-more-countries/)

**Google Search Live全球上线，支持实时视觉搜索与对话**
- Google推出Search Live，允许用户将手机摄像头对准物体获取实时AI帮助，并基于计算机视觉进行双向对话。用户可以实时询问关于物体的信息，AI能够理解上下文并给出相关答案。这是Google将多模态AI能力直接嵌入搜索体验的核心产品，标志搜索从关键词时代进入多模态交互时代。
💡 视觉搜索是搜索引擎的范式转变，多模态交互将成为移动搜索的新入口
- 来源: [TechCrunch](https://techcrunch.com/2026/03/26/google-is-launching-search-live-globally/)

### 初创&融资
**AI驱动的金融数据服务商讯兔科技完成近2亿元A轮融资**
- 讯兔科技宣布完成近2亿元A轮融资，由启明创投、红杉中国、高瓴创投共同领投。讯兔科技定位为AI驱动的金融数据与生产力服务商，**通过AI Agent提升全球机构投资者的工作效率，目标提高资本市场信息有效性**。
  > 💡 AI Agent在金融垂直领域的落地获资本认可，机构投资场景的商业化路径逐渐清晰
   - 来源: [IT桔子](https://www.itjuzi.com/investevent/14694686)

**它石智航发布OmniVTA视触觉世界模型，实现从被动感知到理解接触的跨越**
- 它石智航发布OmniVTA视触觉世界模型，突破传统视觉感知仅能「被动接收信息」的局限，实现对「接触交互」的理解。该模型融合视觉与触觉信息，使AI能够在物理交互中理解物体材质、硬度和接触力度等物理属性。**这是首个能够理解物理接触本质的视触觉统一模型**，为机器人灵巧操作和精细作业提供了新的技术基础。
  > 💡 视触觉融合是机器人智能的关键突破口，率先落地将带来机器人操作能力的质变
   - 来源: [新智元](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA==&mid=2652686704&idx=2&sn=a41c0e510bc8a4aa7395149a343d823d)

### 研究关注

**Sakana AI AI Scientist论文正式发表于Nature**
- Sakana AI宣布其AI Scientist论文正式发表于Nature，该项目由Sakana AI、UBC、Vector Institute和Oxford大学合作完成。AI Scientist-v2生成的论文首次通过严格的人类同行评审，在ICLR 2025 ICBINB workshop获得6.33平均分（超过人类接受阈值），比55%的人类论文得分更高。**更关键的是发现Scaling Law：基础模型越强，生成论文质量越高**，预示着AI做科学研究将快速超越人类。
  > 💡 AI科研从"不可能"到"超越人类"的速度超预期，Nature论文是其合法性的重要标志
   - 来源: [Sakana AI Blog](https://sakana.ai/ai-scientist-nature/); [Nature论文](https://www.nature.com/articles/s41586-026-10265-5)

### X讨论

**研究者发现主流Scaling Laws拟合方法存在偏差，可能浪费数百万美元算力**
- Eric Czech（percyliang的同事）深入分析了Meta、DeepSeek、Microsoft、Waymo等公司使用的parabolic IsoFLOP fits，发现存在系统偏差。Scaling laws本质是回归分析，但这种偏差拟合方法会在前沿规模上悄然浪费数百万美元算力。**这是AI训练成本优化的关键盲区**，大厂都在用但未必用对。
  > 💡 Scaling laws不仅是学术问题，更是工程经济问题，错误的方法会在规模化时放大损失
   - 来源: [@WilliamBarrHeld](https://x.com/WilliamBarrHeld/status/2037259464202740042#m)

---
*更新时间: 2026-03-27 07:55*