# AI 日报运行与恢复手册

## 自动运行

机器当前在每天 06:40 通过 `run.sh` 启动主管线。launchd 的 catch-up 入口用于兜底；两者共用同一把锁，不会并发生成或重复发布。

```text
run.sh
  ├─ 解析唯一 REPORT_DATE 与 24 小时闭窗
  ├─ 获取共享锁
  ├─ published → 幂等结束
  ├─ ready → 从截图/发布阶段续跑
  └─ 其他状态
       ├─ feed_v5.py 抓取并保存日期缓存
       ├─ 全量候选选稿 + 编辑组合
       ├─ 逐条中文写作与失败隔离重试
       ├─ canonical / rendered-md 双门禁
       └─ MD、JSON、HTML、manifest=ready

ready
  → 手机截图
  → 仅提交当日网页产物
  → Git push
  → 可选飞书通知
  → manifest=published
```

任一步失败都会返回非零状态；后续截图、Git、通知和 `published` 不会被误执行。

## 日期与缓存

- 日报日期 `YYYY-MM-DD` 对应北京时间 `[前一日 06:40, 当日 06:40)`。
- 开区间终点不包含 06:40:00，避免相邻两天重复。
- 历史补跑必须显式传日期：`./run.sh 2026-07-28`。
- 抓取缓存按日期保存到 `cache/raw_news_YYYY-MM-DD.json`。
- 跨天只删除 canonical URL 完全相同的条目；标题或实体相似只标注给选稿阶段复核。

## 选稿规则

1. 所有合格候选都有稳定 `candidate_id`，模型只接触短编号。
2. 不设公司/来源的预先截断，排序模型扫描全量候选。
3. 同一事件的多来源报道在排序后合并，保留信息更接近底层动作的一条。
4. Top 15 同时覆盖重要研究、机器人、前沿能源和大额战略资本动作。
5. 不使用 safety net，不用低价值或英文原文强行补足条数。
6. 每次决策都写入 `archive/dropped_YYYY-MM-DD.json`。

## 发布硬门禁

以下任一情况都会进入 `qa_failed`：

- 条目为空、超过 15 条、分类非法或稳定 ID 重复；
- 标题、正文或 insight 中文不足，含连续英文原句；
- 抓取标记、摘要元数据、HTML 实体等原文残留；
- 招聘、报名、活动预告等低价值推广信号；
- body 少于两个完整句子；
- 发现 safety net/raw fallback 路径；
- 缺少可验证的写作 provenance；
- Markdown 解析后的条目数与 canonical 不一致。

门禁之后没有自动改写或补条逻辑，已审核内容不会再被静默改变。

## 故障恢复

查看状态：

```bash
python3 pipeline_manifest.py check \
  --path archive/manifests/2026-07-28.json \
  --date 2026-07-28 \
  --status published
```

- `qa_failed`：查看 manifest 中的 `failure` / `qa`，修复后重新运行指定日期。
- `ready`：直接再次运行 `./run.sh YYYY-MM-DD`，不会重新抓取或改写。
- `published`：再次运行会安全跳过。
- 退出码 `75`：已有实例持有共享锁，等待该实例结束即可。

`ready` 续跑及 `published` 状态推进前会重算 MD、JSON、HTML 的组合哈希；门禁后发生的任何文件改动都会使直接发布失败。

`catchup.sh` 只有看到日期匹配的 `published` 才记录成功；子进程失败会原样向上传递。

## 人工编辑

编辑 `daily-ai-news-YYYY-MM-DD.md` 后使用：

```bash
python3 publish.py --date YYYY-MM-DD
```

该入口会重新解析 Markdown、生成稳定 ID、标注人工 provenance、执行双门禁、原子更新归档与 `ready` manifest，再委托 `run.sh` 完成截图、Git 和通知。不要直接调用 `notify.py`、`gen_screenshot.py` 或手工改 HTML 来绕过状态机。

## 常用诊断

```bash
# 只检查 Markdown，不发布
python3 qa.py YYYY-MM-DD

# 可选：逐条事实核查（需要对应环境凭据）
python3 qa.py --factcheck YYYY-MM-DD

# 从已通过门禁的人工稿只准备 ready 产物
python3 publish.py --date YYYY-MM-DD --prepare-only
```

HTML 始终从 Markdown 生成；canonical JSON 保存经过编辑的公开字段，原始标题、抓取正文和写作证据只保留在缓存/审计链路中。
