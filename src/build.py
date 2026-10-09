"""Genera le pagine HTML del sito nella cartella principale.

Uso:  python3 src/build.py
Header, footer e form di contatto stanno in partials.py e sono uguali su ogni pagina.
I blocchi di sezione qui sotto (frase fissata, scorrimento orizzontale, campo viola,
card impilate, dashboard) sono riutilizzati tra le pagine, ognuna con i propri contenuti.
"""
from pathlib import Path
from partials import page, contact_form, EMAIL, BASE
import spiegato as sp

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- contenuti

# fase, titolo, descrizione, risultato
PHASES = [
    ("Analisi del processo", "Prima veniamo a vedere",
     "Passiamo del tempo con te in ufficio, in reparto o al bancone e seguiamo un ordine dall'arrivo alla consegna, segnando ogni punto in cui qualcuno ricopia un dato a mano.",
     "Una mappa di come lavori oggi e di cosa conviene cambiare per primo"),
    ("Fondamenta riusabili", "Non ripartiamo da zero",
     "Anagrafiche, permessi, stampe e contabilità servono a quasi tutte le aziende e le abbiamo già pronte e collaudate, così il budget va nelle parti che ti distinguono.",
     "Il gestionale di base con i tuoi dati già dentro"),
    ("Componenti su misura", "Poi scriviamo il codice",
     "Commesse, lotti, documenti di trasporto e consegne, costruiti attorno al tuo modo di lavorare e provati con chi li userà, una parte alla volta.",
     "A ogni rilascio un pezzo nuovo da usare, senza aspettare la fine"),
    ("Interfaccia", "Una schermata per ogni lavoro",
     "Pulsanti grandi per chi sta in magazzino con i guanti, tabelle complete per chi sta in ufficio e le operazioni di tutti i giorni a pochi tocchi.",
     "Un software che si impara usandolo"),
]

PRINCIPLES = [
    ("Una schermata, un lavoro", "Chi prepara le spedizioni vede le spedizioni da preparare, non tutto il gestionale."),
    ("Le cose di ogni giorno a un tocco", "Se un'operazione la fai decine di volte al giorno, non può stare in fondo a un menu."),
    ("Funziona anche in magazzino", "Su un telefono di qualche anno fa e con il segnale che va e viene, perché è lì che il gestionale si usa davvero."),
    ("Niente funzioni che non usi", "Aggiungiamo una funzione quando c'è un lavoro vero che la chiede, e se qualcosa non ti serve non te la mettiamo."),
]

SERVICES = [
    ("Sviluppo", "Gestionale su misura",
     "Un ERP personalizzato che tiene insieme ordini, magazzino, produzione e commesse, costruito attorno a come lavori, senza le funzioni che non ti servono.",
     ["Ordini e offerte", "Magazzino", "Produzione", "Commesse", "Documenti di trasporto"]),
    ("Consulenza", "Analisi dei processi aziendali",
     "Veniamo in azienda, guardiamo come lavorate e ti lasciamo un documento che dice dove si perde tempo e da dove conviene partire, anche se poi decidi di non sviluppare niente con noi.",
     ["Mappa del processo", "Punti critici", "Priorità di intervento"]),
    ("Mobile", "App per magazzino e consegne",
     "App per telefono e tablet collegate al gestionale, per caricare la merce, chiudere una consegna con la firma del cliente e lavorare anche dove il segnale è debole.",
     ["Carico e scarico merce", "Consegne", "Firma del cliente"]),
    ("Dopo il rilascio", "Assistenza ed evoluzione del software",
     "Il software lo segue chi l'ha costruito, con un team interno e senza subappalti, e quando cambia il tuo lavoro cambia anche il gestionale.",
     ["Assistenza agli utenti", "Aggiornamenti", "Nuove funzioni"]),
]

