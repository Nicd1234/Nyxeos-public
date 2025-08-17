
# nyx_brain.py — Générateur adaptatif de modules correctifs avec noms logiques

import os
import datetime
from nyx_paths import JOURNAL_DIR, UPDATE_DIR
from pathlib import Path

def lire_logs():
    logs = {}
    for log_name in ["tester_log.txt", "rewriter_log.txt", "guard_log.txt", "patchfinder_log.txt"]:
        path = os.path.join(JOURNAL_DIR, log_name)
        if os.path.exists(path):
            with open(path, "r") as f:
                logs[log_name] = f.read()
        else:
            logs[log_name] = ""
    return logs

def analyser_besoins(logs):
    besoins = []
    for name, content in logs.items():
        if any(kw in content.lower() for kw in ["erreur", "module manquant", "non détecté", "risque", "lien détecté"]):
            base = name.replace("_log.txt", "").replace(".txt", "").replace("tester", "test").replace("patchfinder", "patch")
            nom_module = f"auto_{base}"
            besoins.append((name, nom_module))
    return besoins

def generer_module(nom):
    contenu = f"""# {nom}.py — Généré automatiquement par NyxBrain
def main():
    print("[{nom}] Module généré automatiquement à {datetime.datetime.now().isoformat()}")

if __name__ == "__main__":
    main()
"""
    chemin = os.path.join(UPDATE_DIR, f"{nom}.py")
    with open(chemin, "w") as f:
        f.write(contenu)
    return chemin

def consigner_fusion(source_log, module_genere):
    fusion_path = os.path.join(JOURNAL_DIR, "fusion_log.txt")
    with open(fusion_path, "a") as f:
        f.write(f"[{datetime.datetime.now()}] Fusion : {source_log} => {module_genere}\n")

def main():
    print("[NYXBRAIN] Activation en cours...")
    logs = lire_logs()
    besoins = analyser_besoins(logs)

    if besoins:
        for log, nom_module in besoins:
            chemin = generer_module(nom_module)
            consigner_fusion(log, chemin)
            print(f"[NYXBRAIN] ✅ Module généré : {chemin}")
    else:
        print("[NYXBRAIN] Aucun besoin évolutif détecté.")

if __name__ == "__main__":
    main()
