import { mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSite, loadNote, loadScript } from './lib/pages.mjs';

const root = fileURLToPath(new URL('./', import.meta.url));
const read = path => readFile(resolve(root, path), 'utf8');
const selection = JSON.parse(await read('data/selection.json'));
const reasoning = JSON.parse(await read('data/reasoning.json'));
const provenance = JSON.parse(await read('data/provenance.json'));
const notes = await Promise.all(selection.notes.map(async name => loadNote(name, await read(`data/notes/${name}`))));
const scripts = await Promise.all(selection.scripts.map(async name => loadScript(name, await read(`data/scripts/${name}`))));

const files = buildSite({ reasoning, provenance, notes, scripts });
// Generated directories are rebuilt whole, so removed files do not linger.
for (const dir of ['reasoning', 'notes', 'scripts']) await rm(resolve(root, dir), { recursive: true, force: true });
for (const [path, content] of files) {
  await mkdir(dirname(resolve(root, path)), { recursive: true });
  await writeFile(resolve(root, path), content);
}
console.log(`Built ${files.size} files: ${reasoning.tasks.length} reasoning tasks, ${notes.length} notes, ${scripts.length} scripts.`);
