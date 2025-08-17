
import os
import subprocess

# Configuration de la cible
PI4_USER = "nicolas"
PI4_IP = "192.168.0.46"
PI4_PATH = f"/home/{PI4_USER}/nyxeos_pi5/nyxeos_pi/"
SOURCE_PATH = "/home/nic/nyxeos_pi5/nyxeos_pi/"

def deploy():
    print("[DEPLOY] Déploiement de Nyxeos sur le Pi4...")

    # 1. Création du dossier distant
    subprocess.run(["ssh", f"{PI4_USER}@{PI4_IP}", f"mkdir -p {PI4_PATH}modules"])

    # 2. Copie des dossiers modules/ et update/
    print("[DEPLOY] Transfert des dossiers modules et update...")
    subprocess.run(["scp", "-r",
        os.path.join(SOURCE_PATH, "modules"),
        os.path.join(SOURCE_PATH, "update"),
        f"{PI4_USER}@{PI4_IP}:{PI4_PATH}"
    ])

    # 3. Copie des fichiers critiques situés dans modules/
    fichiers_critiques = [
        "nyxeos_ios_autoload.py",
        "nyxportal.py",
        "nyx_paths.py",
        "known_imports.json"
    ]

    print("[DEPLOY] Transfert des fichiers critiques dans /modules/...")
    for fichier in fichiers_critiques:
        chemin_fichier = os.path.join(SOURCE_PATH, "modules", fichier)
        subprocess.run(["scp", chemin_fichier, f"{PI4_USER}@{PI4_IP}:{PI4_PATH}modules/"])

    # 4. Lancement de nyxeos_start.py sur le Pi4
    print("[DEPLOY] Lancement de nyxeos_start.py sur le Pi4...")
    subprocess.run(["ssh", f"{PI4_USER}@{PI4_IP}",
        f"python3 {PI4_PATH}modules/nyxeos_start.py &"
    ])

    print("[DEPLOY] ✅ Nyxeos entièrement déployé et lancé sans mot de passe.")

if __name__ == "__main__":
    deploy()
