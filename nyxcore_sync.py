
# nyxcore_sync.py
# Version complète avec fonction main() explicite pour autoload

import os
import shutil
from datetime import datetime
import subprocess

MODULES_DIR = "/home/nic/nyxeos_pi5/nyxeos_pi/modules/"
UPDATE_DIR = "/home/nic/nyxeos_pi5/nyxeos_pi/update/"
DEST_PI4_DIR = "/home/nicolas/nyxeos_pi/modules/"
SYNC_LOG_PATH = "/home/nic/nyxeos_pi5/nyxeos_pi/journal/sync_log.txt"

def copier_modules_update_vers_modules():
    print("[SYNC] === Début de synchronisation locale ===")
    try:
        fichiers = [f for f in os.listdir(UPDATE_DIR) if f.endswith(".py")]
        copies = 0
        for f in fichiers:
            src = os.path.join(UPDATE_DIR, f)
            dst = os.path.join(MODULES_DIR, f)
            shutil.copy2(src, dst)
            print(f"[SYNC] Copié localement : {f}")
            copies += 1
        print(f"[SYNC] Copie terminée : {copies} fichiers déplacés.")
    except Exception as e:
        print(f"[SYNC] Erreur lors de la copie locale : {e}")

def synchroniser_vers_pi4():
    print("[SYNC] Tentative de synchronisation vers le Pi4...")
    try:
        subprocess.run(["ssh", "nicolas@192.168.0.46", "mkdir -p " + DEST_PI4_DIR], check=True)

        fichiers = [f for f in os.listdir(MODULES_DIR) if f.endswith(".py")]
        envoyes = 0
        for f in fichiers:
            local_file = os.path.join(MODULES_DIR, f)
            subprocess.run(["scp", local_file, f"nicolas@192.168.0.46:{DEST_PI4_DIR}"], check=True)
            print(f"[SYNC] Envoyé : {f}")
            envoyes += 1

        print(f"[SYNC] Modules envoyés au Pi4 : {envoyes} fichiers")
    except Exception as e:
        print(f"[SYNC] Erreur lors de la synchronisation SSH : {e}")

def log_sync(message):
    try:
        with open(SYNC_LOG_PATH, "a") as log:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            log.write(timestamp + message + "\n")
    except Exception as e:
        print(f"[SYNC] Journalisation échouée : {e}")

def main():
    copier_modules_update_vers_modules()
    synchroniser_vers_pi4()
    log_sync("Synchronisation complète exécutée via main()")

if __name__ == "__main__":
    main()
