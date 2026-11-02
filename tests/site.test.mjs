import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import test from 'node:test';
import { buildSite, loadNote, loadScript } from '../lib/pages.mjs';
import { jsonText, linkPolicy, markdown, plainText, scriptSummary } from '../lib/render.mjs';

const root = new URL('../', import.meta.url);
const read = path => readFileSync(new URL(path, root), 'utf8');
const selection = JSON.parse(read('data/selection.json'));
const reasoning = JSON.parse(read('data/reasoning.json'));
const provenance = JSON.parse(read('data/provenance.json'));
const notes = selection.notes.map(name => loadNote(name, read(`data/notes/${name}`)));
const scripts = selection.scripts.map(name => loadScript(name, read(`data/scripts/${name}`)));
const files = buildSite({ reasoning, provenance, notes, scripts });
const pages = [...files].filter(([path]) => path.endsWith('.html') && !path.startsWith('scripts/code/'));
const decode = html => html.replace(/<[^>]+>/g, '').replace(/&(lt|gt|quot|#x27|#39|amp);/g, (_, e) => ({ lt: '<', gt: '>', quot: '"', '#x27': "'", '#39': "'", amp: '&' })[e]);

test('committed pages are the deterministic build of the committed data', () => {
  for (const [path, content] of files) assert.equal(read(path), content, `${path}: run npm run build`);
  for (const dir of ['reasoning', 'notes', 'scripts/code', 'scripts/source']) {
    const count = readdirSync(new URL(`${dir}/`, root), { recursive: true }).filter(name => /\.(html|txt)$/.test(name)).length;
    assert.equal(count, [...files.keys()].filter(path => path.startsWith(`${dir}/`)).length, `${dir} has no stale files`);
  }
});

test('reasoning keeps every timestamped message and nothing but the messages', () => {
  assert.equal(reasoning.tasks.length, 31);
  assert.equal(reasoning.tasks.reduce((n, t) => n + t.messages.length, 0), provenance.counts.messages);
  for (const task of reasoning.tasks) {
    assert.ok(task.messages.length > 0, `task ${task.n}`);
    for (const [i, m] of task.messages.entries()) {
      assert.match(m.time, /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}-04:00$/);
      if (i) assert.ok(m.time >= task.messages[i - 1].time, `task ${task.n} message ${i + 1} is in order`);
    }
  }
  // Prompts, steers and tool lines stay private.
  const published = read('data/reasoning.json') + pages.filter(([p]) => p.startsWith('reasoning/')).map(([, html]) => html).join('');
  for (const leak of ['] PROMPT:', '] STEER:', '] TOOLS:', 'You are going to be playing Pokemon Reborn', 'Searched files:', 'Read files/logs:']) assert.ok(!published.includes(leak), leak);
  const page = files.get('reasoning/01/index.html');
  assert.match(page, /<li class="message" id="m1"><a class="message-time" href="#m1"><time datetime="2026-09-19T13:45:53-04:00">13:45:53<\/time><\/a>/);
});

test('the selection holds planning notes and gameplay scripts, not media work or copied guides', () => {
  assert.equal(notes.length, 195);
  assert.equal(scripts.length, 1197);
  for (const name of selection.notes) assert.doesNotMatch(name, /walkthrough|-status\.json$|-navigation\.json$|battle-log|media|render|idle|framing|timestamps|capture-log|archive|publish|music|bgm|video/i, name);
  for (const name of selection.scripts) assert.doesNotMatch(name, /^(render|revise\d+_media|rotate\d|audit_|clean_video|bgm|video_|window_record|record_session|qa_|publish|export|trim_|scan_idle|refine_idle|review_idle)/i, name);
  for (const kind of ['notes', 'scripts']) for (const name of selection[kind]) assert.ok(provenance.placements[kind][name], `${kind}/${name} has a task`);
  const text = [...notes.map(n => n.source), ...scripts.map(s => s.source)].join('\n');
  assert.doesNotMatch(text, /sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|BEGIN [A-Z ]*PRIVATE KEY|drive\.google\.com/);
});

test('every highlighted script keeps its exact source text', () => {
  for (const script of scripts) {
    const html = files.get(`scripts/code/${script.name}.html`);
    const code = /<code class="hljs[^"]*">([\s\S]*)<\/code><\/pre>/.exec(html)?.[1];
    assert.ok(code !== undefined, script.name);
    assert.equal(decode(code), script.source, script.name);
    assert.equal(files.get(`scripts/source/${script.name}.txt`), script.source);
    assert.match(html, /<meta name="robots" content="noindex">/);
    assert.match(html, new RegExp(`<pre class="ui-code" data-fragment tabindex="0" aria-label="Source of ${script.name.replace(/[.]/g, '\\.')}">`));
  }
});

