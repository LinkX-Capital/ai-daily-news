#!/usr/bin/env python3
"""Validate and atomically advance the daily pipeline publication manifest."""

from __future__ import annotations

import argparse
from datetime import date, datetime, time, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


VALID_STATUSES = {"running", "ready", "qa_failed", "published"}


def _valid_date(value: str) -> str:
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc
    if parsed.isoformat() != value:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD")
    return value


def _valid_hour(value: str) -> int:
    parsed = int(value)
    if not 0 <= parsed <= 23:
        raise argparse.ArgumentTypeError("hour must be between 0 and 23")
    return parsed


def _valid_minute(value: str) -> int:
    parsed = int(value)
    if not 0 <= parsed <= 59:
        raise argparse.ArgumentTypeError("minute must be between 0 and 59")
    return parsed


def _read_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read a valid manifest at {path}") from exc
    if not isinstance(data, dict):
        raise ValueError("manifest root must be an object")
    return data


def _atomic_write(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
        text=True,
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def check(path: Path, report_date: str, expected_status: str) -> int:
    try:
        data = _read_manifest(path)
    except ValueError:
        return 1
    return int(
        data.get("date") != report_date
        or data.get("status") != expected_status
    )


def mark_running(path: Path, report_date: str) -> int:
    now = datetime.now(timezone.utc).isoformat()
    previous_status = None
    previous_run_id = None
    if path.exists():
        try:
            previous = _read_manifest(path)
            if previous.get("date") == report_date:
                previous_status = previous.get("status")
                previous_run_id = previous.get("run_id")
        except ValueError:
            pass

    data: dict[str, Any] = {
        "date": report_date,
        "status": "running",
        "started_at": now,
    }
    if previous_status:
        data["previous_status"] = previous_status
    if previous_run_id:
        data["previous_run_id"] = previous_run_id
    _atomic_write(path, data)
    return 0


def mark_published(path: Path, report_date: str) -> int:
    try:
        data = _read_manifest(path)
    except ValueError as exc:
        print(f"❌ {exc}", file=os.sys.stderr)
        return 1

    if data.get("date") != report_date:
        print("❌ manifest date does not match REPORT_DATE", file=os.sys.stderr)
        return 1

    current_status = data.get("status")
    if current_status == "published":
        return 0
    if current_status != "ready":
        print(
            f"❌ manifest must be ready before publishing (found {current_status!r})",
            file=os.sys.stderr,
        )
        return 1
    expected_hash = str(data.get("content_hash", "") or "").strip()
    try:
        actual_hash = _ready_content_hash(data)
    except ValueError as exc:
        print(f"❌ {exc}", file=os.sys.stderr)
        return 1
    if not expected_hash or actual_hash != expected_hash:
        print(
            "❌ ready artifacts changed after QA; refusing published",
            file=os.sys.stderr,
        )
        return 1

    # Preserve run_id, content_hash, QA details, and every future producer field.
    # Publication advances only the state and timestamp.
    data["status"] = "published"
    data["published_at"] = datetime.now(timezone.utc).isoformat()
    _atomic_write(path, data)
    return 0


def _ready_content_hash(data: dict[str, Any]) -> str:
    artifacts = data.get("artifacts")
    if not isinstance(artifacts, dict):
        raise ValueError("manifest artifacts are missing")

    try:
        markdown_path = Path(artifacts["markdown"])
        archive_path = Path(artifacts["archive"])
        html_path = Path(artifacts["html"])
    except (KeyError, TypeError) as exc:
        raise ValueError("manifest artifacts are incomplete") from exc

    try:
        markdown = markdown_path.read_text(encoding="utf-8")
        archive_data = json.loads(archive_path.read_text(encoding="utf-8"))
        html = html_path.read_bytes()
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("ready artifact is missing or invalid") from exc

    digest = hashlib.sha256()
    digest.update(markdown.encode("utf-8"))
    digest.update(
        json.dumps(
            archive_data,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    )
    digest.update(html)
    return digest.hexdigest()


def verify_ready(path: Path, report_date: str) -> int:
    try:
        data = _read_manifest(path)
        if data.get("date") != report_date or data.get("status") != "ready":
            return 1
        expected_hash = str(data.get("content_hash", "") or "").strip()
        if not expected_hash:
            return 1
        return int(_ready_content_hash(data) != expected_hash)
    except ValueError:
        return 1


def resolve_date(
    timezone_name: str,
    cutoff_hour: int,
    cutoff_minute: int,
    now_value: str | None = None,
) -> str:
    try:
        local_timezone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"unknown timezone: {timezone_name}") from exc

    if now_value:
        now = datetime.fromisoformat(now_value)
        if now.tzinfo is None:
            now = now.replace(tzinfo=local_timezone)
        else:
            now = now.astimezone(local_timezone)
    else:
        now = datetime.now(local_timezone)

    cutoff = time(cutoff_hour, cutoff_minute)
    report_date = now.date()
    if now.timetz().replace(tzinfo=None) < cutoff:
        report_date -= timedelta(days=1)
    return report_date.isoformat()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("--path", required=True, type=Path)
    check_parser.add_argument("--date", required=True, type=_valid_date)
    check_parser.add_argument("--status", required=True, choices=sorted(VALID_STATUSES))

    running_parser = subparsers.add_parser("mark-running")
    running_parser.add_argument("--path", required=True, type=Path)
    running_parser.add_argument("--date", required=True, type=_valid_date)

    published_parser = subparsers.add_parser("mark-published")
    published_parser.add_argument("--path", required=True, type=Path)
    published_parser.add_argument("--date", required=True, type=_valid_date)

    verify_parser = subparsers.add_parser(
        "verify-ready",
        help="verify that every ready artifact still matches content_hash",
    )
    verify_parser.add_argument("--path", required=True, type=Path)
    verify_parser.add_argument("--date", required=True, type=_valid_date)

    date_parser = subparsers.add_parser(
        "resolve-date",
        help="resolve the most recent report date whose cutoff has passed",
    )
    date_parser.add_argument("--timezone", default="Asia/Shanghai")
    date_parser.add_argument("--cutoff-hour", default=6, type=_valid_hour)
    date_parser.add_argument("--cutoff-minute", default=40, type=_valid_minute)
    date_parser.add_argument(
        "--now",
        help="optional ISO timestamp for deterministic tests",
    )

    return parser


def main() -> int:
    args = _build_parser().parse_args()
    if args.command == "check":
        return check(args.path, args.date, args.status)
    if args.command == "mark-running":
        return mark_running(args.path, args.date)
    if args.command == "mark-published":
        return mark_published(args.path, args.date)
    if args.command == "verify-ready":
        return verify_ready(args.path, args.date)
    if args.command == "resolve-date":
        try:
            print(
                resolve_date(
                    args.timezone,
                    args.cutoff_hour,
                    args.cutoff_minute,
                    args.now,
                )
            )
        except (ValueError, ZoneInfoNotFoundError) as exc:
            print(f"❌ {exc}", file=os.sys.stderr)
            return 1
        return 0
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
