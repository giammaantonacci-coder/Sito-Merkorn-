"""Genera le pagine HTML del sito nella cartella principale.

Uso:  python3 src/build.py
Header, footer e form di contatto stanno in partials.py e sono uguali su ogni pagina.
I blocchi di sezione qui sotto (frase fissata, scorrimento orizzontale, campo viola,
card impilate, dashboard) sono riutilizzati tra le pagine, ognuna con i propri contenuti.
"""
import re
from pathlib import Path
from partials import page, contact_form, EMAIL, BASE

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- contenuti

# fase, titolo, descrizione, risultato
PHASES = [
    ("Analisi del processo", "Capiamo come lavori",
     "Studiamo i tuoi processi e troviamo dove si può guadagnare tempo.",
     "Priorità chiare fin da subito"),
    ("Fondamenta riusabili", "Partiamo da basi solide",
     "Moduli già collaudati per partire veloci e investire dove serve davvero.",
     "La base del gestionale con i tuoi dati"),
    ("Componenti su misura", "Costruiamo le parti su misura",
     "Le funzioni specifiche della tua azienda, rilasciate una alla volta.",
     "Un passo avanti a ogni rilascio"),
    ("Interfaccia", "Rendiamo i dati leggibili",
     "Schermate chiare che mostrano subito quello che conta.",
     "Decisioni più rapide, ogni giorno"),
]

PRINCIPLES = [
    ("I numeri che contano, in primo piano", "Apri la schermata e sai subito come sta andando."),
    ("Tutto in un unico posto", "Ordini, magazzino e fatture parlano tra loro."),
    ("Chiaro al primo sguardo", "Quello che richiede attenzione si nota subito."),
    ("Solo quello che ti serve", "Ogni funzione ha un motivo per esserci."),
]

SERVICES = [
    ("Sviluppo", "Gestionale su misura",
     "Un ERP personalizzato che riunisce ordini, magazzino, produzione e commesse e ti dà la visione completa dell'azienda.",
     ["Ordini e offerte", "Magazzino", "Produzione", "Commesse", "Documenti di trasporto"]),
    ("Consulenza", "Analisi dei processi aziendali",
     "Una fotografia chiara di come lavori oggi e delle priorità per crescere.",
     ["Mappa del processo", "Punti critici", "Priorità di intervento"]),
    ("Mobile", "App per magazzino e consegne",
     "I dati del magazzino e delle consegne, subito visibili in ufficio.",
     ["Carico e scarico merce", "Consegne", "Firma del cliente"]),
    ("Dopo il rilascio", "Assistenza ed evoluzione del software",
     "Il gestionale cresce con la tua azienda, seguito dallo stesso team.",
     ["Assistenza agli utenti", "Aggiornamenti", "Nuove funzioni"]),
]

CHAT_TEXT = "Ci vediamo in azienda, guardiamo insieme come lavorate e ti mostriamo cosa può cambiare."

# line icons for the cards, one per content (64x64, stroke; the "v" part is violet)
CARD_ICONS = {
    "Sviluppo": '<rect x="6" y="10" width="52" height="40" rx="6"/><path d="M6 20h52"/><path class="v" d="M16 30h18M16 38h26"/><path d="M22 56h20M32 50v6"/>',
    "Consulenza": '<circle cx="27" cy="27" r="16"/><path class="v" d="M19 30l6-6 5 5 6-8"/><path d="M39 39l15 15"/>',
    "Mobile": '<rect x="18" y="4" width="28" height="56" rx="7"/><path d="M28 10h8"/><path class="v" d="M25 42h14v8H25z"/><path d="M25 20h14M25 28h14"/>',
    "Dopo il rilascio": '<path d="M50 24a20 20 0 1 0 2 14"/><path d="M52 12v12H40"/><path class="v" d="M24 33l6 6 11-12"/>',
    "Produzione": '<path d="M6 54V30l14 8V30l14 8V22l24 12v20Z"/><path class="v" d="M44 54V44h8v10"/><path d="M4 54h56"/>',
    "Distribuzione": '<path d="M8 26 32 12l24 14v28H8Z"/><path class="v" d="M18 54V36h28v18"/><path d="M18 44h28"/>',
    "Servizi": '<path d="M4 44V20h34v24"/><path d="M38 28h12l8 10v6H38"/><circle class="v" cx="16" cy="46" r="5"/><circle class="v" cx="48" cy="46" r="5"/>',
    "Concretezza": '<rect x="8" y="22" width="48" height="20" rx="4"/><path d="M16 22v8M24 22v12M32 22v8M40 22v12M48 22v8"/><path class="v" d="M8 52h48"/>',
    "Chiarezza": '<rect x="8" y="12" width="48" height="42" rx="6"/><path d="M8 24h48M20 6v12M44 6v12"/><path class="v" d="M20 38l7 7 16-15"/>',
    "Design": '<rect x="6" y="8" width="52" height="38" rx="6"/><path class="v" d="M16 36l8-10 6 6 10-12"/><circle cx="46" cy="18" r="3"/><path d="M22 56h20M32 46v10"/>',
    # handshake: sleeves at the sides, the violet hand's fingers wrap the other hand (drawn on a 24 grid)
    "Commerciale": '<g transform="scale(2.6667)"><path class="v" vector-effect="non-scaling-stroke" d="m11 17 2 2a1 1 0 1 0 3-3"/><path class="v" vector-effect="non-scaling-stroke" d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path vector-effect="non-scaling-stroke" d="m21 3 1 11h-2"/><path vector-effect="non-scaling-stroke" d="M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3"/><path vector-effect="non-scaling-stroke" d="M3 4h8"/></g>',
    "Requisiti": '<rect x="12" y="8" width="40" height="50" rx="6"/><path d="M24 8v6h16V8"/><path class="v" d="M20 28l4 4 8-8M20 44l4 4 8-8"/><path d="M38 30h6M38 46h6"/>',
    "Codice": '<rect x="6" y="10" width="52" height="44" rx="6"/><path d="M6 20h52"/><path class="v" d="M24 30l-7 7 7 7M40 30l7 7-7 7"/><path d="M35 28l-6 18"/>',
    "Continuità": '<circle cx="22" cy="22" r="8"/><circle cx="42" cy="22" r="8"/><path d="M8 52c0-9 6-15 14-15s14 6 14 15"/><path class="v" d="M30 52c0-9 5-15 12-15s14 6 14 15"/>',
}


