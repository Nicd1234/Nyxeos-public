# nyx_instructor.py — Module d’apprentissage autonome pour guider la création de modules Nyxeos

import os
import time
from nyx_paths import JOURNAL_DIR, MODULES_DIR

JOURNAL = os.path.join(JOURNAL_DIR, "instructor_log.txt")
GUIDE_PATH = os.path.join(JOURNAL_DIR, "instructor_guide.txt")

def consigner(msg):
    horodatage = time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open(JOURNAL, "a") as log:
        log.write(f"{horodatage} {msg}\n")

def generer_guide():
    lignes = [
        "=== GUIDE DE CRÉATION DE MODULE NYXEOS ===",
        "- Nom du fichier : nyx_nom_du_module.py",
        "- Contenir une fonction `main()` ou `executer()`",
        "- Utiliser les chemins depuis nyx_paths (ex: MODULES_DIR, JOURNAL_DIR)",
        "- Journaliser chaque action importante",
        "- Toujours permettre une exécution autonome via `if __name__ == '__main__':`",
        "- Éviter les chemins codés en dur",
        "- Prioriser l'efficacité, la lisibilité, et la tolérance aux erreurs"
    ]
    with open(GUIDE_PATH, "w") as f:
        for ligne in lignes:
            f.write(ligne + "\n")
    consigner("Guide de création de module généré.")

def analyser_modules():
    fichiers = [f for f in os.listdir(MODULES_DIR) if f.endswith(".py")]
    modules_sans_main = []
    for fichier in fichiers:
        chemin = os.path.join(MODULES_DIR, fichier)
        with open(chemin, "r") as f:
            contenu = f.read()
            if "def main" not in contenu and "def executer" not in contenu:
                modules_sans_main.append(fichier)

    if modules_sans_main:
        consigner("Modules à corriger (aucune fonction main/executer) : " + ", ".join(modules_sans_main))
    else:
        consigner("Tous les modules analysés ont un point d'entrée.")

def main():
    consigner("=== Lancement de nyx_instructor ===")
    generer_guide()
    analyser_modules()
    consigner("=== Fin d’analyse ===")

if __name__ == "__main__":
    main()
