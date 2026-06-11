import os
import sys
import time
import argparse
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from dotenv import dotenv_values

# --- Costanti ---
CHECK_INTERVAL = 600
SITE_URL = 'https://minecraft-italia.net/'
SERVER_URL = 'https://minecraft-italia.net/lista/server/charlie'


def resource_path(path: str) -> str:
    if getattr(sys, 'frozen', False):
        base = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        return os.path.join(base, path)
    return path


def get_history_folder() -> str:
    """
    Su Linux usa XDG_DATA_HOME se disponibile, altrimenti ~/.local/share/history-vote.
    Fallback nella cartella dello script.
    """
    xdg = os.environ.get('XDG_DATA_HOME', '').strip()
    if xdg:
        base = xdg
    else:
        base = os.path.join(os.path.expanduser('~'), '.local', 'share')
    folder = os.path.join(base, 'history-vote')
    try:
        os.makedirs(folder, exist_ok=True)
    except OSError:
        folder = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'history-vote')
        os.makedirs(folder, exist_ok=True)
    return folder


def get_accounts_file() -> str:
    return os.path.join(get_history_folder(), 'accounts.env')


def get_history_file() -> str:
    return os.path.join(get_history_folder(), 'history.txt')


# ---------------------------------------------------------------------------
# Gestione account
# ---------------------------------------------------------------------------

def ensure_accounts_file_exists():
    path = get_accounts_file()
    if not os.path.exists(path):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(
                    '# Inserisci le tue credenziali qui sotto.\n'
                    'USERNAME=\n'
                    'PASSWORD=\n'
                )
            print(f'Creato file accounts.env in: {path}')
        except OSError as e:
            print(f'ERRORE: impossibile creare accounts.env — {e}')
            sys.exit(1)


def load_account() -> dict | None:
    ensure_accounts_file_exists()
    vals = dotenv_values(get_accounts_file())
    usr = (vals.get('USERNAME') or '').strip()
    pwd = (vals.get('PASSWORD') or '').strip()
    if not usr or not pwd:
        return None
    return {'username': usr, 'password': pwd}


def interactive_set_account():
    ensure_accounts_file_exists()
    print('Imposta le credenziali:')
    usr = input('  Username: ').strip()
    pwd = input('  Password: ').strip()
    if not usr or not pwd:
        print('Username o password vuoti. Credenziali non salvate.')
        return
    path = get_accounts_file()
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write('# Credenziali account.\n')
            f.write(f'USERNAME={usr}\n')
            f.write(f'PASSWORD={pwd}\n')
        print(f'Credenziali per "{usr}" salvate in: {path}')
    except OSError as e:
        print(f'ERRORE durante il salvataggio: {e}')


# ---------------------------------------------------------------------------
# Storico voti
# ---------------------------------------------------------------------------

def already_voted_today(username: str) -> bool:
    path = get_history_file()
    if not os.path.exists(path):
        return False
    today = datetime.now().strftime('%Y-%m-%d')
    prefix = f'{today} | {username} |'
    with open(path, 'r', encoding='utf-8') as f:
        return any(line.startswith(prefix) for line in f)


def log_vote(username: str, status: str):
    path = get_history_file()
    try:
        with open(path, 'a', encoding='utf-8') as f:
            ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'{ts[:10]} | {username} | {ts[11:]} - {status}\n')
    except OSError as e:
        print(f'ERRORE scrittura log: {e}')


# ---------------------------------------------------------------------------
# Selenium — rilevamento browser disponibile
# ---------------------------------------------------------------------------

def _detect_chromium_binary() -> str | None:
    """
    Cerca Chrome/Chromium in tutti i path comuni delle principali distro Linux.
    Supporta: Ubuntu, Debian, Fedora, Arch, openSUSE, Alpine, Snap, Flatpak.
    """
    import shutil
    candidates = [
        'google-chrome',
        'google-chrome-stable',
        'chromium',
        'chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/google-chrome-stable',
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/local/bin/chromium',
        # Snap
        '/snap/bin/chromium',
        '/snap/bin/google-chrome',
        # Flatpak wrapper (se presente nel PATH)
        'flatpak-spawn',
    ]
    for c in candidates:
        found = shutil.which(c) or (os.path.isfile(c) and c)
        if found:
            return found
    return None


def _get_chrome_service() -> Service:
    """
    Ordine di ricerca ChromeDriver su Linux:
    1. webdriver-manager (auto-download, gestisce anche Chromium)
    2. chromedriver nel PATH di sistema (apt/dnf/pacman)
    3. Bundle PyInstaller
    """
    import shutil

    chromium_bin = _detect_chromium_binary()

    # 1. webdriver-manager
    try:
        if chromium_bin and 'chromium' in chromium_bin.lower():
            os.environ.setdefault('WDM_LOCAL', '1')
        driver_path = ChromeDriverManager().install()
        return Service(driver_path)
    except Exception:
        pass

    # 2. PATH di sistema
    system_driver = shutil.which('chromedriver')
    if system_driver:
        return Service(system_driver)

    # 3. Bundle PyInstaller
    bundled = resource_path('chromedriver')
    if os.path.exists(bundled):
        os.chmod(bundled, 0o755)
        return Service(bundled)

    raise RuntimeError(
        'ChromeDriver non trovato.\n'
        'Installa Chrome o Chromium:\n'
        '  Ubuntu/Debian : sudo apt install chromium-browser\n'
        '  Fedora        : sudo dnf install chromium\n'
        '  Arch          : sudo pacman -S chromium\n'
        '  openSUSE      : sudo zypper install chromium\n'
        'Oppure scarica Google Chrome da https://www.google.com/chrome/'
    )


