/* Merkorn, comportamenti comuni a tutte le pagine. */
(() => {
  // Every request from the contact form is delivered to this address through FormSubmit.
  const INBOX = 'merkornsh@gmail.com';
  const ENDPOINT = 'https://formsubmit.co/ajax/' + INBOX;

  /* ---------- mobile menu ---------- */
  const nav = document.querySelector('.nav');
  const menuBtn = document.querySelector('.menu-btn');
  if (menuBtn) menuBtn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', String(open));
  });

  /* ---------- page change: fade out while the nebula speeds up ---------- */
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if (!a || reduce || e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank') return;
    const url = new URL(a.href, location.href);
    if (url.origin !== location.origin || url.pathname === location.pathname || !/\.html$|\/$/.test(url.pathname)) return;
    e.preventDefault();
    document.body.classList.add('leaving');
    if (window.merkornWarp) window.merkornWarp(1);
    setTimeout(() => { location.href = a.href; }, 450);
  });
  addEventListener('pageshow', () => { document.body.classList.remove('leaving'); if (window.merkornWarp) window.merkornWarp(0); });

  /* ---------- statement: split into words for the scroll reveal ---------- */
  document.querySelectorAll('.statement p[data-hl]').forEach(p => {
    const hl = p.dataset.hl.split(',');
    p.innerHTML = p.textContent.trim().split(/\s+/).map(w => `<span class="w${hl.includes(w.replace(/[.,]/g, '')) ? ' hl' : ''}">${w}</span>`).join(' ');
  });

  /* ---------- method phases light up in the middle of the screen ---------- */
  const legs = document.querySelectorAll('.leg');
  if (legs.length) {
    const io = new IntersectionObserver(es => es.forEach(e => e.target.classList.toggle('on', e.isIntersecting)), { rootMargin: '-40% 0px -40% 0px' });
    legs.forEach(l => io.observe(l));
  }

  /* ---------- HUD: current section ---------- */
  const hud = document.querySelector('.hud');
  const hudName = document.querySelector('.hud .hud-name');
  const pm = [...document.querySelectorAll('.hud .pm i')];
  const sections = [...document.querySelectorAll('main > section[data-name]')];
  if (hudName && sections.length) {
    const sio = new IntersectionObserver(es => es.forEach(e => {
      if (!e.isIntersecting) return;
      const i = sections.indexOf(e.target);
      hudName.textContent = e.target.dataset.name;
      hud.classList.toggle('off', e.target.classList.contains('contact'));
      const lit = Math.round((i / Math.max(1, sections.length - 1)) * 5);
      pm.forEach((b, k) => b.classList.toggle('on', k < lit));
    }), { rootMargin: '-50% 0px -50% 0px' });
    sections.forEach(s => sio.observe(s));
  }

  /* ---------- copy email ---------- */
  document.querySelectorAll('[data-copy]').forEach(btn => {
    const out = document.getElementById(btn.dataset.copy);
    btn.addEventListener('click', () => {
      const select = () => { getSelection().selectAllChildren(out); btn.textContent = 'Selezionato, premi Ctrl+C'; };
      try {
        navigator.clipboard.writeText(out.textContent.trim()).then(() => {
          btn.textContent = 'Copiato';
          setTimeout(() => { btn.textContent = 'Copia indirizzo'; }, 1800);
        }, select);
      } catch (err) { select(); }
    });
  });

  /* ---------- contact form ---------- */
  document.querySelectorAll('form.form').forEach(form => {
    const status = form.querySelector('.status');
    const submit = form.querySelector('button[type="submit"]');
    const rules = {
      nome: v => v.trim().length >= 2 || 'Inserisci nome e cognome.',
      email: v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) || 'Inserisci un indirizzo email valido, per esempio nome@azienda.it.',
      messaggio: v => v.trim().length >= 10 || 'Descrivi brevemente la richiesta, bastano poche righe.'
    };
    function check(name) {
      const el = form.elements[name];
      const field = el.closest('.field');
      const res = rules[name](el.value);
      const err = field.querySelector('.err');
      field.classList.toggle('bad', res !== true);
      el.setAttribute('aria-invalid', String(res !== true));
      err.textContent = res === true ? '' : res;
      return res === true;
    }
    Object.keys(rules).forEach(n => form.elements[n].addEventListener('blur', () => { if (form.elements[n].value) check(n); }));

    form.addEventListener('submit', async e => {
      e.preventDefault();
      status.className = 'status'; status.textContent = '';
      const valid = Object.keys(rules).map(check).every(Boolean);
      const privacy = form.elements.privacy;
      privacy.closest('.check').classList.toggle('bad', !privacy.checked);
      if (!valid || !privacy.checked) {
        status.className = 'status ko';
        status.textContent = !privacy.checked && valid ? 'Per inviare la richiesta serve il consenso al trattamento dei dati.' : 'Controlla i campi evidenziati.';
        const first = form.querySelector('.bad input, .bad textarea, .check.bad input');
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
      submit.disabled = true; submit.querySelector('span').textContent = 'Invio in corso';
      try {
        const res = await fetch(ENDPOINT, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) });
        const body = await res.json().catch(() => ({}));
        if (!res.ok || String(body.success) === 'false') throw new Error(body.message || res.status);
        form.reset();
        status.className = 'status ok';
        status.textContent = 'Richiesta inviata. Vi ricontattiamo all\'indirizzo email che avete indicato.';
      } catch (err) {
        status.className = 'status ko';
        status.textContent = 'La richiesta non è stata inviata a causa di un problema di connessione. Riprovate tra qualche minuto oppure scriveteci direttamente a ' + INBOX + '.';
      } finally {
        submit.disabled = false; submit.querySelector('span').textContent = 'Invia la richiesta';
      }
    });
  });
})();
