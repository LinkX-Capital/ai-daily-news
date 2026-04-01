# AI 日报工作流

## 最佳实践（验证版）

```
┌─────────────────────────────────────────────────────────────────┐
│  1. 单独抓取 Twitter 存档                                     │
│     目的：防止管线运行时网络抓取失败，确保数据可用性              │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. 运行管线 (feed_v5.py)                                    │
│     - 读取缓存推文                                             │
│     - 抓取 RSS                                                │
│     - LLM 分类和摘要                                           │
│     - 生成 JSON 存档 + markdown                               │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. 人工核对                                                   │
│     - 核对动态优先级（priority 字段）                           │
│     - 增减内容（漏抓的补上，无关的删除）                        │
│     - 修正分类                                                 │
│     - 编辑 daily-ai-news.md（如果需要）                          │
└─────────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. 生成并分发                                                 │
│     a. 从 markdown 重新生成 JSON（如果手动编辑过）                │
│     b. 运行 generate_html.py 生成 HTML                          │
│     c. 更新 index.html                                         │
│     d. 运行 html_generator.py 生成 HTML（含index）                │
│     e. 运行 notify.py 推送到飞书                                │
│     f. 运行 gen_screenshot.py 生成手机端长图                     │
└─────────────────────────────────────────────────────────────────┘
```

## 命令速查

```bash
# 1. 抓取 Twitter 存档（可提前运行）
python3 tweet_fetcher/main.py

# 2. 运行管线
python3 feed_v5.py

# 3. （人工编辑）daily-ai-news.md

# 4. 生成并分发
python3 html_generator.py  # 生成 HTML + 更新 index
python3 notify.py          # 推送飞书
python3 gen_screenshot.py  # 生成手机端长图
```

## 关键文件

| 文件 | 作用 | 输入 | 输出 |
|------|------|------|------|
| tweet_fetcher/main.py | 抓取 Twitter | - | cache.json |
| feed_v5.py | 主管线 | RSS + cache.json | archive/news_*.json + daily-ai-news.md |
| html_generator.py | 生成 HTML | daily-ai-news.md | daily-ai-news.html + daily-ai-news-YYYY-MM-DD.html + index.html |
| notify.py | 推送飞书 | daily-ai-news.html | 飞书卡片 |
| gen_screenshot.py | 生成长图 | daily-ai-news.html | daily-ai-news-mobile.png |

## 数据流向

```
RSS 源          tweet_fetcher
    │                 │
    └────────┬────────┘
             ↓
         feed_v5.py (LLM 处理)
             │
             ├─→ archive/news_*.json  (唯一真实数据源)
             │
             └─→ daily-ai-news.md     (可手动编辑)
                     │
                     ↓
                 html_generator.py
                     │
                     ├─→ daily-ai-news.html
                     ├─→ daily-ai-news-YYYY-MM-DD.html
                     └─→ index.html
```

## 注意事项

1. **Twitter 缓存优先**：单独抓取可确保管线不因网络问题中断
2. **使用 html_generator.py**：统一使用此脚本生成 HTML，不要用 generate_html.py
3. **HTML 从 md 直接生成**：不要手动编辑 HTML，每次都从 md 重新生成
4. **人工核对必不可少**：LLM 分类可能不准确，优先级需要人工调整
