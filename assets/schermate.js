/* Merkorn, schermate di esempio nella pagina Come lavoriamo.
   Grafici SVG disegnati alla larghezza reale del contenitore, con tooltip,
   tabella equivalente e animazione di ingresso. Tutti i dati sono inventati. */
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const nf = new Intl.NumberFormat('it-IT');
  const nf1 = new Intl.NumberFormat('it-IT', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  const $ = id => document.getElementById(id);
  if (!$('dash-line')) return;

  const svg = (tag, attrs = {}, parent) => {
    const el = document.createElementNS(NS, tag);
    for (const k in attrs) el.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(el);
    return el;
  };
  const text = (parent, x, y, str, attrs = {}) => { const t = svg('text', { x, y, ...attrs }, parent); t.textContent = str; return t; };
  const niceMax = (v, step) => Math.ceil(v / step) * step;
  // bar with a 4px rounded data end and a square base
  const hBar = (x0, y, w, h, r = 4) => { r = Math.min(r, w, h / 2); return `M${x0},${y}H${x0 + w - r}Q${x0 + w},${y} ${x0 + w},${y + r}V${y + h - r}Q${x0 + w},${y + h} ${x0 + w - r},${y + h}H${x0}Z`; };
  const vBarTop = (x, y, w, h, r = 4) => { r = Math.min(r, h, w / 2); return `M${x},${y + h}V${y + r}Q${x},${y} ${x + r},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + r}V${y + h}Z`; };

  function table(el, head, rows) {
    if (!el) return;
    el.textContent = '';
    const wrap = document.createElement('div'); wrap.className = 'tbl-wrap';
    const t = document.createElement('table'); t.className = 'tbl';
    const tr = document.createElement('tr');
    head.forEach((h, i) => { const th = document.createElement('th'); th.scope = 'col'; th.textContent = h; if (i) th.className = 'num'; tr.appendChild(th); });
    const thead = document.createElement('thead'); thead.appendChild(tr); t.appendChild(thead);
    const tb = document.createElement('tbody');
    rows.forEach(r => { const row = document.createElement('tr'); r.forEach((c, i) => { const td = document.createElement('td'); td.textContent = c; if (i) td.className = 'num'; row.appendChild(td); }); tb.appendChild(row); });
    t.appendChild(tb); wrap.appendChild(t); el.appendChild(wrap);
  }

  // the screens are static illustrations: no tooltips, no hover targets
  const STATIC = true;
  function tooltip(fig) {
    if (STATIC) return { show() {}, hide() {} };
    const tip = document.createElement('div'); tip.className = 'tip'; tip.setAttribute('aria-hidden', 'true');
    fig.appendChild(tip);
    return {
      show(title, rows, x, y) {
        tip.textContent = '';
        const tt = document.createElement('span'); tt.className = 'tt'; tt.textContent = title; tip.appendChild(tt);
        rows.forEach(([label, value, color]) => {
          const r = document.createElement('span'); r.className = 'tr';
          if (color) { const i = document.createElement('i'); i.style.background = color; r.appendChild(i); }
          const b = document.createElement('b'); b.textContent = value; r.appendChild(b);
          r.appendChild(document.createTextNode(label));
          tip.appendChild(r);
        });
        const fr = fig.getBoundingClientRect();
        const w = tip.offsetWidth, h = tip.offsetHeight;
        let left = x + 14, top = y - h - 10;
        if (left + w > fr.width - 8) left = x - w - 14;
        if (left < 8) left = 8;
        if (top < 8) top = y + 16;
        tip.style.left = left + 'px'; tip.style.top = top + 'px';
        tip.classList.add('show');
      },
      hide() { tip.classList.remove('show'); }
    };
  }

  // draw-in: the first time a chart is seen, and again when the period changes.
  // prep() puts the marks in their start state, play() animates them to the end state.
  // After the first reveal a redraw (for example on resize) is shown directly in its end state.
  const seen = new WeakSet();
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    io.unobserve(e.target); seen.add(e.target);
    if (e.target._play) raf2(e.target._play);
  }), { threshold: .3 });
  const raf2 = fn => requestAnimationFrame(() => requestAnimationFrame(fn));
  function anim(el, mode, prep, play) {
    if (reduce) return;
    if (mode === 'now') { seen.add(el); prep(); raf2(play); return; }
    if (seen.has(el)) return;
    prep(); el._play = play; io.observe(el);
  }

  /* ================= cruscotto ================= */
  const MONTHS = ['Ott', 'Nov', 'Dic', 'Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set'];
  const FULL = ['ottobre', 'novembre', 'dicembre', 'gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre'];
  const REV = [142, 151, 168, 129, 138, 156, 161, 170, 175, 163, 118, 184];
  const REV_PREV = [131, 139, 152, 121, 127, 140, 149, 155, 160, 150, 109, 167];
  const ORDERS = [248, 262, 290, 221, 236, 270, 281, 296, 305, 284, 205, 312];
  const LATE = [14, 12, 16, 11, 10, 9, 9, 8, 8, 10, 6, 7];
  const LEAD = [3.4, 3.3, 3.5, 3.1, 3.0, 2.9, 2.8, 2.7, 2.6, 2.6, 2.5, 2.4];
  const CATS = [['Ferramenta', .31], ['Idraulica', .24], ['Elettrico', .19], ['Utensili', .15], ['Giardino', .11]];
  let range = 12;

  const sum = a => a.reduce((x, y) => x + y, 0);
  const nf2 = new Intl.NumberFormat('it-IT', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const euro = k => k >= 1000 ? nf2.format(k / 1000) + ' mln €' : nf.format(k) + '.000 €';

  function tiles() {
    const s = 12 - range;
    const rev = sum(REV.slice(s)), prev = sum(REV_PREV.slice(s)), ord = sum(ORDERS.slice(s)), late = sum(LATE.slice(s));
    const pct = (rev - prev) / prev * 100;
    const lead = LEAD[11], lead0 = LEAD[s];
    const box = $('dash-tiles'); box.textContent = '';
    const tile = (label, value, deltaTxt, deltaCls, note) => {
      const d = document.createElement('div'); d.className = 'tile';
      const l = document.createElement('span'); l.className = 't-label'; l.textContent = label;
      const v = document.createElement('span'); v.className = 't-value'; v.textContent = value;
      const dl = document.createElement('span'); dl.className = 't-delta';
      if (deltaTxt) { const b = document.createElement('b'); b.className = deltaCls; b.textContent = deltaTxt; dl.appendChild(b); }
      dl.appendChild(document.createTextNode(note));
      d.append(l, v, dl); box.appendChild(d);
    };
    tile('Fatturato', euro(rev), (pct >= 0 ? '▲ +' : '▼ ') + nf1.format(pct) + '%', pct >= 0 ? 'good' : 'bad', 'sullo stesso periodo dell\'anno scorso');
    tile('Ordini evasi', nf.format(ord), '', '', 'nel periodo selezionato');
    tile('Consegne in ritardo', nf.format(late), '', '', 'su ' + nf.format(ord) + ' consegne, ' + nf1.format(late / ord * 100) + '%');
    const dLead = lead - lead0;
    tile('Tempo medio di evasione', nf1.format(lead) + ' giorni', dLead <= 0 ? '▼ ' + nf1.format(Math.abs(dLead)) + ' giorni' : '▲ ' + nf1.format(dLead) + ' giorni', dLead <= 0 ? 'good' : 'bad', 'da inizio periodo');
  }

  function lineChart(animate) {
    const host = $('dash-line'), fig = host.closest('figure');
    const s = 12 - range, cur = REV.slice(s), prv = REV_PREV.slice(s), labs = MONTHS.slice(s), full = FULL.slice(s);
    const W = Math.max(280, host.clientWidth), H = 230, m = { l: 36, r: 44, t: 14, b: 26 };
    const iw = W - m.l - m.r, ih = H - m.t - m.b;
    const max = niceMax(Math.max(...cur, ...prv), 50);
    const X = i => m.l + (cur.length === 1 ? iw / 2 : i * iw / (cur.length - 1));
    const Y = v => m.t + ih - v / max * ih;
    host.textContent = '';
    const root = svg('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: 'img', 'aria-label': `Fatturato mensile degli ultimi ${range} mesi, anno in corso e anno precedente` }, host);
    const g = svg('g', { class: 'grid' }, root);
    for (let v = 0; v <= max; v += 50) { svg('line', { x1: m.l, x2: W - m.r, y1: Y(v), y2: Y(v) }, g); text(root, m.l - 8, Y(v) + 4, nf.format(v), { 'text-anchor': 'end' }); }
    svg('line', { class: 'base', x1: m.l, x2: W - m.r, y1: Y(0), y2: Y(0) }, root);
    const every = iw / cur.length < 34 ? 2 : 1;
    labs.forEach((l, i) => { if ((cur.length - 1 - i) % every === 0) text(root, X(i), H - 6, l, { 'text-anchor': 'middle' }); });
    const pts = a => a.map((v, i) => `${X(i)},${Y(v)}`).join(' ');
    svg('polygon', { class: 'area', points: `${X(0)},${Y(0)} ${pts(cur)} ${X(cur.length - 1)},${Y(0)}` }, root);
    const lp = svg('polyline', { class: 'ln s0', points: pts(prv) }, root);
    const lc = svg('polyline', { class: 'ln s1', points: pts(cur) }, root);
    const last = cur.length - 1;
    svg('circle', { class: 'dot s0', cx: X(last), cy: Y(prv[last]), r: 4 }, root);
    svg('circle', { class: 'dot s1', cx: X(last), cy: Y(cur[last]), r: 4 }, root);
    text(root, X(last) + 10, Y(cur[last]) + 4, String(cur[last]), { class: 'endlab' });
    if (Math.abs(Y(cur[last]) - Y(prv[last])) > 14) text(root, X(last) + 10, Y(prv[last]) + 4, String(prv[last]), { class: 'endlab', style: 'fill: var(--v-muted)' });

    // crosshair + tooltip, also reachable with the keyboard
    const cross = svg('line', { class: 'cross', y1: m.t, y2: m.t + ih, opacity: 0 }, root);
    const hc = svg('circle', { class: 'dot s1', r: 4, opacity: 0 }, root), hp = svg('circle', { class: 'dot s0', r: 4, opacity: 0 }, root);
    const hit = svg('rect', { class: 'hit', x: m.l - 10, y: 0, width: iw + 20, height: H }, root);
    const tip = fig._tip || (fig._tip = tooltip(fig));
    let idx = -1;
    const at = i => {
      idx = i;
      [cross].forEach(l => { l.setAttribute('x1', X(i)); l.setAttribute('x2', X(i)); l.setAttribute('opacity', 1); });
      hc.setAttribute('cx', X(i)); hc.setAttribute('cy', Y(cur[i])); hc.setAttribute('opacity', 1);
      hp.setAttribute('cx', X(i)); hp.setAttribute('cy', Y(prv[i])); hp.setAttribute('opacity', 1);
      const hr = host.getBoundingClientRect(), fr = fig.getBoundingClientRect();
      tip.show(full[i].charAt(0).toUpperCase() + full[i].slice(1), [['anno in corso', nf.format(cur[i]) + '.000 €', 'var(--s1)'], ['anno precedente', nf.format(prv[i]) + '.000 €', 'var(--s0)']],
        hr.left - fr.left + X(i) * hr.width / W, hr.top - fr.top + Y(Math.max(cur[i], prv[i])) * hr.width / W);
    };
    const off = () => { idx = -1; cross.setAttribute('opacity', 0); hc.setAttribute('opacity', 0); hp.setAttribute('opacity', 0); tip.hide(); };
    hit.addEventListener('pointermove', e => {
      const r = root.getBoundingClientRect(); const x = (e.clientX - r.left) * W / r.width;
      at(Math.max(0, Math.min(cur.length - 1, Math.round((x - m.l) / (iw / Math.max(1, cur.length - 1))))));
    });
    hit.addEventListener('pointerleave', off);

    // trace the lines
    const lines = [lp, lc];
    anim(host, animate,
      () => lines.forEach(l => { const len = l.getTotalLength(); l.classList.remove('draw'); l.style.strokeDasharray = len; l.style.strokeDashoffset = len; }),
      () => lines.forEach(l => { l.classList.add('draw'); l.style.strokeDashoffset = 0; }));

    table($('dash-line-t'), ['Mese', 'Anno in corso (migliaia di euro)', 'Anno precedente (migliaia di euro)'], cur.map((v, i) => [full[i], nf.format(v), nf.format(prv[i])]));
  }

  function barChart(animate) {
    const host = $('dash-bars'), fig = host.closest('figure');
    const s = 12 - range, total = sum(ORDERS.slice(s));
    const data = CATS.map(([name, share]) => [name, Math.round(total * share)]);
    const W = Math.max(240, host.clientWidth), row = 36, H = data.length * row + 6, lw = 84, vw = 46;
    const iw = W - lw - vw, max = Math.max(...data.map(d => d[1]));
    host.textContent = '';
    const root = svg('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: 'img', 'aria-label': 'Ordini per categoria nel periodo selezionato' }, host);
    svg('line', { class: 'base', x1: lw, x2: lw, y1: 0, y2: H }, root);
    const tip = fig._tip || (fig._tip = tooltip(fig));
    const bars = [];
    data.forEach(([name, v], i) => {
      const y = i * row + (row - 16) / 2, w = Math.max(2, v / max * iw);
      text(root, lw - 10, y + 12, name, { 'text-anchor': 'end', class: 'cat' });
      const p = svg('path', { class: 'm s1 grow', d: hBar(lw, y, w, 16) }, root);
      p.style.transformOrigin = `${lw}px ${y + 8}px`;
      bars.push(p);
      text(root, lw + w + 8, y + 12, nf.format(v), { class: 'val' });
      const hit = svg('rect', { class: 'hit', x: 0, y: i * row, width: W, height: row, tabindex: 0, 'aria-label': `${name}, ${nf.format(v)} ordini` }, root);
      const on = () => {
        root.classList.add('dim'); bars.forEach(b => b.classList.toggle('on', b === p));
        const hr = host.getBoundingClientRect(), fr = fig.getBoundingClientRect(), k = hr.width / W;
        tip.show(name, [['ordini', nf.format(v), 'var(--s1)'], ['del totale', Math.round(v / total * 100) + '%']], hr.left - fr.left + (lw + w) * k, hr.top - fr.top + y * k);
      };
      const offf = () => { root.classList.remove('dim'); tip.hide(); };
      hit.addEventListener('pointerenter', on); hit.addEventListener('pointerleave', offf);
      hit.addEventListener('focus', on); hit.addEventListener('blur', offf);
    });
    anim(host, animate,
      () => bars.forEach(b => { b.style.transition = 'none'; b.style.transform = 'scaleX(0)'; }),
      () => bars.forEach((b, i) => { b.style.transition = ''; b.style.transitionDelay = (i * 60) + 'ms'; b.style.transform = 'scaleX(1)'; }));
    table($('dash-bars-t'), ['Categoria', 'Ordini'], data.map(([n, v]) => [n, nf.format(v)]));
  }

  document.querySelectorAll('[data-range]').forEach(b => b.addEventListener('click', () => {
    if (+b.dataset.range === range) return;
    range = +b.dataset.range;
    document.querySelectorAll('[data-range]').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    tiles(); lineChart('now'); barChart('now');
  }));

  /* ================= magazzino ================= */
  const STOCK = [
    ['A-0021', 'Staffa angolare 40 mm', 36, 80, 400, 'pz'],
    ['A-0022', 'Staffa angolare 60 mm', 142, 80, 400, 'pz'],
    ['B-1140', 'Vite M6 zincata, conf. 100', 12, 40, 200, 'conf.'],
    ['B-1152', 'Vite M8 zincata, conf. 100', 54, 40, 200, 'conf.'],
    ['C-0907', 'Tassello nylon 8 mm', 310, 120, 500, 'pz'],
    ['C-0910', 'Tassello nylon 10 mm', 95, 120, 500, 'pz'],
    ['D-2201', 'Guarnizione 1/2"', 64, 50, 300, 'pz'],
    ['D-2210', 'Raccordo ottone 3/4"', 188, 60, 300, 'pz'],
    ['E-3302', 'Cavo unipolare 2,5 mmq', 420, 300, 1500, 'm'],
    ['E-3310', 'Interruttore unipolare', 27, 30, 150, 'pz'],
  ].map(([code, name, qty, min, max, um]) => ({ code, name, qty, min, max, um, st: qty < min ? 'low' : qty < min * 1.5 ? 'warn' : 'ok' }));
  const ST = {
    low: ['Sotto soglia', 'var(--crit)', '<circle cx="7" cy="7" r="6.5"/><path d="M7 3.5v4.2M7 9.8v.4" stroke="#100E13" stroke-width="1.8" stroke-linecap="round"/>'],
    warn: ['In esaurimento', 'var(--warn)', '<path d="M7 1 13.5 12.5H.5Z"/><path d="M7 5.2v3.3M7 10.3v.3" stroke="#100E13" stroke-width="1.6" stroke-linecap="round"/>'],
    ok: ['Regolare', 'var(--good)', '<circle cx="7" cy="7" r="6.5"/><path d="m4.2 7.2 2 2 3.7-4" fill="none" stroke="#100E13" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>'],
  };
  let stFilter = 'all', query = '';
  function stockTiles() {
    const box = $('stock-tiles'); box.querySelectorAll('.tile').forEach(t => t.remove());
    const low = STOCK.filter(s => s.st === 'low'), warn = STOCK.filter(s => s.st === 'warn');
    [['Sotto soglia', low.length + ' articoli', 'da riordinare subito'], ['In esaurimento', warn.length + ' articoli', 'sotto una volta e mezza la soglia'], ['Riordini suggeriti', nf.format(low.length) + ' ordini', 'pronti da inviare ai fornitori']].forEach(([l, v, n]) => {
      const d = document.createElement('div'); d.className = 'tile';
      d.innerHTML = '<span class="t-label"></span><span class="t-value"></span><span class="t-delta"></span>';
      d.children[0].textContent = l; d.children[1].textContent = v; d.children[2].textContent = n; box.appendChild(d);
    });
  }
  function stockTable() {
    const tb = document.querySelector('#stock-table tbody'); tb.textContent = '';
    const q = query.trim().toLowerCase();
    const rows = STOCK.filter(s => (stFilter === 'all' || s.st === stFilter) && (!q || s.code.toLowerCase().includes(q) || s.name.toLowerCase().includes(q)));
    rows.forEach(s => {
      const tr = document.createElement('tr');
      const td = (cls) => { const c = document.createElement('td'); if (cls) c.className = cls; tr.appendChild(c); return c; };
      td('code').textContent = s.code;
      td('name').textContent = s.name;
      const g = td();
      const bar = document.createElement('span'); bar.className = 'stockbar ' + s.st;
      bar.setAttribute('aria-hidden', 'true');
      const fill = document.createElement('i'); fill.style.width = Math.min(100, s.qty / s.max * 100) + '%';
      const tick = document.createElement('b'); tick.style.left = (s.min / s.max * 100) + '%';
      bar.append(fill, tick); g.appendChild(bar);
      g.appendChild(document.createTextNode(`${nf.format(s.qty)} ${s.um}, min ${nf.format(s.min)}`));
      td('num').textContent = s.st === 'low' ? `${nf.format(s.max - s.qty)} ${s.um}` : '—';
      const st = td(); const [label, color, icon] = ST[s.st];
      const span = document.createElement('span'); span.className = 'badge';
      span.innerHTML = `<svg viewBox="0 0 14 14" aria-hidden="true" fill="${color}">${icon}</svg>`;
      span.appendChild(document.createTextNode(label)); st.appendChild(span);
      tb.appendChild(tr);
    });
    if ($('stock-empty')) $('stock-empty').hidden = rows.length > 0;
  }
  document.querySelectorAll('[data-st]').forEach(b => b.addEventListener('click', () => {
    stFilter = b.dataset.st;
    document.querySelectorAll('[data-st]').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
    stockTable();
  }));

  /* ================= produzione ================= */
  const WEEKS = ['30', '31', '32', '33', '34', '35', '36', '37'];
  const DEPTS = [['Taglio', 'var(--s1)', 's1', [120, 132, 128, 140, 96, 60, 135, 142]], ['Assemblaggio', 'var(--s2)', 's2', [160, 171, 165, 180, 120, 70, 176, 184]], ['Collaudo', 'var(--s3)', 's3', [48, 52, 50, 56, 40, 22, 54, 58]]];
  function columns(animate) {
    const host = $('prod-cols'), fig = host.closest('figure');
    const W = Math.max(280, host.clientWidth), H = 230, m = { l: 36, r: 8, t: 22, b: 26 };
    const iw = W - m.l - m.r, ih = H - m.t - m.b;
    const totals = WEEKS.map((_, i) => sum(DEPTS.map(d => d[3][i])));
    const max = niceMax(Math.max(...totals), 100);
    const band = iw / WEEKS.length, cw = Math.min(24, band * .55);
    const Y = v => m.t + ih - v / max * ih;
    host.textContent = '';
    const root = svg('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: 'img', 'aria-label': 'Ore lavorate per reparto nelle ultime otto settimane' }, host);
    const g = svg('g', { class: 'grid' }, root);
    for (let v = 0; v <= max; v += 100) { svg('line', { x1: m.l, x2: W - m.r, y1: Y(v), y2: Y(v) }, g); text(root, m.l - 8, Y(v) + 4, nf.format(v), { 'text-anchor': 'end' }); }
    svg('line', { class: 'base', x1: m.l, x2: W - m.r, y1: Y(0), y2: Y(0) }, root);
    const tip = fig._tip || (fig._tip = tooltip(fig));
    const segs = [];
    WEEKS.forEach((wk, i) => {
      const x = m.l + band * i + (band - cw) / 2;
      text(root, x + cw / 2, H - 6, 'S' + wk, { 'text-anchor': 'middle' });
      let acc = 0;
      DEPTS.forEach(([name, color, cls, vals], k) => {
        const v = vals[i], y0 = Y(acc), y1 = Y(acc + v);
        const h = Math.max(0, y0 - y1 - (k ? 2 : 0));
        const top = k === DEPTS.length - 1;
        const p = svg('path', { class: `m ${cls} grow`, d: top ? vBarTop(x, y1, cw, h) : `M${x},${y1}h${cw}v${h}h${-cw}Z` }, root);
        p.style.transformOrigin = `${x + cw / 2}px ${Y(0)}px`;
        segs.push(p);
        const hit = svg('rect', { class: 'hit', x: x - (band - cw) / 2, y: y1 - 1, width: band, height: h + 2, tabindex: 0, 'aria-label': `Settimana ${wk}, ${name}, ${v} ore` }, root);
        const on = () => {
          root.classList.add('dim'); segs.forEach(s => s.classList.toggle('on', s === p));
          const hr = host.getBoundingClientRect(), fr = fig.getBoundingClientRect(), kk = hr.width / W;
          tip.show('Settimana ' + wk, [[name.toLowerCase(), nf.format(v) + ' ore', color], ['totale settimana', nf.format(totals[i]) + ' ore']], hr.left - fr.left + (x + cw) * kk, hr.top - fr.top + y1 * kk);
        };
        const off = () => { root.classList.remove('dim'); tip.hide(); };
        hit.addEventListener('pointerenter', on); hit.addEventListener('pointerleave', off);
        hit.addEventListener('focus', on); hit.addEventListener('blur', off);
        acc += v;
      });
      if (band > 30) text(root, x + cw / 2, Y(totals[i]) - 6, nf.format(totals[i]), { 'text-anchor': 'middle', class: 'val' });
    });
    anim(host, animate,
      () => segs.forEach(s => { s.style.transition = 'none'; s.style.transform = 'scaleY(0)'; }),
      () => segs.forEach((s, i) => { s.style.transition = ''; s.style.transitionDelay = (Math.floor(i / 3) * 50) + 'ms'; s.style.transform = 'scaleY(1)'; }));
    table($('prod-cols-t'), ['Settimana', 'Taglio (ore)', 'Assemblaggio (ore)', 'Collaudo (ore)', 'Totale (ore)'], WEEKS.map((w, i) => ['Settimana ' + w, ...DEPTS.map(d => nf.format(d[3][i])), nf.format(totals[i])]));
  }
  const JOBS = [
    ['C-2604', 'Scaffalature magazzino', 82, '3 ottobre', 'ok'],
    ['C-2607', 'Carpenteria capannone', 45, '10 ottobre', 'warn'],
    ['C-2609', 'Ringhiere condominio', 30, '2 ottobre', 'low'],
    ['C-2611', 'Pensilina parcheggio', 64, '24 ottobre', 'ok'],
    ['C-2615', 'Soppalco officina', 12, '7 novembre', 'ok'],
  ];
  const JST = { ok: 'In linea', warn: 'A rischio', low: 'In ritardo' };
  function jobs(animate) {
    const ul = $('prod-jobs'); ul.textContent = '';
    const meters = [];
    JOBS.forEach(([code, name, pct, due, st]) => {
      const li = document.createElement('li');
      li.innerHTML = '<div class="j-top"><b></b><span></span></div><div class="meter" aria-hidden="true"><i></i></div><div class="j-bottom"><span></span><span class="badge"></span></div>';
      li.querySelector('b').textContent = code + ' ' + name;
      li.querySelector('.j-top span').textContent = pct + '%';
      li.querySelector('.j-bottom span').textContent = 'Consegna prevista ' + due;
      const s = li.querySelector('.badge'); const [, color, icon] = ST[st];
      s.innerHTML = `<svg viewBox="0 0 14 14" aria-hidden="true" fill="${color}">${icon}</svg>`;
      s.appendChild(document.createTextNode(JST[st]));
      const m = li.querySelector('.meter i'); m.style.scale = (pct / 100) + ' 1'; meters.push([m, pct]);
      ul.appendChild(li);
    });
    anim(ul, animate,
      () => meters.forEach(([m]) => { m.style.transition = 'none'; m.style.scale = '0 1'; }),
      () => meters.forEach(([m, pct], i) => { m.style.transition = ''; m.style.transitionDelay = (i * 80) + 'ms'; m.style.scale = (pct / 100) + ' 1'; }));
  }

  // orders currently in each production stage
  const FLOW = [['Taglio', 6], ['Assemblaggio', 9], ['Collaudo', 4], ['Spedizione', 3]];
  function flow() {
    const ol = $('prod-flow'); ol.textContent = '';
    const tot = sum(FLOW.map(f => f[1]));
    FLOW.forEach(([name, n]) => {
      const li = document.createElement('li');
      const k = document.createElement('span'); k.className = 'f-k'; k.textContent = name;
      const v = document.createElement('strong'); v.textContent = n + (n === 1 ? ' ordine' : ' ordini');
      const m = document.createElement('div'); m.className = 'meter'; m.setAttribute('aria-hidden', 'true');
      const i = document.createElement('i'); i.style.scale = (n / tot) + ' 1'; m.appendChild(i);
      li.append(k, v, m); ol.appendChild(li);
    });
  }

  /* ================= home ================= */
  // the last 14 working days up to Monday 28 September, the date shown in the dashboard header
  const DAYS = ['9', '10', '11', '14', '15', '16', '17', '18', '21', '22', '23', '24', '25', '28'];
  const DAY_LABEL = DAYS.map(d => d + ' set');
  const DAILY = [12, 15, 11, 17, 14, 13, 16, 19, 15, 12, 14, 17, 20, 18];
  function homeTiles() {
    const box = $('home-tiles'); box.querySelectorAll('.tile').forEach(t => t.remove());
    const low = STOCK.filter(s => s.st === 'low').length;
    [['Ordini di oggi', nf.format(DAILY[DAILY.length - 1]), '▼ 2', 'bad', 'rispetto a ieri'],
     ['Consegne in giro', '9 di 14', '', '', 'completate oggi'],
     ['Incassi della settimana', '42.300 €', '▲ +8,4%', 'good', 'sulla settimana scorsa'],
     ['Articoli sotto soglia', String(low), '', '', 'da riordinare']].forEach(([l, v, d, cls, note]) => {
      const t = document.createElement('div'); t.className = 'tile';
      const a = document.createElement('span'); a.className = 't-label'; a.textContent = l;
      const b = document.createElement('span'); b.className = 't-value'; b.textContent = v;
      const c = document.createElement('span'); c.className = 't-delta';
      if (d) { const x = document.createElement('b'); x.className = cls; x.textContent = d; c.appendChild(x); }
      c.appendChild(document.createTextNode(note));
      t.append(a, b, c); box.appendChild(t);
    });
  }
  function homeCols(animate) {
    const host = $('home-cols'), fig = host.closest('figure');
    const W = Math.max(260, host.clientWidth), H = 200, m = { l: 30, r: 6, t: 20, b: 24 };
    const iw = W - m.l - m.r, ih = H - m.t - m.b, max = niceMax(Math.max(...DAILY), 5);
    const band = iw / DAILY.length, cw = Math.min(24, band * .6);
    const Y = v => m.t + ih - v / max * ih;
    host.textContent = '';
    const root = svg('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: 'img', 'aria-label': 'Ordini ricevuti al giorno negli ultimi 14 giorni lavorativi' }, host);
    const g = svg('g', { class: 'grid' }, root);
    for (let v = 0; v <= max; v += 5) { svg('line', { x1: m.l, x2: W - m.r, y1: Y(v), y2: Y(v) }, g); text(root, m.l - 8, Y(v) + 4, String(v), { 'text-anchor': 'end' }); }
    svg('line', { class: 'base', x1: m.l, x2: W - m.r, y1: Y(0), y2: Y(0) }, root);
    const tip = fig._tip || (fig._tip = tooltip(fig));
    const bars = [];
    const every = band < 26 ? 2 : 1;
    DAILY.forEach((v, i) => {
      const x = m.l + band * i + (band - cw) / 2;
      const p = svg('path', { class: 'm s1 grow', d: vBarTop(x, Y(v), cw, Y(0) - Y(v)) }, root);
      p.style.transformOrigin = `${x + cw / 2}px ${Y(0)}px`;
      bars.push(p);
      if ((DAILY.length - 1 - i) % every === 0) text(root, x + cw / 2, H - 6, DAYS[i], { 'text-anchor': 'middle' });
      const hit = svg('rect', { class: 'hit', x: m.l + band * i, y: m.t, width: band, height: ih, tabindex: 0, 'aria-label': `${DAY_LABEL[i]}, ${v} ordini` }, root);
      const on = () => {
        root.classList.add('dim'); bars.forEach(b => b.classList.toggle('on', b === p));
        const hr = host.getBoundingClientRect(), fr = fig.getBoundingClientRect(), k = hr.width / W;
        tip.show(DAY_LABEL[i], [['ordini', String(v), 'var(--s1)']], hr.left - fr.left + (x + cw) * k, hr.top - fr.top + Y(v) * k);
      };
      const off = () => { root.classList.remove('dim'); tip.hide(); };
      hit.addEventListener('pointerenter', on); hit.addEventListener('pointerleave', off);
      hit.addEventListener('focus', on); hit.addEventListener('blur', off);
    });
    const li = DAILY.length - 1, xl = m.l + band * li + band / 2;
    text(root, xl, Y(DAILY[li]) - 6, String(DAILY[li]), { 'text-anchor': 'middle', class: 'val' });
    anim(host, animate,
      () => bars.forEach(b => { b.style.transition = 'none'; b.style.transform = 'scaleY(0)'; }),
      () => bars.forEach((b, i) => { b.style.transition = ''; b.style.transitionDelay = (i * 30) + 'ms'; b.style.transform = 'scaleY(1)'; }));
    table($('home-cols-t'), ['Giorno', 'Ordini'], DAILY.map((v, i) => [DAY_LABEL[i], String(v)]));
  }
  function homeTodo() {
    const ul = $('home-todo'); ul.textContent = '';
    const low = STOCK.filter(s => s.st === 'low').length;
    [[`${low} articoli sotto soglia da riordinare`, 'low', 'stock'],
     ['1 commessa in ritardo, 1 a rischio', 'warn', 'prod'],
     ['Fatturato di settembre sopra l\'anno scorso', 'ok', 'analytics'],
     ['5 consegne ancora da completare', 'warn']].forEach(([label, st]) => {
      const li = document.createElement('li');
      const [, color, ico] = ST[st];
      li.innerHTML = `<svg viewBox="0 0 14 14" aria-hidden="true" fill="${color}">${ico}</svg>`;
      const s = document.createElement('span'); s.textContent = label; li.appendChild(s);
      ul.appendChild(li);
    });
  }

  /* ================= avvio e ridimensionamento ================= */
  // all four screens are visible at once, each chart draws itself when it scrolls into view
  function drawCharts() {
    homeCols(); lineChart(); barChart(); columns(); jobs();
    // static screens: drop the hover targets so nothing inside a screen can take focus
    document.querySelectorAll('.app .hit').forEach(h => h.remove());
  }
  tiles(); stockTiles(); stockTable(); flow(); homeTiles(); homeTodo();
  drawCharts();
  let rw = 0, t;
  const ro = new ResizeObserver(() => {
    const w = document.querySelector('.dash-main').clientWidth;
    if (w === rw) return; rw = w;
    clearTimeout(t); t = setTimeout(drawCharts, 120);
  });
  ro.observe(document.querySelector('.dash-main'));
})();
