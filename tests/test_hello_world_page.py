import unittest
from pathlib import Path


class TestHelloWorldPage(unittest.TestCase):
    def setUp(self) -> None:
        self.repo_root = Path(__file__).resolve().parents[1]

    def test_index_html_exists_and_has_expected_content(self) -> None:
        index_html = self.repo_root / "index.html"
        self.assertTrue(index_html.exists(), "index.html should exist at the repository root")

        content = index_html.read_text(encoding="utf-8")

        # Keep assertions simple and robust; this is a tiny static page.
        self.assertIn("Hello, World!", content)
        self.assertIn("<title>Hello World</title>", content)
        self.assertIn('rel="stylesheet"', content)
        self.assertIn("style.css", content)

    def test_style_css_exists_and_has_basic_styles(self) -> None:
        style_css = self.repo_root / "style.css"
        self.assertTrue(style_css.exists(), "style.css should exist at the repository root")

        css = style_css.read_text(encoding="utf-8")
        self.assertIn("body", css)
        self.assertIn("font-family", css)


if __name__ == "__main__":
    unittest.main()

