# L1-b 资本绑定：AI 基础设施的全链条锁定图谱

> 研究日期：2026-05-11 | 优先级：高 | 状态：进行中

---

## 一、全景图：谁是锁定的，谁还是自由的

### 关键数字（2026）

| 资本方 | 投资/承诺方向 | 规模 | 锁定机制 |
|--------|-------------|------|---------|
| **NVIDIA** | OpenAI（$300亿）、其他AI公司 | $400亿+（2026年至今） | 投资→客户反购GPU，锁定需求 |
| **Google** | Anthropic（$40亿 + 5GW算力） | $400亿+ | 投资→AI公司购买TPU服务→资金回流 |
| **Amazon** | Anthropic（$250亿，含$100亿+云服务承诺） | $250亿 | 投资→AI公司使用AWS Trainium |
| **SpaceX/xAI** | 自建 Terafab 芯片工厂 | $119B（总），$55B（初期） | 垂直整合，绕过芯片采购 |
| **Peter Thiel** | Panthalassa 海上算力 | $1.4亿 | 能源侧切入，独立于陆地电网 |
| **Anthropic** | Google Cloud TPU（$2000亿/5年）、Akamai（$18亿/7年）、Amazon Trainium（$1000亿/10年） | $3000亿+承诺 | 锁定算力优先供应，分散来源 |
| **四巨头** | AI 基础设施 capex | **$7250亿**（2026年，+77%） | 需求侧的资本投入推高算力供给 |

### 锁定格局速写

```
NVIDIA ←——$300亿投资——→ OpenAI（最大客户）
Google ←——$400亿投资+5GW算力——→ Anthropic
Amazon ←——$250亿投资——→ Anthropic
                            ↓
                    Anthropic 还向 Akamai 承诺 $18亿
                            ↓
                    Anthropic 还向 AMD 承诺 $1亿（7年）
                            ↓
                    Anthropic 向 Google 承诺 $2000亿（TPU）
                            ↓
                    Anthropic 向 Amazon 承诺 $1000亿（Trainium）

SpaceX/xAI ——$55B-119B——→ Terafab 芯片工厂（Intel合作）
                                     ↓
                    覆盖：AI服务器/卫星/太空数据中心/Tesla自动驾驶/机器人

Panthalassa ←——$1.4亿——→ 海上波浪算力（Peter Thiel领投）
```

---

## 二、循环交易的结构分析

### 循环的完整路径

Bloomberg 的图解揭示了完整的循环结构：

```
云厂商/芯片商（NVIDIA/Google/Amazon）
    ↓ 投资（股权+算力承诺）
AI 公司（OpenAI/Anthropic）
    ↓ 采购算力/芯片（购买GPU/TPU/Trainium）
云厂商/芯片商
    ↓ 收入回流
AI 公司（训练模型→产品→收入）
    ↓ 融资/上市
投资者（部分回到起点）
```

这个循环在两个方向上成立：
- **NVIDIA → OpenAI**：NVIDIA 投 OpenAI $300亿，OpenAI 反购 NVIDIA GPU 填充数据中心
- **Google/Amazon → Anthropic**：云厂商投 Anthropic 数百亿，Anthropic 承诺数千亿采购云服务

### 循环的可持续性质疑

**质疑1：估值是否建立在真实的商业基础上？**
- Anthropic 零收入时估值 $2000亿+，DeepSeek 零收入时估值 $200亿+
- 如果没有循环投资，这些公司如何获得足够资金维持训练？
- OpenAI 2500亿+年收入是否来自真实市场还是来自关联方？

**质疑2：算力需求是否被过度锁定？**
- NVIDIA 同时投资 OpenAI 和 Anthropic——两者都在争抢 GPU 资源
- 投资承诺锁定了需求，但这些需求是否真实存在？
- 如果 AI 模型商业化失败，谁承担 GPU 过剩的风险？

**质疑3：监管会否介入？**
- NVIDIA 投资自己的最大客户是否违反反垄断？
- 云厂商同时投资和被投资是否构成利益冲突？
- 循环结构是否需要 SEC/FTC 审查？

### 反驳：循环也可以是正向的

- **需求锁定 → 产能保证**：NVIDIA 投资 OpenAI 确保订单量，降低 GPU 过剩风险
- **算力绑定 → 技术绑定**：Anthropic 使用 Google TPU → Google 获得 Claude 的安全能力背书
- **生态锁定 → 转换成本**：Anthropic 的 $3000亿承诺意味着很难迁移到其他云平台
- **资本换市场 → 市场换资本**：AI 公司获得资金，云厂商获得长期大客户

---

## 三、分层分析：谁被锁定了，谁还是自由的

### Layer 1：算力层

| 玩家 | 锁定状态 | 自由度 |
|------|---------|--------|
| **NVIDIA** | 被所有云厂商和AI公司依赖，但选择投资 OpenAI 而非独占 | 中等。投资是双刃剑——锁定需求但可能被反噬 |
| **AMD** | 被 OpenAI 锁定（160M股票期权），被 Anthropic 初步使用（$1亿） | 高。ROCm 性能14天提升75倍，正从NVIDIA生态外争夺客户 |
| **Google TPU** | 被 Anthropic 锁定（$2000亿/5年），超过 Alphabet 40% backlog | 低。对 Anthropic 高度依赖，但反过来 Anthropic 也被锁定 |
| **Amazon Trainium** | 被 Anthropic 承诺（$1000亿/10年） | 低。Anthropic 是 Amazon 的战略赌注 |
| **Intel** | 被 Terafab 绑定（SpaceX/Tesla/xAI），提供代工服务 | 中。代工模式比自研芯片风险低，但受制于 Musk 的决策 |

