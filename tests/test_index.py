from pathlib import Path
import re
import unittest


HTML_PATH = Path(__file__).resolve().parents[1] / "index.html"


class TestHelloWorldPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html_path = HTML_PATH

    def _read_html(self) -> str:
        if not self.html_path.exists():
            self.fail("Expected index.html to exist in the project root.")
        return self.html_path.read_text(encoding="utf-8")

    def test_index_file_exists(self):
        self.assertTrue(self.html_path.exists(), "index.html must exist at the project root.")

    def test_document_declares_language_and_title(self):
        html_text = self._read_html()
        self.assertIn("<!DOCTYPE HTML>", html_text.upper(), "Document must start with an HTML5 doctype.")
        self.assertRegex(html_text, r"<html[^>]+lang=['\"]en['\"]", "Document should declare lang='en'.")
        self.assertIn(
            "<title>hello world | pantheon playground</title>",
            html_text.lower(),
            "Document title should describe the page.",
        )

    def test_single_hello_world_heading_present(self):
        html_text = self._read_html()
        headings = re.findall(r"<h1[^>]*>(.*?)</h1>", html_text, flags=re.IGNORECASE | re.DOTALL)
        self.assertEqual(len(headings), 1, "Page should contain exactly one primary heading.")
        self.assertEqual(headings[0].strip(), "Hello World", "Primary heading must display 'Hello World'.")

    def test_meta_description_exists(self):
        html_text = self._read_html()
        self.assertRegex(
            html_text,
            r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']',
            "Pages intended for production should include a meta description.",
        )

    def test_call_to_action_copy_present(self):
        html_text = re.sub(r"\s+", " ", self._read_html())
        self.assertIn(
            "Explore the Playground",
            html_text,
            "Landing page should include a clear call-to-action for visitors.",
        )


if __name__ == "__main__":
    unittest.main()
