#!/usr/bin/env python3
"""Extract frontier model entries from daily news markdown files"""

import re
from pathlib import Path
from datetime import datetime

def extract_frontier_entries(md_path):
    """Extract all frontier model entries from a markdown file"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = []

    # Find the 模型前沿 section
    frontier_pattern = r'## 模型前沿\s*\n(.*?)(?=\n## |\Z)'
    frontier_match = re.search(frontier_pattern, content, re.DOTALL)

    if not frontier_match:
        return entries

    frontier_section = frontier_match.group(1)

    # Extract individual entries (marked by **Title**)
    entry_pattern = r'\*\*(.*?)\*\*\s*\n(.*?)(?=\n\*\*|\Z)'

    for match in re.finditer(entry_pattern, frontier_section, re.DOTALL):
        title = match.group(1).strip()
        body_text = match.group(2).strip()

        # Extract body (up to insight/key_points or source)
        body_match = re.search(r'^(.*?)(?:\n\n(?:关键影响|来源):|$)', body_text, re.DOTALL)
        body = body_match.group(1).strip() if body_match else body_text

        # Extract insights/key_points
        insights = []
        insights_match = re.search(r'关键影响：\s*\n(.*?)(?:\n\n来源:|$)', body_text, re.DOTALL)
        if insights_match:
            insight_text = insights_match.group(1).strip()
            # Split by bullet points or numbered lists
            insight_items = re.findall(r'[-•]\s*(.*?)(?=\n[-•]|\Z)', insight_text, re.DOTALL)
            insights = [item.strip() for item in insight_items]

        # Extract source
        source_match = re.search(r'来源：\s*\[(.*?)\]\((.*?)\)', body_text)
        source_title = source_match.group(1) if source_match else ""
        source_url = source_match.group(2) if source_match else ""

        entries.append({
            'title': title,
            'body': body,
            'insights': insights,
            'source_title': source_title,
            'source_url': source_url
        })

    return entries

def main():
    start_date = datetime(2026, 6, 16)
    end_date = datetime(2026, 6, 28)

    news_dir = Path('/Users/shenyalan/ai-daily-news')

    all_entries = []

    # Iterate through date range
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        md_file = news_dir / f'daily-ai-news-{date_str}.md'

        if md_file.exists():
            print(f"\n{'='*80}")
            print(f"📅 {date_str}")
            print('='*80)

            entries = extract_frontier_entries(md_file)

            if entries:
                for entry in entries:
                    print(f"\n**{entry['title']}**")
                    print(f"\n{entry['body'][:200]}..." if len(entry['body']) > 200 else f"\n{entry['body']}")
                    if entry['insights']:
                        print(f"\n关键影响: {len(entry['insights'])} 条")
                    print(f"\n来源: {entry['source_title']}")

                all_entries.extend([{'date': date_str, **entry} for entry in entries])
            else:
                print("(无模型前沿条目)")

        current_date = current_date.replace(day=current_date.day + 1)

    print(f"\n\n{'='*80}")
    print(f"总计: {len(all_entries)} 条模型前沿条目")
    print('='*80)

if __name__ == '__main__':
    main()
