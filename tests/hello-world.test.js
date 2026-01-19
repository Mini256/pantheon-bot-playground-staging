import { describe, it, expect, beforeAll } from 'vitest';
import { existsSync, readFileSync } from 'node:fs';
import path from 'node:path';
import { JSDOM } from 'jsdom';

const htmlPath = path.join(process.cwd(), 'index.html');

describe('Hello World page', () => {
  it('should exist at the repository root', () => {
    expect(existsSync(htmlPath)).toBe(true);
  });

  describe('structure and presentation', () => {
    let document;

    beforeAll(() => {
      if (!existsSync(htmlPath)) {
        throw new Error('index.html is missing');
      }
      const html = readFileSync(htmlPath, 'utf-8');
      document = new JSDOM(html).window.document;
    });

    it('sets global metadata for accessibility and responsiveness', () => {
      const htmlTag = document.documentElement;
      expect(htmlTag.lang).toBe('en');

      const charset = document.querySelector('meta[charset]');
      expect(charset).not.toBeNull();

      const viewport = document.querySelector('meta[name="viewport"]');
      expect(viewport?.getAttribute('content')).toContain('width=device-width');
    });

    it('shows a prominent Hello World hero heading', () => {
      const heading = document.querySelector('h1');
      expect(heading).not.toBeNull();
      expect(heading?.textContent?.trim()).toBe('Hello World');
    });

    it('includes supportive descriptive copy under the hero', () => {
      const leadParagraph = document.querySelector('p');
      expect(leadParagraph).not.toBeNull();
      expect((leadParagraph?.textContent ?? '').length).toBeGreaterThan(20);
    });

    it('loads styling to create a professional presentation', () => {
      const styles = Array.from(document.querySelectorAll('style, link[rel="stylesheet"]'));
      expect(styles.length).toBeGreaterThan(0);

      const concatenatedStyles = styles
        .map((node) => node.tagName === 'STYLE' ? node.textContent ?? '' : '')
        .join('\n');

      expect(concatenatedStyles).toMatch(/body\s*{/);
    });
  });
});