def card_icon(key):
    return f'<svg class="cico" viewBox="0 0 64 64" aria-hidden="true">{CARD_ICONS[key]}</svg>'


# ---------------------------------------------------------------- blocchi di sezione


def page_hero(eyebrow, lines, lead, lit):
    h = "".join(f'<span class="ln"><span style="--i:{i}">{l}</span></span>' for i, l in enumerate(lines))
    mini = "".join(('<i class="on"></i>' if k < lit else "<i></i>") for k in range(5))
    return f"""<section class="page-hero" data-exit data-name="{eyebrow}">
    <div class="wrap">
      <span class="eyebrow">{eyebrow}</span>
      <h1>{h}</h1>
      <p class="lead">{lead}</p>
      <div class="mini" aria-hidden="true">{mini}</div>
    </div>
  </section>"""


def statement(eyebrow, text, hl, small, name):
    return f"""<section class="statement pinned" data-scrub data-name="{name}">
    <div class="pin">
      <div class="wrap">
        <span class="eyebrow">{eyebrow}</span>
        <p data-hl="{hl}">{text}</p>
        <small>{small}</small>
      </div>
    </div>
  </section>"""


def hscroll(eyebrow, title, link, panels, name):
    more = f'<a class="more-link" href="{link[0]}">{link[1]} <span aria-hidden="true">→</span></a>' if link else ""
    return f"""<section class="hscroll" data-scrub data-name="{name}">
    <div class="pin">
      <div class="wrap head">
        <div class="sec-head"><span class="eyebrow">{eyebrow}</span><h2>{title}</h2></div>
        {more}
      </div>
      <div class="track">
          {panels}
      </div>
      <div class="wrap"><div class="bar" aria-hidden="true"><i></i></div></div>
    </div>
  </section>"""


def phase_panels():
    return "\n          ".join(
        f'<article class="panel"><span class="num">0{i}</span><span class="k">{k}</span><h3>{h}</h3><p>{p}</p></article>'
        for i, (k, h, p, _) in enumerate(PHASES, 1))


def service_panels():
    out = []
    for i, (k, h, p, tags) in enumerate(SERVICES, 1):
        t = "".join(f"<li>{x}</li>" for x in tags)
        out.append(f'<article class="panel"><span class="num">0{i}</span><span class="k">{k}</span><h3>{h}</h3><p>{p}</p><ul>{t}</ul></article>')
    return "\n          ".join(out)


def band(eyebrow, title, text, cta=("contattaci.html", "Prenota un appuntamento"), name="Primo incontro"):
    return f"""<section class="band-wrap" data-name="{name}">
    <div class="wrap">
      <div class="band" data-grow>
        <span class="eyebrow">{eyebrow}</span>
        <h2>{title}</h2>
        <p>{text}</p>
        <a class="btn light" href="{cta[0]}"><span>{cta[1]}</span></a>
      </div>
    </div>
  </section>"""


def principles(title="Come progettiamo le schermate"):
    items = "\n        ".join(f'<li style="--i:{i}"><div><strong>{a}</strong><span>{b}</span></div></li>' for i, (a, b) in enumerate(PRINCIPLES))
    return f"""<section class="principles" data-name="Principi">
    <div class="wrap">
      <div class="sec-head" data-enter><span class="eyebrow">Principi di progettazione</span><h2>{title}</h2><p>Quattro regole per dati chiari e decisioni rapide.</p></div>
      <ol class="rules stack">
        {items}
      </ol>
    </div>
  </section>"""


def cards(items, cols="", link=None):
    out = []
    for n, (k, h, p) in enumerate(items):
        tag, href = ("a", f' href="{link}"') if link else ("article", "")
        out.append(f'<{tag} class="card" data-enter style="--dir:{-1 if n % 2 == 0 else 1}"{href}>{card_icon(k)}<div class="ctx"><span class="kicker">{k}</span><h3>{h}</h3><p>{p}</p></div></{tag}>')
    return f'<div class="cards{(" " + cols) if cols else ""}">\n        ' + "\n        ".join(out) + "\n      </div>"


def section(name, eyebrow, title, intro, inner, cls=""):
    intro_html = f"<p>{intro}</p>" if intro else ""
    return f"""<section{f' class="{cls}"' if cls else ""} data-name="{name}">
    <div class="wrap">
      <div class="sec-head" data-enter><span class="eyebrow">{eyebrow}</span><h2>{title}</h2>{intro_html}</div>
      {inner}
    </div>
  </section>"""


def prose(name, eyebrow, title, paragraphs):
    ps = "".join(f"<p>{p}</p>" for p in paragraphs)
    return f"""<section data-name="{name}">
    <div class="wrap prose" data-enter>
      <div><span class="eyebrow">{eyebrow}</span><h2>{title}</h2></div>
      <div class="txt">{ps}</div>
    </div>
  </section>"""


def legs():
    out = []
    for i, (k, h, p, res) in enumerate(PHASES, 1):
        out.append(f'<article class="leg" data-enter><span class="dot">{i}</span><div class="body"><span class="k">{k}</span><h3>{h}</h3><p>{p}</p>'
                   f'<p class="res"><b>Risultato</b>{res}</p></div></article>')
    return '<div class="legs" data-line>\n        ' + "\n        ".join(out) + "\n      </div>"


