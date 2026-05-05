#!/usr/bin/env python3
"""
验证 review_dashboard.py 的依赖和基本功能
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

print("🔍 检查依赖...")

# 1. Streamlit
try:
    import streamlit as st
    print(f"✅ Streamlit: {st.__version__}")
except ImportError:
    print("❌ Streamlit 未安装")
    print("   请运行: pip install streamlit")
    sys.exit(1)

# 2. 项目模块
print("\n🔍 检查项目模块...")
try:
    from html_generator import parse_md
    print("✅ html_generator.parse_md")
except Exception as e:
    print(f"❌ html_generator: {e}")

try:
    from qa import (
        check_low_value, check_categories, check_company_dup,
        check_over_inference, check_body_quality, check_source,
        check_summary_sync, check_title_similarity
    )
    print("✅ qa 模块 (8个检查函数)")
except Exception as e:
    print(f"❌ qa: {e}")

try:
    from feed_v5 import generate_report
    print("✅ feed_v5.generate_report (用于保存)")
except Exception as e:
    print(f"⚠️  feed_v5.generate_report: {e}")
    print("   将使用内置简化版本")

# 3. 测试核心函数
print("\n🔍 测试核心函数...")

# 测试文章数据
test_articles = [
    {
        "title": "测试：GPT-5 即将发布",
        "body": "OpenAI 宣布下一代模型 GPT-5 将在下月发布，具备更强的推理能力。",
        "key_points": ["GPT-5 下月发布", "推理能力提升"],
        "categories": ["模型前沿"],
        "priority": 150,
        "link": "https://example.com/gpt5"
    },
    {
        "title": "AI 初创公司融资 1 亿美元",
        "body": "一家专注于 AI 安全的初创公司今天宣布完成 1 亿美元融资。",
        "key_points": ["融资 1 亿美元", "AI 安全领域"],
        "categories": ["初创&融资"],
        "priority": 120,
        "link": "https://example.com/funding"
    }
]

# 测试 QA 检查
try:
    from qa import check_low_value, check_source, check_categories
    
    issues = check_low_value(test_articles)
    print(f"✅ 低价值检查: {len(issues)} 个问题")
    
    issues = check_source(test_articles)
    print(f"✅ 来源检查: {len(issues)} 个问题")
    
    issues = check_categories(test_articles)
    print(f"✅ 分类检查: {len(issues)} 个问题")
    
except Exception as e:
    print(f"❌ QA 检查失败: {e}")

# 测试报告生成
try:
    from review_dashboard import generate_report_simple
    report = generate_report_simple(test_articles, "2026-04-28")
    lines = report.split('\n')
    print(f"✅ 报告生成: {len(lines)} 行")
    print(f"   预览: {lines[0]}")
except Exception as e:
    print(f"❌ 报告生成失败: {e}")

# 4. 检查 MD 文件
print("\n🔍 检查现有 MD 文件...")
md_files = list(PROJECT_ROOT.glob("daily-ai-news-*.md"))
if md_files:
    print(f"✅ 找到 {len(md_files)} 个 MD 文件")
    latest = max(md_files, key=lambda p: p.stat().st_mtime)
    print(f"   最新: {latest.name}")
else:
    print("⚠️  未找到 MD 文件")
    print("   请先运行: python feed_v5.py")

print("\n" + "="*50)
print("✅ 验证完成！")
print("\n🚀 启动命令:")
print("   streamlit run review_dashboard.py")
print("\n📱 访问: http://localhost:8501")
print("="*50)
