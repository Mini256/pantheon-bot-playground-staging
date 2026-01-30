#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


@dataclass(frozen=True)
class CheckFailure:
    message: str


class IndexHtmlInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.seen_tags: set[str] = set()
        self.html_lang: str | None = None
        self.meta_charset: bool = False
        self.meta_viewport: bool = False

        self._in_h1: bool = False
        self._current_h1: list[str] = []
        self.h1_texts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.seen_tags.add(tag)
        attr_map = {key.lower(): (value or "") for key, value in attrs}

        if tag == "html":
            self.html_lang = attr_map.get("lang") or None

        if tag == "meta":
            if "charset" in attr_map:
                self.meta_charset = True
            if attr_map.get("name", "").lower() == "viewport":
                self.meta_viewport = True

        if tag == "h1":
            self._in_h1 = True
            self._current_h1 = []

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag: str) -> None:
        if tag == "h1" and self._in_h1:
            collapsed = " ".join("".join(self._current_h1).split())
            if collapsed:
                self.h1_texts.append(collapsed)
            self._in_h1 = False
            self._current_h1 = []

    def handle_data(self, data: str) -> None:
        if self._in_h1:
            self._current_h1.append(data)


def _fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    index_path = repo_root / "index.html"

    if not index_path.exists():
        _fail("index.html does not exist in the repository root")

    try:
        html = index_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        _fail("index.html is not valid UTF-8")

    if not re.match(r"^\ufeff?\s*<!doctype\s+html\s*>", html, flags=re.IGNORECASE):
        _fail("Missing or invalid HTML5 doctype (expected <!doctype html>)")

    inspector = IndexHtmlInspector()
    inspector.feed(html)
    inspector.close()

    required_tags = {"html", "head", "body", "main", "header", "footer", "title"}
    missing_tags = sorted(required_tags - inspector.seen_tags)
    if missing_tags:
        _fail(f"Missing required semantic tags: {', '.join(missing_tags)}")

    if not inspector.html_lang:
        _fail("Missing required <html lang=\"…\"> attribute")

    if not inspector.meta_charset:
        _fail("Missing <meta charset=\"…\">")

    if not inspector.meta_viewport:
        _fail("Missing mobile-friendly viewport meta tag")

    if "Hello World" not in inspector.h1_texts:
        _fail("Missing required main content heading: <h1>Hello World</h1>")

    print("OK: index.html meets required structure/content checks")


if __name__ == "__main__":
    main()
