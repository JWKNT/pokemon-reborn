import { BASE, page, escapeHtml, number, dayOf, clock, shortClock, longDate, shortDate, weekdayDate, taskLabel, taskHref } from './site.mjs';
import { LANGUAGE_LABELS, extension, languageOf, codeBlock, markdown, linkPolicy, plainText, jsonText, noteSummary, scriptSummary } from './render.mjs';

const pad = n => String(n).padStart(2, '0');
const kib = bytes => bytes < 1024 ? `${bytes} B` : `${number(Math.round(bytes / 102.4) / 10)} KB`;
export const noteHref = name => `${BASE}notes/${encodeURIComponent(name)}.html`;
export const scriptHref = name => `${BASE}scripts/#${encodeURIComponent(name)}`;
const kindOf = name => ({ md: 'markdown', txt: 'text' })[extension(name)] || languageOf(name) || 'text';

export function buildSite({ reasoning, provenance, notes, scripts }) {
  const tasks = reasoning.tasks;
  const messages = tasks.reduce((n, t) => n + t.messages.length, 0);
  const noteLinks = new Map(notes.map(n => [n.name, noteHref(n.name)]));
  const resolve = linkPolicy({ notes: noteLinks, scripts: new Set(scripts.map(s => s.name)), scriptHref });
  const messageText = markdown({ headingOffset: 2, resolve });
  const noteMarkdown = markdown({ headingOffset: 1, resolve });
  const files = new Map();
  const first = tasks[0], last = tasks.at(-1);
  const span = `${longDate(first.start)} to ${longDate(last.end)}`;
  const languages = Object.entries(scripts.reduce((acc, s) => ({ ...acc, [languageOf(s.name)]: (acc[languageOf(s.name)] || 0) + 1 }), {})).sort((a, b) => b[1] - a[1]).map(([l]) => LANGUAGE_LABELS[l]);

  files.set('index.html', page({ path: '', title: 'Pokémon Reborn', description: `Astra's Pokémon Reborn playthrough: ${number(messages)} reasoning messages, ${notes.length} planning notes and ${number(scripts.length)} scripts.`, main: `      <header class="page-head">
        <h1>Pokémon Reborn</h1>
        <p class="lede">Astra played Pokémon Reborn 19.5.43 with the HARDCAP password, ${span}. The run won all 18 badges and completed the main story and the Anna-route postgame.</p>
      </header>
      <dl class="data-strip run-facts">
        <div><dt>Gameplay tasks</dt><dd>${tasks.length}</dd></div>
        <div><dt>Recorded sessions</dt><dd>${escapeHtml(first.sessions.split(/[–-]/)[0])}–${escapeHtml(last.sessions.split(/[–-]/).at(-1))}</dd></div>
        <div><dt>Messages</dt><dd>${number(messages)}</dd></div>
      </dl>
      <ul class="sections ui-directory">
        <li><a href="${BASE}reasoning/">Reasoning</a><p>${number(messages)} timestamped messages from Astra during ${tasks.length} gameplay tasks.</p></li>
        <li><a href="${BASE}notes/">Notes</a><p>${notes.length} planning notes: battle plans, routes, preparation and play policy.</p></li>
        <li><a href="${BASE}scripts/">Scripts</a><p>${number(scripts.length)} gameplay automation scripts in ${languages.join(', ').replace(/, ([^,]*)$/, ' and $1')}.</p></li>
      </ul>
      <p class="provenance">A selection from the private run repository at commit <code>${escapeHtml(provenance.sourceCommit.slice(0, 8))}</code>. Times are Eastern Daylight Time (UTC−04:00). Notes include planning only. Scripts include gameplay automation only.</p>` }));

  const rows = tasks.map(t => `<tr><th scope="row"><a href="${taskHref(t.n)}">${taskLabel(t.n)}</a></th><td>${shortDate(t.start)}</td><td class="num">${shortClock(t.start)}</td><td class="num">${escapeHtml(t.elapsed)}</td><td class="num">${escapeHtml(t.sessions)}</td><td class="num">${number(t.messages.length)}</td></tr>`).join('\n');
  files.set('reasoning/index.html', page({ path: 'reasoning/', title: 'Reasoning · Pokémon Reborn', heading: 'Reasoning', description: `${number(messages)} timestamped messages from Astra during ${tasks.length} Pokémon Reborn gameplay tasks.`, main: `      <header class="page-head">
        <h1>Reasoning</h1>
        <p class="lede">Astra's messages during each gameplay task, as written, with their times in EDT.</p>
      </header>
      <div class="table-scroll" tabindex="0" role="region" aria-label="Gameplay tasks">
        <table class="ui-table task-table">
          <thead><tr><th scope="col">Task</th><th scope="col">Date</th><th scope="col" class="num">Start</th><th scope="col" class="num">Duration</th><th scope="col" class="num">Sessions</th><th scope="col" class="num">Messages</th></tr></thead>
          <tbody>
${rows}
          </tbody>
        </table>
      </div>` }));

  for (const [i, t] of tasks.entries()) {
    const days = [...new Set(t.messages.map(m => dayOf(m.time)))];
    const sections = days.map(day => {
      const list = t.messages.map((m, index) => ({ ...m, index })).filter(m => dayOf(m.time) === day).map(m => `          <li class="message" id="m${m.index + 1}"><a class="message-time" href="#m${m.index + 1}"><time datetime="${m.time}">${clock(m.time)}</time></a><div class="message-text">${messageText(m.text)}</div></li>`).join('\n');
      return `      <section class="day" id="d-${day}" aria-labelledby="h-${day}">
        <h2 id="h-${day}">${weekdayDate(`${day}T00:00:00`)}</h2>
        <ol class="messages">
${list}
        </ol>
      </section>`;
    }).join('\n');
    const prev = tasks[i - 1], next = tasks[i + 1];
    files.set(`reasoning/${pad(t.n)}/index.html`, page({ path: `reasoning/${pad(t.n)}/`, title: `${taskLabel(t.n)} · Reasoning · Pokémon Reborn`, heading: `${taskLabel(t.n)} reasoning`, description: `Astra's ${number(t.messages.length)} messages during Pokémon Reborn gameplay task ${t.n}, ${longDate(t.start)}.`, mainClass: 'task-page', main: `      <header class="page-head">
        <h1>${taskLabel(t.n)}</h1>
        <p class="task-meta">${longDate(t.start)} · ${shortClock(t.start)}–${shortClock(t.end)} EDT${dayOf(t.start) === dayOf(t.end) ? '' : ` ${shortDate(t.end)}`} · ${escapeHtml(t.elapsed)} · Sessions ${escapeHtml(t.sessions)} · ${number(t.messages.length)} messages</p>
      </header>${days.length > 1 ? `
      <nav class="day-index" aria-label="Days in this task">${days.map(day => `<a href="#d-${day}">${shortDate(`${day}T00:00:00`)}</a>`).join('')}</nav>` : ''}
${sections}
      <nav class="task-pager" aria-label="Tasks">${prev ? `<a rel="prev" href="${taskHref(prev.n)}">${taskLabel(prev.n)}</a>` : '<span></span>'}<a href="${BASE}reasoning/">All tasks</a>${next ? `<a rel="next" href="${taskHref(next.n)}">${taskLabel(next.n)}</a>` : '<span></span>'}</nav>` }));
  }

  // One listing per file, grouped under the task that first wrote or used it.
  const grouped = (items, placements) => tasks.map(t => ({ task: t, items: items.filter(item => placements[item.name].task === t.n).sort((a, b) => placements[a.name].time.localeCompare(placements[b.name].time) || a.name.localeCompare(b.name)) })).filter(group => group.items.length);
  const placedAt = (placement, verb) => `${placement.source === 'written' ? 'written' : placement.source === 'committed' ? 'committed' : verb} ${shortDate(placement.time)} ${shortClock(placement.time)}`;
  const toolbar = (id, label) => `      <div class="ui-toolbar listing-tools" data-filter-tools hidden>
        <label class="ui-field ui-field--search" for="${id}">${label}<input id="${id}" type="search" autocomplete="off" spellcheck="false" data-filter-input></label>
        <p class="listing-count" role="status" aria-live="polite" data-filter-count></p>
      </div>`;
  const groupHtml = (group, row) => `      <section class="listing-group" data-filter-group aria-labelledby="g-${group.task.n}">
        <h2 id="g-${group.task.n}"><a href="${taskHref(group.task.n)}">${taskLabel(group.task.n)}</a><span class="group-date">${shortDate(group.task.start)} · ${group.items.length}</span></h2>
        <ul class="listings">
${group.items.map(row).join('\n')}
        </ul>
      </section>`;

  const noteRow = n => {
    const p = provenance.placements.notes[n.name];
    return `<li data-filter-item><details class="listing" id="${escapeHtml(n.name)}" data-src="${encodeURIComponent(n.name)}.html"><summary><span class="listing-name">${escapeHtml(n.name)}</span><span class="listing-meta">${LANGUAGE_LABELS[n.kind]} · ${kib(n.bytes)} · ${placedAt(p, 'first used')}</span>${n.summary ? `<span class="listing-summary">${escapeHtml(n.summary)}</span>` : ''}</summary><div class="listing-body"><p class="listing-fallback"><a href="${encodeURIComponent(n.name)}.html">Open ${escapeHtml(n.name)}</a></p></div></details></li>`;
  };
  files.set('notes/index.html', page({ path: 'notes/', title: 'Notes · Pokémon Reborn', heading: 'Notes', description: `${notes.length} planning notes from Astra's Pokémon Reborn playthrough.`, scripts: true, main: `      <header class="page-head">
        <h1>Notes</h1>
        <p class="lede">Astra's planning notes: battle plans, routes, preparation and play policy. Open a note to read it here.</p>
      </header>
${toolbar('note-filter', 'Find a note')}
${grouped(notes, provenance.placements.notes).map(g => groupHtml(g, noteRow)).join('\n')}` }));

  for (const n of notes) {
    const p = provenance.placements.notes[n.name];
    const body = n.kind === 'markdown' ? `<div class="note-prose prose">${noteMarkdown(n.source)}</div>`
      : n.kind === 'json' ? codeBlock(jsonText(n.source), { language: 'json', label: `Contents of ${n.name}`, wrap: true })
      : `<div class="note-prose note-text">${plainText(n.source)}</div>`;
    files.set(`notes/${n.name}.html`, page({ path: `notes/${encodeURIComponent(n.name)}.html`, title: `${n.name} · Notes · Pokémon Reborn`, heading: n.name, description: n.summary || `Planning note ${n.name} from Astra's Pokémon Reborn playthrough.`, mainClass: 'note-page', main: `      <header class="page-head">
        <h1 class="note-name">${escapeHtml(n.name)}</h1>
        <p class="task-meta">${LANGUAGE_LABELS[n.kind]} · ${kib(n.bytes)} · <a href="${taskHref(p.task)}">${taskLabel(p.task)}</a> · ${placedAt(p, 'first used')}</p>
      </header>
      <article class="note-body" data-fragment>
${body}
      </article>` }));
  }

  const scriptRow = s => {
    const p = provenance.placements.scripts[s.name];
    return `<li data-filter-item><details class="listing" id="${escapeHtml(s.name)}" data-src="code/${encodeURIComponent(s.name)}.html"><summary><span class="listing-name">${escapeHtml(s.name)}</span><span class="listing-meta">${LANGUAGE_LABELS[languageOf(s.name)]} · ${number(s.lines)} lines · ${placedAt(p, 'first run')}</span>${s.summary ? `<span class="listing-summary">${escapeHtml(s.summary)}</span>` : ''}</summary><div class="listing-body"><p class="listing-fallback"><a href="source/${encodeURIComponent(s.name)}.txt">Plain text of ${escapeHtml(s.name)}</a></p></div></details></li>`;
  };
  files.set('scripts/index.html', page({ path: 'scripts/', title: 'Scripts · Pokémon Reborn', heading: 'Scripts', description: `${number(scripts.length)} gameplay automation scripts from Astra's Pokémon Reborn playthrough, with syntax highlighting.`, scripts: true, main: `      <header class="page-head">
        <h1>Scripts</h1>
        <p class="lede">The gameplay automation that Astra wrote during the run. Open a script to read its source.</p>
      </header>
${toolbar('script-filter', 'Find a script')}
${grouped(scripts, provenance.placements.scripts).map(g => groupHtml(g, scriptRow)).join('\n')}` }));

  // Fragments load into the index on first open. They are not linked pages,
  // so they stay out of site search; the plain-text copy is the no-script path.
  for (const s of scripts) {
    files.set(`scripts/code/${s.name}.html`, `<!doctype html>
<html lang="en">
  <head><meta charset="utf-8"><meta name="robots" content="noindex"><title>${escapeHtml(s.name)}</title></head>
  <body>
${codeBlock(s.source, { language: languageOf(s.name), label: `Source of ${s.name}`, fragment: true })}
  </body>
</html>
`);
    files.set(`scripts/source/${s.name}.txt`, s.source);
  }
  return files;
}

export const loadNote = (name, source) => ({ name, source, bytes: Buffer.byteLength(source), kind: kindOf(name), summary: noteSummary(name, source) });
export const loadScript = (name, source) => ({ name, source, lines: source.split('\n').length - (source.endsWith('\n') ? 1 : 0), summary: scriptSummary(name, source) });
