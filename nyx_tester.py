# nyx_tester.py — Test d'import et de structure des modules Nyxéos
# © 2025 Nicolas Deschênes

import os
import importlib.util
from datetime import datetime

MODULES_DIR = "."  # Tous les modules sont déjà dans ce dossier
JOURNAL_DIR = os.path.join("JOURNAL_DIR", "tester_log.txt")

MODULES_A_TESTER = [
    "nyxeos_updater",
    "nyxeos_ios_autoload",
    "nyxcore_sync",
    "nyx_rewriter",
    "nyx_guard",
    "nyx_patchfinder_ios",
    "cleanser"
]

def log(msg):
    now = datetime.now().strftime("[%Y-%m-%d %H:%M:%S']")
    ligne = f"{now} {msg}"
    print(ligne)
    try:
        with open(JOURNAL_DIR, "a", encoding="utf-8") as f:
            f.write(ligne + "\n")
    except Exception as e:
        print(f"[ERREUR] Journalisation impossible : {e}")

def tester_module(nom_fichier):
    path = os.path.join(MODULES_DIR, f"{nom_fichier}.py")
    if not os.path.exists(path):
        log(f"⛔ Introuvable : {nom_fichier}.py")
        return
    try:
        spec = importlib.util.spec_from_file_location(nom_fichier, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "main"):
            log(f"✓ Test OK : {nom_fichier} (main() présent)")
        else:
            log(f"⚠️ Test OK : {nom_fichier} (pas de main())")
    except Exception as e:
        log(f"❌ Erreur dans {nom_fichier} : {e}")

def main():
    log("=== Lancement de nyx_tester ===")
    for mod in MODULES_A_TESTER:
        tester_module(mod)
    log("=== Fin de nyx_tester ===")

if __name__ == "__main__":
    main()
