import unittest
from unittest.mock import Mock, patch

import qa_autofix
from release_gate import GateResult


def llm_response(text):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "content": [{"type": "text", "text": text}],
    }
    return response


class QAAutofixTests(unittest.TestCase):
    @patch.object(qa_autofix.httpx, "post")
    def test_enrichment_accepts_valid_chinese_output(self, post):
        post.return_value = llm_response(
            "研究团队公布了新的训练方法，并报告多项评测结果。"
            "该方法降低了计算成本，同时保持模型准确率。"
            "团队还公开了实验设置与主要参数，供研究者复核。"
        )
        with patch.object(qa_autofix, "API_KEY", "test-key"):
            result = qa_autofix._enrich_body_with_llm(
                "测试标题", "当前正文", "source text", "研究关注",
            )

        self.assertIsNotNone(result)

    @patch.object(qa_autofix.httpx, "post")
    def test_enrichment_rejects_unprocessed_english_output(self, post):
        post.return_value = llm_response(
            "This source says the model achieved much better results "
            "than all previous systems on several difficult benchmarks."
        )
        with patch.object(qa_autofix, "API_KEY", "test-key"):
            result = qa_autofix._enrich_body_with_llm(
                "测试标题", "当前正文", "source text", "研究关注",
            )

        self.assertIsNone(result)

    @patch.object(qa_autofix, "run_release_gate_on_md")
    @patch.object(qa_autofix, "run_checks")
    @patch.object(qa_autofix, "autofix_short_body")
    def test_autofix_and_recheck_does_not_treat_fix_as_qa_pass(
        self,
        autofix,
        run_checks,
        run_gate,
    ):
        autofix.return_value = 2
        run_checks.return_value = 1
        run_gate.return_value = GateResult([], 2, 15)

        result = qa_autofix.autofix_and_recheck("2026-07-28")

        self.assertEqual(result.fixed_count, 2)
        self.assertEqual(result.issue_count, 1)
        self.assertFalse(result.passed)
        run_checks.assert_called_once_with("2026-07-28", factcheck=False)
        run_gate.assert_called_once_with("2026-07-28")


if __name__ == "__main__":
    unittest.main()
