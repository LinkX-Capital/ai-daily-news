import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from pipeline_core import (
    atomic_write_json,
    atomic_write_text,
    ensure_candidate_ids,
    make_candidate_id,
    parse_llm_array,
    reconcile_written_results,
    report_window,
    validate_rank_results,
)

try:
    import feed_v5
except ModuleNotFoundError as exc:  # Allow pure-core tests in minimal environments.
    feed_v5 = None
    FEED_IMPORT_ERROR = str(exc)
else:
    FEED_IMPORT_ERROR = ""


class CandidateIdentityTests(unittest.TestCase):
    def test_tracking_parameters_do_not_change_candidate_id(self):
        clean = {
            "source": "Example Feed",
            "title": "A launch",
            "link": "https://example.com/news/item?id=42",
        }
        tracked = {
            "source": "Example Feed",
            "title": "A launch",
            "link": (
                "HTTPS://EXAMPLE.COM/news/item/?id=42&utm_source=newsletter"
                "&utm_medium=email&fbclid=tracking#section"
            ),
        }

        self.assertEqual(make_candidate_id(clean), make_candidate_id(tracked))

        prepared = ensure_candidate_ids([tracked])[0]
        self.assertEqual(prepared["link"], "https://example.com/news/item?id=42")
        self.assertEqual(prepared["candidate_id"], make_candidate_id(clean))

    def test_same_native_id_from_different_sources_does_not_collide(self):
        source_a = {
            "source": "Publisher A",
            "source_item_id": "native-123",
            "link": "https://example.com/shared",
            "title": "Same title",
        }
        source_b = {
            "source": "Publisher B",
            "source_item_id": "native-123",
            "link": "https://example.com/shared",
            "title": "Same title",
        }
        next_item = {
            **source_a,
            "source_item_id": "native-124",
        }

        self.assertNotEqual(make_candidate_id(source_a), make_candidate_id(source_b))
        self.assertNotEqual(make_candidate_id(source_a), make_candidate_id(next_item))


class LLMContractTests(unittest.TestCase):
    def test_valid_json_escapes_are_not_rewritten(self):
        expected = [
            {
                "candidate_id": "cand_1",
                "title": '包含"引号"与反斜杠',
                "body": "第一行\n第二行",
                "source_path": r"C:\temp\news.json",
            }
        ]
        encoded = json.dumps(expected, ensure_ascii=False)

        self.assertEqual(parse_llm_array(f"```json\n{encoded}\n```"), expected)

    def test_rank_results_are_sorted_only_after_exact_validation(self):
        rows = [
            {"candidate_id": "cand_b", "rank": 2},
            {"candidate_id": "cand_c", "rank": 3},
            {"candidate_id": "cand_a", "rank": 1},
        ]

        self.assertEqual(
            validate_rank_results(rows, {"cand_a", "cand_b", "cand_c"}, 3),
            ["cand_a", "cand_b", "cand_c"],
        )

    def test_rank_result_count_id_and_rank_violations_are_rejected(self):
        cases = {
            "wrong count": (
                [{"candidate_id": "cand_a", "rank": 1}],
                {"cand_a", "cand_b"},
                2,
            ),
            "unknown id": (
                [
                    {"candidate_id": "cand_a", "rank": 1},
                    {"candidate_id": "unknown", "rank": 2},
                ],
                {"cand_a", "cand_b"},
                2,
            ),
            "duplicate id": (
                [
                    {"candidate_id": "cand_a", "rank": 1},
                    {"candidate_id": "cand_a", "rank": 2},
                ],
                {"cand_a", "cand_b"},
                2,
            ),
            "duplicate rank": (
                [
                    {"candidate_id": "cand_a", "rank": 1},
                    {"candidate_id": "cand_b", "rank": 1},
                ],
                {"cand_a", "cand_b"},
                2,
            ),
            "non-integer rank": (
                [
                    {"candidate_id": "cand_a", "rank": 1},
                    {"candidate_id": "cand_b", "rank": "2"},
                ],
                {"cand_a", "cand_b"},
                2,
            ),
            "out-of-range rank": (
                [
                    {"candidate_id": "cand_a", "rank": 1},
                    {"candidate_id": "cand_b", "rank": 3},
                ],
                {"cand_a", "cand_b"},
                2,
            ),
        }

        for label, (rows, valid_ids, expected_count) in cases.items():
            with self.subTest(label=label):
                with self.assertRaises(ValueError):
                    validate_rank_results(rows, valid_ids, expected_count)

    def test_partial_writer_result_reports_missing_ids_in_expected_order(self):
        rows = [{"candidate_id": "cand_b", "title": "已成稿"}]

        by_id, missing = reconcile_written_results(
            rows, ["cand_a", "cand_b", "cand_c"]
        )

        self.assertEqual(list(by_id), ["cand_b"])
        self.assertEqual(missing, ["cand_a", "cand_c"])

    def test_writer_unknown_and_duplicate_ids_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown candidate_id"):
            reconcile_written_results(
                [{"candidate_id": "unknown"}],
                ["cand_a"],
            )

        with self.assertRaisesRegex(ValueError, "duplicate candidate_id"):
            reconcile_written_results(
                [
                    {"candidate_id": "cand_a", "title": "版本一"},
                    {"candidate_id": "cand_a", "title": "版本二"},
                ],
                ["cand_a"],
            )


