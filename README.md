# Mini256 Pantheon Bot Dev Playground

A minimal, production-ready "Hello World" landing page backing issue #31. The page lives in `index.html`
with companion styles in `assets/styles.css` and highlights the Pantheon Playground brand.

## Running the page

Open `index.html` directly in any modern browser. All assets are local, so no build step is required.

## Tests

Validate the HTML contract enforced by `tests/test_homepage.py` via Python's unittest runner:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

The suite ensures the core structure, title, accessibility metadata, and call-to-action links remain intact.
