#!/usr/bin/env python3
"""Deterministic, offline release gate for daily-news articles.

This module deliberately has no network or LLM dependency.  The pipeline can
run it against the canonical article dictionaries immediately before writing
or publishing any artifact.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence


VALID_CATEGORIES = {
    "模型前沿",
    "产业动态",
    "算力追踪",
    "初创&融资",
    "研究关注",
    "X讨论",
}
MAX_ARTICLES = 15

# These markers are produced by crawlers/search tools, not by an editor.
SCRAPE_RESIDUE_MARKERS = (
    "[深抓补充]",
    "[搜索补充]",
    "Image Credits",
    "Abstract:",
    "Keywords:",
    "关键词:",
    "作者:",
    "Announce Type:",
    "Sign up for",
    "Advertisement",
    "```",
)

LOW_VALUE_MARKERS = (
    "招募",
    "征集中",
    "倒计时",
    "沙龙",
    "报名",
    "活动预告",
    "招聘",
    "求职",
    "hiring",
    "讲座预告",
    "直播预告",
)

RAW_FALLBACK_FLAGS = (
    "_safety_net",
    "safety_net",
    "_raw_fallback",
    "raw_fallback",
    "is_raw_fallback",
    "unprocessed_fallback",
)

PROVENANCE_FIELDS = (
    "provenance",
    "_provenance",
    "writing_provenance",
    "body_provenance",
    "generation_path",
)

_RAW_PROVENANCE_TOKENS = {
    "raw",
    "fallback",
    "safety",
    "passthrough",
    "unprocessed",
    "untranslated",
    "source_text",
}
_SAFE_PROVENANCE_TOKENS = {
    "llm",
    "writer",
    "written",
    "rewrite",
    "rewritten",
    "edited",
    "human",
    "manual",
    "recovered",
    "validated",
}


@dataclass(frozen=True)
class GateIssue:
    """One machine-readable release-gate finding."""

    code: str
    severity: str
    title: str
    detail: str
    article_index: Optional[int] = None
    candidate_id: Optional[str] = None
    field: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def as_legacy_tuple(self):
        """Return the tuple shape historically used by ``qa.run_checks``."""
        return self.code, self.title, self.detail


@dataclass
class GateResult:
    """Structured result suitable for a hard publication decision."""

    issues: List[GateIssue]
    article_count: int
    max_articles: int

    @property
    def blockers(self) -> List[GateIssue]:
        return [issue for issue in self.issues if issue.severity == "blocker"]

    @property
    def warnings(self) -> List[GateIssue]:
        return [issue for issue in self.issues if issue.severity == "warning"]

    @property
    def passed(self) -> bool:
        return not self.blockers

    @property
    def exit_code(self) -> int:
        return 0 if self.passed else 1

    def count_by_code(self) -> Dict[str, int]:
        return dict(Counter(issue.code for issue in self.issues))

    def as_dict(self) -> Dict[str, Any]:
        return {
            "passed": self.passed,
            "article_count": self.article_count,
            "max_articles": self.max_articles,
            "blocker_count": len(self.blockers),
            "warning_count": len(self.warnings),
            "counts_by_code": self.count_by_code(),
            "issues": [issue.as_dict() for issue in self.issues],
        }


def cjk_count(text: Any) -> int:
    return len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", str(text or "")))


def ascii_letter_count(text: Any) -> int:
    return sum(char.isascii() and char.isalpha() for char in str(text or ""))


def _mask_cited_titles(text: Any) -> str:
    value = str(text or "")
    value = re.sub(r"《[^》]{1,300}》", " ", value)
    return re.sub(r"\[[^\]]{1,300}\]\([^)]+\)", " ", value)


def is_english_heavy(text: Any) -> bool:
    """Detect a field dominated by English prose, while allowing brand names."""
    value = _mask_cited_titles(text)
    latin = ascii_letter_count(value)
    cjk = cjk_count(value)
    # Chinese editorial titles often contain several English model/product
    # names.  Require a much stronger imbalance once a meaningful Chinese
    # sentence is present, while still catching an English title with a short
    # Chinese label prepended.
    return latin >= 24 and (
        (cjk < 6 and latin > max(20, cjk * 2))
        or latin > max(40, cjk * 4)
    )


def has_continuous_english_sentence(text: Any, min_words: int = 8) -> bool:
    """Detect an unprocessed English sentence embedded in otherwise Chinese text."""
    # A cited English paper/book title is valid Chinese editorial copy, not an
    # untranslated sentence.  Markdown link labels are treated the same way.
    value = _mask_cited_titles(text)
    pattern = rf"(?:\b[A-Za-z][A-Za-z'’\-]*\b[\s,;:—–\-]*){{{min_words},}}"
    return bool(re.search(pattern, value))


def find_scrape_residue(text: Any) -> Optional[str]:
    value = str(text or "")
    lower = value.lower()
    for marker in SCRAPE_RESIDUE_MARKERS:
        if marker.lower() in lower:
            return marker
    # Encoded HTML is another reliable sign that crawler output leaked through.
    if re.search(r"&#(?:x[0-9a-f]+|\d+);", value, re.IGNORECASE):
        return "HTML entity"
    return None


def find_low_value_marker(text: Any) -> Optional[str]:
    value = str(text or "")
    lower = value.lower()
    for marker in LOW_VALUE_MARKERS:
        if marker.lower() in lower:
            return marker
    return None


def chinese_text_ok(text: Any, *, min_cjk: int = 8) -> bool:
    """Return whether generated prose is safe to expose as Chinese output."""
    value = str(text or "").strip()
    return bool(
        value
        and cjk_count(value) >= min_cjk
        and not is_english_heavy(value)
        and not has_continuous_english_sentence(value)
        and not find_scrape_residue(value)
    )


def sentence_count(text: Any) -> int:
    """Count non-empty sentence fragments separated by Chinese/English stops."""
    return len([
        fragment
        for fragment in re.split(r"[。.!?！？]", str(text or ""))
        if fragment.strip()
    ])


def _categories(article: Mapping[str, Any]) -> List[str]:
    value = article.get("categories", [])
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, Sequence):
        return [str(category) for category in value if category]
    return []


def _candidate_id(article: Mapping[str, Any]) -> str:
    value = article.get("candidate_id", article.get("_candidate_id", ""))
    return str(value or "").strip()


def _truthy_flag(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    return str(value).strip().lower() not in {"", "0", "false", "none", "no", "off"}


def _flatten_provenance_values(value: Any) -> Iterable[str]:
    if isinstance(value, Mapping):
        for nested in value.values():
            yield from _flatten_provenance_values(nested)
    elif isinstance(value, (list, tuple, set)):
        for nested in value:
            yield from _flatten_provenance_values(nested)
    elif value is not None:
        yield str(value).strip().lower()


def _provenance(article: Mapping[str, Any]):
    for field in PROVENANCE_FIELDS:
        value = article.get(field)
        if value not in (None, "", {}, []):
            return field, value
    return None, None


def _provenance_tokens(value: Any) -> set:
    tokens = set()
    for part in _flatten_provenance_values(value):
        for token in re.findall(r"[a-z_]+", part):
            tokens.add(token)
            tokens.update(piece for piece in token.split("_") if piece)
    return tokens


def _has_raw_fallback(article: Mapping[str, Any], provenance: Any) -> Optional[str]:
    for flag in RAW_FALLBACK_FLAGS:
        if _truthy_flag(article.get(flag)):
            return flag

    # Some older records used a generic fallback field.
    for field in ("fallback", "fallback_type", "writing_fallback"):
        if _truthy_flag(article.get(field)):
            return field

    if isinstance(provenance, Mapping):
        # Source/input provenance may legitimately say "raw RSS".  Only output
        # path/status fields can prove that raw text was exposed as the body.
        for key, value in provenance.items():
            key_tokens = set(re.findall(r"[a-z]+", str(key).lower()))
            if "fallback" in key_tokens and _truthy_flag(value):
                return f"provenance.{key}"
            output_path_keys = {
                "writing", "writer", "body", "generation", "output",
                "path", "mode", "status", "processing",
            }
            if key_tokens & output_path_keys:
                if _provenance_tokens(value) & _RAW_PROVENANCE_TOKENS:
                    return f"provenance.{key}"
    elif _provenance_tokens(provenance) & _RAW_PROVENANCE_TOKENS:
        return "provenance"
    return None


def _has_verified_provenance(provenance: Any) -> bool:
    return bool(_provenance_tokens(provenance) & _SAFE_PROVENANCE_TOKENS)


def evaluate_release_gate(
    articles: Sequence[Mapping[str, Any]],
    *,
    max_articles: int = MAX_ARTICLES,
    require_candidate_id: bool = True,
    require_provenance: bool = True,
    valid_categories: Optional[Iterable[str]] = None,
) -> GateResult:
    """Evaluate canonical articles without network access.

    ``require_candidate_id`` and ``require_provenance`` default to ``True`` so
    production callers fail closed.  Legacy Markdown QA can explicitly disable
    those requirements because Markdown does not preserve the metadata.
    """

    valid = set(valid_categories or VALID_CATEGORIES)
    issues: List[GateIssue] = []

    if not articles:
        issues.append(GateIssue(
            "empty_report", "blocker", "日报", "没有可发布条目",
        ))
        return GateResult(issues, 0, max_articles)

    if len(articles) > max_articles:
        issues.append(GateIssue(
            "article_overflow",
            "blocker",
            "日报",
            f"条目数 {len(articles)} 超过硬上限 {max_articles}",
        ))

    ids: Dict[str, List[int]] = {}
    for index, raw_article in enumerate(articles):
        if not isinstance(raw_article, Mapping):
            issues.append(GateIssue(
                "invalid_article",
                "blocker",
                f"条目 #{index + 1}",
                "条目不是字典结构",
                article_index=index,
            ))
            continue

        article = raw_article
        title = str(article.get("title", "") or "").strip()
        display_title = title or f"条目 #{index + 1}"
        candidate_id = _candidate_id(article)

        if not title:
            issues.append(GateIssue(
                "empty_title", "blocker", display_title, "标题为空",
                index, candidate_id or None, "title",
            ))

        body = str(article.get("body", "") or "").strip()
        if not body:
            issues.append(GateIssue(
                "empty_body", "blocker", display_title, "body 为空",
                index, candidate_id or None, "body",
            ))
        elif sentence_count(body) < 2:
            issues.append(GateIssue(
                "short_body",
                "blocker",
                display_title,
                "body 少于 2 个完整句子",
                index,
                candidate_id or None,
                "body",
            ))

        low_value_marker = find_low_value_marker(f"{title}\n{body}")
        if low_value_marker:
            issues.append(GateIssue(
                "low_value",
                "blocker",
                display_title,
                f"含低价值/推广信号: {low_value_marker}",
                index,
                candidate_id or None,
            ))

        for field, value, min_cjk in (("title", title, 2), ("body", body, 8)):
            if value and cjk_count(value) < min_cjk:
                issues.append(GateIssue(
                    f"insufficient_chinese_{field}",
                    "blocker",
                    display_title,
                    f"{field} 中文字符不足（{cjk_count(value)} < {min_cjk}）",
                    index,
                    candidate_id or None,
                    field,
                ))
            if value and is_english_heavy(value):
                issues.append(GateIssue(
                    f"english_heavy_{field}",
                    "blocker",
                    display_title,
                    f"{field} 以英文为主，疑似未经中文编辑",
                    index,
                    candidate_id or None,
                    field,
                ))
            if value and has_continuous_english_sentence(value):
                issues.append(GateIssue(
                    f"continuous_english_{field}",
                    "blocker",
                    display_title,
                    f"{field} 含连续英文句子，疑似原文泄漏",
                    index,
                    candidate_id or None,
                    field,
                ))
            residue = find_scrape_residue(value)
            if residue:
                issues.append(GateIssue(
                    "scrape_residue",
                    "blocker",
                    display_title,
                    f"{field} 含抓取残留: {residue}",
                    index,
                    candidate_id or None,
                    field,
                ))

        insight = str(article.get("insight", "") or "").strip()
        if not insight:
            key_points = article.get("key_points")
            if isinstance(key_points, Sequence) and not isinstance(
                key_points, (str, bytes)
            ):
                insight = " ".join(
                    str(item) for item in key_points if item
                ).strip()
        if insight and not chinese_text_ok(insight, min_cjk=4):
            issues.append(GateIssue(
                "unsafe_insight",
                "blocker",
                display_title,
                "insight 中文不足、含连续英文原句或抓取残留",
                index,
                candidate_id or None,
                "insight",
            ))

        categories = _categories(article)
        if not categories:
            issues.append(GateIssue(
                "no_category", "blocker", display_title, "无分类",
                index, candidate_id or None, "categories",
            ))
        for category in categories:
            if category not in valid:
                issues.append(GateIssue(
                    "invalid_category",
                    "blocker",
                    display_title,
                    f"无效分类: {category}",
                    index,
                    candidate_id or None,
                    "categories",
                ))

        if candidate_id:
            ids.setdefault(candidate_id, []).append(index)
        elif require_candidate_id:
            issues.append(GateIssue(
                "candidate_id_missing",
                "blocker",
                display_title,
                "缺少稳定 candidate_id，无法验证选稿与写作链路",
                index,
                None,
                "candidate_id",
            ))

        provenance_field, provenance = _provenance(article)
        raw_fallback_field = _has_raw_fallback(article, provenance)
        if raw_fallback_field:
            issues.append(GateIssue(
                "raw_fallback",
                "blocker",
                display_title,
                f"检测到未经编辑的 fallback 路径: {raw_fallback_field}",
                index,
                candidate_id or None,
                provenance_field or raw_fallback_field,
            ))
        elif provenance is None:
            if require_provenance:
                issues.append(GateIssue(
                    "provenance_missing",
                    "blocker",
                    display_title,
                    "缺少写作 provenance，无法证明正文经过编辑",
                    index,
                    candidate_id or None,
                    "provenance",
                ))
        elif not _has_verified_provenance(provenance):
            severity = "blocker" if require_provenance else "warning"
            issues.append(GateIssue(
                "provenance_unverified",
                severity,
                display_title,
                "provenance 未标明已写作/编辑/验证",
                index,
                candidate_id or None,
                provenance_field,
            ))

        if not article.get("link"):
            issues.append(GateIssue(
                "no_source", "warning", display_title, "缺少来源链接",
                index, candidate_id or None, "link",
            ))

    for candidate_id, indexes in ids.items():
        if len(indexes) <= 1:
            continue
        titles = [
            str(articles[index].get("title", "") or f"条目 #{index + 1}")
            for index in indexes
        ]
        issues.append(GateIssue(
            "candidate_id_duplicate",
            "blocker",
            titles[0],
            f"candidate_id={candidate_id} 重复 {len(indexes)} 次: {'; '.join(titles)}",
            indexes[0],
            candidate_id,
            "candidate_id",
        ))

    return GateResult(issues, len(articles), max_articles)
