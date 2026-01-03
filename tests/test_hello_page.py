import unittest
from pathlib import Path
from html.parser import HTMLParser


class TagCollector(HTMLParser):
    """Simple parser that tracks start tags and text content."""

    def __init__(self):
        super().__init__()
        self.start_tags = []
        self.text_nodes = []

    def handle_starttag(self, tag, attrs):
        attr_map = {name.lower(): value for name, value in attrs}
        self.start_tags.append((tag.lower(), attr_map))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_data(self, data):
        text = data.strip()
        if text:
            self.text_nodes.append(text)


class HelloWorldPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_root = Path(__file__).resolve().parents[1]
        cls.index_path = cls.repo_root / "index.html"
        cls.styles_path = cls.repo_root / "styles.css"
        cls.html_content = cls.index_path.read_text(encoding="utf-8") if cls.index_path.exists() else ""
        cls.parser = TagCollector()
        if cls.html_content:
            cls.parser.feed(cls.html_content)

    def test_index_html_file_exists(self):
        self.assertTrue(self.index_path.exists(), "index.html must exist at the repository root.")

    def test_stylesheet_file_exists(self):
        self.assertTrue(self.styles_path.exists(), "styles.css must exist alongside index.html.")

    def test_has_doctype_and_language(self):
        self.assertIn("<!doctype html", self.html_content.lower(), "HTML5 doctype is required.")
        self.assertIn('<html lang="en">', self.html_content.lower(), "Root html tag should declare lang='en'.")

    def test_meta_tags_for_accessibility_and_responsiveness(self):
        meta_tags = [attrs for tag, attrs in self.parser.start_tags if tag == "meta"]
        has_charset = any(attrs.get("charset", "").lower() == "utf-8" for attrs in meta_tags)
        has_viewport = any(
            attrs.get("name", "").lower() == "viewport"
            and "width=device-width" in attrs.get("content", "").lower()
            for attrs in meta_tags
        )
        self.assertTrue(has_charset, "A UTF-8 meta charset tag should be present.")
        self.assertTrue(has_viewport, "Responsive viewport meta tag should be present.")

    def test_required_semantic_sections_present(self):
        tag_names = {tag for tag, _ in self.parser.start_tags}
        for section in ("header", "main", "section", "footer"):
            with self.subTest(section=section):
                self.assertIn(section, tag_names, f"{section} tag should be used for semantic structure.")

    def test_stylesheet_is_linked(self):
        link_tags = [attrs for tag, attrs in self.parser.start_tags if tag == "link"]
        linked = any(
            attrs.get("rel", "").lower() == "stylesheet" and attrs.get("href") == "styles.css"
            for attrs in link_tags
        )
        self.assertTrue(linked, "styles.css should be linked from index.html.")

    def test_contains_hello_world_copy_and_cta(self):
        combined_text = " ".join(node.lower() for node in self.parser.text_nodes)
        self.assertIn("hello", combined_text)
        self.assertIn("world", combined_text)
        self.assertIn("pantheon", combined_text, "Page copy should reference Pantheon for context.")
        button_tags = [attrs for tag, attrs in self.parser.start_tags if tag == "button"]
        self.assertTrue(button_tags, "A call-to-action button should be present.")

    def test_stylesheet_contains_responsive_rules(self):
        if not self.styles_path.exists():
            self.fail("styles.css must exist for responsive checks.")
        styles = self.styles_path.read_text(encoding="utf-8")
        self.assertIn("@media", styles, "Responsive @media rules are required for mobile support.")
        self.assertIn("font-family", styles, "Base typography styles should be declared.")


if __name__ == "__main__":
    unittest.main()
