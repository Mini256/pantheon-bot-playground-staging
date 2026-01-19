# Mini256-pantheon-bot-dev-playground

## Hello World Page

This repo now contains a minimal, modern hello world landing page that can be opened directly in any browser. It uses plain HTML/CSS plus a tiny Vitest suite to guard against regressions.

### Prerequisites

- [Node.js 18+](https://nodejs.org/) (for running the tests)

### Setup & Tests

```bash
npm install
npm test
```

### View the Page

You can open `index.html` directly in your browser, or serve the folder locally:

```bash
python3 -m http.server 4173
# visit http://localhost:4173
```

### Project Structure

- `index.html` – semantic markup with hero content and CTA.
- `styles.css` – glassmorphic styling, gradients, and typography tokens.
- `tests/hello.test.js` – Vitest + JSDOM assertions for the greeting and styles.
- `worklog.md` – notes on context verification, design, and implementation decisions.
