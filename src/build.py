"""Genera le pagine HTML del sito nella cartella principale.

Uso:  python3 src/build.py
Header, footer e form di contatto stanno in partials.py e sono uguali su ogni pagina.
"""
from pathlib import Path
from partials import page, contact_form, EMAIL

ROOT = Path(__file__).resolve().parent.parent

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

HERO_MARK = """<div class="constellation" aria-hidden="true">
          <svg viewBox="0 0 100 66" preserveAspectRatio="none">
            <line x1="10" y1="56" x2="30" y2="33"/><line x1="30" y1="33" x2="50" y2="10"/><line x1="50" y1="10" x2="70" y2="33"/><line x1="70" y1="33" x2="90" y2="56"/><line x1="10" y1="56" x2="90" y2="56"/>
          </svg>
          <i class="s" style="left:50%;top:15%;--d:4"></i><i class="s" style="left:30%;top:50%;--d:2"></i><i class="s" style="left:70%;top:50%;--d:3"></i><i class="s" style="left:10%;top:85%;--d:0"></i><i class="s" style="left:90%;top:85%;--d:1"></i>
        </div>"""


def page_hero(eyebrow, lines, lead, lit):
    h = "".join(f'<span class="ln"><span style="--i:{i}">{l}</span></span>' for i, l in enumerate(lines))
    mini = "".join(('<i class="on"></i>' if k < lit else "<i></i>") for k in range(5))
    return f"""<section class="page-hero" data-name="{eyebrow}">
    <div class="wrap">
      <span class="eyebrow">{eyebrow}</span>
      <h1>{h}</h1>
      <p class="lead">{lead}</p>
      <div class="mini" aria-hidden="true">{mini}</div>
    </div>
  </section>"""


def legs(detailed):
    out = []
    for i, (k, h, p, doing, get) in enumerate(PHASES, 1):
        extra = ""
        if detailed:
            d = "".join(f"<li>{x}</li>" for x in doing)
            g = "".join(f"<li>{x}</li>" for x in get)
            extra = f'<div class="split"><div><b>Cosa facciamo</b><ul>{d}</ul></div><div><b>Cosa ricevete</b><ul>{g}</ul></div></div>'
        out.append(f'<article class="leg rise"><span class="dot">{i}</span><div class="body"><span class="k">{k}</span><h3>{h}</h3><p>{p}</p>{extra}</div></article>')
    return "\n        ".join(out)


def rules():
    return "\n        ".join(f'<li class="rise"><div><strong>{a}</strong><span>{b}</span></div></li>' for a, b in PRINCIPLES)


def service_cards(detailed, link=False):
    out = []
    for k, h, p, tags in SERVICES:
        t = ("<ul>" + "".join(f"<li>{x}</li>" for x in tags) + "</ul>") if detailed else ""
        tag = "a" if link else "article"
        href = ' href="servizi.html"' if link else ""
        out.append(f'<{tag} class="card rise"{href}><span class="ico" aria-hidden="true"><i></i><i></i><i></i></span><span class="kicker">{k}</span><h3>{h}</h3><p>{p}</p>{t}</{tag}>')
    return "\n        ".join(out)


# ---------------------------------------------------------------- pages

