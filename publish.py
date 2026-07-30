#!/usr/bin/env python3
"""Safely publish a human-edited daily report.

This compatibility entry point preserves the manual editing workflow, but it
can no longer bypass the deterministic release gate.  It prepares canonical
JSON and HTML, writes a ``ready`` manifest, and delegates all external publish
side effects to ``run.sh``.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any

from html_generator import parse_md
from pipeline_core import atomic_write_json, ensure_candidate_ids
from pipeline_manifest import resolve_date
from qa import run_release_gate


BASE_DIR = Path(__file__).resolve().parent
ARCHIVE_DIR = BASE_DIR / "archive"
MANIFEST_DIR = ARCHIVE_DIR / "manifests"


def _canonical_manual_articles(md_content: str) -> tuple[list[dict], Any]:
    parsed, summary_items = parse_md(md_content)
    articles = []
    for rank, parsed_article in enumerate(parsed, 1):
        key_points = parsed_article.get("key_points") or []
        insight = " ".join(str(item) for item in key_points if item).strip()
        articles.append({
            "title": str(parsed_article.get("title", "") or "").strip(),
            "body": str(parsed_article.get("body", "") or "").strip(),
            "insight": insight,
            "categories": list(parsed_article.get("categories") or []),
            "source": str(parsed_article.get("source", "") or "").strip(),
            "link": str(parsed_article.get("link", "") or "").strip(),
            "priority": int(parsed_article.get("priority", 100) or 100),
            "provenance": {
                "selection": "human_manual",
                "writing": "human_edited",
                "status": "validated",
            },
            "_selection_status": "manual",
            "_editorial_rank": rank,
        })
    ensure_candidate_ids(articles)
    return articles, summary_items


def _archive_payload(articles: list[dict], report_date: str) -> dict:
    allowed = (
        "candidate_id",
        "title",
        "body",
        "insight",
        "categories",
        "source",
        "link",
        "priority",
        "provenance",
        "_selection_status",
        "_editorial_rank",
    )
    return {
        "date": report_date,
        "count": len(articles),
        "articles": [
            {key: article[key] for key in allowed if key in article}
            for article in articles
        ],
    }


def _content_hash(
    md_content: str,
    archive_payload: dict,
    html_path: Path,
) -> str:
    digest = hashlib.sha256()
    digest.update(md_content.encode("utf-8"))
    digest.update(
        json.dumps(
            archive_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    digest.update(html_path.read_bytes())
    return digest.hexdigest()


def _print_gate(label: str, gate) -> None:
    print(
        f"{label}: blocker={len(gate.blockers)}, "
        f"warning={len(gate.warnings)}"
    )
    for issue in gate.issues:
        marker = "❌" if issue.severity == "blocker" else "⚠️"
        print(f"  {marker} [{issue.code}] {issue.title}: {issue.detail}")


def prepare_manual_release(report_date: str) -> Path:
    md_path = BASE_DIR / f"daily-ai-news-{report_date}.md"
    html_path = BASE_DIR / f"daily-ai-news-{report_date}.html"
    archive_path = ARCHIVE_DIR / f"news_{report_date}.json"
    manifest_path = MANIFEST_DIR / f"{report_date}.json"

    if not md_path.is_file():
        raise FileNotFoundError(f"日报不存在: {md_path}")

    md_content = md_path.read_text(encoding="utf-8")
    articles, _ = _canonical_manual_articles(md_content)
    canonical_gate = run_release_gate(articles, strict=True)

    rendered_articles, _ = parse_md(md_content)
    rendered_gate = run_release_gate(rendered_articles, strict=False)
    _print_gate("canonical", canonical_gate)
    _print_gate("rendered-md", rendered_gate)
    qa_payload = {
        "canonical": canonical_gate.as_dict(),
        "rendered_md": rendered_gate.as_dict(),
    }

    if not canonical_gate.passed or not rendered_gate.passed:
        atomic_write_json(str(manifest_path), {
            "date": report_date,
            "status": "qa_failed",
            "manual_release": True,
            "failed_at": datetime.now(timezone.utc).isoformat(),
            "qa": qa_payload,
        })
        raise RuntimeError("人工编辑稿未通过发布硬门禁")

    run_id = (
        "manual-"
        + hashlib.sha256(
            (
                f"{report_date}|{datetime.now(timezone.utc).isoformat()}|"
                f"{os.getpid()}"
            ).encode("utf-8")
        ).hexdigest()[:16]
    )
    base_manifest = {
        "date": report_date,
        "run_id": run_id,
        "pipeline_version": "manual-release-v2",
        "prompt_hash": "human-edited",
        "manual_release": True,
        "qa": qa_payload,
    }
    atomic_write_json(str(manifest_path), {
        **base_manifest,
        "status": "running",
        "started_at": datetime.now(timezone.utc).isoformat(),
    })

    try:
        env = os.environ.copy()
        env["NEWS_DATE"] = report_date
        subprocess.run(
            [sys.executable, str(BASE_DIR / "html_generator.py")],
            cwd=BASE_DIR,
            env=env,
            check=True,
        )
        if not html_path.is_file() or html_path.stat().st_size == 0:
            raise RuntimeError(f"HTML 产物缺失或为空: {html_path}")

        archive_data = _archive_payload(articles, report_date)
        atomic_write_json(str(archive_path), archive_data)
        atomic_write_json(str(manifest_path), {
            **base_manifest,
            "status": "ready",
            "ready_at": datetime.now(timezone.utc).isoformat(),
            "content_hash": _content_hash(
                md_content, archive_data, html_path
            ),
            "article_count": len(articles),
            "artifacts": {
                "markdown": str(md_path),
                "archive": str(archive_path),
                "html": str(html_path),
            },
        })
    except Exception as exc:
        atomic_write_json(str(manifest_path), {
            **base_manifest,
            "status": "qa_failed",
            "failed_at": datetime.now(timezone.utc).isoformat(),
            "failure": {
                "type": type(exc).__name__,
                "detail": str(exc)[:1000],
            },
        })
        raise

    print(f"✅ 人工编辑稿已通过门禁，manifest=ready: {manifest_path}")
    return manifest_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report_date", nargs="?", help="YYYY-MM-DD")
    parser.add_argument("--date", dest="date_option", help="兼容旧用法")
    parser.add_argument(
        "--prepare-only",
        action="store_true",
        help="只生成 ready 产物，不截图、推送或通知",
    )
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    if (
        args.report_date
        and args.date_option
        and args.report_date != args.date_option
    ):
        print("❌ 位置日期与 --date 不一致", file=sys.stderr)
        return 64

    report_date = args.date_option or args.report_date
    if not report_date:
        report_date = resolve_date(
            os.environ.get("REPORT_TIMEZONE", "Asia/Shanghai"),
            int(os.environ.get("REPORT_CUTOFF_HOUR", "6")),
            int(os.environ.get("REPORT_CUTOFF_MINUTE", "40")),
        )
    try:
        parsed = datetime.strptime(report_date, "%Y-%m-%d")
        if parsed.strftime("%Y-%m-%d") != report_date:
            raise ValueError
    except ValueError:
        print("❌ 日期必须使用 YYYY-MM-DD", file=sys.stderr)
        return 64

    try:
        prepare_manual_release(report_date)
    except Exception as exc:
        print(f"❌ 人工发布准备失败: {exc}", file=sys.stderr)
        return 2

    if args.prepare_only:
        return 0

    result = subprocess.run(
        [str(BASE_DIR / "run.sh"), report_date],
        cwd=BASE_DIR,
        check=False,
    )
    if result.returncode != 0:
        print(
            f"❌ 发布阶段失败（退出码 {result.returncode}），"
            "ready 状态已保留，可安全重试",
            file=sys.stderr,
        )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
