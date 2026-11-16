/* Merkorn, blocchi che si fondono.
   A grid of rounded squares drawn on a canvas; an SVG "goo" filter (blur + alpha threshold)
   melts neighbouring blocks together with soft bridges when they grow.
   Light on purpose: grids out of view do nothing, frames are capped at 30 per second
   and drop to 15 while the page is scrolling, so blocks keep moving without slowing the scroll down.
   Usage: Goo(element, { cols, rows, pattern, cursor, animate, accent: [[c, r]] }) */
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const MARK = [[2, 0], [1, 1], [3, 1], [0, 2], [4, 2]];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const FRAME = 1000 / 30, FRAME_SCROLLING = 1000 / 15;
  let uid = 0;
  const hash = (a, b, c) => { const x = Math.sin(a * 127.1 + b * 311.7 + c * 74.7) * 43758.5453; return x - Math.floor(x); };

  const PATTERNS = {
    logo: (c, r, t, g) => g.inMark(c, r) ? 1.26 + .05 * Math.sin(t * 2.4 + c) : .34 + .16 * Math.sin(t * 2 + c * .9 + r * .7),
    wave: (c, r, t) => .62 + .58 * Math.sin(c * .7 + r * .45 - t * 1.4),
    rings: (c, r, t, g) => { const d = Math.hypot(c - (g.cols - 1) / 2, r - (g.rows - 1) / 2); return .6 + .62 * Math.sin(d * 1.15 - t * 1.8); },
    diag: (c, r, t) => .52 + .66 * Math.sin((c - r) * .95 - t * 1.2),
    drops: (c, r, t, g) => { const d = (c + (g.rows - 1 - r)) / (g.cols + g.rows - 2); return 1.38 - d * 1.15 + .12 * Math.sin(t * 2 + c + r); },
    // every block changes size at its own moment, so the grid is always moving from the first frame
    mosaic: (c, r, t) => { const e = Math.floor(t / 1.6 + hash(c, r, 0) * 1.6), h = hash(c, r, e); return (h < .34 ? 1.24 : h < .7 ? .98 : .55) + .06 * Math.sin(t * 2.2 + c + r); },
    checker: (c, r, t) => ((c + r) % 2 ? 1.18 : .55) + .18 * Math.sin(t * 2.4 + c + r * .7),
    breathe: (c, r, t) => .8 + .3 * Math.sin(t * 1.6 + (c + r) * .5),
  };
  const CYCLE = ['mosaic', 'logo', 'wave', 'logo', 'diag', 'logo'];

  // one shared listener for scrolling and one for the pointer, instead of one per grid
  const all = [];
  let scrolling = false, stillTimer = 0, mx = -1e4, my = -1e4;
  addEventListener('scroll', () => {
    scrolling = true; all.forEach(i => i.moved());
    clearTimeout(stillTimer);
    stillTimer = setTimeout(() => { scrolling = false; }, 120);
  }, { passive: true });
  addEventListener('pointermove', e => { mx = e.clientX; my = e.clientY; }, { passive: true });

  window.Goo = function (el, opt = {}) {
    const o = Object.assign({ cols: 6, rows: 6, pattern: 'cycle', cursor: true, animate: true, scroll: false, fill: .74, radius: .3, accent: [], speed: 1, gap: .07 }, opt);
    const css = getComputedStyle(el);
    const color = o.color || css.getPropertyValue('--goo').trim() || '#100E13';
    const accentColor = o.accentColor || css.getPropertyValue('--accent').trim() || '#9747FF';
    if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
    const id = 'goo' + (uid++);
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', '0'); svg.setAttribute('height', '0'); svg.setAttribute('aria-hidden', 'true');
    svg.style.cssText = 'position:absolute;width:0;height:0';
    svg.innerHTML = `<filter id="${id}" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="6"/><feColorMatrix values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 26 -11"/></filter>`;
    document.body.appendChild(svg);
    const blur = svg.querySelector('feGaussianBlur');
    const layer = () => { const c = document.createElement('canvas'); c.style.cssText = 'position:absolute;inset:0;display:block;width:100%;height:100%;pointer-events:none'; c.style.filter = `url(#${id})`; el.appendChild(c); return c; };
    const cv = layer(), x = cv.getContext('2d');
    // the violet block sits on its own layer so its colour stays clean; only grids that can show it get one
    const needsAccent = o.accent.length > 0 || o.pattern === 'logo' || o.pattern === 'cycle';
    const cv2 = needsAccent ? layer() : null, x2 = cv2 && cv2.getContext('2d');

    const g = { cols: o.cols, rows: o.rows, cell: 10, ox: 0, oy: 0 };
    let mc = 0, ac = 0; const mr = Math.floor((o.rows - 3) / 2);
    g.inMark = (c, r) => MARK.some(([a, b]) => a + mc === c && b + mr === r);
    const isAccent = (c, r, pat) => needsAccent && (o.accent.some(([a, b]) => a + ac === c && b === r) || (pat === 'logo' && c === 2 + mc && r === mr));
    let cells = [];
    // a box wider than the grid gets extra columns, so the blocks reach both edges
    const setCols = n => {
      if (cells.length && n === g.cols) return;
      const old = new Map(cells.map(k => [k.c + ',' + k.r, k.s]));
      g.cols = n; mc = Math.floor((n - 5) / 2); ac = Math.floor((n - o.cols) / 2);
      cells = [];
      for (let r = 0; r < o.rows; r++) for (let c = 0; c < n; c++) cells.push({ c, r, s: old.get(c + ',' + r) ?? .4 });
    };
    setCols(o.cols);
    const minS = o.cols * o.rows <= 9 ? .5 : .12;

    let pattern = o.pattern, w = 0, h = 0, dpr = 1, ready = false, clock = o.time || 0, rect = null;
    const size = () => {
      dpr = Math.min(devicePixelRatio || 1, 1.5); w = el.clientWidth; h = el.clientHeight;
      for (const c of [cv, cv2]) if (c) { c.width = Math.max(1, Math.round(w * dpr)); c.height = Math.max(1, Math.round(h * dpr)); }
      if (o.fit !== false && h > 0) setCols(Math.max(o.cols, Math.round(w / (h / o.rows))));
      g.cell = Math.min(w / g.cols, h / o.rows); g.ox = (w - g.cell * g.cols) / 2; g.oy = (h - g.cell * o.rows) / 2;
      blur.setAttribute('stdDeviation', (g.cell * o.gap).toFixed(2));
      rect = null;
      if (ready) draw(clock, true);
    };
    size();
    if ('ResizeObserver' in window) new ResizeObserver(size).observe(el); else addEventListener('resize', size);

    const current = t => pattern === 'cycle' ? CYCLE[Math.floor(t / 3.6) % CYCLE.length] : pattern;
    const draw = (t, snap) => {
      const pat = current(t), fn = PATTERNS[pat] || PATTERNS.wave;
      let px = -1e4, py = -1e4, near = false;
      if (o.cursor) {
        rect = rect || el.getBoundingClientRect();
        if (mx >= rect.left && mx <= rect.right && my >= rect.top && my <= rect.bottom) { near = true; px = (mx - rect.left - g.ox) / g.cell - .5; py = (my - rect.top - g.oy) / g.cell - .5; }
      }
      x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, w, h); x.fillStyle = color;
      if (x2) { x2.setTransform(dpr, 0, 0, dpr, 0, 0); x2.clearRect(0, 0, w, h); x2.fillStyle = accentColor; }
      x.beginPath();
      for (const k of cells) {
        let target = fn(k.c, k.r, t, g);
        if (near) target += .5 * Math.exp(-((k.c - px) ** 2 + (k.r - py) ** 2) / 2.2);
        target = target < minS ? minS : target > 1.32 ? 1.32 : target;
        k.s = snap ? target : k.s + (target - k.s) * .22;
        const side = g.cell * o.fill * k.s, cx = g.ox + (k.c + .5) * g.cell, cy = g.oy + (k.r + .5) * g.cell;
        if (isAccent(k.c, k.r, pat)) { x2.beginPath(); x2.roundRect ? x2.roundRect(cx - side / 2, cy - side / 2, side, side, side * o.radius) : x2.rect(cx - side / 2, cy - side / 2, side, side); x2.fill(); continue; }
        x.roundRect ? x.roundRect(cx - side / 2, cy - side / 2, side, side, side * o.radius) : x.rect(cx - side / 2, cy - side / 2, side, side);
      }
      x.fill(); // all blocks in one fill call
    };
    ready = true;

    const live = o.animate && !reduce;
    let visible = true, raf = 0, last = 0;
    const loop = now => {
      raf = 0;
      if (!visible) return;
      const dt = now - last;
      if (dt >= (scrolling && !o.scroll ? FRAME_SCROLLING : FRAME)) { if (last) clock += Math.min(dt, 100) / 1000 * o.speed; last = now; draw(clock); }
      raf = requestAnimationFrame(loop);
    };
    const inst = {
      moved() { rect = null; },
      pause() { if (raf) cancelAnimationFrame(raf); raf = 0; last = 0; rect = null; },
      resume() { if (live && visible && !raf) raf = requestAnimationFrame(loop); },
    };
    all.push(inst);
    if ('IntersectionObserver' in window) new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible) inst.resume(); else inst.pause(); }).observe(el);
    requestAnimationFrame(() => { draw(clock, true); inst.resume(); });

    return {
      setPattern(p) { pattern = p; if (!live) draw(0, true); },
      get pattern() { return pattern; },
    };
  };

  // any element with data-goo="pattern" becomes a grid; data-cols / data-rows / data-static / data-cursor
  window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-goo]').forEach(el => {
      const d = el.dataset;
      Goo(el, { pattern: d.goo, cols: +d.cols || 3, rows: +d.rows || 3, cursor: d.cursor === '1', animate: d.static !== '1', speed: +d.speed || 1, time: +d.time || 0, accent: d.accent ? [d.accent.split(',').map(Number)] : [] });
    });
  });
})();
