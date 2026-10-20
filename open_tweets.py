#!/usr/bin/env python3
"""一键打开 Twitter 预览里的推文链接（桌面快捷方式调用）

用法:
  python open_tweets.py              # 最新一期
  python open_tweets.py 2026-10-20   # 指定日期

可选：今日重点 / 公司发布 / 研究者动态 / 全部。
链接多时每批打开 BATCH_SIZE 个，按回车再开下一批，避免浏览器一次弹出几十个标签卡死。
"""

from __future__ import annotations

import json
import re
import sys
import time
import webbrowser
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BATCH_SIZE = 10

_SECTION_RE = re.compile(r"^##\s+(.*)$")
_LINK_RE = re.compile(r"\[查看\]\((https?://[^)\s]+)\)")


def latest_preview_date(base_dir: Path = BASE_DIR) -> str | None:
    dates = sorted(
        m.group(1)
        for p in base_dir.glob("twitter-preview-*.md")
        if (m := re.fullmatch(r"twitter-preview-(\d{4}-\d{2}-\d{2})\.md", p.name))
    )
    return dates[-1] if dates else None


def parse_preview_links(text: str) -> dict[str, list[str]]:
    """{section heading: [tweet links]} from a twitter-preview markdown file."""
    sections: dict[str, list[str]] = {}
    current = None
    for line in text.splitlines():
        heading = _SECTION_RE.match(line)
        if heading:
            current = heading.group(1).strip()
            continue
        if current is None:
            continue
        for link in _LINK_RE.findall(line):
            sections.setdefault(current, []).append(link)
    return sections


def highlight_links(date: str, base_dir: Path = BASE_DIR) -> list[tuple[str, str]]:
    """[(title, link)] from cache/twitter_highlights_<date>.json (highlights carry links there)."""
    path = base_dir / "cache" / f"twitter_highlights_{date}.json"
    try:
        records = json.loads(path.read_text(encoding="utf-8")).get("highlights", [])
    except (OSError, ValueError):
        return []
    return [(r.get("title", ""), r["link"]) for r in records if r.get("link")]


def _dedupe(links: list[str]) -> list[str]:
    seen: set[str] = set()
    return [link for link in links if not (link in seen or seen.add(link))]


def build_menu(date: str, base_dir: Path = BASE_DIR) -> list[tuple[str, list[str]]]:
    """[(label, links)] menu entries, empty ones dropped."""
    preview = base_dir / f"twitter-preview-{date}.md"
    sections = parse_preview_links(preview.read_text(encoding="utf-8")) if preview.exists() else {}

    menu: list[tuple[str, list[str]]] = []
    highlights = [link for _, link in highlight_links(date, base_dir)]
    if highlights:
        menu.append(("⭐ 今日重点", _dedupe(highlights)))
    for heading, links in sections.items():
        menu.append((re.sub(r"[（(]\d+条[）)]", "", heading).strip(), _dedupe(links)))
    everything = _dedupe([link for _, links in sections.items() for link in links])
    if len(sections) > 1 and everything:
        menu.append(("📚 全部推文", everything))
    return [(label, links) for label, links in menu if links]


def open_links(links: list[str], batch_size: int = BATCH_SIZE) -> None:
    for start in range(0, len(links), batch_size):
        batch = links[start : start + batch_size]
        for link in batch:
            webbrowser.open_new_tab(link)
            time.sleep(0.3)  # 连续打开太快，部分浏览器会丢标签
        opened = start + len(batch)
        if opened < len(links):
            answer = input(f"已打开 {opened}/{len(links)}，回车继续下一批，输入 q 停止：").strip().lower()
            if answer == "q":
                return
    print(f"✅ 已打开 {len(links)} 个链接")


def main() -> int:
    date = sys.argv[1] if len(sys.argv) > 1 else latest_preview_date()
    if not date:
        print("❌ 没有找到 Twitter 预览文件（twitter-preview-*.md）")
        input("按回车键关闭...")
        return 1

    menu = build_menu(date)
    print(f"🐦 {date} Twitter 预览\n")
    if not menu:
        print("❌ 这一期没有可打开的推文链接")
        input("按回车键关闭...")
        return 1

    for index, (label, links) in enumerate(menu, 1):
        print(f"  [{index}] {label}（{len(links)} 条）")
    print("  [q] 退出\n")

    choice = input("选择要打开的内容，直接回车 = [1]：").strip().lower() or "1"
    if choice == "q":
        return 0
    if not choice.isdigit() or not 1 <= int(choice) <= len(menu):
        print("❌ 无效选择")
        input("按回车键关闭...")
        return 1

    label, links = menu[int(choice) - 1]
    print(f"\n正在打开「{label}」{len(links)} 个链接...")
    open_links(links)
    time.sleep(1)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
