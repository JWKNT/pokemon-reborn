// Video: a chapter link moves the embedded YouTube player to the start of its
// chapter, and the list marks the chapter that plays. Without this script,
// each link opens the video on YouTube at that time.
(() => {
  const frame = document.getElementById('video-player');
  const links = [...document.querySelectorAll('a[data-chapter-start]')];
  if (!frame || !links.length) return;
  const origin = new URL(frame.src).origin;
  const starts = links.map(link => Number(link.dataset.chapterStart));
  let ready = false;

  // With enablejsapi=1, the player accepts JSON commands through postMessage.
  const post = message => frame.contentWindow?.postMessage(JSON.stringify({ ...message, id: 'reborn-video', channel: 'widget' }), origin);
  const command = (func, args = []) => post({ event: 'command', func, args });

  function mark(index) {
    links.forEach((link, i) => {
      if (i === index) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });
  }
  const chapterAt = time => {
    let i = 0;
    while (i + 1 < starts.length && starts[i + 1] <= time + 0.5) i++;
    return i;
  };

  window.addEventListener('message', event => {
    if (event.origin !== origin || event.source !== frame.contentWindow) return;
    let data;
    try { data = typeof event.data === 'string' ? JSON.parse(event.data) : event.data; } catch { return; }
    ready = true;
    const time = data?.info?.currentTime;
    if (typeof time === 'number') mark(chapterAt(time));
  });

  // Ask the player for its state until it answers.
  let tries = 0;
  const listen = () => {
    if (ready || tries++ >= 40) return;
    post({ event: 'listening' });
    setTimeout(listen, 250);
  };
  frame.addEventListener('load', () => { tries = 0; listen(); });
  listen();

  document.addEventListener('click', event => {
    const link = event.target.closest?.('a[data-chapter-start]');
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    const start = Number(link.dataset.chapterStart);
    if (ready) {
      command('seekTo', [start, true]);
      command('playVideo');
    } else {
      // The player did not answer: load it again at the start of the chapter.
      const url = new URL(frame.src);
      url.searchParams.set('start', String(start));
      url.searchParams.set('autoplay', '1');
      frame.src = url.href;
    }
    mark(links.indexOf(link));
    frame.scrollIntoView({ block: 'nearest' });
  });
})();
