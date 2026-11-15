/* Merkorn, proposte: one particle system that morphs between shapes as the page scrolls.
   Usage: MorphScene(container, [shapeName, ...], options). Shapes are generated below. */
(() => {
  const TAU = Math.PI * 2, rnd = Math.random;
  const sprite = () => {
    const c = document.createElement('canvas'); c.width = c.height = 64;
    const g = c.getContext('2d'), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.3, 'rgba(255,255,255,.8)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 64, 64);
    return new THREE.CanvasTexture(c);
  };

  // point on the surface or edge of a box centred at (cx,cy,cz)
  const boxPoint = (cx, cy, cz, sx, sy, sz, edge) => {
    let p = [rnd() - .5, rnd() - .5, rnd() - .5];
    if (edge) { const a = Math.floor(rnd() * 3); const b = (a + 1) % 3; p[a] = rnd() < .5 ? -.5 : .5; p[b] = rnd() < .5 ? -.5 : .5; }
    else if (rnd() < .8) { const a = Math.floor(rnd() * 3); p[a] = rnd() < .5 ? -.5 : .5; }
    return [cx + p[0] * sx, cy + p[1] * sy, cz + p[2] * sz];
  };
  const MARK = [[2, 0], [1, 1], [3, 1], [0, 2], [4, 2]];
  const fill = (N, fn) => { const a = new Float32Array(N * 3); for (let i = 0; i < N; i++) a.set(fn(i, N), i * 3); return a; };

  const SHAPES = {
    chaos: N => fill(N, i => {
      if (i % 7 === 0) { // little clumps, like scattered sheets of paper
        const k = (i * 13) % 23, cx = Math.sin(k * 7.1) * 7, cy = Math.cos(k * 3.7) * 3.6, cz = Math.sin(k * 1.9) * 3;
        return [cx + (rnd() - .5) * .9, cy + (rnd() - .5) * .6, cz + (rnd() - .5) * .05];
      }
      return [(rnd() - .5) * 20, (rnd() - .5) * 11, (rnd() - .5) * 10 - 1];
    }),
    logo: N => fill(N, i => { const [cx, cy] = MARK[i % 5]; return boxPoint((cx - 2) * 1.12, (1 - cy) * 1.14, 0, 1, 1, 1, rnd() < .3); }),
    row: N => fill(N, i => { const k = i % 5; return boxPoint((k - 2) * 2.3, 0, 0, 1.3, 1.3, 1.3, rnd() < .3); }),
    bars: N => {
      const h = [1.1, 1.7, 1.4, 2.4, 2.1, 3.3];
      return fill(N, i => {
        if (i % 9 === 0) return [(rnd() - .5) * 7.4, -1.6, (rnd() - .5) * 2.4]; // floor grid
        const k = i % 6, x = (k - 2.5) * 1.15;
        return boxPoint(x, -1.6 + h[k] / 2, 0, .7, h[k], .7, rnd() < .25);
      });
    },
    timeline: N => fill(N, i => {
      if (i % 3 === 0) { const t = rnd(); return [(t - .5) * 8, Math.sin(t * TAU) * .25, (rnd() - .5) * .06]; }
      const k = i % 4, x = (k - 1.5) * 2.66, y = Math.sin(((k + .5) / 4 + 0) * TAU) * .25 * 0 + 0;
      const u = rnd() * 2 - 1, th = rnd() * TAU, r = Math.sqrt(1 - u * u), R = k === 3 ? .55 : .42;
      return [x + Math.cos(th) * r * R, y + u * R, Math.sin(th) * r * R];
    }),
    puglia: N => {
      const P = [[15.0,41.9],[15.6,41.93],[16.0,41.95],[16.2,41.9],[16.17,41.75],[15.95,41.62],[16.4,41.32],[16.9,41.12],[17.3,40.95],[17.9,40.68],[18.3,40.42],[18.52,40.14],[18.37,39.8],[18.0,40.05],[17.75,40.3],[17.2,40.42],[16.9,40.47],[16.75,40.65],[16.4,40.75],[16.0,41.0],[15.55,41.05],[15.2,41.25],[14.95,41.5]];
      const pr = ([lo, la]) => [(lo - 16.75) * 1.5, (la - 40.88) * 2.0];
      const poly = P.map(pr), [mx, my] = pr([17.04, 40.63]);
      const inside = (x, y) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const [xi, yi] = poly[i], [xj, yj] = poly[j]; if ((yi > y) !== (yj > y) && x < (xj - xi) * (y - yi) / (yj - yi) + xi) c = !c; } return c; };
      return fill(N, i => {
        if (i % 6 === 0) { const a = rnd() * TAU, r = Math.pow(rnd(), 2) * .35; return [mx + Math.cos(a) * r, my + Math.sin(a) * r, .1 + rnd() * .3]; }
        if (i % 4 === 0) { const s = Math.floor(rnd() * poly.length), [x1, y1] = poly[s], [x2, y2] = poly[(s + 1) % poly.length], t = rnd(); return [x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, 0]; }
        for (;;) { const x = (rnd() - .5) * 8, y = (rnd() - .5) * 5.4; if (inside(x, y)) return [x, y, (rnd() - .5) * .15]; }
      });
    },
    form: N => fill(N, i => {
      const rows = [[-1.6, 1.9, 3.2, .62], [1.6, 1.9, 3.2, .62], [0, .95, 6.4, .62], [0, -.55, 6.4, 1.6], [-2.2, -2.05, 2, .62]];
      const k = i % 5, [cx, cy, w, h] = rows[k];
      if (k === 4) return [cx + (rnd() - .5) * w, cy + (rnd() - .5) * h, (rnd() - .5) * .1]; // filled button
      const per = 2 * (w + h), d = rnd() * per; let x, y;
      if (d < w) { x = d - w / 2; y = h / 2; } else if (d < w + h) { x = w / 2; y = h / 2 - (d - w); } else if (d < 2 * w + h) { x = w / 2 - (d - w - h); y = -h / 2; } else { x = -w / 2; y = -h / 2 + (d - 2 * w - h); }
      return [cx + x, cy + y, (rnd() - .5) * .05];
    }),
  };

  window.MorphScene = (box, names, opt = {}) => {
    if (!window.THREE) return null;
    const N = opt.count || 14000, reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let renderer; try { renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true }); } catch (e) { return null; }
    renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 2)); box.appendChild(renderer.domElement);
    const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(opt.fov || 40, 1, .1, 100);
    camera.position.set(0, 0, opt.distance || 12);
    const targets = names.map(n => SHAPES[n](N));
    const pos = new Float32Array(targets[0]), col = new Float32Array(N * 3), delay = new Float32Array(N);
    const ivory = [0.95, 0.94, 0.92], violet = [0.79, 0.64, 1], deep = [0.59, 0.28, 1];
    for (let i = 0; i < N; i++) {
      const r = rnd(), c = r < .08 ? deep : r < .2 ? violet : ivory, f = .5 + rnd() * .5;
      col.set([c[0] * f, c[1] * f, c[2] * f], i * 3); delay[i] = rnd();
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('color', new THREE.BufferAttribute(col, 3));
    const mat = new THREE.PointsMaterial({ size: opt.size || .05, map: sprite(), vertexColors: true, transparent: true, opacity: .95, depthWrite: false, blending: THREE.AdditiveBlending });
    const pts = new THREE.Points(g, mat), group = new THREE.Group(); group.add(pts); scene.add(group);
    const size = () => { const w = box.clientWidth, h = box.clientHeight; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); };
    size(); addEventListener('resize', size);
    let mx = 0, my = 0; addEventListener('pointermove', e => { mx = e.clientX / innerWidth - .5; my = e.clientY / innerHeight - .5; });
    const api = { progress: 0, group, camera };
    const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    const t0 = performance.now();
    const frame = now => {
      const t = (now - t0) / 1000, p = Math.max(0, Math.min(names.length - 1, api.progress));
      const a = Math.floor(p), b = Math.min(names.length - 1, a + 1), f = p - a;
      const A = targets[a], B = targets[b];
      for (let i = 0; i < N; i++) {
        const k = ease(Math.max(0, Math.min(1, (f - delay[i] * .35) / .65)));
        const j = i * 3, w = Math.sin(t * 1.3 + i) * .012;
        pos[j] = A[j] + (B[j] - A[j]) * k + w; pos[j + 1] = A[j + 1] + (B[j + 1] - A[j + 1]) * k + w; pos[j + 2] = A[j + 2] + (B[j + 2] - A[j + 2]) * k;
      }
      g.attributes.position.needsUpdate = true;
      const spin = opt.spin == null ? 1 : opt.spin;
      group.rotation.y += ((Math.sin(t * .3) * .45 * spin + mx * .5) - group.rotation.y) * .05;
      group.rotation.x += ((Math.sin(t * .23) * .15 * spin + my * .3 - .05) - group.rotation.x) * .05;
      if (opt.offsetX) group.position.x = opt.offsetX();
      renderer.render(scene, camera);
      requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
    if (reduce) mat.size *= 1;
    return api;
  };
})();
