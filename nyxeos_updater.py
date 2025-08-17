
# nyxeos_updater.py — v9.5
# Mise à jour locale avec exécution et journalisation

import os
import shutil
import datetime
from nyx_paths import UPDATE_DIR, MODULES_DIR, BACKUP_DIR, JOURNAL_DIR

def mise_a_jour_module(nom_fichier):
    try:
        chemin_source = os.path.join(UPDATE_DIR, nom_fichier)
        chemin_cible = os.path.join(MODULES_DIR, nom_fichier)

        if not os.path.exists(chemin_source):
            return f"[UPDATER] Fichier absent : {chemin_source}"

        if os.path.exists(chemin_cible):
            os.makedirs(BACKUP_DIR, exist_ok=True)
            shutil.copy2(chemin_cible, os.path.join(BACKUP_DIR, nom_fichier))

        shutil.copy2(chemin_source, chemin_cible)
        return f"[UPDATER] ✅ Mis à jour : {nom_fichier}"

    except Exception as e:
        return f"[UPDATER] ❌ Erreur : {e}"

def executer_module(nom_fichier):
    try:
        module_path = os.path.join(MODULES_DIR, nom_fichier)
        with open(module_path, "r") as f:
            exec(f.read(), {})
        return f"[UPDATER] 🚀 Exécuté : {nom_fichier}"
    except Exception as e:
        return f"[UPDATER] ⚠️ Erreur d'exécution : {e}"

def main():
    print("[UPDATER] Démarrage de la mise à jour locale...")
    fichiers_update = [f for f in os.listdir(UPDATE_DIR) if f.endswith(".py") and f != "nyxeos_updater.py"]
    log_entries = []

    for fichier in fichiers_update:
        maj_msg = mise_a_jour_module(fichier)
        exe_msg = executer_module(fichier)
        log_entries.append(f"{maj_msg}\n{exe_msg}")

    log_path = os.path.join(JOURNAL_DIR, "updater_log.txt")
    with open(log_path, "a") as log_file:
        log_file.write(f"\n--- [{datetime.datetime.now()}] ---\n")
        for entry in log_entries:
            log_file.write(entry + "\n")

    print("[UPDATER] Mise à jour terminée.")

if __name__ == "__main__":
    main()
