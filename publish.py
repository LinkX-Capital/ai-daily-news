#!/usr/bin/env python3
"""
发布脚本：从 md 文档生成 JSON、HTML、飞书通知

工作流：
1. feed_v5.py --cache  (抓取内容到 md)
2. 手动编辑 daily-ai-news.md
3. python publish.py  (发布：md → JSON → HTML → 飞书 → GitHub)
"""

import json
import re
import os
from datetime import datetime

# 配置
MD_FILE = f"/Users/shenyalan/ai-daily-news/daily-ai-news-{datetime.now().strftime('%Y-%m-%d')}.md"
ARCHIVE_DIR = "/Users/shenyalan/ai-daily-news/archive"
ARCHIVE_FILE = None  # 自动从日期提取


def parse_md_to_articles(md_content):
    """从 md 文档解析文章"""
    articles = []

    # 提取日期
    date_match = re.search(r'(\d{2})月(\d{2})日', md_content)
    if date_match:
        month, day = date_match.groups()
        date_str = f"2026-{month.zfill(2)}-{day.zfill(2)}"
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    # 直接查找所有 **标题** 块
    pattern = r'\*\*([^\*]+?)\*\*\s*\n(.*?)(?=\n\*\*|\n###|$)'
    matches = list(re.finditer(pattern, md_content, re.DOTALL))

    # 确定每个文章所属分类
    cat_positions = []
    for cat in ["产业动态", "初创&融资", "研究关注", "X讨论", "模型前沿", "算力追踪"]:
        pos = md_content.find(f"### {cat}")
        if pos >= 0:
            cat_positions.append((pos, cat))
    cat_positions.sort()

    for match in matches:
        title = match.group(1).strip()
        body_content = match.group(2).strip()

        # 确定分类
        article_pos = match.start()
        current_cat = "其他"
        for pos, cat in cat_positions:
            if article_pos >= pos:
                current_cat = cat

        # 解析正文、insight、来源
        body_lines = []
        insight = ""
        source = ""
        link = ""

        lines = body_content.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('> 💡'):
                insight = line.replace('> 💡', '').strip()
            elif line.startswith('- 来源:'):
                source_line = line.replace('- 来源:', '').strip()
                link_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', source_line)
                if link_match:
                    source = link_match.group(1)
                    link = link_match.group(2)
                else:
                    source = source_line
            elif line.startswith('- ') and not line.startswith('- 来源'):
                body_text = line[2:].strip()
                if body_text:
                    body_lines.append(body_text)

        body = ' '.join(body_lines) if body_lines else ""
        insight = insight.replace('💡', '').strip()

        # 优先级
        if current_cat == "X讨论":
            priority = 90
        elif current_cat == "研究关注":
            priority = 140
        elif current_cat == "初创&融资":
            priority = 110
        else:
            priority = 120

        articles.append({
            'title': title,
            'body': body,
            'insight': insight,
            'categories': [current_cat],
            'source': f"- {source}" if source else "",
            'link': link,
            'priority': priority
        })

    return articles, date_str


