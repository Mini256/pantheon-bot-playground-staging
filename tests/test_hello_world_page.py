import re
import unittest
from pathlib import Path


class TestHelloWorldPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # tests/ -> repo root
        cls.repo_root = Path(__file__).resolve().parents[1]

    def test_index_html_exists(self) -> None:
        self.assertTrue((self.repo_root / "index.html").is_file())

    def test_supporting_assets_exist(self) -> None:
        self.assertTrue((self.repo_root / "assets" / "styles.css").is_file())
        self.assertTrue((self.repo_root / "assets" / "favicon.svg").is_file())

    def test_index_html_contains_expected_content(self) -> None:
        html = (self.repo_root / "index.html").read_text(encoding="utf-8")

        # Basic document metadata for a standalone page.
        self.assertRegex(html.lower(), r"<!doctype html>")
        self.assertRegex(html, r'<meta\s+charset=["\']utf-8["\']\s*/?>', msg="Missing UTF-8 meta tag")
        self.assertIn('name="viewport"', html, msg="Missing viewport meta tag")

        # Content and styling hooks.
        self.assertIn("Hello, world!", html)
        self.assertIn('href="assets/styles.css"', html)

        # Avoid accidental broken HTML where head/body are missing entirely.
        self.assertIsNotNone(re.search(r"<head\b", html, re.IGNORECASE))
        self.assertIsNotNone(re.search(r"<body\b", html, re.IGNORECASE))
