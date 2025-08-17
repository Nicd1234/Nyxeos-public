# nyxportal.py — Portail Flask Nyxeos
from flask import Flask, request, jsonify, render_template_string
import os
from nyx_paths import UPDATE_DIR, MODULES_DIR

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPDATE_DIR

HTML_TEMPLATE = """
<!doctype html>
<title>Nyxeos Portal</title>
<h1>Déposer un fichier .py pour mise à jour</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Téléverser>
</form>
<p>{{ message }}</p>
"""

@app.route("/", methods=["GET", "POST"])
def upload_file():
    message = ""
    if request.method == "POST":
        if "file" not in request.files:
            message = "Aucun fichier sélectionné."
        else:
            file = request.files["file"]
            if file.filename == "":
                message = "Nom de fichier vide."
            elif file:
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)
                message = f"Fichier reçu : {file.filename}"
    return render_template_string(HTML_TEMPLATE, message=message)

@app.route("/update", methods=["GET"])
def lister_updates():
    try:
        fichiers = [f for f in os.listdir(UPDATE_DIR) if f.endswith(".py")]
        return jsonify({"modules_disponibles": fichiers})
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500

@app.route("/exec/<module>", methods=["POST"])
def executer_module(module):
    chemin = os.path.join(MODULES_DIR, f"{module}.py")
    if not os.path.exists(chemin):
        return jsonify({"erreur": "Module introuvable."}), 404

    try:
        exec(open(chemin).read())
        return jsonify({"statut": f"{module} exécuté avec succès."})
    except Exception as e:
        return jsonify({"erreur_exec": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
