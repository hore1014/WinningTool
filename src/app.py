import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
import main
from xmlInOut.importXml import get_current_period
from database import lookupArticles

app = Flask(__name__)
port = 5000  # default
filename = ""
period = 1  # default
stock_P1 = 0
stock_P2 = 0
stock_P3 = 0


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
    full_filename = os.path.join(app.config["UPLOAD_PATH"], filename)

    if filename == "":
        return render_template("1_lastPeriod.html", error=True, message=False)

    # Prüfen, ob es sich um ein xml file handelt
    file_ext = os.path.splitext(filename)[1]
    if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
        abort(415)
    uploaded_file.save(full_filename)

    # Periode des Files bestimmen
    file_period = main.get_period_by_file(full_filename)
    new_filename = app.config["UPLOAD_PATH"] + \
        f'ergebnis_periode{file_period}.xml'

    # Dateiname umbenennen für einheitliche Struktur, falls Name bereits existiert ggf. überschreiben
    dataOverwritten = False  # default
    if(os.path.exists(new_filename)):
        os.remove(new_filename)
        dataOverwritten = True
    os.rename(src=full_filename, dst=new_filename)

    # Einlesen der XML files
    main.parse_all_xml(app.config["UPLOAD_PATH"])
    global period
    period = main.get_current_period()

    if(dataOverwritten):
        return render_template("1_lastPeriod.html", error=False, message=True, overwrite=True, period=file_period)
    return render_template("1_lastPeriod.html", error=False, message=True, period=file_period)


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
    # TODO: zwei dicts statt der vielen Einzelwerte übergeben


@app.route("/2_salesPrediction.html", methods=["POST"])
def upload_prediction():
    global stock_P1
    global stock_P2
    global stock_P3
    stock_P1 = request.form.get('stock_P1_0')
    stock_P2 = request.form.get('stock_P2_0')
    stock_P3 = request.form.get('stock_P3_0')

    salesData = [
        {
            'Periode': period,
            'Artikel': 'P1',
            'Aktuell_0': stock_P1,
            'Aktuell_1': request.form.get('sales_P1_1'),
            'Aktuell_2': request.form.get('sales_P1_2'),
            'Aktuell_3': request.form.get('sales_P1_3'),
        },
        {
            'Periode': period,
            'Artikel': 'P2',
            'Aktuell_0': stock_P2,
            'Aktuell_1': request.form.get('sales_P2_1'),
            'Aktuell_2': request.form.get('sales_P2_2'),
            'Aktuell_3': request.form.get('sales_P2_3'),
        },
        {
            'Periode': period,
            'Artikel': 'P3',
            'Aktuell_0': stock_P3,
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
    # Daten in die DB schreiben
    main.write_input_to_db(salesData, "Absatzprognose")
    print("Daten für Absatzprognose wurden in die Datenbank geschrieben")

    main.write_input_to_db(stockData, "Strategie_Lagerbestand")
    print("Daten für die Lagerbestandstrategie der P-Teile wurden in die Datenbank geschrieben")
    return redirect(url_for('stock_planer'))


@app.route("/3_stockPlaner.html")
def stock_planer():
    # TODO: hier vielleicht noch eine Funktion, die die Angaben aus der letzten Periode als Startwerte setzt
    stock_data = {"P1": stock_P1, "P2": stock_P2, "P3": stock_P3}
    for article in lookupArticles.e_list:
        stock_data[article] = 100

    prod_data = {"P1": 0, "P2": 0, "P3": 0}
    for article in lookupArticles.e_list:
        prod_data[article] = 0

    print(stock_data)
    return render_template("3_stockPlaner.html", period=period, stock_data=stock_data, prod_data=prod_data)


@app.route("/3_stockPlaner.html", methods=["POST"])
def upload_plan():
    stock_data = {"P1": stock_P1, "P2": stock_P2, "P3": stock_P3}
    result_data = []
    # User Eingaben für Planlagerbestand einlesen
    for article in lookupArticles.e_list:
        stock_data[article] = request.form.get(f'stock_{article}')
        result_data.append({
            'Periode': period,
            'Artikel': article,
            'Aktuell_0': request.form.get(f'stock_{article}'),
            'Aktuell_1': 0,
            'Aktuell_2': 0,
            'Aktuell_3': 0
        })

    # Daten in die DB schreiben
    main.write_input_to_db(result_data, "Strategie_Lagerbestand")
    print("Daten für die Lagerbestandstrategie der E-Teile wurden in die Datenbank geschrieben")

    # Produktionsdaten berechnen
    prod_data = main.get_production()

    return render_template("3_stockPlaner.html", period=period, calculated=True, stock_data=stock_data, prod_data=prod_data)


@app.route("/4_productionSequence.html")
def production_sequence():
    production = main.production

    return render_template("4_productionSequence.html", period=period, production=production)


@app.route("/4_productionSequence.html", methods=["POST"])
def upload_Sequence():
    return render_template("4_productionSequence.html", period=period)


if __name__ == "__main__":
    # "debug" refreshes app every time a change is made
    app.run(debug=True, port=port)
