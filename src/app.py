import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)
port = 5000  # default

app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024  # max 1MB upload size
app.config["UPLOAD_EXTENSIONS"] = [".xml"]
app.config["UPLOAD_PATH"] = "src/data/"
app.config["SECRET_KEY"] = os.urandom(24).hex()  # random key


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/1_lastPeriod.html")
def lastPeriod():
    return render_template("1_lastPeriod.html", error=False)


@app.route("/1_lastPeriod.html", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        abort(400)
    uploaded_file = request.files["file"]
    filename = secure_filename(uploaded_file.filename)
    if filename == "":
        return render_template("1_lastPeriod.html", error=True)
    file_ext = os.path.splitext(filename)[1]
    if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
        abort(415)
    uploaded_file.save(os.path.join(app.config["UPLOAD_PATH"], filename))
    # TODO: hier muss ggf. bereits veranlasst werden, dass die xml datei eingelesen wird
    return redirect(url_for("salesPrediction"))


@app.route("/2_salesPrediction.html")
def salesPrediction():
    return render_template("2_salesPrediction.html", sales_1_0=110, sales_1_1=100, sales_1_2=150, sales_1_3=200, sales_2_0=200, sales_2_1=150, sales_2_2=250, sales_2_3=100, sales_3_0=150, sales_3_1=50, sales_3_2=100, sales_3_3=250)


@app.route("/2_salesPrediction.html", methods=["POST"])
def upload_prediction():
    # TODO: Absatzprognose in die DB schreiben
    return render_template("3_stockPlaner.html")


@app.route("/3_stockPlaner.html")
def stockPlaner():
    return render_template("3_stockPlaner.html")


@app.route("/3_stockPlaner.html", methods=["POST"])
def upload_plan():
    # TODO: Lagerstrategie in die DB schreiben
    return render_template("4_productionSequence.html")


@app.route("/4_productionSequence.html")
def productionSequence():
    return render_template("4_productionSequence.html")


if __name__ == "__main__":
    # "debug" refreshes app every time a change is made
    app.run(debug=True, port=port)
