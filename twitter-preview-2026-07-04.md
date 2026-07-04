# Twitter 动态预览
**日期**：2026-07-04 07:15
**窗口**：2026-07-03 07:00 - 2026-07-04 08:00 北京时间
**总计**：41 条推文

---

## 📋 过滤说明

**抓取规则**：24小时内、去除重复账号、内容 >30字符
**存疑过滤**：无

---

## ⭐ 今日重点（LLM 提炼）

1. **中国去年新增543吉瓦电网容量，其中434吉瓦来自可再生能源，而美国仅增加53吉瓦**
   @ylecun
2. **未来18个月内，RTX 5090 GPU将能运行GLM 5.2同等智能水平的模型**
   @swyx
3. **Vercel高管解读：智能体代表新型软件形态，Vercel自身也在转变为智能体**
   @swyx
4. **Meta研究发现量化推理模型的失败模式：模型在推理中途得出正确答案后，反而因犹豫而自我否定**
   @TheTuringPost
5. **Transformer架构全面解析：从token嵌入、自注意力机制到GPT和BERT的工作原理**
   @TheTuringPost

---


---

## 抓取失败账号
- @deepseek: https://nitter.hu ConnectError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1028)
- @liquid: https://nitter.hu ConnectError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1028)
- @minimax: https://nitter.hu ConnectError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1028)

---

## 📄 全量抓取内容

# Twitter 窗口抓取
窗口：2026-07-03 07:00 - 2026-07-04 08:00 北京时间

抓取账号数：45；命中推文：41；失败账号：3

## 1. @ylecun · 07-03 07:21
China added over 543 Gigawatts to their grid last year. 434 GW was renewables because they are faster to build. The U.S. added a paltry 53 GW. We are losing the “AI race” to China because these idiots hate green energy. This is suicide by stupid. Secretary Chris Wright (@SecretaryWright) I'm thrilled to report that after 35 years, on July 4th, we will end the subsidies for new wind and solar projects, thanks President Trump’s Working Families Tax Cut. Video — https://nitter.net/SecretaryWright/status/2072743412080504921#m

来源: https://x.com/FPWellman/status/2072823095178453168#m

## 2. @swyx · 07-03 07:26
“Within the next 18 months, you will be able to host GLM 5.2 equivalent intelligence on an RTX 5090 GPU.” -Ahmad Osman, AI World’s Fair

来源: https://x.com/MikeBradleyAI/status/2072824211702444318#m

## 3. @ylecun · 07-03 07:51
Article Concentration of power in AI is a risk, not a solution The answer to concentration of power in AI is not openness at all costs, but a serious research commons with the resources to compete. Over the past few months, I've become increasingly uneasy about

来源: https://x.com/andykonwinski/status/2072830533739192560#m

## 4. @swyx · 07-03 08:41
In this interview at @aiDotEngineer World's Fair, @vercel chief of software @andrewqu explains why agents represent a new form of software, what Vercel learned from building its own, and why Vercel itself is turning into an agent! latent.space/p/vercel-agents… Link Vercel's Andrew Qu on why agents are a new kind of software The Vercel Chief of Software explains how its agent framework, eve, was created — and why skills, sandboxes and agent-readable websites now matter. latent.space

来源: https://x.com/latentspacepod/status/2072843022572953963#m

## 5. @gklambauer · 07-03 09:25
Claude Science is incredible. I gave it some sequencing data, and in 8 hours it did a full analysis, generated figures, wrote a paper, submitted it for publication, got rejected, revised and resubmitted, got rejected again, it is now applying for positions in industry

来源: https://x.com/blekhman/status/2072854130133967018#m

## 6. @TheTuringPost · 07-03 10:22
"Quantized Reasoning Models Think They Need to Think Longer, but They Do Not" @AIatMeta found a weird failure mode in quantized reasoning models: ▪️ They don’t just get cheaper and less capable – they start overthinking. In up to 52% of failures, the model actually reaches the correct answer halfway through its reasoning... then talks itself out of it. It spirals into hesitation with "wait," "but," "maybe," and new branches. Why does this happen? Quantization mainly affects high-uncertainty decoding steps. It makes hesitation tokens much more likely to be sampled, sending the model into unnecessary self-reflection. → Meta proposed a very simple fix: apply a small decoding penalty to about 50 hesitation tokens. No retraining. Results: • 12–23% shorter Chain-of-Thoughts • Up to 58% fewer overthinking errors • Accuracy is often preserved (or even improved) across math, coding, and science benchmarks. So knowing when to stop is almost as important as knowing how to reason.

