// Refresh data/ from a local checkout of the private reborn repository.
// Usage: node tools/import-reborn.mjs [--from ../reborn]
// Copies only the curated files in data/selection.json and extracts only the
// REASONING messages from CODEX_LOG.md. Prompts, steers and tool lines stay private.
import { cp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
const at = process.argv.indexOf('--from');
const source = resolve(root, at > 0 ? process.argv[at + 1] : '../reborn');
const selection = JSON.parse(await readFile(resolve(root, 'data/selection.json'), 'utf8'));
const log = await readFile(resolve(source, 'CODEX_LOG.md'), 'utf8');

// All log times are EDT (UTC-04:00); keep the offset in ISO form.
const iso = text => {
  const match = /^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) EDT$/.exec(text.trim());
  if (!match) throw new Error(`Unexpected log time: ${text}`);
  return `${match[1]}T${match[2]}-04:00`;
};

export function parseLog(text) {
  const index = [...text.matchAll(/^\| \[(\d+)\]\(#gameplay-prompt-\d+\) \| ([^|]+) \| ([^|]+) \| ([^|]+) \| ([^|]+) \|$/gm)];
  if (!index.length) throw new Error('No gameplay prompt index');
  const tasks = index.map(([, n, start, end, elapsed, sessions]) => ({ n: Number(n), start: iso(`${start.trim()} EDT`), end: iso(`${end.trim()} EDT`), elapsed: elapsed.trim(), sessions: sessions.trim(), messages: [] }));
  const sections = text.split(/^## Gameplay prompt (\d+)\s*$/m);
  const mentions = [];
  for (let i = 1; i < sections.length; i += 2) {
    const task = tasks.find(t => t.n === Number(sections[i]));
    if (!task) throw new Error(`Gameplay prompt ${sections[i]} is missing from the index`);
    const body = sections[i + 1];
    for (const [, time, quote] of body.matchAll(/^\*\*\[([^\]]+)\] REASONING:\*\*\n\n((?:>.*\n?)+)/gm)) {
      const message = quote.replace(/\n$/, '').split('\n').map(line => line.replace(/^> ?/, '')).join('\n').trim();
      if (!message) throw new Error(`Empty REASONING message at ${time}`);
      task.messages.push({ time: iso(time), text: message });
    }
    for (const [, time, line] of body.matchAll(/^- \[([^\]]+?)(?: → [^\]]+)?\] (.*)$/gm)) {
      const wrote = new Set();
      for (const write of line.matchAll(/(?:Wrote|Edited local files:|Created)\s+([^;]*)/g)) for (const [, kind, name] of write[1].matchAll(/\b(notes|scripts)\/([\w.\-]+)/g)) wrote.add(`${kind}/${name}`);
      for (const [, kind, name] of line.matchAll(/\b(notes|scripts)\/([\w.\-]+)/g)) mentions.push({ path: `${kind}/${name}`, time: iso(time), task: task.n, wrote: wrote.has(`${kind}/${name}`) });
    }
  }
  return { tasks, mentions };
}

const taskAt = (tasks, time) => {
  const t = Date.parse(time);
  return (tasks.find(task => Date.parse(task.start) <= t && t <= Date.parse(task.end)) || tasks.filter(task => Date.parse(task.start) <= t).at(-1) || tasks[0]).n;
};

const { tasks, mentions } = parseLog(log);
// Place each file at its first write in the log, else its first mention,
// else its first Git commit; the page lists files under that gameplay task.
const firstAdd = new Map();
const history = execFileSync('git', ['-C', source, 'log', '--diff-filter=A', '--format=@%aI', '--name-only', '--reverse', '--', 'notes', 'scripts'], { encoding: 'utf8', maxBuffer: 64 << 20 });
let when;
for (const line of history.split('\n')) {
  if (line.startsWith('@')) when = line.slice(1);
  else if (line && !firstAdd.has(line)) firstAdd.set(line, when);
}
const placements = {};
for (const [kind, names] of [['notes', selection.notes], ['scripts', selection.scripts]]) {
  placements[kind] = {};
  for (const name of names) {
    const path = `${kind}/${name}`;
    const found = mentions.filter(m => m.path === path);
    const pick = (kind === 'scripts' && found.find(m => m.wrote)) || found[0];
    if (pick) placements[kind][name] = { time: pick.time, task: pick.task, source: pick.wrote ? 'written' : 'mentioned' };
    else if (firstAdd.has(path)) placements[kind][name] = { time: firstAdd.get(path), task: taskAt(tasks, firstAdd.get(path)), source: 'committed' };
    else throw new Error(`Cannot place ${path}`);
  }
}

for (const kind of ['notes', 'scripts']) {
  await rm(resolve(root, 'data', kind), { recursive: true, force: true });
  await mkdir(resolve(root, 'data', kind), { recursive: true });
  for (const name of selection[kind]) await cp(resolve(source, kind, name), resolve(root, 'data', kind, name));
}
const commit = execFileSync('git', ['-C', source, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
await writeFile(resolve(root, 'data/reasoning.json'), JSON.stringify({ timezone: 'America/New_York (EDT, UTC-04:00)', tasks }, null, 1) + '\n');
await writeFile(resolve(root, 'data/provenance.json'), JSON.stringify({
  sourceCommit: commit,
  logSha256: createHash('sha256').update(log).digest('hex'),
  counts: { tasks: tasks.length, messages: tasks.reduce((n, t) => n + t.messages.length, 0), notes: selection.notes.length, scripts: selection.scripts.length },
  placements,
}, null, 1) + '\n');
console.log(`Imported ${tasks.length} tasks, ${tasks.reduce((n, t) => n + t.messages.length, 0)} messages, ${selection.notes.length} notes and ${selection.scripts.length} scripts from ${commit.slice(0, 8)}.`);
