"""Genera le pagine HTML del sito nella cartella principale.

Uso:  python3 src/build.py
Header, footer e form di contatto stanno in partials.py e sono uguali su ogni pagina.
I blocchi di sezione qui sotto (frase fissata, scorrimento orizzontale, campo viola,
card impilate, dashboard) sono riutilizzati tra le pagine, ognuna con i propri contenuti.
"""
from pathlib import Path
from partials import page, contact_form, EMAIL

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- contenuti

# fase, titolo, descrizione, risultato
PHASES = [
    ("Analisi del processo", "Studiamo come lavorate",
     "Seguiamo un ordine dall'ufficio al magazzino e annotiamo dove i dati si ricopiano a mano.",
     "Una mappa del processo e le priorità di intervento"),
    ("Fondamenta riusabili", "Partiamo da moduli collaudati",
     "Anagrafiche, permessi, stampe e contabilità servono a quasi tutte le aziende. Averli pronti riduce tempi e costi.",
     "Una base stabile con i vostri dati già importati"),
    ("Componenti su misura", "Sviluppiamo le parti specifiche",
     "Commesse, documenti di trasporto e consegne, costruiti sul vostro flusso e provati con chi li userà.",
     "Rilasci frequenti che potete verificare"),
    ("Interfaccia", "Una schermata per ogni attività",
     "Pulsanti grandi in reparto, tabelle complete in ufficio. Ogni operazione con meno passaggi possibile.",
     "Un software che si impara in poco tempo"),
]

PRINCIPLES = [
    ("Una schermata, un compito", "Chi la usa sa subito cosa fare."),
    ("Funzioni principali a un tocco", "Niente menu annidati per le operazioni di tutti i giorni."),
    ("Leggibile ovunque", "Anche su telefoni meno recenti e con connessioni lente."),
    ("Nuove funzioni quando servono", "Ogni aggiunta parte da un'esigenza reale del lavoro."),
]

SERVICES = [
    ("Sviluppo", "Gestionali su misura",
     "Ordini, magazzino, produzione e commesse in un unico sistema, costruito sul vostro modo di lavorare.",
     ["Ordini e offerte", "Magazzino", "Produzione", "Commesse", "Documenti di trasporto"]),
    ("Consulenza", "Analisi dei processi",
     "Un documento che descrive come lavorate oggi e dove il software può ridurre tempi ed errori.",
     ["Mappa del processo", "Punti critici", "Priorità di intervento"]),
    ("Mobile", "App per reparto e consegne",
     "App per tablet e smartphone, utilizzabili anche con una connessione lenta.",
     ["Carico e scarico merce", "Consegne", "Firma del cliente"]),
    ("Dopo il rilascio", "Assistenza ed evoluzione",
     "Lo stesso team che ha sviluppato il software lo segue e lo fa crescere nel tempo.",
     ["Assistenza agli utenti", "Aggiornamenti", "Nuove funzioni"]),
]

CHAT_TEXT = "Ci raccontate come lavorate, noi vi spieghiamo come possiamo aiutarvi. Senza impegno, in azienda o online."

ICO = '<span class="ico" aria-hidden="true"><i></i><i></i><i></i></span>'

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


def principles(title="Come progettiamo le interfacce"):
    items = "\n        ".join(f'<li style="--i:{i}"><div><strong>{a}</strong><span>{b}</span></div></li>' for i, (a, b) in enumerate(PRINCIPLES))
    return f"""<section class="principles" data-name="Principi">
    <div class="wrap">
      <div class="sec-head" data-enter><span class="eyebrow">Principi di progettazione</span><h2>{title}</h2><p>Le regole che applichiamo a ogni progetto, prima di scrivere codice.</p></div>
      <ol class="rules stack">
        {items}
      </ol>
    </div>
  </section>"""


