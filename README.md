# Mini256 · Pantheon Bot Dev Playground

## Overview
A tiny, self-contained hello world webpage that showcases a clean, modern layout using only static HTML/CSS plus a lightweight Node toolchain for local serving and automated tests (Vitest + JSDOM).

## Prerequisites
- Node.js 18+ (tested with v24)
- npm (ships with Node)

## Getting Started
```bash
npm install
```

### Run the page locally
```bash
npm run dev
```
This launches a simple static server on `http://localhost:4173`. Alternatively, open `public/index.html` directly in your browser.

### Run tests
```bash
npm test
```
Vitest reads the generated HTML via JSDOM and checks the title, hero copy, and key layout hooks.

## Project Structure
```
public/
  index.html      # Hello World page with embedded styles
tests/
  hello-page.test.js  # DOM-level regression checks
package.json      # npm scripts plus dev tooling config
```

## Implementation Notes
- Static HTML keeps the stack minimal while still offering responsive styling (Inter font, centered hero card, soft gradients).
- `serve` provides a zero-config dev server for quick previews.
- Vitest + JSDOM ensure core content and structure remain intact as changes are made.
