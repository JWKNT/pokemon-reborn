// Shared page frame for every generated page. Root-relative paths match the
// published /pokemon-reborn/ route and a local server rooted one level up.
export const BASE = '/pokemon-reborn/';
export const ORIGIN = 'https://jehlp.net';
const THEME = 'https://jehlp.net/site-theme/v2/';
export const ASSET_VERSION = '20261102-reborn2';

export const escapeHtml = value => String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
export const number = n => n.toLocaleString('en-US');

const SECTIONS = [['', 'Overview'], ['reasoning/', 'Reasoning'], ['notes/', 'Notes'], ['scripts/', 'Scripts']];

// Log times are stored as EDT ISO strings. Format their own fields; never let
// the build machine's time zone shift a date or a clock time.
const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const WEEKDAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const parts = iso => {
  const match = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})/.exec(iso);
  if (!match) throw new Error(`Invalid time: ${iso}`);
  const [, y, m, d, hh, mm, ss] = match;
  return { y: +y, m: +m, d: +d, hh, mm, ss, day: iso.slice(0, 10) };
};
export const dayOf = iso => parts(iso).day;
export const clock = iso => { const p = parts(iso); return `${p.hh}:${p.mm}:${p.ss}`; };
export const shortClock = iso => { const p = parts(iso); return `${p.hh}:${p.mm}`; };
export const longDate = iso => { const p = parts(iso); return `${MONTHS[p.m - 1]} ${p.d}, ${p.y}`; };
export const shortDate = iso => { const p = parts(iso); return `${MONTHS[p.m - 1].slice(0, 3)} ${p.d}`; };
export const weekdayDate = iso => { const p = parts(iso); return `${WEEKDAYS[new Date(Date.UTC(p.y, p.m - 1, p.d)).getUTCDay()]}, ${MONTHS[p.m - 1]} ${p.d}`; };
export const taskLabel = n => `Task ${String(n).padStart(2, '0')}`;
export const taskHref = n => `${BASE}reasoning/${String(n).padStart(2, '0')}/`;

export function page({ path, title, heading = title, description, main, scripts = false, mainClass = '' }) {
  const canonical = ORIGIN + BASE + path;
  const nav = SECTIONS.filter(([href]) => href !== path).map(([href, label]) => `<a href="${BASE}${href}">${label}</a>`).join('');
  return `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="${escapeHtml(description)}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="${escapeHtml(heading)}">
    <meta property="og:url" content="${canonical}">
    <meta property="og:site_name" content="jehlp.net">
    <meta name="theme-color" content="#fbfaf7">
    <link rel="canonical" href="${canonical}">
    <title>${escapeHtml(title)} · jehlp.net</title>
    <link rel="icon" href="${THEME}favicons/pokemon-reborn.png" type="image/png">
    <script src="${THEME}theme.js?v=20261009-reading-folio"></script>
    <link rel="stylesheet" href="${THEME}base.css?v=20261102-code">
    <link rel="stylesheet" href="${THEME}components.css?v=20261102-code">
    <link rel="stylesheet" href="${BASE}assets/styles.css?v=${ASSET_VERSION}">${scripts ? `
    <script src="${THEME}components.js?v=20261102-code" defer></script>
    <script src="${BASE}assets/app.js?v=${ASSET_VERSION}" defer></script>` : ''}
  </head>
  <body data-site-tone="teal">
    <a class="skip-link" href="#main">Skip to content</a>
    <header class="site-header site-header--identity">
      <div class="site-brand"><img class="site-mark" src="${THEME}marks/pokemon-reborn.png" width="32" height="32" alt=""><span class="site-title">Pokémon Reborn</span></div>
      <nav aria-label="Site links">${nav}<span class="site-utility-pair"><a class="site-home" href="https://jehlp.net/" aria-label="Home — jehlp.net" title="Home — jehlp.net"><span aria-hidden="true">✳</span></a><button class="theme-toggle" type="button" data-theme-toggle aria-label="Use dark theme" aria-pressed="false">◐</button></span></nav>
    </header>
    <main id="main" tabindex="-1" class="reborn-main${mainClass ? ` ${mainClass}` : ''}">
${main}
    </main>
  </body>
</html>
`;
}
