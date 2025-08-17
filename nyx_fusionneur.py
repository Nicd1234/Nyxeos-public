
import os
from datetime import datetime
import sys

FUSION_LOG = "/home/nic/nyxeos_pi5/nyxeos_pi/journal/fusion_log.txt"
REFERENCES_DIR = "/home/nic/nyxeos_pi5/nyxeos_pi/references/"
MODULES_DIR = "/home/nic/nyxeos_pi5/nyxeos_pi/modules/"
UPDATE_DIR = "/home/nic/nyxeos_pi5/nyxeos_pi/update/"

os.makedirs(REFERENCES_DIR, exist_ok=True)
os.makedirs(UPDATE_DIR, exist_ok=True)

def charger_fichier(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()

def sauvegarder_fichier(path, lignes):
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lignes)

def fusionner_modules(module_local, module_externe):
    nom_module = os.path.basename(module_local)
    contenu_local = charger_fichier(module_local)
    contenu_externe = charger_fichier(module_externe)

    fusion = []
    log_diff = []

    max_len = max(len(contenu_local), len(contenu_externe))
    for i in range(max_len):
        ligne_locale = contenu_local[i] if i < len(contenu_local) else ""
        ligne_externe = contenu_externe[i] if i < len(contenu_externe) else ""

        if ligne_locale.strip() == ligne_externe.strip():
            fusion.append(ligne_locale)
        elif ligne_externe.strip() and not ligne_locale.strip():
            fusion.append(ligne_externe)
            log_diff.append(f"Ligne ajoutée de externe: {ligne_externe.strip()}")
        elif ligne_locale.strip() and not ligne_externe.strip():
            fusion.append(ligne_locale)
            log_diff.append(f"Ligne conservée de local: {ligne_locale.strip()}")
        else:
            fusion.append(ligne_externe)
            log_diff.append(f"Conflit, externe prioritaire: {ligne_externe.strip()}")

    path_fusion = os.path.join(UPDATE_DIR, nom_module)
    sauvegarder_fichier(path_fusion, fusion)

    log_texte = f"\n=== Fusion: {nom_module} ===\nDate: {datetime.now()}\n"
    log_texte += "\n".join(log_diff) + "\n"
    with open(FUSION_LOG, "a", encoding="utf-8") as f:
        f.write(log_texte)

    print(f"[Fusionneur] Fusion terminée : {nom_module}")
    print(f"[Fusionneur] Résultat : {path_fusion}")
    print(f"[Fusionneur] Journal mis à jour.")

def executer_fusion(nom_module):
    path_local = os.path.join(MODULES_DIR, nom_module)
    path_externe = os.path.join(REFERENCES_DIR, nom_module)

    if not os.path.exists(path_local):
        print(f"[Erreur] Fichier local manquant : {nom_module}")
        return
    if not os.path.exists(path_externe):
        print(f"[Erreur] Fichier externe manquant dans /references : {nom_module}")
        return

    fusionner_modules(path_local, path_externe)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        executer_fusion(sys.argv[1])
    else:
        print("[Erreur] Aucun nom de module fourni.")