来源: https://x.com/TheTuringPost/status/2072868677872157078#m

## 7. @TheTuringPost · 07-03 10:23
arxiv.org/abs/2606.00206 Link Quantized Reasoning Models Think They Need to Think Longer, but They Do Not Post-training quantization (PTQ) is widely used to deploy large language models efficiently, but its effect on reasoning models is not well understood. Across math, coding, and science QA, we find... arxiv.org

来源: https://x.com/TheTuringPost/status/2072868690979385762#m

## 8. @TheTuringPost · 07-03 10:54
A great source to understand or refresh Transformer architecture It explains how transformers process text token by token, using self-attention to build contextual representations Covers: - Token embeddings and positional encodings - The residual stream that carries information across layers - Multi-head self-attention and long-range dependencies - Feedforward networks, layer normalization, and residual connections - Transformer blocks stacked into deep language models - The language modeling head that predicts the next token It also connects these concepts to GPT and BERT

来源: https://x.com/TheTuringPost/status/2072876709284852116#m

## 9. @TheTuringPost · 07-03 10:54
web.stanford.edu/~jurafsky/s…

来源: https://x.com/TheTuringPost/status/2072876721674793367#m

## 10. @TheTuringPost · 07-03 10:55
Also, check out our article on what it actually takes to get from tokens to answers in LLMs turingpost.com/p/llm-inferen… Link AI 101: From Tokens to Answers: What Actually Happens During LLM Inference How LLM inference works end-to-end: tokenization, embeddings, prefill, decode, KV cache, batching, retrieval, and modern inference orchestration. turingpost.com

来源: https://x.com/TheTuringPost/status/2072876733746061326#m

## 11. @gklambauer · 07-03 13:55
TiRex-2: IT-giants are no match for us! Sepp Hochreiter (@HochreiterSepp) 1/5🚀 Introducing TiRex-2— our next-generation time series foundation model. Time series forecasting in the real world is streaming: -new observations continuously arrive, -variables interact, -some covariates are known for the future, -models must update predictions efficiently. — https://nitter.net/HochreiterSepp/status/2072676772953424034#m

来源: https://x.com/gklambauer/status/2072922052701417897#m

## 12. @vllm_project · 07-03 15:15
🎙️ @Alibaba_Qwen 's Qwen3-Omni listens, reasons, and talks back. Serving that in real time is a pipeline problem, not a single model: a multimodal Thinker, then Talker → Code2Wav for the speech. Each stage bottlenecks differently, so the wins come from optimizing them layer by layer. One neat trick: under load, replicate only the two speech stages and let the heavy multimodal Thinker run once. At high concurrency that lands first audio in ~0.6s instead of ~6s, speech faster than real time, and ~5.4x the throughput on the same GPUs. Built with @AntGroup 's Super Computing Technology (SCT) team and the vLLM-Omni team. The blog breaks down the full stack, one bottleneck at a time 👇 🔗 vllm.ai/blog/2026-07-01-qwen…

来源: https://x.com/vllm_project/status/2072942203966812438#m

## 13. @gklambauer · 07-03 15:35
G-RRM: Guiding Symbolic Solvers with Recurrent Reasoning Models Symbolic solver have to branch to check different choices -- recurrent reasoning models ( not LLMs!) can help them to speed up solving. BTW: Frontier AIs fail here! P: arxiv.org/abs/2607.02491

来源: https://x.com/gklambauer/status/2072947444812247199#m

## 14. @gklambauer · 07-03 16:11
We used SE-RRM to guide the solver. Richard and I will be available at our ICML poster on SE-RRM next week in Seoul. See you there! Günter Klambauer (@gklambauer) G-RRM: Guiding Symbolic Solvers with Recurrent Reasoning Models Symbolic solver have to branch to check different choices -- recurrent reasoning models ( not LLMs!) can help them to speed up solving. BTW: Frontier AIs fail here! P: arxiv.org/abs/2607.02491 — https://nitter.net/gklambauer/status/2072947444812247199#m

来源: https://x.com/AndreasMayr11/status/2072956297478082684#m

## 15. @ylecun · 07-03 17:49
Using AI to improve cancer immunotherapy outcomes, via training from transcriptomes of 10,000 tumor samples, 33 cancer types @NatureMedicine nature.com/articles/s41591-0… Link Generalizable AI predicts immunotherapy outcomes across cancers and treatments Nature Medicine - COMPASS is a pan-cancer foundation model that predicts immunotherapy response, across cancer types and treatments, from bulk tumor transcriptomes. nature.com