class WindowAndAtomicWriteTests(unittest.TestCase):
    def test_report_window_uses_0640_utc_plus_8_half_open_boundaries(self):
        start_utc, end_utc, start_local, end_local = report_window("2026-07-28")
        cst = timezone(timedelta(hours=8))

        self.assertEqual(
            start_local,
            datetime(2026, 7, 27, 6, 40, tzinfo=cst),
        )
        self.assertEqual(
            end_local,
            datetime(2026, 7, 28, 6, 40, tzinfo=cst),
        )
        self.assertEqual(
            start_utc,
            datetime(2026, 7, 26, 22, 40, tzinfo=timezone.utc),
        )
        self.assertEqual(
            end_utc,
            datetime(2026, 7, 27, 22, 40, tzinfo=timezone.utc),
        )
        self.assertEqual(end_utc - start_utc, timedelta(days=1))

        just_before_start = start_utc - timedelta(microseconds=1)
        just_before_end = end_utc - timedelta(microseconds=1)
        self.assertFalse(start_utc <= just_before_start < end_utc)
        self.assertTrue(start_utc <= start_utc < end_utc)
        self.assertTrue(start_utc <= just_before_end < end_utc)
        self.assertFalse(start_utc <= end_utc < end_utc)

    def test_atomic_writes_replace_content_and_leave_no_temp_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            text_path = root / "nested" / "report.md"
            json_path = root / "nested" / "manifest.json"

            atomic_write_text(str(text_path), "旧内容")
            atomic_write_text(str(text_path), "新内容")
            atomic_write_json(str(json_path), {"状态": "ready"})

            self.assertEqual(text_path.read_text(encoding="utf-8"), "新内容")
            self.assertEqual(
                json.loads(json_path.read_text(encoding="utf-8")),
                {"状态": "ready"},
            )
            self.assertTrue(json_path.read_text(encoding="utf-8").endswith("\n"))
            self.assertEqual(list((root / "nested").glob(".tmp-*")), [])

    def test_atomic_write_failure_preserves_old_file_and_cleans_temp_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            target = Path(temp_dir) / "report.md"
            target.write_text("已发布版本", encoding="utf-8")

            with patch(
                "pipeline_core.os.replace",
                side_effect=OSError("simulated replace failure"),
            ):
                with self.assertRaises(OSError):
                    atomic_write_text(str(target), "不完整的新版本")

            self.assertEqual(target.read_text(encoding="utf-8"), "已发布版本")
            self.assertEqual(list(target.parent.glob(".tmp-*")), [])