HOME = f"""  <section class="hero" data-name="Inizio">
    <div class="wrap">
      <div class="meta"><span class="eyebrow">Software house per le PMI italiane</span><span class="eyebrow">Puglia</span></div>
      <div class="grid">
        <div>
          <h1>
            <span class="ln"><span style="--i:0">Software gestionale</span></span>
            <span class="ln"><span style="--i:1"><em>su misura</em></span></span>
            <span class="ln"><span style="--i:2">per le PMI</span></span>
          </h1>
          <p class="lead">Progettiamo e sviluppiamo gestionali partendo da come lavora la vostra azienda. Prima analizziamo il processo, poi costruiamo il software che lo segue, dall'ordine alla fattura.</p>
          <div class="actions">
            <a class="btn" href="contattaci.html"><span>Richiedi un'analisi</span></a>
            <a class="btn ghost" href="metodo.html"><span>Come lavoriamo</span></a>
          </div>
        </div>
        {HERO_MARK}
      </div>
      <div class="scroll-cue"><i aria-hidden="true"></i>Scorri per continuare</div>
    </div>
  </section>

  <section class="statement" data-name="Approccio">
    <div class="wrap">
      <span class="eyebrow">Il nostro approccio</span>
      <p data-hl="persone,lavoro">Molti gestionali chiedono alle persone di adattarsi al software. Noi partiamo dal lavoro che si svolge ogni giorno in ufficio, in magazzino e in produzione.</p>
      <small>Un software costruito sul processo reale viene adottato più facilmente e riduce i passaggi manuali, come ricopiare gli stessi dati tra fogli di calcolo e programmi diversi.</small>
    </div>
  </section>

  <section data-name="Come lavoriamo">
    <div class="wrap">
      <div class="sec-head"><span class="eyebrow">Come lavoriamo</span><h2>Quattro fasi, sempre nello stesso ordine</h2></div>
      <div class="legs">
        {legs(False)}
      </div>
      <a class="more-link" href="metodo.html">Il metodo nel dettaglio <span aria-hidden="true">→</span></a>
    </div>
  </section>

  <section data-name="Servizi">
    <div class="wrap">
      <div class="sec-head"><span class="eyebrow">Servizi</span><h2>Cosa facciamo</h2><p>Lavoriamo con piccole e medie imprese che hanno processi specifici e hanno bisogno di un software che li gestisca in modo completo.</p></div>
      <div class="cards">
        {service_cards(False, link=True)}
      </div>
      <a class="more-link" href="servizi.html">Tutti i servizi <span aria-hidden="true">→</span></a>
    </div>
  </section>

  <section data-name="Principi">
    <div class="wrap">
      <div class="sec-head"><span class="eyebrow">Principi di progettazione</span><h2>Come progettiamo le interfacce</h2><p>La progettazione dell'esperienza d'uso viene prima dello sviluppo. Queste sono le regole che applichiamo a ogni progetto.</p></div>
      <ol class="rules">
        {rules()}
      </ol>
    </div>
  </section>"""

METODO = f"""  {page_hero("Come lavoriamo", ["Un metodo in <em>quattro fasi</em>"], "Ogni progetto parte dall'analisi del lavoro reale e arriva a un software che le persone usano senza difficoltà. Le fasi si susseguono sempre nello stesso ordine e ciascuna produce un risultato che potete verificare.", 2)}

  <section data-name="Le fasi">
    <div class="wrap">
      <div class="sec-head"><span class="eyebrow">Le fasi</span><h2>Dall'analisi all'interfaccia</h2></div>
      <div class="legs">
        {legs(True)}
      </div>
    </div>
  </section>

  <section data-name="Principi">
    <div class="wrap">
      <div class="sec-head"><span class="eyebrow">Principi di progettazione</span><h2>Come progettiamo le interfacce</h2><p>La progettazione dell'esperienza d'uso viene prima dello sviluppo. Queste sono le regole che applichiamo a ogni progetto.</p></div>
      <ol class="rules">
        {rules()}
      </ol>
    </div>
  </section>

  <section data-name="Coinvolgimento">
    <div class="wrap">
      <div class="sec-head"><span class="eyebrow">Coinvolgimento</span><h2>Chi partecipa al progetto</h2><p>Un gestionale funziona bene quando chi lo usa ha contribuito a definirlo. Per questo coinvolgiamo figure diverse in momenti diversi.</p></div>
      <div class="cards three">
        <article class="card rise"><span class="ico" aria-hidden="true"><i></i><i></i><i></i></span><span class="kicker">Direzione</span><h3>Titolare e responsabili</h3><p>Definiscono obiettivi e priorità all'inizio del progetto e approvano ogni rilascio.</p></article>
        <article class="card rise"><span class="ico" aria-hidden="true"><i></i><i></i><i></i></span><span class="kicker">Ufficio</span><h3>Amministrazione e commerciale</h3><p>Ci mostrano documenti, procedure e passaggi con clienti e fornitori.</p></article>
        <article class="card rise"><span class="ico" aria-hidden="true"><i></i><i></i><i></i></span><span class="kicker">Reparto</span><h3>Magazzino, produzione e consegne</h3><p>Provano le schermate nel luogo in cui verranno usate e ci segnalano cosa migliorare.</p></article>
      </div>
    </div>
  </section>"""

