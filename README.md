# Mini256-pantheon-bot-dev-playground

## Hello World Webpage Implementation

The landing page lives at `index.html` and is built with plain HTML5 and
embedded CSS to keep the solution lightweight. The document declares the HTML5
doctype, sets `lang="en"`, and defines UTF-8 and responsive viewport meta tags
so screen readers and mobile browsers render the page correctly.

### Design Decisions
- **Semantic layout:** The greeting is wrapped in a `<main>` landmark with an
  `<h1>` and supporting paragraph to provide clear structure for accessibility
  tools.
- **Responsive styling:** Flexbox centering, `min()`/`clamp()` sizing, and a
  mobile media query keep the layout balanced from small phones to desktops
  without extra frameworks.
- **Professional aesthetic:** A subtle gradient background, elevated card, and
  system font stack give a polished look while remaining performant.

### Testing & Validation
- `tests/test_homepage.py` contains unit tests that verify the presence of the
  HTML file, required meta tags, landmarks, and the “Hello World” content.
- Run the suite with `python -m unittest discover tests` before committing to
  ensure regressions are caught early.
