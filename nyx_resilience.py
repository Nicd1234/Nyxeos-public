# nyx_resilience.py — Module de restauration automatique post-crash de Nyxeos

import os
import shutil
import time
from nyx_paths import MODULES_DIR, BACKUP_DIR, JOURNAL_DIR

JOURNAL = os.path.join(JOURNAL_DIR, "resilience_log.txt")

def consigner(msg):
    horodatage = time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open(JOURNAL, "a") as log:
        log.write(f"{horodatage} {msg}\n")

def detecter_modules_vides():
    vides = []
    for fichier in os.listdir(MODULES_DIR):
        chemin = os.path.join(MODULES_DIR, fichier)
        if fichier.endswith(".py") and os.path.isfile(chemin) and os.path.getsize(chemin) == 0:
            vides.append(fichier)
    return vides

def restaurer_depuis_backup(fichier):
    # Recherche dans les sauvegardes récentes
    backups = sorted([d for d in os.listdir(BACKUP_DIR) if d.startswith("backup_")], reverse=True)
    for dossier in backups:
        chemin_backup = os.path.join(BACKUP_DIR, dossier, fichier)
        if os.path.exists(chemin_backup):
            shutil.copy2(chemin_backup, os.path.join(MODULES_DIR, fichier))
            consigner(f"[RESTAURATION] {fichier} restauré depuis {dossier}")
            return True
    consigner(f"[ÉCHEC] {fichier} non trouvé dans les sauvegardes")
    return False

def main():
    consigner("=== NyxResilience démarré ===")
    fichiers_vides = detecter_modules_vides()
    if not fichiers_vides:
        consigner("Aucun fichier vide détecté.")
    else:
        consigner(f"Fichiers vides détectés : {', '.join(fichiers_vides)}")
        for f in fichiers_vides:
            restaurer_depuis_backup(f)
    consigner("=== NyxResilience terminé ===")

if __name__ == "__main__":
    main()