### Layer 2：模型层

| 玩家 | 锁定状态 | 自由度 |
|------|---------|--------|
| **OpenAI** | 被 NVIDIA $300亿投资锁定；被 Oracle/OpenAI/SoftBank $5000亿 Stargate 绑定 | 低。Oracle 是基础设施合伙人，但 AMD 提供了替代选择 |
| **Anthropic** | 被 Google+Amazon 合计 $650亿+锁定；多源算力（Akmai/Google/Amazon/Colossus1/SpaceX） | 中。算力来源最多样，但也意味着转换成本最高 |
| **DeepSeek** | 唯一的纯 MIT 开源前沿实验室；首次外部融资（腾讯/阿里，$200亿+） | 高。但腾讯/阿里融资意味着中国资本绑定 |
| **xAI/Grok** | 被 SpaceX/xAI 合并实体 $1.25万亿估值绑定；Terafab 自建芯片 | 中。垂直整合程度最高，但 IPO 后面临公开市场审查 |

### Layer 3：谁还是自由的

**目前相对自由的玩家：**
- **Meta**：最大 AI 推理用户（数千万 Graviton CPU），但无深度算力绑定；Llama 转闭源说明在探索新的价值捕获方式
- **Mistral**：开源路线，坚持独立发展，无大厂投资
- **国内模型公司**：DeepSeek 已经融资，Kimi/MiniMax 仍独立但承压

---

## 四、Terafab：一个独特的反锁定案例

### Terafab 的本质：绕过锁定，不是参与锁定

SpaceX/Tesla/xAI 的 Terafab 项目不是传统的"投资换锁定"，而是**垂直整合绕过芯片采购**：

```
传统路径：AI公司 → 向 NVIDIA/AMD 采购芯片
Terafab路径：SpaceX/xAI → 自建芯片工厂 → 芯片自用
```

这意味着：
- Terafab 不是 NVIDIA 的客户，而是 NVIDIA 的**潜在竞争对手**
- 如果 Terafab 成功，NVIDIA 失去一个重要客户（xAI/Grok）
- 芯片工厂 → 覆盖 AI服务器 + 卫星 + 太空数据中心 + Tesla自动驾驶 + 机器人

**Terafab 的风险：**
- $119B 总投资 vs $55B 初期——规模是最大风险
- Intel 代工模式是否可靠？Intel 制造能力在 7nm 以下仍落后台积电
- IPO 前为了给投资人信心而宣布大型项目——可能存在融资驱动而非技术驱动

**Terafab 的意义：**
- 它是第一个"用资本直接锁定芯片制造"的案例（而非投资已有的AI公司）
- 它的 IPO 估值（$1.75万亿-2万亿）会给整个 AI 基础设施市场定锚
- 如果成功，它会成为"AI公司垂直整合芯片制造"的模板

---

## 五、投资含义

### L1-b 资本锁定对投资决策的影响

**1. 闭源模型公司的估值逻辑正在重构**
- Anthropic 零收入估值 $2000亿+ → DeepSeek 零收入估值 $200亿+ → 差距不是技术，是资本绑定强度
- 纯技术实力（DeepSeek V4 benchmark 追平 GPT-5.5）不等于高估值，资本背书才是估值的主要驱动力

**2. 算力供应商的估值逻辑同样在重构**
- NVIDIA 投资 OpenAI $300亿 → OpenAI 反购 GPU → 这是锁定还是补贴？
- 回答这个问题，需要看 NVIDIA 的毛利率是否因为"投资换取出货量"而受益

**3. 新进入者的壁垒不是技术，是资本**
- 任何新进入 AI 基础层的公司，面临的不是技术壁垒，而是**没有足够的资本绑定云厂商/芯片商**
- AMD 是当前唯一有潜力的替代者（ROCm 追赶，OpenAI 股票期权，Anthropic 小额合同）

**4. 循环结构的崩塌路径**
- 如果任何一个环节失效（AI 公司商业化不及预期 / 云厂商停止投资 / 监管介入），整个循环可能崩塌
- 最脆弱的环节：Anthropic 的 $3000亿+承诺 vs 当前收入是否支撑？

### 追踪指标

| 指标 | 重要性 | 当前值 |
|------|--------|--------|
| Anthropic ARR | 验证 $3000亿+承诺的可持续性 | $440亿 |
| NVIDIA 毛利率变化 | 投资换出货量是否影响盈利能力 | 约75-78% |
| AMD ROCm 市占率 | 替代 NVIDIA 的进度 | 快速追赶中 |
| Terafab 工厂进度 | 2027/2028 是否实际开工 | 初期提案阶段 |
| 监管介入信号 | FTC/SEC 是否审查循环投资 | 暂无明确信号 |
| 云厂商 capex 实际 vs 预期 | 需求是否真实 | $7250亿（2026年计划） |

---

## 六、待追踪的问题

- [ ] Anthropic $3000亿+算力承诺的履约条件是什么？能否提前退出？
- [ ] NVIDIA 投资 $300亿换 OpenAI 出货量承诺——这是否在合同中有约束力？
- [ ] Terafab 的 $55B 初期投资，资金来源是 IPO 融资、债务、还是 Musk 个人/关联方？
- [ ] 四巨头 $7250亿 capex 中，有多少是实际建设 vs 承诺而未开工？
- [ ] Panthalassa 的 $1.4亿够建多少算力？波浪供电 vs 陆电的成本对比？

---

*最后更新：2026-05-11*