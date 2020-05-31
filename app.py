from flask import Flask, render_template, url_for, request, send_from_directory
import os
from map_excel import mapExcelMain
from manual_map import manualMapExcel

app = Flask(__name__)

app.config['MAX_CONTENT_PATH'] = 2*1024*1024


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        try:
            f = request.files.get('file')
            autoMapped = mapExcelMain(f)
            return autoMapped
        except:
            return 'Error'

@app.route('/savemap', methods = ['GET', 'POST'])
def manualMap():
    if request.method == 'POST':
        try:
            f = request.files.get('file')
            h = request.form['header']
            manualMapped = manualMapExcel(f, h)
            return manualMapped
        except:
            return 'Error'

if __name__ == '__main__':
    app.run()
