#!/usr/bin/env python3
"""
交互式编辑新闻条目
用法: python edit_news.py [YYYY-MM-DD]
例如: python edit_news.py 2026-03-16
"""

import json
import os
import httpx
import re
import sys
from datetime import datetime, timedelta

ARCHIVE_DIR = "/Users/shenyalan/ai-daily-news/archive"
OUTPUT_DIR = "/Users/shenyalan/ai-daily-news"

def get_date(default_date=None):
    """获取日期，默认昨天"""
    if default_date:
        return default_date
    # 默认昨天
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")

def load_articles(date_str):
    """加载指定日期的文章"""
    archive_file = os.path.join(ARCHIVE_DIR, f"news_{date_str}.json")
    if not os.path.exists(archive_file):
        print(f"❌ 归档文件不存在: {archive_file}")
        return None

    with open(archive_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('articles', []), archive_file

def save_articles(articles, archive_file):
    """保存文章"""
    with open(archive_file, 'w', encoding='utf-8') as f:
        json.dump({
            "date": os.path.basename(archive_file).replace("news_", "").replace(".json", ""),
            "count": len(articles),
            "articles": articles
        }, f, ensure_ascii=False, indent=2)
    print(f"✅ 已保存")

def show_articles(articles, title="新闻列表"):
    """显示文章列表"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    if not articles:
        print("  (无)")
        return

    for i, a in enumerate(articles):
        cat = a.get('categories', ['?'])[0]
        title = a.get('title', '')[:40]
        print(f"  {i+1}. [{cat}] {title}")



# ========== LLM 处理 ==========
def call_llm_for_article(article):
    """用 LLM 处理单篇文章"""
    import httpx
    
    API_KEY = os.environ.get("MINIMAX_API_KEY", "")
    if not API_KEY:
        return None
    
    API_URL = "https://api.minimaxi.com/anthropic/v1/messages"
    
    title = article.get('title', '')
    summary = article.get('summary', '') or article.get('content', '')
    source = article.get('source', '')
    
    prompt = f"""处理下方新闻，输出JSON：

{{
    "title": "中文标题，事件主体+做什么+为什么重要",
    "body": "3-6句话，必须有so what（为什么重要），关键数据/判断加粗**",
    "insight": "一句话点评：趋势洞察、竞争分析、机会风险",
    "category": "分类"
}}

标题：{title}
来源：{source}
摘要：{summary[:500]}"""

    try:
        r = httpx.post(API_URL, headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }, json={
            "model": "MiniMax-M2.5",
            "temperature": 0.2,
            "max_tokens": 2000,
            "system": "你是一个顶尖AI新闻分析师。",
            "messages": [{"role": "user", "content": prompt}]
        }, timeout=60, verify=False)
        
        result = r.json()
        if result.get("content"):
            for item in result["content"]:
                if item.get("type") == "text":
                    import re
                    json_match = re.search(r'\{[\s\S]*\}', item.get("text", ""))
                    if json_match:
                        import json
                        return json.loads(json_match.group())
        return None
    except Exception as e:
        print(f"  ⚠️ LLM调用失败: {e}")
        return None

def add_article():
    """添加新文章"""
    print("\n--- 添加新文章 ---")
    title = input("  标题: ").strip()
    if not title:
        print("  ❌ 标题不能为空")
        return None

    summary = input("  摘要/正文: ").strip()
    source = input("  来源: ").strip()
    link = input("  链接 (可选): ").strip()
    
    # 询问是否需要 LLM 处理
    use_llm = input("  是否需要 LLM 处理? (y/n): ").strip().lower() == 'y'
    
    article = {
        "title": title,
        "summary": summary,
        "content": summary,
        "link": link,
        "source": source,
        "categories": ["产业动态"],  # 默认
        "body": summary,
        "insight": "",
        "priority": 100,
    }
    
    if use_llm:
        print("  🔄 调用 LLM 处理...")
        result = call_llm_for_article(article)
        if result:
            if result.get('title'):
                article['title'] = result['title']
            if result.get('body'):
                article['body'] = result['body']
            if result.get('insight'):
                article['insight'] = result['insight']
            if result.get('category'):
                article['categories'] = [result['category']]
            print("  ✅ LLM 处理完成")
        else:
            print("  ⚠️ LLM 处理失败，使用原始输入")
            # 让用户手动填写
            category = input("  分类 (模型前沿/产业动态/算力追踪/初创&融资/研究关注/X讨论): ").strip()
            if category:
                article['categories'] = [category]
    
    return article

def edit_article(article):
    """编辑单篇文章"""
    print("\n--- 编辑文章 ---")
    print(f"  原文标题: {article.get('title', '')}")

    new_title = input(f"  新标题 (回车保留): ").strip()
    if new_title:
        article['title'] = new_title

    print(f"  原文正文: {article.get('body', '')}")
    new_body = input(f"  新正文 (回车保留): ").strip()
    if new_body:
        article['body'] = new_body

    print(f"  原文来源: {article.get('source', '')}")
    new_source = input(f"  新来源 (回车保留): ").strip()
    if new_source:
        article['source'] = new_source

    print(f"  原文链接: {article.get('link', '')}")
    new_link = input(f"  新链接 (回车保留): ").strip()
    if new_link:
        article['link'] = new_link

    print(f"  原文分类: {article.get('categories', ['?'])[0]}")
    new_cat = input(f"  新分类 (回车保留): ").strip()
    if new_cat:
        article['categories'] = [new_cat]

    print(f"  原文点评: {article.get('insight', '')}")
    new_insight = input(f"  新点评 (回车保留): ").strip()
    if new_insight:
        article['insight'] = new_insight

    return article

def generate_md(articles, date_str):
    """生成 MD 文档"""
    lines = [f"# {date_str} AI 前沿动态", "", "---", ""]

    by_cat = {}
    for a in articles:
        cat = a.get('categories', ['其他'])[0]
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(a)

    for cat in ["模型前沿", "产业动态", "算力追踪", "初创&融资", "研究关注", "X讨论"]:
        items = by_cat.get(cat, [])
        if items:
            lines.append(f"## {cat}")
            for a in items:
                title = a.get('title', '')
                body = a.get('body', '')
                insight = a.get('insight', '')
                link = a.get('link', '')
                source = a.get('source', '')
                lines.append(f"### {title}")
                if body:
                    lines.append(body)
                if insight:
                    lines.append(f"> 💡 {insight}")
                if link:
                    lines.append(f"[来源: {source}]({link})")
                elif source:
                    lines.append(f"来源: {source}")
                lines.append("")

    output_file = os.path.join(OUTPUT_DIR, f"daily-ai-news-{date_str}.md")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"✅ 已生成: {output_file}")

def main():
    date_str = get_date(sys.argv[1] if len(sys.argv) > 1 else None)

    while True:
        result = load_articles(date_str)
        if result is None:
            return

        articles, archive_file = result
        show_articles(articles)

        print(f"\n{'='*50}")
        print("  操作: [a]添加 [d]删除 [e]编辑 [g]生成MD [q]退出")
        print(f"{'='*50}")

        choice = input("\n请选择操作: ").strip().lower()

        if choice == 'q':
            print("👋 再见!")
            break
        elif choice == 'a':
            new_article = add_article()
            if new_article:
                articles.append(new_article)
                save_articles(articles, archive_file)
        elif choice == 'd':
            try:
                idx = int(input("  输入要删除的编号: ")) - 1
                if 0 <= idx < len(articles):
                    removed = articles.pop(idx)
                    print(f"  ❌ 已删除: {removed.get('title', '')}")
                    save_articles(articles, archive_file)
                else:
                    print("  ❌ 编号无效")
            except ValueError:
                print("  ❌ 请输入数字")
        elif choice == 'e':
            try:
                idx = int(input("  输入要编辑的编号: ")) - 1
                if 0 <= idx < len(articles):
                    articles[idx] = edit_article(articles[idx])
                    save_articles(articles, archive_file)
                else:
                    print("  ❌ 编号无效")
            except ValueError:
                print("  ❌ 请输入数字")
        elif choice == 'g':
            generate_md(articles, date_str)
        else:
            print("  ❌ 无效选择")

if __name__ == "__main__":
    main()
