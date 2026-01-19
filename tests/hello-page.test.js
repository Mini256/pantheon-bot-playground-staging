import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { JSDOM } from 'jsdom';

const htmlFile = new URL('../public/index.html', import.meta.url);

const loadDocument = () => {
  const markup = readFileSync(htmlFile, 'utf-8');
  return new JSDOM(markup).window.document;
};

describe('hello world page', () => {
  it('sets a descriptive document title', () => {
    const document = loadDocument();
    expect(document.title).toBe('Pantheon Playground · Hello World');
  });

  it('renders the hello world hero copy', () => {
    const document = loadDocument();
    const heading = document.querySelector('h1');
    expect(heading).not.toBeNull();
    expect(heading.textContent?.trim()).toBe('Hello, World!');
  });

  it('exposes the styled hero container class for theming', () => {
    const document = loadDocument();
    const card = document.querySelector('.hello-card');
    expect(card).not.toBeNull();
    expect(card?.classList.contains('hello-card')).toBe(true);
  });
});
