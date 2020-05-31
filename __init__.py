from flask import Flask, render_template, url_for, request, send_from_directory
import os
from map_excel import mapExcelMain
from manual_map import manualMapExcel

app = Flask(__name__)

app.config['MAX_CONTENT_PATH'] = 2*1024*1024


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        try:
            print('Executing Python Script')
            for f in os.listdir('working'):
                os.remove('working/' + f)

            f = request.files.get('file')
            fileLocation = 'working/' + f.filename
            f.save(fileLocation)

            autoMapped = mapExcelMain(fileLocation)
            os.remove(fileLocation)

            return autoMapped

        except:
            return 'Error'

@app.route('/savemap', methods = ['GET', 'POST'])
def manualMap():
    if request.method == 'POST':
        try:
            print('Executing Python Script')
            for f in os.listdir('working'):
                os.remove('working/' + f)

            f = request.files.get('file')
            fileLocation = 'working/' + f.filename
            f.save(fileLocation)

            h = request.form['header']

            manualMapped = manualMapExcel(fileLocation, h)
            os.remove(fileLocation)

            return manualMapped

        except:
            return 'Error'

if __name__ == '__main__':
    app.run(debug=True)