def _build_chrome_options() -> webdriver.ChromeOptions:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-notifications')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-dev-shm-usage')  # Fondamentale su Linux
    options.add_argument('--single-process')          # Più stabile in ambienti headless
    options.add_argument('--disable-extensions')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Se l'utente è root (es. Docker, CI), Chrome richiede questo flag
    if os.getuid() == 0:
        options.add_argument('--no-sandbox')

    # Punta al binario corretto se è Chromium
    chromium_bin = _detect_chromium_binary()
    if chromium_bin and 'chromium' in chromium_bin.lower():
        options.binary_location = chromium_bin

    return options


def perform_vote(username: str, password: str):
    options = _build_chrome_options()

    try:
        service = _get_chrome_service()
    except RuntimeError as e:
        print(str(e))
        log_vote(username, 'fallito - ChromeDriver non trovato')
        return

    try:
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        log_vote(username, f'fallito - Chrome non avviabile: {e}')
        return

    wait = WebDriverWait(driver, 15)

    try:
        driver.get(SITE_URL)

        # Accetta cookie
        try:
            consent_button = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button.fc-button.fc-cta-consent.fc-primary-button')
                )
            )
            consent_button.click()
        except TimeoutException:
            pass

        # Apre menu login
        try:
            login_menu_button = wait.until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'a.p-navgroup-link.p-navgroup-link--logIn')
                )
            )
            login_menu_button.click()
        except TimeoutException:
            log_vote(username, 'fallito - pulsante login non trovato')
            return

        # Compila form login
        try:
            username_input = wait.until(
                EC.presence_of_element_located((By.NAME, 'login'))
            )
            password_input = wait.until(
                EC.presence_of_element_located((By.NAME, 'password'))
            )
            username_input.clear()
            username_input.send_keys(username)
            password_input.clear()
            password_input.send_keys(password)

            enter_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//span[@class='button-text' and text()='Entra']")
                )
            )
            enter_button.click()

            wait.until_not(
                EC.presence_of_element_located((By.NAME, 'login'))
            )
        except TimeoutException:
            log_vote(username, 'fallito - errore login (timeout)')
            return

        # Vota
        driver.get(SERVER_URL)

        try:
            vote_button_plus_one = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'openVote'))
            )
            vote_button_plus_one.click()

            vote_button_confirm = wait.until(
                EC.element_to_be_clickable((By.ID, 'ho-votato'))
            )
            vote_button_confirm.click()
        except TimeoutException:
            log_vote(username, 'fallito - pulsante voto non trovato (timeout)')
            return

        log_vote(username, 'successo - voto registrato')
        print(f'[{datetime.now().strftime("%H:%M:%S")}] Voto registrato per {username}')

    except Exception as e:
        log_vote(username, f'fallito - {e}')

    finally:
        driver.quit()


# ---------------------------------------------------------------------------
# Loop principale
# ---------------------------------------------------------------------------

def run_loop():
    account = load_account()
    if not account:
        print('Nessun account configurato. Usa --set-credenziali.')
        sys.exit(1)

    print(f'Avviato loop per account: {account["username"]}')
    print(f'Controllo ogni {CHECK_INTERVAL // 60} minuti. Premi Ctrl+C per uscire.\n')

    while True:
        account = load_account()
        if account:
            usr = account['username']
            if already_voted_today(usr):
                print(f'[{datetime.now().strftime("%H:%M:%S")}] {usr} ha già votato oggi.')
            else:
                print(f'[{datetime.now().strftime("%H:%M:%S")}] Voto in corso per {usr}...')
                perform_vote(usr, account['password'])
        time.sleep(CHECK_INTERVAL)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Auto vote script per Minecraft-Italia (Linux).'
    )
    parser.add_argument('--set-credenziali', action='store_true',
                        help='Imposta username e password.')
    parser.add_argument('--once', action='store_true',
                        help='Esegue un solo ciclo ed esce.')
    args = parser.parse_args()

    ensure_accounts_file_exists()

    if args.set_credenziali:
        interactive_set_account()
        return

    if args.once:
        account = load_account()
        if not account:
            print('Nessun account configurato. Usa --set-credenziali.')
            return
        usr = account['username']
        if already_voted_today(usr):
            print(f'{usr} ha già votato oggi.')
        else:
            print(f'Voto in corso per {usr}...')
            perform_vote(usr, account['password'])
        return

    run_loop()


if __name__ == '__main__':
    main()