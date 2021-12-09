import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
import main
from xmlInOut.importXml import get_current_period

app = Flask(__name__)
port = 5000  # default
filename = ""
period = 1  # default

app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024  # max 1MB upload size
app.config["UPLOAD_EXTENSIONS"] = [".xml"]
app.config["UPLOAD_PATH"] = "src/data/"
app.config["SECRET_KEY"] = os.urandom(24).hex()  # random key


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/1_lastPeriod.html")
def lastPeriod():
    return render_template("1_lastPeriod.html", error=False, message=False)


@app.route("/1_lastPeriod.html", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        abort(400)
    uploaded_file = request.files["file"]
    filename = secure_filename(uploaded_file.filename)
    if filename == "":
        return render_template("1_lastPeriod.html", error=True, message=False)
    file_ext = os.path.splitext(filename)[1]
    if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
        abort(415)
    uploaded_file.save(os.path.join(app.config["UPLOAD_PATH"], filename))

    # Einlesen der XML files
    main.parse_all_xml()
    global period
    period = main.get_current_period()

    return render_template("1_lastPeriod.html", error=False, message=True)


@app.route("/2_salesPrediction.html")
def salesPrediction():
    # init database
    main.init_db()
    # Get default values
    sales = main.get_sales_forecast(period)

    return render_template(
        "2_salesPrediction.html", period=period,

        sales_P1_0=sales["P1"][0], sales_P1_1=sales["P1"][1], sales_P1_2=sales["P1"][2], sales_P1_3=sales["P1"][3],
        sales_P2_0=sales["P2"][0], sales_P2_1=sales["P2"][1], sales_P2_2=sales["P2"][2], sales_P2_3=sales["P2"][3],
        sales_P3_0=sales["P3"][0], sales_P3_1=sales["P3"][1], sales_P3_2=sales["P3"][2], sales_P3_3=sales["P3"][3],

        stock_P1_0=100, stock_P1_1=100, stock_P1_2=100, stock_P1_3=100,
        stock_P2_0=100, stock_P2_1=100, stock_P2_2=100, stock_P2_3=100,
        stock_P3_0=100, stock_P3_1=100, stock_P3_2=100, stock_P3_3=100
    )


@app.route("/2_salesPrediction.html", methods=["POST"])
def upload_prediction():
    salesData = [
        {
            'Periode': period,
            'Artikel': 'P1',
            'Aktuell_0': request.form.get('sales_P1_0'),
            'Aktuell_1': request.form.get('sales_P1_1'),
            'Aktuell_2': request.form.get('sales_P1_2'),
            'Aktuell_3': request.form.get('sales_P1_3'),
        },
        {
            'Periode': period,
            'Artikel': 'P2',
            'Aktuell_0': request.form.get('sales_P2_0'),
            'Aktuell_1': request.form.get('sales_P2_1'),
            'Aktuell_2': request.form.get('sales_P2_2'),
            'Aktuell_3': request.form.get('sales_P2_3'),
        },
        {
            'Periode': period,
            'Artikel': 'P3',
            'Aktuell_0': request.form.get('sales_P3_0'),
            'Aktuell_1': request.form.get('sales_P3_1'),
            'Aktuell_2': request.form.get('sales_P3_2'),
            'Aktuell_3': request.form.get('sales_P3_3'),
        },
    ]
    stockData = [
        {
            'Periode': period,
            'Artikel': 'P1',
            'Aktuell_0': request.form.get('stock_P1_0'),
            'Aktuell_1': request.form.get('stock_P1_1'),
            'Aktuell_2': request.form.get('stock_P1_2'),
            'Aktuell_3': request.form.get('stock_P1_3'),
        },
        {
            'Periode': period,
            'Artikel': 'P2',
            'Aktuell_0': request.form.get('stock_P2_0'),
            'Aktuell_1': request.form.get('stock_P2_1'),
            'Aktuell_2': request.form.get('stock_P2_2'),
            'Aktuell_3': request.form.get('stock_P2_3'),
        },
        {
            'Periode': period,
            'Artikel': 'P3',
            'Aktuell_0': request.form.get('stock_P3_0'),
            'Aktuell_1': request.form.get('stock_P3_1'),
            'Aktuell_2': request.form.get('stock_P3_2'),
            'Aktuell_3': request.form.get('stock_P3_3'),
        },
    ]
    # Absatzprognose in die DB schreiben
    # TODO: Lagerstrategie auch mit einbinden
    main.write_input_to_db(salesData, "Absatzprognose")
    print("Daten für Absatzprognose wurden in die Datenbank geschrieben")

    return render_template("3_stockPlaner.html", period=period)


@app.route("/3_stockPlaner.html")
def stockPlaner():
    return render_template(
        "3_stockPlaner.html", period=period,
        stock_P1_0=100, stock_P1_1=100, stock_P1_2=100, stock_P1_3=100,
        stock_P2_0=100, stock_P2_1=100, stock_P2_2=100, stock_P2_3=100,
        stock_P3_0=100, stock_P3_1=100, stock_P3_2=100, stock_P3_3=100
    )


@app.route("/3_stockPlaner.html", methods=["POST"])
def upload_plan():
    data = [
        {
            'Periode': period,
            'Artikel': 'P1',
            'Aktuell_0': request.form.get('stock_P1_0'),
            'Aktuell_1': request.form.get('stock_P1_1'),
            'Aktuell_2': request.form.get('stock_P1_2'),
            'Aktuell_3': request.form.get('stock_P1_3'),
        },
        {
            'Periode': period,
            'Artikel': 'P2',
            'Aktuell_0': request.form.get('stock_P2_0'),
            'Aktuell_1': request.form.get('stock_P2_1'),
            'Aktuell_2': request.form.get('stock_P2_2'),
            'Aktuell_3': request.form.get('stock_P2_3'),
        },
        {
            'Periode': period,
            'Artikel': 'P3',
            'Aktuell_0': request.form.get('stock_P3_0'),
            'Aktuell_1': request.form.get('stock_P3_1'),
            'Aktuell_2': request.form.get('stock_P3_2'),
            'Aktuell_3': request.form.get('stock_P3_3'),
        },
    ]
    print(data)
    # Lagerstrategie in die DB schreiben
    main.write_input_to_db(data, "Strategie_Lagerbestand")
    print("Daten für die Lagerbestand Strategie wurden in die Datenbank geschrieben")
    return render_template("4_productionSequence.html", period=period)


@app.route("/4_productionSequence.html")
def productionSequence():
    return render_template("4_productionSequence.html", period=period)


if __name__ == "__main__":
    # "debug" refreshes app every time a change is made
    app.run(debug=True, port=port)
