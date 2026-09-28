"""Genera le pagine HTML del sito nella cartella principale.

Uso:  python3 src/build.py
Header, footer e form di contatto stanno in partials.py e sono uguali su ogni pagina.
I blocchi di sezione qui sotto (frase fissata, scorrimento orizzontale, campo viola,
card impilate) sono riutilizzati tra le pagine, ognuna con i propri contenuti.
"""
from pathlib import Path
from partials import page, contact_form, EMAIL

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- contenuti

PHASES = [
    ("Analisi del processo", "Studiamo come lavora l'azienda",
     "Passiamo del tempo in azienda per capire come si muove un ordine tra ufficio, magazzino e produzione. Annotiamo dove i dati vengono ricopiati a mano e dove si creano attese.",
     ["Incontri brevi con chi usa ogni giorno gli strumenti attuali", "Raccolta di documenti, moduli e fogli di calcolo in uso", "Mappa delle attività e dei passaggi tra reparti"],
     ["Un documento che descrive il processo attuale", "Le priorità di intervento concordate con voi"]),
    ("Fondamenta riusabili", "Partiamo da moduli collaudati",
     "Anagrafiche, utenti e permessi, stampe e collegamento con la contabilità sono comuni a quasi tutte le aziende. Usiamo moduli già testati su altri progetti, così tempi e costi restano contenuti.",
     ["Anagrafiche di clienti, fornitori e articoli", "Utenti, ruoli e permessi di accesso", "Modelli di stampa e collegamento con i software già in uso"],
     ["Una base stabile su cui costruire il resto", "Dati esistenti importati e verificati"]),
    ("Componenti su misura", "Sviluppiamo le parti specifiche",
     "Commesse, documenti di trasporto, pianificazione delle consegne e controlli di qualità vengono sviluppati sul vostro flusso di lavoro. Ogni componente viene provato con le persone che lo useranno.",
     ["Sviluppo per rilasci successivi, un componente alla volta", "Prove con il personale prima di ogni rilascio", "Correzioni in base a come viene usato nella pratica"],
     ["Componenti in uso già durante il progetto", "Un avanzamento che potete verificare di settimana in settimana"]),
    ("Interfaccia", "Progettiamo ogni schermata per un'attività",
     "In reparto usiamo pulsanti grandi e pochi passaggi, in ufficio tabelle complete per confrontare i dati. L'obiettivo è che ogni operazione richieda il minor numero possibile di passaggi.",
     ["Schermate diverse per ruoli diversi", "Versioni per computer, tablet e smartphone", "Verifica della leggibilità nei luoghi di lavoro reali"],
     ["Un software che si impara in poco tempo", "Meno errori di inserimento dei dati"]),
]

PRINCIPLES = [
    ("Una schermata per ogni attività", "Ogni pagina è dedicata a un compito preciso, così chi la usa sa subito cosa fare."),
    ("Funzioni principali a portata di mano", "Le operazioni di tutti i giorni si raggiungono con un tocco, senza menu annidati."),
    ("Leggibile su qualsiasi dispositivo", "Testi chiari e pagine leggere, pensati anche per telefoni meno recenti e connessioni lente."),
    ("Nuove funzioni solo quando servono", "Ogni aggiunta parte da un'esigenza del lavoro quotidiano e viene introdotta in modo graduale."),
]

SERVICES = [
    ("Sviluppo", "Gestionali su misura",
     "Ordini, magazzino, produzione e commesse gestiti in un unico sistema, costruito sul flusso di lavoro reale dell'azienda.",
     ["Ordini e offerte", "Magazzino", "Produzione", "Commesse", "Documenti di trasporto"]),
    ("Consulenza", "Analisi dei processi",
     "Un documento che descrive come lavora oggi l'azienda e dove il software può ridurre tempi ed errori. Resta di vostra proprietà in ogni caso.",
     ["Mappa del processo", "Punti critici", "Priorità di intervento"]),
    ("Mobile", "App per reparto e consegne",
     "Applicazioni per tablet e smartphone pensate per magazzino e trasporti, utilizzabili anche con una connessione lenta.",
     ["Carico e scarico merce", "Consegne", "Firma del cliente", "Foto e note"]),
    ("Dopo il rilascio", "Assistenza ed evoluzione",
     "Il software viene seguito dallo stesso team che lo ha sviluppato. Le nuove funzioni vengono aggiunte quando emergono esigenze concrete.",
     ["Assistenza agli utenti", "Aggiornamenti", "Nuove funzioni"]),
]

