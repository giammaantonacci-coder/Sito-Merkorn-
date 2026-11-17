"""Merkorn, contenuti delle pagine.

Genera index, servizi, metodo, chi-siamo, contattaci, privacy, cookie, 404 e sitemap.xml:
    python3 src/build.py
Lo stile è in assets/sito.css, i blocchi animati in assets/goo.js, menu e modulo in assets/sito.js.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from partials import ROOT, EMAIL, MARK, page, contact_form  # noqa: E402
from legal import PRIVACY_DOC, COOKIE_DOC  # noqa: E402

# ---------------------------------------------------------------- contenuti condivisi

SERVICES = [
    ("Gestionale su misura",
     "I programmi pronti ti chiedono di cambiare il tuo modo di lavorare, e le differenze le colmano le persone, a mano. Noi costruiamo il gestionale sui tuoi processi: ordini, magazzino, produzione e commesse in un unico sistema.",
     ["Ordini e offerte", "Magazzino", "Produzione", "Commesse", "Documenti di trasporto"]),
    ("Analisi dei processi aziendali",
     "Prima di scrivere codice seguiamo il lavoro in azienda e troviamo dove si ferma. Ti consegniamo la mappa dei processi, con i punti critici e da dove conviene partire.",
     ["Mappa del processo", "Punti critici", "Priorità di intervento"]),
    ("UX e design delle schermate",
     "Un software scomodo viene aggirato con fogli Excel e appunti. Disegniamo le schermate prima del codice e le mettiamo alla prova con il tuo team, quando cambiarle costa ancora poco.",
     ["Prototipi cliccabili", "Test con il tuo team", "Computer, tablet e telefono"]),
    ("App per magazzino e consegne",
     "Chi lavora in magazzino o fuori sede spesso scrive su carta e ricopia in ufficio. Con l'app i dati arrivano subito, senza passaggi in mezzo.",
     ["Carico e scarico merce", "Consegne", "Firma del cliente"]),
    ("Assistenza ed evoluzione del software",
     "Il progetto non finisce al rilascio. Lo stesso team che l'ha costruito segue il gestionale, risolve i problemi e aggiunge funzioni quando l'azienda cambia.",
     ["Assistenza agli utenti", "Aggiornamenti", "Nuove funzioni"]),
]
# short versions for the home, each with its own moving pattern
HOME_SERVICES = [
    ("Gestionale su misura", "Costruito sui tuoi processi, non preso da un catalogo.", "mosaic"),
    ("Analisi dei processi", "Troviamo dove si ferma il lavoro e cosa conviene sistemare prima.", "rings"),
    ("UX design", "Schermate provate con chi le userà, prima di scrivere il codice.", "diag"),
    ("Assistenza ed evoluzione", "Il progetto non finisce al rilascio: lo stesso team lo fa crescere.", "wave"),
]
# the method: title, text, pattern shown by the sticky grid, result
PHASES = [
    ("Capiamo come lavori", "Seguiamo il lavoro dove succede, dal magazzino all'ufficio, e troviamo dove si perde tempo.", "mosaic", "Priorità chiare fin da subito"),
    ("Partiamo da basi solide", "Moduli già collaudati per partire veloci e investire dove serve davvero.", "drops", "La base del gestionale con i tuoi dati"),
    ("Costruiamo le parti su misura", "Le funzioni specifiche della tua azienda, rilasciate una alla volta.", "wave", "Un passo avanti a ogni rilascio"),
    ("Rendiamo i dati leggibili", "Schermate chiare che mostrano subito quello che conta.", "logo", "Decisioni più rapide, ogni giorno"),
]

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
    ("Si può partire da un solo reparto?", "Sì. Si parte da dove si perde più tempo e il resto si aggiunge dopo."),
    ("Potete importare i dati da Excel o dal vecchio gestionale?", "Sì. Importiamo anagrafiche, articoli e giacenze, dopo averli ripuliti da doppioni ed errori."),
    ("Sviluppate anche app per telefono e tablet?", "Sì, per magazzino, consegne e interventi fuori sede, collegate al gestionale."),
    ("Cosa succede dopo il rilascio?", "Il software lo segue lo stesso team che l'ha costruito, con assistenza e aggiornamenti."),
]
FAQ_METODO = [
    ("Quanto costa un gestionale su misura?", "Dipende da quante aree deve seguire. Dopo l'analisi ricevi un preventivo diviso per fasi, con tempi e costi chiari."),
    ("Quanto tempo serve?", "Lavoriamo per rilasci, quindi le prime parti le usi già durante il progetto. La durata la fissiamo dopo l'analisi."),
    ("Quando conviene rispetto a un programma pronto?", "Quando accanto al gestionale torna fuori il foglio Excel. Se ti basta un programma pronto, te lo diciamo."),
]


def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


SERVICES_LD = [{"@type": "Service", "name": t, "serviceType": t, "description": d, "provider": {"@id": "https://merkorn.com/#org"},
                "areaServed": ["Taranto", "Bari", "Brindisi", "Lecce", "Matera", "Puglia", "Italia"]} for t, d, _ in SERVICES]

# ---------------------------------------------------------------- pezzi di pagina


def grid(pattern, cols, rows, cls="g", cursor=True, extra=""):
    """A block grid animated by assets/goo.js."""
    c = ' data-cursor="1"' if cursor else ""
    return f'<div class="{cls}" data-goo="{pattern}" data-cols="{cols}" data-rows="{rows}"{c}{extra} aria-hidden="true"></div>'


def caption(*items):
    left = "<span>•</span>".join(f"<span>{x}</span>" for x in items[:-1])
    return f'  <div class="caption caps" aria-hidden="true">{left}<i></i><span>{items[-1]}</span></div>'


def sh(n, h, level="h2"):
    return f'<div class="sh"><span class="caps">{n}</span><{level}>{h}</{level}></div>'


def phero(h1, p, pattern, cols=10, rows=4):
    return f"""  <section class="phero">
    <div><h1>{h1}</h1><p>{p}</p></div>
    {grid(pattern, cols, rows)}
  </section>"""


def end(title):
    return f"""  <section class="end">
    <div><h2>{title}<span>.</span></h2><p style="margin-top:24px;color:var(--muted);max-width:36ch">Ci vediamo in azienda, guardiamo insieme come lavorate e ti mostriamo cosa può cambiare.</p><div style="margin-top:26px"><a class="btn" href="contattaci.html">Prenota un appuntamento</a></div></div>
    {grid("drops", 9, 4)}
  </section>"""


def faq(items):
    return '<div class="faq">' + "".join(
        f"<details><summary><span>Domanda {i:02d}</span><h3>{q}</h3></summary><p>{a}</p></details>"
        for i, (q, a) in enumerate(items, 1)) + "</div>"


def method(with_results):
    steps = ""
    for i, (t, d, pat, res) in enumerate(PHASES, 1):
        r = f'<p style="margin-top:18px;color:var(--ink)"><span style="color:var(--accent)">Risultato</span> · {res}</p>' if with_results else ""
        steps += f'<div data-pat="{pat}" data-n="0{i}"><b>Fase 0{i}</b><h3>{t}</h3><p>{d}</p>{r}</div>'
    return f"""<div class="split">
      <div class="sticky"><div class="g" id="stickyGoo" aria-hidden="true"></div><div class="caption caps" aria-hidden="true"><span>Fase</span><span id="patLabel">01</span><i></i><span>Merkorn</span></div></div>
      <div class="steps">{steps}</div>
    </div>"""


# the method grid follows the phase in view, and keeps moving while the page scrolls
METHOD_JS = """<script>
(() => {
  const box = document.getElementById('stickyGoo'); if (!box || !window.Goo) return;
  const g = Goo(box, { cols: 7, rows: 7, pattern: 'mosaic', cursor: true, scroll: true });
  const steps = [...document.querySelectorAll('[data-pat]')], label = document.getElementById('patLabel');
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { g.setPattern(e.target.dataset.pat); steps.forEach(s => s.classList.toggle('on', s === e.target)); if (label) label.textContent = e.target.dataset.n; } }), { rootMargin: '-45% 0px -45% 0px' });
  steps.forEach(s => io.observe(s));
})();
</script>"""

# ---------------------------------------------------------------- case study

# each case: page, name, sector line, hero, client text, facts, problems, process, screens, devices text, teaser, logo
CASES = [
    dict(
        page="case-study-kuelle.html", name="Kuelle Sports Center", slug="kuelle", sector="Centro sportivo · Mottola (TA)",
        hero=("Kuelle Sports Center: <span>campi, partite e saldi</span> in un unico gestionale",
              "Un centro sportivo polifunzionale a Mottola, con due campi da padel coperti, beach volley, tennis e soccer e un campo da calcio a 5/6."),
        teaser="Prenotazioni, partite da completare, saldi dei giocatori e turni in un'unica schermata.",
        client_title="Un centro sportivo che cresce ogni stagione.",
        client=("Kuelle è un centro sportivo polifunzionale a Mottola, in provincia di Taranto.",
                "Ogni giorno passano decine di giocatori tra padel, beach e calcio, con lezioni, tornei e una scuola calcio."),
        facts=[("2", "campi da padel coperti"), ("1", "campo beach per volley, tennis e soccer"), ("1", "campo da calcio a 5/6")],
        problems_title="Cinque cose che rubavano tempo ogni giorno.",
        problems=[
            ("L'andamento dei campi non si vedeva", "Quanto erano pieni i campi, quali fasce restavano vuote e quanto rendeva ogni attività si scopriva solo a fine mese, mettendo insieme appunti diversi."),
            ("Prenotazioni sparse", "Le richieste arrivavano per telefono, in chat e di persona. Tenere un calendario unico per padel, beach e calcio voleva dire ricontrollare tutto più volte al giorno."),
            ("Partite da chiudere, un giocatore alla volta", "Quando a una partita mancava qualcuno, la reception cercava i giocatori uno per uno, senza sapere chi aveva il livello giusto ed era libero."),
            ("Saldi e crediti difficili da seguire", "Conti aperti, quote parziali delle squadre e crediti ricaricati erano su supporti diversi: capire chi doveva saldare, e da quando, richiedeva tempo."),
            ("Turni dei dipendenti", "Reception, maestri, bar e manutenzione: chi era in turno e chi registrava gli incassi non era scritto in un posto solo."),
        ],
        steps=[
            ("Capiamo come lavori", "Siamo stati al centro una giornata intera: dalla reception al bar, abbiamo seguito come nasce una prenotazione, come si chiude una partita e come si incassa."),
            ("Partiamo da basi solide", "Anagrafica dei giocatori, campi, listini e cassa sono partiti dai nostri moduli già collaudati, con i dati del centro importati e ripuliti."),
            ("Costruiamo le parti su misura", "Calendario dei campi, partite da completare con l'invito su WhatsApp e credito dei giocatori sono stati costruiti attorno al modo di lavorare di Kuelle."),
            ("Rendiamo i dati leggibili", "Tre schermate, pensate per chi sta in reception: quello che richiede attenzione si vede subito, in verde e giallo come i colori del centro."),
        ],
        screens=[
            ("Andamento campi", "Tutti i campi della giornata, in un colpo d'occhio",
             "Una riga per campo, dalle 9 alle 23. In verde le partite confermate, in giallo quelle a cui mancano giocatori, in rosso le fasce serali ancora libere. Sotto, l'occupazione media di ogni campo e l'incasso diviso per attività.",
             ["Occupazione e incasso di oggi in alto", "Partite incomplete evidenziate", "Fasce libere da proporre"], (1, 2)),
            ("Partite da chiudere", "Il giocatore giusto, con un messaggio",
             "Per ogni partita incompleta il gestionale propone chi invitare: livello compatibile, libero in quell'orario, abituato a giocare in quella fascia. Il messaggio WhatsApp è già pronto e chi risponde per primo entra in partita.",
             ["Giocatori suggeriti per livello e disponibilità", "Invito su WhatsApp in un tocco", "Risposte e conferme registrate"], (3,)),
            ("Giocatori, saldi e dipendenti", "Chi deve saldare, chi ha credito, chi è in turno",
             "La tabella dei saldi mette in cima chi deve pagare da più tempo, con il sollecito pronto. Le ricariche di credito pagano le partite in automatico e ogni movimento registra chi l'ha fatto. A fianco, i turni del giorno.",
             ["Conti aperti ordinati per anzianità", "Credito ricaricato e scalato a ogni partita", "Turni e movimenti di cassa per dipendente"], (4, 5)),
        ],
        devices=("Dalla reception al telefono, lo stesso gestionale.",
                 "In reception si lavora sul computer; a bordo campo o al bar, chi è in turno controlla i campi, chiude una partita e vede chi deve saldare direttamente dal telefono."),
        note="Nelle schermate nomi, cifre e orari sono dimostrativi: i dati reali dei giocatori restano riservati.",
        pattern="mosaic",
    ),
    dict(
        page="case-study-mongelli.html", name="Autoscuola Centrale Mongelli", slug="mongelli", sector="Autoscuola · Mottola (TA)",
        hero=("Autoscuola Centrale Mongelli: <span>lezioni, esami e allievi</span> sotto controllo",
              "Un'autoscuola a Mottola, in via Boito, che prepara allievi per le patenti AM, A2, B, C e CQC, con lezioni di teoria in aula e guide con due istruttori."),
        teaser="Calendario delle guide, gruppi d'esame da quattro e andamento degli allievi in un'unica schermata.",
        client_title="Una nuova autoscuola, organizzata fin dal primo giorno.",
        client=("L'Autoscuola Centrale Mongelli ha aperto a Mottola, in provincia di Taranto.",
                "Due istruttori seguono le guide di auto, moto e mezzi pesanti, mentre in aula si preparano gli allievi all'esame di teoria."),
        facts=[("5", "tipi di patente, da AM a CQC"), ("2", "istruttori per guide e aula"), ("4", "allievi per ogni gruppo d'esame")],
        problems_title="Quattro cose da tenere sempre in ordine.",
        problems=[
            ("Guide e aula su calendari diversi", "Guide con due istruttori, lezioni di teoria e veicoli da condividere: ogni spostamento andava ricontrollato a mano, e le disdette dell'ultimo momento si perdevano."),
            ("Allievi pronti per l'esame, ma quali?", "Capire chi aveva fatto tutte le guide obbligatorie e chi superava i quiz di prova voleva dire scorrere ogni scheda, una per una."),
            ("Gruppi d'esame da comporre", "Gli esami si fanno in gruppi da quattro, per tipo di patente: riempire ogni sessione, senza lasciare posti vuoti, era un incastro da rifare ogni volta."),
            ("Andamento e scadenze poco visibili", "Quanti iscritti, quanti esami superati e quanti da rifare, e quali fogli rosa stavano per scadere, si sapeva solo mettendo insieme dati sparsi."),
        ],
        steps=[
            ("Capiamo come lavori", "Abbiamo seguito una settimana tipo: dalla segreteria che iscrive un allievo all'istruttore che chiude una guida, fino alla prenotazione dell'esame."),
            ("Partiamo da basi solide", "Anagrafica degli allievi, patenti, veicoli e pagamenti sono partiti dai nostri moduli già collaudati."),
            ("Costruiamo le parti su misura", "Calendario di guide e aula, controllo delle guide obbligatorie e composizione dei gruppi d'esame da quattro sono costruiti sulle regole dell'autoscuola."),
            ("Rendiamo i dati leggibili", "Tre schermate per segreteria e istruttori, nei colori del marchio: nero per Cosimo, rosso per Carmen, rosso per quello che richiede attenzione."),
        ],
        screens=[
            ("Panoramica", "Iscritti, esami superati e da rifare",
             "In alto gli iscritti attivi, gli esami sostenuti, quelli superati e quelli da rifare. Il grafico mostra mese per mese superati e da rifare, a fianco l'esito di teoria e pratica, sotto gli iscritti per patente e le scadenze da controllare.",
             ["Esami superati e da rifare, mese per mese", "Iscritti per tipo di patente", "Fogli rosa e documenti in scadenza"], (4,)),
            ("Calendario lezioni", "Guide e aula nella stessa settimana",
             "Le guide sono colorate per istruttore, le lezioni di teoria e gli esami sono in evidenza. Sotto il calendario le note della settimana, a fianco le ore di ogni istruttore, le lezioni di oggi e le guide disdette da recuperare.",
             ["Un colore per ogni istruttore", "Note della settimana sotto il calendario", "Guide disdette da riprogrammare"], (1,)),
            ("Esami", "Gruppi da quattro, già composti",
             "Gli allievi pronti sono divisi in gruppi da quattro per sessione e per patente. Per la pratica si vedono le guide obbligatorie fatte, per la teoria gli errori al quiz di prova. I posti liberi propongono chi è quasi pronto.",
             ["Guide obbligatorie e quiz di prova per allievo", "Posti liberi con gli allievi da proporre", "Elenco di chi deve rifare l'esame"], (2, 3)),
        ],
        devices=("Dalla segreteria all'auto, lo stesso gestionale.",
                 "In segreteria si lavora sul computer; l'istruttore, dal telefono, vede le guide del giorno, il prossimo esame con il suo gruppo e avvisa gli allievi con un tocco."),
        note="Nelle schermate i nomi degli allievi e le cifre sono dimostrativi: i dati reali restano riservati.",
        pattern="drops",
    ),
]


def case_screens(c):
    out = ""
    for i, (cap, title, text, points, solves) in enumerate(c["screens"], 1):
        pts = "".join(f"<li>{p}</li>" for p in points)
        sv = " e ".join(f"0{n}" for n in solves)
        out += f"""<article class="case-screen">
      <div class="txt"><span class="caps">Schermata 0{i} · {cap}</span><h3>{title}</h3><p>{text}</p><ul>{pts}</ul><span class="solves">Risolve {"il problema" if len(solves) == 1 else "i problemi"} {sv}</span></div>
      <figure class="frame"><img src="assets/case/{c['slug']}-{i}.webp" alt="Gestionale di {c['name']}, schermata {cap.lower()}" width="1800" loading="lazy"></figure>
    </article>"""
    return out


def case_page(c, other):
    n = len(c["problems"])
    return f"""{phero(c['hero'][0], c['hero'][1], c['pattern'])}
{caption('Case study', c['name'], 'Mottola (TA)', 'Gestionale su misura')}
  <div class="back"><a class="u" href="case-study.html">← Tutti i case study</a></div>
  <section class="sec">
    {sh('01 / Il cliente', c['client_title'])}
    <div class="case-client">
      <img src="assets/case/{c['slug']}-logo.png" alt="Logo di {c['name']}" width="160" height="160">
      <div><p class="big">{c['client'][0]} <span>{c['client'][1]}</span></p>
        <ul class="facts">{''.join(f'<li><b>{a}</b>{b}</li>' for a, b in c['facts'])}</ul></div>
    </div>
  </section>
  <section class="sec">
    {sh('02 / I problemi', c['problems_title'])}
    <div class="list">{''.join(f'<div class="item"><span class="n">0{i}</span><div><h3>{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(c['problems'], 1))}</div>
  </section>
  <div class="strip" data-goo="wave" data-cols="28" data-rows="1" data-cursor="1" aria-hidden="true"></div>
  <section class="sec" style="padding-top:clamp(60px,8vw,100px)">
    {sh('03 / Il processo', 'Le quattro fasi del nostro metodo, applicate al progetto.')}
    <div class="cols" style="--c:4">{''.join(f'<div><span class="caps">Fase 0{i}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(c['steps'], 1))}</div>
  </section>
  <section class="sec">
    {sh('04 / La soluzione', 'Tre schermate, costruite sui problemi da risolvere.')}
    <div class="case-screens">{case_screens(c)}</div>
    <div class="case-devices">
      <div class="txt"><span class="caps">Su ogni dispositivo</span><h3>{c['devices'][0]}</h3><p>Le schermate si adattano a computer, tablet e telefono. {c['devices'][1]}</p></div>
      <div class="devices">
        <figure class="frame desk"><img src="assets/case/{c['slug']}-1.webp" alt="Gestionale di {c['name']} da computer" width="1800" loading="lazy"></figure>
        <figure class="phone"><img src="assets/case/{c['slug']}-mobile.webp" alt="Gestionale di {c['name']} da telefono" width="780" loading="lazy"></figure>
      </div>
    </div>
    <p class="case-note">{c['note']}</p>
  </section>
  <section class="sec">
    {sh('Altro case study', other['name'])}
    {case_teaser(other)}
  </section>
{end('Il prossimo è il tuo')}"""


def case_teaser(c, n=None):
    num = f'<span class="caps">Case study {n:02d} · {c["sector"]}</span>' if n else f'<span class="caps">{c["sector"]}</span>'
    return f"""<a class="case-teaser" href="{c['page']}">
      <figure class="frame"><img src="assets/case/{c['slug']}-1.webp" alt="Gestionale di {c['name']}" width="1800" loading="lazy"></figure>
      <div>{num}<h3>{c['name']}</h3><p>{c['teaser']}</p><ul class="mini-probs">{''.join(f'<li>{t}</li>' for t, _ in c['problems'])}</ul><span class="u">Leggi il case study</span></div>
    </a>"""


CASE_HERO = phero('Case study: <span>come lavoriamo</span>, progetto dopo progetto', "Ogni gestionale parte da come lavora davvero un'azienda. Qui raccontiamo due progetti: i problemi da cui siamo partiti, il metodo e le schermate che li risolvono.", 'logo', 5, 3)
CASE_HUB = f"""{CASE_HERO}
{caption('Case study', 'Progetti reali', 'Mottola (TA)', 'Gestionali su misura')}
  <section class="sec">
    {sh('01 / Il nostro approccio', 'Stesso metodo, soluzioni diverse.')}
    <div class="who"><span></span><p class="big">Un centro sportivo e un'autoscuola hanno poco in comune. <span>Eppure il lavoro parte sempre dallo stesso punto: vedere come si lavora ogni giorno, capire dove si perde tempo e costruire solo quello che serve.</span></p></div>
    <div class="cols" style="--c:4">
      <div><span class="caps">Fase 01</span><h3>Capiamo come lavori</h3><p>Passiamo del tempo con chi usa il gestionale: reception, segreteria, istruttori.</p></div>
      <div><span class="caps">Fase 02</span><h3>Partiamo da basi solide</h3><p>Anagrafiche, listini, cassa e calendari partono dai nostri moduli collaudati.</p></div>
      <div><span class="caps">Fase 03</span><h3>Costruiamo su misura</h3><p>Le parti che fanno la differenza seguono le regole di quel lavoro: partite da completare, gruppi d'esame.</p></div>
      <div><span class="caps">Fase 04</span><h3>Rendiamo i dati leggibili</h3><p>Poche schermate, nei colori del cliente, che mostrano subito cosa richiede attenzione.</p></div>
    </div>
  </section>
  <section class="sec">
    {sh('02 / I progetti', 'Due aziende di Mottola, due gestionali su misura.')}
    <div class="case-list">{''.join(case_teaser(c, i) for i, c in enumerate(CASES, 1))}</div>
  </section>
{end('Il prossimo è il tuo')}"""

CASE_PAGES = [case_page(CASES[0], CASES[1]), case_page(CASES[1], CASES[0])]


# ---------------------------------------------------------------- ux design

UX_IMPACT = [
    ("Meno errori", "Campi chiari e controlli al momento giusto: il dato entra corretto la prima volta, invece di essere corretto dopo."),
    ("Operativi prima", "Una schermata che si capisce da sola riduce la formazione. Chi arriva in azienda impara facendo, non leggendo un manuale."),
    ("Più tempo per il lavoro vero", "Meno passaggi per le operazioni di tutti i giorni. Ogni clic risparmiato si ripete decine di volte al giorno, per ogni persona."),
    ("Lo usano davvero tutti", "Un gestionale scomodo viene aggirato con fogli Excel e appunti. Uno comodo viene usato da tutti, ed è l'unico modo per avere dati completi."),
]
UX_COST = [
    ("Doppio lavoro", "Lo stesso dato scritto nel gestionale, poi in un foglio Excel, poi in un messaggio. Ogni copia è un'occasione per sbagliare."),
    ("Telefonate all'assistenza", "Se non è chiaro dove cliccare, qualcuno deve chiedere. Il tempo perso è doppio: di chi chiede e di chi risponde."),
    ("Resistenza al cambiamento", "Quando il nuovo programma è più difficile del vecchio metodo, le persone tornano al vecchio metodo. E l'investimento resta fermo."),
    ("Decisioni su dati incompleti", "Se l'inserimento è faticoso, i dati arrivano in ritardo o non arrivano. I numeri sulla schermata non raccontano più l'azienda."),
]
UX_STEPS = [
    ("Osserviamo sul posto", "Passiamo del tempo con chi userà il gestionale: in ufficio, in magazzino, alla reception. Guardiamo cosa fa davvero, non solo cosa dovrebbe fare."),
    ("Disegniamo i flussi", "Mettiamo in fila le operazioni di ogni giorno e togliamo i passaggi inutili, prima ancora di pensare alle schermate."),
    ("Proviamo un prototipo", "Prima di scrivere il codice, le schermate si possono cliccare. Le provi con il tuo team e cambiarle costa pochi minuti, non settimane."),
    ("Miglioriamo con l'uso", "Dopo il rilascio raccogliamo dubbi e richieste di chi lavora ogni giorno con il gestionale, e lo rendiamo più semplice a ogni versione."),
]
FAQ_UX = [
    ("Cos'è la UX?", "UX sta per user experience, l'esperienza di chi usa un prodotto. Nel software vuol dire progettare schermate e passaggi perché siano facili, veloci e senza errori per chi li usa ogni giorno."),
    ("Che differenza c'è tra UX e UI?", "La UX decide cosa c'è in una schermata e in che ordine si fanno le cose. La UI ne cura l'aspetto: colori, caratteri, icone. Servono entrambe, ma si parte sempre dalla UX."),
    ("La progettazione UX fa aumentare i costi?", "È una parte del progetto, non un extra. Cambiare un prototipo costa molto meno che riscrivere un programma già sviluppato, e un gestionale che si usa bene si ripaga con il tempo risparmiato."),
    ("Serve anche per un gestionale interno?", "Soprattutto lì. Un gestionale si usa ogni giorno, per ore: anche un piccolo attrito, ripetuto per mesi, diventa un costo grande."),
]

def ux_compare():
    return f"""<div class="ux-compare">
      <div><div class="g" data-goo="mosaic" data-cols="7" data-rows="4" data-cursor="1" data-speed="1.6" aria-hidden="true"></div><span class="caps">Senza progettazione</span><h3>Tutto c'è, ma niente si trova.</h3><p>Funzioni sparse, passaggi in più, informazioni importanti nascoste tra quelle che non servono.</p></div>
      <div><div class="g" data-goo="breathe" data-cols="7" data-rows="4" data-cursor="1" data-accent="3,1" aria-hidden="true"></div><span class="caps">Con la UX</span><h3>Ogni cosa al suo posto.</h3><p>Quello che serve è davanti agli occhi, nell'ordine in cui lavori. Il resto non disturba.</p></div>
    </div>"""

def numbered(items):
    return '<div class="list">' + "".join(f'<div class="item"><span class="n">{i:02d}</span><div><h3>{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(items, 1)) + "</div>"

UX = f"""{phero('UX design: il gestionale <span>che si capisce da solo</span>', "Un software può avere tutte le funzioni del mondo. Se è difficile da usare, nessuno le userà. Per questo progettiamo l'esperienza prima del codice.", 'wave')}
{caption('UX design', 'Prototipi', 'Test con chi lo usa', 'Merkorn')}
  <section class="sec">
    {sh('01 / Perché conta', 'Un gestionale vale quanto è facile da usare.')}
    <div class="who"><span></span><div><p class="big">La UX non è una questione estetica. <span>Decide quanto tempo perdono le persone, quanti errori fanno e se il gestionale verrà usato davvero.</span></p></div></div>
    {ux_compare()}
  </section>
  <section class="sec">
    {sh("02 / L'impatto", 'Cosa cambia quando un software è progettato bene.')}
    {numbered(UX_IMPACT)}
  </section>
  <section class="sec">
    {sh('03 / Il costo nascosto', 'Cosa succede quando la UX manca.')}
    {numbered(UX_COST)}
  </section>
  <div class="strip" data-goo="diag" data-cols="28" data-rows="1" data-cursor="1" aria-hidden="true"></div>
  <section class="sec" style="padding-top:clamp(60px,8vw,100px)">
    {sh('04 / Come lavoriamo', 'Si disegna con chi lo userà, si prova prima di costruire.')}
    <div class="cols" style="--c:4">{''.join(f'<div><span class="caps">Passo 0{i}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(UX_STEPS, 1))}</div>
  </section>
  <section class="sec">
    {sh('05 / Nei nostri progetti', 'La UX, vista dentro due gestionali veri.')}
    <div class="list">
      <div class="item"><span class="n">01</span><div><h3>Kuelle Sports Center</h3><p>Chi sta in reception doveva chiudere le partite incomplete cercando i giocatori uno a uno. Oggi il gestionale propone chi invitare e il messaggio WhatsApp parte con un tocco. <a class="u" href="case-study-kuelle.html">Leggi il case study</a></p></div></div>
      <div class="item"><span class="n">02</span><div><h3>Autoscuola Centrale Mongelli</h3><p>Comporre i gruppi d'esame voleva dire incrociare calendari e liste. Oggi gli allievi pronti sono già raggruppati da quattro, per patente. <a class="u" href="case-study-mongelli.html">Leggi il case study</a></p></div></div>
    </div>
  </section>
  <section class="sec">
    {sh('06 / Domande', 'UX design, le domande più comuni.')}
    {faq(FAQ_UX)}
  </section>
{end('Progettiamolo insieme')}"""

# ---------------------------------------------------------------- home

HOME_FOUR = "".join(f'<div>{grid(p, 3, 3, cls="ico", extra=" data-speed=.8")}<h3>{t}</h3><p>{d}</p></div>' for t, d, p in HOME_SERVICES)

HOME = f"""  <section class="hero">
    <div>
      <h1>Dati chiari.<br>Decisioni <span>migliori.</span></h1>
      <p>Merkorn è una software house in Puglia. Invece di chiederti di adattarti a un programma, guardiamo come lavori e costruiamo il gestionale attorno a te.</p>
      <div class="acts"><a class="btn" href="contattaci.html">Prenota un appuntamento</a><a class="u" href="metodo.html">Come lavoriamo</a></div>
    </div>
    <div class="panel" id="heroGoo" aria-hidden="true"></div>
  </section>
{caption('Merkorn', 'Mottola', 'Puglia', 'Gestionali su misura')}
  <section class="sec">
    {sh('01 / Servizi', 'Ogni servizio risolve un problema preciso.')}
    <div class="four">{HOME_FOUR}</div>
    <div style="margin-top:30px"><a class="u" href="servizi.html">Tutti i servizi</a></div>
  </section>
  <section class="sec">
    {sh('02 / UX design', 'Un gestionale vale quanto è facile da usare.')}
    <div class="who"><span></span><div><p class="big">Un software scomodo non lo usa nessuno. <span>Per questo disegniamo ogni schermata con chi la userà ogni giorno, e la proviamo prima di scrivere il codice.</span></p></div></div>
    {ux_compare()}
    <div style="margin-top:30px"><a class="u" href="ux-design.html">Perché la UX conta</a></div>
  </section>
  <div class="strip" data-goo="wave" data-cols="28" data-rows="1" data-cursor="1" aria-hidden="true"></div>
  <section class="sec" style="padding-top:clamp(60px,8vw,100px)">
    {sh('03 / Metodo', 'Quattro fasi, un disegno che cambia.')}
    {method(False)}
  </section>
  <section class="sec">
    {sh('04 / Chi siamo', 'Da Mottola, per le PMI.')}
    <div class="who"><span></span><div><p class="big">Prima veniamo a vedere come lavori. <span>Poi costruiamo il gestionale attorno a te, con lo stesso team dal primo incontro all'assistenza.</span></p>
      <div style="margin-top:30px"><a class="u" href="chi-siamo.html">Conosci il team</a></div></div></div>
  </section>
  <section class="sec">
    {sh('05 / Case study', 'Due gestionali su misura, nati a Mottola.')}
    <div class="case-list">{''.join(case_teaser(c, i) for i, c in enumerate(CASES, 1))}</div>
    <div style="margin-top:30px"><a class="u" href="case-study.html">Come lavoriamo nei case study</a></div>
  </section>
  <section class="sec">
    {sh('06 / Domande', 'Software gestionale su misura, le domande più comuni.')}
    {faq(FAQ_HOME)}
  </section>
{end('Parliamo')}"""
HOME_JS = "<script>Goo(document.getElementById('heroGoo'), { cols: 5, rows: 6, pattern: 'cycle', cursor: true, accent: [[3, 4]] });</script>\n" + METHOD_JS

# ---------------------------------------------------------------- servizi

# programs placed around the logo: inner ring first (the core ones are highlighted), then outer ring
INTEGRATIONS_INNER = ["Fatturazione elettronica", "Contabilità", "Fatture in Cloud", "TeamSystem", "Zucchetti", "WhatsApp Business", "Excel", "Google Workspace"]
INTEGRATIONS_OUTER = ["Microsoft 365", "Teams", "Slack", "Notion", "Shopify", "WooCommerce", "Stripe", "HubSpot", "Zapier"]
CORE = {"Fatturazione elettronica", "Contabilità"}


def orbit():
    import math
    pills = []
    for names, rx, ry, shift in ((INTEGRATIONS_INNER, 27, 31, 0), (INTEGRATIONS_OUTER, 45, 45, .5)):
        n = len(names)
        for i, name in enumerate(names):
            a = math.radians(-90 + (i + shift) * 360 / n)
            x, y = 50 + rx * math.cos(a), 50 + ry * math.sin(a)
            cls = "pill core" if name in CORE else "pill"
            pills.append(f'<li class="{cls}" style="left:{x:.1f}%;top:{y:.1f}%">{name}</li>')
    return f"""<div class="orbit">
      <span class="ring r1" aria-hidden="true"></span><span class="ring r2" aria-hidden="true"></span>
      {grid('logo', 5, 3, cls='hub')}
      <ul aria-label="Programmi che colleghiamo al gestionale">{''.join(pills)}</ul>
    </div>"""


ORBIT = orbit()

SERV_PATTERNS = ["checker", "rings", "drops", "diag", "breathe"]
SERV_PROBLEMS = [
    ("Il programma non segue il tuo lavoro", "Un gestionale pronto impone i suoi passaggi. Le differenze le coprono le persone, a mano, ogni giorno."),
    ("Excel accanto al gestionale", "Quello che il programma non sa fare finisce in un file Excel. Dopo un anno i numeri veri stanno lì, non nel gestionale."),
    ("Programmi che non si parlano", "Ordini, fatture e magazzino su sistemi diversi: lo stesso dato si ricopia più volte, e ogni copia può sbagliare."),
    ("Nessuno lo usa volentieri", "Schermate confuse e troppi passaggi: appena possono, le persone tornano al vecchio metodo. <a class=\"u\" href=\"ux-design.html\">Perché la UX conta</a>"),
    ("Dopo il rilascio, nessuno", "Il fornitore consegna e sparisce. Errori aperti, richieste senza risposta, un software che invecchia."),
]
SERV_ROWS = "".join(
    f'<div class="row"><span class="n">0{i}</span><h3>{t}</h3><div><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in tags)}</ul></div>{grid(p, 3, 3)}</div>'
    for i, ((t, d, tags), p) in enumerate(zip(SERVICES, SERV_PATTERNS), 1))
SERVIZI = f"""{phero('Software gestionale su misura: <span>prima guardiamo come lavori</span>', "Cinque servizi, ognuno nato da un problema preciso. Puoi sceglierne uno o metterli insieme, con lo stesso team dall'inizio alla fine.", 'checker')}
{caption('Servizi', 'Cinque servizi', 'Un solo team')}
  <section class="sec">
    {sh('01 / I problemi', 'Dove si bloccano i gestionali.')}
    {numbered(SERV_PROBLEMS)}
  </section>
  <section class="sec">
    {sh('02 / Cosa facciamo', 'Un servizio per ogni problema, sempre le stesse persone.')}
    <div class="rows" style="border-top:0">{SERV_ROWS}</div>
  </section>
  <section class="sec">
    {sh('03 / Per chi lavoriamo', 'Imprese che vogliono crescere con i propri dati.')}
    <div class="three">
      <div>{grid('drops', 3, 3, cls='ico')}<h3>Agroalimentare e produzione</h3><p>Lotti, scadenze e commesse sempre tracciati.</p></div>
      <div>{grid('wave', 3, 3, cls='ico')}<h3>Commercio e logistica</h3><p>Giacenze, ordini e consegne sempre aggiornati.</p></div>
      <div>{grid('mosaic', 3, 3, cls='ico')}<h3>Squadre sul territorio</h3><p>Interventi e rapportini visibili subito in ufficio.</p></div>
    </div>
  </section>
  <section class="sec">
    {sh('04 / Integrazioni', 'Ci colleghiamo ai programmi che usi già.')}
    {ORBIT}
    <p style="color:var(--muted);max-width:56ch;margin-top:24px">Contabilità, fatturazione elettronica, messaggi, documenti e vendite online parlano con il gestionale. Ogni dato si scrive una volta sola.</p>
  </section>
  <section class="sec">
    {sh('05 / Domande', 'Domande sui nostri servizi.')}
    {faq(FAQ_SERVIZI)}
  </section>
{end('Iniziamo')}"""

# ---------------------------------------------------------------- metodo

METODO = f"""{phero('Come sviluppiamo un gestionale <span>personalizzato</span>', 'Quattro fasi, ognuna con un risultato concreto da verificare.', 'drops')}
{caption('Metodo', 'Quattro fasi', 'Un risultato per fase')}
  <section class="sec">
    {sh('01 / Le fasi', "Dall'analisi alle schermate.")}
    {method(True)}
  </section>
  <div class="strip" data-goo="diag" data-cols="28" data-rows="1" data-cursor="1" aria-hidden="true"></div>
  <section class="sec" style="padding-top:clamp(60px,8vw,100px)">
    {sh('02 / Principi', 'Come progettiamo le schermate.')}
    <div class="four">
      <div>{grid('logo', 5, 3, cls='ico')}<h3>I numeri che contano, in primo piano</h3><p>Apri la schermata e sai subito come sta andando.</p></div>
      <div>{grid('checker', 3, 3, cls='ico')}<h3>Tutto in un unico posto</h3><p>Ordini, magazzino e fatture parlano tra loro.</p></div>
      <div>{grid('rings', 3, 3, cls='ico')}<h3>Chiaro al primo sguardo</h3><p>Quello che richiede attenzione si nota subito.</p></div>
      <div>{grid('breathe', 3, 3, cls='ico')}<h3>Solo quello che ti serve</h3><p>Ogni funzione ha un motivo per esserci.</p></div>
    </div>
  </section>
  <section class="sec">
    {sh('03 / Domande', 'Tempi e costi, senza sorprese.')}
    {faq(FAQ_METODO)}
  </section>
{end('Cominciamo')}"""

# ---------------------------------------------------------------- chi siamo

# partner studios: name, field, description, services, website
PARTNERS = [
    ("GA Studio", "Product design",
     "GA Studio è lo studio di product design di Gianmarco Antonacci. Progetta app, siti web e brand identity, e usa l'intelligenza artificiale per creare foto, video e semplificare i processi. Un solo referente dalla prima call alla consegna, con aggiornamenti ogni settimana.",
     ["App", "Siti web", "Brand identity", "Contenuti con l'AI"],
     "https://gianmarcoantonaccidesigner.it"),
]
PARTNER_ROWS = "".join(
    f'<article class="partner"><div><span class="caps">Studio partner · {field}</span><h3>{name}</h3></div>'
    f'<div><p>{desc}</p><ul>{"".join(f"<li>{t}</li>" for t in tags)}</ul>'
    f'<a class="u" href="{url}" target="_blank" rel="noopener">Visita il sito di {name}</a></div>{grid("rings", 3, 3)}</article>'
    for name, field, desc, tags, url in PARTNERS)

CHI = f"""{phero('Una software house che <span>prima viene a vedere</span>', 'Siamo a Mottola, in provincia di Taranto. Aiutiamo le PMI a lavorare meglio con i propri dati.', 'logo', 5, 3)}
{caption('Chi siamo', 'Mottola', 'Taranto', 'Puglia')}
  <section class="sec">
    {sh('01 / Missione', 'Il digitale, comprensibile e utile.')}
    <div class="who"><span></span><p class="big">Rendere il digitale comprensibile e utile <span>per chi lavora nelle PMI pugliesi. Disegniamo le schermate con chi le userà e le proviamo sul posto, finché ogni passaggio è chiaro.</span></p></div>
  </section>
  <section class="sec">
    {sh('02 / Il team', 'Le persone che seguono il tuo progetto.')}
    <div class="team">
      <div>{grid('breathe', 3, 3)}<h3>Sales manager</h3><p>Il tuo primo contatto. Viene in azienda e prepara con te proposta, tempi e costi.</p></div>
      <div>{grid('rings', 3, 3)}<h3>Project manager e data analyst</h3><p>Trasforma le esigenze in requisiti chiari e segue l'avanzamento del progetto.</p></div>
      <div>{grid('diag', 3, 3)}<h3>Product designer</h3><p>Progetta le schermate e le prova con chi le userà.</p></div>
      <div>{grid('mosaic', 3, 3)}<h3>Developer</h3><p>Scrive il software, lo collega ai tuoi programmi e lo segue dopo il rilascio.</p></div>
    </div>
  </section>
  <section class="sec">
    {sh('03 / Come costruiamo', 'Fondamenta riusabili, superficie su misura.')}
    <div class="layers">
      <div><b>Livello 03</b><div><strong>Le tue schermate</strong><span>Disegnate su come lavori.</span></div>{grid('logo', 5, 3)}</div>
      <div><b>Livello 02</b><div><strong>Componenti su misura</strong><span>Le funzioni specifiche della tua azienda.</span></div>{grid('wave', 8, 2)}</div>
      <div><b>Livello 01</b><div><strong>Moduli collaudati</strong><span>La base solida da cui partire.</span></div>{grid('checker', 8, 2)}</div>
    </div>
  </section>
  <section class="sec">
    {sh('04 / Impegni', 'Tre impegni che manteniamo.')}
    <div class="three">
      <div><h3>Esempi basati su esperienze reali</h3><p>Ogni proposta parte da situazioni già viste in altre aziende.</p></div>
      <div><h3>Tempi e costi definiti</h3><p>Durata e costo di ogni fase, concordati prima di iniziare.</p></div>
      <div><h3>Lo stesso team nel tempo</h3><p>Chi scrive il software lo segue anche dopo.</p></div>
    </div>
  </section>
  <section class="sec">
    {sh('05 / Partner', 'Lavoriamo con studi di cui ci fidiamo.')}
    <div class="partners">{PARTNER_ROWS}</div>
  </section>
{end('Conosciamoci')}"""

# ---------------------------------------------------------------- contattaci

CONTATTI = f"""{phero('Parliamo della <span>tua azienda</span>', 'Scrivici per un appuntamento o un preventivo. Ti rispondiamo personalmente.', 'mosaic')}
{caption('Contatti', 'Mottola', 'Puglia', 'Rispondiamo personalmente')}
  <section class="sec" style="padding-top:clamp(50px,6vw,80px)">
    <div class="contact-block">
      <div class="info">
        <div><small>Email</small><output id="mail-addr">{EMAIL}</output><button class="copy" type="button" data-copy="mail-addr" style="margin-top:12px">Copia indirizzo</button></div>
        <div><small>Sede</small><a href="https://maps.app.goo.gl/npZnGgNFNNix1mri9" target="_blank" rel="noopener">Via Carlo Alberto della Chiesa 12<br>74017 Mottola (TA)</a></div>
        <div><small>Dove lavoriamo</small><b>Soprattutto in Puglia. Per il resto d'Italia il primo incontro si fa online.</b></div>
      </div>
      {contact_form()}
    </div>
  </section>
  <div class="strip" data-goo="wave" data-cols="28" data-rows="1" data-cursor="1" aria-hidden="true" style="margin:clamp(80px,10vw,130px) 0 40px"></div>"""

# ---------------------------------------------------------------- legali e 404


def legal(h1, p, doc, n):
    return f"""{phero(h1, p, 'checker', 8, 3)}
{caption(n, 'Merkorn S.r.l.s.', 'Mottola (TA)')}
  <section class="sec" style="padding-top:clamp(40px,5vw,70px)">
    <div class="doc">{doc}</div>
  </section>"""


PRIVACY = legal('Informativa sul trattamento dei <span>dati personali</span>',
                'Come trattiamo i dati di chi visita il sito e di chi ci scrive, ai sensi degli articoli 13 e 14 del Regolamento UE 2016/679 (GDPR).',
                PRIVACY_DOC, 'Privacy policy')
COOKIE = legal('Come usiamo i <span>cookie</span>',
               'Quali cookie usa il sito merkorn.com, a cosa servono e come potete cambiare le vostre scelte.',
               COOKIE_DOC, 'Cookie policy')

E404 = f"""  <section class="e404">
    <div>
      <div class="num">404<span>.</span></div>
      <h1>Questa pagina si è spostata.</h1>
      <p>L'indirizzo che hai aperto non esiste più, ma il resto è al suo posto.</p>
      <div class="acts"><a class="btn" href="index.html">Torna alla home</a><a class="u" href="contattaci.html">Contattaci</a></div>
    </div>
    <div class="g" id="lostGoo" aria-hidden="true"></div>
  </section>"""
E404_JS = "<script>Goo(document.getElementById('lostGoo'), { cols: 6, rows: 6, pattern: 'cycle', cursor: true });</script>"

# ---------------------------------------------------------------- pagine

# path, <title>, meta description, body, scripts, structured data
PAGES = [
    ("index.html", "Software gestionale su misura per PMI | Merkorn",
     "Merkorn è una software house in Puglia che sviluppa software gestionali su misura per PMI: ordini, magazzino, produzione e fatturazione in un unico sistema.",
     HOME, HOME_JS, [faq_ld(FAQ_HOME)]),
    ("ux-design.html", "UX design per software gestionali | Merkorn",
     "Perché la UX conta in un software gestionale: meno errori, formazione più breve, più tempo per il lavoro vero. Come la progettiamo con chi userà il gestionale.",
     UX, "", [faq_ld(FAQ_UX)]),
    ("metodo.html", "Come sviluppiamo un gestionale personalizzato | Merkorn",
     "Il metodo Merkorn per sviluppare un gestionale personalizzato: analisi dei processi, moduli collaudati, componenti su misura e interfacce semplici da usare.",
     METODO, METHOD_JS, [faq_ld(FAQ_METODO)]),
    ("servizi.html", "Gestionale personalizzato, magazzino e produzione | Merkorn",
     "Gestionale su misura per aziende, gestionale di magazzino e produzione, app per le consegne e analisi dei processi, integrati con la fatturazione elettronica.",
     SERVIZI, "", SERVICES_LD + [faq_ld(FAQ_SERVIZI)]),
    ("chi-siamo.html", "Software house a Taranto e in Puglia per PMI | Merkorn",
     "Merkorn è una software house di Mottola (Taranto): sales manager, project manager, product designer e developer che sviluppano gestionali su misura per PMI.",
     CHI, "", []),
    ("case-study.html", "Case study: gestionali su misura realizzati | Merkorn",
     "I progetti di Merkorn: il gestionale di Kuelle Sports Center e quello dell'Autoscuola Centrale Mongelli, dai problemi di partenza alle schermate.",
     CASE_HUB, "", []),
    ("case-study-kuelle.html", "Case study: gestionale per centro sportivo | Merkorn",
     "Come Merkorn ha costruito il gestionale di Kuelle Sports Center a Mottola: andamento dei campi, partite da completare con WhatsApp, saldi dei giocatori e turni.",
     CASE_PAGES[0], "", []),
    ("case-study-mongelli.html", "Case study: gestionale per autoscuola | Merkorn",
     "Come Merkorn ha costruito il gestionale dell'Autoscuola Centrale Mongelli a Mottola: calendario delle guide, gruppi d'esame da quattro e andamento degli allievi.",
     CASE_PAGES[1], "", []),
    ("contattaci.html", "Preventivo gestionale su misura | Merkorn",
     "Contatta Merkorn per un appuntamento o un preventivo per un software gestionale su misura. Primo incontro in azienda o online, senza impegno.",
     CONTATTI, "", []),
    ("404.html", "Pagina non trovata | Merkorn",
     "La pagina cercata si è spostata. Torna alla home di Merkorn.",
     E404, E404_JS, []),
    ("privacy.html", "Privacy policy | Merkorn",
     "Privacy policy di Merkorn: come trattiamo i dati di chi visita il sito e di chi ci contatta, ai sensi del GDPR.",
     PRIVACY, "", []),
    ("cookie.html", "Cookie policy | Merkorn",
     "Quali cookie usa il sito di Merkorn, a cosa servono e come modificare le scelte sul consenso.",
     COOKIE, "", []),
]

if __name__ == "__main__":
    from datetime import date
    for path, title, desc, body, scripts, ld in PAGES:
        html = page(path, title, desc, body, scripts, ld)
        if path == "404.html":
            # served at any missing address: absolute base for links and assets, kept out of search results
            html = html.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<base href="/">', 1)
            html = html.replace('content="index, follow, max-image-preview:large, max-snippet:-1"', 'content="noindex, follow"')
            html = re.sub(r'<link rel="(canonical|alternate)"[^>]*>\n', "", html)
            html = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", html, flags=re.S)
        (ROOT / path).write_text(html, encoding="utf-8")
        print("scritto", path)
    today = date.today().isoformat()
    urls = "".join(
        f"<url><loc>https://merkorn.com/{'' if p == 'index.html' else p}</loc><lastmod>{today}</lastmod>"
        f"<priority>{'1.0' if p == 'index.html' else '0.3' if p in ('privacy.html', 'cookie.html') else '0.8'}</priority></url>"
        for p, *_ in PAGES if p != "404.html")
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    print("scritto sitemap.xml")
