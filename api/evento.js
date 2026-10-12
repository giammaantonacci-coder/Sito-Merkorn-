/* Merkorn, statistiche anonime del sito.
   Riceve dal browser gruppi di eventi (pagina vista, uso del modulo di contatto) e li salva nel gestionale.
   Nessun cookie e nessun dato personale: niente IP, niente contenuto dei campi, solo il nome del campo.
   Variabili d'ambiente: GESTIONALE_URL, GESTIONALE_KEY, GESTIONALE_TOKEN (come api/contact.js). */
const EVENTI = new Set(['pagina', 'form_visto', 'form_iniziato', 'campo', 'errore', 'abbandono', 'invio', 'invio_fallito']);
const CAMPI = new Set(['nome', 'azienda', 'email', 'telefono', 'argomento', 'messaggio', 'privacy']);
const BOT = /bot|crawl|spider|slurp|preview|lighthouse|headless|facebookexternalhit|whatsapp/i;

const testo = (v, max) => (typeof v === 'string' && v ? v.slice(0, max) : null);

function dispositivo(ua) {
  if (/iPad|Tablet/i.test(ua)) return 'tablet';
  if (/Mobi|Android|iPhone/i.test(ua)) return 'mobile';
  return 'desktop';
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).end(); }
  const ua = String(req.headers['user-agent'] || '');
  const url = process.env.GESTIONALE_URL, key = process.env.GESTIONALE_KEY, token = process.env.GESTIONALE_TOKEN;
  if (!url || !key || !token || BOT.test(ua)) return res.status(204).end();

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = null; } }
  if (!Array.isArray(body)) return res.status(400).end();

  const disp = dispositivo(ua);
  const eventi = body.slice(0, 50).filter(e => e && EVENTI.has(e.evento)).map(e => ({
    evento: e.evento,
    pagina: testo(e.pagina, 120),
    campo: CAMPI.has(e.campo) ? e.campo : null,
    sorgente: testo(e.sorgente, 80),
    dispositivo: disp,
    visita: testo(e.visita, 40),
  }));
  if (!eventi.length) return res.status(204).end();

  try {
    await fetch(`${url.replace(/\/+$/, '')}/rest/v1/rpc/sito_evento`, {
      method: 'POST',
      headers: { apikey: key, Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ chiave: token, eventi }),
      signal: AbortSignal.timeout(4000),
    });
  } catch (err) {
    console.error('evento: gestionale non raggiungibile', err && err.message);
  }
  return res.status(204).end();
};
