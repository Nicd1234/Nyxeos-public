import os
import ast
import traceback
import json
import subprocess
from nyx_paths import MODULES_DIR, UPDATE_DIR

KNOWN_IMPORTS_PATH = os.path.join(UPDATE_DIR, "known_imports.json")

def charger_known_imports():
    if not os.path.exists(KNOWN_IMPORTS_PATH):
        return {}
    with open(KNOWN_IMPORTS_PATH, 'r') as f:
        return json.load(f)

def ajouter_import_manquant(contenu, fonctions_utilisées, known_imports):
    lignes = contenu.splitlines()
    nouvelles_lignes = []
    imports_ajoutés = set()
    fonctions_déjà_importées = set()

    for ligne in lignes:
        if ligne.startswith("import") or ligne.startswith("from"):
            for nom, instr in known_imports.items():
                if nom in ligne:
                    fonctions_déjà_importées.add(nom)

    for nom in fonctions_utilisées:
        if nom in known_imports and nom not in fonctions_déjà_importées and nom not in imports_ajoutés:
            nouvelles_lignes.append(known_imports[nom])
            imports_ajoutés.add(nom)

    return "\n".join(nouvelles_lignes + lignes)

def detecter_fonctions_utilisées(contenu):
    fonctions = set()
    for ligne in contenu.splitlines():
        for mot in ligne.strip().split():
            if "(" in mot:
                fonctions.add(mot.split("(")[0])
    return fonctions

def rewriter(nom_fichier):
    print(f"[REWRITER] Analyse de {nom_fichier}...")

    try:
        with open(nom_fichier, 'r') as f:
            contenu = f.read()

        if contenu.strip() == "":
            raise ValueError("Fichier vide.")

        try:
            ast.parse(contenu)
            print("[REWRITER] Fichier valide, pas de correction nécessaire.")
            return True
        except SyntaxError:
            print("[REWRITER] Erreur détectée, tentative de correction...")

        fonctions_utilisées = detecter_fonctions_utilisées(contenu)
        known_imports = charger_known_imports()
        contenu_corrige = ajouter_import_manquant(contenu, fonctions_utilisées, known_imports)

        lignes = contenu_corrige.splitlines()
        lignes_reindentees = []
        indent = 0
        for ligne in lignes:
            stripped = ligne.strip()
            if stripped.endswith(":") and not stripped.startswith("else"):
                lignes_reindentees.append("    " * indent + stripped)
                indent += 1
            elif stripped.startswith(("return", "print", "raise", "pass")):
                lignes_reindentees.append("    " * indent + stripped)
            elif stripped.startswith(("except", "elif", "else")):
                indent = max(0, indent - 1)
                lignes_reindentees.append("    " * indent + stripped)
                indent += 1
            else:
                lignes_reindentees.append("    " * indent + stripped)

        contenu_final = "\n".join(lignes_reindentees)

        ast.parse(contenu_final)

        nom_fichier_cible = os.path.join(UPDATE_DIR, os.path.basename(nom_fichier))
        with open(nom_fichier_cible, 'w') as f:
            f.write(contenu_final)

        print(f"[REWRITER] Correction réussie. Fichier sauvegardé dans : {nom_fichier_cible}")

        print("[REWRITER] Exécution du module corrigé...")
        subprocess.run(["python3", nom_fichier_cible])

        return True

    except Exception as e:
        print(f"[REWRITER] Échec de la réécriture : {e}")
        traceback.print_exc()
        return False

def main():
    print("[REWRITER] Aucun fichier cible défini dans le mode autoload.")
