import hljs from 'highlight.js/lib/core';
import python from 'highlight.js/lib/languages/python';
import ruby from 'highlight.js/lib/languages/ruby';
import swift from 'highlight.js/lib/languages/swift';
import json from 'highlight.js/lib/languages/json';
import { Marked } from 'marked';
import { escapeHtml } from './site.mjs';

hljs.registerLanguage('python', python);
hljs.registerLanguage('ruby', ruby);
hljs.registerLanguage('swift', swift);
hljs.registerLanguage('json', json);

const LANGUAGES = { py: 'python', rb: 'ruby', swift: 'swift', json: 'json', jsonl: 'json' };
export const LANGUAGE_LABELS = { python: 'Python', ruby: 'Ruby', swift: 'Swift', json: 'JSON', markdown: 'Markdown', text: 'Text' };
export const extension = name => (/\.([a-z0-9]+)$/i.exec(name)?.[1] || '').toLowerCase();
export const languageOf = name => LANGUAGES[extension(name)] || null;

// Build-time highlighting per the site-theme code contract: spans only, so the
// listing keeps the exact source text. Unknown languages stay escaped text.
export const highlight = (code, language) => language && hljs.getLanguage(language)
  ? hljs.highlight(code, { language, ignoreIllegals: true }).value
  : escapeHtml(code);

export const codeBlock = (code, { language = null, label, wrap = false, fragment = false }) =>
  `<pre class="ui-code${wrap ? ' ui-code--wrap' : ''}"${fragment ? ' data-fragment' : ''} tabindex="0" aria-label="${escapeHtml(label)}"><code class="hljs${language ? ` language-${language}` : ''}">${highlight(code, language)}</code></pre>`;

// Web links stay links. A path that names a published note or script links to
// it; any other local path (a private file, a video) stays plain text.
export function linkPolicy({ notes = new Map(), scripts = new Set(), scriptHref = name => name } = {}) {
  return href => {
    const value = String(href || '').replace(/^<|>$/g, '');
    if (/^https?:\/\//i.test(value)) return value;
    const name = decodeURIComponent(value.split(/[?#]/)[0].split('/').pop() || '');
    if (notes.has(name)) return notes.get(name);
    if (scripts.has(name)) return scriptHref(name);
    return null;
  };
}

export function markdown({ headingOffset = 0, resolve = () => null } = {}) {
  const md = new Marked({ gfm: true });
  md.use({ renderer: {
    html: token => escapeHtml(token.text),
    image: token => escapeHtml(token.text || ''),
    heading(token) {
      const level = Math.min(6, token.depth + headingOffset);
      return `<h${level}>${this.parser.parseInline(token.tokens)}</h${level}>\n`;
    },
    link(token) {
      const label = this.parser.parseInline(token.tokens);
      const href = resolve(token.href);
      return href ? `<a href="${escapeHtml(href)}">${label}</a>` : label;
    },
    code: token => codeBlock(token.text, { language: hljs.getLanguage(token.lang || '') ? token.lang : null, label: token.lang ? `${token.lang} example` : 'Code example', wrap: true }) + '\n',
  } });
  // A wide table scrolls inside a named, focusable region instead of the page.
  return text => md.parse(String(text)).replaceAll('<table>', '<div class="table-scroll" tabindex="0" role="region" aria-label="Table"><table>').replaceAll('</table>', '</table></div>');
}

const URL_PATTERN = /https?:\/\/[^\s<>"')\]]+/g;
const linkText = text => {
  let html = '', last = 0;
  for (const match of text.matchAll(URL_PATTERN)) {
    html += escapeHtml(text.slice(last, match.index)) + `<a href="${escapeHtml(match[0])}">${escapeHtml(match[0])}</a>`;
    last = match.index + match[0].length;
  }
  return html + escapeHtml(text.slice(last));
};

// Plain-text notes keep their own line breaks; blank lines separate paragraphs.
export const plainText = text => String(text).replace(/\r\n?/g, '\n').trim().split(/\n\s*\n/).map(p => `<p>${linkText(p)}</p>`).join('\n');

// Keep JSON exactly as written unless it is on one line; then indent it by two
// spaces for reading. Highlighting never changes the characters themselves.
export function jsonText(source) {
  const text = String(source).replace(/\s+$/, '');
  if (text.includes('\n')) return text;
  try { return JSON.stringify(JSON.parse(text), null, 2); } catch { return text; }
}

const flat = text => String(text).replace(/[*_`#>]/g, '').replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/\s+/g, ' ').trim();
const clip = (text, max = 140) => text.length > max ? `${text.slice(0, max - 1).replace(/\s+\S*$/, '')}…` : text;

// A one-line description for an index row, taken from the note's own words.
export function noteSummary(name, source) {
  const text = String(source);
  if (extension(name) === 'md') {
    const h1 = /^#\s+(.+)$/m.exec(text);
    return clip(flat(h1 ? h1[1] : text.split('\n').find(line => line.trim()) || ''));
  }
  if (extension(name) === 'json') {
    try {
      const data = JSON.parse(text);
      if (data && typeof data === 'object' && !Array.isArray(data)) {
        for (const key of ['objective', 'goal', 'plan', 'policy', 'summary', 'status', 'note', 'notes', 'purpose', 'basis', 'source']) if (typeof data[key] === 'string' && data[key].trim().length > 12) return clip(flat(data[key]));
        const first = Object.values(data).find(value => typeof value === 'string' && value.length >= 24);
        if (first) return clip(flat(first));
      }
    } catch {}
    return '';
  }
  return clip(flat(text.split('\n').find(line => line.trim()) || ''));
}

// The first line of a module docstring or leading comment, as the author wrote it.
export function scriptSummary(name, source) {
  const text = String(source).replace(/^#![^\n]*\n/, '');
  if (extension(name) === 'py') {
    const doc = /^(?:\s*#[^\n]*\n|\s*\n)*\s*[rRuU]?("""|''')([\s\S]*?)\1/.exec(text);
    if (doc) return clip(flat(doc[2].trim().split('\n')[0]));
  }
  const comment = /^\s*(?:#|\/\/)\s*(\S[^\n]*)/m.exec(text.split('\n').slice(0, 12).join('\n'));
  return comment && !/^(?:frozen_string_literal|swift-tools-version|-\*-)/.test(comment[1]) ? clip(flat(comment[1])) : '';
}
