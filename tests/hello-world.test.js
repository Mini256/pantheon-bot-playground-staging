const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const htmlPath = path.join(__dirname, '..', 'public', 'index.html');

const readHtml = () => fs.readFileSync(htmlPath, 'utf8');

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

test('page defines professional styling rules', () => {
  const html = readHtml();
  const styleMatch = html.match(/<style[^>]*>([\s\S]*?)<\/style>/i);
  assert.ok(styleMatch, 'Expected an inline <style> block for basic styling');
  const css = styleMatch[1];
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