@unittest.skipUnless(
    feed_v5 is not None,
    f"feed_v5 dependencies unavailable: {FEED_IMPORT_ERROR}",
)
class CanonicalArchiveTests(unittest.TestCase):
    def test_canonical_archive_excludes_raw_text_and_keeps_provenance(self):
        provenance = {
            "selection": "llm_ranked",
            "writing": "llm_writer",
            "status": "validated",
        }
        article = {
            "candidate_id": "cand_1",
            "title": "中文成稿标题",
            "body": "这是已经处理完成的中文正文。",
            "insight": "这项进展值得持续关注。",
            "categories": ["模型前沿"],
            "source": "Example",
            "link": "https://example.com/item",
            "provenance": provenance,
            "raw_title": "Raw English source title",
            "raw_summary": "Raw English source summary",
            "summary": "Unprocessed summary",
            "content": "Full scraped source content",
            "_writer_evidence": "Private evidence text",
        }

        archive = feed_v5.build_archive_data([article], "2026-07-28")
        saved = archive["articles"][0]

        self.assertEqual(saved["provenance"], provenance)
        self.assertEqual(saved["title"], "中文成稿标题")
        for forbidden in (
            "raw_title",
            "raw_summary",
            "summary",
            "content",
            "_writer_evidence",
        ):
            with self.subTest(field=forbidden):
                self.assertNotIn(forbidden, saved)
        self.assertIn("raw_title", article, "archive build must not mutate input")

    def test_post_rank_event_identity_collapses_release_duplicates_only(self):
        kimi_release = {
            "candidate_id": "kimi-release",
            "raw_title": "Kimi K3 weights have been released",
            "link": "https://example.com/kimi-release",
        }
        kimi_integration = {
            "candidate_id": "kimi-vllm",
            "raw_title": "Kimi K3 Is Here: Efficient Day-0 Support on vLLM",
            "link": "https://example.com/kimi-vllm",
        }
        duv_report = {
            "candidate_id": "duv-report",
            "raw_title": (
                "ASML Shares Slide After Report on China Producing DUV Tool"
            ),
            "link": "https://example.com/duv-report",
        }
        duv_production = {
            "candidate_id": "duv-production",
            "raw_title": (
                "China Begins Mass Production of Homegrown DUV Chip Tools"
            ),
            "link": "https://example.com/duv-production",
        }
        vera = {
            "candidate_id": "nvidia-vera",
            "raw_title": "NVIDIA Harnesses Vera CPU to Speed Up CPU and GPU Design",
            "link": "https://example.com/vera",
        }
        rubin = {
            "candidate_id": "nvidia-rubin",
            "raw_title": "Nvidia New Rubin Servers Offer Relief to Cloud Providers",
            "link": "https://example.com/rubin",
        }
        microsoft_media_a = {
            "candidate_id": "ms-a",
            "raw_title": (
                "Microsoft launches its first cybersecurity model and "
                "a new agentic cybersecurity system"
            ),
            "link": "https://example.com/ms-a",
        }
        microsoft_media_b = {
            "candidate_id": "ms-b",
            "raw_title": (
                "Microsoft Launches New Homegrown AI for Cybersecurity"
            ),
            "link": "https://example.com/ms-b",
        }

        self.assertTrue(feed_v5._same_ranked_event(kimi_release, kimi_integration))
        self.assertTrue(feed_v5._same_ranked_event(duv_report, duv_production))
        self.assertTrue(
            feed_v5._same_ranked_event(microsoft_media_a, microsoft_media_b)
        )
        self.assertFalse(feed_v5._same_ranked_event(vera, rubin))

        by_id = {
            article["candidate_id"]: article
            for article in (duv_report, duv_production, vera)
        }
        collapsed = feed_v5._collapse_ranked_events(
            ["duv-report", "duv-production", "nvidia-vera"],
            by_id,
            2,
        )
        self.assertEqual(collapsed[0], "duv-production")
        self.assertEqual(
            duv_report["_event_duplicate_of"],
            "duv-production",
        )

    def test_rank_prompt_order_interleaves_categories_and_sources_without_loss(self):
        articles = [
            {
                "candidate_id": "industry-a1",
                "categories": ["产业动态"],
                "source": "Outlet A",
                "priority": 100,
            },
            {
                "candidate_id": "industry-a2",
                "categories": ["产业动态"],
                "source": "Outlet A",
                "priority": 90,
            },
            {
                "candidate_id": "industry-b1",
                "categories": ["产业动态"],
                "source": "Outlet B",
                "priority": 10,
            },
            {
                "candidate_id": "research-c1",
                "categories": ["研究关注"],
                "source": "arXiv",
                "priority": 5,
            },
        ]

        ordered = feed_v5._interleave_rank_candidates(articles)
        ordered_ids = [article["candidate_id"] for article in ordered]

        self.assertEqual(set(ordered_ids), {a["candidate_id"] for a in articles})
        self.assertEqual(len(ordered_ids), len(articles))
        self.assertLess(
            ordered_ids.index("industry-b1"),
            ordered_ids.index("industry-a2"),
            "a second source should appear before one source monopolizes a desk",
        )
        self.assertLess(
            ordered_ids.index("research-c1"),
            ordered_ids.index("industry-a2"),
            "a low-priority desk must still appear early enough to be read",
        )

    def test_material_strategic_investments_survive_portfolio_balancing(self):
        articles = []
        for index in range(1, 19):
            articles.append(
                {
                    "candidate_id": f"item-{index}",
                    "raw_title": f"Independent AI event {index}",
                    "source": f"Source {index}",
                }
            )
        by_id = {article["candidate_id"]: article for article in articles}
        by_id["item-4"]["raw_title"] = "Kimi developer helper update"
        by_id["item-5"]["raw_title"] = "MoonEP developer helper update"
        by_id["item-6"]["raw_title"] = (
            "Nvidia to Invest $1 Billion in an AI Data Center"
        )
        by_id["item-15"]["raw_title"] = (
            "Microsoft Launches a New AI Cybersecurity System"
        )
        by_id["item-17"]["raw_title"] = (
            "Nvidia Makes Multibillion Dollar Investment in an AI Lab"
        )

        preliminary = [f"item-{index}" for index in range(1, 19)]
        result = feed_v5._build_editorial_portfolio(
            global_ids=preliminary[:15],
            preliminary_ids=preliminary,
            all_candidate_ids=preliminary,
            research_ids=[],
            article_by_id=by_id,
            selected_count=15,
            final_count=15,
        )

        self.assertIn("item-6", result)
        self.assertIn("item-17", result)
        self.assertIn("item-15", result)
        self.assertNotIn(
            "item-5",
            result,
            "a lower-ranked same-company helper update should yield first",
        )
        self.assertEqual(
            by_id["item-17"]["_portfolio_required"],
            ["strategic_capital"],
        )

    def test_writer_uses_short_refs_and_retries_only_invalid_item(self):
        article = {
            "candidate_id": "cand_very_long_internal_hash",
            "_writer_ref": "W01",
            "_writer_evidence": "公司发布了一项经过验证的新系统。",
            "raw_title": "Company launches a new system",
            "source": "Example",
            "link": "https://example.com/item",
        }
        one_sentence = json.dumps(
            [
                {
                    "candidate_id": "W01",
                    "title": "公司发布全新系统",
                    "body": "公司发布了一项经过验证的新系统。",
                    "insight": "这项进展值得持续观察。",
                    "category": "产业动态",
                }
            ],
            ensure_ascii=False,
        )
        two_sentences = json.dumps(
            [
                {
                    "candidate_id": "W01",
                    "title": "公司发布全新系统",
                    "body": (
                        "公司发布了一项经过验证的新系统。"
                        "该系统目前面向指定场景使用。"
                    ),
                    "insight": "这项进展值得持续观察。",
                    "category": "产业动态",
                }
            ],
            ensure_ascii=False,
        )

        with patch(
            "feed_v5.call_llm",
            side_effect=[one_sentence, two_sentences],
        ) as mocked_call, patch("time.sleep"):
            written, missing = feed_v5._call_writer(
                [article], [], attempts=2
            )

        self.assertEqual(missing, [])
        self.assertEqual(list(written), ["cand_very_long_internal_hash"])
        self.assertEqual(
            written["cand_very_long_internal_hash"]["candidate_id"],
            "cand_very_long_internal_hash",
        )
        self.assertEqual(mocked_call.call_count, 2)
        retry_prompt = mocked_call.call_args_list[1].args[0]
        self.assertIn("candidate_id: W01", retry_prompt)
        self.assertIn("body 少于 2 句", retry_prompt)


if __name__ == "__main__":
    unittest.main()
