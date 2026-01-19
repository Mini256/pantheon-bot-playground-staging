import { describe, it, expect } from 'vitest';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { JSDOM } from 'jsdom';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const htmlPath = resolve(__dirname, '..', 'index.html');
const cssPath = resolve(__dirname, '..', 'styles.css');

const loadDom = () => {
  const markup = readFileSync(htmlPath, 'utf8');
  return new JSDOM(markup);
};

describe('hello world landing page', () => {
  it('renders a titled hero with hello message', () => {
    const dom = loadDom();
    const { document } = dom.window;

    expect(document.title).toBe('Pantheon Hello');

    const heading = document.querySelector('main h1');
    expect(heading).toBeTruthy();
    expect(heading.textContent?.trim()).toBe('Hello, World!');

    const subheading = document.querySelector('main p.subtitle');
    expect(subheading?.textContent?.trim()).toContain('Pantheon bot dev playground');
  });

  it('links the stylesheet and exposes core tokens', () => {
    const dom = loadDom();
    const { document } = dom.window;
    const stylesheet = document.querySelector('link[rel="stylesheet"][href="styles.css"]');

    expect(stylesheet).toBeTruthy();

    const css = readFileSync(cssPath, 'utf8');
    expect(css).toContain(':root');
    expect(css).toMatch(/font-family:\s*"?Inter/);
    expect(css).toMatch(/background:\s*linear-gradient/);
  });
});
