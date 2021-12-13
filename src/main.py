import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
from . import handler
from .handler import lookupArticles
from .procurement import lookupProcurement
#from database import lookupArticles

app = Flask(__name__)
port = 5000  # default
filename = ""
period = 1  # default
stock_P1 = 0
stock_P2 = 0
stock_P3 = 0
sequence = []
k_list = lookupArticles.k_list

# TODO Get this values from user input (use a dict)
language = "ru"


app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024  # max 1MB upload size
app.config["UPLOAD_EXTENSIONS"] = [".xml"]
app.config["UPLOAD_PATH"] = "src/data/"
app.config["SECRET_KEY"] = os.urandom(24).hex()  # random key


@app.route("/")
def home():
    return render_template(f"{language}/index.html")


@app.route("/", methods=["POST"])
def reset():
    handler.delete_all_xml()
    return render_template(f"{language}/index.html")


@app.route("/1_lastPeriod.html")
def lastPeriod():
    return render_template(f"{language}/1_lastPeriod.html", error=False, message=False)


@app.route("/1_lastPeriod.html", methods=["POST"])
def upload_file():
    dataOverwritten = False  # default

    if "file" not in request.files:
        abort(400)
    uploaded_file = request.files["file"]
    filename = secure_filename(uploaded_file.filename)
    full_filename = os.path.join(app.config["UPLOAD_PATH"], filename)

    if filename == "":
        return render_template(f"{language}/1_lastPeriod.html", error=True, message=False)

    # Prüfen, ob es sich um ein xml file handelt
    file_ext = os.path.splitext(filename)[1]
    if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
        abort(415)

    # File im filesystem speichern
    # Wenn im data storage bereits ein file mit gleichem Namen wie das upload_file existiert
    # soll gekennzeichnet werden, dass es überschrieben wurde
    if os.path.exists(full_filename):
        dataOverwritten = True
    uploaded_file.save(full_filename)

    # Periode des Files bestimmen
    file_period = handler.get_period_by_file(full_filename)
    if file_period < 0:
        # File wieder löschen
        os.remove(full_filename)
        return render_template(f"{language}/1_lastPeriod.html", invalid=True, message=False)

    # Dateiname umbenennen für einheitliche Struktur, falls Name bereits existiert ggf. überschreiben
    new_filename = app.config["UPLOAD_PATH"] + \
        f'ergebnis_periode{file_period}.xml'

    if os.path.exists(new_filename):
        if full_filename != new_filename:
            os.remove(new_filename)
            dataOverwritten = True
    os.rename(src=full_filename, dst=new_filename)

    # Einlesen der XML files
    handler.parse_all_xml(app.config["UPLOAD_PATH"])
    global period
    period = handler.get_current_period()

    if dataOverwritten:
        return render_template(f"{language}/1_lastPeriod.html", error=False, message=True, overwrite=True, period=file_period)
    return render_template(f"{language}/1_lastPeriod.html", error=False, message=True, period=file_period)


@app.route("/2_salesPrediction.html")
def salesPrediction():
    # init database
    handler.init_db()
    # Get default values
    sales = handler.get_sales_forecast(period)
    # get inventory
    current_parts = handler.get_parts_inventory(period)

    return render_template(
        f"{language}/2_salesPrediction.html", period=period, inventory=current_parts,

        sales_P1_0=sales["P1"][0], sales_P1_1=sales["P1"][1], sales_P1_2=sales["P1"][2], sales_P1_3=sales["P1"][3],
        sales_P2_0=sales["P2"][0], sales_P2_1=sales["P2"][1], sales_P2_2=sales["P2"][2], sales_P2_3=sales["P2"][3],
        sales_P3_0=sales["P3"][0], sales_P3_1=sales["P3"][1], sales_P3_2=sales["P3"][2], sales_P3_3=sales["P3"][3],

        # default
        # stock_P1_0=100, stock_P1_1=100, stock_P1_2=100, stock_P1_3=100,
        # stock_P2_0=100, stock_P2_1=100, stock_P2_2=100, stock_P2_3=100,
        # stock_P3_0=100, stock_P3_1=100, stock_P3_2=100, stock_P3_3=100

        # test
        stock_P1_0=100, stock_P1_1=50, stock_P1_2=50, stock_P1_3=100,
        stock_P2_0=50, stock_P2_1=50, stock_P2_2=50, stock_P2_3=50,
        stock_P3_0=50, stock_P3_1=50, stock_P3_2=50, stock_P3_3=50

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
            'Aktuell_0': stock_P1,
            'Aktuell_1': request.form.get('stock_P1_1'),
            'Aktuell_2': request.form.get('stock_P1_2'),
            'Aktuell_3': request.form.get('stock_P1_3'),
        },
        {
            'Periode': period,
            'Artikel': 'P2',
            'Aktuell_0': stock_P2,
            'Aktuell_1': request.form.get('stock_P2_1'),
            'Aktuell_2': request.form.get('stock_P2_2'),
            'Aktuell_3': request.form.get('stock_P2_3'),
        },
        {
            'Periode': period,
            'Artikel': 'P3',
            'Aktuell_0': stock_P3,
            'Aktuell_1': request.form.get('stock_P3_1'),
            'Aktuell_2': request.form.get('stock_P3_2'),
            'Aktuell_3': request.form.get('stock_P3_3'),
        },
    ]
    # Daten in die DB schreiben
    handler.write_input_to_db(salesData, "Absatzprognose")
    print("Daten für Absatzprognose wurden in die Datenbank geschrieben")

    handler.write_input_to_db(stockData, "Strategie_Lagerbestand")
    print("Daten für die Lagerbestandstrategie der P-Teile wurden in die Datenbank geschrieben")

    # Daten für exportXml speichern
    for el in salesData:
        handler.xml_absatz.append(
            (el['Artikel'], el['Aktuell_0'])
        )

    return redirect(url_for('stock_planer'))