CHAT_TEXT = ("Ci raccontate come lavorate e di cosa avete bisogno, noi vi spieghiamo come potremmo aiutarvi. "
             "Senza impegno, in azienda oppure online.")

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
        for i, (k, h, p, _, _) in enumerate(PHASES, 1))


def service_panels():
    out = []
    for i, (k, h, p, tags) in enumerate(SERVICES, 1):
        t = "".join(f"<li>{x}</li>" for x in tags)
        out.append(f'<article class="panel"><span class="num">0{i}</span><span class="k">{k}</span><h3>{h}</h3><p>{p}</p><ul>{t}</ul></article>')
    return "\n          ".join(out)


def band(eyebrow, title, text, cta=("contattaci.html", "Prenota una chiacchierata"), name="Primo incontro"):
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
      <div class="sec-head" data-enter><span class="eyebrow">Principi di progettazione</span><h2>{title}</h2><p>La progettazione dell'esperienza d'uso viene prima dello sviluppo. Queste sono le regole che applichiamo a ogni progetto.</p></div>
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


def legs_detailed():
    out = []
    for i, (k, h, p, doing, get) in enumerate(PHASES, 1):
        d = "".join(f"<li>{x}</li>" for x in doing)
        g = "".join(f"<li>{x}</li>" for x in get)
        out.append(f'<article class="leg" data-enter><span class="dot">{i}</span><div class="body"><span class="k">{k}</span><h3>{h}</h3><p>{p}</p>'
                   f'<div class="split"><div><b>Cosa facciamo</b><ul>{d}</ul></div><div><b>Cosa ricevete</b><ul>{g}</ul></div></div></div></article>')
    return '<div class="legs" data-line>\n        ' + "\n        ".join(out) + "\n      </div>"



def app_frame(crumb, inner, kind="desk"):
    return f"""<div class="app {kind}" data-enter>
        <div class="app-bar"><span class="mark" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span><span class="crumb">{crumb}</span><span class="sample">Dati di esempio</span></div>
        <div class="app-body">{inner}</div>
      </div>"""


def screen(name, eyebrow, title, text, points, frame, flip=False):
    pts = "".join(f"<li>{x}</li>" for x in points)
    return f"""<section class="screen{' flip' if flip else ''}" data-name="{name}">
    <div class="wrap screen-grid">
      <div class="screen-txt" data-enter>
        <span class="eyebrow">{eyebrow}</span>
        <h2>{title}</h2>
        <p>{text}</p>
        <ul class="ticks">{pts}</ul>
      </div>
      {frame}
    </div>
  </section>"""


DASH = app_frame("Direzione / Cruscotto", """
          <div class="filters" role="group" aria-label="Periodo">
            <button type="button" class="chip" data-range="3">Ultimi 3 mesi</button>
            <button type="button" class="chip" data-range="6">Ultimi 6 mesi</button>
            <button type="button" class="chip" data-range="12" aria-pressed="true">Ultimi 12 mesi</button>
          </div>
          <div class="tiles" id="dash-tiles"></div>
          <div class="viz-row">
            <figure class="viz wide">
              <figcaption><strong>Fatturato mensile</strong><span>Migliaia di euro, IVA esclusa</span></figcaption>
              <div class="legend"><span><i class="lk s1"></i>Anno in corso</span><span><i class="lk s0"></i>Anno precedente</span></div>
              <div class="chart" id="dash-line"></div>
              <details class="tview"><summary>Mostra i dati in tabella</summary><div id="dash-line-t"></div></details>
            </figure>
            <figure class="viz">
              <figcaption><strong>Ordini per categoria</strong><span>Numero di ordini evasi nel periodo</span></figcaption>
              <div class="chart" id="dash-bars"></div>
              <details class="tview"><summary>Mostra i dati in tabella</summary><div id="dash-bars-t"></div></details>
            </figure>
          </div>""")

