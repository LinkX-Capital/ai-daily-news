import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import open_tweets

PREVIEW = """# Twitter 动态预览

## ⭐ 今日重点（LLM 提炼）

1. **标题**
   @openai

---

## 🏢 公司发布（3条）

### @openai | Model

- tweet one
  [查看](https://x.com/OpenAI/status/1)
- tweet two
  [查看](https://x.com/OpenAI/status/2)

## 👤 研究者动态（1条）

### @karpathy | Research

- tweet three
  [查看](https://x.com/karpathy/status/3)
- duplicate
  [查看](https://x.com/OpenAI/status/1)
"""


class OpenTweetsTests(unittest.TestCase):
    def _project(self, directory: str) -> Path:
        base = Path(directory)
        (base / "cache").mkdir()
        (base / "twitter-preview-2099-01-02.md").write_text(PREVIEW, encoding="utf-8")
        (base / "twitter-preview-2099-01-01.md").write_text(PREVIEW, encoding="utf-8")
        (base / "cache" / "twitter_highlights_2099-01-02.json").write_text(
            json.dumps({"highlights": [
                {"title": "重点", "link": "https://x.com/OpenAI/status/2"},
                {"title": "无链接"},
            ]}),
            encoding="utf-8",
        )
        return base

    def test_parse_groups_links_by_section(self) -> None:
        sections = open_tweets.parse_preview_links(PREVIEW)
        self.assertEqual(sections["🏢 公司发布（3条）"], [
            "https://x.com/OpenAI/status/1", "https://x.com/OpenAI/status/2",
        ])
        self.assertEqual(len(sections["👤 研究者动态（1条）"]), 2)
        self.assertNotIn("⭐ 今日重点（LLM 提炼）", sections)

    def test_menu_has_highlights_sections_and_deduped_all(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = self._project(directory)
            self.assertEqual(open_tweets.latest_preview_date(base), "2099-01-02")
            menu = dict(open_tweets.build_menu("2099-01-02", base))

        self.assertEqual(menu["⭐ 今日重点"], ["https://x.com/OpenAI/status/2"])
        self.assertIn("🏢 公司发布", menu)
        self.assertEqual(len(menu["📚 全部推文"]), 3)

    def test_open_links_batches_and_can_stop(self) -> None:
        links = [f"https://x.com/a/status/{i}" for i in range(25)]
        with mock.patch("open_tweets.webbrowser.open_new_tab") as open_tab, \
                mock.patch("open_tweets.time.sleep"), \
                mock.patch("builtins.input", side_effect=["", "q"]):
            open_tweets.open_links(links, batch_size=10)
        self.assertEqual(open_tab.call_count, 20)


if __name__ == "__main__":
    unittest.main()
