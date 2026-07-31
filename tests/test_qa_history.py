import csv
import tempfile
import unittest
from pathlib import Path

from qa import _log_score


class QAHistoryTests(unittest.TestCase):
    def test_date_and_prompt_version_are_the_deduplication_key(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            log_path = temp_path / "qa_history.csv"
            prompt_path = temp_path / "news_processor.md"
            log_path.touch()
            prompt_path.write_text("prompt v1", encoding="utf-8")
            articles = [{"title": "测试条目"}]
            issues = [("short_body", "测试条目", "正文过短")]

            _log_score(
                "2026-07-28",
                articles,
                issues,
                log_path=str(log_path),
                prompt_path=str(prompt_path),
            )
            _log_score(
                "2026-07-28",
                articles,
                issues,
                log_path=str(log_path),
                prompt_path=str(prompt_path),
            )

            with log_path.open(encoding="utf-8", newline="") as history_file:
                rows = list(csv.DictReader(history_file))
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["date"], "2026-07-28")
            self.assertTrue(rows[0]["prompt_version"])

            prompt_path.write_text("prompt v2", encoding="utf-8")
            _log_score(
                "2026-07-28",
                articles,
                issues,
                log_path=str(log_path),
                prompt_path=str(prompt_path),
            )

            with log_path.open(encoding="utf-8", newline="") as history_file:
                rows = list(csv.DictReader(history_file))
            self.assertEqual(len(rows), 2)
            self.assertNotEqual(
                rows[0]["prompt_version"],
                rows[1]["prompt_version"],
            )


if __name__ == "__main__":
    unittest.main()
