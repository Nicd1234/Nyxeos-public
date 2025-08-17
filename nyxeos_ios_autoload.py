# nyxeos_ios_autoload.py v9.0 — corrigé avec intégration du collector
# © 2025 Nicolas Deschênes

import os
import time
import importlib
import traceback
import subprocess
from nyx_paths import MODULES_DIR

# === Appel sécurisé de nyxbrain_analyseur ===
try:
    subprocess.Popen(["python3", os.path.join(MODULES_DIR, "nyxbrain_analyseur.py")])
    print("[Autoload] NyxBrain Analyseur lancé.")
except Exception as e:
    print(f"[Autoload] Erreur NyxBrain : {e}")

# === Intégration du collecteur des modules générés dans /mnt/data ===
try:
    subprocess.run(["python3", os.path.join(MODULES_DIR, "nyx_collector.py")], check=True)
    print("[Autoload] NyxCollector exécuté.")
except Exception as e:
    print(f"[Autoload] Erreur NyxCollector : {e}")

# === Modules à surveiller (avec ordre stratégique) ===
modules_a_surveille = [
    "nyx_brain",
    "nyxcore_sync",
    "nyxeos_updater",
    "nyxeos_prime",
    "nyxeos_offline",
    "cleanser",
    "nyx_rewriter"
]

REWRITER_PATH = os.path.join(MODULES_DIR, "nyx_rewriter.py")

def charger_module(module_name):
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, 'main'):
            module.main()
            print(f"[Autoload] Module exécuté : {module_name}")
        else:
            print(f"[Autoload] Module {module_name} n'a pas de fonction main() détectée.")
    except Exception as e:
        print(f"[Autoload] Erreur en chargeant {module_name} : {e}")
        print("[Autoload] Tentative de correction avec nyx_rewriter...")
        try:
            module_path = os.path.join(MODULES_DIR, f"{module_name}.py")
            subprocess.run(["python3", REWRITER_PATH, module_path])
        except Exception as ex:
            print(f"[Autoload] Échec du rewriter pour {module_name} : {ex}")
            traceback.print_exc()

def main():
    horodatage = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{horodatage}] ==== NYXÉOS iOS v9.0 DÉMARRÉ ====")
    print(f"[{horodatage}] Journal actif.")
    print(f"[{horodatage}] Modules à surveiller : {', '.join(modules_a_surveille)}")

    for module_name in modules_a_surveille:
        charger_module(module_name)

if __name__ == "__main__":
    main()
