from pathlib import Path
import tempfile
import unittest

import pipeline_notify


class PipelineNotifyTests(unittest.TestCase):
    def test_payload_contains_rendered_summary_before_button(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            base_dir = Path(temporary_directory)
            (base_dir / "daily-ai-news-2099-01-02.html").write_text(
                """
                <div class="summary">
                  <div class="sum-cat">
                    <span class="sum-cat-name">模型前沿</span>
                    <span class="sum-item">模型 A &amp; 模型 B</span>
                    <span class="sum-item"><strong>智能体</strong>更新</span>
                  </div>
                  <div class="sum-cat">
                    <span class="sum-cat-name">研究关注</span>
                    <span class="sum-item">新论文</span>
                  </div>
                </div>
                <div class="layout"></div>
                """,
                encoding="utf-8",
            )

            payload = pipeline_notify._build_payload(
                "2099-01-02",
                "https://example.com/report.html",
                base_dir,
            )

        elements = payload["card"]["elements"]
        self.assertEqual(
            [element["tag"] for element in elements],
            ["div", "div", "hr", "action"],
        )
        self.assertIn("**模型前沿**", elements[0]["text"]["content"])
        self.assertIn("模型 A & 模型 B", elements[0]["text"]["content"])
        self.assertIn("智能体更新", elements[0]["text"]["content"])
        self.assertEqual(
            elements[-1]["actions"][0]["url"],
            "https://example.com/report.html",
        )

    def test_missing_summary_still_produces_nonempty_body(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            payload = pipeline_notify._build_payload(
                "2099-01-02",
                "https://example.com/report.html",
                Path(temporary_directory),
            )

        elements = payload["card"]["elements"]
        self.assertEqual(elements[0]["tag"], "div")
        self.assertTrue(elements[0]["text"]["content"].strip())
        self.assertEqual(elements[-1]["tag"], "action")

    def test_partially_unparseable_summary_uses_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            base_dir = Path(temporary_directory)
            (base_dir / "daily-ai-news-2099-01-02.html").write_text(
                """
                <div class="summary">
                  <div class="sum-cat">
                    <span class="sum-cat-name">模型前沿</span>
                    <span class="sum-item">模型更新</span>
                  </div>
                  <div class="sum-cat extra-class">
                    <span class="sum-cat-name">研究关注</span>
                    <span class="sum-item">新论文</span>
                  </div>
                </div>
                <div class="layout"></div>
                """,
                encoding="utf-8",
            )

            payload = pipeline_notify._build_payload(
                "2099-01-02",
                "https://example.com/report.html",
                base_dir,
            )

        elements = payload["card"]["elements"]
        self.assertEqual([element["tag"] for element in elements], ["div", "hr", "action"])
        self.assertIn("今日日报已发布", elements[0]["text"]["content"])


if __name__ == "__main__":
    unittest.main()
