import flask
from zipfile import ZipFile

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    file_name = "zip.zip"
    with ZipFile(file_name, 'r') as zip:
        zip.printdir()
        zip.extractall()
app.run()