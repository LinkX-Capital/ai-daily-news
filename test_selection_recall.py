#!/usr/bin/env python3
"""预排序召回回归测试。"""

import contextlib
import io
import json
import unittest
from pathlib import Path

from improve_news import (
    _extract_company,
    filter_company_duplicates,
    filter_similar_duplicates,
    improve_news,
    is_non_news,
    merge_tweet_threads,
)


ROOT = Path(__file__).resolve().parent
TARGET_EVENTS = ("Tacta", "Naver", "Antares", "Thea", "Molt")


def _contains(article, needle):
    text = " ".join(
        str(article.get(key, ""))
        for key in ("title", "summary", "content", "source", "link")
    )
    return needle.lower() in text.lower()


class SelectionRecallTests(unittest.TestCase):
    def test_routine_cfo_appointment_is_low_value(self):
        self.assertTrue(
            is_non_news(
                "Michael Beer is joining Agility as our Chief Financial Officer"
            )
        )
        self.assertFalse(
            is_non_news(
                "Robotics Startup Tacta Shows Its Hand (and Glove)"
            )
        )

    def test_unknown_company_does_not_fall_back_to_media_source(self):
        self.assertIsNone(
            _extract_company(
                "Robotics Startup Tacta Shows Its Hand (and Glove)",
                "",
                "The Information",
            )
        )
        self.assertIsNone(
            _extract_company(
                "Molt: A Scalable PyTorch-Native Training Framework",
                "",
                "arXiv cs.LG",
            )
        )

        articles = [
            {
                "title": f"Independent startup event {index}",
                "summary": "",
                "source": "TechCrunch",
                "priority": 10 - index,
            }
            for index in range(5)
        ]
        self.assertEqual(filter_company_duplicates(articles, max_per_company=2), articles)

    def test_minimal_july_28_fixture_keeps_all_target_events(self):
        articles = [
            {
                "title": "Robotics Startup Tacta Shows Its Hand (and Glove)",
                "source": "The Information",
                "priority": 36,
            },
            {
                "title": "Nvidia to Invest $1 Billion in South Korea's Naver",
                "source": "The Information",
                "priority": 54,
            },
            {
                "title": "Antares raises $470M to build nuclear reactors",
                "source": "TechCrunch",
                "priority": 32,
            },
            {
                "title": "Thea Energy lands $20M federal grant",
                "source": "TechCrunch",
                "priority": 32,
            },
            {
                "title": "Molt: A Scalable PyTorch-Native Training Framework",
                "source": "arXiv cs.LG",
                "priority": 20,
            },
            {
                "title": "Another TechCrunch AI infrastructure story",
                "source": "TechCrunch",
                "priority": 80,
            },
            {
                "title": "Another Information AI policy story",
                "source": "The Information",
                "priority": 80,
            },
            {
                "title": "Another arXiv learning systems paper",
                "source": "arXiv cs.LG",
                "priority": 80,
            },
        ]

        with contextlib.redirect_stdout(io.StringIO()):
            selected = improve_news(articles, do_filter=True)

        for target in TARGET_EVENTS:
            self.assertTrue(
                any(_contains(article, target) for article in selected),
                f"{target} disappeared before rank",
            )
        self.assertEqual(len(selected), len(articles))

    def test_reply_marker_and_adjacent_status_ids_are_not_thread_evidence(self):
        articles = [
            {
                "title": "Independent product announcement",
                "source": "@example",
                "link": "https://x.com/example/status/100",
                "priority": 20,
                "is_tweet": True,
            },
            {
                "title": "R to @someone: unrelated reply about another event",
                "source": "@example",
                "link": "https://x.com/example/status/101",
                "priority": 10,
                "is_tweet": True,
            },
        ]

        self.assertEqual(merge_tweet_threads(articles), articles)

    def test_explicit_parent_id_merges_only_the_real_thread(self):
        articles = [
            {
                "title": "Main announcement",
                "source": "@example",
                "link": "https://x.com/example/status/100",
                "priority": 20,
                "is_tweet": True,
            },
            {
                "title": "Supporting detail",
                "source": "@example",
                "link": "https://x.com/example/status/900",
                "in_reply_to_status_id": "100",
                "priority": 10,
                "is_tweet": True,
            },
            {
                "title": "R to @other: unrelated reply",
                "source": "@example",
                "link": "https://x.com/example/status/901",
                "priority": 5,
                "is_tweet": True,
            },
        ]

        with contextlib.redirect_stdout(io.StringIO()):
            merged = merge_tweet_threads(articles)

        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0]["thread_count"], 2)
        self.assertIn("Main announcement", merged[0]["summary"])
        self.assertIn("Supporting detail", merged[0]["summary"])
        self.assertEqual(merged[1]["title"], "R to @other: unrelated reply")

    def test_template_similarity_does_not_merge_different_funding_events(self):
        articles = [
            {
                "title": "Workstreet获得种子轮融资",
                "link": "https://example.com/workstreet",
                "priority": 20,
            },
            {
                "title": "Reverie AI获得种子轮融资",
                "link": "https://example.com/reverie",
                "priority": 20,
            },
            {
                "title": "Uvera获得种子轮融资",
                "link": "https://example.com/uvera",
                "priority": 20,
            },
        ]
        self.assertEqual(len(filter_similar_duplicates(articles, threshold=0.35)), 3)

    def test_provider_specific_announcements_are_not_treated_as_one_event(self):
        articles = [
            {
                "title": "Kimi K3 is now available on Nebius",
                "link": "https://x.com/kimi/status/100",
                "priority": 20,
            },
            {
                "title": "Kimi K3 is now live on Together AI",
                "link": "https://x.com/kimi/status/200",
                "priority": 20,
            },
            {
                "title": "Excited to have Baseten as our Day 0 launch partner",
                "link": "https://x.com/kimi/status/300",
                "priority": 20,
            },
            {
                "title": "Happy to have Fireworks as our Day 0 launch partner",
                "link": "https://x.com/kimi/status/400",
                "priority": 20,
            },
        ]
        self.assertEqual(len(filter_similar_duplicates(articles, threshold=0.35)), 4)

    def test_full_july_28_cache_does_not_collapse_before_rank(self):
        payload = json.loads((ROOT / "cache_raw_news.json").read_text(encoding="utf-8"))
        articles = payload["articles"]
        self.assertEqual(len(articles), 159)

        with contextlib.redirect_stdout(io.StringIO()):
            selected = improve_news(articles, do_filter=True)

        # 21 条显式非新闻仍应过滤；预排序阶段不能再次从约 130 条砍到 47。
        self.assertGreaterEqual(len(selected), 130)
        for target in TARGET_EVENTS:
            self.assertTrue(
                any(_contains(article, target) for article in selected),
                f"{target} disappeared in the 159-item replay",
            )

        sources = [article.get("source") for article in selected]
        self.assertGreater(sources.count("TechCrunch"), 2)
        self.assertGreater(sources.count("The Information"), 2)
        self.assertGreater(sources.count("arXiv cs.LG"), 2)


if __name__ == "__main__":
    unittest.main()
