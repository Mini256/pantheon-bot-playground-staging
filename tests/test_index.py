import unittest
from html.parser import HTMLParser
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HTML_FILE = REPO_ROOT / "index.html"


class TagCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.start_tags = []

    def handle_starttag(self, tag, attrs):
        self.start_tags.append(tag)


class MainContentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_main = False
        self.in_h1 = False
        self.main_chunks = []
        self.heading_chunks = []
        self.heading_in_main = False

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.in_main = True
        if tag == "h1":
            self.in_h1 = True
            if self.in_main:
                self.heading_in_main = True

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
        if tag == "h1":
            self.in_h1 = False

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self.in_main:
            self.main_chunks.append(text)
        if self.in_h1:
            self.heading_chunks.append(text)

    @property
    def main_text(self):
        return " ".join(self.main_chunks).strip()

    @property
    def primary_heading(self):
        return " ".join(self.heading_chunks).strip()


class TestIndexHtml(unittest.TestCase):
    def test_index_html_exists(self):
        self.assertTrue(HTML_FILE.exists(), "index.html should exist at the repository root")

    def test_has_html5_doctype(self):
        self.assertTrue(HTML_FILE.exists(), "index.html is missing")
        html = HTML_FILE.read_text(encoding="utf-8")
        self.assertTrue(html.lstrip().lower().startswith("<!doctype html>"), "Document must start with <!DOCTYPE html>")

    def test_contains_required_tags(self):
        self.assertTrue(HTML_FILE.exists(), "index.html is missing")
        html = HTML_FILE.read_text(encoding="utf-8")
        parser = TagCollector()
        parser.feed(html)
        for tag in ("html", "head", "title", "body", "main", "h1"):
            self.assertIn(tag, parser.start_tags, f"<{tag}> tag is required for the hello world page")
        self.assertTrue(html.rstrip().lower().endswith("</html>"), "Document should close with </html>")

    def test_main_displays_hello_world(self):
        self.assertTrue(HTML_FILE.exists(), "index.html is missing")
        html = HTML_FILE.read_text(encoding="utf-8")
        parser = MainContentParser()
        parser.feed(html)
        self.assertTrue(parser.main_text, "<main> should include visible content")
        self.assertIn("hello world", parser.main_text.lower(), "Main content should include 'Hello World'")
        self.assertTrue(parser.heading_in_main, "Primary heading should live inside <main>")
        self.assertEqual(parser.primary_heading.lower(), "hello world", "Primary heading should be 'Hello World'")

    def test_document_is_clean_and_simple(self):
        self.assertTrue(HTML_FILE.exists(), "index.html is missing")
        html = HTML_FILE.read_text(encoding="utf-8")
        parser = TagCollector()
        parser.feed(html)
        self.assertNotIn("script", parser.start_tags, "Page should remain static without scripts for simplicity")
        whitespace_ratio = html.count("\n") / max(len(html), 1)
        self.assertLess(whitespace_ratio, 0.3, "Document should remain concise without unnecessary whitespace noise")


if __name__ == "__main__":
    unittest.main()
