from pathlib import Path
import re
import unittest


HTML_PATH = Path(__file__).resolve().parents[1] / "index.html"


class TestIndexHtml(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html_path = HTML_PATH

    def _read_html(self):
        if not self.html_path.exists():
            self.fail("Expected index.html to exist at project root.")
        return self.html_path.read_text(encoding="utf-8")

    def test_index_file_exists(self):
        self.assertTrue(self.html_path.exists(), "index.html must exist in the project root.")

    def test_contains_required_structure(self):
        html_text = self._read_html()
        self.assertIn("<!DOCTYPE HTML>", html_text.upper())
        self.assertRegex(html_text, r"<html[^>]*lang=", msg="Document should declare a language.")
        self.assertIn("<title>", html_text.lower(), "Document needs a title for accessibility.")

    def test_displays_single_hello_world_heading(self):
        html_text = self._read_html()
        headings = re.findall(r"<h1[^>]*>(.*?)</h1>", html_text, flags=re.IGNORECASE | re.DOTALL)
        self.assertEqual(len(headings), 1, "There should be exactly one primary greeting heading.")
        self.assertEqual(headings[0].strip().lower(), "hello world", "Heading must read 'Hello World'.")

    def test_page_mentions_welcome_message(self):
        html_text = self._read_html()
        normalized = re.sub(r"\s+", " ", html_text.lower())
        self.assertIn("welcome", normalized, "Page should include a short welcome/supporting description.")


if __name__ == "__main__":
    unittest.main()
