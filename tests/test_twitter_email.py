import unittest

import twitter_push


class TwitterEmailTests(unittest.TestCase):
    def test_highlights_link_back_to_tweets(self) -> None:
        cache = [
            {"title": "a", "source": "@openai", "category": "Company"},
            {"title": "b", "source": "@karpathy", "category": "Researcher"},
        ]
        records = [
            {"title": "OpenAI 发布 <新模型>", "source": "openai", "link": "https://x.com/OpenAI/status/1"},
            {"title": "无链接条目", "source": "karpathy"},
        ]

        subject, html_content, text_content = twitter_push.build_twitter_email(
            cache, records, "2099-01-02"
        )

        self.assertIn("01月02日", subject)
        self.assertIn("公司发布 1 条", html_content)
        self.assertIn('<a href="https://x.com/OpenAI/status/1">OpenAI 发布 &lt;新模型&gt;</a>', html_content)
        self.assertIn("<li>无链接条目", html_content)
        self.assertIn("twitter-preview-2099-01-02.md", html_content)
        self.assertIn("https://x.com/OpenAI/status/1", text_content)

    def test_no_highlights_still_links_full_preview(self) -> None:
        subject, html_content, _ = twitter_push.build_twitter_email([], [], "2099-01-02")

        self.assertIn("今日未能提取重点", html_content)
        self.assertIn("twitter-preview-2099-01-02.md", html_content)


if __name__ == "__main__":
    unittest.main()