def cards(items, cols="", link=None):
    out = []
    for n, (k, h, p) in enumerate(items):
        tag, href = ("a", f' href="{link}"') if link else ("article", "")
        out.append(f'<{tag} class="card" data-enter style="--dir:{-1 if n % 2 == 0 else 1}"{href}>{ICO}<span class="kicker">{k}</span><h3>{h}</h3><p>{p}</p></{tag}>')
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
    screen(1, "Home", "Home", "La prima schermata della giornata: cosa sta succedendo e cosa richiede attenzione.", SCREEN_HOME, [
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
      <div class="sec-head centered" data-enter><span class="eyebrow">Fase 4 in pratica</span><h2>Come si vedono i dati</h2><p>Quattro schermate di un gestionale Merkorn, con dati di esempio. Per ognuna spieghiamo le scelte di UX che rendono i dati leggibili a colpo d'occhio.</p></div>
    </div>
  </section>

  {SCREENS}"""


# ---------------------------------------------------------------- pagine

HOME_SERVICES = (cards([(k, h, p) for k, h, p, _ in SERVICES], link="servizi.html")
                 + '\n      <a class="more-link" href="servizi.html">Tutti i servizi <span aria-hidden="true">→</span></a>')

HOME = f"""  <section class="hero" data-exit data-name="Inizio">
    <div class="wrap">
      <div class="center">
        <span class="eyebrow">Software house in Puglia</span>
        <h1>
          <span class="ln"><span style="--i:0">Software gestionale</span></span>
          <span class="ln"><span style="--i:1"><em>su misura</em> per le PMI</span></span>
        </h1>
        <p class="lead">Progettiamo gestionali partendo da come lavora la vostra azienda, dall'ordine alla fattura.</p>
        <div class="actions">
          <a class="btn" href="contattaci.html"><span>Prenota un appuntamento</span></a>
          <a class="btn ghost" href="metodo.html"><span>Come lavoriamo</span></a>
        </div>
        <div class="scroll-cue"><i aria-hidden="true"></i>Scorri per continuare</div>
      </div>
    </div>
  </section>

  {statement("Il nostro approccio",
             "Molti gestionali chiedono alle persone di adattarsi al software. Noi partiamo dal lavoro di ogni giorno.",
             "persone,lavoro",
             "Così il software viene adottato più facilmente e spariscono i passaggi manuali tra fogli di calcolo e programmi diversi.",
             "Approccio")}

  {hscroll("Come lavoriamo", "Quattro fasi, sempre nello stesso ordine", ("metodo.html", "Il metodo nel dettaglio"), phase_panels(), "Come lavoriamo")}

  {section("Servizi", "Servizi", "Cosa facciamo", "Per piccole e medie imprese con processi specifici.", HOME_SERVICES)}

  {band("Primo incontro", "Il primo incontro è una chiacchierata", CHAT_TEXT)}

  {principles()}"""

METODO = f"""  {page_hero("Come lavoriamo", ["Un metodo in <em>quattro fasi</em>"], "Dall'analisi del lavoro reale a un software semplice da usare. Ogni fase produce un risultato che potete verificare.", 2)}

  <section data-name="Le fasi">
    <div class="wrap">
      <div class="sec-head" data-enter><span class="eyebrow">Le fasi</span><h2>Dall'analisi all'interfaccia</h2></div>
      {legs()}
    </div>
  </section>

  {dashboard()}

  {principles()}"""

SERVIZI = f"""  {page_hero("Servizi", ["Software su misura per il <em>vostro processo</em>"], "Gestionali, app per il reparto e analisi dei processi per le PMI. Il software si adatta a come lavorate.", 3)}

  {hscroll("Cosa facciamo", "Quattro servizi collegati tra loro", None, service_panels(), "Cosa facciamo")}

  {statement("Un unico progetto",
             "Un solo progetto, seguito dalle stesse persone dall'analisi all'assistenza.",
             "progetto,persone",
             "Così nessuna informazione si perde tra un passaggio e l'altro.",
             "Un unico progetto")}

  {section("Per chi lavoriamo", "Per chi lavoriamo", "Aziende con processi specifici",
           "Imprese che hanno superato i fogli di calcolo ma non trovano un software pronto adatto a loro.",
           cards([("Produzione", "Aziende manifatturiere", "Commesse, avanzamento della produzione e controlli di qualità."),
                  ("Distribuzione", "Commercio e logistica", "Ordini, magazzino su più depositi e consegne."),
                  ("Servizi", "Squadre sul territorio", "Interventi programmati e rapportini digitali.")], "three"))}

  {prose("Integrazioni", "Integrazioni", "Collegato ai software che usate già",
         ["Colleghiamo il gestionale ai programmi già in uso, come contabilità e fatturazione elettronica, così i dati si inseriscono una sola volta."])}

  {band("Primo incontro", "Parliamo del servizio che vi serve", CHAT_TEXT)}"""

CHI = f"""  {page_hero("Chi siamo", ["Una software house che parte dalla <em>UX</em>"], "Software gestionale su misura per le PMI italiane, dalla Puglia.", 4)}

  {statement("Missione",
             "Portiamo il digitale nelle piccole e medie imprese partendo dalle persone e dal loro lavoro quotidiano.",
             "persone,digitale",
             "Prima osserviamo come lavorate, poi sviluppiamo.",
             "Missione")}

  {prose("UX design first", "UX design first", "Prima si progetta l'uso, poi si scrive il codice",
         ["Disegniamo le schermate insieme a chi le userà e le proviamo nei luoghi di lavoro prima di svilupparle. Il risultato è un software che richiede poca formazione."])}

  {prose("Come costruiamo", "Come costruiamo", "Fondamenta riusabili, superficie su misura",
         ["I cinque blocchi del marchio raccontano il nostro metodo: una base di moduli collaudati, i componenti sopra e, in cima, le schermate su misura."])}

  {section("Valori", "Come lavoriamo con i clienti", "Tre impegni che manteniamo", None,
           cards([("Concretezza", "Esempi reali, non concetti", "Ogni proposta dice cosa cambierà nel vostro lavoro."),
                  ("Chiarezza", "Tempi e costi definiti", "Obiettivi, durata e costo di ogni fase concordati prima di iniziare."),
                  ("Continuità", "Lo stesso team nel tempo", "Chi sviluppa il software lo segue anche dopo il rilascio.")], "three"))}

  {band("Primo incontro", "Conosciamoci con una chiacchierata", CHAT_TEXT)}"""

CONTATTI = contact_form(
    heading="Contattaci",
    intro="Scriveteci per prenotare un appuntamento o per qualsiasi domanda. Vi rispondiamo personalmente.",
    level="h1",
).replace('class="contact"', 'class="contact page-contact"', 1)

PRIVACY = f"""  {page_hero("Privacy", ["Informativa sul trattamento dei dati"], "Come trattiamo i dati inviati con il modulo di contatto, ai sensi del Regolamento UE 2016/679.", 5)}

  <section data-name="Informativa">
    <div class="wrap doc">
      <div><h2>Titolare del trattamento</h2><p>Merkorn, <span class="todo">ragione sociale, partita IVA e sede legale da completare</span>. Per qualsiasi richiesta potete scrivere a {EMAIL}.</p></div>
      <div><h2>Dati raccolti</h2><p>Nome e cognome, indirizzo email e, se li indicate, azienda, telefono e testo del messaggio.</p></div>
      <div><h2>Finalità e base giuridica</h2><p>Usiamo i dati solo per rispondere alla richiesta e organizzare un eventuale appuntamento. La base giuridica è il consenso espresso con l'invio del modulo.</p></div>
      <div><h2>Modalità del trattamento</h2><p>Il modulo invia i dati alla nostra email tramite il servizio FormSubmit, che agisce come fornitore tecnico.</p></div>
      <div><h2>Conservazione</h2><p>Conserviamo i dati per il tempo necessario a gestire la richiesta e comunque non oltre <span class="todo">periodo da definire</span>, salvo un successivo rapporto contrattuale.</p></div>
      <div><h2>Diritti dell'interessato</h2><p>Potete chiedere accesso, rettifica, cancellazione o limitazione dei dati e revocare il consenso scrivendo a {EMAIL}. Potete anche presentare reclamo al Garante per la protezione dei dati personali.</p></div>
    </div>
  </section>"""

PAGES = [
    ("index.html", "Merkorn", "Merkorn sviluppa software gestionale su misura per le piccole e medie imprese italiane, partendo dal processo aziendale.", 0.0, HOME, True),
    ("metodo.html", "Come lavoriamo", "Il metodo Merkorn in quattro fasi e quattro schermate di esempio che mostrano come la UX rende leggibili i dati.", 1.3, METODO, True, ("assets/schermate.js",)),
    ("servizi.html", "Servizi", "Gestionali su misura, analisi dei processi, app per reparto e consegne, assistenza ed evoluzione del software.", 2.6, SERVIZI, True),
    ("chi-siamo.html", "Chi siamo", "Merkorn è una software house pugliese che sviluppa gestionali su misura per le PMI partendo dalla UX.", 3.9, CHI, True),
    ("contattaci.html", "Contattaci", "Contattate Merkorn per prenotare un appuntamento o chiedere informazioni sui servizi.", 5.2, CONTATTI, False),
    ("privacy.html", "Privacy", "Informativa sul trattamento dei dati personali raccolti tramite il modulo di contatto del sito Merkorn.", 6.5, PRIVACY, True),
]

if __name__ == "__main__":
    for path, title, desc, seed, body, form, *extra in PAGES:
        (ROOT / path).write_text(page(path, title, desc, seed, body, form, *extra), encoding="utf-8")
        print("scritto", path)
