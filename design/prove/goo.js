/* Merkorn, blocchi che si fondono.
   A grid of rounded squares drawn on a canvas; an SVG "goo" filter (blur + alpha threshold)
   melts neighbouring blocks together with soft bridges when they grow.
   Usage: Goo(element, { cols, rows, pattern, cursor, animate, accent: [[c, r]] }) */
(() => {
  const NS = 'http://www.w3.org/2000/svg';
  const MARK = [[2, 0], [1, 1], [3, 1], [0, 2], [4, 2]];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let uid = 0;
  const hash = (a, b, c) => { const x = Math.sin(a * 127.1 + b * 311.7 + c * 74.7) * 43758.5453; return x - Math.floor(x); };

  const PATTERNS = {
    logo: (c, r, t, g) => g.inMark(c, r) ? 1.3 : .32 + .1 * Math.sin(t * 2 + c * .9 + r * .7),
    wave: (c, r, t) => .62 + .58 * Math.sin(c * .7 + r * .45 - t * 1.4),
    rings: (c, r, t, g) => { const d = Math.hypot(c - (g.cols - 1) / 2, r - (g.rows - 1) / 2); return .6 + .62 * Math.sin(d * 1.15 - t * 1.8); },
    diag: (c, r, t) => .52 + .66 * Math.sin((c - r) * .95 - t * 1.2),
    drops: (c, r, t, g) => { const d = (c + (g.rows - 1 - r)) / (g.cols + g.rows - 2); return 1.38 - d * 1.15 + .12 * Math.sin(t * 2 + c + r); },
    mosaic: (c, r, t) => { const e = Math.floor(t / 2.2), h = hash(c, r, e); return h < .34 ? 1.24 : h < .7 ? .98 : .55; },
    checker: (c, r, t) => ((c + r) % 2 ? 1.24 : .5) + .1 * Math.sin(t * 2.4 + c),
    breathe: (c, r, t) => .8 + .3 * Math.sin(t * 1.6 + (c + r) * .5),
  };
  const CYCLE = ['mosaic', 'logo', 'wave', 'logo', 'diag', 'logo'];

  window.Goo = function (el, opt = {}) {
    const o = Object.assign({ cols: 6, rows: 6, pattern: 'cycle', cursor: true, animate: true, fill: .74, radius: .3, accent: [], speed: 1, gap: .07 }, opt);
    const css = getComputedStyle(el);
    const color = o.color || css.getPropertyValue('--goo').trim() || '#100E13';
    const accentColor = o.accentColor || css.getPropertyValue('--accent').trim() || '#9747FF';
    const cv = document.createElement('canvas');
    cv.style.cssText = 'display:block;width:100%;height:100%';
    el.appendChild(cv);
    const id = 'goo' + (uid++);
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', '0'); svg.setAttribute('height', '0'); svg.setAttribute('aria-hidden', 'true');
    svg.style.cssText = 'position:absolute;width:0;height:0';
    svg.innerHTML = `<filter id="${id}" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="6"/><feColorMatrix values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 26 -11"/></filter>`;
    document.body.appendChild(svg);
    const blur = svg.querySelector('feGaussianBlur');
    cv.style.filter = `url(#${id})`;
    const x = cv.getContext('2d');
    // accent blocks live on their own layer, so the colour stays crisp after the goo filter
    el.style.position = el.style.position || (getComputedStyle(el).position === 'static' ? 'relative' : '');
    const cv2 = document.createElement('canvas');
    cv2.style.cssText = 'position:absolute;inset:0;display:block;width:100%;height:100%;pointer-events:none';
    cv2.style.filter = `url(#${id})`;
    el.appendChild(cv2);
    const x2 = cv2.getContext('2d');

    const g = { cols: o.cols, rows: o.rows, cell: 10, ox: 0, oy: 0 };
    const mc = Math.floor((o.cols - 5) / 2), mr = Math.floor((o.rows - 3) / 2);
    g.inMark = (c, r) => MARK.some(([a, b]) => a + mc === c && b + mr === r);
    const isAccent = (c, r, pat) => o.accent.some(([a, b]) => a === c && b === r) || (pat === 'logo' && c === 2 + mc && r === mr);
    const cells = [];
    for (let r = 0; r < o.rows; r++) for (let c = 0; c < o.cols; c++) cells.push({ c, r, s: .4 });

    let pattern = o.pattern, w = 0, h = 0, dpr = 1, ready = false, lastT = o.time || 0;
    const size = () => {
      dpr = Math.min(devicePixelRatio || 1, 2); w = el.clientWidth; h = el.clientHeight;
      cv.width = cv2.width = Math.max(1, w * dpr); cv.height = cv2.height = Math.max(1, h * dpr);
      g.cell = Math.min(w / o.cols, h / o.rows); g.ox = (w - g.cell * o.cols) / 2; g.oy = (h - g.cell * o.rows) / 2;
      blur.setAttribute('stdDeviation', (g.cell * o.gap).toFixed(2));
      if (ready) draw(lastT, true);
    };
    size(); addEventListener('resize', size);
    if ('ResizeObserver' in window) new ResizeObserver(size).observe(el);

    let px = -999, py = -999, pin = 0;
    if (o.cursor) {
      addEventListener('pointermove', e => { const b = cv.getBoundingClientRect(); px = (e.clientX - b.left - g.ox) / g.cell - .5; py = (e.clientY - b.top - g.oy) / g.cell - .5; pin = (e.clientX >= b.left && e.clientX <= b.right && e.clientY >= b.top && e.clientY <= b.bottom) ? 1 : 0; }, { passive: true });
    }

    const current = t => pattern === 'cycle' ? CYCLE[Math.floor(t / 3.6) % CYCLE.length] : pattern;
    const draw = (t, snap) => {
      lastT = t;
      const pat = current(t), fn = PATTERNS[pat] || PATTERNS.wave;
      x.setTransform(dpr, 0, 0, dpr, 0, 0); x.clearRect(0, 0, w, h);
      x2.setTransform(dpr, 0, 0, dpr, 0, 0); x2.clearRect(0, 0, w, h);
      for (const k of cells) {
        let target = fn(k.c, k.r, t, g);
        if (o.cursor && pin) { const d2 = (k.c - px) ** 2 + (k.r - py) ** 2; target += .5 * Math.exp(-d2 / 2.2); }
        target = Math.max(o.cols * o.rows <= 9 ? .5 : .12, Math.min(1.32, target));
        k.s = snap ? target : k.s + (target - k.s) * .085;
        const side = g.cell * o.fill * k.s, cx = g.ox + (k.c + .5) * g.cell, cy = g.oy + (k.r + .5) * g.cell;
        const acc = isAccent(k.c, k.r, pat), ctx = acc ? x2 : x;
        ctx.fillStyle = acc ? accentColor : color;
        ctx.beginPath();
        if (ctx.roundRect) ctx.roundRect(cx - side / 2, cy - side / 2, side, side, side * o.radius); else ctx.rect(cx - side / 2, cy - side / 2, side, side);
        ctx.fill();
      }
    };

    ready = true;
    let visible = true, t0 = performance.now(), raf = 0;
    if ('IntersectionObserver' in window) new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible && !raf && o.animate && !reduce) raf = requestAnimationFrame(loop); }).observe(el);
    const loop = now => { raf = 0; if (!visible) return; draw((now - t0) / 1000 * o.speed); raf = requestAnimationFrame(loop); };
    if (o.animate && !reduce) raf = requestAnimationFrame(loop); else requestAnimationFrame(() => draw(o.time || 0, true));

    return {
      setPattern(p) { pattern = p; if (!o.animate || reduce) draw(0, true); },
      get pattern() { return pattern; },
    };
  };

  // any element with data-goo="pattern" becomes a small grid; data-cols / data-rows / data-static
  window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-goo]').forEach(el => {
      const d = el.dataset;
      Goo(el, { pattern: d.goo, cols: +d.cols || 3, rows: +d.rows || 3, cursor: d.cursor === '1', animate: d.static !== '1', speed: +d.speed || 1, time: +d.time || 0, accent: d.accent ? [d.accent.split(',').map(Number)] : [] });
    });
  });
})();
