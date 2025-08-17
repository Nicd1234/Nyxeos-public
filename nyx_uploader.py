from flask import Flask, request, render_template_string
import os

UPLOAD_FOLDER = '/home/nic/nyxeos_pi5/nyxeos_pi/update'
ALLOWED_EXTENSIONS = {'PUP'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_PAGE = """
<!doctype html>
<title>Uploader un fichier vers Nyxeos</title>
<h1>Choisir un fichier à transférer</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Uploader>
</form>
"""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].upper() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Aucun fichier détecté'
        file = request.files['file']
        if file.filename == '':
            return 'Aucun fichier sélectionné'
        if file and allowed_file(file.filename):
            filename = file.filename
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(save_path)
            return f'Fichier {filename} sauvegardé avec succès dans {UPLOAD_FOLDER}'
        else:
            return 'Extension de fichier non autorisée (seuls .PUP)'
    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
