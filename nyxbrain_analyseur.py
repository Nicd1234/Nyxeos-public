
import os
import requests
import json
from datetime import datetime
from urllib.parse import urlparse

REFERENCES_DIR = "/home/nic/nyxeos_pi5/nyxeos_pi/references/"
SOURCE_LOG = "/home/nic/nyxeos_pi5/nyxeos_pi/journal/source_log.txt"
URLS_JSON = "/home/nic/nyxeos_pi5/nyxeos_pi/urls_sources.json"
FUSIONNEUR = "/home/nic/nyxeos_pi5/nyxeos_pi/modules/nyx_fusionneur.py"

os.makedirs(REFERENCES_DIR, exist_ok=True)
os.makedirs(os.path.dirname(SOURCE_LOG), exist_ok=True)

def telecharger_fichier(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        nom_fichier = os.path.basename(urlparse(url).path)
        chemin_complet = os.path.join(REFERENCES_DIR, nom_fichier)

        with open(chemin_complet, "w", encoding="utf-8") as f:
            f.write(response.text)

        with open(SOURCE_LOG, "a", encoding="utf-8") as log:
            log.write(f"{datetime.now()} | {nom_fichier} | {url}\n")

        print(f"[✓] Téléchargé : {nom_fichier}")
        return nom_fichier
    except Exception as e:
        print(f"[Ignoré] Fichier non valide ou vide : {url}")
        return None

def executer_fusion(nom_module):
    os.system(f"python3 {FUSIONNEUR} {nom_module}")

def analyser_sources():
    if not os.path.exists(URLS_JSON):
        print("[Erreur] urls_sources.json manquant : " + URLS_JSON)
        return

    with open(URLS_JSON, "r", encoding="utf-8") as f:
        urls = json.load(f)

    for url in urls:
        nom = telecharger_fichier(url)
        if nom:
            chemin_local = f"/home/nic/nyxeos_pi5/nyxeos_pi/modules/{nom}"
            if os.path.exists(chemin_local):
                print(f"[Fusion] Déclenchement pour : {nom}")
                executer_fusion(nom)

if __name__ == "__main__":
    analyser_sources()