STOCK = app_frame("Magazzino / Scorte", """
          <div class="tiles three" id="stock-tiles"></div>
          <div class="filters" role="group" aria-label="Filtra gli articoli">
            <button type="button" class="chip" data-st="all" aria-pressed="true">Tutti</button>
            <button type="button" class="chip" data-st="low">Sotto soglia</button>
            <button type="button" class="chip" data-st="warn">In esaurimento</button>
            <label class="search"><span class="sr">Cerca un articolo</span><input type="search" id="stock-q" placeholder="Cerca per codice o nome" autocomplete="off"></label>
          </div>
          <div class="tbl-wrap"><table class="tbl" id="stock-table">
            <thead><tr><th scope="col">Codice</th><th scope="col">Articolo</th><th scope="col">Giacenza</th><th scope="col" class="num">Riordino</th><th scope="col">Stato</th></tr></thead>
            <tbody></tbody>
          </table></div>
          <p class="empty" id="stock-empty" hidden>Nessun articolo corrisponde alla ricerca.</p>""")

PROD = app_frame("Produzione / Carico dei reparti", """
          <div class="viz-row">
            <figure class="viz wide">
              <figcaption><strong>Ore lavorate per reparto</strong><span>Ultime otto settimane</span></figcaption>
              <div class="legend"><span><i class="sw s1"></i>Taglio</span><span><i class="sw s2"></i>Assemblaggio</span><span><i class="sw s3"></i>Collaudo</span></div>
              <div class="chart" id="prod-cols"></div>
              <details class="tview"><summary>Mostra i dati in tabella</summary><div id="prod-cols-t"></div></details>
            </figure>
            <figure class="viz">
              <figcaption><strong>Avanzamento commesse</strong><span>Percentuale completata e consegna prevista</span></figcaption>
              <ul class="jobs" id="prod-jobs"></ul>
            </figure>
          </div>""")

PHONE = app_frame("Consegne / Giro di oggi", """
          <div class="ph-head"><span class="ph-k">Giro di oggi</span><strong id="ph-count"></strong><div class="meter"><i id="ph-meter"></i></div></div>
          <div class="ph-next">
            <span class="ph-k">Prossima consegna</span>
            <h3 id="ph-name"></h3>
            <p id="ph-addr"></p>
            <ul class="ph-items" id="ph-items"></ul>
          </div>
          <button type="button" class="ph-go" id="ph-go">Consegna completata</button>
          <button type="button" class="ph-alt" id="ph-reset">Ricomincia il giro</button>
          <ul class="ph-list" id="ph-list" aria-label="Consegne successive"></ul>""", kind="phone")

