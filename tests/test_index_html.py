import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


class _AuditParser(HTMLParser):
    """Lightweight HTML checks without external dependencies."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[tuple[str, dict[str, str]]] = []
        self.meta: list[dict[str, str]] = []
        self._in_title = False
        self.title_text: list[str] = []
        self.text_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {k: (v or "") for k, v in attrs}
        self.tags.append((tag.lower(), attrs_dict))
        if tag.lower() == "meta":
            self.meta.append(attrs_dict)
        if tag.lower() == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            if data.strip():
                self.title_text.append(data.strip())
        self.text_chunks.append(data)


class TestHelloWorldPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = Path(__file__).resolve().parents[1]
        cls.index_path = cls.repo_root / "index.html"
        cls.styles_path = cls.repo_root / "styles.css"

    def test_index_html_exists(self) -> None:
        self.assertTrue(self.index_path.exists(), "index.html should exist at the repo root")

    def test_doctype_present(self) -> None:
        content = self.index_path.read_text(encoding="utf-8")
        self.assertRegex(content, r"(?is)<!doctype\s+html\s*>", "HTML5 doctype should be present")

    def test_basic_structure_and_meta(self) -> None:
        content = self.index_path.read_text(encoding="utf-8")
        parser = _AuditParser()
        parser.feed(content)

        html_tags = [attrs for tag, attrs in parser.tags if tag == "html"]
        self.assertTrue(html_tags, "<html> tag should exist")
        self.assertTrue(html_tags[0].get("lang"), "<html> should declare a language via lang attribute")

        # Required meta tags (HTML5 baseline).
        has_charset = any("charset" in m and m["charset"].strip() for m in parser.meta)
        self.assertTrue(has_charset, "Document should include <meta charset=...>")

        viewport = [
            m
            for m in parser.meta
            if m.get("name", "").lower() == "viewport" and "width=device-width" in m.get("content", "")
        ]
        self.assertTrue(viewport, "Document should include a responsive viewport meta tag")

        self.assertTrue(parser.title_text, "<title> should be present and non-empty")

    def test_semantic_elements_present(self) -> None:
        content = self.index_path.read_text(encoding="utf-8")
        parser = _AuditParser()
        parser.feed(content)
        tags = {t for t, _ in parser.tags}

        for required in ("header", "main", "footer"):
            self.assertIn(required, tags, f"Expected semantic <{required}> element")

    def test_hello_world_visible(self) -> None:
        content = self.index_path.read_text(encoding="utf-8")
        self.assertRegex(
            content,
            r"(?is)<h1[^>]*>\s*hello\s+world\s*</h1>",
            "Page should render an <h1>Hello World</h1>",
        )

    def test_stylesheet_linked_and_nontrivial(self) -> None:
        content = self.index_path.read_text(encoding="utf-8")
        self.assertRegex(
            content,
            r'(?is)<link[^>]+rel=["\']stylesheet["\'][^>]+href=["\']styles\.css["\']',
            "index.html should link to styles.css",
        )

        self.assertTrue(self.styles_path.exists(), "styles.css should exist at the repo root")
        css = self.styles_path.read_text(encoding="utf-8")
        self.assertGreater(len(css.strip()), 200, "styles.css should contain meaningful styling")
        self.assertIn("clamp(", css, "Use modern responsive sizing (e.g., clamp())")


if __name__ == "__main__":
    unittest.main()
