# nyx_collector.py — Récupère automatiquement les fichiers générés par ChatGPT (/mnt/data/*.py)
import os
import shutil
from nyx_paths import UPDATE_DIR, JOURNAL_DIR

SOURCE_DIR = "/mnt/data"
LOG_PATH = os.path.join(JOURNAL_DIR, "collector_log.txt")

def consigner(msg):
    with open(LOG_PATH, "a") as log:
        log.write(msg + "\n")

def collecter_modules():
    fichiers = [f for f in os.listdir(SOURCE_DIR) if f.endswith(".py")]
    for fichier in fichiers:
        src = os.path.join(SOURCE_DIR, fichier)
        dst = os.path.join(UPDATE_DIR, fichier)
        try:
            shutil.copy2(src, dst)
            consigner(f"[COLLECTOR] Copié : {fichier}")
        except Exception as e:
            consigner(f"[COLLECTOR] Échec : {fichier} — {e}")

if __name__ == "__main__":
    collecter_modules()
