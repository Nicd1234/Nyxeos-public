# nyx_backupper.py — Sauvegarde intelligente des modules Nyxeos avec horodatage
import os
import shutil
import time
from nyx_paths import MODULES_DIR, BACKUP_DIR, JOURNAL_DIR

JOURNAL = os.path.join(JOURNAL_DIR, "backupper_log.txt")

def consigner(msg):
    horodatage = time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open(JOURNAL, "a") as log:
        log.write(f"{horodatage} {msg}\n")

def creer_sous_dossier_backup():
    horodatage = time.strftime("backup_%Y%m%d_%H%M%S")
    chemin = os.path.join(BACKUP_DIR, horodatage)
    os.makedirs(chemin, exist_ok=True)
    return chemin

def sauvegarder_modules():
    destination = creer_sous_dossier_backup()
    fichiers = [f for f in os.listdir(MODULES_DIR) if f.endswith(".py")]
    for fichier in fichiers:
        src = os.path.join(MODULES_DIR, fichier)
        dst = os.path.join(destination, fichier)
        try:
            shutil.copy2(src, dst)
            consigner(f"[SAUVEGARDE] {fichier} → {destination}")
        except Exception as e:
            consigner(f"[ÉCHEC] {fichier} — {e}")

def main():
    consigner("=== Début de la sauvegarde ===")
    sauvegarder_modules()
    consigner("=== Sauvegarde terminée ===")

if __name__ == "__main__":
    main()
