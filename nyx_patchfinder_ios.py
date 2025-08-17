# nyx_patchfinder_ios.py — Vérification des dépendances (sans subprocess)
# © 2025 Nicolas Deschênes

import os
from datetime import datetime

JOURNAL_DIR = os.path.join("JOURNAL_DIR", "patchfinder_log.txt")
if not os.path.exists(os.path.dirname(JOURNAL_DIR)):
    try:
        os.makedirs(os.path.dirname(JOURNAL_DIR))
    except:
        JOURNAL_DIR = "patchfinder_log.txt"  # fallback

DEPENDANCES = [
    "requests",
    "dropbox",
    "flask",
    "watchdog",  # Ne s’installe pas automatiquement sur iOS
    "pybluez"
]

manquants = []

def log(msg):
    now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    ligne = f"{now} {msg}"
    print(ligne)
    try:
        with open(JOURNAL_DIR, "a", encoding="utf-8") as f:
            f.write(ligne + "\n")
    except Exception as e:
        print(f"[ERREUR] Journal : {e}")

def verifier_modules():
    for lib in DEPENDANCES:
        try:
            __import__(lib)
            log(f"✓ Présent : {lib}")
        except ImportError:
            log(f"⛔ Absent : {lib} — à installer manuellement")
            manquants.append(lib)

if __name__ == "__main__":
    log("=== Vérification des dépendances (iOS) ===")
    verifier_modules()
    if manquants:
        log("Modules à installer manuellement : " + ", ".join(manquants))
    else:
        log("Toutes les dépendances sont présentes.")
    log("=== Fin patchfinder_ios ===")
