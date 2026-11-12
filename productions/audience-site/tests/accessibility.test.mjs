import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const html=fs.readFileSync(new URL('../src/index.html',import.meta.url),'utf8');
const css=fs.readFileSync(new URL('../src/styles.css',import.meta.url),'utf8');
const app=fs.readFileSync(new URL('../src/app.js',import.meta.url),'utf8');

test('document exposes skip navigation and labeled menu controls',()=>{
  assert.ok(html.includes('class="skip" href="#main"'));
  assert.ok(html.includes('aria-expanded="false"'));
  assert.ok(html.includes('aria-controls="navigation"'));
  assert.ok(html.includes('main id="main" tabindex="-1"'));
});

test('focus and reduced-motion contracts are present',()=>{
  assert.ok(css.includes(':focus-visible'));
  assert.ok(css.includes('@media(prefers-reduced-motion:reduce)'));
  assert.ok(css.includes('@media(max-width:740px)'));
});

test('primary interactive controls meet 44px target recommendation',()=>{
  assert.ok(css.includes('.menu,.button,.location-button,nav a{min-height:44px'));
});

test('map and menu keyboard paths are explicit',()=>{
  assert.ok(app.includes("e.key==='Enter'||e.key===' '"));
  assert.ok(app.includes("e.key==='Escape'"));
});

test('public shell has no edit or credential controls',()=>{
  const lower=(html+app).toLowerCase();
  for(const token of ['password','api_key','secret_key','edit canon','publish now']) assert.equal(lower.includes(token),false);
});
