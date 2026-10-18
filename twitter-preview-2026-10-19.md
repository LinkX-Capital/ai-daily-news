# Twitter 动态预览
**日期**：2026-10-19 07:15
**总计**：29 条推文

---

## 📋 过滤说明

**抓取规则**：24小时内、去除重复账号、内容 >30字符
**存疑过滤**：无

---

## ⭐ 今日重点（LLM 提炼）

1. **Inferact & Google 提交首款 TPUv7 Kimi K3 2.8T 模型，性能对标 GB200 NVL72**
   @semianalysis_
2. **NVIDIA 通过 vLLM 上游优化实现 Kimi K3 2.8T 模型 423 tok/s/user，速度提升 1.68 倍**
   @semianalysis_
3. **vLLM v0.32.0 发布：814 个 commits、363 位贡献者，新增结构化决策端点与低精度 KV 缓存支持**
   @vllm_project
4. **Kimi K3 在 NVIDIA GB300 NVL72 上实现 842 tokens/s (batch 1) 解码速度**
   @vllm_project
5. **GLM 5.3 完全通过后训练构建，后训练 GPU 效率远超从头预训练**
   @semianalysis_
6. **Anthropic 成立公益基金，承诺让渡 5% 股份用于公共利益**
   @anthropicai
7. **Gemini 4 Argon 多智能体协作 27 小时击败 Minecraft 末影龙**
   @demishassabis
8. **Stanford 与 Together Compute 提出文本生成第三范式，超越自回归与扩散模型**
   @theturingpost

---

## 🏢 公司发布（13条）

### @anthropicai | Model

