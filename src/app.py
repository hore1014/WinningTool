import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
import main
from database import lookupArticles

app = Flask(__name__)
port = 5000  # default
filename = ""
period = 1  # default
stock_P1 = 0
stock_P2 = 0
stock_P3 = 0
sequence = []


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

    # File im filesystem speichern
    uploaded_file.save(full_filename)

    # Periode des Files bestimmen
    file_period = main.get_period_by_file(full_filename)
    if file_period < 0:
        # File wieder löschen
        os.remove(full_filename)
        return render_template("1_lastPeriod.html", invalid=True, message=False)


    # Dateiname umbenennen für einheitliche Struktur, falls Name bereits existiert ggf. überschreiben
    new_filename = app.config["UPLOAD_PATH"] + \
    f'ergebnis_periode{file_period}.xml'
    dataOverwritten = False  # default
    if os.path.exists(new_filename):
        if full_filename != new_filename:
            os.remove(new_filename)
        dataOverwritten = True
    os.rename(src=full_filename, dst=new_filename)

    # Einlesen der XML files
    main.parse_all_xml(app.config["UPLOAD_PATH"])
    global period
    period = main.get_current_period()

    if dataOverwritten:
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
    
    # Daten für exportXml speichern
    for el in salesData:
        main.xml_absatz.append(
            (el['Artikel'], el['Aktuell_0'])
        )

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
    global sequence
    sequence = ["E16", "E7", "E8", "E9", "E13", "E14", "E15", "E18", "E19", "E20", "E4", "E5", "E6", "E10",
                "E11", "E12", "E29", "E49", "E54", "E17", "E30", "E50", "E55", "E26", "E31", "E51", "E56", "P1", "P3", "P2"]
    production = main.production

    return render_template("4_productionSequence.html", period=period, len=len(sequence), sequence=sequence, production=production, results_list=[], error=False)


@app.route("/4_productionSequence.html", methods=["POST"])
def upload_Sequence():
    production = main.production
    data = request.form.to_dict(flat=False)

    # check if aount of production orders is greater than 60
    if (len(data)-1 > 60):
        return render_template("4_productionSequence.html", period=period, len=len(sequence), sequence=sequence, production=production, results_list=[], error="limit")

    # check if products are missing
    if (len(data)-1 < len(production)):
        return render_template("4_productionSequence.html", period=period, len=len(sequence), sequence=sequence, production=production, results_list=[], error="keys")
    for article in production:
        if (article not in data.keys()):
            return render_template("4_productionSequence.html", period=period, len=len(sequence), sequence=sequence, production=production, results_list=[], error="keys")

    # check if sum of part orders is equal to calculated order
    for article, item in data.items():
        if (article == "results_list"):
            continue
        sum = 0
        for amount in item:
            sum += int(amount) if amount != "" else 0
        if (production[article]["sum"] != sum):
            print("Error detected!")
            return render_template("4_productionSequence.html", period=period, len=len(sequence), sequence=sequence, production=production, results_list=[], error="sum")

    # get the items out while preserving the order
    results = request.form.get("results_list").split(",")
    article_temp = ""
    results_list = []
    for index, item in enumerate(results):
        if (index % 2 == 0):
            article_temp = item
        else:
            if item == "":
                continue
            results_list.append((article_temp, int(item)))

    # save data to exportXml
    main.xml_produktion = results_list
    
    # TODO: Das muss ganz am Ende passieren!
    main.write_to_xml()

    return render_template("index.html", period=period)


if __name__ == "__main__":
    # "debug=True" refreshes app every time a change is made, but Debugging is only possible for "debug=False"
    app.run(debug=True, port=port)