CHAT_TEXT = "Ci vediamo in azienda, guardiamo insieme come lavorate e ti diciamo con franchezza se possiamo esserti utili. Se è più comodo, anche online."

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
      <div class="sec-head" data-enter><span class="eyebrow">Principi di progettazione</span><h2>{title}</h2><p>Quattro regole che seguiamo prima di scrivere una riga di codice.</p></div>
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
    screen(1, "Home", "Home", "La prima schermata della giornata, con quello che sta succedendo e quello che chiede attenzione.", SCREEN_HOME, [
        ("Quattro numeri, sempre nello stesso posto", "Gli indicatori del giorno stanno in alto e non cambiano ordine, così l'occhio li ritrova senza cercarli. Il confronto con ieri è una freccia e un valore, non un altro grafico."),
        ("Un colore per una serie", "Le colonne hanno un solo colore perché raccontano un solo dato. Il valore di oggi è scritto sopra l'ultima colonna, gli altri si leggono sull'asse."),
        ("Priorità in forma di elenco", "Le cose da fare sono ordinate per urgenza. Ogni stato ha colore, simbolo e parola, quindi resta chiaro anche a chi distingue male i colori."),
    ]),
    screen(2, "Analitiche", "Analitiche", "L'andamento dell'azienda nel tempo, per chi prende decisioni.", SCREEN_ANALYTICS, [
        ("Un periodo per tutta la schermata", "Il periodo si sceglie una sola volta, in alto. Numeri e grafici raccontano sempre lo stesso intervallo e non si contraddicono."),
        ("Il dato che conta in primo piano", "L'anno in corso è viola, quello precedente grigio. Il confronto c'è, ma l'attenzione va subito al presente. Il valore finale è scritto accanto alla linea."),
        ("Barre orizzontali per i nomi lunghi", "Le categorie si leggono senza ruotare il testo e il valore sta alla fine di ogni barra. Le barre partono tutte dalla stessa linea, così il confronto è immediato."),
    ]),
    screen(3, "Magazzino", "Magazzino", "Le scorte da tenere sotto controllo, per chi gestisce il magazzino.", SCREEN_STOCK, [
        ("Prima il riepilogo", "Sopra l'elenco, quanti articoli richiedono un intervento. Si capisce subito se oggi c'è qualcosa da fare."),
        ("Giacenza e soglia nella stessa barra", "La barra mostra quanto resta, la tacca chiara indica la soglia minima. Chi è sotto soglia si vede senza leggere i numeri."),
        ("Stato con colore, simbolo e parola", "Rosso, giallo e verde hanno sempre un simbolo diverso e un'etichetta. Il colore aiuta, ma non è l'unica informazione."),
        ("Numeri solo dove serve un'azione", "La quantità da riordinare compare solo per gli articoli sotto soglia. Nelle altre righe un trattino lascia la tabella pulita."),
    ]),
    screen(4, "Produzione", "Produzione", "Il carico dei reparti e lo stato delle commesse, per il responsabile di produzione.", SCREEN_PROD, [
        ("Le fasi nell'ordine reale", "Gli ordini in lavorazione seguono il percorso del processo, da sinistra a destra, dal taglio alla spedizione."),
        ("Tre reparti, tre colori distinguibili", "I colori delle colonne sono scelti per essere distinti anche da chi è daltonico. Il totale sta in cima a ogni colonna, il dettaglio nella legenda."),
        ("Avanzamento e scadenza sulla stessa riga", "La barra dice quanto manca, l'etichetta dice se la commessa è in tempo. Le due informazioni si leggono insieme."),
    ]),
])


