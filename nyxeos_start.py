
import os
import subprocess
from datetime import datetime

# Détection dynamique du chemin utilisateur
BASE_DIR = os.path.expanduser("~/nyxeos_pi5/nyxeos_pi/")
MODULES_DIR = os.path.join(BASE_DIR, "modules")
JOURNAL_DIR = os.path.join(BASE_DIR, "journal")

# Liste des modules à exécuter automatiquement
MODULES_AUTOLOAD = [
    "nyx_brain",
    "nyxeos_prime",
    "nyxeos_offline",
    "nyxeos_updater",
    "cleanser",
    "nyx_rewriter",
    "nyxcore_sync"
]

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    entry = f"{timestamp} {message}\n"
    os.makedirs(JOURNAL_DIR, exist_ok=True)
    with open(os.path.join(JOURNAL_DIR, "start_log.txt"), "a") as log_file:
        log_file.write(entry)
    print(entry.strip())

def start_module(module_name):
    path = os.path.join(MODULES_DIR, f"{module_name}.py")
    if os.path.isfile(path):
        try:
            subprocess.run(["python3", path], check=True)
            log(f"[Autoload] Module exécuté : {module_name}")
        except subprocess.CalledProcessError:
            log(f"[ERREUR] Échec du module : {module_name}")
    else:
        log(f"[ERREUR] Module introuvable : {module_name}")

def main():
    log("==== NYXÉOS iOS v8.9 DÉMARRÉ ====")
    log("Journal actif.")
    log("Modules à surveiller : " + ", ".join(MODULES_AUTOLOAD))
    for module in MODULES_AUTOLOAD:
        start_module(module)

    # Démarrage de NyxPortal (Flask) si présent
    nyxportal_path = os.path.join(MODULES_DIR, "nyxportal.py")
    if os.path.isfile(nyxportal_path):
        log("[START] Démarrage de nyxportal en arrière-plan...")
        subprocess.Popen(["python3", nyxportal_path])
    else:
        log("[ERREUR] nyxportal.py introuvable.")

if __name__ == "__main__":
    log("[START] Démarrage de Nyxeos via autoload...")
    main()
