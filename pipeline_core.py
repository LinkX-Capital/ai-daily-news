#!/usr/bin/env python3
"""Pure, deterministic helpers for the daily-news pipeline.

This module deliberately contains no network or model calls.  Keeping IDs,
model-response parsing and atomic writes here makes the failure paths testable
without importing the large feed runner.
"""

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


TRACKING_QUERY_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "source",
}


def canonicalize_url(url: str) -> str:
    """Return a stable URL suitable for identity and exact deduplication."""
    url = (url or "").strip()
    if not url:
        return ""
    try:
        parts = urlsplit(url)
        query = [
            (key, value)
            for key, value in parse_qsl(parts.query, keep_blank_values=True)
            if not key.lower().startswith("utm_") and key.lower() not in TRACKING_QUERY_KEYS
        ]
        path = re.sub(r"/+$", "", parts.path) or "/"
        return urlunsplit(
            (
                parts.scheme.lower(),
                parts.netloc.lower(),
                path,
                urlencode(query, doseq=True),
                "",
            )
        )
    except Exception:
        return url.split("#", 1)[0].rstrip("/")


def make_candidate_id(article: Dict[str, Any]) -> str:
    """Build a stable ID from source-native identity, URL, or raw title."""
    source = str(article.get("source") or "").strip().lower()
    native_id = str(
        article.get("source_item_id")
        or article.get("guid")
        or article.get("tweet_id")
        or ""
    ).strip()
    link = canonicalize_url(str(article.get("link") or ""))
    raw_title = str(article.get("raw_title") or article.get("title") or "")
    normalized_title = re.sub(r"\s+", " ", raw_title).strip().lower()
    identity = native_id or link or normalized_title
    digest = hashlib.sha256(f"{source}\n{identity}".encode("utf-8")).hexdigest()
    return f"cand_{digest[:20]}"


def ensure_candidate_ids(articles: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Populate stable IDs and immutable raw fields in-place."""
    result = []
    for article in articles:
        if not article.get("raw_title"):
            article["raw_title"] = article.get("title", "")
        if not article.get("raw_summary"):
            article["raw_summary"] = article.get("summary", "")
        article["link"] = canonicalize_url(str(article.get("link") or ""))
        article["candidate_id"] = article.get("candidate_id") or make_candidate_id(article)
        result.append(article)
    return result


def _strip_code_fence(text: str) -> str:
    text = (text or "").strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _decode_first_array(text: str) -> Optional[List[Any]]:
    decoder = json.JSONDecoder()
    for index, char in enumerate(text):
        if char != "[":
            continue
        try:
            value, _ = decoder.raw_decode(text[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(value, list):
            return value
    return None


def parse_llm_array(raw: str) -> List[Dict[str, Any]]:
    """Parse a model JSON array without rewriting valid escape sequences."""
    text = _strip_code_fence(raw)
    attempts = [text]
    limited_fix = re.sub(r",(\s*[\]}])", r"\1", text)
    if limited_fix != text:
        attempts.append(limited_fix)
    # MiniMax-M3 intermittently drops the closing bracket while still
    # reporting stop_reason=end_turn; repair such truncated arrays.
    if text.startswith("[") and not text.rstrip().endswith("]"):
        attempts.append(text.rstrip().rstrip(",") + "]")
        bracket_fix = re.sub(r",(\s*[\]}])", r"\1", attempts[-1])
        if bracket_fix != attempts[-1]:
            attempts.append(bracket_fix)

    for candidate in attempts:
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError:
            value = _decode_first_array(candidate)
        if isinstance(value, list) and all(isinstance(item, dict) for item in value):
            return value
    raise ValueError("LLM response does not contain a valid JSON object array")


def validate_rank_results(
    rows: Sequence[Dict[str, Any]],
    valid_candidate_ids: Iterable[str],
    expected_count: int,
) -> List[str]:
    """Validate and normalize an exact ranked candidate-ID response."""
    valid_ids = set(valid_candidate_ids)
    if len(rows) != expected_count:
        raise ValueError(f"rank result count {len(rows)} != expected {expected_count}")

    normalized: List[Tuple[int, str]] = []
    seen_ids = set()
    seen_ranks = set()
    for row in rows:
        candidate_id = str(row.get("candidate_id") or "").strip()
        rank = row.get("rank")
        if candidate_id not in valid_ids:
            raise ValueError(f"unknown candidate_id: {candidate_id or '<missing>'}")
        if candidate_id in seen_ids:
            raise ValueError(f"duplicate candidate_id: {candidate_id}")
        if not isinstance(rank, int) or rank < 1 or rank > expected_count:
            raise ValueError(f"invalid rank for {candidate_id}: {rank}")
        if rank in seen_ranks:
            raise ValueError(f"duplicate rank: {rank}")
        seen_ids.add(candidate_id)
        seen_ranks.add(rank)
        normalized.append((rank, candidate_id))

    expected_ranks = set(range(1, expected_count + 1))
    if seen_ranks != expected_ranks:
        raise ValueError("rank sequence is incomplete")
    normalized.sort()
    return [candidate_id for _, candidate_id in normalized]


def reconcile_written_results(
    rows: Sequence[Dict[str, Any]],
    valid_candidate_ids: Iterable[str],
) -> Tuple[Dict[str, Dict[str, Any]], List[str]]:
    """Bind writer results by stable ID and report missing IDs."""
    expected = list(valid_candidate_ids)
    expected_set = set(expected)
    by_id: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        candidate_id = str(row.get("candidate_id") or "").strip()
        if candidate_id not in expected_set:
            raise ValueError(f"writer returned unknown candidate_id: {candidate_id or '<missing>'}")
        if candidate_id in by_id:
            raise ValueError(f"writer returned duplicate candidate_id: {candidate_id}")
        by_id[candidate_id] = dict(row)
    missing = [candidate_id for candidate_id in expected if candidate_id not in by_id]
    return by_id, missing


def report_window(
    report_date: str,
    cutoff_hour: int = 6,
    cutoff_minute: int = 40,
    utc_offset_hours: int = 8,
) -> Tuple[datetime, datetime, datetime, datetime]:
    """Return UTC and local boundaries for one explicit report date."""
    local_tz = timezone(timedelta(hours=utc_offset_hours))
    end_local = datetime.strptime(report_date, "%Y-%m-%d").replace(
        hour=cutoff_hour,
        minute=cutoff_minute,
        second=0,
        microsecond=0,
        tzinfo=local_tz,
    )
    start_local = end_local - timedelta(days=1)
    return (
        start_local.astimezone(timezone.utc),
        end_local.astimezone(timezone.utc),
        start_local,
        end_local,
    )


def atomic_write_text(path: str, content: str) -> None:
    """Atomically replace a UTF-8 text file in its destination directory."""
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".tmp-", dir=directory, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def atomic_write_json(path: str, data: Any) -> None:
    atomic_write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