def dashboard():
    return f"""<section class="screens-intro" data-name="Come si vedono i dati">
    <div class="wrap">
      <div class="sec-head centered" data-enter><span class="eyebrow">Fase 4 in pratica</span><h2>Come si vedono i dati</h2><p>Quattro schermate di un gestionale Merkorn con dati di esempio, e accanto a ognuna il motivo delle scelte, così vedi cosa intendiamo quando parliamo di esperienza d'uso.</p></div>
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
     "È un gestionale progettato sui processi di una sola azienda. Invece di cambiare il tuo modo di lavorare per stare dentro un programma pronto, il software segue il percorso vero di ordini, magazzino, produzione e fatture."),
    ("Quando conviene un gestionale personalizzato rispetto a uno pronto?",
     "Quando accanto al gestionale torna fuori il foglio Excel, perché il programma non copre una parte del lavoro. Nel primo incontro guardiamo insieme se il su misura conviene davvero, e se ti basta un programma pronto te lo diciamo."),
    ("Quanto costa un gestionale su misura?",
     "Dipende da quante aree deve seguire. Dopo l'analisi ti diamo un preventivo diviso per fasi, con tempi e costi chiari prima di iniziare, e partiamo da moduli già collaudati per non farti pagare quello che esiste già."),
    ("Quanto tempo serve per sviluppare un gestionale personalizzato?",
     "Lavoriamo per rilasci, quindi le prime parti le usi già durante il progetto. La durata complessiva la fissiamo fase per fase, dopo aver visto come lavori."),
    ("Il gestionale si collega alla fatturazione elettronica e alla contabilità?",
     "Sì. Lo colleghiamo ai programmi che usi già, contabilità e fatturazione elettronica comprese, così ogni dato si scrive una volta sola e il commercialista continua a lavorare come prima."),
    ("Lavorate solo in Puglia?",
     "Siamo a Mottola, in provincia di Taranto, e lavoriamo soprattutto con imprese pugliesi, tra Taranto, Bari, Brindisi, Lecce e Matera. Seguiamo anche aziende nel resto d'Italia, con il primo incontro online."),
]

FAQ_SERVIZI = [
    ("Si può partire da un solo reparto?",
     "Sì, ed è spesso la scelta migliore. Si parte da dove si perde più tempo, per esempio il magazzino, e le altre aree si aggiungono dopo sulla stessa base."),
    ("Potete importare i dati da Excel o dal vecchio gestionale?",
     "Sì. Importiamo anagrafiche, articoli e giacenze, e prima facciamo pulizia di doppioni e righe incomplete, così il nuovo gestionale parte con dati di cui ti puoi fidare."),
    ("Sviluppate anche app per telefono e tablet?",
     "Sì, per il magazzino, le consegne e gli interventi fuori sede, collegate al gestionale e pensate per funzionare anche con poco segnale."),
    ("Cosa succede dopo il rilascio?",
     "Il software lo segue lo stesso team che l'ha costruito, senza subappalti. Assistenza, aggiornamenti e nuove funzioni arrivano quando è il tuo lavoro a chiederle."),
]


def faq(items, title="Domande frequenti", intro=None, name="Domande frequenti"):
    qs = "\n        ".join(f'<details class="qa"><summary><h3>{q}</h3><span class="qa-i" aria-hidden="true"></span></summary><p>{a}</p></details>' for q, a in items)
    return section(name, "Domande frequenti", title, intro, f'<div class="faq" data-enter>\n        {qs}\n      </div>')


def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


# ---------------------------------------------------------------- il digitale spiegato

MONTHS = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]


def it_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)} {MONTHS[int(m) - 1]} {y}"


def link_cards(items):
    """Cards that each open their own page: (icon key, kicker, title, text, href)."""
    out = []
    for n, (ico, k, h, t, href) in enumerate(items):
        out.append(f'<a class="card" data-enter style="--dir:{-1 if n % 2 == 0 else 1}" href="{href}">{card_icon(ico)}<div class="ctx"><span class="kicker">{k}</span><h3>{h}</h3><p>{t}</p></div></a>')
    return '<div class="cards">\n        ' + "\n        ".join(out) + "\n      </div>"


def scene_cards(items):
    out = [f'<article class="card" data-enter style="--dir:{-1 if n % 2 == 0 else 1}">{card_icon(ico)}<div class="ctx"><h3>{h}</h3><p>{t}</p></div></article>'
           for n, (ico, h, t) in enumerate(items)]
    return '<div class="cards">\n        ' + "\n        ".join(out) + "\n      </div>"


def article_cards(articles):
    return link_cards([(ico, f"{k} · {sp.reading_minutes(intro, secs)} min", title, desc, sp.article_path(slug))
                       for slug, k, ico, title, _, desc, intro, secs in articles])


def glossary():
    rows = []
    for term, definition, rel in sp.GLOSSARY:
        more = f' <a href="{sp.article_path(rel)}">Leggi l\'articolo</a>' if rel else ""
        rows.append(f'<div class="gl" id="{sp.term_id(term)}"><dt>{term}</dt><dd>{definition}{more}</dd></div>')
    return f'<dl class="gloss" data-enter>\n        ' + "\n        ".join(rows) + "\n      </dl>"


SPIEGATO = f"""  {page_hero("Il digitale spiegato", ["Il digitale <em>spiegato</em>", "con calma"], "Articoli brevi su gestionali, dati e processi, scritti per chi lavora in azienda e non per gli addetti ai lavori. Esempi concreti e parole di tutti i giorni.", 3)}

  {section("Articoli", "Articoli", "Da leggere in pochi minuti", "Ogni articolo risponde a una domanda che ci fanno spesso nei primi incontri.", article_cards(sp.ARTICLES))}

  {section("Situazioni tipiche", "Situazioni tipiche", "Scene di lavoro che un software può semplificare", "Momenti che si ripetono in molte piccole imprese, e cosa cambia quando il gestionale li segue.",
           scene_cards(sp.SITUATIONS))}

  {section("Glossario", "Glossario", "Le parole del gestionale, in breve", "I termini che si incontrano più spesso quando si parla di software gestionale.", glossary())}

  {band("Primo incontro", "Hai una domanda che qui non trovi?", "Scrivici, la risposta potrebbe diventare il prossimo articolo. Oppure fissiamo un appuntamento e ne parliamo guardando come lavorate.")}"""

SPIEGATO_LD = [
    {"@type": "ItemList", "name": "Il digitale spiegato, articoli", "itemListElement": [
        {"@type": "ListItem", "position": i, "url": f"{BASE}/{sp.article_path(a[0])}", "name": a[3]} for i, a in enumerate(sp.ARTICLES, 1)]},
    {"@type": "DefinedTermSet", "@id": f"{BASE}/{sp.HUB}#glossario", "name": "Glossario del software gestionale", "inLanguage": "it-IT",
     "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t, "description": d, "url": f"{BASE}/{sp.HUB}#{sp.term_id(t)}"} for t, d, _ in sp.GLOSSARY]},
]


def article_page(a):
    slug, k, ico, title, hero_title, desc, intro, secs = a
    mins = sp.reading_minutes(intro, secs)
    body = "".join(f'<div><h2>{h}</h2>{"".join(f"<p>{x}</p>" for x in ps)}</div>' for h, ps in secs)
    others = [o for o in sp.ARTICLES if o[0] != slug][:2]
    html = f"""  {page_hero("Il digitale spiegato", [hero_title], intro, 3)}

  <section data-name="Articolo">
    <div class="wrap doc article">
      <p class="meta">{k} · {mins} minuti di lettura · {it_date(sp.PUBLISHED)}</p>
      {body}
      <div><a class="more-link" href="{sp.HUB}"><span aria-hidden="true">←</span> Tutti gli articoli</a></div>
    </div>
  </section>

  {section("Altri articoli", "Il digitale spiegato", "Altri articoli", None, article_cards(others))}"""
    ld = [{"@type": "Article", "headline": title, "description": desc, "inLanguage": "it-IT",
           "datePublished": sp.PUBLISHED, "dateModified": sp.PUBLISHED, "image": f"{BASE}/assets/og-image.png",
           "author": {"@id": f"{BASE}/#org"}, "publisher": {"@id": f"{BASE}/#org"},
           "mainEntityOfPage": f"{BASE}/{sp.article_path(slug)}", "isPartOf": {"@id": f"{BASE}/{sp.HUB}#page"}}]
    return (sp.article_path(slug), f"{title} | Merkorn", desc, 3.3, html, True, (), ld)


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
        <p class="lead">Costruiamo il gestionale attorno al tuo lavoro, dagli ordini al magazzino, dalla produzione alla fattura. Prima di scrivere una riga di codice veniamo a vedere come lavori, in reparto, al bancone, in magazzino.</p>
        <div class="actions">
          <a class="btn" href="contattaci.html"><span>Prenota un appuntamento</span></a>
          <a class="btn ghost" href="metodo.html"><span>Come lavoriamo</span></a>
        </div>
        <div class="scroll-cue"><i aria-hidden="true"></i>Scorri per continuare</div>
      </div>
    </div>
  </section>

  {statement("Il nostro approccio",
             "Lo strumento si piega al processo, non il contrario.",
             "strumento,processo",
             "Se ogni venerdì qualcuno passa due ore a ricopiare ordini da WhatsApp, c'è un pezzo di lavoro che un software può togliere.",
             "Approccio")}

  {hscroll("Come lavoriamo", "Prima veniamo a vedere, poi scriviamo il codice", ("metodo.html", "Il metodo nel dettaglio"), phase_panels(), "Come lavoriamo")}

  {section("Servizi", "Servizi", "Gestionali personalizzati per ogni reparto", "Per le piccole e medie imprese pugliesi, dall'agroalimentare alla logistica, e per chi ci cerca dal resto d'Italia.", HOME_SERVICES)}

  {band("Primo incontro", "Il primo incontro è in azienda", CHAT_TEXT)}

  {principles()}

  {faq(FAQ_HOME, "Software gestionale su misura, le domande più comuni")}"""