SCREENS = "\n\n  ".join([
    screen("Cruscotto", "Esempi di schermate", "Il cruscotto della direzione",
           "Una sola schermata per capire come sta andando l'azienda. Il periodo si sceglie una volta e aggiorna tutti i numeri e i grafici insieme.",
           ["I quattro valori principali in evidenza, con il confronto rispetto al periodo precedente", "L'anno in corso in viola, l'anno precedente in grigio per confrontarli a colpo d'occhio", "Passando sul grafico si leggono i valori di ogni mese, e ogni grafico ha la sua tabella"], DASH),
    screen("Magazzino", "Esempi di schermate", "Le scorte da riordinare",
           "Chi gestisce il magazzino vede subito quali articoli stanno finendo e quanto riordinare. Lo stato è indicato con colore, simbolo e testo, così è leggibile da tutti.",
           ["La barra mostra la giacenza e il segno verticale la soglia minima", "I filtri e la ricerca restringono l'elenco senza cambiare pagina", "Il riordino suggerito è calcolato sulla scorta massima dell'articolo"], STOCK, flip=True),
    screen("Produzione", "Esempi di schermate", "Il carico dei reparti",
           "Il responsabile di produzione confronta le ore lavorate settimana per settimana e controlla l'avanzamento delle commesse aperte.",
           ["Le colonne sommano le ore dei tre reparti, con il totale in cima", "Le commesse a rischio o in ritardo sono segnalate accanto alla data di consegna", "Il calo di agosto si vede senza bisogno di leggere i numeri"], PROD),
    screen("Consegne", "Esempi di schermate", "Il giro consegne sul telefono",
           "L'autista vede una consegna alla volta, con indirizzo e merce da scaricare. Un solo pulsante grande conferma la consegna e passa alla successiva.",
           ["Pulsanti grandi, utilizzabili anche con i guanti", "L'avanzamento del giro sempre visibile in alto", "Provate a premere Consegna completata"], PHONE, flip=True),
])

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
        <p class="lead">Progettiamo e sviluppiamo gestionali partendo da come lavora la vostra azienda. Prima analizziamo il processo, poi costruiamo il software che lo segue, dall'ordine alla fattura.</p>
        <div class="actions">
          <a class="btn" href="contattaci.html"><span>Prenota una chiacchierata</span></a>
          <a class="btn ghost" href="metodo.html"><span>Come lavoriamo</span></a>
        </div>
        <div class="scroll-cue"><i aria-hidden="true"></i>Scorri per continuare</div>
      </div>
    </div>
  </section>

  {statement("Il nostro approccio",
             "Molti gestionali chiedono alle persone di adattarsi al software. Noi partiamo dal lavoro che si svolge ogni giorno in ufficio, in magazzino e in produzione.",
             "persone,lavoro",
             "Un software costruito sul processo reale viene adottato più facilmente e riduce i passaggi manuali, come ricopiare gli stessi dati tra fogli di calcolo e programmi diversi.",
             "Approccio")}

  {hscroll("Come lavoriamo", "Quattro fasi, sempre nello stesso ordine", ("metodo.html", "Il metodo nel dettaglio"), phase_panels(), "Come lavoriamo")}

  {section("Servizi", "Servizi", "Cosa facciamo",
           "Lavoriamo con piccole e medie imprese che hanno processi specifici e hanno bisogno di un software che li gestisca in modo completo.",
           HOME_SERVICES)}

  {band("Primo incontro", "Il primo incontro è una chiacchierata", CHAT_TEXT)}

  {principles()}"""

METODO = f"""  {page_hero("Come lavoriamo", ["Un metodo in <em>quattro fasi</em>"], "Ogni progetto parte dall'analisi del lavoro reale e arriva a un software che le persone usano senza difficoltà. Le fasi si susseguono sempre nello stesso ordine e ciascuna produce un risultato che potete verificare.", 2)}

  {statement("Perché un metodo",
             "Un gestionale funziona quando rispecchia il modo in cui l'azienda lavora davvero. Per questo ogni progetto segue le stesse fasi, dall'osservazione del lavoro alle schermate finali.",
             "lavora,fasi",
             "Seguire sempre lo stesso ordine permette di concordare tempi e costi fase per fase e di verificare i risultati prima di andare avanti.",
             "Perché un metodo")}

  <section data-name="Le fasi">
    <div class="wrap">
      <div class="sec-head" data-enter><span class="eyebrow">Le fasi</span><h2>Dall'analisi all'interfaccia</h2><p>Per ogni fase trovate le attività che svolgiamo e i risultati che vi consegniamo.</p></div>
      {legs_detailed()}
    </div>
  </section>

  <section class="screens-intro" data-name="Esempi">
    <div class="wrap">
      <div class="sec-head centered" data-enter><span class="eyebrow">Fase 4 in pratica</span><h2>Come si vedono i dati</h2><p>Alcune schermate di esempio di un gestionale Merkorn, nello stesso stile di questo sito. Sono interattive e usano dati inventati, per mostrare come ogni schermata risponde a una domanda precisa di chi la usa.</p></div>
    </div>
  </section>

  {SCREENS}

  {band("Primo incontro", "Prima delle fasi c'è una chiacchierata", CHAT_TEXT)}

  {principles()}

  {section("Coinvolgimento", "Coinvolgimento", "Chi partecipa al progetto",
           "Un gestionale funziona bene quando chi lo usa ha contribuito a definirlo. Per questo coinvolgiamo figure diverse in momenti diversi.",
           cards([("Direzione", "Titolare e responsabili", "Definiscono obiettivi e priorità all'inizio del progetto e approvano ogni rilascio."),
                  ("Ufficio", "Amministrazione e commerciale", "Ci mostrano documenti, procedure e passaggi con clienti e fornitori."),
                  ("Reparto", "Magazzino, produzione e consegne", "Provano le schermate nel luogo in cui verranno usate e ci segnalano cosa migliorare.")], "three"))}"""

SERVIZI = f"""  {page_hero("Servizi", ["Software su misura per il <em>vostro processo</em>"], "Sviluppiamo gestionali, applicazioni per il lavoro in reparto e strumenti di analisi per piccole e medie imprese. Ogni servizio parte dallo stesso principio: il software si adatta al modo in cui lavora l'azienda.", 3)}

  {hscroll("Cosa facciamo", "Quattro servizi collegati tra loro", None, service_panels(), "Cosa facciamo")}

  {statement("Un unico progetto",
             "I servizi si possono richiedere separatamente, ma danno il risultato migliore quando fanno parte dello stesso progetto, seguito dalle stesse persone dall'analisi all'assistenza.",
             "progetto,persone",
             "Chi analizza il processo è anche chi progetta le schermate e segue il software dopo il rilascio. In questo modo nessuna informazione si perde tra un passaggio e l'altro.",
             "Un unico progetto")}

  {section("Per chi lavoriamo", "Per chi lavoriamo", "Aziende con processi specifici",
           "Lavoriamo soprattutto con imprese che hanno superato i fogli di calcolo ma non trovano un software pronto adatto al loro modo di lavorare.",
           cards([("Produzione", "Aziende manifatturiere", "Commesse, distinte, avanzamento della produzione e controlli di qualità."),
                  ("Distribuzione", "Commercio e logistica", "Ordini, magazzino su più depositi, documenti di trasporto e consegne."),
                  ("Servizi", "Squadre sul territorio", "Interventi programmati, rapportini digitali e comunicazione con l'ufficio.")], "three"))}

  {prose("Integrazioni", "Integrazioni", "Collegato ai software che usate già",
         ["Il gestionale non sostituisce per forza tutto quello che avete. Quando serve lo colleghiamo ai programmi già in uso in azienda, per esempio il software di contabilità o quello per la fatturazione elettronica, in modo che i dati vengano inseriti una sola volta.",
          "Durante l'analisi verifichiamo quali collegamenti sono possibili con i programmi che utilizzate e quali dati conviene condividere tra un sistema e l'altro."])}

  {band("Primo incontro", "Parliamo del servizio che vi serve", CHAT_TEXT)}"""

CHI = f"""  {page_hero("Chi siamo", ["Una software house che parte dalla <em>UX</em>"], "Merkorn sviluppa software gestionale su misura per le piccole e medie imprese italiane. Lavoriamo dalla Puglia con aziende del Mezzogiorno e del resto d'Italia.", 4)}

  {statement("Missione",
             "Vogliamo portare il digitale nelle piccole e medie imprese partendo dalle persone che ci lavorano e dal modo in cui lavorano ogni giorno.",
             "persone,digitale",
             "La digitalizzazione di un'azienda riesce quando il software rispetta il suo processo. Per questo ogni progetto parte dall'osservazione del lavoro quotidiano e solo dopo passa allo sviluppo.",
             "Missione")}

  {prose("UX design first", "UX design first", "Prima si progetta l'uso, poi si scrive il codice",
         ["La progettazione dell'esperienza d'uso, in inglese UX design, stabilisce come una persona svolge un'attività con il software. Per noi è il primo passo di ogni progetto, prima della scelta delle tecnologie.",
          "Disegniamo le schermate insieme a chi le userà, le proviamo nei luoghi di lavoro reali e le correggiamo prima di svilupparle. Il risultato è un software che richiede poca formazione e riduce gli errori."])}

  {prose("Come costruiamo", "Come costruiamo", "Fondamenta riusabili, superficie su misura",
         ["Il nostro marchio è formato da cinque blocchi che compongono una piramide. Rappresenta il modo in cui costruiamo il software: una base di moduli collaudati, componenti che si montano sopra e, in cima, le schermate progettate per la singola azienda.",
          "Questa struttura permette di offrire software su misura con tempi e costi sostenibili anche per le piccole imprese."])}

  {section("Valori", "Come lavoriamo con i clienti", "Tre impegni che manteniamo", None,
           cards([("Concretezza", "Esempi reali, non concetti", "Parliamo di ordini, documenti e reparti. Ogni proposta descrive cosa cambierà nel lavoro di tutti i giorni."),
                  ("Chiarezza", "Tempi e costi definiti", "Ogni fase ha obiettivi, durata e costo concordati prima di iniziare."),
                  ("Continuità", "Lo stesso team nel tempo", "Chi ha sviluppato il software lo segue anche dopo il rilascio.")], "three"))}

  {band("Primo incontro", "Conosciamoci con una chiacchierata", CHAT_TEXT)}"""

CONTATTI = contact_form(
    heading="Contattaci",
    intro="Compilate il modulo per prenotare una prima chiacchierata o per qualsiasi domanda sui nostri servizi. La richiesta arriva direttamente al nostro indirizzo email e vi rispondiamo personalmente.",
    level="h1",
).replace('class="contact"', 'class="contact page-contact"', 1)

PRIVACY = f"""  {page_hero("Privacy", ["Informativa sul trattamento dei dati"], "Questa informativa descrive come vengono trattati i dati inviati tramite il modulo di contatto del sito, ai sensi del Regolamento UE 2016/679.", 5)}

  <section data-name="Informativa">
    <div class="wrap doc">
      <div><h2>Titolare del trattamento</h2><p>Merkorn, <span class="todo">ragione sociale, partita IVA e sede legale da completare</span>. Per qualsiasi richiesta sul trattamento dei dati potete scrivere a {EMAIL}.</p></div>
      <div><h2>Dati raccolti</h2><p>Tramite il modulo di contatto raccogliamo nome e cognome, indirizzo email, e facoltativamente azienda, numero di telefono e il testo del messaggio.</p></div>
      <div><h2>Finalità e base giuridica</h2><p>I dati vengono usati solo per rispondere alla richiesta e, se lo desiderate, per organizzare un incontro. La base giuridica è il consenso espresso con l'invio del modulo e l'esecuzione di misure precontrattuali richieste dall'interessato.</p></div>
      <div><h2>Modalità del trattamento</h2><p>Il modulo invia i dati al nostro indirizzo email tramite il servizio FormSubmit, che agisce come fornitore tecnico. I messaggi vengono conservati nella casella di posta aziendale.</p></div>
      <div><h2>Conservazione</h2><p>I dati vengono conservati per il tempo necessario a gestire la richiesta e comunque non oltre <span class="todo">periodo da definire</span>, salvo che nasca un rapporto contrattuale.</p></div>
      <div><h2>Diritti dell'interessato</h2><p>Potete chiedere in qualsiasi momento l'accesso, la rettifica o la cancellazione dei vostri dati, la limitazione del trattamento e la revoca del consenso scrivendo a {EMAIL}. Potete inoltre presentare reclamo al Garante per la protezione dei dati personali.</p></div>
    </div>
  </section>"""

PAGES = [
    ("index.html", "Merkorn", "Merkorn sviluppa software gestionale su misura per le piccole e medie imprese italiane, partendo dall'analisi del processo aziendale.", 0.0, HOME, True),
    ("metodo.html", "Come lavoriamo", "Il metodo Merkorn in quattro fasi: analisi del processo, fondamenta riusabili, componenti su misura e interfaccia, con esempi di schermate.", 1.3, METODO, True, ("assets/schermate.js",)),
    ("servizi.html", "Servizi", "Gestionali su misura, analisi dei processi, app per reparto e consegne, assistenza ed evoluzione del software.", 2.6, SERVIZI, True),
    ("chi-siamo.html", "Chi siamo", "Merkorn è una software house pugliese che sviluppa gestionali su misura per le PMI partendo dalla progettazione dell'esperienza d'uso.", 3.9, CHI, True),
    ("contattaci.html", "Contattaci", "Contattate Merkorn per prenotare una prima chiacchierata o chiedere informazioni sui servizi di sviluppo software gestionale.", 5.2, CONTATTI, False),
    ("privacy.html", "Privacy", "Informativa sul trattamento dei dati personali raccolti tramite il modulo di contatto del sito Merkorn.", 6.5, PRIVACY, True),
]

if __name__ == "__main__":
    for path, title, desc, seed, body, form, *extra in PAGES:
        (ROOT / path).write_text(page(path, title, desc, seed, body, form, *extra), encoding="utf-8")
        print("scritto", path)
