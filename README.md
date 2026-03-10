# AI 前沿动态 - 自动化管线

## 功能特性

1. **智能优先级排序** - 来源权重 + 热度关键词 + 时效性
2. **LLM 摘要提取** - 使用 MiniMax-M2.5 提取关键信息
3. **GitHub Actions 自动运行** - 无需本地定时任务
4. **历史存档** - 每日报告自动保存
5. **飞书通知** - 每日推送

## 快速开始

### 1. 设置 Secrets

在仓库 Settings → Secrets and variables → Actions 中添加：

- `ANTHROPIC_AUTH_TOKEN`: MiniMax API Token
- `FEISHU_WEBHOOK`: 飞书机器人 Webhook URL

### 2. GitHub Actions 自动运行

每天 9:00 UTC（北京时 17:00）自动运行：
- 抓取新闻
- 生成 HTML
- 推送到仓库

### 3. GitHub Pages

在仓库 Settings → Pages 中开启：
- Source: Deploy from a branch
- Branch: main
- Folder: / (root)

访问 `https://yl0223-ai.github.io/ai-daily-news/` 查看。

## 本地运行（可选）

```bash
pip install feedparser httpx urllib3 python-dateutil

python feed_v5.py
python generate_html.py
python notify.py
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `feed_v5.py` | 主抓取脚本 |
| `generate_html.py` | 生成 HTML 页面 |
| `notify.py` | 飞书通知 |
| `run.sh` | 本地运行脚本 |
| `index.html` | GitHub Pages 首页 |
| `.github/workflows/daily-news.yml` | GitHub Actions 配置 |

## LLM 处理要求

- **标题**: 是什么+为什么重要（不用媒体口吻）
- **body**: 2句话完整摘要
- **key_points**: 从body提取新信息，不重复body
- **要点速览**: 只显示"是什么"
- **分类**: 模型前沿/产业动态/算力追踪/初创&融资/研究关注
