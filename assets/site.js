/* Merkorn, comportamenti comuni a tutte le pagine. */
(() => {
  // Every request from the contact form reaches this inbox: through the site's own mail function
  // (api/contact.js, sent from Gmail) and, until that is configured, through FormSubmit.
  const INBOX = 'merkornsh@gmail.com';
  const ENDPOINT = '/api/contact';
  const BACKUP = 'https://formsubmit.co/ajax/' + INBOX;

  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp = v => Math.max(0, Math.min(1, v));
  let dirty = true;

  /* ---------- mobile menu ---------- */
  const nav = document.querySelector('.nav');
  const menuBtn = document.querySelector('.menu-btn');
  const setMenu = open => {
    if (!menuBtn) return;
    nav.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Chiudi il menu' : 'Apri il menu');
  };
  if (menuBtn) {
    menuBtn.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && nav.classList.contains('open')) { setMenu(false); menuBtn.focus(); } });
    document.addEventListener('click', e => { if (nav.classList.contains('open') && !e.target.closest('.pill')) setMenu(false); });
    matchMedia('(min-width: 821px)').addEventListener('change', e => { if (e.matches) setMenu(false); });
  }

  /* ---------- page change: fade out while the nebula speeds up ---------- */
  let leaving = false;
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if (!a || reduce || leaving || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.target === '_blank' || a.hasAttribute('download')) return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin || !/(\.html|\/)$/.test(url.pathname)) return;
    if (url.pathname === location.pathname) return; // same page: let the browser handle it
    e.preventDefault();
    leaving = true;
    setMenu(false);
    document.body.classList.add('leaving');
    if (window.merkornWarp) window.merkornWarp(1);
    setTimeout(() => { location.href = url.href; }, 420);
  });
  // coming back with the browser buttons restores the page from cache: undo the fade
  addEventListener('pageshow', () => {
    leaving = false;
    document.body.classList.remove('leaving');
    if (window.merkornWarp) window.merkornWarp(0);
    dirty = true;
  });

  /* ---------- statement: split into words ---------- */
  const statements = [...document.querySelectorAll('.statement.pinned')].map(sec => {
    const p = sec.querySelector('p[data-hl]');
    const hl = p.dataset.hl.split(',');
    p.innerHTML = p.textContent.trim().split(/\s+/).map(w => `<span class="w${hl.includes(w.replace(/[.,]/g, '')) ? ' hl' : ''}">${w}</span>`).join(' ');
    return { sec, words: [...p.querySelectorAll('.w')], small: sec.querySelector('small'), lit: -1 };
  });

  /* ---------- method phases light up in the middle of the screen ---------- */
  const legs = document.querySelectorAll('.leg');
  if (legs.length) {
    const io = new IntersectionObserver(es => es.forEach(e => e.target.classList.toggle('on', e.isIntersecting)), { rootMargin: '-45% 0px -45% 0px' });
    legs.forEach(l => io.observe(l));
  }

  /* ---------- HUD: current section ---------- */
  const hud = document.querySelector('.hud');
  const hudName = hud && hud.querySelector('.hud-name');
  const pm = hud ? [...hud.querySelectorAll('.pm i')] : [];
  const named = [...document.querySelectorAll('main > section[data-name]')];
  if (hudName && named.length) {
    const sio = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      const i = named.indexOf(e.target);
      hudName.textContent = e.target.dataset.name;
      hud.classList.toggle('off', e.target.classList.contains('contact'));
      const lit = Math.round((i / Math.max(1, named.length - 1)) * 5);
      pm.forEach((b, k) => b.classList.toggle('on', k < lit));
    }), { rootMargin: '-50% 0px -50% 0px' });
    named.forEach(s => sio.observe(s));
  }

  /* ---------- scroll engine ----------
     data-scrub  pinned section, --p from 0 to 1 while it is pinned
     data-enter  --e from 0 to 1 while the element enters the screen
     data-exit   --x from 0 to 1 while the section leaves the top
     data-grow   --g from 0 to 1, the purple band grows into place
     data-line   --l fills the line of the method phases
     .rules      --k shrinks each stacked card as the next one covers it
     Values are written once per frame, only when the scroll position or the
     viewport changed, and never through CSS transitions. */
  const all = sel => [...document.querySelectorAll(sel)];
  const scrubs = all('[data-scrub]');
  const enters = all('[data-enter]');
  const exits = all('[data-exit]');
  const grows = all('[data-grow]');
  const lines = all('[data-line]');
  const stacks = all('.rules').map(ol => [...ol.children]);
  const tracks = all('.hscroll').map(sec => ({ sec, pin: sec.querySelector('.pin'), track: sec.querySelector('.track'), extra: 0 }));
  const set = (el, name, v) => { const s = v.toFixed(3); if (el.style.getPropertyValue(name) !== s) el.style.setProperty(name, s); };

  // the horizontal track is active only where the CSS keeps it pinned
  const hMode = matchMedia('(min-width: 761px) and (min-height: 621px) and (prefers-reduced-motion: no-preference)');
  let lastW = innerWidth, lastH = innerHeight;
  function sizeTracks() {
    tracks.forEach(t => {
      t.track.style.translate = '';
      if (!hMode.matches) { t.sec.style.height = ''; t.extra = 0; return; }
      t.extra = Math.max(0, t.track.scrollWidth - t.sec.clientWidth);
      t.sec.style.height = (t.pin.offsetHeight + t.extra) + 'px';
    });
    dirty = true;
  }
  addEventListener('resize', () => {
    // ignore the small height changes of mobile browser toolbars
    if (innerWidth !== lastW || Math.abs(innerHeight - lastH) > 120) { lastW = innerWidth; lastH = innerHeight; sizeTracks(); }
    dirty = true;
  });
  hMode.addEventListener('change', sizeTracks);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(sizeTracks);
  addEventListener('load', sizeTracks);
  addEventListener('scroll', () => { dirty = true; }, { passive: true });

  function update() {
    const vh = innerHeight;
    // 1. read every position first: mixing reads and writes forced a layout per element and caused stutter
    const rs = scrubs.map(el => el.getBoundingClientRect());
    const re = reduce ? [] : enters.map(el => el.getBoundingClientRect().top);
    const rx = reduce ? [] : exits.map(el => el.getBoundingClientRect());
    const rg = reduce ? [] : grows.map(el => el.getBoundingClientRect().top);
    const rk = reduce ? [] : stacks.map(items => items.map(li => li.getBoundingClientRect()));
    const rl = lines.map(el => el.getBoundingClientRect());
    // 2. then write
    scrubs.forEach((el, i) => {
      const r = rs[i];
      el._p = clamp(-r.top / Math.max(1, r.height - vh));
      set(el, '--p', el._p);
    });
    statements.forEach(st => {
      const p = reduce ? 1 : (st.sec._p || 0);
      const lit = Math.round(clamp(p * 1.4) * st.words.length);
      if (lit !== st.lit) { st.words.forEach((w, i) => w.classList.toggle('lit', i < lit)); st.lit = lit; }
      set(st.small, '--sm', clamp((p - .62) * 4));
    });
    tracks.forEach(t => {
      if (t.extra) t.track.style.translate = `${(-(t.sec._p || 0) * t.extra).toFixed(1)}px 0`;
    });
    if (!reduce) {
      enters.forEach((el, i) => set(el, '--e', clamp((vh - re[i]) / (vh * .38))));
      exits.forEach((el, i) => set(el, '--x', clamp(-rx[i].top / (rx[i].height * .8))));
      grows.forEach((el, i) => set(el, '--g', clamp((vh - rg[i]) / (vh * .7))));
      stacks.forEach((items, s) => items.forEach((li, i) => {
        if (i === items.length - 1) return;
        const a = rk[s][i], b = rk[s][i + 1];
        set(li, '--k', clamp((a.bottom - b.top) / a.height));
      }));
    }
    lines.forEach((el, i) => set(el, '--l', clamp((vh * .5 - rl[i].top) / rl[i].height)));
  }

  sizeTracks();
  update();
  (function tick() {
    if (dirty) { dirty = false; update(); }
    requestAnimationFrame(tick);
  })();

  /* ---------- copy email ---------- */
  document.querySelectorAll('[data-copy]').forEach(btn => {
    const out = document.getElementById(btn.dataset.copy);
    let timer;
    btn.addEventListener('click', () => {
      const done = text => { btn.textContent = text; clearTimeout(timer); timer = setTimeout(() => { btn.textContent = 'Copia indirizzo'; }, 2000); };
      const select = () => { getSelection().selectAllChildren(out); done('Selezionato, premi Ctrl+C'); };
      try { navigator.clipboard.writeText(out.textContent.trim()).then(() => done('Copiato'), select); } catch (err) { select(); }
    });
  });

  /* ---------- contact form ---------- */
  document.querySelectorAll('form.form').forEach(form => {
    const status = form.querySelector('.status');
    const submit = form.querySelector('button[type="submit"]');
    const label = submit.querySelector('span');
    const privacy = form.elements.privacy;
    const rules = {
      nome: v => v.trim().length >= 2 || 'Inserisci nome e cognome.',
      email: v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) || 'Inserisci un indirizzo email valido, per esempio nome@azienda.it.',
      messaggio: v => v.trim().length >= 10 || 'Descrivi brevemente la richiesta, bastano poche righe.'
    };
    const touched = new Set();
    function check(name) {
      const el = form.elements[name];
      const field = el.closest('.field');
      const res = rules[name](el.value);
      field.classList.toggle('bad', res !== true);
      el.setAttribute('aria-invalid', String(res !== true));
      field.querySelector('.err').textContent = res === true ? '' : res;
      return res === true;
    }
    Object.keys(rules).forEach(n => {
      const el = form.elements[n];
      el.addEventListener('blur', () => { if (el.value) { touched.add(n); check(n); } });
      el.addEventListener('input', () => { if (touched.has(n)) check(n); });
    });
    privacy.addEventListener('change', () => { if (privacy.checked) privacy.closest('.check').classList.remove('bad'); });

    let sending = false;
    form.addEventListener('submit', async e => {
      e.preventDefault();
      if (sending) return;
      status.className = 'status'; status.textContent = '';
      Object.keys(rules).forEach(n => touched.add(n));
      const valid = Object.keys(rules).map(check).every(Boolean);
      privacy.closest('.check').classList.toggle('bad', !privacy.checked);
      if (!valid || !privacy.checked) {
        status.className = 'status ko';
        status.textContent = valid ? 'Per inviare la richiesta serve il consenso al trattamento dei dati.' : 'Controlla i campi evidenziati.';
        const first = form.querySelector('.field.bad input, .field.bad textarea') || (!privacy.checked ? privacy : null);
        if (first) first.focus();
        return;
      }
      if (form.elements._honey.value) return; // bots fill the hidden field

      const data = {
        'Nome e cognome': form.elements.nome.value.trim(),
        'Azienda': form.elements.azienda.value.trim(),
        'Email': form.elements.email.value.trim(),
        'Telefono': form.elements.telefono.value.trim(),
        'Argomento': form.elements.argomento.value,
        'Messaggio': form.elements.messaggio.value.trim(),
        'Pagina': document.title,
        _subject: 'Nuova richiesta dal sito Merkorn: ' + form.elements.argomento.value,
        _replyto: form.elements.email.value.trim(),
        _template: 'table',
        _captcha: 'false'
      };
      sending = true;
      submit.disabled = true; label.textContent = 'Invio in corso';
      form.setAttribute('aria-busy', 'true');
      // the service can be slow: say so instead of leaving the button looking frozen
      const slow = setTimeout(() => {
        status.className = 'status wait';
        status.textContent = 'Invio in corso, il servizio può richiedere qualche secondo.';
      }, 3500);
      const ctrl = new AbortController();
      const timeout = setTimeout(() => ctrl.abort(), 12000);
      try {
        const post = url => fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data), signal: ctrl.signal });
        let res = await post(ENDPOINT);
        // 404 or 503: the mail function is not deployed or not configured yet
        if (res.status === 404 || res.status === 503) res = await post(BACKUP);
        const body = await res.json().catch(() => ({}));
        if (!res.ok || String(body.success) === 'false') throw new Error(body.message || res.status);
        form.reset(); touched.clear();
        status.className = 'status ok';
        status.textContent = 'Richiesta inviata. Vi ricontattiamo all\'indirizzo email che avete indicato.';
      } catch (err) {
        // never lose the request: the same text, ready to send from the visitor's own mail app
        const text = Object.entries(data).filter(([k, v]) => k[0] !== '_' && k !== 'Pagina' && v).map(([k, v]) => k + ': ' + v).join('\n');
        const mail = document.createElement('a');
        mail.className = 'mail-fallback';
        mail.href = 'mailto:' + INBOX + '?subject=' + encodeURIComponent(data._subject) + '&body=' + encodeURIComponent(text);
        mail.textContent = 'Invia la richiesta via email';
        status.className = 'status ko';
        status.textContent = 'Il servizio di invio non ha risposto, i dati che avete inserito sono ancora nel modulo. Potete inviare la stessa richiesta con il vostro programma di posta, a ' + INBOX + '. ';
        status.appendChild(mail);
      } finally {
        clearTimeout(timeout); clearTimeout(slow);
        sending = false;
        form.removeAttribute('aria-busy');
        submit.disabled = false; label.textContent = 'Invia la richiesta';
      }
    });
  });
})();
