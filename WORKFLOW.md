# AI 日报工作流

## 自动管线（cron，周一到周五）

| 时间 | 任务 | 说明 |
|------|------|------|
| 7:15 | twitter_digest.sh | Twitter 抓取 |
| 8:00 | run.sh | 主管线（全自动） |

### run.sh 执行流程

```
1. 检查 archive/news_{当天}.json 是否存在
   ├─ 存在 → 跳过（你已手动跑过，防止覆盖）
   └─ 不存在 → 继续

2. feed_v5.py --cache
   抓取 RSS + Twitter → LLM 处理 → 生成 md + archive

3. html_generator.py
   从 md 生成 HTML + index.html（不从 archive JSON）

4. gen_screenshot.py → 手机端截图

5. notify.py → 飞书通知

6. git push → 推送到 GitHub
```

## 手动编辑后的发布

手动编辑了 `daily-ai-news.md` 后：

```bash
python3 html_generator.py   # md → HTML + index
python3 gen_screenshot.py   # 手机截图
python3 notify.py           # 飞书通知
```

或一键发布：

```bash
python3 publish.py
```

## 手动补充新闻

往当天日报加一条新闻：

1. 编辑 `daily-ai-news.md`，在对应分类下添加条目
2. `python3 html_generator.py` 更新 HTML
3. `python3 publish.py` 发布

## 防覆盖机制

- **run.sh**：`archive/news_{当天}.json` 存在则跳过整个管线
- **feed_v5.py --no-overwrite**：单独跳过覆盖 md 和 summary
- 典型场景：早上手动跑管线并编辑 → 8:00 cron 检测到 archive → 自动跳过

## 关键文件

| 文件 | 作用 | 输入 | 输出 |
|------|------|------|------|
| feed_v5.py | 主管线 | RSS + cache.json | archive/news_*.json + daily-ai-news.md |
| html_generator.py | MD→HTML | daily-ai-news.md | HTML + index.html |
| publish.py | 一键发布 | daily-ai-news.md | JSON + HTML + 飞书 + git push |
| qa.py | 质量检查 | daily-ai-news.md | 检查报告 |
| improve_news.py | 去重 | articles list | 去重后 articles |
| notify.py | 推送飞书 | daily-ai-news.html | 飞书卡片 |
| gen_screenshot.py | 生成长图 | daily-ai-news.html | daily-ai-news-mobile.png |

## 数据流向

```
RSS 源          tweet_fetcher
    |                 |
    +--------+--------+
             |
         feed_v5.py (LLM 处理)
             |
             +-> archive/news_*.json
             |
             +-> daily-ai-news.md -> 可手动编辑
                                        |
                                        v
                                  html_generator.py
                                        |
                                        +-> daily-ai-news.html
                                        +-> daily-ai-news-YYYY-MM-DD.html
                                        +-> index.html
```

## 注意事项

1. **HTML 从 md 生成**：使用 html_generator.py，不要手动编辑 HTML
2. **不要手动编辑 HTML**：每次都从 md 重新生成
3. **archive 存在即跳过**：run.sh 防覆盖机制确保手动编辑不被 cron 覆盖
4. **publish.py 是手动发布入口**：编辑完 md 后用 publish.py 一键完成发布
5. **qa.py 在发布前检查**：`python qa.py` 检查 body/insight 质量