METODO = f"""  {page_hero("Come lavoriamo", ["Come sviluppiamo un <em>gestionale personalizzato</em>"], "Prima veniamo a vedere, poi scriviamo il codice. Sono quattro fasi, e alla fine di ognuna hai in mano qualcosa che puoi controllare.", 2)}

  <section data-name="Le fasi">
    <div class="wrap">
      <div class="sec-head" data-enter><span class="eyebrow">Le fasi</span><h2>Dal primo sopralluogo alle schermate</h2></div>
      {legs()}
    </div>
  </section>

  {dashboard()}

  {principles()}"""

SERVIZI = f"""  {page_hero("Servizi", ["Software gestionale <em>personalizzato</em> per la tua azienda"], "Gestionale su misura, magazzino e produzione, app per le consegne e analisi dei processi, per le PMI che hanno superato i fogli Excel ma non si ritrovano in un programma pronto.", 3)}

  {hscroll("Cosa facciamo", "Quattro servizi, un solo progetto", None, service_panels(), "Cosa facciamo")}

  {statement("Un unico progetto",
             "Dall'analisi all'assistenza ti seguono le stesse persone, senza subappalti.",
             "persone,subappalti",
             "Così niente si perde tra chi raccoglie le esigenze e chi scrive il codice.",
             "Un unico progetto")}

  {section("Per chi lavoriamo", "Per chi lavoriamo", "Imprese con processi tutti loro",
           "Lavoriamo soprattutto con PMI pugliesi, molte nella filiera agroalimentare, che hanno superato i fogli Excel ma non trovano un gestionale pronto che le segua.",
           cards([("Produzione", "Agroalimentare e produzione", "Lotti, scadenze e tracciabilità, fasi di lavorazione, commesse e controlli di qualità."),
                  ("Distribuzione", "Commercio e logistica", "Magazzino su più depositi, ordini dei clienti, documenti di trasporto e consegne."),
                  ("Servizi", "Squadre sul territorio", "Interventi programmati, rapportini dal telefono e un'app per i tecnici collegata all'ufficio.")], "three"))}

  {prose("Integrazioni", "Integrazioni", "Collegato ai programmi che usi già",
         ["Colleghiamo il gestionale alla contabilità e alla fatturazione elettronica che usi oggi, così ogni dato si scrive una volta sola e non devi cambiare commercialista."])}

  {faq(FAQ_SERVIZI, "Domande sui nostri servizi")}

  {band("Primo incontro", "Raccontaci cosa ti serve", CHAT_TEXT)}"""