def save_archive(articles, date_str):
    """保存到 JSON 存档"""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    archive_file = os.path.join(ARCHIVE_DIR, f"news_{date_str}.json")

    output = {
        "date": date_str,
        "count": len(articles),
        "articles": articles,
        "archived_at": datetime.now().isoformat()
    }

    with open(archive_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ 已保存存档: {archive_file}")
    return archive_file


def generate_html(date_str):
    """调用 html_generator.py"""
    import subprocess
    result = subprocess.run(
        ['python', '/Users/shenyalan/ai-daily-news/html_generator.py'],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"⚠️ HTML生成警告: {result.stderr}")


def send_feishu():
    """调用 notify.py"""
    import subprocess
    result = subprocess.run(
        ['python', '/Users/shenyalan/ai-daily-news/notify.py'],
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"⚠️ 飞书通知警告: {result.stderr}")


def git_push(date_str):
    """只推送 3 个 HTML 文件到 GitHub"""
    import subprocess

    html_files = [
        f"daily-ai-news-{date_str}.html",
        "daily-ai-news.html",
        "index.html"
    ]

    try:
        # 切换到项目目录
        os.chdir('/Users/shenyalan/ai-daily-news')

        # 添加文件
        for f in html_files:
            subprocess.run(['git', 'add', f], check=True, capture_output=True)
            print(f"   git add {f}")

        # 提交
        commit_msg = f"Update: {date_str}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
        print(f"   git commit -m '{commit_msg}'")

        # 推送 (首次设置 upstream)
        result = subprocess.run(['git', 'push', '--set-upstream', 'origin', 'main'], capture_output=True)
        if result.returncode != 0:
            # 可能已经设置过，重试普通 push
            result = subprocess.run(['git', 'push'], capture_output=True)
        if result.returncode == 0:
            print(f"   git push")
        else:
            print(f"   git push stderr: {result.stderr.decode()}")
            raise subprocess.CalledProcessError(result.returncode, 'git push')

        print("✅ Git push 成功")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git 失败: {e}")
    except Exception as e:
        print(f"⚠️ Git 错误: {e}")


def main():
    print("📝 从 md 发布")
    print("=" * 50)

    # 检查 md 文件是否有未提交的更改
    import subprocess
    result = subprocess.run(
        ['git', 'diff', '--name-only', MD_FILE],
        capture_output=True, text=True,
        cwd='/Users/shenyalan/ai-daily-news'
    )
    if result.stdout.strip():
        print(f"⚠️ 警告: {MD_FILE} 有未提交的更改:")
        print(result.stdout.strip())
        response = input("继续发布将覆盖这些更改，是否继续？(y/N): ")
        if response.lower() != 'y':
            print("已取消发布")
            return

    # 读取 md 文件
    if not os.path.exists(MD_FILE):
        print(f"❌ 文件不存在: {MD_FILE}")
        return

    with open(MD_FILE, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 解析文章
    articles, date_str = parse_md_to_articles(md_content)

    if not articles:
        print("❌ 未找到文章")
        return

    print(f"📄 解析到 {len(articles)} 篇文章")
    by_cat = {}
    for a in articles:
        cat = a['categories'][0]
        by_cat[cat] = by_cat.get(cat, 0) + 1

    print(f"   分类: {', '.join(f'{k}:{v}' for k, v in sorted(by_cat.items()))}")

    # 信息补充
    print("\n🔍 运行信息补充...")
    enrich_result = subprocess.run(
        ['python3', os.path.join(os.path.dirname(__file__), 'enrich.py'), date_str],
        capture_output=True, text=True,
        cwd='/Users/shenyalan/ai-daily-news'
    )
    print(enrich_result.stdout)

    # QA 检查
    print("\n🔍 运行 QA 检查...")
    qa_result = subprocess.run(
        ['python3', os.path.join(os.path.dirname(__file__), 'qa.py'), date_str],
        capture_output=True, text=True,
        cwd='/Users/shenyalan/ai-daily-news'
    )
    print(qa_result.stdout)
    if qa_result.returncode != 0:
        print(f"⚠️ QA 发现问题（详见上方），但仍继续发布。如需修复请 Ctrl+C 中断。")

    # 保存存档
    save_archive(articles, date_str)

    # 生成 HTML
    print("\n🌐 生成 HTML...")
    generate_html(date_str)

    # 发送飞书
    print("\n📤 发送飞书通知...")
    send_feishu()

    # Git push
    print("\n🔄 Git push...")
    git_push(date_str)

    # 生成手机端截图
    print("\n📸 生成手机端截图...")
    import subprocess
    result = subprocess.run(
        ['python3', '/Users/shenyalan/ai-daily-news/gen_screenshot.py'],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"⚠️ 截图生成警告: {result.stderr}")

    print("\n✅ 发布完成!")


if __name__ == "__main__":
    main()
