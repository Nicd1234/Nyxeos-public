
# nyx_patchfinder.py — Nettoyé pour éviter les faux positifs

from nyx_paths import MODULES_DIR, JOURNAL_DIR
import os

def verifier_patches_locaux():
    resultats = []
    for fichier in os.listdir(MODULES_DIR):
        chemin = os.path.join(MODULES_DIR, fichier)
        if os.path.isfile(chemin) and fichier.endswith(".py"):
            try:
                with open(chemin, "r", encoding="utf-8") as f:
                    contenu = f.read()
                if "http" in contenu:
                    resultats.append((fichier, "Lien détecté"))
            except Exception as e:
                resultats.append((fichier, f"Erreur: {e}"))
    log_path = os.path.join(JOURNAL_DIR, "patchfinder_log.txt")
    with open(log_path, "w") as log:
        for nom, info in resultats:
            log.write(f"{nom}: {info}\n")
    return resultats

if __name__ == "__main__":
    r = verifier_patches_locaux()
    if r:
        print("[NyxPatchFinder] Liaisons externes détectées :", r)
    else:
        print("[NyxPatchFinder] Aucun lien externe détecté.")
