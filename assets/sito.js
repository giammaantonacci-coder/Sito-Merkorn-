/* Merkorn, comportamenti comuni a tutte le pagine: menu mobile, copia dell'indirizzo email,
   statistiche anonime e modulo di contatto. */
(() => {
  // Every request from the contact form reaches this inbox: through the site's own mail function
  // (api/contact.js, sent from Gmail) and, if that fails, through FormSubmit.
  const INBOX = 'merkornsh@gmail.com';
  const ENDPOINT = '/api/contact';
  const BACKUP = 'https://formsubmit.co/ajax/' + INBOX;

  /* ---------- mobile menu ---------- */
  const top = document.querySelector('.top');
  const menuBtn = document.querySelector('.burger');
  const setMenu = open => {
    if (!menuBtn) return;
    top.classList.toggle('open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Chiudi il menu' : 'Apri il menu');
  };
  if (menuBtn) {
    menuBtn.addEventListener('click', () => setMenu(!top.classList.contains('open')));
    top.querySelectorAll('nav a').forEach(a => a.addEventListener('click', () => setMenu(false)));
    addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
  }

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

  /* ---------- anonymous statistics ----------
     No cookies and no personal data: which page, where the visit comes from, and how the contact
     form is used (field names only, never what is typed). An id kept for this tab only groups the
     events of one visit. Everything goes to api/evento.js and from there to the Merkorn gestionale. */
  const track = (() => {
    let visita = null;
    try {
      visita = sessionStorage.getItem('mk_visita') || (crypto.randomUUID ? crypto.randomUUID() : String(Math.random()).slice(2));
      sessionStorage.setItem('mk_visita', visita);
    } catch { /* private mode: events stay anonymous without a visit id */ }
    const pagina = location.pathname.replace(/\.html$/, '').replace(/\/index$/, '/') || '/';
    const sorgente = (() => {
      const utm = new URLSearchParams(location.search).get('utm_source');
      if (utm) return utm;
      try {
        const host = new URL(document.referrer).hostname.replace(/^www\./, '');
        return host && host !== location.hostname.replace(/^www\./, '') ? host : null;
      } catch { return null; }
    })();
    const queue = [];
    const flush = () => {
      if (!queue.length) return;
      const body = JSON.stringify(queue.splice(0));
      const sent = navigator.sendBeacon && navigator.sendBeacon('/api/evento', new Blob([body], { type: 'text/plain' }));
      if (!sent) fetch('/api/evento', { method: 'POST', body, keepalive: true }).catch(() => {});
    };
    addEventListener('pagehide', flush);
    document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') flush(); });
    return (evento, campo, now) => {
      queue.push({ evento, pagina, campo: campo || null, sorgente: evento === 'pagina' ? sorgente : null, visita });
      if (now || queue.length >= 10) flush();
    };
  })();
  track('pagina', null, true);

  /* ---------- contact form ---------- */
  document.querySelectorAll('form.form').forEach(form => {
    // how far visitors get in the form, and where they stop
    let started = false, sent = false, last = null;
    const filled = new Set();
    if ('IntersectionObserver' in window) {
      const seen = new IntersectionObserver(entries => {
        if (entries.some(en => en.isIntersecting)) { track('form_visto'); seen.disconnect(); }
      }, { threshold: 0.4 });
      seen.observe(form);
    }
    form.addEventListener('input', () => { if (!started) { started = true; track('form_iniziato', last); } });
    form.addEventListener('focusin', e => { if (e.target.name && e.target.name[0] !== '_') last = e.target.name; });
    form.addEventListener('change', e => {
      const n = e.target.name;
      if (n && n[0] !== '_' && !filled.has(n) && (e.target.type === 'checkbox' ? e.target.checked : e.target.value)) { filled.add(n); track('campo', n); }
    });
    addEventListener('pagehide', () => { if (started && !sent) { started = false; track('abbandono', last, true); } });

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
        Object.keys(rules).filter(n => form.elements[n].closest('.field').classList.contains('bad')).forEach(n => track('errore', n));
        if (!privacy.checked) track('errore', 'privacy');
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
        // any failure of the mail function (not configured yet, Gmail refusing, network) goes to the backup service
        let res = await post(ENDPOINT).catch(err => { if (ctrl.signal.aborted) throw err; return null; });
        if (!res || (!res.ok && res.status !== 422)) res = await post(BACKUP);
        const body = await res.json().catch(() => ({}));
        if (!res.ok || String(body.success) === 'false') throw new Error(body.message || res.status);
        form.reset(); touched.clear();
        sent = true; track('invio', null, true);
        status.className = 'status ok';
        status.textContent = 'Richiesta inviata. Ti ricontattiamo all\'indirizzo email che hai indicato.';
      } catch (err) {
        track('invio_fallito', null, true);
        // never lose the request: the same text, ready to send from the visitor's own mail app
        const text = Object.entries(data).filter(([k, v]) => k[0] !== '_' && k !== 'Pagina' && v).map(([k, v]) => k + ': ' + v).join('\n');
        const mail = document.createElement('a');
        mail.className = 'mail-fallback';
        mail.href = 'mailto:' + INBOX + '?subject=' + encodeURIComponent(data._subject) + '&body=' + encodeURIComponent(text);
        mail.textContent = 'Invia la richiesta via email';
        status.className = 'status ko';
        status.textContent = 'Il servizio di invio non ha risposto, i dati che hai inserito sono ancora nel modulo. Puoi inviare la stessa richiesta con il tuo programma di posta, a ' + INBOX + '. ';
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
