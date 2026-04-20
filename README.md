# AI 前沿动态 - 自动化管线

每日自动追踪 AI 领域前沿进展，生成结构化日报，推送给 LP。

## 管线流程

```
RSS + Twitter → LLM处理 → MD → QA质检 → 人工修正 → HTML/截图/飞书 → Git
```

**自动（cron 每天 6:00）：**
1. `twitter_push.py` — 抓取 Twitter 账号推文，缓存到 `tweet_fetcher/cache.json`
2. `feed_v5.py --cache` — RSS 抓取 → LLM(MiniMax-M2.5) 分类/摘要 → 生成 `daily-ai-news.md`
3. `html_generator.py` — MD → HTML（含日期归档 + index.html）
4. `gen_screenshot.py` — Playwright 生成手机端长图
5. `notify.py` — 飞书 webhook 推送
6. git push 到 GitHub Pages

**手动（Claude Code 辅助）：**
1. `python qa.py` — 10 项质量检查
2. `python qa.py --factcheck` — +LLM 事实校验（抓原文比对）
3. 修正 md → 重新生成 HTML/截图/飞书/git push

## 关键文件

| 文件 | 职责 |
|------|------|
| `feed_v5.py` | 主管线：RSS抓取 + LLM处理 + 生成MD |
| `config_loader.py` | 配置加载（RSS源、Twitter账号、分类规则） |
| `improve_news.py` | 新闻质量优化（过滤/分类修正/去重） |
| `html_generator.py` | MD → HTML（含 parse_md 解析器） |
| `gen_screenshot.py` | Playwright 生成手机端长图 |
| `notify.py` | 飞书 webhook 推送 |
| `qa.py` | 质检层：10项检查 + LLM事实校验 |
| `run.sh` | cron 定时脚本 |

## 数据源

- **RSS Feeds**：新智元、量子位、机器之心、36氪、IT桔子等（通过 config.json 配置）
- **Twitter**：SemiAnalysis、Luma、vLLM、x.ai、Yann LeCun 等（`tweet_fetcher/`）
- **手动补充**：用户提供 URL，Claude Code 抓取原文后写入 MD

## LLM 处理规范

- **Title**：事件主体 + 做什么 + 为什么重要（不用媒体口吻/感叹号）
- **Body**：3-6 句话完整摘要，必须有 so what（为什么重要），关键判断加粗
- **Insight**：基于原文事实，禁止过度推断和空洞宏大叙事
- **分类**：模型前沿 / 产业动态 / 算力追踪 / 初创&融资 / 研究关注 / X讨论
- **海外公司/人名不翻译**：保持英文（OpenAI、Google、Anthropic 等）

详细规范见 `CLAUDE.md`。

## 环境配置

```bash
# 必需环境变量
MINIMAX_API_KEY=sk-cp-xxx        # MiniMax LLM API（feed_v5.py + qa.py）

# 飞书推送
FEISHU_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/xxx

# 可选：邮件推送
SMTP_SERVER=smtp.qiye.aliyun.com
SMTP_USER=xxx@xxx.com
SMTP_PASSWORD=xxx
EMAIL_RECIPIENTS=lp1@xxx.com,lp2@xxx.com
```

## Cron 配置

```bash
# 每天 6:00 运行主管线
0 6 * * * source /Users/shenyalan/ai-daily-news/run.sh >> /Users/shenyalan/ai-daily-news/logs/cron.log 2>&1

# 工作日 7:15 运行 Twitter 摘要
15 7 * * 1-5 /Users/shenyalan/ai-daily-news/twitter_digest.sh >> /Users/shenyalan/ai-daily-news/logs/cron_twitter.log 2>&1
```

## QA 质检层

```bash
python qa.py              # 快速 10 项检查（秒级）
python qa.py --factcheck  # + LLM 事实校验（逐条抓原文比对，约 5 分钟）
```

10 项检查：
1. 低价值条目检测（活动/招聘/品牌宣传）
2. 分类校验
3. 同公司去重（>2 条告警）
4. 过度推断检测
5. Body 质量（句数 + so-what）
6. 来源链接完整性
7. 要点速览同步
8. Insight 重复标题检测
9. 启发式事实校验（模糊称呼/英文名翻译/无依据声称）
10. LLM 事实校验（MCP web-reader 抓原文 → MiniMax 比对）

事实校验抓取链路：MCP web-reader（绕付费墙）→ httpx → web-search 搜索替代来源

## 输出

| 文件 | 说明 |
|------|------|
| `daily-ai-news.md` | 当天日报（Markdown，源文件） |
| `daily-ai-news.html` | 当天 HTML |
| `daily-ai-news-YYYY-MM-DD.html` | 历史归档 |
| `daily-ai-news-mobile.png` | 手机端长图 |
| `index.html` | 总索引页 |
| `archive/` | JSON 格式历史存档 |
