import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "index.html"


class HelloWorldPageTest(unittest.TestCase):
    def _read_html(self) -> str:
        if not HTML_PATH.exists():
            self.fail("Expected index.html to exist at the repository root.")
        return HTML_PATH.read_text(encoding="utf-8")

    def test_index_html_exists(self):
        self.assertTrue(
            HTML_PATH.exists(),
            "index.html should be present at the repository root.",
        )

    def test_declares_html5_doctype_and_language(self):
        html = self._read_html().lower()
        self.assertIn("<!doctype html>", html, "Missing HTML5 doctype.")
        self.assertIn(
            'lang="en"', html, "Document should set lang attribute for accessibility."
        )

    def test_has_required_meta_tags(self):
        html = self._read_html().lower()
        self.assertIn('charset="utf-8"', html, "Document should define UTF-8 charset.")
        self.assertIn(
            'name="viewport"', html, "Viewport meta tag required for responsiveness."
        )

    def test_contains_semantic_structure_and_content(self):
        html = self._read_html().lower()
        self.assertIn("<main", html, "Main landmark should wrap the primary content.")
        self.assertIn("<h1", html, "Primary heading is required.")
        self.assertIn("hello world", html, "Page should prominently say 'Hello World'.")


if __name__ == "__main__":
    unittest.main()
