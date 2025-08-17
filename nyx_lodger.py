# nyx_logger.py — Agrégation et analyse des logs Nyxéos
# © 2025 Nicolas Deschênes

import os
import re
from datetime import datetime

JOURNAL_DIR = "JOURNAL_DIR"
LOG_FINAL = os.path.join(JOURNAL_DIR, "nyx_log_central.txt")

def extraire_date(ligne):
    match = re.match(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", ligne)
    if match:
        try:
            return datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
        except:
            return None
    return None

def scanner_logs():
    lignes = []
    modules_detectés = {}
    for fichier in os.listdir(JOURNAL_DIR):
        if fichier.endswith(".txt") and fichier != "nyx_log_central.txt":
            chemin = os.path.join(JOURNAL_DIR, fichier)
            with open(chemin, "r", encoding="utf-8") as f:
                for line in f:
                    date = extraire_date(line)
                    lignes.append((date, fichier, line.strip()))
                    module = fichier.replace("_log.txt", "")
                    if module not in modules_detectés:
                        modules_detectés[module] = 1
                    else:
                        modules_detectés[module] += 1
    return lignes, modules_detectés

def construire_log(lignes):
    lignes_valides = [l for l in lignes if l[0] is not None]
    lignes_valides.sort(key=lambda x: x[0])
    with open(LOG_FINAL, "w", encoding="utf-8") as out:
        for _, fichier, contenu in lignes_valides:
            out.write(f"{contenu}\n")

def afficher_résumé(lignes):
    total = len(lignes)
    erreurs = [l for l in lignes if "❌" in l[2] or "[ERREUR]" in l[2]]
    alertes = [l for l in lignes if "⚠️" in l[2]]
    succès = [l for l in lignes if "✓" in l[2]]
    print("\n=== Résumé des Journaux ===")
    print(f"Total de lignes : {total}")
    print(f"✓ Succès      : {len(succès)}")
    print(f"⚠️ Avertissements : {len(alertes)}")
    print(f"❌ Erreurs     : {len(erreurs)}")
    print("===========================\n")
    if erreurs:
        print("Erreurs récentes :")
        for e in erreurs[-5:]:
            print(" -", e[2])
    print("===========================\n")

def main():
    print("=== NYX LOGGER DÉMARRÉ ===")
    lignes, modules = scanner_logs()
    if not lignes:
        print("Aucun journal détecté.")
        return
    construire_log(lignes)
    afficher_résumé(lignes)
    print("Fichier central généré :", LOG_FINAL)
    print("=== NYX LOGGER TERMINÉ ===")

if __name__ == "__main__":
    main()
