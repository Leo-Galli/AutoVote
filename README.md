# ⚔️ AutoVote — Minecraft-Italia

Bot automatico per votare il server **Charlie** su [minecraft-italia.net](https://minecraft-italia.net) ogni giorno, senza aprire il browser.

> Funziona in background, silenzioso. Vota da solo ogni 10 minuti finché non registra il voto del giorno, poi si ferma fino al giorno successivo.

---

## 📦 Download

Vai nella sezione [**Releases**](../../releases) e scarica l'ultimo `AutoVote.exe`.  
Non serve installare Python o nient'altro.

---

## ⚙️ Configurazione iniziale

### 1. Inserisci le credenziali

Apri il **Prompt dei comandi** nella cartella dove hai messo `AutoVote.exe` e lancia:

```
AutoVote.exe --set-credenziali
```

Ti verrà chiesto:
```
Imposta le credenziali:
  Username: il_tuo_username
  Password: la_tua_password
```

Le credenziali vengono salvate in:
```
C:\Users\<TuoNome>\Documents\history-vote\accounts.env
```

> ⚠️ Il file è in testo semplice. Non condividerlo con nessuno.

---

### 2. Prova manuale (opzionale)

Per verificare che tutto funzioni prima di impostare l'avvio automatico:

```
AutoVote.exe --once
```

Controlla poi il log in:
```
C:\Users\<TuoNome>\Documents\history-vote\history.txt
```

Dovresti vedere una riga come:
```
2025-01-15 | tuo_username | 08:32:11 - successo - voto registrato
```

---

## 🚀 Avvio automatico con Windows

Per far partire il bot automaticamente ad ogni accensione del PC, aggiungilo alla **Cartella di Avvio** di Windows.

### Procedura

**1.** Premi `Win + R`, scrivi:
```
shell:startup
```
e premi **Invio**. Si apre una cartella di Esplora file.

**2.** Crea un collegamento di `AutoVote.exe` in quella cartella:
- Fai clic destro su `AutoVote.exe` → **Invia a** → **Desktop (crea collegamento)**
- Poi sposta il collegamento appena creato dentro la cartella `shell:startup`

oppure più velocemente:
- Fai clic destro dentro la cartella `shell:startup` → **Nuovo** → **Collegamento**
- Inserisci il percorso completo dell'exe, ad esempio:
  ```
  C:\Users\<TuoNome>\Desktop\AutoVote.exe
  ```
- Dai un nome al collegamento (es. `AutoVote`) e clicca **Fine**

**3.** Da questo momento, ogni volta che accendi il PC il bot si avvia da solo in background.

> 💡 Non vedrai nessuna finestra aperta: il programma gira silenzioso. Puoi verificare che stia funzionando dal file `history.txt`.

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
- Assicurati di aver inserito le credenziali con `--set-credenziali`
- Verifica che Google Chrome sia installato sul PC
- Controlla `history.txt` per vedere il messaggio di errore

**"Chrome non avviabile"**
- Aggiorna Google Chrome all'ultima versione (richiede Chrome 112 o superiore)

**Non trovo la cartella shell:startup**
- Percorso manuale: `C:\Users\<TuoNome>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

---

## 🛠️ Compilare da sorgente

Se vuoi compilare l'exe da solo:

```bash
pip install pyinstaller selenium webdriver-manager python-dotenv
pyinstaller --onefile --noconsole --name AutoVote auto_vote.py
```

L'exe sarà in `dist/AutoVote.exe`.

---

## 📄 Licenza

MIT — fai quello che vuoi, a tuo rischio e pericolo.
