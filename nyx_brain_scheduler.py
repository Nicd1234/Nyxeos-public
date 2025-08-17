# nyx_brain_scheduler.py — Planificateur interne des actions Nyxeos
import os
import time
import random
from nyx_paths import JOURNAL_DIR, MODULES_DIR

JOURNAL = os.path.join(JOURNAL_DIR, "scheduler_log.txt")

# Liste des tâches périodiques possibles
TACHES = [
    "generer_module_auto_guard",
    "generer_module_auto_patch",
    "verifier_etat_modules",
    "lancer_sync",
    "executer_cleanser",
    "lancer_fusion",
    "lancer_analyse_sources"
]

def consigner(msg):
    horodatage = time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open(JOURNAL, "a") as log:
        log.write(f"{horodatage} {msg}\n")

def executer_tache(tache):
    if tache == "generer_module_auto_guard":
        with open(os.path.join(MODULES_DIR, "auto_guard.py"), "w") as f:
            f.write("# module auto_guard généré par scheduler\n")
        consigner("Module auto_guard.py généré.")
    elif tache == "generer_module_auto_patch":
        with open(os.path.join(MODULES_DIR, "auto_patch.py"), "w") as f:
            f.write("# module auto_patch généré par scheduler\n")
        consigner("Module auto_patch.py généré.")
    elif tache == "verifier_etat_modules":
        fichiers = [f for f in os.listdir(MODULES_DIR) if f.endswith(".py")]
        consigner(f"Modules présents : {', '.join(fichiers)}")
    elif tache == "executer_cleanser":
        os.system(f"python3 {os.path.join(MODULES_DIR, 'cleanser.py')}")
        consigner("Module cleanser exécuté.")
    elif tache == "lancer_sync":
        os.system(f"python3 {os.path.join(MODULES_DIR, 'nyxcore_sync.py')}")
        consigner("Module nyxcore_sync exécuté.")
    elif tache == "lancer_fusion":
        os.system(f"python3 {os.path.join(MODULES_DIR, 'nyx_fusionneur.py')}")
        consigner("Fusionneur lancé.")
    elif tache == "lancer_analyse_sources":
        os.system(f"python3 {os.path.join(MODULES_DIR, 'nyxbrain_analyseur.py')}")
        consigner("Analyseur lancé.")

def main():
    tache = random.choice(TACHES)
    consigner(f"Tâche choisie : {tache}")
    executer_tache(tache)

if __name__ == "__main__":
    main()
