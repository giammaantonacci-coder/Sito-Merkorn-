/* Merkorn, invio del modulo di contatto.
   Riceve la richiesta dal sito e la spedisce alla casella Gmail di Merkorn tramite SMTP.
   Variabili d'ambiente su Vercel:
     GMAIL_USER          indirizzo Gmail che invia e riceve (merkornsh@gmail.com)
     GMAIL_APP_PASSWORD  password per le app creata nell'account Google
   Senza queste variabili risponde 503 e il sito usa il servizio di riserva.
   Ogni richiesta valida entra anche nel gestionale Merkorn (cliente, trattativa e attività):
     GESTIONALE_URL    indirizzo del progetto Supabase del gestionale
     GESTIONALE_KEY    chiave pubblica (anon) del progetto
     GESTIONALE_TOKEN  chiave segreta del sito, salvata nel gestionale (impostazioni.sito_token) */
const nodemailer = require('nodemailer');

const FIELDS = ['Nome e cognome', 'Azienda', 'Email', 'Telefono', 'Argomento', 'Messaggio', 'Pagina'];
const LIMITS = { 'Messaggio': 5000 };
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

// Only the site itself may post here: other origins are refused
const ORIGINS = /^https:\/\/(www\.)?merkorn\.com$|^https:\/\/sito-merkorn[\w-]*\.vercel\.app$/;
function fromSite(req) {
  const o = String(req.headers.origin || req.headers.referer || '');
  try { return ORIGINS.test(new URL(o).origin); } catch { return false; }
}

// A light per-instance brake against floods: at most 5 requests per IP every 10 minutes
const hits = new Map();
function tooMany(ip) {
  const now = Date.now(), win = 10 * 60 * 1000;
  const list = (hits.get(ip) || []).filter(t => now - t < win);
  list.push(now); hits.set(ip, list);
  if (hits.size > 5000) hits.clear();
  return list.length > 5;
}

const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clean = (v, max = 300) => String(v == null ? '' : v).replace(/\r/g, '').trim().slice(0, max);

let transport = null;
function mailer() {
  if (!transport) {
    transport = nodemailer.createTransport({
      host: 'smtp.gmail.com', port: 465, secure: true,
      auth: { user: process.env.GMAIL_USER, pass: String(process.env.GMAIL_APP_PASSWORD).replace(/\s+/g, '') },
    });
  }
  return transport;
}

// Porta la richiesta nel gestionale. Se non riesce l'email parte comunque: nessuna richiesta va persa.
async function inGestionale(data) {
  const url = process.env.GESTIONALE_URL, key = process.env.GESTIONALE_KEY, token = process.env.GESTIONALE_TOKEN;
  if (!url || !key || !token) return;
  try {
    const r = await fetch(`${url.replace(/\/+$/, '')}/rest/v1/rpc/sito_richiesta`, {
      method: 'POST',
      headers: { apikey: key, Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ chiave: token, dati: {
        nome: data['Nome e cognome'], azienda: data['Azienda'], email: data['Email'], telefono: data['Telefono'],
        argomento: data['Argomento'], messaggio: data['Messaggio'], pagina: data['Pagina'],
      } }),
      signal: AbortSignal.timeout(5000),
    });
    if (!r.ok) console.error('contact: gestionale', r.status, (await r.text()).slice(0, 200));
  } catch (err) {
    console.error('contact: gestionale non raggiungibile', err && err.message);
  }
}

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') { res.setHeader('Allow', 'POST'); return res.status(405).json({ success: false, message: 'Metodo non consentito' }); }
  if (!fromSite(req)) return res.status(403).json({ success: false, message: 'Origine non consentita' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = null; } }
  if (!body || typeof body !== 'object') return res.status(400).json({ success: false, message: 'Richiesta non valida' });

  // bots fill the hidden field: answer as if it went through
  if (body._honey) return res.status(200).json({ success: true });

  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'n/d';
  if (tooMany(ip)) return res.status(429).json({ success: false, message: 'Troppe richieste, riprovate più tardi' });

  const data = {};
  for (const k of FIELDS) data[k] = clean(body[k], LIMITS[k] || 300);
  if (data['Nome e cognome'].length < 2 || !EMAIL_RE.test(data['Email']) || data['Messaggio'].length < 10) {
    return res.status(422).json({ success: false, message: 'Campi mancanti o non validi' });
  }

  await inGestionale(data);

  const user = process.env.GMAIL_USER, pass = process.env.GMAIL_APP_PASSWORD;
  if (!user || !pass) return res.status(503).json({ success: false, message: 'Invio non configurato' });

  const rows = FIELDS.filter(k => data[k]).map(k =>
    `<tr><td style="padding:8px 14px 8px 0;color:#6b6475;vertical-align:top;white-space:nowrap">${esc(k)}</td>` +
    `<td style="padding:8px 0;color:#100E13;white-space:pre-wrap">${esc(data[k])}</td></tr>`).join('');
  const html = `<div style="font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif">
    <p style="margin:0 0 14px;font-weight:600">Nuova richiesta dal sito merkorn.com</p>
    <table style="border-collapse:collapse">${rows}</table>
    <p style="margin:18px 0 0;color:#6b6475;font-size:13px">Rispondete a questa email per scrivere direttamente a ${esc(data['Nome e cognome'])}.</p></div>`;
  const text = FIELDS.filter(k => data[k]).map(k => `${k}: ${data[k]}`).join('\n');

  try {
    await mailer().sendMail({
      from: { name: 'Sito Merkorn', address: user },
      to: user,
      replyTo: { name: data['Nome e cognome'], address: data['Email'] },
      subject: `Nuova richiesta dal sito: ${data['Argomento'] || 'Contatto'} (${data['Nome e cognome']})`,
      text, html,
    });
    return res.status(200).json({ success: true });
  } catch (err) {
    console.error('contact: invio non riuscito', err && err.code, err && err.message);
    transport = null;
    return res.status(502).json({ success: false, message: 'Invio non riuscito' });
  }
};
