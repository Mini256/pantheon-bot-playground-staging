#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def _assert_contains(pattern: str, html: str, *, description: str, flags: int = 0) -> None:
    if re.search(pattern, html, flags) is None:
        _fail(f"missing {description}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Lightweight validation for repo root index.html")
    parser.add_argument(
        "--path",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "index.html",
        help="Path to index.html (defaults to repo root)",
    )
    args = parser.parse_args()

    index_path: Path = args.path
    if not index_path.exists():
        _fail(f"{index_path} does not exist")
    if not index_path.is_file():
        _fail(f"{index_path} is not a file")

    html = index_path.read_text(encoding="utf-8")

    _assert_contains(r"<!doctype\s+html\s*>", html, description="HTML5 doctype", flags=re.IGNORECASE)
    _assert_contains(r"<html\b[^>]*>", html, description="<html> element", flags=re.IGNORECASE)
    _assert_contains(
        r"<html\b[^>]*\blang=[\"'][^\"']+[\"']",
        html,
        description='a lang attribute on <html>',
        flags=re.IGNORECASE,
    )
    _assert_contains(r"<head\b[^>]*>", html, description="<head> element", flags=re.IGNORECASE)
    _assert_contains(r"<body\b[^>]*>", html, description="<body> element", flags=re.IGNORECASE)

    _assert_contains(
        r'<meta\s+name=["\']viewport["\']\s+content=["\'][^"\']*width=device-width',
        html,
        description='responsive viewport meta tag (width=device-width)',
        flags=re.IGNORECASE,
    )

    _assert_contains(r"<main\b[^>]*>", html, description="<main> landmark", flags=re.IGNORECASE)
    _assert_contains(r"<header\b[^>]*>", html, description="<header> landmark", flags=re.IGNORECASE)
    _assert_contains(r"<footer\b[^>]*>", html, description="<footer> landmark", flags=re.IGNORECASE)

    _assert_contains(
        r"<h1\b[^>]*>\s*Hello World\s*</h1>",
        html,
        description='an <h1> containing "Hello World"',
        flags=re.IGNORECASE,
    )

    print("PASS: index.html looks good")


if __name__ == "__main__":
    main()
