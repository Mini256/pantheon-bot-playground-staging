import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { JSDOM } from 'jsdom';

const html = readFileSync(resolve('index.html'), 'utf-8');
const dom = new JSDOM(html);
const { document } = dom.window;

describe('hello world page', () => {
  it('renders the document title', () => {
    expect(document.title).toBe('Hello from Pantheon');
  });

  it('has a hero heading and supporting copy', () => {
    const heading = document.querySelector('h1');
    expect(heading).toBeTruthy();
    expect(heading?.textContent).toMatch(/hello, world/i);

    const paragraph = document.querySelector('p');
    expect(paragraph?.textContent?.trim().length).toBeGreaterThan(10);
  });

  it('shows an action button for interaction', () => {
    const button = document.querySelector('button');
    expect(button).toBeTruthy();
    expect(button?.textContent).toMatch(/explore/i);
  });
});
