#!/usr/bin/env python3
"""检查三天的X讨论内容"""

import json

for date in ['2026-03-14', '2026-03-15', '2026-03-16']:
    with open(f'archive/news_{date}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"\n=== {date} ===")
    x_count = 0
    for a in data['articles']:
        if 'X讨论' in a.get('categories', []):
            x_count += 1
            print(f"  - {a['title']}")
    if x_count == 0:
        print("  (无)")