来源: https://x.com/EricTopol/status/2072981022581444951#m

## 16. @claudeai · 07-03 20:59
Squidsoup is a collective of artists and designers who make immersive experiences with sound, light and space. We caught up with them before one of their largest projects to date: a live performance with an orchestra at the Southbank Centre in London. Video

来源: https://x.com/claudeai/status/2073028947478995406#m

## 17. @ylecun · 07-03 21:35
Exactly. I've been disseminating a similar message for years. The concentration of power in AI and the desire for control is by far the biggest danger of AI. It could lead to a few private companies and/or countries being in control of access to information, access to knowledge, and access to the tools of economic expansion. It's a kind of medieval obscurantism akin to the Ottoman empire banning the use of the printing press for 200 years, in part to keep control of the dogma, but also to protect the corporation of the calligraphers and scribes. Relevant historical bits about the Internet: 1. It took a deliberate decision by Al Gore and Bill Clinton to open up access of what was then ARPAnet to commercial entities and to the public, against the desires of the entrenched telecom industry. During a public roundtable about the "information superhighway" in 1993, the CEO of AT&T told Gore and Clinton "leave it to us". Gore said no. 2. In the late 1980s, setting up an Internet presence required buying proprietary hardware with proprietary OS and software stack from Sun Microsystems, HP, IBM, or Dell. By the 2000s, all of this was wiped out by commodity hardware, Linux, Apache, and an entirely free/open software stack. This migration to open platforms was the result of market forces. Infrastructure wants to be open. Foundation models are becoming an infrastructure and will inevitably become commoditized. Long term, the money is in the application layer, which is what I, Arthur Mensch, Alex Karp, and others have been saying.

来源: https://x.com/ylecun/status/2073037974153896312#m

## 18. @ylecun · 07-03 22:04
Brazenly self-serving: the Trump family’s earnings during his first year in office "have moved him into an echelon of enrichment more associated with strongmen in Russia and Turkey." trib.al/imEzjid Link Trump’s Huge Windfall Has Few Known Global Precedents President Trump’s earnings in office are at a level once unimaginable for any leader of a liberal democracy, particularly a sitting American president. nytimes.com

来源: https://x.com/KenRoth/status/2073045340006068269#m

## 19. @swyx · 07-03 22:19
None of it was an accident. A team that gave up recharge week, and a partnership @GeoffBibby built with @swyx + the AI Engineer crew that turned a year-old idea into the biggest stage in AI eng. Thank you swyx and @liamcbride for the trust and the hospitality.

来源: https://x.com/mnair1/status/2073049060412371065#m

## 20. @swyx · 07-03 23:26
Recorded an impromptu podcast episode with @swyx for @latentspacepod last month at @aiDotEngineer SG. Covered good ground including: - Why "second brain" is the killer agent use case - Messaging platform tier list - NanoCo's origin and business model piped.video/hLUGXO5DSpo?si=buMG… Link The Blueprint for Autonomous Work Agents | Gavriel Cohen, NanoClaw We chat with the founder of NanoClaw at AI Engineer Singapore! youtube.com

来源: https://x.com/Gavriel_Cohen/status/2073065932897779984#m

## 21. @ylecun · 07-03 23:56
Are you ready for the open-source AI summer™️? Video

来源: https://x.com/ClementDelangue/status/2073073416114995300#m

## 22. @swyx · 07-03 23:56
I've been going to tech conferences since eternity and I have to say @aiDotEngineer is something else every time I go I meet coolest people, we stay in touch and ship cool things together, it eventually alters @huggingface ecosystem this time I met @0xSero @alexocheema @TheAhmadOsman @NaderLikeLadder we have so much work to do on local AI, last time in AIE Europe we shipped a ton for your Claws on Hub 🙌🏼 but also I meet my long time internet friends like @josephofiowa @danielhanchen @llm_wizard or people I'm a fan of @willccbb @latkins 🐐 talent density and signals in talks are immense and it takes a huge skill to pick people, many thanks @swyx for putting it together 🫶🏻 you do god's work

来源: https://x.com/mervenoyann/status/2073073440395768109#m

## 23. @svlevine · 07-04 00:09
We can think of this as the robot analogue of RL for thinking, optimizing for good "thoughts" through trial-and-error. The surprising thing is that it's so fast, learning in under a hundred real-world trials. Website: semantic-action-rl.github.io… Paper: arxiv.org/abs/2606.31958 Link Adapting Generalist Robot Policies with Semantic Reinforcement Learning We run RL over a VLA's language prompts, enabling efficient real-robot adaptation on complex & long-horizon tasks, where existing methods for improving robot behavior in deployment struggle. semantic-action-rl.github.io

