# nyx_sentinel.py — Détection d'anomalies système et modules corrompus
import os
import time
import hashlib
from nyx_paths import MODULES_DIR, JOURNAL_DIR

JOURNAL = os.path.join(JOURNAL_DIR, "sentinel_log.txt")
FICHIER_SIGNATURES = os.path.join(JOURNAL_DIR, "sentinel_signatures.txt")

def consigner(msg):
    horodatage = time.strftime("[%Y-%m-%d %H:%M:%S]")
    with open(JOURNAL, "a") as log:
        log.write(f"{horodatage} {msg}\n")

def calculer_hash(fichier):
    try:
        with open(fichier, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def charger_signatures():
    if not os.path.exists(FICHIER_SIGNATURES):
        return {}
    with open(FICHIER_SIGNATURES, "r") as f:
        lignes = f.readlines()
    signatures = {}
    for ligne in lignes:
        parts = ligne.strip().split("  ")
        if len(parts) == 2:
            signatures[parts[1]] = parts[0]
    return signatures

def enregistrer_signatures(signatures):
    with open(FICHIER_SIGNATURES, "w") as f:
        for nom, hash_val in signatures.items():
            f.write(f"{hash_val}  {nom}\n")

def verifier_modules():
    fichiers = [f for f in os.listdir(MODULES_DIR) if f.endswith(".py")]
    anciennes = charger_signatures()
    nouvelles = {}
    changements = []

    for fichier in fichiers:
        chemin = os.path.join(MODULES_DIR, fichier)
        hash_actuel = calculer_hash(chemin)
        nouvelles[fichier] = hash_actuel
        if fichier not in anciennes:
            changements.append(f"[NOUVEAU] {fichier}")
        elif anciennes[fichier] != hash_actuel:
            changements.append(f"[MODIFIÉ] {fichier}")

    for ancien in anciennes:
        if ancien not in nouvelles:
            changements.append(f"[SUPPRIMÉ] {ancien}")

    enregistrer_signatures(nouvelles)

    if changements:
        for ligne in changements:
            consigner(ligne)
    else:
        consigner("Aucun changement détecté.")

def main():
    consigner("=== Vérification Sentinel lancée ===")
    verifier_modules()
    consigner("=== Vérification terminée ===")

if __name__ == "__main__":
    main()
