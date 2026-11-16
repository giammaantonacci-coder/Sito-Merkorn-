# Sito Merkorn

Sito statico di Merkorn. Non serve un server applicativo: basta pubblicare la cartella principale su un hosting statico (per esempio Vercel, Netlify o GitHub Pages).

## Pagine

| File | Pagina |
| --- | --- |
| `index.html` | Home |
| `metodo.html` | Come lavoriamo |
| `servizi.html` | Servizi |
| `chi-siamo.html` | Chi siamo |
| `contattaci.html` | Contattaci |
| `privacy.html` | Informativa privacy |

Il form di contatto è nella pagina Contattaci; tutte le altre pagine si chiudono con un invito che porta lì.

## Struttura

- `assets/sito.css` stili del sito: fondo chiaro, impaginazione editoriale, colori e font della brand identity
- `assets/goo.js` i blocchi del logo che si fondono, reagiscono al cursore e cambiano disegno. Si fermano mentre la pagina scorre (tranne il riquadro delle fasi) e restano fermi se il dispositivo chiede meno animazioni
- `assets/sito.js` menu mobile, copia dell'indirizzo email, statistiche anonime, form di contatto
- `assets/consent.js` banner dei cookie e caricamento di Google Tag Manager solo con il consenso
- `src/partials.py` head (SEO, dati strutturati, consenso), menu, form e footer, uguali su tutte le pagine
- `src/build.py` contenuti delle pagine
- `src/legal.py` testi di privacy e cookie policy

Le pagine HTML si generano con:

```
python3 src/build.py
```

Dopo aver modificato testi, header, footer o form, rieseguire il comando e pubblicare i file generati.

## Form di contatto

Il form invia le richieste alla funzione `api/contact.js`, che Vercel pubblica come `/api/contact`. La funzione spedisce ogni richiesta dalla casella **merkornsh@gmail.com** alla stessa casella, tramite il server SMTP di Gmail. Rispondendo all'email si risponde direttamente a chi ha scritto.

Configurazione, da fare una sola volta:

1. Nell'account Google di merkornsh@gmail.com attivare la verifica in due passaggi, poi creare una password per le app su https://myaccount.google.com/apppasswords.
2. Su Vercel, nel progetto sito-merkorn, aprire Settings, poi Environment Variables, e aggiungere per l'ambiente Production:
   - `GMAIL_USER` = `merkornsh@gmail.com`
   - `GMAIL_APP_PASSWORD` = la password di 16 caratteri appena creata
3. Rifare il deploy dell'ultima versione (Deployments, poi Redeploy) e inviare una richiesta di prova dal sito.

Finché le due variabili non sono impostate, la funzione risponde 503 e il form usa FormSubmit come riserva. Se anche l'invio non riesce, il form offre un link che apre la stessa richiesta già compilata nel programma di posta di chi scrive.

## Da completare

- Configurare le variabili `GMAIL_USER` e `GMAIL_APP_PASSWORD` su Vercel (vedi sopra).
- Inserire l'ID di Google Analytics in `GA_ID` (`src/partials.py`) per attivare le statistiche.

## Proposte di design

La cartella `design/` contiene le proposte grafiche esplorate prima della versione definitiva.