ICONS = {
    "home": '<path d="M3 9.5 10 4l7 5.5V16a1 1 0 0 1-1 1h-3.5v-4.5h-5V17H4a1 1 0 0 1-1-1Z"/>',
    "analytics": '<path d="M4 16V11M8.5 16V7M13 16v-6M17 16V4"/>',
    "stock": '<path d="M3 7.5 10 4l7 3.5v7L10 18l-7-3.5Z"/><path d="M3 7.5 10 11l7-3.5M10 11v7"/>',
    "prod": '<circle cx="10" cy="10" r="2.5"/><path d="M10 2.5v2.2M10 15.3v2.2M17.5 10h-2.2M4.7 10H2.5M15.3 4.7l-1.6 1.6M6.3 13.7l-1.6 1.6M15.3 15.3l-1.6-1.6M6.3 6.3 4.7 4.7"/>',
}
VIEWS = [("home", "Home"), ("analytics", "Analitiche"), ("stock", "Magazzino"), ("prod", "Produzione")]


def icon(name):
    return f'<svg viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'


def pin(n):
    return f'<span class="mk" aria-hidden="true">{n}</span>'


def chips(labels, on):
    return "".join(f'<span class="chip{" on" if i == on else ""}">{l}</span>' for i, l in enumerate(labels))


def frame(active, title, body):
    nav = "".join(f'<span class="nav-item{" on" if k == active else ""}">{icon(k)}<span>{label}</span></span>' for k, label in VIEWS)
    return f"""<div class="float" data-enter><div class="app dash" aria-hidden="true">
        <div class="side">
          <div class="side-brand"><span class="mark"><i></i><i></i><i></i><i></i><i></i></span><span>Gestionale</span></div>
          <div class="side-nav">{nav}</div>
          <div class="side-foot"><span class="avatar">UF</span><span>Ufficio<small>Amministrazione</small></span></div>
        </div>
        <div class="dash-main">
          <div class="dash-top"><strong>{title}</strong><span class="dash-date">Lunedì 28 settembre</span></div>
          <div class="view">{body}</div>
        </div>
      </div></div>"""


def screen(n, name, title, purpose, frame_html, notes):
    items = "".join(f'<li><span class="mk">{i}</span><div><strong>{t}</strong><p>{d}</p></div></li>' for i, (t, d) in enumerate(notes, 1))
    return f"""<section class="screen" data-name="{name}">
    <div class="wrap">
      <div class="screen-head" data-enter><span class="eyebrow">Schermata {n} di 4</span><h2>{title}</h2><p>{purpose}</p></div>
      {frame_html}
      <ol class="notes">{items}</ol>
    </div>
  </section>"""


SCREEN_HOME = frame("home", "Home", f"""
            <div class="tiles rel" id="home-tiles">{pin(1)}</div>
            <div class="viz-row">
              <figure class="viz wide">{pin(2)}
                <figcaption><strong>Ordini degli ultimi 14 giorni</strong><span>Ordini ricevuti al giorno</span></figcaption>
                <div class="chart" id="home-cols"></div>
              </figure>
              <figure class="viz">{pin(3)}
                <figcaption><strong>Da fare oggi</strong><span>In ordine di urgenza</span></figcaption>
                <ul class="todo" id="home-todo"></ul>
              </figure>
            </div>""")

SCREEN_ANALYTICS = frame("analytics", "Analitiche", f"""
            <div class="filters rel">{chips(["Ultimi 3 mesi", "Ultimi 6 mesi", "Ultimi 12 mesi"], 2)}{pin(1)}</div>
            <div class="tiles" id="dash-tiles"></div>
            <div class="viz-row">
              <figure class="viz wide">{pin(2)}
                <figcaption><strong>Fatturato mensile</strong><span>Migliaia di euro, IVA esclusa</span></figcaption>
                <div class="legend"><span><i class="lk s1"></i>Anno in corso</span><span><i class="lk s0"></i>Anno precedente</span></div>
                <div class="chart" id="dash-line"></div>
              </figure>
              <figure class="viz">{pin(3)}
                <figcaption><strong>Ordini per categoria</strong><span>Ordini evasi negli ultimi 12 mesi</span></figcaption>
                <div class="chart" id="dash-bars"></div>
              </figure>
            </div>""")

SCREEN_STOCK = frame("stock", "Magazzino", f"""
            <div class="tiles three rel" id="stock-tiles">{pin(1)}</div>
            <div class="filters">{chips(["Tutti", "Sotto soglia", "In esaurimento"], 0)}<span class="search"><span>Cerca per codice o nome</span></span></div>
            <div class="tbl-wrap"><table class="tbl" id="stock-table">
              <thead><tr><th>Codice</th><th>Articolo</th><th>{pin(2)}Giacenza</th><th class="num">{pin(4)}Riordino</th><th>{pin(3)}Stato</th></tr></thead>
              <tbody></tbody>
            </table></div>""")

SCREEN_PROD = frame("prod", "Produzione", f"""
            <div class="rel">{pin(1)}<ol class="flow" id="prod-flow"></ol></div>
            <div class="viz-row">
              <figure class="viz wide">{pin(2)}
                <figcaption><strong>Ore lavorate per reparto</strong><span>Ultime otto settimane</span></figcaption>
                <div class="legend"><span><i class="sw s1"></i>Taglio</span><span><i class="sw s2"></i>Assemblaggio</span><span><i class="sw s3"></i>Collaudo</span></div>
                <div class="chart" id="prod-cols"></div>
              </figure>
              <figure class="viz">{pin(3)}
                <figcaption><strong>Avanzamento commesse</strong><span>Completamento e consegna prevista</span></figcaption>
                <ul class="jobs" id="prod-jobs"></ul>
              </figure>
            </div>""")

