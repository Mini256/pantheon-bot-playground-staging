import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PAGE_PATH = REPO_ROOT / "hello-world.html"


class HelloWorldPageTest(unittest.TestCase):
    def read_page_text(self) -> str:
        if not PAGE_PATH.exists():
            self.fail("hello-world.html must exist before reading.")
        return PAGE_PATH.read_text(encoding="utf-8")

    def test_page_file_exists(self) -> None:
        self.assertTrue(
            PAGE_PATH.exists(),
            "Expected hello-world.html to exist at the repository root.",
        )

    def test_has_doctype_and_meta(self) -> None:
        lower_html = self.read_page_text().lower()
        self.assertIn("<!doctype html>", lower_html, "Missing HTML5 doctype.")
        self.assertIn('name="viewport"', lower_html, "Viewport meta tag missing.")
        self.assertIn('name="description"', lower_html, "Description meta tag missing.")

    def test_has_accessible_structure(self) -> None:
        lower_html = self.read_page_text().lower()
        self.assertIn("<main", lower_html, "Main landmark is required for accessibility.")
        self.assertIn("<header", lower_html, "Header landmark missing.")
        self.assertIn("<footer", lower_html, "Footer landmark missing.")

    def test_displays_hello_world_heading(self) -> None:
        heading_match = re.search(
            r"<h1[^>]*>\s*hello world\s*</h1>",
            self.read_page_text(),
            flags=re.IGNORECASE,
        )
        self.assertIsNotNone(heading_match, "Page should feature a Hello World heading.")

    def test_skip_link_points_to_main_content(self) -> None:
        html = self.read_page_text().lower()
        self.assertIn('class="skip-link"', html, "Skip link should be present for accessibility.")
        self.assertIn('href="#page-title"', html, "Skip link should jump directly to the main heading.")

    def test_section_is_labelled_by_heading(self) -> None:
        html = self.read_page_text()
        self.assertIn(
            'aria-labelledby="page-title"',
            html,
            "Primary section should reference the Hello World heading for screen readers.",
        )
        self.assertIn('id="page-title"', html, "Hello World heading must supply the aria-labelledby target.")


if __name__ == "__main__":
    unittest.main()
