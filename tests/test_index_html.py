import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = REPO_ROOT / "index.html"


class TestHelloWorldPage(unittest.TestCase):
    def _assert_match(self, pattern: str, text: str, msg: str):
        self.assertIsNotNone(re.search(pattern, text, re.IGNORECASE), msg)

    def _read_html(self) -> str:
        self.assertTrue(HTML_PATH.exists(), "index.html must exist at the repository root")
        return HTML_PATH.read_text(encoding="utf-8")

    def test_index_file_exists(self):
        self.assertTrue(HTML_PATH.exists(), "Expected index.html to be created at the repository root")

    def test_has_required_structure(self):
        content = self._read_html()
        stripped = content.lstrip()
        self.assertTrue(stripped.lower().startswith("<!doctype html>"), "Document must start with the HTML5 doctype")

        self._assert_match(r"<html\b", content, "Missing <html> tag")
        self._assert_match(r"<head\b", content, "Missing <head> tag")
        self._assert_match(r"<body\b", content, "Missing <body> tag")

    def test_has_title_and_body_content(self):
        content = self._read_html()
        self._assert_match(r"<title>[^<]*hello world[^<]*</title>", content, "Title must contain 'Hello World'")
        self._assert_match(r">\s*hello world\b", content, "Body must contain the greeting text")

    def test_has_viewport_meta(self):
        content = self._read_html()
        self._assert_match(r'<meta[^>]*name=["\']viewport["\'][^>]*>', content, "Page should declare a responsive viewport")


if __name__ == "__main__":
    unittest.main()
