"""Sanity checks for the hello world page described in issue #26."""

from __future__ import annotations

from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = REPO_ROOT / "index.html"


class IndexHtmlTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if INDEX_PATH.exists():
            cls.contents = INDEX_PATH.read_text(encoding="utf-8")
        else:
            cls.contents = ""
        cls.contents_lower = cls.contents.lower()

    def test_index_exists(self) -> None:
        self.assertTrue(INDEX_PATH.exists(), "index.html must exist in the repo root")

    def test_has_basic_html5_structure(self) -> None:
        stripped = self.contents_lower.lstrip()
        self.assertTrue(
            stripped.startswith("<!doctype html>"),
            "Document should begin with an HTML5 doctype",
        )
        for tag in ("<html", "<head", "<title", "<body"):
            self.assertIn(tag, self.contents_lower, f"Expected {tag} tag in document")

    def test_has_title_and_hello_world_text(self) -> None:
        match = re.search(r"<title>\s*([^<]+)\s*</title>", self.contents, re.IGNORECASE)
        self.assertIsNotNone(match, "Title tag with text is required")
        title_text = match.group(1).strip()
        self.assertGreater(len(title_text), 0, "Title text should not be empty")
        self.assertIn("hello world", self.contents_lower, "Body should include 'Hello World'")

    def test_has_basic_styling(self) -> None:
        self.assertRegex(
            self.contents_lower,
            r"<style[\s>]+",
            "Inline <style> block required for basic visual design",
        )

    def test_has_viewport_meta_for_responsiveness(self) -> None:
        self.assertRegex(
            self.contents_lower,
            r"<meta[^>]+name=\"viewport\"",
            "Viewport meta tag required for responsive layout",
        )


if __name__ == "__main__":
    unittest.main()
