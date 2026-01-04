const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const htmlPath = path.join(process.cwd(), 'index.html');

function readHtml() {
  assert.ok(
    fs.existsSync(htmlPath),
    'index.html should exist at the repository root'
  );
  return fs.readFileSync(htmlPath, 'utf8');
}

test('index.html exists at the repository root', () => {
  assert.ok(fs.existsSync(htmlPath), 'index.html is missing');
});

test('document declares the HTML5 doctype', () => {
  const html = readHtml();
  const normalizedStart = html.trimStart().toLowerCase();
  assert.ok(
    normalizedStart.startsWith('<!doctype html>'),
    'HTML5 doctype declaration should be the first meaningful content'
  );
});

test('document contains required structural tags', () => {
  const html = readHtml();
  assert.match(html, /<html[\s>]/i, 'Missing <html> tag');
  assert.match(html, /<head[\s>]/i, 'Missing <head> tag');
  assert.match(html, /<title>[^<]+<\/title>/i, 'Missing <title> element');
  assert.match(html, /<body[\s>]/i, 'Missing <body> tag');
});

test('page exposes a prominent Hello World heading', () => {
  const html = readHtml();
  assert.match(
    html,
    /<h1[^>]*>\s*Hello World\s*<\/h1>/i,
    'Expected an <h1> with the text "Hello World"'
  );
});

test('visible content is wrapped in a main section', () => {
  const html = readHtml();
  const mainMatch = html.match(/<main[^>]*>([\s\S]*?)<\/main>/i);
  assert.ok(mainMatch, 'Expected content to be wrapped in <main> tags');
  assert.match(
    mainMatch[1],
    /Hello World/i,
    'Main section should include the Hello World text'
  );
});
