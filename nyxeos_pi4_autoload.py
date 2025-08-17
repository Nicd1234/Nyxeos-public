
# nyxeos_pi4_autoload.py
# Autoload dédié au Pi4 (Secondaire)
# © 2025 Nicolas Deschênes

import os
import time
import importlib
import traceback
import subprocess

MODULES_DIR = "/home/nicolas/nyxeos_pi/modules/"
REWRITER_PATH = os.path.join(MODULES_DIR, "nyx_rewriter.py")
MODULES_A_SURVEILLER = [
    "nyx_brain",            # cerveau secondaire
    "nyxeos_prime",         # config
    "nyxeos_offline",       # mode déconnecté
    "nyxeos_updater",       # mise à jour locale
    "cleanser",             # nettoyage
    "nyx_rewriter",         # correction
    "nyxcore_sync"          # synchronisation inverse
]

def charger_module(module_name):
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, 'main'):
            module.main()
            print(f"[Autoload Pi4] Module exécuté : {module_name}")
        else:
            print(f"[Autoload Pi4] Module {module_name} n'a pas de fonction main().")
    except Exception as e:
        print(f"[Autoload Pi4] Erreur dans {module_name} : {e}")
        try:
            module_path = os.path.join(MODULES_DIR, f"{module_name}.py")
            subprocess.run(["python3", REWRITER_PATH, module_path])
        except Exception as ex:
            print(f"[Autoload Pi4] Rewriter échoué pour {module_name} : {ex}")
            traceback.print_exc()

def main():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ==== NYXÉOS PI4 DÉMARRÉ ====")
    for module_name in MODULES_A_SURVEILLER:
        charger_module(module_name)

if __name__ == "__main__":
    main()
