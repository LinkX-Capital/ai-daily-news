#!/usr/bin/env python3
"""Batch convert all old-format HTML files to v2 format.

Parses old HTML to extract articles/summary, then re-renders with v2 template.
Handles prev/next navigation using the canonical file list from index.html.
"""

import os
import re
import sys
from html import unescape

# Import from v2 generator
from html_generator_v2 import generate_html, CAT_ORDER

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_old_html(html_path):
    """Parse old-format HTML file to extract articles and summary items."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract date from filename
    basename = os.path.basename(html_path)
    date_match = re.match(r'daily-ai-news-(\d{4}-\d{2}-\d{2}(?:\+\d{2})?)\.html', basename)
    file_date = date_match.group(1) if date_match else None

    # Extract display date from title (multiple formats)
    title_match = re.search(r'<title>(\d{2})月(\d{2})日', html)
    if title_match:
        month_day = f"{title_match.group(1)}月{title_match.group(2)}日"
    else:
        # Format: "AI前沿动态 2026.03.28-29"
        title_match2 = re.search(r'<title>[^<]*?(\d{4})\.(\d{2})\.(\d{2}(?:-\d{2})?)', html)
        if title_match2:
            month_day = f"{title_match2.group(2)}月{title_match2.group(3)}日"
        else:
            month_day = None

    # Parse summary items - build dict {category: [items]}
    summary_items = {}
    # Find summary-item blocks which have cat-tag + summary-title pairs
    summary_blocks = re.finditer(
        r'<span class="cat-tag">(.*?)</span>(.*?)(?=<div class="summary-item">|</div>\s*</div>\s*<div class="content">|$)',
        html, re.DOTALL
    )
    for m in summary_blocks:
        cat = unescape(m.group(1).strip())
        titles = re.findall(r'<span class="summary-title">(.*?)</span>', m.group(2), re.DOTALL)
        items = [unescape(t.strip()) for t in titles if t.strip()]
        if cat and items:
            summary_items[cat] = items

    # Parse articles grouped by section-title
    articles = []
    current_cat = ""

    # Split by section-title to get category groups
    parts = re.split(r'<div class="section-title">(.*?)</div>', html)

    for i, part in enumerate(parts):
        if i % 2 == 1:
            # This is a section title (category)
            current_cat = unescape(part.strip())
        elif i > 0 and current_cat:
            # Split by card divs
            card_splits = re.split(r'<div class="card">', part)

            for card_html in card_splits[1:]:  # skip first empty part
                article = parse_card(card_html, current_cat)
                if article:
                    articles.append(article)

    return articles, summary_items, file_date, month_day


def parse_card(card_html, category):
    """Parse a single card's HTML to extract article data."""
    # Title - try both class variants, tag-agnostic (span or div)
    title_match = re.search(r'<(?:span|div) class="card-title">(.*?)</(?:span|div)>', card_html, re.DOTALL)
    if not title_match:
        title_match = re.search(r'<(?:span|div) class="title">(.*?)</(?:span|div)>', card_html, re.DOTALL)
    if not title_match:
        return None
    title = unescape(title_match.group(1).strip())
    if not title:
        return None

    # Body - try both class variants
    body_match = re.search(r'<div class="card-body">(.*?)</div>', card_html, re.DOTALL)
    if not body_match:
        body_match = re.search(r'<div class="body">(.*?)</div>', card_html, re.DOTALL)
    body = unescape(body_match.group(1).strip()) if body_match else ""

    # Key points / insights - multiple formats
    key_points = []
    # Format 1: <li> items (older files)
    for m in re.finditer(r'<li>(.*?)</li>', card_html, re.DOTALL):
        point = unescape(m.group(1).strip())
        if point:
            key_points.append(point)
    # Format 2: <div class="insight">...</div>
    if not key_points:
        for m in re.finditer(r'<div class="insight">(.*?)</div>', card_html, re.DOTALL):
            point = unescape(m.group(1).strip())
            if point:
                key_points.append(point)
    # Format 3: <div class="card-insight">...</div>
    if not key_points:
        for m in re.finditer(r'<div class="card-insight">(.*?)</div>', card_html, re.DOTALL):
            point = unescape(m.group(1).strip())
            if point:
                key_points.append(point)

    # Sources - extract all links as (name, url) tuples
    sources = []
    src_matches = re.finditer(
        r'<a href="([^"]*)"[^>]*>(.*?)</a>', card_html, re.DOTALL
    )
    for m in src_matches:
        url = m.group(1)
        name = unescape(m.group(2).strip())
        sources.append((name, url))

    # Priority
    priority_match = re.search(r'class="priority (\w+)"', card_html)
    priority = priority_match.group(1) if priority_match else "medium"

    return {
        "title": title,
        "body": body,
        "key_points": key_points,
        "sources": sources,
        "source": sources[0][0] if sources else "",
        "link": sources[0][1] if sources else "",
        "categories": [category],
        "priority": priority,
    }