SERVIZI = f"""  {page_hero("Servizi", ["Software su misura per il <em>vostro processo</em>"], "Sviluppiamo gestionali, applicazioni per il lavoro in reparto e strumenti di analisi per piccole e medie imprese. Ogni servizio parte dallo stesso principio: il software si adatta al modo in cui lavora l'azienda.", 3)}

  <section data-name="Cosa facciamo">
    <div class="wrap">
      <div class="sec-head"><span class="eyebrow">Cosa facciamo</span><h2>Quattro servizi collegati tra loro</h2><p>Si possono richiedere separatamente, ma danno il risultato migliore quando fanno parte dello stesso progetto.</p></div>
      <div class="cards">
        {service_cards(True)}
      </div>
    </div>
  </section>

  <section data-name="Per chi lavoriamo">
    <div class="wrap">
      <div class="sec-head"><span class="eyebrow">Per chi lavoriamo</span><h2>Aziende con processi specifici</h2><p>Lavoriamo soprattutto con imprese che hanno superato i fogli di calcolo ma non trovano un software pronto adatto al loro modo di lavorare.</p></div>
      <div class="cards three">
        <article class="card rise"><span class="ico" aria-hidden="true"><i></i><i></i><i></i></span><span class="kicker">Produzione</span><h3>Aziende manifatturiere</h3><p>Commesse, distinte, avanzamento della produzione e controlli di qualità.</p></article>
        <article class="card rise"><span class="ico" aria-hidden="true"><i></i><i></i><i></i></span><span class="kicker">Distribuzione</span><h3>Commercio e logistica</h3><p>Ordini, magazzino su più depositi, documenti di trasporto e consegne.</p></article>
        <article class="card rise"><span class="ico" aria-hidden="true"><i></i><i></i><i></i></span><span class="kicker">Servizi</span><h3>Squadre sul territorio</h3><p>Interventi programmati, rapportini digitali e comunicazione con l'ufficio.</p></article>
      </div>
    </div>
  </section>

  <section data-name="Integrazioni">
    <div class="wrap prose">
      <div><span class="eyebrow">Integrazioni</span><h2 style="margin-top:22px">Collegato ai software che usate già</h2></div>
      <div class="txt">
        <p>Il gestionale non sostituisce per forza tutto quello che avete. Quando serve lo colleghiamo ai programmi già in uso in azienda, per esempio il software di contabilità o quello per la fatturazione elettronica, in modo che i dati vengano inseriti una sola volta.</p>
        <p>Durante l'analisi verifichiamo quali collegamenti sono possibili con i programmi che utilizzate e quali dati conviene condividere tra un sistema e l'altro.</p>
      </div>
    </div>
  </section>"""

