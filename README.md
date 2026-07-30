# AI 前沿动态日报管线

每天汇集 RSS、研究论文与研究者动态，经过全量选稿、中文编辑和发布硬门禁后生成日报。

## 现在的发布链路

```text
抓取与日期过滤
  → 保守去重（只提前删除确定重复）
  → 全量排序与编辑组合
  → 证据补充
  → 逐条中文写作
  → canonical / Markdown 双重硬门禁
  → 原子写入 MD、JSON、HTML
  → 截图、Git 推送、可选飞书通知
```

管线不再使用 safety net，也不会用英文原文或抓取摘要补足条数。任何入选条目写作失败、中文不足、含抓取残留、低价值推广信号或来源链路不明，都会阻断发布。

## 运行

```bash
# 最近一个已经闭窗的日报日期
./run.sh

# 指定日期或历史补跑
./run.sh 2026-07-28

# launchd/断点兜底
./catchup.sh 2026-07-28
```

日报窗口固定为北京时间 `[前一日 06:40, 当日 06:40)`。指定日期后，抓取、缓存、近三日去重、文件名和 manifest 都使用同一个日期。

## 人工编辑后的安全发布

```bash
# 检查人工编辑稿，准备产物并继续发布
python3 publish.py --date 2026-07-28

# 只生成通过门禁的 ready 产物，不截图、推送或通知
python3 publish.py --date 2026-07-28 --prepare-only
```

`publish.py` 也必须通过同一套硬门禁。QA 不通过时不会生成归档、发送通知或推送网页。

## 状态与恢复

每个日期都有 `archive/manifests/YYYY-MM-DD.json`：

- `running`：正在生成；
- `qa_failed`：质量门禁或生成步骤失败，禁止发布；
- `ready`：MD、JSON、HTML 已通过门禁，可从发布阶段续跑；
- `published`：截图、Git 推送和已配置的通知均成功。

续跑和推进 `published` 前都会重算内容哈希；门禁后任一产物被改动，就会拒绝直接发布并重新生成。只有日期匹配的 `published` 才代表完成，仅有归档文件不再被视为成功。

## 关键文件

| 文件 | 职责 |
|---|---|
| `feed_v5.py` | 抓取、全量选稿、证据准备、中文写作与 canonical 产物 |
| `improve_news.py` | 非新闻过滤与高置信事件去重 |
| `pipeline_core.py` | 稳定 ID、严格 LLM 协议、日期窗口与原子写入 |
| `release_gate.py` | 离线、确定性的发布硬门禁 |
| `qa.py` | Markdown 诊断与可选事实核查 |
| `run.sh` | 唯一自动发布入口及状态机 |
| `publish.py` | 人工编辑稿的安全发布入口 |
| `pipeline_manifest.py` | manifest 校验、状态推进和默认日期解析 |

选稿过程保存在 `archive/dropped_YYYY-MM-DD.json`，包含候选短编号、初排位置、最终排序、组合保护原因、事件重复关系和最终去向，便于复盘漏选。

## 环境变量

复制 `.env.example` 为 `.env`，至少配置：

```bash
MINIMAX_API_KEY=your_key
```

`FEISHU_WEBHOOK` 是可选项；未配置时明确跳过通知，配置后发送失败会阻断 `published`。也可通过 `PIPELINE_ENV_FILE` 指定环境文件。

## 验证

```bash
python3 -m unittest \
  tests.test_pipeline_core \
  tests.test_release_gate \
  tests.test_manual_publish \
  tests.test_qa_autofix \
  tests.test_qa_history

python3 test_selection_recall.py
bash tests/test_pipeline_scripts.sh
```

测试覆盖历史漏选、稳定 ID、写作缺项恢复、英文/低价值门禁、人工发布旁路、日期边界、失败传播、并发锁和断点续发。
