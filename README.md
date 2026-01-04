# Mini256 Pantheon Bot Dev Playground

This repository now ships a minimal yet production-ready "Hello World" landing page for issue #31.

## Running the page

Open `index.html` in any modern browser to view the styled page.

## Tests

Use Python's standard library test runner to validate the HTML contract enforced by `tests/test_homepage.py`:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

These tests ensure core accessibility and structure requirements remain intact.
