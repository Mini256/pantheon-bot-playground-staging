const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const htmlPath = path.join(__dirname, '..', 'public', 'index.html');

const readHtml = () => fs.readFileSync(htmlPath, 'utf8');
const readStyles = () => {
  const html = readHtml();
  const styleMatch = html.match(/<style[^>]*>([\s\S]*?)<\/style>/i);
  assert.ok(styleMatch, 'Expected inline <style> block for base styling');
  return styleMatch[1];
};

test('hello world page exists', () => {
  assert.ok(fs.existsSync(htmlPath), `Expected ${htmlPath} to exist`);
});

test('page contains a prominent Hello World heading', () => {
  const html = readHtml();
  const headingMatch = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i);
  assert.ok(headingMatch, 'Expected an <h1> element');
  assert.match(
    headingMatch[1],
    /hello world/i,
    'Expected the primary heading to contain "Hello World"'
  );
});

test('hero region is connected to its heading for accessibility', () => {
  const html = readHtml();
  const heroSectionMatch = html.match(/<section[^>]*class="[^"]*hero-card[^"]*"[^>]*>/i);
  assert.ok(heroSectionMatch, 'Expected a hero section with the hero-card class');
  assert.match(
    heroSectionMatch[0],
    /aria-labelledby="hero-title"/i,
    'Hero section should reference the primary heading'
  );

  const headingMatch = html.match(/<h1[^>]*id="hero-title"[^>]*>([\s\S]*?)<\/h1>/i);
  assert.ok(
    headingMatch,
    'Expected the primary heading to expose id="hero-title" for aria-labelledby'
  );
});

test('tagline reinforces Pantheon playground context', () => {
  const html = readHtml();
  const taglineMatch = html.match(/<p[^>]*data-testid="tagline"[^>]*>([\s\S]*?)<\/p>/i);
  assert.ok(taglineMatch, 'Expected a tagline paragraph with data-testid="tagline"');
  const text = taglineMatch[1];
  assert.match(text, /Pantheon/i, 'Tagline should mention Pantheon');
  assert.match(text, /playground/i, 'Tagline should mention the playground context');
});

test('feature list highlights key experience pillars', () => {
  const html = readHtml();
  const featureListMatch = html.match(/<ul[^>]*class="[^"]*feature-list[^"]*"[^>]*>([\s\S]*?)<\/ul>/i);
  assert.ok(featureListMatch, 'Expected a feature list with the feature-list class');
  const listItems = [...featureListMatch[1].matchAll(/<li[^>]*>([\s\S]*?)<\/li>/gi)];
  assert.ok(listItems.length >= 2, 'Feature list should call out at least two highlights');
  assert.ok(
    listItems.some(([, copy]) => /responsive/i.test(copy)),
    'Feature list should mention responsive layout'
  );
  assert.ok(
    listItems.some(([, copy]) => /accessible|accessibility/i.test(copy)),
    'Feature list should mention accessibility'
  );
});

test('page defines professional styling rules', () => {
  const css = readStyles();
  assert.match(
    css,
    /body\s*{[\s\S]*?font-family:/i,
    'Body styles should set a modern font-family'
  );
  assert.match(
    css,
    /\.hero-card[\s\S]*box-shadow/i,
    'Hero card styles should include a subtle box shadow'
  );
});

test('global styles declare a reusable gradient token and motion-safe fallbacks', () => {
  const css = readStyles();
  assert.match(
    css,
    /--brand-gradient:\s*linear-gradient/i,
    'Styles should define a --brand-gradient custom property'
  );
  assert.match(
    css,
    /@media\s*\(prefers-reduced-motion:\s*reduce\)[\s\S]*?{[\s\S]*?}/i,
    'Styles should include reduced-motion safeguards'
  );
});
