
# deep_cleanser_forceur.py — Version locale sans dépendance externe

import os

def deep_cleanser(root_dir="./"):
    log = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "forcer_update.py":
                filepath = os.path.join(dirpath, filename)
                try:
                    os.remove(filepath)
                    log.append(f"[DeepCleanser] Supprimé : {filepath}")
                except Exception as e:
                    log.append(f"[DeepCleanser] Échec suppression {filepath} : {e}")

    if not log:
        print("[DeepCleanser] Aucun fichier 'forcer_update.py' trouvé.")
    else:
        for entry in log:
            print(entry)
        print(f"[DeepCleanser] Nettoyage terminé. {len(log)} fichier(s) supprimé(s).")

if __name__ == "__main__":
    deep_cleanser("./")
