
import os
import subprocess
from datetime import datetime

# Configuration
LOCAL_BASE = os.path.expanduser("~/nyxeos_pi5/nyxeos_pi/")
LOCAL_MODULES = os.path.join(LOCAL_BASE, "modules")
REMOTE_USER = "nicolas"
REMOTE_IP = "192.168.0.46"
REMOTE_MODULES = f"/home/{REMOTE_USER}/nyxeos_pi5/nyxeos_pi/modules"
LOG_FILE = os.path.join(LOCAL_BASE, "journal", "monitor_log.txt")

def check_module(path, filename):
    try:
        subprocess.run(["python3", "-m", "py_compile", os.path.join(path, filename)],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL,
                       check=True)
        return "✅"
    except subprocess.CalledProcessError:
        return "❌"

def scan_local():
    print("🧠 [MONITOR] Scan local...")
    entries = []
    for file in os.listdir(LOCAL_MODULES):
        if file.endswith(".py") and not file.startswith("_"):
            status = check_module(LOCAL_MODULES, file)
            print(f"{status} {file[:-3]} (local)")
            entries.append(f"{status} {file} (local)")
    return entries

def scan_remote():
    print("🌐 [MONITOR] Scan distant sur Pi4...")
    try:
        result = subprocess.run([
            "ssh", f"{REMOTE_USER}@{REMOTE_IP}",
            f"ls {REMOTE_MODULES}/*.py"
        ], capture_output=True, text=True, check=True)

        files = result.stdout.strip().split("\n")
        entries = []
        for file in files:
            remote_check = subprocess.run([
                "ssh", f"{REMOTE_USER}@{REMOTE_IP}",
                f"python3 -m py_compile {file}"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            status = "✅" if remote_check.returncode == 0 else "❌"
            filename = os.path.basename(file)
            print(f"{status} {filename} (pi4)")
            entries.append(f"{status} {filename} (pi4)")
        return entries
    except subprocess.CalledProcessError:
        print("⚠️  Impossible d’accéder au Pi4.")
        return ["❌ Échec de connexion SSH au Pi4"]

def main():
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    all_entries = [f"\n{timestamp} - État des modules :"]
    all_entries.extend(scan_local())
    all_entries.extend(scan_remote())

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as log:
        log.write("\n".join(all_entries) + "\n")

if __name__ == "__main__":
    main()
