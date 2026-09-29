/* Merkorn, consenso ai cookie.
   Il sito usa un solo cookie tecnico (mk_consent) che ricorda la scelta per 6 mesi.
   Google Analytics viene caricato solo dopo il consenso ai cookie statistici e solo
   se nello script è indicato un ID di misurazione (data-ga). Nessun altro servizio. */
(() => {
  const script = document.currentScript;
  const GA = (script && script.dataset.ga) || '';
  const NAME = 'mk_consent';
  const MAX_AGE = 60 * 60 * 24 * 180;

  const read = () => {
    const m = document.cookie.match(/(?:^|;\s*)mk_consent=([^;]+)/);
    if (!m) return null;
    try { const v = JSON.parse(decodeURIComponent(m[1])); return v && v.v === 1 ? v : null; } catch { return null; }
  };
  const write = stats => {
    const secure = location.protocol === 'https:' ? '; Secure' : '';
    document.cookie = `${NAME}=${encodeURIComponent(JSON.stringify({ v: 1, stats, t: Date.now() }))}; Max-Age=${MAX_AGE}; Path=/; SameSite=Lax${secure}`;
  };

  // Removes the Google Analytics cookies when the visitor withdraws consent
  const clearGa = () => {
    const host = location.hostname.replace(/^www\./, '');
    document.cookie.split(';').map(c => c.split('=')[0].trim()).filter(n => /^_ga/.test(n)).forEach(n => {
      for (const d of ['', `; Domain=${host}`, `; Domain=.${host}`]) document.cookie = `${n}=; Max-Age=0; Path=/${d}`;
    });
  };

  let gaLoaded = false;
  const loadGa = () => {
    if (!GA || gaLoaded) return;
    gaLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA, { cookie_expires: MAX_AGE, allow_google_signals: false, allow_ad_personalization_signals: false });
    const s = document.createElement('script');
    s.async = true;
    s.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(GA)}`;
    document.head.appendChild(s);
  };

  const box = document.createElement('div');
  box.className = 'cookie';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-labelledby', 'cookie-title');
  box.hidden = true;
  box.innerHTML = `
    <button class="cookie-x" type="button" data-act="reject" aria-label="Chiudi e rifiuta i cookie facoltativi"><i></i><i></i></button>
    <h2 id="cookie-title">Cookie</h2>
    <p>Usiamo un cookie tecnico per ricordare la vostra scelta. Con il vostro consenso usiamo anche cookie statistici, per capire in forma aggregata come viene visitato il sito. Nessun cookie di profilazione o pubblicità. Trovate i dettagli nella <a href="cookie.html">cookie policy</a>.</p>
    <div class="cookie-prefs" hidden>
      <label class="cookie-opt"><span><b>Tecnici</b><small>Necessari al funzionamento del sito. Sempre attivi.</small></span><input type="checkbox" checked disabled><i aria-hidden="true"></i></label>
      <label class="cookie-opt"><span><b>Statistici</b><small>Google Analytics, con dati aggregati sulle visite.</small></span><input type="checkbox" id="cookie-stats"><i aria-hidden="true"></i></label>
    </div>
    <div class="cookie-actions">
      <button class="btn" type="button" data-act="reject"><span>Rifiuta</span></button>
      <button class="btn" type="button" data-act="accept"><span>Accetta tutti</span></button>
      <button class="btn ghost wide" type="button" data-act="custom"><span>Personalizza</span></button>
      <button class="btn ghost wide" type="button" data-act="save" hidden><span>Salva le scelte</span></button>
    </div>`;
  document.body.appendChild(box);

  const prefs = box.querySelector('.cookie-prefs');
  const stats = box.querySelector('#cookie-stats');
  const btn = act => box.querySelector(`.cookie-actions [data-act="${act}"]`);

  const open = custom => {
    const cur = read();
    stats.checked = !!(cur && cur.stats);
    prefs.hidden = !custom;
    btn('custom').hidden = custom;
    btn('save').hidden = !custom;
    box.hidden = false;
    document.body.classList.add('cookie-open');
    requestAnimationFrame(() => box.classList.add('in'));
  };
  let trigger = null;
  const close = () => {
    if (trigger && box.contains(document.activeElement)) trigger.focus();
    trigger = null;
    box.classList.remove('in');
    document.body.classList.remove('cookie-open');
    setTimeout(() => { if (!box.classList.contains('in')) box.hidden = true; }, 300);
  };
  const decide = value => {
    const before = read();
    write(value);
    close();
    if (value) loadGa();
    else if (before && before.stats) { clearGa(); if (gaLoaded) location.reload(); }
  };

  box.addEventListener('click', e => {
    const b = e.target.closest('[data-act]');
    if (!b) return;
    const act = b.dataset.act;
    if (act === 'accept') decide(true);
    else if (act === 'reject') decide(false);
    else if (act === 'save') decide(stats.checked);
    else if (act === 'custom') { open(true); stats.focus(); }
  });
  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape' || box.hidden) return;
    if (read()) close(); else decide(false);
  });

  document.addEventListener('click', e => {
    if (!e.target.closest('[data-cookie-prefs]')) return;
    e.preventDefault();
    trigger = e.target.closest('[data-cookie-prefs]');
    open(true);
    stats.focus();
  });

  const cur = read();
  if (!cur) open(false);
  else if (cur.stats) loadGa();
})();
