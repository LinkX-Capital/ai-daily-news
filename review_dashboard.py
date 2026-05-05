#!/usr/bin/env python3
"""
AI Daily News - 交互式审核工作台
将人工审核时间从 30 分钟缩短至 5 分钟

用法：
    streamlit run review_dashboard.py -- --date 2026-04-28
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

import streamlit as st

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from html_generator import parse_md
from qa import (
    check_low_value, check_categories, check_company_dup,
    check_over_inference, check_body_quality, check_source,
    check_summary_sync, check_title_similarity,
    VALID_CATEGORIES, LOW_VALUE_KEYWORDS, COMPANY_ALIASES
)

# ========== 页面配置 ==========
st.set_page_config(
    page_title="AI Daily News - 审核工作台",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== 自定义 CSS ==========
st.markdown("""
<style>
/* 全局样式 */
.stApp { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }

/* 文章卡片 */
.article-card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 8px;
    background: #fafafa;
    transition: all 0.2s;
}
.article-card:hover { border-color: #ff6b6b; background: #fff5f5; }
.article-card.selected { border-color: #4CAF50; background: #e8f5e9; }
.article-card.problem { border-left: 4px solid #ff6b6b; }
.article-card.warning { border-left: 4px solid #ffa726; }

/* 问题标签 */
.tag-error { background: #ffebee; color: #c62828; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.tag-warning { background: #fff3e0; color: #ef6c00; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.tag-info { background: #e3f2fd; color: #1565c0; padding: 2px 8px; border-radius: 4px; font-size: 12px; }

/* 按钮优化 */
.stButton > button { height: 32px; font-size: 13px; }

/* 文本区域 */
.stTextArea textarea { font-size: 13px; line-height: 1.4; }
</style>
""", unsafe_allow_html=True)

# ========== 辅助函数 ==========

def load_articles(date_str):
    """加载指定日期的 MD 文件并解析"""
    md_path = PROJECT_ROOT / f"daily-ai-news-{date_str}.md"
    if not md_path.exists():
        return None, None, None
    
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    articles, summary_items = parse_md(md_content)
    return articles, summary_items, md_path


def run_qa_checks(articles, summary_items):
    """运行所有 QA 检查，返回问题列表"""
    all_issues = []
    
    # 1. 低价值检测
    issues = check_low_value(articles)
    for tag, title, detail in issues:
        all_issues.append({
            "type": tag,
            "title": title,
            "detail": detail,
            "severity": "error"
        })
    
    # 2. 分类检查
    issues = check_categories(articles)
    for tag, title, detail in issues:
        all_issues.append({
            "type": tag,
            "title": title,
            "detail": detail,
            "severity": "error"
        })
    
    # 3. 同公司去重
    issues = check_company_dup(articles)
    for tag, company, detail in issues:
        all_issues.append({
            "type": tag,
            "title": f"[{company}] 多条新闻",
            "detail": detail,
            "severity": "warning"
        })
    
    # 4. 过度推断
    issues = check_over_inference(articles)
    for tag, title, detail in issues:
        all_issues.append({
            "type": tag,
            "title": title,
            "detail": detail,
            "severity": "warning"
        })
    
    # 5. Body 质量
    issues = check_body_quality(articles)
    for tag, title, detail in issues:
        all_issues.append({
            "type": tag,
            "title": title,
            "detail": detail,
            "severity": "warning"
        })
    
    # 6. 来源检查
    issues = check_source(articles)
    for tag, title, detail in issues:
        all_issues.append({
            "type": tag,
            "title": title,
            "detail": detail,
            "severity": "error"
        })
    
    # 7. 要点速览同步
    issues = check_summary_sync(articles, summary_items)
    for tag, title, detail in issues:
        all_issues.append({
            "type": tag,
            "title": title,
            "detail": detail,
            "severity": "warning"
        })
    
    # 8. 标题相似度
    issues = check_title_similarity(articles)
    for tag, title, detail in issues:
        all_issues.append({
            "type": tag,
            "title": title,
            "detail": detail,
            "severity": "warning"
        })
    
    return all_issues


def get_article_problems(article, all_issues):
    """获取单篇文章的所有问题"""
    problems = []
    for issue in all_issues:
        if issue["title"] == article.get("title", ""):
            problems.append(issue)
    return problems


def generate_report_simple(articles, date_str):
    """简化版报告生成器（不依赖 feed_v5 全局变量）"""
    from collections import defaultdict
    
    # 分类
    VALID_CATEGORIES = ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]
    MAX_PER_CATEGORY = 8
    
    by_cat = defaultdict(list)
    for a in articles:
        for c in a.get("categories", ["未分类"]):
            if c in VALID_CATEGORIES:
                by_cat[c].append(a)
    
    # 分类内按优先级排序
    for cat in by_cat:
        by_cat[cat] = sorted(by_cat[cat], key=lambda x: x.get("priority", 0), reverse=True)[:MAX_PER_CATEGORY]
    
    # 生成 Markdown
    lines = [
        f"## {date_str} AI 前沿动态",
        "",
        f"> 自动汇总 | 条目数: {len(articles)}",
        "",
        "---",
        "",
        "## 要点汇总",
        ""
    ]
    
    for cat in VALID_CATEGORIES:
        items = by_cat.get(cat, [])
        if items:
            titles = "; ".join([a['title'] for a in items[:5]])
            lines.append(f"- {cat}：{titles}")
    
    lines.extend(["", "---", "", "## 📖 详细参考", ""])
    
    for cat in VALID_CATEGORIES:
        items = by_cat.get(cat, [])
        if not items:
            continue
        lines.append(f"### {cat}")
        for a in items:
            priority = a.get("priority", 0)
            priority_emoji = "🔥" if priority > 150 else "📰" if priority > 100 else "📄"
            
            title = a.get("title", "")
            body = a.get("body", "")
            link = a.get("link", "")
            key_points = a.get("key_points", [])
            
            lines.append(f"#### {priority_emoji} {title}")
            if link:
                lines.append(f"- 🔗 来源: [{link}]({link})")
            if key_points:
                lines.append("- 💡 要点:")
                for kp in key_points[:3]:
                    lines.append(f"  - {kp}")
            lines.append(f"- 📄 内容:\n  {body}")
            lines.append("")
    
    return "\n".join(lines)


def save_md(articles, md_path):
    """保存修改后的 MD 文件"""
    # 提取日期
    date_str = md_path.stem.replace("daily-ai-news-", "")
    
    # 生成报告
    try:
        report = generate_report_simple(articles, date_str)
    except Exception as e:
        st.error(f"❌ 生成报告失败: {e}")
        return False
    
    # 备份原文件
    if md_path.exists():
        backup_path = md_path.with_suffix('.md.bak')
        import shutil
        shutil.copy2(md_path, backup_path)
    
    # 保存新文件
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    st.success(f"✅ 已保存 {len(articles)} 条到 {md_path.name}")
    
    # 同时生成 HTML
    try:
        import subprocess
        result = subprocess.run(
            ['python', 'html_generator.py', md_path.name],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            st.success("✅ HTML 预览已更新")
        else:
            st.warning(f"⚠️ HTML 生成失败: {result.stderr[:200]}")
    except Exception as e:
        st.warning(f"⚠️ HTML 生成异常: {e}")
    
    return True


# ========== 主界面 ==========

def main():
    st.title("🤖 AI Daily News - 交互审核工作台")
    
    # 侧边栏：日期选择与统计
    with st.sidebar:
        st.header("📅 日期选择")
        
        # 默认今天
        default_date = datetime.now().strftime("%Y-%m-%d")
        date_str = st.text_input("日期 (YYYY-MM-DD)", value=default_date)
        
        st.divider()
        
        # 加载按钮
        if st.button("🔄 加载日报", type="primary", use_container_width=True):
            st.session_state.articles, st.session_state.summary_items, st.session_state.md_path = load_articles(date_str)
            if st.session_state.articles:
                st.session_state.all_issues = run_qa_checks(st.session_state.articles, st.session_state.summary_items)
                st.session_state.date_str = date_str
                st.success(f"✅ 已加载 {len(st.session_state.articles)} 条新闻")
            else:
                st.error(f"❌ 未找到文件: daily-ai-news-{date_str}.md")
        
        st.divider()
        
        # 统计面板
        if "articles" in st.session_state:
            total = len(st.session_state.articles)
            errors = len([i for i in st.session_state.all_issues if i["severity"] == "error"])
            warnings = len([i for i in st.session_state.all_issues if i["severity"] == "warning"])
            
            st.metric("总条目", total)
            st.metric("❌ 错误", errors, delta_color="inverse")
            st.metric("⚠️ 警告", warnings, delta_color="off")
            
            st.divider()
            st.subheader("快速筛选")
            filter_option = st.radio(
                "显示",
                ["全部", "仅有问题", "仅无问题", "已选中"],
                label_visibility="collapsed"
            )
            st.session_state.filter_option = filter_option
    
    # 主内容区
    if "articles" not in st.session_state:
        st.info("👈 请在侧边栏选择日期并点击【加载日报】")
        st.markdown("""
        ### 使用说明
        1. **加载**：选择日期，点击"加载日报"
        2. **审查**：左侧列表查看文章，右侧查看 QA 问题
        3. **操作**：
           - ✓ 接受：保留该条目
           - ✗ 拒绝：删除该条目
           - ✏️ 编辑：修改标题/正文/Insight
        4. **批量**：全选 → 批量接受/拒绝
        5. **保存**：点击"保存并生成 MD"
        """)
        st.stop()
    
    # 此时 articles 一定存在，安全访问
    articles = st.session_state.get("articles", [])
    all_issues = st.session_state.get("all_issues", [])
    md_path = st.session_state.get("md_path")
    
    # 根据筛选条件过滤
    filter_option = st.session_state.get("filter_option", "全部")
    filtered_indices = []
    for idx, a in enumerate(articles):
        problems = get_article_problems(a, all_issues)
        has_error = any(p["severity"] == "error" for p in problems)
        has_warning = any(p["severity"] == "warning" for p in problems)
        selected = idx in st.session_state.get("selected_articles", [])
        
        if filter_option == "全部":
            filtered_indices.append(idx)
        elif filter_option == "仅有问题" and (has_error or has_warning):
            filtered_indices.append(idx)
        elif filter_option == "仅无问题" and not problems:
            filtered_indices.append(idx)
        elif filter_option == "已选中" and selected:
            filtered_indices.append(idx)
    
    # 三栏布局
    col_list, col_detail, col_qa = st.columns([1.2, 1.5, 1])
    
    # === 左侧：文章列表 ===
    with col_list:
        st.subheader(f"📋 文章列表 ({len(filtered_indices)}/{len(articles)})")
        
        # 批量操作栏
        with st.container():
            col_a, col_b, col_c, col_d = st.columns(4)
            with col_a:
                if st.button("全选", use_container_width=True):
                    st.session_state.selected_articles = list(filtered_indices)
            with col_b:
                if st.button("接受选中", type="primary", use_container_width=True):
                    # 标记为接受（从待删除列表移除）
                    pass
            with col_c:
                if st.button("拒绝选中", use_container_width=True):
                    # 标记为拒绝
                    pass
            with col_d:
                if st.button("清空选择", use_container_width=True):
                    st.session_state.selected_articles = []
        
        st.divider()
        
        # 文章列表
        for idx in filtered_indices:
            a = articles[idx]
            problems = get_article_problems(a, all_issues)
            has_error = any(p["severity"] == "error" for p in problems)
            has_warning = any(p["severity"] == "warning" for p in problems)
            selected = idx in st.session_state.get("selected_articles", [])
            
            # 卡片样式
            card_class = "article-card"
            if has_error:
                card_class += " problem"
            elif has_warning:
                card_class += " warning"
            if selected:
                card_class += " selected"
            
            # 问题标记
            problem_badge = ""
            if has_error:
                problem_badge = '<span class="tag-error">❌ 错误</span>'
            elif has_warning:
                problem_badge = '<span class="tag-warning">⚠️ 警告</span>'
            
            # 分类标签颜色
            cat = a.get("categories", ["未分类"])[0]
            cat_colors = {
                "模型前沿": "#4CAF50",
                "产业动态": "#2196F3",
                "算力追踪": "#FF9800",
                "初创&融资": "#9C27B0",
                "研究关注": "#F44336",
                "X讨论": "#607D8B",
            }
            cat_color = cat_colors.get(cat, "#9E9E9E")
            
            with st.container():
                col_check, col_content = st.columns([0.5, 3.5])
                
                with col_check:
                    checked = st.checkbox(
                        "✓",
                        value=selected,
                        key=f"check_{idx}",
                        label_visibility="collapsed"
                    )
                    if checked:
                        if "selected_articles" not in st.session_state:
                            st.session_state.selected_articles = []
                        if idx not in st.session_state.selected_articles:
                            st.session_state.selected_articles.append(idx)
                    else:
                        if "selected_articles" not in st.session_state:
                            st.session_state.selected_articles = []
                        if idx in st.session_state.selected_articles:
                            st.session_state.selected_articles.remove(idx)
                
                with col_content:
                    # 标题 + 问题标记
                    title_html = f"""
                    <div class="{card_class}">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong>{a.get('title', '')[:60]}...</strong>
                            {problem_badge}
                        </div>
                        <div style="margin-top:4px;">
                            <span style="background:{cat_color}; color:white; padding:2px 6px; border-radius:3px; font-size:11px;">{cat}</span>
                            <span style="color:#666; font-size:11px; margin-left:8px;">优先级: {a.get('priority', 0)}</span>
                        </div>
                    </div>
                    """
                    st.markdown(title_html, unsafe_allow_html=True)
    
    # === 中间：详情编辑 ===
    with col_detail:
        st.subheader("📝 详情编辑")
        
        # 选择文章
        if filtered_indices:
            # 默认选中第一个有问题的
            default_idx = None
            for idx in filtered_indices:
                if get_article_problems(articles[idx], all_issues):
                    default_idx = idx
                    break
            if default_idx is None:
                default_idx = filtered_indices[0]
            
            selected_idx = st.selectbox(
                "选择文章",
                options=filtered_indices,
                format_func=lambda x: f"{articles[x].get('title', '')[:50]}...",
                index=filtered_indices.index(default_idx) if default_idx in filtered_indices else 0
            )
            
            a = articles[selected_idx]
            problems = get_article_problems(a, all_issues)
            
            # 编辑表单
            with st.form(key=f"edit_form_{selected_idx}"):
                new_title = st.text_input("标题", value=a.get("title", ""), key=f"title_{selected_idx}")
                new_body = st.text_area(
                    "正文 (Body)",
                    value=a.get("body", ""),
                    height=150,
                    key=f"body_{selected_idx}"
                )
                new_insight = st.text_area(
                    "Insight (要点)",
                    value="\n".join(a.get("key_points", [])),
                    height=100,
                    key=f"insight_{selected_idx}"
                )
                new_categories = st.multiselect(
                    "分类",
                    options=list(VALID_CATEGORIES),
                    default=a.get("categories", []),
                    key=f"cat_{selected_idx}"
                )
                new_link = st.text_input("来源链接", value=a.get("link", ""), key=f"link_{selected_idx}")
                
                col_save, col_discard = st.columns(2)
                with col_save:
                    if st.form_submit_button("💾 保存修改", use_container_width=True, type="primary"):
                        articles[selected_idx]["title"] = new_title
                        articles[selected_idx]["body"] = new_body
                        articles[selected_idx]["key_points"] = [p for p in new_insight.split("\n") if p.strip()]
                        articles[selected_idx]["categories"] = new_categories
                        articles[selected_idx]["link"] = new_link
                        st.success("✅ 已保存")
                        st.rerun()
                with col_discard:
                    if st.form_submit_button("↩️ 撤销", use_container_width=True):
                        st.rerun()
            
            # 快速操作按钮
            st.divider()
            col_accept, col_reject, col_skip = st.columns(3)
            with col_accept:
                if st.button("✓ 接受", use_container_width=True, type="primary"):
                    # 标记为已接受（从待处理列表移除）
                    if "accepted" not in st.session_state:
                        st.session_state.accepted = set()
                    st.session_state.accepted.add(selected_idx)
                    st.rerun()
            with col_reject:
                if st.button("✗ 拒绝", use_container_width=True):
                    # 标记为已拒绝
                    if "rejected" not in st.session_state:
                        st.session_state.rejected = set()
                    st.session_state.rejected.add(selected_idx)
                    st.rerun()
            with col_skip:
                if st.button("⏭️ 跳过", use_container_width=True):
                    pass
            
            # 显示当前状态
            status = ""
            if selected_idx in st.session_state.get("accepted", set()):
                status = "✅ 已接受"
            elif selected_idx in st.session_state.get("rejected", set()):
                status = "❌ 已拒绝"
            else:
                status = "⏳ 待处理"
            st.caption(f"状态: {status}")
    
    # === 右侧：QA 问题 ===
    with col_qa:
        st.subheader("🔍 QA 问题")
        
        if problems:
            for prob in problems:
                severity = prob["severity"]
                icon = "❌" if severity == "error" else "⚠️"
                css_class = "tag-error" if severity == "error" else "tag-warning"
                
                st.markdown(f"""
                <div style="margin-bottom:12px; padding:8px; border-left:3px solid {'#f44336' if severity=='error' else '#ff9800'}; background:#fafafa;">
                    <span class="{css_class}">{icon} {prob['type']}</span>
                    <div style="margin-top:4px; font-size:13px; color:#333;">
                        {prob['detail']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ 无质量问题")
    
    # === 底部：全局操作 ===
    st.divider()
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 2])
        
        with col1:
            if st.button("📥 导出 MD (保存修改)", use_container_width=True, type="primary"):
                # 应用接受/拒绝标记
                final_articles = []
                accepted = st.session_state.get("accepted", set())
                rejected = st.session_state.get("rejected", set())
                
                for idx, a in enumerate(articles):
                    if idx in rejected:
                        continue  # 跳过已拒绝
                    # 已接受的保留，未操作的也保留（默认接受）
                    final_articles.append(a)
                
                # 保存
                if save_md(final_articles, md_path):
                    st.success(f"✅ 已保存 {len(final_articles)} 条到 {md_path.name}")
                    
                    # 同时生成 HTML
                    try:
                        import subprocess
                        subprocess.run(
                            ['python', 'html_generator.py', md_path.name],
                            cwd=PROJECT_ROOT,
                            capture_output=True
                        )
                        st.success("✅ HTML 已生成")
                    except Exception as e:
                        st.warning(f"HTML 生成失败: {e}")
        
        with col2:
            if st.button("🚀 直接发布", use_container_width=True):
                # 调用 publish.py
                st.info("请运行: python publish.py --date {date_str}")
        
        with col3:
            if st.button("📊 QA 报告", use_container_width=True):
                st.session_state.show_qa_report = not st.session_state.get("show_qa_report", False)
        
        with col4:
            if st.button("🔄 重新加载", use_container_width=True):
                for key in ["articles", "all_issues", "selected_articles", "accepted", "rejected"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        
        with col5:
            # 导出统计
            if st.button("📈 统计", use_container_width=True):
                pass
    
    # QA 详细报告（可折叠）
    if st.session_state.get("show_qa_report", False):
        with st.expander("📋 QA 检查详细报告", expanded=True):
            # 按类型分组
            issues_by_type = {}
            for issue in all_issues:
                t = issue["type"]
                if t not in issues_by_type:
                    issues_by_type[t] = []
                issues_by_type[t].append(issue)
            
            for issue_type, issues in issues_by_type.items():
                st.markdown(f"**{issue_type}**: {len(issues)} 个")
                for issue in issues:
                    st.markdown(f"- {issue['title'][:50]}... → {issue['detail']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', type=str, default=None, help='日期 YYYY-MM-DD')
    args = parser.parse_args()
    
    # 如果命令行指定了日期，写入 session state
    if args.date:
        st.session_state.date_str = args.date
    
    main()
