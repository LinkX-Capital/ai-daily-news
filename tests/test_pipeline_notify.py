import os
from pathlib import Path
import smtplib
import tempfile
import unittest
from unittest import mock

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

    def test_pushplus_payload_lists_summary_and_link(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            base_dir = Path(temporary_directory)
            (base_dir / "daily-ai-news-2099-01-02.html").write_text(
                """
                <div class="summary">
                  <div class="sum-cat">
                    <span class="sum-cat-name">模型前沿</span>
                    <span class="sum-item">模型 A &amp; 模型 B</span>
                  </div>
                </div>
                <div class="layout"></div>
                """,
                encoding="utf-8",
            )

            payload = pipeline_notify._build_pushplus_payload(
                "2099-01-02",
                "https://example.com/report.html",
                "test-token",
                base_dir,
            )

        self.assertEqual(payload["token"], "test-token")
        self.assertEqual(payload["template"], "html")
        self.assertIn("01月02日", payload["title"])
        self.assertIn("<h4>模型前沿</h4>", payload["content"])
        self.assertIn("<li>模型 A &amp; 模型 B</li>", payload["content"])
        self.assertIn('href="https://example.com/report.html"', payload["content"])

    def test_pushplus_payload_without_summary_still_links_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            payload = pipeline_notify._build_pushplus_payload(
                "2099-01-02",
                "https://example.com/report.html",
                "test-token",
                Path(temporary_directory),
            )

        self.assertIn("今日日报已发布", payload["content"])
        self.assertIn('href="https://example.com/report.html"', payload["content"])

    def test_email_has_subject_recipients_and_html_link(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            message = pipeline_notify._build_email(
                "2099-01-02",
                "https://example.com/report.html",
                "sender@example.com",
                ["a@example.com", "b@example.com"],
                Path(temporary_directory),
            )

        self.assertIn("01月02日", message["Subject"])
        self.assertEqual(message["To"], "a@example.com, b@example.com")
        html_part = message.get_body(preferencelist=("html",))
        self.assertIn('href="https://example.com/report.html"', html_part.get_content())

    def test_send_email_logs_in_and_sends_to_all_recipients(self) -> None:
        environment = {
            "EMAIL_RECIPIENTS": "a@example.com, b@example.com",
            "SMTP_USER": "sender@example.com",
            "SMTP_PASSWORD": "offline-code",
            "SMTP_SERVER": "smtp.example.com",
            "SMTP_PORT": "465",
        }
        with mock.patch.dict(os.environ, environment), mock.patch(
            "pipeline_notify.smtplib.SMTP_SSL"
        ) as smtp_ssl:
            client = smtp_ssl.return_value
            ok = pipeline_notify._send_email("2099-01-02", "https://example.com/r.html")

        self.assertTrue(ok)
        smtp_ssl.assert_called_once_with("smtp.example.com", 465, timeout=20)
        client.login.assert_called_once_with("sender@example.com", "offline-code")
        sent = client.send_message.call_args.args[0]
        self.assertEqual(sent["To"], "a@example.com, b@example.com")

    def test_send_email_rejected_login_fails(self) -> None:
        environment = {
            "EMAIL_RECIPIENTS": "a@example.com",
            "SMTP_USER": "sender@example.com",
            "SMTP_PASSWORD": "wrong-code",
        }
        with mock.patch.dict(os.environ, environment), mock.patch(
            "pipeline_notify.smtplib.SMTP_SSL"
        ) as smtp_ssl:
            client = smtp_ssl.return_value
            client.login.side_effect = smtplib.SMTPAuthenticationError(535, b"denied")
            ok = pipeline_notify._send_email("2099-01-02", "https://example.com/r.html")

        self.assertFalse(ok)
        client.send_message.assert_not_called()

    def test_send_email_without_credentials_fails(self) -> None:
        with mock.patch.dict(os.environ, {"EMAIL_RECIPIENTS": "a@example.com"}, clear=True):
            self.assertFalse(
                pipeline_notify._send_email("2099-01-02", "https://example.com/r.html")
            )


if __name__ == "__main__":
    unittest.main()
