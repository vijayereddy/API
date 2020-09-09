import flask
from flask import jsonify
import os
from zipfile import ZipFile

app = flask.Flask(__name__)
app.config["DEBUG"] = True
@app.route('/', methods=['GET'])
def home():
    path = 'extracted/'
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.csv' in file:
                files.append(os.path.join(r, file))
    return jsonify({'response':files})

file_name = "zip.zip"
with ZipFile(file_name, 'r') as zip:
    zip.extractall('extracted')

app.run()