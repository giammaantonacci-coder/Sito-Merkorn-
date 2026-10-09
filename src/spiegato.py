"""Il digitale spiegato: articoli brevi, situazioni tipiche e glossario.

Ogni articolo diventa una pagina digitale-spiegato-<slug>.html. Per aggiungerne uno basta
inserirlo in ARTICLES e rieseguire src/build.py.
Regole di scrittura: esempi concreti, parole di tutti i giorni, niente due punti, niente numeri
senza una fonte, niente casi di clienti inventati.
"""

HUB = "digitale-spiegato.html"
PUBLISHED = "2026-10-09"

# slug, kicker, icon key (CARD_ICONS), title, title in the hero (with <em>), description, intro, [(h2, [paragraphs])]
ARTICLES = [
    ("gestionale-su-misura-o-pronto", "Scegliere", "Chiarezza",
     "Gestionale su misura o pronto, come scegliere",
     "Gestionale su misura o pronto, <em>come scegliere</em>",
     "Quando basta un gestionale pronto e quando serve un gestionale su misura. I segnali da guardare e un modo semplice per decidere.",
     "Un gestionale pronto si installa in poco tempo e costa meno all'inizio. Un gestionale su misura richiede più lavoro prima di partire, ma segue il tuo processo. La scelta dipende da quanto il tuo modo di lavorare somiglia a quello previsto dal programma.",
     [("Quando basta un gestionale pronto",
       ["Se i tuoi processi sono simili a quelli di molte altre aziende del settore, per esempio una fatturazione semplice e un magazzino con pochi articoli, un programma standard fa il suo lavoro. Conviene provarlo con i tuoi dati veri prima di acquistarlo."]),
      ("I segnali che serve qualcosa su misura",
       ["Il segnale più chiaro è il foglio Excel che torna fuori accanto al gestionale. Se per gestire commesse, varianti di prodotto o consegne qualcuno ricopia i dati a mano, il programma non copre una parte del lavoro.",
        "Altri segnali sono le funzioni pagate e mai usate, e le persone che chiedono ogni volta a un collega come si fa una certa operazione."]),
      ("Una via di mezzo",
       ["Molti gestionali su misura non partono da zero. Si usano moduli già collaudati per anagrafiche, permessi e stampe, e si sviluppa su misura solo la parte che distingue la tua azienda. Così tempi e costi restano sotto controllo."]),
      ("Come decidere",
       ["Prima di scegliere, scrivi il percorso di un ordine dal primo contatto alla fattura, con le persone coinvolte e i programmi usati in ogni passaggio. Se un programma pronto copre tutto il percorso, parti da quello. Se restano dei buchi, vale la pena valutare un software su misura.",
        "Nel primo appuntamento facciamo proprio questo esercizio, e te lo diciamo con franchezza anche quando il su misura non conviene."])]),

    ("cos-e-un-erp", "Concetti", "Sviluppo",
     "Cos'è un ERP e quando serve a una piccola impresa",
     "Cos'è un <em>ERP</em> e quando serve a una piccola impresa",
     "Cosa vuol dire ERP, che differenza c'è con un gestionale e quando conviene anche a una piccola o media impresa.",
     "ERP sta per Enterprise Resource Planning, cioè pianificazione delle risorse aziendali. In pratica è un gestionale che tiene insieme in un unico sistema le aree dell'azienda, come vendite, acquisti, magazzino, produzione e contabilità.",
     [("Che differenza c'è con un gestionale",
       ["Nel linguaggio di tutti i giorni le due parole si usano quasi come sinonimi. Di solito si parla di ERP quando il sistema copre più reparti e i dati passano da uno all'altro senza essere ricopiati.",
        "Un ordine inserito dal commerciale aggiorna il magazzino, avvisa la produzione e arriva in fattura, senza che nessuno lo riscriva."]),
      ("Serve anche a una PMI?",
       ["Non serve la dimensione di una grande azienda. Serve quando gli stessi dati vengono inseriti più volte in programmi diversi, o quando per sapere a che punto è un ordine bisogna telefonare a tre persone. Succede anche in aziende con pochi dipendenti."]),
      ("Da dove partire",
       ["Non è necessario digitalizzare tutto insieme. Si può partire dal reparto dove si perde più tempo, per esempio il magazzino, e aggiungere le altre aree un passo alla volta. Ogni parte rilasciata si usa subito, senza aspettare la fine del progetto."])]),

    ("da-excel-al-gestionale", "Dati", "Concretezza",
     "Dal foglio Excel al gestionale, come si passa senza fermare il lavoro",
     "Dal foglio Excel al gestionale, <em>senza fermare il lavoro</em>",
     "Come si passa dai fogli Excel a un gestionale. Cosa si importa, come si fa pulizia nei dati e perché il passaggio avviene per gradi.",
     "Molte aziende gestiscono ordini, magazzino o commesse con fogli Excel cresciuti negli anni. Funzionano finché li usa una persona sola. Quando i file diventano tanti e li aggiornano in più persone, arrivano gli errori e le versioni diverse dello stesso dato.",
     [("Prima si guarda come si usano i fogli",
       ["Ogni foglio Excel racconta un pezzo del processo. Colonne aggiunte nel tempo, colori usati come promemoria, formule che solo una persona sa modificare.",
        "Prima di sviluppare qualcosa guardiamo questi file insieme a chi li usa, perché contengono regole che nessuno ha mai scritto altrove."]),
      ("I dati si importano, non si ricopiano",
       ["Anagrafiche di clienti e fornitori, articoli, listini e giacenze si possono importare nel nuovo gestionale. Prima dell'importazione si fa pulizia, eliminando doppioni e righe incomplete. È un lavoro noioso, ma è il momento giusto per farlo."]),
      ("Il passaggio avviene per gradi",
       ["Per qualche settimana il vecchio foglio e il nuovo gestionale possono convivere su una sola area, così si confrontano i risultati e le persone imparano senza pressione. Quando i numeri tornano, il foglio va in archivio."]),
      ("Cosa non cambia",
       ["Le persone continuano a fare il loro lavoro nello stesso ordine di prima. Il gestionale toglie i passaggi di copia e i controlli manuali, non aggiunge passaggi nuovi."])]),

    ("gestionale-e-fatturazione-elettronica", "Fatture", "Requisiti",
     "Gestionale e fatturazione elettronica, cosa vuol dire collegarli",
     "Gestionale e fatturazione elettronica, <em>cosa vuol dire collegarli</em>",
     "Cosa succede quando il gestionale è collegato alla fatturazione elettronica e allo SDI, e cosa cambia per l'ufficio e per il commercialista.",
     "In Italia le fatture elettroniche passano dal Sistema di Interscambio dell'Agenzia delle Entrate, lo SDI. Molte imprese le preparano con un programma di fatturazione separato dal resto e ricopiano a mano i dati degli ordini e delle consegne.",
     [("Cosa succede quando sono collegati",
       ["Con un collegamento la fattura nasce dai dati che sono già nel gestionale. Cliente, articoli, prezzi e documenti di trasporto arrivano in fattura senza essere riscritti.",
        "Il file della fattura elettronica viene generato e inviato allo SDI tramite il programma o l'intermediario che usi già."]),
      ("Cosa si guadagna",
       ["Meno errori di battitura, nessun dato inserito due volte e lo stato di ogni fattura visibile accanto all'ordine da cui è nata. Anche le fatture ricevute dai fornitori possono essere abbinate agli ordini di acquisto."]),
      ("Non serve cambiare commercialista",
       ["Il collegamento si adatta ai programmi di contabilità e di fatturazione che usi. Il commercialista continua a ricevere i dati come prima, e li riceve più ordinati."])]),

    ("cos-e-la-ux", "Esperienza d'uso", "Design",
     "Cos'è la UX e perché conta in un gestionale",
     "Cos'è la <em>UX</em> e perché conta in un gestionale",
     "Cosa vuol dire UX, perché l'esperienza d'uso conta in un software che si usa ogni giorno e come si progetta un gestionale facile da usare.",
     "UX sta per user experience, l'esperienza di chi usa un software. Riguarda quanto è facile capire cosa fare, trovare un'informazione e completare un'operazione senza errori.",
     [("Perché conta proprio nei gestionali",
       ["Un gestionale si usa ogni giorno, spesso di corsa, al bancone o in magazzino. Se un'operazione frequente richiede dieci clic invece di tre, il tempo perso si somma giorno dopo giorno. Se una schermata è confusa, le persone tornano al foglio di carta."]),
      ("Come si progetta",
       ["Si osservano le persone mentre lavorano, si disegnano le schermate e si provano prima di scrivere il codice. Le informazioni più usate stanno in alto, le azioni frequenti hanno un pulsante visibile, i dati che richiedono attenzione sono evidenziati."]),
      ("Cosa cambia per l'azienda",
       ["Un software progettato bene richiede meno formazione, genera meno errori e viene usato davvero. È la differenza tra un programma che aiuta il lavoro e uno che resta acceso ma ignorato."])]),
]

