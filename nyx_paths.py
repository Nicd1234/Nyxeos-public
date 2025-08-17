# nyx_paths.py — version optimale combinée : détection, fallback, robustesse
import os
import socket

hostname = socket.gethostname()

# Détection du système
if "pi5" in hostname or "pironman" in hostname or hostname == "raspberrypi5":
    BASE_DIR_RAW = "/home/nic/nyxeos_pi5/nyxeos_pi"
    IS_PI5 = True
else:
    BASE_DIR_RAW = "/home/nicolas/nyxeos_pi"
    IS_PI5 = False

def test_or_fallback(path, fallback_root="~/nyxeos_fallback"):
    try:
        os.makedirs(path, exist_ok=True)
        testfile = os.path.join(path, ".testwrite")
        with open(testfile, "w") as f:
            f.write("ok")
        os.remove(testfile)
        return path
    except Exception as e:
        fallback = os.path.join(os.path.expanduser(fallback_root), os.path.relpath(path, BASE_DIR_RAW))
        os.makedirs(fallback, exist_ok=True)
        log_path = os.path.join(os.path.expanduser(fallback_root), "journal_fallback.txt")
        with open(log_path, "a") as log:
            log.write(f"Redirection de {path} vers {fallback} — Raison : {e}\n")
        return fallback

MODULES_DIR = test_or_fallback(os.path.join(BASE_DIR_RAW, "modules/"))
UPDATE_DIR = test_or_fallback(os.path.join(BASE_DIR_RAW, "update/"))
BACKUP_DIR = test_or_fallback(os.path.join(BASE_DIR_RAW, "backup/"))
JOURNAL_DIR = test_or_fallback(os.path.join(BASE_DIR_RAW, "journal/"))
SAFE_DIR = test_or_fallback(os.path.join(BASE_DIR_RAW, "nyxeos_safe/"))

# Synchronisation vers le Pi4 (utilisé uniquement par le Pi5)
DEST_PI4_DIR = "/home/nicolas/nyxeos_pi/modules/"
