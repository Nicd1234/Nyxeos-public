# cleanser.py — Nyxeos AutoCleanser v3.0
import os
import time
from nyx_paths import MODULES_DIR, UPDATE_DIR, SAFE_DIR

IGNORER = ["__init__.py", "nyxeos_updater.py"]

def fichier_est_inutile(fichier_path):
    try:
        if os.path.getsize(fichier_path) == 0:
            return True
        if "forcer_update" in fichier_path:
            return True
        return False
    except Exception:
        return True

def supprimer_doublons_et_fichiers_vides(dossier):
    fichiers_supprimes = 0
    fichiers_vus = set()

    for fichier in os.listdir(dossier):
        chemin_fichier = os.path.join(dossier, fichier)

        if os.path.isfile(chemin_fichier):
            if fichier in fichiers_vus or fichier_est_inutile(chemin_fichier):
                try:
                    os.remove(chemin_fichier)
                    print(f"[CLEAN] Supprimé : {fichier}")
                    fichiers_supprimes += 1
                except Exception as e:
                    print(f"[CLEAN] Erreur suppression {fichier} : {e}")
            else:
                fichiers_vus.add(fichier)

    return fichiers_supprimes

def main():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] === Cleanser lancé ===")
    total = 0

    for dossier in [UPDATE_DIR, MODULES_DIR, SAFE_DIR]:
        if os.path.exists(dossier):
            total += supprimer_doublons_et_fichiers_vides(dossier)
        else:
            print(f"[Cleanser] Dossier non trouvé : {dossier}")

    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] === Cleanser terminé : {total} fichiers supprimés ===")

if __name__ == "__main__":
    main()
