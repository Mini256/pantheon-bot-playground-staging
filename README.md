# Pantheon Bot Hello World Playground

A single-page "hello world" experience for the Mini256 / Pantheon bot development stories. It is intentionally lightweight: pure HTML + CSS with a tiny automated test suite to guarantee the key UI elements stay present.

## Getting started

```bash
npm install
npm run dev  # serves the static page on http://localhost:4173
```

You can also open `index.html` directly in any modern browser if you do not want to run a local server.

## Testing

```bash
npm test
```

The Vitest + JSDOM spec checks that the document title, hero copy, and call-to-action button are rendered as expected.

## Implementation notes

- Static HTML keeps footprint low while still enabling modern styling via gradients, glassmorphism, and responsive typography.
- A short `serve` script offers a zero-config way to preview the page without any build tooling.
- Vitest with JSDOM gives us a deterministic safety net that the hello world copy and CTA remain intact.
