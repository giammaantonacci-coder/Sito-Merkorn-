/* Mini dashboard modulare della pagina 404: i moduli si trascinano per cambiare ordine,
   si eliminano con la X e si ripristinano. Funziona con mouse, dito e tastiera. */
(() => {
  const grid = document.querySelector('.dash');
  if (!grid) return;
  const tray = document.querySelector('.dash-tray');
  const reset = document.querySelector('[data-dash-reset]');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const original = [...grid.children].map(el => el.cloneNode(true));

  // animate the cards from where they were to where they are now
  const flip = mutate => {
    const cards = [...grid.querySelectorAll('.mod:not(.lift)')];
    const before = new Map(cards.map(c => [c, c.getBoundingClientRect()]));
    mutate();
    if (reduce) return;
    cards.forEach(c => {
      const a = before.get(c), b = c.getBoundingClientRect();
      if (!a || !c.isConnected) return;
      const dx = a.left - b.left, dy = a.top - b.top;
      if (!dx && !dy) return;
      c.animate([{ transform: `translate(${dx}px, ${dy}px)` }, { transform: 'none' }], { duration: 260, easing: 'cubic-bezier(.2,.8,.2,1)' });
    });
  };

  const status = document.querySelector('.dash-status');
  const say = t => { if (status) status.textContent = t; };
  const name = w => w.querySelector('.mod-title').textContent;

  const sync = () => {
    const empty = !grid.querySelector('.mod');
    grid.classList.toggle('empty', empty);
    if (reset) reset.hidden = grid.children.length === original.length && [...grid.children].every((c, i) => c.dataset.id === original[i].dataset.id);
  };

  /* ---- delete ---- */
  const remove = w => {
    const label = name(w);
    let gone = false;
    const done = () => {
      if (gone) return; gone = true;
      flip(() => w.remove());
      if (tray) {
        const chip = document.createElement('button');
        chip.type = 'button'; chip.className = 'chip'; chip.dataset.id = w.dataset.id;
        chip.innerHTML = `<span aria-hidden="true">+</span> ${label}`;
        tray.querySelector('.chips').appendChild(chip);
        tray.hidden = false;
      }
      say(`${label} eliminato`);
      sync();
      const next = grid.querySelector('.mod .mod-move'); if (next) next.focus({ preventScroll: true });
    };
    if (reduce) return done();
    w.classList.add('out');
    w.addEventListener('animationend', done, { once: true });
    setTimeout(done, 400);
  };

  /* ---- add back from the tray ---- */
  if (tray) tray.addEventListener('click', e => {
    const chip = e.target.closest('.chip'); if (!chip) return;
    const src = original.find(o => o.dataset.id === chip.dataset.id);
    const w = src.cloneNode(true); w.classList.add('in');
    flip(() => grid.appendChild(w));
    chip.remove();
    tray.hidden = !tray.querySelector('.chip');
    say(`${name(w)} aggiunto`); sync();
  });

  if (reset) reset.addEventListener('click', () => {
    flip(() => { grid.replaceChildren(...original.map(o => { const c = o.cloneNode(true); c.classList.add('in'); return c; })); });
    if (tray) { tray.querySelector('.chips').replaceChildren(); tray.hidden = true; }
    say('Dashboard ripristinata'); sync();
  });

  grid.addEventListener('click', e => {
    const x = e.target.closest('.mod-del'); if (x) remove(x.closest('.mod'));
  });

  /* ---- keyboard: arrows move the focused module ---- */
  grid.addEventListener('keydown', e => {
    const h = e.target.closest('.mod-move'); if (!h) return;
    const w = h.closest('.mod');
    if (e.key === 'Delete' || e.key === 'Backspace') { e.preventDefault(); remove(w); return; }
    const back = e.key === 'ArrowLeft' || e.key === 'ArrowUp', fwd = e.key === 'ArrowRight' || e.key === 'ArrowDown';
    if (!back && !fwd) return;
    e.preventDefault();
    const sib = back ? w.previousElementSibling : w.nextElementSibling; if (!sib) return;
    flip(() => back ? sib.before(w) : sib.after(w));
    h.focus({ preventScroll: true });
    say(`${name(w)} spostato`); sync();
  });

  /* ---- drag with pointer events (mouse, pen and touch) ---- */
  let drag = null;
  grid.addEventListener('pointerdown', e => {
    const h = e.target.closest('.mod-move');
    if (!h || e.button > 0) return;
    e.preventDefault();
    const w = h.closest('.mod'), r = w.getBoundingClientRect();
    const ph = document.createElement('div');
    ph.className = 'mod ph' + (w.classList.contains('wide') ? ' wide' : '');
    ph.style.height = r.height + 'px';
    w.before(ph);
    Object.assign(w.style, { position: 'fixed', left: r.left + 'px', top: r.top + 'px', width: r.width + 'px', height: r.height + 'px', margin: 0 });
    w.classList.add('lift');
    document.body.appendChild(w);
    drag = { w, ph, ox: e.clientX - r.left, oy: e.clientY - r.top, id: e.pointerId };
    h.setPointerCapture(e.pointerId);
    document.documentElement.classList.add('dragging');
  });
  const move = e => {
    if (!drag || e.pointerId !== drag.id) return;
    const { w, ph } = drag;
    w.style.left = e.clientX - drag.ox + 'px';
    w.style.top = e.clientY - drag.oy + 'px';
    // auto scroll near the edges on small screens
    if (e.clientY < 70) scrollBy(0, -12); else if (e.clientY > innerHeight - 70) scrollBy(0, 12);
    w.style.pointerEvents = 'none';
    const over = document.elementFromPoint(e.clientX, e.clientY);
    w.style.pointerEvents = '';
    const t = over && over.closest('.dash > .mod:not(.ph)');
    if (!t) return;
    const tr = t.getBoundingClientRect();
    const after = (e.clientY - tr.top) / tr.height > .5 || (e.clientX - tr.left) / tr.width > .5;
    if (after ? t.nextElementSibling === ph : t.previousElementSibling === ph) return;
    flip(() => after ? t.after(ph) : t.before(ph));
  };
  const end = e => {
    if (!drag || e.pointerId !== drag.id) return;
    const { w, ph } = drag; drag = null;
    document.documentElement.classList.remove('dragging');
    const from = w.getBoundingClientRect();
    w.removeAttribute('style'); w.classList.remove('lift');
    ph.replaceWith(w);
    const to = w.getBoundingClientRect();
    if (!reduce) w.animate([{ transform: `translate(${from.left - to.left}px, ${from.top - to.top}px) scale(1.02)` }, { transform: 'none' }], { duration: 240, easing: 'cubic-bezier(.2,.8,.2,1)' });
    say(`${name(w)} spostato`); sync();
  };
  addEventListener('pointermove', move, { passive: true });
  addEventListener('pointerup', end);
  addEventListener('pointercancel', end);
  sync();
})();