来源: https://x.com/svlevine/status/2073076767292813579#m

## 24. @svlevine · 07-04 00:09
With our method, SARL, the policy steers the robot to put the gripper over the hammer before telling it to move down, so that it's obvious which object is the right one, and it works! Video

来源: https://x.com/svlevine/status/2073076765824831538#m

## 25. @svlevine · 07-04 00:09
If we get a VLM high-level policy to break down the task into steps, which is a common trick to solve more complex prompts, we get reasonable intermediate steps, but the VLM still keeps asking for the hammer -- it doesn't know what the robot can and can't understand! Video

来源: https://x.com/svlevine/status/2073076763199262901#m

## 26. @svlevine · 07-04 00:09
Here is a nice example to illustrate the main idea: the VLA trained on Bridge doesn't know what a hammer is (I know...), so if we just ask it to put the hammer on the plate for an iron-rich meal, it grabs the spoon instead (good guess!). Video

来源: https://x.com/svlevine/status/2073076761110401348#m

## 27. @svlevine · 07-04 00:09
The RL bit looks almost exactly like normal RL, but with language commands as the actions. B/c good VLAs are so steerable, these actions are very expressive. We run RL in the real world directly, in real time, and show that the robot can master tasks in under 100 episodes.

来源: https://x.com/svlevine/status/2073076759034298876#m

## 28. @svlevine · 07-04 00:09
The idea is simple: instead of running RL over robot actions, run RL over language commands to a VLA. This is much easier, because any vision-language model worth its salt provides a great prior over likely semantic commands, so RL has a much smaller search space.

来源: https://x.com/svlevine/status/2073076756920287626#m

## 29. @svlevine · 07-04 00:09
If you want a robot to do something well, you need to know how to talk to it. If you don't, you can learn, with Semantic Action RL! In our paper, @JagdeepBhatia8 , @ajwagenmaker , @verityw_ show how RL over VLA prompts enables new tasks and learns blazing fast in the real world! Video

来源: https://x.com/svlevine/status/2073076755108377009#m

## 30. @swyx · 07-04 00:11
That's a wrap of @aiDotEngineer World's Fair 2026 🥳 Many times larger than in previous years and yet it still felt like an intimate gathering of friends and family, what an incredible production by @swyx and the entire team and army of volunteers 💪 Thanks for great talks, insightful workshops, a fantastic expo and hallway track, fabulous side events and the awesome newly added music corner (thank you @FeatherlessAI !) I love how this conference is just so wholesomely centered around humans 🫶 Can't wait to see y'all in NYC in the fall!

来源: https://x.com/thorwebdev/status/2073077114929287236#m

## 31. @swyx · 07-04 01:32
Had a long and eventful week at @aiDotEngineer It’s time to go back to Paris and ship. Taking back some great conversations, ideas and new friends. Great show @swyx . @GradiumAI and I will be back with more events. PS: We’re hiring in SF!

来源: https://x.com/BhosalePratim/status/2073097508742668489#m

## 32. @swyx · 07-04 01:33
Some notes from @aiDotEngineer world fair: > the energy was incredible. it's magical to have a large group of smart, hungry, technical, and driven people learning from each other under one roof. > the frontier is accelerating rapidly. in six months, we went from software factories barely being a thing to questioning whether it makes sense/what comes next. > the CL convergence: companies previously doing observability, evals, memory, fine-tuning, agent improvement are all now focussed on continual learning. > memory has become a super load-bearing term. databases (oracle), knowledge bases, personalization, company knowledge, agent continuity can all be described as memory. > agentic commerce is being slept upon. the talks barely had attendance, even though volume/traction is accelerating. > the ai in gtm track was fun! packed with tactical advice and a glimpse into how job functions beyond coding changing > ai is the great levelling field. folks with 10 years of experience in their domain learning from those with one year of ai-native experience in the llm-native version of the same domain. > new jobs are being created as we speak - met someone who is a "software factory manager" internally within their team. > talks that stood out: @RLanceMartin on claude for long-horizon talk, @BurnedChris on AEO for dev tools, @theo on thinking bigger. > kudos to @swyx , @liamcbride and the AIE team. incredible organization, impressive scale, no major visible hiccups - this could not have been easy.

