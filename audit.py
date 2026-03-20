#!/usr/bin/env python3
"""日报审核工具 - 统一处理增删改"""

import json
import os
import sys

ARCHIVE_DIR = "/Users/shenyalan/ai-daily-news/archive"

def get_latest_archive():
    files = sorted(os.listdir(ARCHIVE_DIR))
    if not files:
        print("❌ 没有找到存档文件")
        sys.exit(1)
    return os.path.join(ARCHIVE_DIR, files[-1])

def load_archive(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_archive(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def show_current_articles(data):
    """显示当前所有文章"""
    print("\n📰 当前日报内容:")
    print("=" * 60)
    for i, a in enumerate(data['articles'], 1):
        cats = a.get('categories', ['未分类'])
        print(f"{i}. [{cats[0]}] {a.get('title', '')[:50]}")
    print("=" * 60)

def show_twitter_preview():
    """显示 Twitter 预览"""
    preview_file = "/Users/shenyalan/ai-daily-news/twitter_preview.md"
    if not os.path.exists(preview_file):
        print("⚠️ twitter_preview.md 不存在，跳过")
        return []

    with open(preview_file, 'r', encoding='utf-8') as f:
        content = f.read()

    import re
    items = []
    blocks = content.split('## ')
    for block in blocks[1:]:
        lines = block.strip().split('\n')
        if not lines:
            continue
        first_line = lines[0]
        match = re.match(r'(\d+)\.\s*(@\w+)', first_line)
        if match:
            source = match.group(2)
            title = ""
            for line in lines[1:]:
                if line.strip() and not line.startswith('-'):
                    title = line.strip()
                    break
            url = ""
            for line in lines:
                if '链接:' in line:
                    url = line.split('链接:')[1].strip()
            items.append({'source': source, 'title': title, 'url': url})
    return items

def delete_article(data):
    """删除文章"""
    show_current_articles(data)
    try:
        idx = int(input("\n🗑️  输入要删除的编号 (0取消): "))
        if idx == 0:
            return data
        if idx < 1 or idx > len(data['articles']):
            print("❌ 无效编号")
            return data

        removed = data['articles'].pop(idx - 1)
        print(f"✅ 已删除: {removed.get('title', '')[:40]}...")
    except ValueError:
        print("❌ 请输入数字")
    return data

def add_from_twitter(data, twitter_items):
    """从 Twitter 预览添加"""
    if not twitter_items:
        print("⚠️ 没有 Twitter 预览")
        return data

    print("\n🐦 Twitter 预览 (可添加):")
    print("-" * 40)
    for i, item in enumerate(twitter_items, 1):
        print(f"{i}. [{item['source']}] {item['title'][:50]}...")
    print("-" * 40)

    try:
        idx = input("\n📝 输入要添加的编号 (逗号分隔多个，0取消): ").strip()
        if idx == "0" or idx == "":
            return data

        for i in idx.split(','):
            i = int(i.strip())
            if i < 1 or i > len(twitter_items):
                continue
            item = twitter_items[i-1]

            body = input(f"\n📝 body (回车用默认): ").strip() or f"{item['title']}"
            insight = input("💡 insight (回车跳过): ").strip()
            category = input("📂 分类 [产业动态]: ").strip() or "产业动态"

            data['articles'].append({
                "title": item['title'],
                "body": body,
                "categories": [category],
                "source": item['source'],
                "url": item['url'],
                "link": item['url'],
                "insight": insight,
                "priority": 100
            })
            print(f"✅ 已添加: {item['title'][:30]}...")
    except ValueError:
        print("❌ 输入错误")
    return data

def add_manual(data):
    """手动添加"""
    print("\n📝 手动添加新闻:")
    title = input("  标题: ").strip()
    body = input("  body: ").strip()
    category = input("  分类 [产业动态]: ").strip() or "产业动态"
    source = input("  来源: ").strip()
    url = input("  链接: ").strip()
    insight = input("  insight: ").strip()

    data['articles'].append({
        "title": title,
        "body": body,
        "categories": [category],
        "source": source,
        "url": url,
        "link": url,
        "insight": insight,
        "priority": 100
    })
    print(f"✅ 已添加: {title[:30]}...")
    return data

def rebuild():
    """重新生成"""
    import subprocess
    print("\n🔄 重新生成 HTML...")
    subprocess.run(['python3', 'generate_html.py'], check=True)
    print("📸 生成截图...")
    subprocess.run(['python3', 'gen_screenshot.py'], check=True)
    print("📨 推送飞书...")
    subprocess.run(['python3', 'notify.py'], check=True)
    print("✅ 全部完成!")

def main():
    print("""
📋 日报审核工具
================
1. 查看当前日报
2. 删除文章
3. 从 Twitter 添加
4. 手动添加
5. 增删完成后生成推送 (1234可重复操作)
0. 退出
""")

    archive_path = get_latest_archive()
    data = load_archive(archive_path)
    twitter_items = show_twitter_preview()

    while True:
        choice = input("\n👉 选择操作 [0-5]: ").strip()

        if choice == "0":
            print("👋 退出")
            break
        elif choice == "1":
            show_current_articles(data)
        elif choice == "2":
            data = delete_article(data)
            save_archive(data, archive_path)
        elif choice == "3":
            data = add_from_twitter(data, twitter_items)
            save_archive(data, archive_path)
        elif choice == "4":
            data = add_manual(data)
            save_archive(data, archive_path)
        elif choice == "5":
            rebuild()
            break
        else:
            print("❌ 无效选择")

if __name__ == "__main__":
    main()
