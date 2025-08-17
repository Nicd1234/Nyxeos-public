
# nyx_guard.py — Version avec JOURNAL_DIR

from nyx_paths import MODULES_DIR, JOURNAL_DIR
import os

def verifier_securite_modules():
    erreurs = []
    for fichier in os.listdir(MODULES_DIR):
        chemin = os.path.join(MODULES_DIR, fichier)
        if os.path.isfile(chemin):
            try:
                with open(chemin, "r", encoding="utf-8") as f:
                    contenu = f.read()
                if "DROPBOX_TOKEN" in contenu or "dropbox.com" in contenu:
                    erreurs.append(fichier)
            except Exception as e:
                erreurs.append(f"{fichier} (erreur lecture: {e})")
    log_path = os.path.join(JOURNAL_DIR, "guard_log.txt")
    with open(log_path, "w") as log:
        for e in erreurs:
            log.write(f"[Risque] {e}\n")
    return erreurs

if __name__ == "__main__":
    problemes = verifier_securite_modules()
    if problemes:
        print("[NyxGuard] Problèmes détectés :", problemes)
    else:
        print("[NyxGuard] Aucun problème détecté.")