@app.route("/3_stockPlaner.html")
def stock_planer():
    stock_data = {"P1": stock_P1, "P2": stock_P2, "P3": stock_P3}
    current_parts = handler.get_parts_inventory(period)
    for article in lookupArticles.e_list:
        stock_data[article] = current_parts[article][0]

    prod_data = {"P1": 0, "P2": 0, "P3": 0}
    for article in lookupArticles.e_list:
        prod_data[article] = 0

    return render_template(f"{language}/3_stockPlaner.html", period=period, stock_data=stock_data, prod_data=prod_data)


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
    handler.write_input_to_db(result_data, "Strategie_Lagerbestand")
    print("Daten für die Lagerbestandstrategie der E-Teile wurden in die Datenbank geschrieben")

    # Produktionsdaten berechnen
    prod_data = handler.get_production()
    return render_template(f"{language}/3_stockPlaner.html", period=period, calculated=True, stock_data=stock_data, prod_data=prod_data)


@app.route("/4_productionSequence.html")
def production_sequence():
    global sequence
    sequence = ["E16", "E7", "E8", "E9", "E13", "E14", "E15", "E18", "E19", "E20", "E4", "E5", "E6", "E10",
                "E11", "E12", "E29", "E49", "E54", "E17", "E30", "E50", "E55", "E26", "E31", "E51", "E56", "P1", "P3", "P2"]
    production = handler.production

    handler.get_capacity()

    return render_template(f"{language}/4_productionSequence.html", period=period, len=len(sequence), sequence=sequence, production=production, results_list=[], error=False)


@app.route("/4_productionSequence.html", methods=["POST"])
def upload_Sequence():
    production = handler.production
    data = request.form.to_dict(flat=False)

    # check if aount of production orders is greater than 60
    if (len(data)-1 > 60):
        return render_template(f"{language}/4_productionSequence.html", period=period, len=len(sequence), sequence=sequence, production=production, results_list=[], error="limit")

    # check if products are missing
    if (len(data)-1 < len(production)):
        return render_template(f"{language}/4_productionSequence.html", period=period, len=len(sequence), sequence=sequence, production=production, results_list=[], error="keys")
    for article in production:
        if (article not in data.keys()):
            return render_template(f"{language}/4_productionSequence.html", period=period, len=len(sequence), sequence=sequence, production=production, results_list=[], error="keys")

    # check if sum of part orders is equal to calculated order
    for article, item in data.items():
        if (article == "results_list"):
            continue
        sum = 0
        for amount in item:
            sum += int(amount) if amount != "" else 0
        if (production[article]["sum"] != sum):
            print("Error detected!")
            return render_template(f"{language}/4_productionSequence.html", period=period, len=len(sequence), sequence=sequence, production=production, results_list=[], error="sum")

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
    handler.xml_produktion = results_list

    return redirect(url_for('procurement_planer'))


@app.route("/5_orders_purchase.html")
def procurement_planer():
    current_parts = handler.get_parts_inventory(period)
    # calculate forecasts and suggestion for orders
    forecasts = handler.get_consumption_forecast()
    orders = handler.get_orders()

    # TODO: ggf. im template die Schriftfarbe ändern, um Probleme hervorzuheben
    # TODO: Warnungen implementieren

    return render_template(
        f"{language}/5_orders_purchase.html",
        period=period,
        articles=lookupArticles.k_list,
        len=len(lookupArticles.k_list),
        discounts=lookupProcurement.discount_amount,
        delivery=lookupProcurement.delivery_days,
        inventory=current_parts,
        forecasts=forecasts,
        orders=orders)


@app.route("/5_orders_purchase.html", methods=["POST"])
def upload_orders():
    orders = []
    for article in lookupArticles.k_list:
        orders.append((  # tuple
            article,
            request.form.get(f"normal_{article}"),
            request.form.get(f"express_{article}")
        ))

    handler.xml_bestellungen = orders

    return render_template(f"{language}/index.html")
    # return render_template("6_capacity.html")


@app.route("/6_capacity.html")
def capacity_planer():
    return render_template(f"{language}/6_capacity.html")


@app.route("/6_capacity.html", methods=["POST"])
def upload_shifts():
    return render_template(f"{language}/index.html")
    # return render_template(f"{language}/7_financial.html")


@app.route("/7_financial.html")
def financial_planer():
    return render_template(f"{language}/7_financial.html")


@app.route("/7_financial.html", methods=["POST"])
def create_results():

    handler.write_to_xml()
    # TODO: XML runterladbar machen

    return render_template(f"{language}/index.html")
    # return render_template(f"{language}/8_finish.html")
