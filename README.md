# Mini256-pantheon-bot-dev-playground

## Hello World Webpage

This repository hosts a production-ready `index.html` that showcases a polished “Hello World” experience for the Pantheon bot playground. The page is a single, portable asset with semantic markup, accessibility-minded structure, and lightweight inline styles so it can be deployed from any static host without extra tooling.

## Implementation Approach

- Crafted a standards-compliant HTML5 document with descriptive metadata, a single `h1` greeting, and supportive copy that clarifies the page’s purpose.
- Added responsive, theme-aware styling directly in the document head (including light/dark support and reduced-motion handling) to keep the asset self-contained yet professional.
- Introduced regression tests (`tests/test_index.py`) to enforce the document contract: file presence, language declaration, metadata, and the single “Hello World” heading plus CTA copy.

## Testing

- `python3 -m unittest` – verifies the HTML structure and key content markers (passing).
