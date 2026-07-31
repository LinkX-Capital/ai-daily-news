import unittest

from release_gate import chinese_text_ok, evaluate_release_gate


def valid_article(**overrides):
    article = {
        "candidate_id": "candidate-1",
        "title": "OpenAI 发布新一代推理模型",
        "body": "OpenAI 发布新一代推理模型，并公布了训练方法与评测结果。该模型将在本周向开发者开放。",
        "categories": ["模型前沿"],
        "link": "https://example.com/news",
        "provenance": {
            "selection": "llm_ranked",
            "writing": "llm_writer",
            "status": "validated",
        },
    }
    article.update(overrides)
    return article


class ReleaseGateTests(unittest.TestCase):
    def test_valid_canonical_article_passes(self):
        result = evaluate_release_gate([valid_article()])

        self.assertTrue(result.passed)
        self.assertEqual(result.blockers, [])
        self.assertEqual(result.warnings, [])
        self.assertEqual(result.exit_code, 0)

    def test_pipeline_string_provenance_passes(self):
        article = valid_article()
        article.pop("provenance")
        article["_provenance"] = "llm_written_validated"

        result = evaluate_release_gate([article])

        self.assertTrue(result.passed)

    def test_english_and_scrape_residue_are_blockers(self):
        article = valid_article(
            title="Microsoft launches a new artificial intelligence platform for developers",
            body=(
                "微软公布产品更新。This new system gives software developers "
                "a faster way to build intelligent production applications. "
                "[深抓补充] Image Credits: Microsoft"
            ),
        )

        result = evaluate_release_gate([article])
        codes = result.count_by_code()

        self.assertFalse(result.passed)
        self.assertIn("english_heavy_title", codes)
        self.assertIn("continuous_english_title", codes)
        self.assertIn("continuous_english_body", codes)
        self.assertIn("scrape_residue", codes)

    def test_raw_fallback_is_blocked_even_when_text_is_chinese(self):
        article = valid_article(_safety_net=True)

        result = evaluate_release_gate([article])

        self.assertIn("raw_fallback", result.count_by_code())
        self.assertFalse(result.passed)

    def test_raw_fallback_in_provenance_is_blocked(self):
        article = valid_article(provenance={"writing": "raw_fallback"})

        result = evaluate_release_gate([article])

        self.assertIn("raw_fallback", result.count_by_code())

    def test_raw_input_source_is_allowed_when_body_was_rewritten(self):
        article = valid_article(provenance={
            "input": "raw_rss",
            "writing": "llm_writer",
            "status": "validated",
        })

        result = evaluate_release_gate([article])

        self.assertTrue(result.passed)

    def test_strict_mode_requires_candidate_id_and_verified_provenance(self):
        article = valid_article()
        article.pop("candidate_id")
        article.pop("provenance")

        result = evaluate_release_gate([article])

        self.assertEqual(
            {"candidate_id_missing", "provenance_missing"},
            set(result.count_by_code()),
        )

    def test_legacy_mode_allows_metadata_missing(self):
        article = valid_article()
        article.pop("candidate_id")
        article.pop("provenance")

        result = evaluate_release_gate(
            [article],
            require_candidate_id=False,
            require_provenance=False,
        )

        self.assertTrue(result.passed)

    def test_duplicate_candidate_id_invalid_category_empty_body_and_overflow(self):
        articles = []
        for index in range(16):
            articles.append(valid_article(
                candidate_id=f"candidate-{index}",
                title=f"模型团队发布第{index + 1}项中文技术更新",
            ))
        articles[1]["candidate_id"] = articles[0]["candidate_id"]
        articles[2]["categories"] = ["其他"]
        articles[3]["body"] = ""

        result = evaluate_release_gate(articles)
        codes = result.count_by_code()

        self.assertIn("article_overflow", codes)
        self.assertIn("candidate_id_duplicate", codes)
        self.assertIn("invalid_category", codes)
        self.assertIn("empty_body", codes)

    def test_missing_source_is_warning_not_blocker(self):
        result = evaluate_release_gate([valid_article(link="")])

        self.assertTrue(result.passed)
        self.assertEqual([issue.code for issue in result.warnings], ["no_source"])

    def test_promotional_or_recruiting_item_is_blocked_as_low_value(self):
        for marker in ("招聘", "报名", "活动预告", "直播预告", "Hiring"):
            with self.subTest(marker=marker):
                result = evaluate_release_gate([valid_article(
                    body=f"团队发布最新消息，并宣布开发者{marker}现已开始。",
                )])
                self.assertIn("low_value", result.count_by_code())
                self.assertFalse(result.passed)

    def test_one_sentence_body_and_unsafe_insight_are_blocked(self):
        result = evaluate_release_gate([
            valid_article(
                body="公司公布了一项经过验证的新系统。",
                insight=(
                    "This is an unprocessed English sentence copied directly "
                    "from the source article."
                ),
            )
        ])

        self.assertIn("short_body", result.count_by_code())
        self.assertIn("unsafe_insight", result.count_by_code())
        self.assertFalse(result.passed)

    def test_chinese_output_gate_allows_brand_names_but_rejects_english_prose(self):
        self.assertTrue(chinese_text_ok(
            "OpenAI 发布模型并公布完整评测，开发者可通过 API 使用。",
            min_cjk=8,
        ))
        self.assertTrue(chinese_text_ok(
            "论文《Molt: A Scalable PyTorch-Native Training Framework for "
            "Agentic Reinforcement Learning》提出新的训练框架，并公布实验结果。",
            min_cjk=8,
        ))
        self.assertTrue(chinese_text_ok(
            "Molt：PyTorch-native Agentic RL训练框架，降低算法改动和异步成本。",
            min_cjk=8,
        ))
        self.assertFalse(chinese_text_ok(
            "This output is still a complete English sentence copied from the source.",
            min_cjk=8,
        ))
        self.assertFalse(chinese_text_ok(
            "模型公布结果。[搜索补充] Abstract: copied text",
            min_cjk=8,
        ))


if __name__ == "__main__":
    unittest.main()