CHI = f"""  {page_hero("Chi siamo", ["Una software house in Puglia che <em>prima viene a vedere</em>"], "Siamo a Mottola, in provincia di Taranto. Sviluppiamo gestionali su misura per le PMI e spieghiamo il digitale con calma, perché un'impresa che lo capisce lo sa anche scegliere.", 4)}

  {statement("Missione",
             "Rendere il digitale comprensibile e utile per chi lavora nelle PMI pugliesi.",
             "comprensibile,utile",
             "Con strumenti costruiti attorno al loro lavoro e con contenuti che spiegano invece di vendere.",
             "Missione")}

  {prose("Esperienza d'uso", "Esperienza d'uso", "Prima si progetta l'uso, poi si scrive il codice",
         ["Disegniamo le schermate insieme a chi le userà e le proviamo al bancone, in magazzino o in reparto prima di svilupparle. Se qualcuno deve chiedere a un collega come si fa, la schermata va rifatta."])}

  {section("Il team", "Il team", "Le persone che seguono il tuo progetto",
           "Un team piccolo e interno, senza subappalti. Le persone che conosci al primo incontro sono le stesse che ti seguono dopo il rilascio.",
           cards([("Commerciale", "Sales manager", "È la prima persona che incontri. Viene in azienda, ascolta come lavorate e prepara con te proposta, tempi e costi, dicendoti anche cosa non conviene fare."),
                  ("Requisiti", "Project manager e data analyst", "Trasforma quello che abbiamo visto in requisiti chiari. Studia i dati e i processi di oggi, divide il progetto in fasi e ti tiene aggiornato a ogni passo."),
                  ("Design", "Product designer", "Progetta le schermate. Osserva chi le userà, disegna i passaggi e li prova sul posto prima che diventino codice."),
                  ("Codice", "Developer", "Scrive il software, lo collega ai programmi che usi già e resta il tuo riferimento dopo il rilascio, per aggiornamenti e assistenza.")]))}

  {prose("Come costruiamo", "Come costruiamo", "Fondamenta riusabili, superficie su misura",
         ["I cinque blocchi del marchio raccontano il metodo, una base di moduli collaudati, sopra i componenti costruiti per te e in cima le schermate disegnate per il tuo lavoro."])}

  {section("Valori", "Come lavoriamo con i clienti", "Tre impegni che manteniamo", None,
           cards([("Concretezza", "Esempi basati su esperienze reali", "Ogni proposta parte da situazioni che abbiamo già visto in altre aziende e ti dice cosa cambia nella tua giornata."),
                  ("Chiarezza", "Tempi e costi definiti", "Obiettivi, durata e costo di ogni fase li concordiamo prima di iniziare, e se qualcosa cambia te lo diciamo subito."),
                  ("Continuità", "Lo stesso team nel tempo", "Chi scrive il software lo segue anche dopo, senza passarlo a qualcun altro.")], "three"))}

  {band("Primo incontro", "Conosciamoci in azienda", CHAT_TEXT)}"""