test('notes keep their content: JSON data is unchanged and text keeps its words', () => {
  for (const note of notes.filter(n => n.kind === 'json')) assert.deepEqual(JSON.parse(jsonText(note.source)), JSON.parse(note.source), note.name);
  for (const note of notes) assert.match(files.get(`notes/${note.name}.html`), /<article class="note-body" data-fragment>/, note.name);
  const sample = notes.find(n => n.kind === 'text');
  const words = sample.source.match(/[A-Za-z]{6,}/g).slice(0, 20);
  for (const word of words) assert.ok(files.get(`notes/${sample.name}.html`).includes(word), word);
});

test('Markdown is escaped and only web links or published files become links', () => {
  const resolve = linkPolicy({ notes: new Map([['gym-03-plan.md', '/pokemon-reborn/notes/gym-03-plan.md.html']]), scripts: new Set(['nav.py']), scriptHref: n => `/pokemon-reborn/scripts/#${n}` });
  const render = markdown({ headingOffset: 1, resolve });
  const html = render('# Plan\n\nSee <script>alert(1)</script> [guide](https://bigjra.github.io/reborn/) [video](</Users/jw/Desktop/bin/reborn/gym-10-game-4x-bgm.mp4>) [note](notes/gym-03-plan.md) [code](scripts/nav.py) ![x](a.png)');
  assert.match(html, /<h2>Plan<\/h2>/);
  assert.match(html, /&lt;script&gt;alert\(1\)&lt;\/script&gt;/);
  assert.match(html, /<a href="https:\/\/bigjra\.github\.io\/reborn\/">guide<\/a>/);
  assert.doesNotMatch(html, /href="[^"]*(?:Users|\.mp4)/);
  assert.match(html, /<a href="\/pokemon-reborn\/notes\/gym-03-plan\.md\.html">note<\/a>/);
  assert.match(html, /<a href="\/pokemon-reborn\/scripts\/#nav\.py">code<\/a>/);
  assert.doesNotMatch(html, /<img|<script/);
  // Inline tags stay visible as escaped text around the rendered Markdown.
  assert.equal(render('<b>[x](https://a.example/)</b>').trim(), '<p>&lt;b&gt;<a href="https://a.example/">x</a>&lt;/b&gt;</p>');
  assert.equal(plainText('one <b>\ntwo\n\nhttps://x.example/a'), '<p>one &lt;b&gt;\ntwo</p>\n<p><a href="https://x.example/a">https://x.example/a</a></p>');
  assert.equal(scriptSummary('a.py', '#!/usr/bin/env python3\n"""Enter a fight.\n\nMore."""\nimport os\n'), 'Enter a fight.');
});

test('pages share the site frame, identity and canonical routes', () => {
  for (const [path, html] of pages) {
    assert.match(html, /<link rel="canonical" href="https:\/\/jehlp\.net\/pokemon-reborn\/[^"]*">/, path);
    assert.match(html, /<a class="skip-link" href="#main">/, path);
    assert.match(html, /<img class="site-mark" src="https:\/\/jehlp\.net\/site-theme\/v2\/marks\/pokemon-reborn\.png" width="32" height="32" alt=""><span class="site-title">Pokémon Reborn<\/span>/, path);
    assert.match(html, /<span class="site-utility-pair"><a class="site-home" href="https:\/\/jehlp\.net\/"/, path);
    assert.match(html, /site-theme\/v2\/components\.css\?v=20261102-code/, path);
    assert.equal((html.match(/<h1\b/g) || []).length, 1, path);
  }
});

test('every internal link and listing source resolves, and fragments stay unlinked', () => {
  const exists = path => existsSync(new URL(path.replace(/^\/pokemon-reborn\//, '').replace(/\/$/, '/index.html').replace(/^$/, 'index.html'), root)) || files.has(path.replace(/^\/pokemon-reborn\//, '').replace(/\/$/, '/index.html'));
  for (const [path, html] of pages) {
    const base = new URL(path, 'https://jehlp.net/pokemon-reborn/');
    const ids = new Set([...html.matchAll(/ id="([^"]+)"/g)].map(m => m[1]));
    for (const [, attr, href] of html.matchAll(/ (href|data-src)="([^"]+)"/g)) {
      const url = new URL(href.replaceAll('&amp;', '&'), base);
      if (url.origin !== 'https://jehlp.net' || !url.pathname.startsWith('/pokemon-reborn/')) continue;
      const target = decodeURIComponent(url.pathname);
      assert.ok(exists(target === '/pokemon-reborn/' ? '' : target), `${path}: ${href}`);
      if (url.hash && url.pathname === base.pathname) assert.ok(ids.has(decodeURIComponent(url.hash.slice(1))), `${path}: ${href}`);
      if (attr === 'href') assert.doesNotMatch(target, /\/scripts\/code\//, `${path} links a fragment`);
    }
  }
});
