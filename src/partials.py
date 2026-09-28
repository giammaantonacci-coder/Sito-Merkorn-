"""Parti comuni a tutte le pagine: head, navigazione, form di contatto, footer."""

SITE = "Merkorn"
EMAIL = "merkornsh@gmail.com"

NAV = [
    ("metodo.html", "Come lavoriamo"),
    ("servizi.html", "Servizi"),
    ("chi-siamo.html", "Chi siamo"),
]

MARK = '<span class="mark" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>'

FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 50 32'%3E"
    "%3Crect width='50' height='32' rx='6' fill='%23100E13'/%3E"
    "%3Cg fill='%239747FF'%3E%3Crect x='21' y='4' width='8' height='8' rx='2'/%3E"
    "%3Crect x='13' y='12' width='8' height='8' rx='2'/%3E%3Crect x='29' y='12' width='8' height='8' rx='2'/%3E"
    "%3Crect x='5' y='20' width='8' height='8' rx='2'/%3E%3Crect x='37' y='20' width='8' height='8' rx='2'/%3E%3C/g%3E%3C/svg%3E"
)


def head(title, description, path):
    full = title if title == SITE else f"{title} | {SITE}"
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{full}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta name="theme-color" content="#08070B">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,500;9..40,700&amp;family=Inter:wght@400;600&amp;display=swap">
<link rel="stylesheet" href="assets/style.css">
</head>"""


def nav(current):
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{href}"{cur if href == current else ""}>{label}</a>'
        for href, label in NAV
    )
    return f"""<a class="skip" href="#contenuto">Vai al contenuto</a>
<header class="nav">
  <div class="pill">
    <a class="brand" href="index.html" aria-label="Merkorn, pagina iniziale">{MARK}MERKORN</a>
    <nav class="links" id="menu" aria-label="Pagine">{links}</nav>
    <a class="btn" href="contattaci.html"{cur if current == 'contattaci.html' else ''}><span>Contattaci</span></a>
    <button class="menu-btn" type="button" aria-label="Apri il menu" aria-expanded="false" aria-controls="menu"><i></i><i></i></button>
  </div>
</header>"""


TOPICS = [
    "Nuovo gestionale su misura",
    "Analisi dei processi",
    "App per reparto e consegne",
    "Assistenza su un software esistente",
    "Altro",
]


def contact_form(heading="Contattaci", intro=None, level="h2"):
    intro = intro or (
        "Raccontateci in poche righe di cosa si occupa l'azienda. "
        "Vi ricontattiamo per fissare un appuntamento, in azienda o online."
    )
    options = "".join(f"<option>{t}</option>" for t in TOPICS)
    return f"""<section class="contact" id="contattaci" data-name="Contattaci">
    <div class="wrap">
      <div class="layout">
        <div class="aside">
          <span class="eyebrow">Contattaci</span>
          <{level}>{heading}</{level}>
          <p>{intro}</p>
          <div class="mailline">
            <div><small>Oppure scriveteci a</small><output id="mail-addr">{EMAIL}</output></div>
            <button class="copy" type="button" data-copy="mail-addr">Copia indirizzo</button>
          </div>
        </div>
        <form class="form" novalidate aria-label="Modulo di contatto">
          <div class="field"><label for="f-nome">Nome e cognome</label><input id="f-nome" name="nome" autocomplete="name" required><span class="err" aria-live="polite"></span></div>
          <div class="field"><label for="f-azienda">Azienda <span>facoltativo</span></label><input id="f-azienda" name="azienda" autocomplete="organization"></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required><span class="err" aria-live="polite"></span></div>
          <div class="field"><label for="f-telefono">Telefono <span>facoltativo</span></label><input id="f-telefono" name="telefono" type="tel" autocomplete="tel"></div>
          <div class="field full"><label for="f-argomento">Argomento</label><select id="f-argomento" name="argomento">{options}</select></div>
          <div class="field full"><label for="f-messaggio">Messaggio</label><textarea id="f-messaggio" name="messaggio" required placeholder="Per esempio: siamo un'azienda di produzione con dodici persone e gestiamo ordini e magazzino su fogli di calcolo separati."></textarea><span class="err" aria-live="polite"></span></div>
          <label class="hp" aria-hidden="true">Non compilare questo campo<input name="_honey" tabindex="-1" autocomplete="off"></label>
          <label class="check"><input type="checkbox" name="privacy" id="f-privacy"><span>Ho letto l'<a href="privacy.html">informativa sulla privacy</a> e acconsento al trattamento dei dati per ricevere una risposta.</span></label>
          <div class="status" role="status" aria-live="polite"></div>
          <div class="foot-row">
            <span class="note">Tutti i campi sono obbligatori, salvo dove indicato.</span>
            <button class="btn" type="submit"><span>Invia la richiesta</span></button>
          </div>
        </form>
      </div>
    </div>
  </section>"""


def footer():
    links = "".join(f'<a href="{h}">{l}</a>' for h, l in NAV)
    return f"""<footer class="site-foot">
  <div class="wrap">
    <div class="top">
      <nav aria-label="Pagine del sito"><a href="index.html">Home</a>{links}<a href="contattaci.html">Contattaci</a><a href="privacy.html">Privacy</a></nav>
      <p>{EMAIL}</p>
    </div>
    <div class="bottom">
      <a class="powered" href="index.html" aria-label="Powered by Merkorn, pagina iniziale"><small>Powered by</small>{MARK}<strong>MERKORN</strong></a>
      <p>Software gestionale su misura per le PMI italiane, dalla Puglia</p>
    </div>
  </div>
</footer>"""


HUD = """<div class="hud" aria-hidden="true"><span class="pm"><i></i><i></i><i></i><i></i><i></i></span><div><b>Sezione</b><span class="hud-name">Inizio</span><small class="hud-by">powered by <strong>Merkorn</strong></small></div></div>"""


def page(path, title, description, seed, body, form=True, scripts=()):
    return f"""{head(title, description, path)}
<body data-seed="{seed}">
<canvas id="sky" aria-hidden="true"></canvas>
{nav(path)}
<main id="contenuto">
{body}
{contact_form() if form else ''}
</main>
{footer()}
{HUD}
<script src="assets/nebula.js" defer></script>
<script src="assets/site.js" defer></script>
{"".join(f'<script src="{x}" defer></script>' for x in scripts)}
</body>
</html>
"""
