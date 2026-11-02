// Notes and scripts: load each listing's static fragment on its first open.
// Without this script, every closed panel still links to the note or source.
(() => {
  async function load(details) {
    if (details.dataset.loaded) return;
    details.dataset.loaded = 'loading';
    const body = details.querySelector('.listing-body');
    const status = document.createElement('p');
    status.className = 'listing-status';
    status.setAttribute('role', 'status');
    status.textContent = 'Loading…';
    body.prepend(status);
    body.setAttribute('aria-busy', 'true');
    try {
      const response = await fetch(details.dataset.src);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const fragment = new DOMParser().parseFromString(await response.text(), 'text/html').querySelector('[data-fragment]');
      if (!fragment) throw new Error('No listing in the response');
      body.replaceChildren(document.importNode(fragment, true));
      details.dataset.loaded = 'true';
      window.JehlpUI?.enhance(body);
    } catch {
      delete details.dataset.loaded;
      status.textContent = 'The listing did not load. Close and open it to try again, or use the link.';
    } finally {
      body.removeAttribute('aria-busy');
    }
  }

  // toggle does not bubble; a capturing listener sees every disclosure.
  document.addEventListener('toggle', event => {
    if (event.target.matches?.('details[data-src]') && event.target.open) load(event.target);
  }, true);

  // A link to #file opens that file's panel.
  function openFromHash() {
    const target = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!target?.matches('details[data-src]')) return;
    const item = target.closest('[data-filter-item]');
    if (item?.hidden) clearFilter();
    target.open = true;
    target.scrollIntoView({ block: 'start' });
  }

  const tools = document.querySelector('[data-filter-tools]');
  const input = tools?.querySelector('[data-filter-input]');
  const count = tools?.querySelector('[data-filter-count]');
  const items = [...document.querySelectorAll('[data-filter-item]')].map(item => ({ item, text: item.querySelector('summary').textContent.toLowerCase() }));
  const groups = [...document.querySelectorAll('[data-filter-group]')];
  const total = items.length.toLocaleString('en-US');
  function filter() {
    const query = input.value.trim().toLowerCase();
    let shown = 0;
    for (const { item, text } of items) {
      item.hidden = Boolean(query) && !text.includes(query);
      if (!item.hidden) shown++;
    }
    for (const group of groups) group.hidden = !group.querySelector('[data-filter-item]:not([hidden])');
    count.textContent = query ? `${shown.toLocaleString('en-US')} of ${total} shown` : `${total} files`;
  }
  function clearFilter() {
    if (!input || !input.value) return;
    input.value = '';
    filter();
  }
  if (tools && input && count) {
    tools.hidden = false;
    input.addEventListener('input', filter);
    input.addEventListener('keydown', event => {
      if (event.key === 'Escape' && !event.defaultPrevented && input.value) { event.preventDefault(); clearFilter(); }
    });
    filter();
  }
  window.addEventListener('hashchange', openFromHash);
  openFromHash();
})();