CONTATTI = contact_form(
    heading="Contattaci",
    intro="Scrivici per fissare un appuntamento o chiedere un preventivo per un gestionale su misura. Ti rispondiamo personalmente.",
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
          <li><b>Cookie.</b> Un cookie tecnico che ricorda le vostre scelte e, solo con il vostro consenso, cookie statistici. I dettagli sono nella <a href="cookie.html">cookie policy</a>.</li>
        </ul></div>
      <div><h2>Finalità e basi giuridiche</h2>
        <ul>
          <li>Rispondere alle richieste, fissare un appuntamento e preparare un preventivo: misure precontrattuali adottate su vostra richiesta (art. 6.1.b GDPR).</li>
          <li>Garantire il funzionamento e la sicurezza del sito: legittimo interesse del titolare (art. 6.1.f GDPR).</li>
          <li>Statistiche aggregate sulle visite: consenso, che potete revocare in qualsiasi momento (art. 6.1.a GDPR).</li>
        </ul></div>
      <div><h2>Conferimento dei dati</h2><p>Il conferimento dei dati nel modulo è facoltativo, ma senza nome, email e messaggio non possiamo rispondere alla richiesta.</p></div>
      <div><h2>Chi riceve i dati</h2><p>I dati sono trattati dal personale di Merkorn e da fornitori che agiscono come responsabili del trattamento:</p>
        <ul>
          <li>Vercel Inc., per l'hosting del sito e per la funzione che inoltra i messaggi del modulo alla nostra casella email;</li>
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
    (sp.HUB, "Il digitale spiegato, gestionali in parole semplici | Merkorn",
     "Articoli brevi e un glossario per capire gestionali, ERP, fatturazione elettronica e digitalizzazione delle PMI, con esempi concreti.",
     3.3, SPIEGATO, True, (), SPIEGATO_LD),
] + [article_page(a) for a in sp.ARTICLES] + [
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
        (ROOT / path).write_text(page(path, title, desc, seed, body, form, scripts, ld), encoding="utf-8")
        print("scritto", path)
    # sitemap for search engines
    today = date.today().isoformat()
    urls = "".join(
        f"<url><loc>https://merkorn.com/{'' if p == 'index.html' else p}</loc><lastmod>{today}</lastmod>"
        f"<priority>{'1.0' if p == 'index.html' else '0.3' if p in ('privacy.html', 'cookie.html') else '0.8'}</priority></url>"
        for p, *_ in PAGES)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    print("scritto sitemap.xml")
