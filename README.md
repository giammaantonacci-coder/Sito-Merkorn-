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

Il form di contatto è presente in fondo a ogni pagina e occupa l'intera pagina Contattaci.

## Struttura

- `assets/style.css` stili condivisi, derivati dalla brand identity
- `assets/nebula.js` sfondo animato (WebGL, nessuna libreria). Ogni pagina usa una zona diversa della nebula tramite `data-seed` sul `<body>`
- `assets/site.js` menu mobile, transizione tra pagine, indicatore di sezione, form di contatto
- `src/partials.py` header, footer e form, uguali su tutte le pagine
- `src/build.py` contenuti delle pagine

Le pagine HTML si generano con:

```
python3 src/build.py
```

Dopo aver modificato testi, header, footer o form, rieseguire il comando e pubblicare i file generati.

## Form di contatto

Le richieste vengono inviate a **merkornsh@gmail.com** tramite il servizio gratuito [FormSubmit](https://formsubmit.co), senza bisogno di un backend.

Attivazione, da fare una sola volta dopo la pubblicazione:

1. Aprire il sito pubblicato e inviare una richiesta di prova dal form.
2. FormSubmit invia a merkornsh@gmail.com un'email di conferma. Aprirla e cliccare il link di attivazione.
3. Da quel momento tutte le richieste arrivano nella casella, con oggetto "Nuova richiesta dal sito Merkorn" e l'argomento scelto. Rispondendo all'email si risponde direttamente a chi ha scritto.

Facoltativo: dopo l'attivazione FormSubmit fornisce un indirizzo alternativo (una stringa casuale) che nasconde l'email nel codice della pagina. Per usarlo basta sostituire il valore di `ENDPOINT` in `assets/site.js`.

## Da completare

- `privacy.html`: ragione sociale, partita IVA, sede legale e periodo di conservazione dei dati (evidenziati nella pagina).

## Proposte di design

La cartella `design/` contiene le proposte grafiche esplorate prima della versione definitiva.
