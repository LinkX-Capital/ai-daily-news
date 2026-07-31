import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import publish


VALID_MD = """# AI 前沿动态

### 产业动态

**公司发布经过验证的新系统**

公司发布了一项经过验证的新系统。该系统目前面向指定场景开放。

> 💡 这项进展值得持续观察。

- 来源: [Example](https://example.com/item)
"""


class ManualPublishTests(unittest.TestCase):
    def _patch_paths(self, root):
        return (
            patch.object(publish, "BASE_DIR", root),
            patch.object(publish, "ARCHIVE_DIR", root / "archive"),
            patch.object(
                publish,
                "MANIFEST_DIR",
                root / "archive" / "manifests",
            ),
        )

    def test_manual_release_is_gated_and_prepares_ready_manifest(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            report_date = "2026-07-28"
            (root / f"daily-ai-news-{report_date}.md").write_text(
                VALID_MD,
                encoding="utf-8",
            )

            def render_stub(*args, **kwargs):
                (root / f"daily-ai-news-{report_date}.html").write_text(
                    "<html>validated</html>",
                    encoding="utf-8",
                )

            path_patches = self._patch_paths(root)
            with path_patches[0], path_patches[1], path_patches[2], patch(
                "publish.subprocess.run",
                side_effect=render_stub,
            ) as rendered:
                manifest_path = publish.prepare_manual_release(report_date)

            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            archive = json.loads(
                (root / "archive" / f"news_{report_date}.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(manifest["status"], "ready")
            self.assertEqual(manifest["article_count"], 1)
            self.assertTrue(manifest["qa"]["canonical"]["passed"])
            self.assertEqual(archive["count"], 1)
            self.assertTrue(archive["articles"][0]["candidate_id"])
            self.assertEqual(
                archive["articles"][0]["provenance"]["writing"],
                "human_edited",
            )
            rendered.assert_called_once()

    def test_manual_release_failure_writes_qa_failed_without_side_effects(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            report_date = "2026-07-28"
            invalid_md = VALID_MD.replace(
                "公司发布了一项经过验证的新系统。该系统目前面向指定场景开放。",
                "This is raw English source copy and it was never edited.",
            )
            (root / f"daily-ai-news-{report_date}.md").write_text(
                invalid_md,
                encoding="utf-8",
            )

            path_patches = self._patch_paths(root)
            with path_patches[0], path_patches[1], path_patches[2], patch(
                "publish.subprocess.run"
            ) as rendered:
                with self.assertRaisesRegex(RuntimeError, "未通过"):
                    publish.prepare_manual_release(report_date)

            manifest = json.loads(
                (
                    root
                    / "archive"
                    / "manifests"
                    / f"{report_date}.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["status"], "qa_failed")
            self.assertFalse(
                manifest["qa"]["canonical"]["passed"]
            )
            self.assertFalse(
                (root / "archive" / f"news_{report_date}.json").exists()
            )
            rendered.assert_not_called()

    def test_html_failure_cannot_leave_manual_release_ready(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            report_date = "2026-07-28"
            (root / f"daily-ai-news-{report_date}.md").write_text(
                VALID_MD,
                encoding="utf-8",
            )

            path_patches = self._patch_paths(root)
            with path_patches[0], path_patches[1], path_patches[2], patch(
                "publish.subprocess.run",
                side_effect=OSError("simulated renderer failure"),
            ):
                with self.assertRaisesRegex(OSError, "renderer failure"):
                    publish.prepare_manual_release(report_date)

            manifest = json.loads(
                (
                    root
                    / "archive"
                    / "manifests"
                    / f"{report_date}.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["status"], "qa_failed")
            self.assertEqual(
                manifest["failure"]["type"],
                "OSError",
            )


if __name__ == "__main__":
    unittest.main()
