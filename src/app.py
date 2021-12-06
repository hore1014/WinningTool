import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)
port = 5000  # default

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.xml']
app.config['UPLOAD_PATH'] = 'src/data/'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/1_lastPeriod.html')
def lastPeriod():
    return render_template('1_lastPeriod.html')


@app.route('/1_lastPeriod.html', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        print(
            f"File '{filename}' uploaded to {os.path.join(app.config['UPLOAD_PATH'], filename)}")
        return redirect(url_for('salesPrediction'))
    else:
        return redirect(url_for('lastPeriod'))


@app.route('/2_salesPrediction.html')
def salesPrediction():
    return render_template('2_salesPrediction.html')


if __name__ == "__main__":
    # "debug" refreshes app every time a change is made
    app.run(debug=True, port=port)