SCREENS = "\n\n  ".join([
    screen(1, "Home", "Home", "La giornata in un colpo d'occhio.", SCREEN_HOME, [
        ("Quattro numeri, sempre nello stesso posto", "Sempre in alto e nello stesso ordine, così li ritrovi senza cercarli."),
        ("Un colore per una serie", "Un solo dato, un solo colore. Il valore di oggi è scritto sopra."),
        ("Priorità in forma di elenco", "In ordine di urgenza, con colore, simbolo e parola."),
    ]),
    screen(2, "Analitiche", "Analitiche", "L'andamento dell'azienda, per chi decide.", SCREEN_ANALYTICS, [
        ("Un periodo per tutta la schermata", "Si sceglie una volta e vale per tutti i numeri."),
        ("Il dato che conta in primo piano", "Quest'anno in viola, l'anno scorso in grigio."),
        ("Barre orizzontali per i nomi lunghi", "Si leggono senza girare la testa, il valore è in fondo alla barra."),
    ]),
    screen(3, "Magazzino", "Magazzino", "Le scorte sotto controllo.", SCREEN_STOCK, [
        ("Prima il riepilogo", "Quanti articoli richiedono un intervento, prima dell'elenco."),
        ("Giacenza e soglia nella stessa barra", "Chi è sotto soglia si vede senza leggere i numeri."),
        ("Stato con colore, simbolo e parola", "Colore, simbolo ed etichetta, sempre insieme."),
        ("Numeri solo dove serve un'azione", "La quantità da riordinare compare solo dove serve."),
    ]),
    screen(4, "Produzione", "Produzione", "Reparti e commesse, a che punto sono.", SCREEN_PROD, [
        ("Le fasi nell'ordine reale", "Da sinistra a destra, dal taglio alla spedizione."),
        ("Tre reparti, tre colori distinguibili", "Colori distinguibili anche per chi è daltonico."),
        ("Avanzamento e scadenza sulla stessa riga", "Quanto manca e se sei in tempo, sulla stessa riga."),
    ]),
])


def dashboard():
    return f"""<section class="screens-intro" data-name="Come si vedono i dati">
    <div class="wrap">
      <div class="sec-head centered" data-enter><span class="eyebrow">Fase 4 in pratica</span><h2>Come si vedono i dati</h2><p>Così i dati diventano decisioni. Quattro schermate di esempio e il perché di ogni scelta.</p></div>
    </div>
  </section>

  {SCREENS}"""


# ---------------------------------------------------------------- pagine

HOME_SERVICES = (cards([(k, h, p) for k, h, p, _ in SERVICES], link="servizi.html")
                 + '\n      <a class="more-link" href="servizi.html">Tutti i servizi <span aria-hidden="true">→</span></a>')

# Frequently asked questions: visible on the page and published as FAQPage structured data,
# written as short, quotable answers (what Google and AI assistants pick up)
FAQ_HOME = [
    ("Cos'è un software gestionale su misura?",
     "È un gestionale progettato sui processi di una sola azienda. Segue il tuo modo di lavorare e riunisce tutti i dati in un unico posto."),
    ("Cosa cambia con un gestionale su misura?",
     "Vedi i dati di tutta l'azienda in un colpo d'occhio, risparmi tempo sulle operazioni ripetitive e prendi decisioni basate su numeri aggiornati."),
    ("Quando conviene un gestionale personalizzato rispetto a uno pronto?",
     "Quando accanto al gestionale torna fuori il foglio Excel. Se ti basta un programma pronto, te lo diciamo."),
    ("Quanto costa un gestionale su misura?",
     "Dipende da quante aree deve seguire. Dopo l'analisi ricevi un preventivo diviso per fasi, con tempi e costi chiari."),
    ("Quanto tempo serve per sviluppare un gestionale personalizzato?",
     "Lavoriamo per rilasci, quindi le prime parti le usi già durante il progetto. La durata la fissiamo dopo l'analisi."),
    ("Il gestionale si collega alla fatturazione elettronica e alla contabilità?",
     "Sì, ai programmi che usi già. Ogni dato si scrive una volta sola."),
    ("Lavorate solo in Puglia?",
     "Siamo a Mottola, in provincia di Taranto, e lavoriamo soprattutto in Puglia. Per il resto d'Italia il primo incontro si fa online."),
]

FAQ_SERVIZI = [
    ("Si può partire da un solo reparto?",
     "Sì. Si parte da dove si perde più tempo e il resto si aggiunge dopo."),
    ("Potete importare i dati da Excel o dal vecchio gestionale?",
     "Sì. Importiamo anagrafiche, articoli e giacenze, dopo averli ripuliti da doppioni ed errori."),
    ("Sviluppate anche app per telefono e tablet?",
     "Sì, per magazzino, consegne e interventi fuori sede, collegate al gestionale."),
    ("Cosa succede dopo il rilascio?",
     "Il software lo segue lo stesso team che l'ha costruito, con assistenza e aggiornamenti."),
]


def faq(items, title="Domande frequenti", intro=None, name="Domande frequenti"):
    qs = "\n        ".join(f'<details class="qa"><summary><h3>{q}</h3><span class="qa-i" aria-hidden="true"></span></summary><p>{a}</p></details>' for q, a in items)
    return section(name, "Domande frequenti", title, intro, f'<div class="faq" data-enter>\n        {qs}\n      </div>')


def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}



# ---------------------------------------------------------------- pagina 404: mini dashboard modulare

GRIP = '<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><circle cx="5" cy="3" r="1.4"/><circle cx="11" cy="3" r="1.4"/><circle cx="5" cy="8" r="1.4"/><circle cx="11" cy="8" r="1.4"/><circle cx="5" cy="13" r="1.4"/><circle cx="11" cy="13" r="1.4"/></svg>'
X = '<svg viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M3 3l8 8M11 3l-8 8"/></svg>'