CHI = f"""  {page_hero("Chi siamo", ["Una software house che parte dalla <em>UX</em>"], "Merkorn sviluppa software gestionale su misura per le piccole e medie imprese italiane. Lavoriamo dalla Puglia con aziende del Mezzogiorno e del resto d'Italia.", 4)}

  <section data-name="Missione">
    <div class="wrap prose">
      <div><span class="eyebrow">Missione</span><h2 style="margin-top:22px">Portare il digitale nelle PMI partendo dalle persone</h2></div>
      <div class="txt">
        <p>La digitalizzazione di una piccola o media impresa riesce quando il software rispetta il modo in cui l'azienda lavora. Per questo ogni nostro progetto parte dall'osservazione del lavoro quotidiano e solo dopo passa allo sviluppo.</p>
        <p>Costruiamo strumenti su misura sopra fondamenta riusabili. In questo modo ogni azienda ottiene un software adatto al proprio processo, con tempi e costi sostenibili.</p>
      </div>
    </div>
  </section>

  <section data-name="UX design first">
    <div class="wrap prose">
      <div><span class="eyebrow">UX design first</span><h2 style="margin-top:22px">Prima si progetta l'uso, poi si scrive il codice</h2></div>
      <div class="txt">
        <p>La progettazione dell'esperienza d'uso, in inglese UX design, stabilisce come una persona svolge un'attività con il software. Per noi è il primo passo di ogni progetto, prima della scelta delle tecnologie.</p>
        <p>Disegniamo le schermate insieme a chi le userà, le proviamo nei luoghi di lavoro reali e le correggiamo prima di svilupparle. Il risultato è un software che richiede poca formazione e riduce gli errori.</p>
      </div>
    </div>
  </section>

  <section data-name="Valori">
    <div class="wrap">
      <div class="sec-head"><span class="eyebrow">Come lavoriamo con i clienti</span><h2>Tre impegni che manteniamo</h2></div>
      <div class="cards three">
        <article class="card rise"><span class="ico" aria-hidden="true"><i></i><i></i><i></i></span><span class="kicker">Concretezza</span><h3>Esempi reali, non concetti</h3><p>Parliamo di ordini, documenti e reparti. Ogni proposta descrive cosa cambierà nel lavoro di tutti i giorni.</p></article>
        <article class="card rise"><span class="ico" aria-hidden="true"><i></i><i></i><i></i></span><span class="kicker">Chiarezza</span><h3>Tempi e costi definiti</h3><p>Ogni fase ha obiettivi, durata e costo concordati prima di iniziare.</p></article>
        <article class="card rise"><span class="ico" aria-hidden="true"><i></i><i></i><i></i></span><span class="kicker">Continuità</span><h3>Lo stesso team nel tempo</h3><p>Chi ha sviluppato il software lo segue anche dopo il rilascio.</p></article>
      </div>
    </div>
  </section>"""

CONTATTI = contact_form(
    heading="Contattaci",
    intro="Compilate il modulo per richiedere un primo incontro o per qualsiasi domanda sui nostri servizi. La richiesta arriva direttamente al nostro indirizzo email e vi rispondiamo personalmente.",
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
    ("metodo.html", "Come lavoriamo", "Il metodo Merkorn in quattro fasi: analisi del processo, fondamenta riusabili, componenti su misura e interfaccia.", 1.3, METODO, True),
    ("servizi.html", "Servizi", "Gestionali su misura, analisi dei processi, app per reparto e consegne, assistenza ed evoluzione del software.", 2.6, SERVIZI, True),
    ("chi-siamo.html", "Chi siamo", "Merkorn è una software house pugliese che sviluppa gestionali su misura per le PMI partendo dalla progettazione dell'esperienza d'uso.", 3.9, CHI, True),
    ("contattaci.html", "Contattaci", "Contattate Merkorn per richiedere un primo incontro o informazioni sui servizi di sviluppo software gestionale.", 5.2, CONTATTI, False),
    ("privacy.html", "Privacy", "Informativa sul trattamento dei dati personali raccolti tramite il modulo di contatto del sito Merkorn.", 6.5, PRIVACY, True),
]

for path, title, desc, seed, body, form in PAGES:
    (ROOT / path).write_text(page(path, title, desc, seed, body, form), encoding="utf-8")
    print("scritto", path)
