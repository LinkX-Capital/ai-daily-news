# Research Agent 维护指南

## 一、日常维护

### 1.1 知识图谱更新

```bash
# 查看当前图谱状态
python knowledge.py summary

# 从历史新闻学习新实体/关系（最近7天）
python knowledge.py update 7

# 查询特定实体
python knowledge.py competitors 可灵AI
python knowledge.py track L4-应用Agent

# 对比多个实体
python knowledge.py compare 可灵AI Runway Sora
```

### 1.2 手动添加实体/关系

```python
from knowledge import Knowledge, Entity, EntityType, RelationType, Track

k = Knowledge()

# 添加新公司
k.graph.add_entity("deepseek", "DeepSeek", EntityType.COMPANY, Track.L2_MODEL,
                   description="中国开源大模型公司",
                   aliases=["深度求索", "深求"])

# 添加竞争关系
k.graph.add_relation("deepseek", "qwen", RelationType.COMPETES, 0.8, "开源模型竞争")

# 保存
k.graph.save()
```

### 1.3 更新被投企业列表

编辑 `research_agent.py` 中的 `LINKX_PORTFOLIO`:

```python
LINKX_PORTFOLIO = {
    "模型": ["智谱AI", "面壁智能", "生数科技", "新公司A"],
    "Infra": ["基流科技", "谦和益邦", "AGICmicro", "无问芯穹", "趋境科技"],
    # ... 添加新被投
}
```

---

## 二、质量改进

### 2.1 Feedback Log

创建 `feedback.md` 记录每次用户修正:

```markdown
## 2026-05-12

### 错误1: 竞品信息过时
- file: reports/20260512-可灵AI.md
- field: 竞争格局
- before: 只列了 Runway、Sora
- after: 补充了字节 Seedance、Luma AI
- reason: 知识图谱未更新，缺少新竞争者
- rule_hint: 视频生成赛道每季度更新竞品图谱
```

### 2.2 Prompt 优化

基于 feedback 定期更新 prompt（在 `research_agent.py`）:

### 2.3 质量检查

```bash
# 运行测试并检查质量
python research_agent.py --date 2026-05-12 --index 0 --full

# 检查:
# 1. 事实是否准确（对比原始来源）
# 2. 竞品是否完整
# 3. 投资建议是否具体可执行
```

---

## 三、数据管理

### 3.1 报告归档

```bash
# 报告位置
ls -la reports/

# 按月归档
mkdir reports/2026-04
mv reports/202604*.md reports/2026-04/

# 清理超过3个月的测试报告
find reports/ -name "*.md" -mtime +90 -delete
```

### 3.2 Archive 清理

```bash
# 压缩旧数据
gzip archive/news_2026-03-*.json
```

---

## 四、Token & 成本监控

### 4.1 查看消耗

每次运行会显示:
```
▶ Token 消耗统计:
  Stage 1: 1,091 in + 1,632 out = 2,723
  Stage 2: 1,292 in + 1,862 out = 3,154
  总计: 3,067 in + 4,072 out = 7,139 tokens
  预估成本: $0.0703
```

### 4.2 成本估算

| 用量 | Stage 1 | Stage 2 | 单次完整 |
|------|---------|---------|----------|
| Tokens | ~2,700 | ~3,100 | ~7,000 |
| 成本 (Sonnet) | ~$0.03 | ~$0.04 | ~$0.07 |
| 成本 (MiniMax) | ~$0.01 | ~$0.015 | ~$0.025 |

### 4.3 预算控制

```bash
# 设置月度预算检查
# 单次 ~$0.07, 100次/月 = $7, 1000次/月 = $70
```

---

## 五、定期任务

| 频率 | 任务 | 命令 |
|------|------|------|
| 每周 | 更新知识图谱 | `python knowledge.py update 7` |
| 每周 | 抽检报告质量 | 随机检查 2-3 份 |
| 每月 | 归档旧报告 | `mv reports/202604*.md archive/2026-04/` |
| 每季度 | 复盘 feedback.md | 提取规则更新 prompt |
| 每次新投资 | 更新 PORTFOLIO | 编辑 research_agent.py |

---

## 六、常见问题

### Q1: 报告质量下降
- 知识图谱过时 → `python knowledge.py update 7`
- LLM prompt 需调整 → 检查 feedback.md
- 搜索结果差 → 检查 source_url

### Q2: Token 消耗异常高
- Archive 范围过大 → 减少 `archive_days` (默认90)
- 历史动态太多 → 减少 `archive_results` (默认10)

### Q3: 知识图谱关系错误
```python
from knowledge import Knowledge, RelationType
k = Knowledge()
# 删除错误关系
k.graph.relations = [r for r in k.graph.relations if r.source != "wrong_id"]
# 添加正确关系
k.graph.add_relation("correct_id", "target", RelationType.COMPETES, 0.8, "...")
k.graph.save()
```

---

## 七、快速命令参考

```bash
# 知识图谱
python knowledge.py summary              # 概览
python knowledge.py competitors <公司>   # 查竞品
python knowledge.py track <赛道>         # 查赛道
python knowledge.py compare A B C        # 对比
python knowledge.py update 7             # 从新闻学习

# 研究报告
python research_agent.py --list-today                    # 列出今日条目
python research_agent.py --date YYYY-MM-DD --index N     # 研究指定条目
python research_agent.py --topic "<主题>" --full         # 完整研究
python research_agent.py --company "<公司>" --full       # 公司研究

# 验证器
python validator.py                                        # 测试验证
```

---

## 八、配置文件位置

| 配置 | 文件 |
|------|------|
| 被投企业 | research_agent.py `LINKX_PORTFOLIO` |
| 赛道关键词 | research_agent.py `TRACK_KEYWORDS` |
| 搜索限制 | research_agent.py `SEARCH_LIMITS` |
| 知识图谱 | knowledge_graph.db (自动生成) |
| 反馈日志 | feedback.md (手动创建) |