# icon key, title, text: everyday scenes, not client cases
SITUATIONS = [
    ("Requisiti", "Gli ordini arrivano su WhatsApp",
     "Un modulo ordini li raccoglie in un posto solo e li passa al magazzino."),
    ("Distribuzione", "Le giacenze non tornano mai",
     "Con carichi e scarichi registrati al momento, il dato è sempre quello vero."),
    ("Produzione", "Lo stato della commessa si chiede al telefono",
     "Una schermata con lo stato delle commesse risponde al posto del reparto."),
    ("Servizi", "La bolla torna in ufficio a fine giro",
     "Con un'app l'autista chiude la consegna con la firma del cliente."),
]

# term, definition, related article slug or None
GLOSSARY = [
    ("Anagrafica", "L'archivio con i dati di clienti, fornitori o articoli, usato da tutte le parti del gestionale.", None),
    ("API", "Un canale che permette a due programmi di scambiarsi dati in automatico, senza esportare e importare file.", None),
    ("Backup", "Una copia dei dati salvata in un altro luogo, per recuperarli in caso di guasto o di errore.", None),
    ("Cloud", "Il software e i dati stanno su server esterni e si usano dal browser, senza installare programmi sui computer dell'azienda.", None),
    ("Commessa", "Un lavoro per un cliente seguito dall'ordine alla consegna, con tempi, materiali e costi propri.", None),
    ("DDT", "Il documento di trasporto che accompagna la merce e indica cosa viene consegnato, a chi e quando.", None),
    ("ERP", "Un gestionale che tiene insieme più aree dell'azienda in un unico sistema, dalle vendite alla contabilità.", "cos-e-un-erp"),
    ("Gestionale", "Il software che un'azienda usa per gestire ordini, magazzino, fatture e le altre attività di ogni giorno.", None),
    ("Gestionale su misura", "Un gestionale progettato sui processi di una specifica azienda, invece di adattare il lavoro a un programma pronto.", "gestionale-su-misura-o-pronto"),
    ("Giacenza", "La quantità di un articolo presente in magazzino in un certo momento.", None),
    ("Integrazione", "Il collegamento tra il gestionale e altri programmi, per esempio la contabilità, così i dati si inseriscono una volta sola.", "gestionale-e-fatturazione-elettronica"),
    ("Modulo", "Una parte del gestionale dedicata a un'area, come il magazzino o la fatturazione, che si aggiunge quando serve.", None),
    ("Rilascio", "La consegna di una nuova versione o di una nuova parte del software, pronta per essere usata.", None),
    ("SDI", "Il Sistema di Interscambio dell'Agenzia delle Entrate, da cui passano le fatture elettroniche.", "gestionale-e-fatturazione-elettronica"),
    ("UX", "L'esperienza di chi usa un software, cioè quanto è facile e chiaro usarlo.", "cos-e-la-ux"),
]


def article_path(slug):
    return f"digitale-spiegato-{slug}.html"


def reading_minutes(intro, sections):
    words = len(intro.split()) + sum(len(h.split()) + sum(len(p.split()) for p in ps) for h, ps in sections)
    return max(1, round(words / 200))


def term_id(term):
    return "t-" + term.lower().replace(" ", "-").replace("'", "")
