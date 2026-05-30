# ⚔️ AutoVote — Minecraft-Italia

Bot automatico per votare il server **Charlie** su [minecraft-italia.net](https://minecraft-italia.net) ogni giorno, senza aprire il browser.

> Funziona in background, silenzioso. Vota da solo ogni 10 minuti finché non registra il voto del giorno, poi si ferma fino al giorno successivo.

---

## 📦 Download

Vai nella sezione [**Releases**](../../releases) e scarica l'ultimo `AutoVote.exe`.  
Non serve installare Python o nient'altro.

---

## ⚙️ Configurazione iniziale

### 1. Avvia il bot almeno una volta

Fai doppio clic su `AutoVote.exe` oppure aggiungilo subito allo **shell:startup** (vedi sotto).  
Al primo avvio il bot crea automaticamente il file delle credenziali in:

```
C:\Users\<TuoNome>\Documents\history-vote\accounts.env
```

### 2. Inserisci le credenziali

Apri il file `accounts.env` con il Blocco Note e compila i campi:

```env
# Credenziali account.
USERNAME=il_tuo_username
PASSWORD=la_tua_password
```

Salva e chiudi. Il bot leggerà le credenziali al prossimo ciclo automaticamente.

> ⚠️ Il file è in testo semplice. Non condividerlo con nessuno.

---

## 🚀 Avvio automatico con Windows

Per far partire il bot automaticamente ad ogni accensione del PC, aggiungilo alla **Cartella di Avvio** di Windows.

**1.** Premi `Win + R`, scrivi:
```
shell:startup
```
e premi **Invio**. Si apre una cartella di Esplora file.

**2.** Metti il collegamento a `AutoVote.exe` in quella cartella:
- Fai clic destro su `AutoVote.exe` → **Invia a** → **Desktop (crea collegamento)**
- Sposta il collegamento appena creato dentro la cartella `shell:startup`

oppure:
- Fai clic destro dentro `shell:startup` → **Nuovo** → **Collegamento**
- Inserisci il percorso completo, ad esempio:
  ```
  C:\Users\<TuoNome>\Desktop\AutoVote.exe
  ```
- Dai un nome (es. `AutoVote`) e clicca **Fine**

**3.** Da questo momento il bot si avvia da solo ad ogni accensione, in background, senza nessuna finestra visibile.

> 💡 Puoi verificare che stia funzionando aprendo il file `history.txt` nella stessa cartella di `accounts.env`.

---

## 📋 Come funziona

```
Avvio
  │
  ├─ Controlla se ha già votato oggi
  │     └─ Sì → aspetta 10 minuti e ricontrolla
  │     └─ No → apre Chrome invisibile
  │               ├─ Accetta i cookie
  │               ├─ Effettua il login
  │               ├─ Naviga alla pagina del server Charlie
  │               ├─ Clicca "Vota"
  │               ├─ Clicca "Ho votato"
  │               └─ Salva il risultato nel log
  │
  └─ Aspetta 10 minuti → ricomincia
```

Il log giornaliero tiene traccia di ogni tentativo:
- ✅ `successo - voto registrato`
- ❌ `fallito - errore login (timeout)`
- ❌ `fallito - Chrome non avviabile: ...`

---

## 🗂️ File generati

| Percorso | Contenuto |
|---|---|
| `Documents\history-vote\accounts.env` | Username e password |
| `Documents\history-vote\history.txt` | Log di tutti i voti |

---

## ❓ Problemi comuni

**Il bot non vota / il log è vuoto**
- Verifica che `accounts.env` abbia username e password compilati
- Verifica che Google Chrome sia installato sul PC
- Controlla `history.txt` per leggere il messaggio di errore

**"Chrome non avviabile"**
- Aggiorna Google Chrome all'ultima versione (richiede Chrome 112 o superiore)

**Non trovo la cartella shell:startup**
- Percorso manuale: `C:\Users\<TuoNome>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

---

## 🛠️ Compilare da sorgente

```bash
pip install pyinstaller selenium webdriver-manager python-dotenv
pyinstaller --onefile --noconsole --name AutoVote auto_vote.py
```

L'exe sarà in `dist/AutoVote.exe`.

---

## 📄 Licenza

MIT — fai quello che vuoi, a tuo rischio e pericolo.