来源: https://x.com/shloked/status/2073097807804969087#m

## 33. @bobmcgrewai · 07-04 01:33
America turns 250 this week and Silicon Valley is still debating whether it's ok to work with the US military... Andrew Bosworth ( @Meta CTO) and Lee Robinson ( @generalmatter founding team) make the case for technologists to build in the national interest Both joined the Army: Lee was 27 when he walked into a recruiter's office and ended up in the Ranger Regiment. @boztank was 44, already exec at Meta, when he got a cold call from @ssankar They also serve America through the technologies they choose to build, from LLMs to uranium enrichment We cover: 8:25 - the unglamorous tech the country needs: chips, energy, manufacturing, infra 11:15 - how the US went from inventing uranium enrichment to producing 0.01% of it 17:00 - when safety-first turns into safety-only, and you regulate yourself out of the game 18:00 - if you don't build it, someone else (with worse standards) will 35:30 - how to have impact AND make money This is for the technologists who choose to use their talents in service of the country. Happy 4th! Video

来源: https://x.com/lulumeservey/status/2073097814070939883#m

## 34. @LangChain · 07-04 02:46
OpenWiki is at 1.7k stars in just 3 days! Right now it's just for codebases, but we're working to expand it to everything for memory. What do you want to see in a general purpose memory wiki agent? github.com/langchain-ai/open…

来源: https://x.com/BraceSproul/status/2073116191116431497#m

## 35. @swyx · 07-04 03:01
. @aiDotEngineer World's Fair was one of the most unique, interesting conferences I've been to: - incredible conversations with builders - hilarious & creative touches (shout out @swyx ) from a flash mob to cleric costumes and the integration of the USMNT game - a @altryne / @thursdai_pod livestream alongside excellent talks + stellar side events like the Agent Open by @jerryjliu0 + @murtazakhomusi & @morgane_paloma Fantastic week with @chaoyu_ & the rest of the @Modular team - exciting times ahead in AI!

来源: https://x.com/ConorBronsdon/status/2073119902391750730#m

## 36. @swyx · 07-04 04:22
The @aiDotEngineer World's Fair was fantastic! A well curated, info and fun packed event by @swyx & team. Definitely go in future if you have a chance.

来源: https://x.com/addyosmani/status/2073140413851123756#m

## 37. @swyx · 07-04 04:32
Had an amazing time talking to some of the most energetic builders in AI at @aiDotEngineer thanks to @swyx for organizing and thanks to @altryne and friends for hallway chats and podcasts to share about what everyone is building. This year marks the clear transition from agents to multi-agent spaces that are continuously evolving and learning. Below are the top slides that you should not miss.

来源: https://x.com/Gangadhar_P/status/2073142948020318689#m

## 38. @ylecun · 07-04 05:11
I’ve been asked many times over why I keep posting when so many of the replies I receive are personal attacks. The answer is actually really simple. As scientists, we cannot concede to silence. If we do, we leave space for disinformation to fill the void. and it will. Science doesn’t advance by being the loudest voice. But it does depend on people willing to keep speaking out - even and perhaps especially during the most difficult chapters.

来源: https://x.com/DrCatharineY/status/2073152550597984441#m

## 39. @swyx · 07-04 05:16
had alot of fun at @aiDotEngineer - nerding out about Codexmaxxing, meeting old friends and making new ones congratulations @swyx and team for the fantastic conference!

来源: https://x.com/gabrielchua/status/2073153836966092993#m

## 40. @swyx · 07-04 05:29
Individual AIE World's Fair SFO videos aren't out yet — so here's a timestamped index of all 3 days of main-stage. See all sessions summary and jump straight to any session: wfsf.gopicreations.com/recor… cc @aiDotEngineer @swyx Link AI Engineer World's Fair 2026 — Session Index Jump straight to any talk across three full days of main-stage recordings. wfsf.gopicreations.com

来源: https://x.com/gopikori/status/2073157099568378068#m

## 41. @swyx · 07-04 07:30
seriously tho who is this dance crew because they were GOOD in bug suits Lynsey Smith (@misslynsey) Okay @greptile I was unfamiliar with your game @aiDotEngineer Video — https://nitter.net/misslynsey/status/2072766433155776657#m

来源: https://x.com/swyx/status/2073187695803969593#m


---

## 抓取失败账号
- @deepseek: https://nitter.hu ConnectError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1028)
- @liquid: https://nitter.hu ConnectError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1028)
- @minimax: https://nitter.hu ConnectError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1028)
