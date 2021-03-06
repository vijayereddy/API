import json
import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename, html
from zipfile import ZipFile

ALLOWED_EXTENSIONS = set(['zip'])
UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET'])
def fileFrontPage():
    return render_template('index.html')

@app.route('/uploadfile', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        resp = html.format('No file part in the request')
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = html.format('No file selected for uploading')
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filename = 'uploads/'+filename
        with ZipFile(filename, 'r') as zip:
            zip.extractall('extracted'+filename)
            path = 'extracted'+filename
            files = []
            for r, d, f in os.walk(path):
                for file in f:
                    if '.csv' or '.xlsx' or '.xls' in file:
                        files.append(os.path.join(r, file))
            resp = json.dumps(files)
        return resp
    else:
        resp = html.format('Allowed file type is zip only')
        return resp

if __name__ == "__main__":
    app.secret_key = '1234'
    app.run(port = 5001)