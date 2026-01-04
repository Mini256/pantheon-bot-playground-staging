from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import unittest

REPO_ROOT = Path(__file__).resolve().parents[1]
HTML_FILE = REPO_ROOT / "index.html"
STYLESHEET = REPO_ROOT / "assets" / "styles.css"


class DocumentParser(HTMLParser):
    """Collects structural information while parsing the document."""

    def __init__(self) -> None:
        super().__init__()
        self._open_tags: list[str] = []
        self.titles: list[str] = []
        self.h1_text: list[str] = []
        self.links: list[dict[str, str]] = []
        self.stylesheets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        self._open_tags.append(tag)
        attr_dict = dict(attrs)
        if tag == "a":
            self.links.append(attr_dict)
        if tag == "link" and attr_dict.get("rel") == "stylesheet":
            href = attr_dict.get("href")
            if href:
                self.stylesheets.append(href)

    def handle_endtag(self, tag: str) -> None:
        if self._open_tags:
            self._open_tags.pop()

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if not text or not self._open_tags:
            return
        tag = self._open_tags[-1]
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
            "Document should include an HTML5 doctype",
        )
        self.assertIn('<html lang="en"', content,
                      "Root html tag should carry a lang attribute")
        self.assertIn('<meta charset="utf-8"', content.lower(),
                      "Page should define utf-8 encoding")

    def test_title_heading_and_stylesheet(self) -> None:
        parser = DocumentParser()
        parser.feed(_read_html())
        joined_title = " ".join(parser.titles)
        joined_h1 = " ".join(parser.h1_text)
        self.assertIn("Hello World", joined_title,
                      "Title should mention Hello World")
        self.assertIn("Hello World", joined_h1,
                      "Primary heading should announce Hello World")
        self.assertIn("assets/styles.css", parser.stylesheets,
                      "Main stylesheet must be linked")
        self.assertTrue(STYLESHEET.exists(), "Stylesheet file should exist")

    def test_primary_links_exist(self) -> None:
        parser = DocumentParser()
        parser.feed(_read_html())
        hrefs = {link.get("href"): link for link in parser.links}
        self.assertIn(
            "https://github.com/Mini256/pantheon-bot-dev-playground",
            hrefs,
            "CTA should point to the GitHub repository",
        )
        self.assertIn(
            "mailto:hello@pantheon.dev",
            hrefs,
            "CTA should expose the contact email",
        )


if __name__ == "__main__":
    unittest.main()