- We’re committing a portion of Anthropic’s shares to the Anthropic Public Benefit Fund, a new wholly owned entity dedicated entirely to the public benefit.  It will start off with 5% of our shares. For every 50% increase in the company’s value over a set baseline, we can contribute up to an extra 2%, subject to our board’s discretion.  In total, this means that roughly 20% of Anthropic’s shares are...
  [查看](https://x.com/AnthropicAI/status/2111881963657412903)

### @openrouter | Infra

- RT @0xRampey: Gave my coding agent every frontier model on @OpenRouter and let a router pick the best one for each step.  Guess which model…
  [查看](https://x.com/OpenRouter/status/2111912353843605846)
- RT @OpenRouter: Today, we are launching OpenRouter Armor in beta.  Tool calls allow agents to interact with the world, and regex-based filt…
  [查看](https://x.com/OpenRouter/status/2111596499687878912)

### @semianalysis_ | Infra

- BREAKING NEWS🚨: @Inferact & Google submit their FIRST preliminary TPUv7 Kimi K3 2.8T Model Submission, and it is already delivering strong perf per TCO against GB200 NVL72, B300, and MI355 in the ultra-high-interactivity regime due to their megakernel approach for external customers.  One of the most important aspects of an external compute platform is a strong community, and what makes this submi...
  [查看](https://x.com/SemiAnalysis_/status/2111938013852762351)
- BREAKING NEWS🚨: NVIDIA has just achieved 423 tok/s/user 🚀 on the 2.8T Parameter Kimi K3 model via a new upstream vLLM optimization. 1.68x Faster on the Same Hardware!  This was done by NVIDIA CentML's Benjamin, who wrote NVIDIA's new decode-specialized kernels in Cute DSL via aggressive Megakernel fusion. This is a 12,000 LoC Megakernel and is the future of advanced AI-assisted kernel generation. ...
  [查看](https://x.com/SemiAnalysis_/status/2111627094878790023)
- GLM 5.3’s biggest leap came from post-training alone.  “GLM 5.3 was built entirely by post-training the previous model. For me, that was a wake-up call.”  “Post-training is far more GPU-efficient than pre-training from scratch. Plenty of companies can’t afford to train a model from scratch, but they have proprietary data. They can post-train themselves and beat some of the closed models.”  “There’...
  [查看](https://x.com/SemiAnalysis_/status/2111596468528087078)

### @theturingpost | Research

- RT @TheTuringPost: Text generation now has a third option. Beyond autoregressive and diffusion models.  @Stanford and @togethercompute prop…
  [查看](https://x.com/TheTuringPost/status/2111925638634635461)
- RT @TheTuringPost: It’s a hot week for looped Transformers. For example, @Princeton and the University of Pennsylvania proposed an elegant…
  [查看](https://x.com/TheTuringPost/status/2111857979960312189)
- RT @TheTuringPost: What is AI agent memory?  Memory lets an agent use information from earlier work in a later decision - a preference, a p…
  [查看](https://x.com/TheTuringPost/status/2111774303243169825)
- RT @TheTuringPost: A great textbook to learn or refresh the math behind ML concepts - "Introduction to Machine Learning" by Laurent Younes…
  [查看](https://x.com/TheTuringPost/status/2111752783510774236)
- What is AI agent memory?  Memory lets an agent use information from earlier work in a later decision - a preference, a project fact, a working procedure, etc.  But "memory" also hides the design decisions: what survives a session, when it resurfaces, and how it shapes the next decision.  Lewis Liu, who works on enterprise AI at @Microsoft, separates 3 ambitions - each asks the system to carry some...
  [查看](https://x.com/TheTuringPost/status/2111637119064322518)

### @vllm_project | Infra

- 🚀 vLLM v0.32.0 is out! 814 commits · 363 contributors · 121 first-timers  🧭 New /v1/systemone structured-decision endpoint + generic hf tool/reasoning parser 🗜️ Low-precision KV everywhere: NVFP4 on SM8x/90/12x, FP8 KV default for GLM-5.x, 4-bit KV on ROCm 🛠️ Model Runner V2: GPU n-gram speculator, Elastic EP, PP+CP for MLA, now default on ROCm ⚡ Faster startup & serving: precompiled kernel downlo...
  [查看](https://x.com/vllm_project/status/2111814711956168760)
- Kimi K3 decode on NVIDIA GB300 NVL72: 842 tokens/s at batch 1 with DSpark 🚀  A unified CuTe DSL decode path fuses attention, MoE and communication, delivering 1.5–2× higher decode throughput in several tested configurations and up to 1.8× higher P90 interactivity on the @SemiAnalysis_ AgentX workload.  The post covers the kernel work, the correctness and long-context evals behind it, and benchmark...
  [查看](https://x.com/vllm_project/status/2111637219647840611)

## 👤 研究者动态（16条）

### @demishassabis [Isomorphic Labs / Google DeepMind] | Research

- RT @maxencefaldor: Four Gemini 4 Argon agents, one shared Minecraft world, one goal: defeat the Ender Dragon. 27 hours and 2,783 self-writt…
  [查看](https://x.com/demishassabis/status/2111699132217688417)

### @steipete [OpenClaw] | Application

- RT @fforres: Life is good now.  🎉 Tell your agent to: - create a new volume in you mac - disable fseventsd (and spotlight) on it - and move…
  [查看](https://x.com/steipete/status/2111822399884927050)

### @swyx [AI社区] | App

- i believe this essay i wrote 5 years ago is the closest i've ever come to @benthompson level of "nailing it" https://t.co/4GbAWZ7mst
  [查看](https://x.com/swyx/status/2111914776217747673)
- If you loved our jev pod with @completeskeptic and are in the react/js/frontend community (especially if i've seen your work before), hit me up and i can refer you in to typesafe
  [查看](https://x.com/swyx/status/2111751323389731265)
- RT @hackgoofer: Hello Software Engineers, I lead TypeSafe AI Model Capabilities team. We are hiring. Here are a few qualities we are lookin…
  [查看](https://x.com/swyx/status/2111750995143471310)
- RT @climatepaige: Single ladies in San Francisco: I know a guy who is a real catch who would be a GREAT dad! DM me for an intro!  if you fo…
  [查看](https://x.com/swyx/status/2111685069639389426)
- RT @ricklamers: Love this format; @swyx cooked, once again  https://t.co/B4UAwme7ce
  [查看](https://x.com/swyx/status/2111666858663522808)
- RT @milan_milanovic: The most life-changing books, statistically https://t.co/ReaEmH9W7F
  [查看](https://x.com/swyx/status/2111625302237757625)
- RT @hallerite: "Reading" is one of the core staples of "self-improvement" slopfluencers, but it's truly incredible how few books are actual…
  [查看](https://x.com/swyx/status/2111625288564293830)

### @thesephist [Anthropic] | Research

- RT @geoffreylitt: I recently gave a kinda personal talk at @recursecenter, where I shared some stories about taking your interests very ser…
  [查看](https://x.com/thesephist/status/2111945494620708936)
- RT @enjalot: but its not just aggregate data vis, its also crucial to zoom into a single trajectory and quickly get a handle on it. inspire…
  [查看](https://x.com/thesephist/status/2111822359330230666)
- RT @enjalot: i want new ways to look at lots of trajectories, currently exploring: - treemap laid out by groupings (metadata or computed) -…
  [查看](https://x.com/thesephist/status/2111822277490638895)
- It would be a tragedy for embedding models to become narrowly optimized for retrieval in the same way that generative text models have become narrowly optimized for conversational rollout. There is much magic to explore in the realm of representations.
  [查看](https://x.com/thesephist/status/2111624899680706715)
- RT @hamiltonulmer: More DAGs should be drawn this way. In a pipeline like the one below, the nodes form a list, so each node can be a table…
  [查看](https://x.com/thesephist/status/2111593101622128850)

### @ylecun [NYU] | Research

- RT @KenRoth: Trump’s longstanding groundless attacks on the integrity of voting systems are crystallizing into what many fear is an attempt…
  [查看](https://x.com/ylecun/status/2111648121809752394)
- RT @alexandr_wang: you’ll never believe what i saw on the highway today https://t.co/RnU3vKmFTN
  [查看](https://x.com/ylecun/status/2111590540701737351)
