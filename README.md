# AI 前沿动态 - 自动化管线

## 功能特性

1. **智能优先级排序** - 来源权重 + 热度关键词 + 时效性
2. **LLM 摘要提取** - 使用 MiniMax-M2.5 提取关键信息
3. **本地定时运行** - 无需 GitHub Actions
4. **历史存档** - 每日报告自动保存
5. **多平台通知** - 飞书/钉钉/Slack/邮件

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 设置环境变量
```bash
export ANTHROPIC_AUTH_TOKEN="your-api-key"
```

### 3. 测试运行
```bash
python feed_v2.py
```

### 4. 设置定时任务 (macOS)

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天早上8点运行）
0 8 * * * /Users/shenyalan/ai-daily-news/run_local.sh >> /Users/shenyalan/ai-daily-news/logs/cron.log 2>&1
```

或者使用 launchd:
```bash
# 创建 plist 文件
cat > ~/Library/LaunchAgents/com.ai-daily-news.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ai-daily-news</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/shenyalan/ai-daily-news/run_local.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>

# 加载定时任务
launchctl load ~/Library/LaunchAgents/com.ai-daily-news.plist
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `feed_v2.py` | 主脚本 (新版) |
| `feed.py` | 主脚本 (旧版) |
| `improve.py` | LLM 内容优化 |
| `notify.py` | 通知工具 |
| `run_local.sh` | 本地运行脚本 |
| `archive/` | 历史存档目录 |
| `logs/` | 日志目录 |

## 配置说明

### 优先级机制
- 来源权重: OpenAI/Google DeepMind > NVIDIA > YC > 顶级媒体 > 其他
- 热度关键词: 融资/收购/突破性研究 加分
- 时效性: 24小时内权重更高

### LLM 处理
- 自动提取关键信息
- 简化标题
- 添加影响/意义分析
- 过滤低质量内容

## 通知配置

在 `notify.py` 或环境变量中配置:

```bash
# 飞书
export FEISHU_WEBHOOK="https://open.feishu.cn/open-apis/bot/v2/hook/xxx"

# 钉钉
export DINGTALK_WEBHOOK="https://oapi.dingtalk.com/robot/send?access_token=xxx"

# 邮件
export SMTP_USER="xxx@gmail.com"
export SMTP_PASS="xxx"
export EMAIL_TO="xxx@xxx.com"
```
