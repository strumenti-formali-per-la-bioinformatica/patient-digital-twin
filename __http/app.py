import os

from flask import Flask, render_template
from pathlib import Path
import signal
from subprocess import Popen, PIPE
from flask_cors import CORS

app = Flask(__name__, template_folder='template')
CORS(app)

@app.route('/')
def index():
    dir = str(Path('__http/template/index.html').parent.absolute())
    return render_template('index.html')

@app.route('/ras')
def ras():
    dir = str(Path('__http/template/ras.html').parent.absolute())
    return render_template('ras.html')

@app.route('/patient')
def patient():
    dir = str(Path('__http/template/patient.html').parent.absolute())
    return render_template('patient.html')

@app.route('/run/<command>')
def run(command):
    dir = str(Path('__twin/examples/' + command + '.py').parent.absolute())
    path = str(dir) + '/' + command + '.py'
    print(path)
    out = os.popen('python3.7 ' + path).read()
    return render_template('index.html')