def get_canonical_file_list():
    """Get the canonical list of daily files from index.html."""
    index_path = os.path.join(BASE_DIR, "index.html")
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract dates from archive links
    dates = re.findall(
        r'href="daily-ai-news-(\d{4}-\d{2}-\d{2}(?:\+\d{2})?)\.html"', html
    )
    return dates  # ordered newest-first in index


def main():
    # Get canonical file list
    canonical = get_canonical_file_list()
    # Build lookup: date -> index in canonical list
    # canonical is newest-first, so prev = i+1, next = i-1
    date_index = {d: i for i, d in enumerate(canonical)}

    # Find all old-format HTML files
    old_files = []
    for f in sorted(os.listdir(BASE_DIR)):
        if not re.match(r'daily-ai-news-\d{4}-\d{2}-\d{2}', f):
            continue
        if not f.endswith('.html'):
            continue
        if '副本' in f:  # skip backup copies
            continue

        filepath = os.path.join(BASE_DIR, f)
        with open(filepath, 'r', encoding='utf-8') as fh:
            content = fh.read()
        if 'particle-bg' in content:
            continue  # already v2
        old_files.append(f)

    print(f"Found {len(old_files)} old-format files to convert")
    print(f"Canonical file list: {len(canonical)} entries\n")

    converted = 0
    errors = []

    for f in old_files:
        # Extract date from filename
        dm = re.match(r'daily-ai-news-(\d{4}-\d{2}-\d{2}(?:\+\d{2})?)\.html', f)
        if not dm:
            print(f"SKIP (bad filename): {f}")
            continue

        file_date = dm.group(1)
        filepath = os.path.join(BASE_DIR, f)

        # Find prev/next in canonical list
        idx = date_index.get(file_date)
        if idx is not None:
            prev_file = canonical[idx + 1] if idx + 1 < len(canonical) else None
            next_file = canonical[idx - 1] if idx > 0 else None
        else:
            print(f"WARN: {file_date} not in index.html, skipping prev/next")
            prev_file = None
            next_file = None

        # Parse old HTML
        try:
            articles, summary_items, parsed_date, month_day = parse_old_html(filepath)
        except Exception as e:
            errors.append(f"{f}: parse error: {e}")
            continue

        if not articles:
            errors.append(f"{f}: no articles parsed")
            continue

        # Determine if this is the latest file
        is_latest = (file_date == canonical[0]) if canonical else False

        # Generate v2 HTML
        try:
            v2_html = generate_html(
                articles, summary_items,
                month_day=month_day,
                is_latest=is_latest,
                file_date=file_date,
                prev_file=prev_file,
                next_file=next_file,
            )
        except Exception as e:
            errors.append(f"{f}: generate error: {e}")
            continue

        # Write back to same file
        with open(filepath, 'w', encoding='utf-8') as fh:
            fh.write(v2_html)

        print(f"OK: {f} ({len(articles)} articles, prev={prev_file}, next={next_file})")
        converted += 1

    print(f"\n=== Done: {converted} converted, {len(errors)} errors ===")
    for e in errors:
        print(f"  ERROR: {e}")


if __name__ == "__main__":
    main()
