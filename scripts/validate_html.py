#!/usr/bin/env python3
"""Minimal structural checks for the Hello World HTML page."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX_FILE = REPO_ROOT / "index.html"


def main() -> int:
    errors: list[str] = []

    if not INDEX_FILE.exists():
        errors.append(f"Missing {INDEX_FILE.name} at repo root.")
    else:
        content = INDEX_FILE.read_text(encoding="utf-8")
        lowered = content.lower()
        if "<!doctype html>" not in lowered:
            errors.append("Missing HTML5 doctype declaration.")
        if not re.search(r"<html\b[^>]*\blang=", content, re.IGNORECASE):
            errors.append("Root <html> element must declare a lang attribute.")
        if "Hello World" not in content:
            errors.append("Page must prominently display 'Hello World'.")

    if errors:
        print("HTML validation failed:")
        for err in errors:
            print(f" - {err}")
        return 1

    print("HTML validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
