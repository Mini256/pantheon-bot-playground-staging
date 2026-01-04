from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
HTML_FILE = REPO_ROOT / "index.html"
STYLESHEET = REPO_ROOT / "assets" / "styles.css"


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._tag_stack: list[str] = []
        self.titles: list[str] = []
        self.h1_text: list[str] = []
        self.stylesheets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        self._tag_stack.append(tag)
        attr_dict = dict(attrs)
        if tag == "link" and attr_dict.get("rel") == "stylesheet":
            href = attr_dict.get("href")
            if href:
                self.stylesheets.append(href)

    def handle_endtag(self, tag: str) -> None:
        if self._tag_stack:
            self._tag_stack.pop()

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if not text or not self._tag_stack:
            return
        tag = self._tag_stack[-1]
        if tag == "title":
            self.titles.append(text)
        elif tag == "h1":
            self.h1_text.append(text)


def _read_html() -> str:
    if not HTML_FILE.exists():
        raise FileNotFoundError("index.html is missing")
    return HTML_FILE.read_text(encoding="utf-8")


class TestHelloWorldHomepage(unittest.TestCase):
    def test_html_file_exists(self) -> None:
        self.assertTrue(HTML_FILE.exists(), "Expected index.html at repo root")

    def test_basic_structure(self) -> None:
        content = _read_html()
        self.assertTrue(
            content.lstrip().startswith("<!DOCTYPE html>"),
            "Document should declare HTML5 DOCTYPE at the top",
        )
        self.assertIn("<html lang=\"en\"", content,
                      "Root html tag should include lang attribute for accessibility")
        self.assertIn("<meta charset=\"utf-8\"", content.lower(),
                      "Page should specify utf-8 charset")

    def test_title_and_heading(self) -> None:
        parser = DocumentParser()
        parser.feed(_read_html())
        self.assertIn("Hello World", " ".join(parser.titles),
                      "Title should communicate Hello World")
        self.assertIn("Hello World", " ".join(parser.h1_text),
                      "H1 should prominently display Hello World")

    def test_stylesheet_is_linked_and_present(self) -> None:
        parser = DocumentParser()
        parser.feed(_read_html())
        self.assertIn(
            "assets/styles.css",
            parser.stylesheets,
            "index.html should link to assets/styles.css",
        )
        self.assertTrue(STYLESHEET.exists(), "Stylesheet file should exist")


if __name__ == "__main__":
    unittest.main()
