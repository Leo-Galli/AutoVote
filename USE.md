# 🗳️ AutoVote — Guida all'uso

Script Python per votare automaticamente CharlieRoleplay su minecraft-italia.net.  
Disponibile per **Windows**, **macOS** e **Linux**.

---

## Quale script usare?

| Sistema Operativo | File                  |
|-------------------|-----------------------|
| Windows           | `autovote_win.py`     |
| macOS             | `autovote_mac.py`     |
| Linux (qualsiasi) | `autovote_linux.py`   |

---

## Requisiti comuni

- **Python 3.10+**
- **Google Chrome** o **Chromium** installato
- Connessione Internet

---

---

## 🪟 Windows

### 1. Installa Python

Scarica Python da [python.org](https://www.python.org/downloads/).  
Durante l'installazione spunta **"Add Python to PATH"**.

### 2. Installa le dipendenze

Apri il **Prompt dei comandi** (`cmd`) o **PowerShell** nella cartella dello script:

```bat
pip install selenium webdriver-manager python-dotenv
```

### 3. Configura le credenziali

```bat
python autovote_win.py --set-credenziali
```

Inserisci username e password di minecraft-italia.net quando richiesto.

### 4. Avvia lo script

**Loop continuo** (controlla ogni 10 minuti):
```bat
python autovote_win.py
```

**Una sola esecuzione:**
```bat
python autovote_win.py --once
```

### 5. Avvio automatico con Windows (opzionale)

Per avviare il loop all'avvio del PC:

1. Premi `Win + R`, digita `shell:startup`, premi Invio
2. Crea un file `autovote.bat` con questo contenuto:
   ```bat
   @echo off
   python C:\percorso\autovote_win.py
   ```
3. Metti il file `.bat` nella cartella Startup

### File di log e credenziali

I file vengono salvati in:
```
C:\Users\<TuoNome>\Documents\history-vote\
├── accounts.env   ← credenziali
└── history.txt    ← log voti
```

---

---

## 🍎 macOS

### 1. Installa Python

**Opzione A — Homebrew (consigliato):**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

**Opzione B:** Scarica da [python.org](https://www.python.org/downloads/).

### 2. Installa Google Chrome

Scarica da [google.com/chrome](https://www.google.com/chrome/) e installalo normalmente.  
ChromeDriver viene scaricato automaticamente dallo script.

### 3. Installa le dipendenze

Apri il **Terminale** nella cartella dello script:

```bash
pip3 install selenium webdriver-manager python-dotenv
```

### 4. Configura le credenziali

```bash
python3 autovote_mac.py --set-credenziali
```

### 5. Avvia lo script

**Loop continuo:**
```bash
python3 autovote_mac.py
```

**Una sola esecuzione:**
```bash
python3 autovote_mac.py --once
```

### 6. Avvio automatico con launchd (opzionale)

Crea il file `~/Library/LaunchAgents/com.autovote.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.autovote</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/percorso/completo/autovote_mac.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/autovote.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/autovote.err</string>
</dict>
</plist>
```

Attivalo:
```bash
launchctl load ~/Library/LaunchAgents/com.autovote.plist
```

### Errore "chromedriver non verificato" (Gatekeeper)

Se macOS blocca chromedriver:
```bash
xattr -d com.apple.quarantine $(which chromedriver)
```
Oppure: **Preferenze di Sistema → Privacy e Sicurezza → Consenti**.

### File di log e credenziali

```
~/.local/share/history-vote/    (o ~/Documents/history-vote/)
├── accounts.env
└── history.txt
```

---

---

## 🐧 Linux (Ubuntu, Debian, Fedora, Arch, openSUSE…)

### 1. Installa Python

Python 3 è già presente sulla maggior parte delle distro. Verifica:
```bash
python3 --version
```

Se non è installato:

| Distro            | Comando                            |
|-------------------|------------------------------------|
| Ubuntu / Debian   | `sudo apt install python3 python3-pip` |
| Fedora            | `sudo dnf install python3 python3-pip` |
| Arch              | `sudo pacman -S python python-pip` |
| openSUSE          | `sudo zypper install python3 python3-pip` |

### 2. Installa Chrome o Chromium

Lo script rileva automaticamente qualsiasi browser Chrome/Chromium installato.

**Ubuntu / Debian:**
```bash
sudo apt install chromium-browser
# oppure Google Chrome:
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update && sudo apt install google-chrome-stable
```

**Fedora:**
```bash
sudo dnf install chromium
```

**Arch:**
```bash
sudo pacman -S chromium
```

**openSUSE:**
```bash
sudo zypper install chromium
```

### 3. Installa le dipendenze Python

```bash
pip3 install selenium webdriver-manager python-dotenv
```

> Su alcune distro potrebbe essere necessario `pip3 install --user ...` oppure usare un virtualenv.

### 4. Configura le credenziali

```bash
python3 autovote_linux.py --set-credenziali
```

### 5. Avvia lo script

**Loop continuo:**
```bash
python3 autovote_linux.py
```

**Una sola esecuzione:**
```bash
python3 autovote_linux.py --once
```

**In background (nohup):**
```bash
nohup python3 autovote_linux.py > ~/autovote.log 2>&1 &
echo $! > ~/autovote.pid   # salva il PID per killarlo dopo
```

Per fermarlo:
```bash
kill $(cat ~/autovote.pid)
```

### 6. Avvio automatico con systemd (opzionale)

Crea il file `/etc/systemd/system/autovote.service` (o `~/.config/systemd/user/autovote.service` per user service):

```ini
[Unit]
Description=AutoVote Minecraft-Italia
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /percorso/completo/autovote_linux.py
Restart=on-failure
RestartSec=30

[Install]
WantedBy=default.target
```

Attivalo:
```bash
systemctl --user daemon-reload
systemctl --user enable --now autovote.service

# Controlla i log:
journalctl --user -u autovote.service -f
```

### Ambienti senza display (server headless, VPS, Docker)

Lo script gira già in modalità headless (nessuna finestra). Su server senza X11 potrebbe essere necessario installare le dipendenze grafiche minime:

```bash
# Ubuntu/Debian
sudo apt install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 \
    libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 \
    libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 \
    ca-certificates fonts-liberation libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 \
    libnspr4 xdg-utils
```

### File di log e credenziali

```
~/.local/share/history-vote/
├── accounts.env
└── history.txt
```

---

---

## 📋 Riepilogo comandi

| Azione                    | Comando                                  |
|---------------------------|------------------------------------------|
| Imposta credenziali       | `python3 autovote_<os>.py --set-credenziali` |
| Avvia loop continuo       | `python3 autovote_<os>.py`               |
| Esegui una sola volta     | `python3 autovote_<os>.py --once`        |
| Aiuto                     | `python3 autovote_<os>.py --help`        |

---

## 🔍 Formato del log

```
2025-06-11 | mario_rossi | 08:32:14 - successo - voto registrato
2025-06-11 | mario_rossi | 14:10:02 - fallito - errore login (timeout)
```

Lo script non vota mai due volte nello stesso giorno per lo stesso account.

---

## ❓ Problemi comuni

**`ModuleNotFoundError`** — installa le dipendenze con `pip3 install selenium webdriver-manager python-dotenv`

**`Chrome non avviabile`** — assicurati che Chrome o Chromium sia installato e aggiornato

**`Timeout login`** — verifica che username e password in `accounts.env` siano corretti

**`Permission denied` su chromedriver (macOS/Linux)** — esegui `chmod +x /path/to/chromedriver`

**Loop che non riparte dopo il riavvio** — configura l'avvio automatico con launchd (macOS) o systemd (Linux) come descritto sopra