def mod(mid, title, body, wide=False):
    return (f'<article class="mod{" wide" if wide else ""}" data-id="{mid}"><div class="mod-top">'
            f'<button class="mod-move" type="button" aria-label="Sposta il modulo {title}, usa le frecce">{GRIP}</button>'
            f'<span class="mod-title">{title}</span>'
            f'<button class="mod-del" type="button" aria-label="Elimina il modulo {title}">{X}</button></div>{body}</article>')

bars = "".join(f'<i style="height:{h}%"></i>' for h in [46, 62, 54, 71, 66, 38, 84])
days = "".join(f"<span>{d}</span>" for d in ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Oggi"])
E404_MODS = "".join([
    mod("ordini", "Ordini di oggi", '<div class="kpi">128</div><div class="delta"><b>+12%</b> rispetto a ieri</div>'),
    mod("fatturato", "Fatturato del mese", '<div class="kpi">€ 84.300</div><svg class="spark" viewBox="0 0 200 46" preserveAspectRatio="none" aria-hidden="true"><path d="M0 38 L25 34 L50 36 L75 26 L100 28 L125 18 L150 21 L175 10 L200 6" fill="none" stroke="#9747FF" stroke-width="2.5" vector-effect="non-scaling-stroke"/></svg>'),
    mod("consegne", "Consegne in corso", '<div class="kpi">14</div><div class="delta"><b>3</b> in arrivo entro un\'ora</div>'),
    mod("settimana", "Ordini della settimana", f'<div class="bars" aria-hidden="true">{bars}</div><div class="days" aria-hidden="true">{days}</div>', wide=True),
    mod("todo", "Da fare oggi", '<ul class="rows"><li><span class="dot"></span>Confermare ordine Rossi<small>9:30</small></li><li><span class="dot mid"></span>Riordinare olio 5 L<small>11:00</small></li><li><span class="dot low"></span>Fattura Bianchi<small>16:00</small></li></ul>'),
    mod("scorte", "Scorte sotto soglia", '<div class="mstack"><div class="dmeter"><div class="mt">Farina tipo 00<small>12 sacchi</small></div><div class="mb"><i class="lowv" style="width:22%"></i></div></div><div class="dmeter"><div class="mt">Bottiglie 75 cl<small>340 pz</small></div><div class="mb"><i style="width:48%"></i></div></div><div class="dmeter"><div class="mt">Etichette<small>1.200 pz</small></div><div class="mb"><i style="width:63%"></i></div></div></div>'),
    mod("commesse", "Commesse", '<div class="mstack"><div class="dmeter"><div class="mt">Linea confezionamento<small>80%, in tempo</small></div><div class="mb"><i style="width:80%"></i></div></div><div class="dmeter"><div class="mt">Ordine fiera Bari<small>45%, consegna venerdì</small></div><div class="mb"><i style="width:45%"></i></div></div><div class="dmeter"><div class="mt">Nuovo magazzino<small>20%, avvio lunedì</small></div><div class="mb"><i style="width:20%"></i></div></div></div>', wide=True),
])

HEAD = ('<div class="head"><span class="eyebrow">Errore 404</span>'
        '<h1>Cogli l\'attimo e prova la potenza della <em>modularità</em></h1>'
        '<p class="lead">Questa pagina si è spostata. Intanto trascina i moduli, togli quelli superflui e costruisci la tua dashboard.</p></div>')
ACTIONS = ('<div class="actions"><button class="btn ghost" type="button" data-dash-reset hidden><span>Ripristina la dashboard</span></button>'
           '<a class="btn" href="index.html"><span>Torna alla home</span></a></div>'
           '<p class="note">Dati di esempio. Ogni modulo del gestionale si aggiunge o si toglie così.</p><p class="sr dash-status" role="status" aria-live="polite"></p>')

# on phones the dashboard is replaced by a plain page
E404_SIMPLE = ('<div class="e404-simple"><span class="eyebrow">Errore 404</span><h1>Questa pagina <em>si è spostata</em></h1>'
               '<p class="lead">Ripartiamo dalla home o da quello che ti serve.</p>'
               '<div class="actions"><a class="btn" href="index.html"><span>Torna alla home</span></a><a class="btn ghost" href="contattaci.html"><span>Contattaci</span></a></div></div>')

E404 = f"""  <section class="e404" data-name="Pagina non trovata"><div class="wrap"><div class="e404-full">{HEAD}<div class="dash">{E404_MODS}</div>{ACTIONS}</div>{E404_SIMPLE}</div></section>"""

SERVICES_LD = [{"@type": "Service", "name": h, "serviceType": h, "description": p, "provider": {"@id": "https://merkorn.com/#org"},
                "areaServed": ["Taranto", "Bari", "Brindisi", "Lecce", "Matera", "Puglia", "Italia"]} for _, h, p, _ in SERVICES]

HOME = f"""  <section class="hero" data-exit data-name="Inizio">
    <div class="wrap">
      <div class="center">
        <span class="eyebrow">Software house in Puglia</span>
        <h1>
          <span class="ln"><span style="--i:0">Software gestionale</span></span>
          <span class="ln"><span style="--i:1"><em>su misura</em> per le PMI</span></span>
        </h1>
        <p class="lead">Mettiamo in ordine i dati della tua azienda. Vedi tutto in un colpo d'occhio e decidi prima, con più sicurezza.</p>
        <div class="actions">
          <a class="btn" href="contattaci.html"><span>Prenota un appuntamento</span></a>
          <a class="btn ghost" href="metodo.html"><span>Come lavoriamo</span></a>
        </div>
        <div class="scroll-cue"><i aria-hidden="true"></i>Scorri per continuare</div>
      </div>
    </div>
  </section>

  {statement("Il nostro approccio",
             "Dati chiari, decisioni migliori.",
             "Dati,decisioni",
             "Ordini, magazzino e produzione in un unico posto, sempre aggiornati. Più tempo per pensare alla strategia.",
             "Approccio")}

  {hscroll("Come lavoriamo", "Quattro fasi per un gestionale che usi ogni giorno", ("metodo.html", "Il metodo nel dettaglio"), phase_panels(), "Come lavoriamo")}

  {section("Servizi", "Servizi", "Gestionali personalizzati per ogni reparto", "Più controllo su ogni area dell'azienda, dagli ordini alla produzione.", HOME_SERVICES)}

  {band("Primo incontro", "Scopri cosa può cambiare nella tua azienda", CHAT_TEXT)}

  {principles()}

  {faq(FAQ_HOME, "Software gestionale su misura, le domande più comuni")}"""

METODO = f"""  {page_hero("Come lavoriamo", ["Come sviluppiamo un <em>gestionale personalizzato</em>"], "Quattro fasi, ognuna con un risultato concreto da verificare.", 2)}

  <section data-name="Le fasi">
    <div class="wrap">
      <div class="sec-head" data-enter><span class="eyebrow">Le fasi</span><h2>Dall'analisi alle schermate</h2></div>
      {legs()}
    </div>
  </section>

  {dashboard()}

  {principles()}"""

SERVIZI = f"""  {page_hero("Servizi", ["Software gestionale <em>personalizzato</em> per la tua azienda"], "Tutto quello che serve per avere i dati sotto controllo e decidere con più sicurezza.", 3)}

  {hscroll("Cosa facciamo", "Quattro servizi, un solo progetto", None, service_panels(), "Cosa facciamo")}

  {statement("Un unico progetto",
             "Dall'analisi all'assistenza, sempre le stesse persone.",
             "stesse,persone",
             "Team interno, senza subappalti.",
             "Un unico progetto")}

  {section("Per chi lavoriamo", "Per chi lavoriamo", "Imprese che vogliono crescere con i propri dati",
           "Soprattutto PMI pugliesi, molte nella filiera agroalimentare.",
           cards([("Produzione", "Agroalimentare e produzione", "Lotti, scadenze e commesse sempre tracciati."),
                  ("Distribuzione", "Commercio e logistica", "Giacenze, ordini e consegne sempre aggiornati."),
                  ("Servizi", "Squadre sul territorio", "Interventi e rapportini visibili subito in ufficio.")], "three"))}

  {prose("Integrazioni", "Integrazioni", "Collegato ai programmi che usi già",
         ["Contabilità e fatturazione elettronica collegate al gestionale. Ogni dato si scrive una volta sola."])}

  {faq(FAQ_SERVIZI, "Domande sui nostri servizi")}

  {band("Primo incontro", "Scopri cosa può fare per te", CHAT_TEXT)}"""

CHI = f"""  {page_hero("Chi siamo", ["Una software house in Puglia che <em>prima viene a vedere</em>"], "Siamo a Mottola, in provincia di Taranto. Aiutiamo le PMI a lavorare meglio con i propri dati.", 4)}

  {statement("Missione",
             "Rendere il digitale comprensibile e utile per chi lavora nelle PMI pugliesi.",
             "comprensibile,utile",
             "Con strumenti su misura e contenuti chiari.",
             "Missione")}

  {prose("Esperienza d'uso", "Esperienza d'uso", "Prima si progetta l'uso, poi si scrive il codice",
         ["Disegniamo le schermate con chi le userà e le proviamo sul posto, finché ogni passaggio è chiaro."])}

  {section("Il team", "Il team", "Le persone che seguono il tuo progetto",
           "Un team interno, dal primo incontro all'assistenza.",
           cards([("Commerciale", "Sales manager", "Il tuo primo contatto. Viene in azienda e prepara con te proposta, tempi e costi."),
                  ("Requisiti", "Project manager e data analyst", "Trasforma le esigenze in requisiti chiari e segue l'avanzamento del progetto."),
                  ("Design", "Product designer", "Progetta le schermate e le prova con chi le userà."),
                  ("Codice", "Developer", "Scrive il software, lo collega ai tuoi programmi e lo segue dopo il rilascio.")]))}

  {prose("Come costruiamo", "Come costruiamo", "Fondamenta riusabili, superficie su misura",
         ["I cinque blocchi del marchio sono il metodo. Moduli collaudati alla base, componenti su misura sopra, le tue schermate in cima."])}

  {section("Valori", "Come lavoriamo con i clienti", "Tre impegni che manteniamo", None,
           cards([("Concretezza", "Esempi basati su esperienze reali", "Ogni proposta parte da situazioni già viste in altre aziende."),
                  ("Chiarezza", "Tempi e costi definiti", "Durata e costo di ogni fase, concordati prima di iniziare."),
                  ("Continuità", "Lo stesso team nel tempo", "Chi scrive il software lo segue anche dopo.")], "three"))}

  {band("Primo incontro", "Conosciamoci in azienda", CHAT_TEXT)}"""

CONTATTI = contact_form(
    heading="Contattaci",
    intro="Scrivici per un appuntamento o un preventivo. Ti rispondiamo personalmente.",
    level="h1",
).replace('class="contact"', 'class="contact page-contact"', 1)

TITOLARE = "MERKORN S.R.L.S., partita IVA e codice fiscale 03494760733, con sede in Via Carlo Alberto della Chiesa 12, 74017 Mottola (TA)"
UPDATED = "29 settembre 2026"

PRIVACY = f"""  {page_hero("Privacy policy", ["Informativa sul trattamento dei <em>dati personali</em>"], "Come trattiamo i dati di chi visita il sito e di chi ci scrive, ai sensi degli articoli 13 e 14 del Regolamento UE 2016/679 (GDPR).", 5)}

  <section data-name="Informativa">
    <div class="wrap doc">
      <div><h2>Titolare del trattamento</h2><p>{TITOLARE}. Per qualsiasi richiesta sui vostri dati potete scrivere a <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>
      <div><h2>Dati che trattiamo</h2>
        <ul>
          <li><b>Dati di navigazione.</b> Per mostrare il sito il server registra dati tecnici come indirizzo IP, tipo di browser, pagina richiesta, data e ora. Servono al funzionamento e alla sicurezza del sito e non vengono usati per identificarvi.</li>
          <li><b>Dati inviati con il modulo di contatto o per email.</b> Nome e cognome, email e, se li indicate, azienda, telefono e testo del messaggio.</li>
          <li><b>Statistiche anonime, senza cookie.</b> Quali pagine vengono viste, da quale sito si arriva, il tipo di dispositivo e come viene usato il modulo di contatto (quali campi vengono compilati, dove ci si ferma, se l'invio riesce), mai il contenuto dei campi. Un codice casuale tenuto solo nella scheda del browser, e cancellato alla sua chiusura, raggruppa gli eventi di una stessa visita. Non registriamo l'indirizzo IP e non possiamo risalire a chi visita.</li>
          <li><b>Cookie.</b> Un cookie tecnico che ricorda le vostre scelte e, solo con il vostro consenso, cookie statistici. I dettagli sono nella <a href="cookie.html">cookie policy</a>.</li>
        </ul></div>
      <div><h2>Finalità e basi giuridiche</h2>
        <ul>
          <li>Rispondere alle richieste, fissare un appuntamento e preparare un preventivo: misure precontrattuali adottate su vostra richiesta (art. 6.1.b GDPR).</li>
          <li>Garantire il funzionamento e la sicurezza del sito e migliorarlo con statistiche anonime, senza cookie, sulle visite e sull'uso del modulo: legittimo interesse del titolare (art. 6.1.f GDPR).</li>
          <li>Statistiche aggregate sulle visite: consenso, che potete revocare in qualsiasi momento (art. 6.1.a GDPR).</li>
        </ul></div>
      <div><h2>Conferimento dei dati</h2><p>Il conferimento dei dati nel modulo è facoltativo, ma senza nome, email e messaggio non possiamo rispondere alla richiesta.</p></div>
      <div><h2>Chi riceve i dati</h2><p>I dati sono trattati dal personale di Merkorn e da fornitori che agiscono come responsabili del trattamento:</p>
        <ul>
          <li>Vercel Inc., per l'hosting del sito e per la funzione che inoltra i messaggi del modulo alla nostra casella email;</li>
          <li>Supabase Inc., per il database del nostro gestionale interno, in cui registriamo le richieste ricevute e le statistiche anonime;</li>
          <li>FormSubmit, solo come servizio di riserva per l'inoltro dei messaggi quando la funzione principale non è disponibile;</li>
          <li>Google LLC, per il servizio di posta elettronica e, solo con il vostro consenso, per Google Tag Manager e Google Analytics.</li>
        </ul>
        <p>I dati non vengono venduti né diffusi.</p></div>
      <div><h2>Trasferimento fuori dall'Unione europea</h2><p>Alcuni fornitori hanno sede negli Stati Uniti. Il trasferimento avviene sulla base della decisione di adeguatezza della Commissione europea (EU-US Data Privacy Framework) oppure delle clausole contrattuali standard previste dall'art. 46 GDPR.</p></div>
      <div><h2>Conservazione</h2>
        <ul>
          <li>Richieste di contatto: per il tempo necessario a gestirle e comunque non oltre 12 mesi dall'ultimo contatto, salvo un successivo rapporto contrattuale.</li>
          <li>Dati di navigazione: per il tempo previsto dal fornitore di hosting per la sicurezza del servizio.</li>
          <li>Dati statistici: non oltre 14 mesi.</li>
        </ul></div>
      <div><h2>I vostri diritti</h2><p>Potete chiedere l'accesso ai dati, la rettifica, la cancellazione, la limitazione del trattamento e la portabilità, opporvi al trattamento basato sul legittimo interesse e revocare il consenso in qualsiasi momento, senza conseguenze sui trattamenti già effettuati. Basta scrivere a <a href="mailto:{EMAIL}">{EMAIL}</a>. Avete anche il diritto di presentare reclamo al <a href="https://www.garanteprivacy.it" rel="noopener">Garante per la protezione dei dati personali</a>.</p></div>
      <div><h2>Decisioni automatizzate</h2><p>Non prendiamo decisioni basate unicamente su trattamenti automatizzati, compresa la profilazione.</p></div>
      <div><p class="updated">Ultimo aggiornamento: {UPDATED}.</p></div>
    </div>
  </section>"""

COOKIE_HEAD = ["Nome", "Tipo", "Fornitore", "Finalità", "Durata"]
COOKIE_ROWS = [
    ("mk_consent", "Tecnico", "Merkorn", "Ricorda le scelte sui cookie", "6 mesi"),
    ("_ga", "Statistico", "Google Analytics", "Distingue le visite in forma aggregata", "6 mesi"),
    ("_ga_&lt;ID&gt;", "Statistico", "Google Analytics", "Mantiene lo stato della sessione di visita", "6 mesi"),
]

COOKIE = f"""  {page_hero("Cookie policy", ["Come usiamo i <em>cookie</em>"], "Quali cookie usa il sito merkorn.com, a cosa servono e come potete cambiare le vostre scelte.", 5)}

  <section data-name="Cookie policy">
    <div class="wrap doc">
      <div><h2>Cosa sono i cookie</h2><p>I cookie sono piccoli file di testo che il sito salva nel browser. Alcuni sono necessari al funzionamento, altri servono a raccogliere statistiche e richiedono il vostro consenso.</p></div>
      <div><h2>Cookie tecnici</h2><p>Usiamo un solo cookie tecnico, che registra le scelte fatte nel banner così da non chiedervele a ogni visita. Non richiede consenso e non raccoglie dati per altre finalità.</p></div>
      <div><h2>Statistiche senza cookie</h2><p>Indipendentemente dal banner, il sito conta in forma anonima le pagine viste e l'uso del modulo di contatto, senza cookie e senza indirizzo IP. Per raggruppare gli eventi di una stessa visita usa un codice casuale salvato solo nella scheda del browser (sessionStorage), che si cancella quando la scheda viene chiusa e non permette di identificarvi.</p></div>
      <div><h2>Cookie statistici</h2><p>Con il vostro consenso carichiamo Google Tag Manager e, tramite questo, Google Analytics, per sapere in forma aggregata quante persone visitano il sito e quali pagine consultano. Abbiamo disattivato le funzioni pubblicitarie e i segnali Google. Senza consenso nessuno dei due servizi viene caricato.</p></div>
      <div><h2>Cookie di profilazione e di terze parti</h2><p>Non usiamo cookie di profilazione né cookie pubblicitari. I caratteri tipografici sono ospitati direttamente sul sito, quindi aprendo le pagine non vengono contattati servizi esterni.</p></div>
      <div><h2>Elenco dei cookie</h2>
        <div class="table"><table>
          <thead><tr>{"".join(f"<th>{h}</th>" for h in COOKIE_HEAD)}</tr></thead>
          <tbody>{"".join("<tr>" + "".join(f'<td data-label="{l}">{c}</td>' for l, c in zip(COOKIE_HEAD, r)) + "</tr>" for r in COOKIE_ROWS)}</tbody>
        </table></div></div>
      <div><h2>Come cambiare le scelte</h2><p>Potete modificare o revocare il consenso in qualsiasi momento da <button class="linkbtn" type="button" data-cookie-prefs>Preferenze cookie</button>, un link presente anche in fondo a ogni pagina. Potete inoltre cancellare o bloccare i cookie dalle impostazioni del browser. Chiudendo il banner con la X vengono mantenuti solo i cookie tecnici.</p></div>
      <div><h2>Titolare</h2><p>{TITOLARE}. Per domande: <a href="mailto:{EMAIL}">{EMAIL}</a>. Maggiori informazioni sul trattamento dei dati sono nella <a href="privacy.html">privacy policy</a>.</p></div>
      <div><p class="updated">Ultimo aggiornamento: {UPDATED}.</p></div>
    </div>
  </section>"""

# path, <title>, meta description, nebula seed, body, contact form, scripts, structured data
PAGES = [
    ("index.html", "Software gestionale su misura per PMI | Merkorn",
     "Merkorn è una software house in Puglia che sviluppa software gestionali su misura per PMI: ordini, magazzino, produzione e fatturazione in un unico sistema.",
     0.0, HOME, True, (), [faq_ld(FAQ_HOME)]),
    ("metodo.html", "Come sviluppiamo un gestionale personalizzato | Merkorn",
     "Il metodo Merkorn per sviluppare un gestionale personalizzato: analisi dei processi, moduli collaudati, componenti su misura e interfacce semplici da usare.",
     1.3, METODO, True, ("assets/schermate.js",), []),
    ("servizi.html", "Gestionale personalizzato, magazzino e produzione | Merkorn",
     "Gestionale su misura per aziende, gestionale di magazzino e produzione, app per le consegne e analisi dei processi, integrati con la fatturazione elettronica.",
     2.6, SERVIZI, True, (), SERVICES_LD + [faq_ld(FAQ_SERVIZI)]),
    ("chi-siamo.html", "Software house a Taranto e in Puglia per PMI | Merkorn",
     "Merkorn è una software house di Mottola (Taranto): sales manager, project manager, product designer e developer che sviluppano gestionali su misura per PMI.",
     3.9, CHI, True, (), []),
    ("contattaci.html", "Preventivo gestionale su misura | Merkorn",
     "Contatta Merkorn per un appuntamento o un preventivo per un software gestionale su misura. Primo incontro in azienda o online, senza impegno.",
     5.2, CONTATTI, False, (), []),
    ("404.html", "Pagina non trovata | Merkorn",
     "La pagina cercata si è spostata. Torna alla home di Merkorn.",
     9.1, E404, False, ("assets/dash404.js",), []),
    ("privacy.html", "Privacy policy | Merkorn",
     "Privacy policy di Merkorn: come trattiamo i dati di chi visita il sito e di chi ci contatta, ai sensi del GDPR.",
     6.5, PRIVACY, True, (), []),
    ("cookie.html", "Cookie policy | Merkorn",
     "Quali cookie usa il sito di Merkorn, a cosa servono e come modificare le scelte sul consenso.",
     7.8, COOKIE, False, (), []),
]

if __name__ == "__main__":
    from datetime import date
    for path, title, desc, seed, body, form, scripts, ld in PAGES:
        html = page(path, title, desc, seed, body, form, scripts, ld)
        if path == "404.html":
            # served at any missing address: absolute base for links and assets, kept out of search results
            html = html.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<base href="/">', 1)
            html = html.replace('content="index, follow, max-image-preview:large, max-snippet:-1"', 'content="noindex, follow"')
            html = re.sub(r'<link rel="(canonical|alternate)"[^>]*>\n', "", html)
            html = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", html, flags=re.S)
        (ROOT / path).write_text(html, encoding="utf-8")
        print("scritto", path)
    # sitemap for search engines
    today = date.today().isoformat()
    urls = "".join(
        f"<url><loc>https://merkorn.com/{'' if p == 'index.html' else p}</loc><lastmod>{today}</lastmod>"
        f"<priority>{'1.0' if p == 'index.html' else '0.3' if p in ('privacy.html', 'cookie.html') else '0.8'}</priority></url>"
        for p, *_ in PAGES if p != "404.html")
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    print("scritto sitemap.xml")
