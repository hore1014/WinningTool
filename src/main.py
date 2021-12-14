import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
from . import handler
from .handler import lookupArticles
from .procurement import lookupProcurement
# from database import lookupArticles

app = Flask(__name__)
port = 5000  # default
filename = ""
period = 1  # default
stock_P1 = 0
stock_P2 = 0
stock_P3 = 0
sequence = []
k_list = lookupArticles.k_list
stations = ["Station_1", "Station_2", "Station_3", "Station_4", "Station_5", "Station_6", "Station_7",
            "Station_8", "Station_9", "Station_10", "Station_11", "Station_12", "Station_13", "Station_14", "Station_15"]
header_list = ["P1", "P2", "P3", "E4", "E5", "E6", "E10", "E11", "E12", "E16",
               "E17", "E26", "E29", "E30", "E31", "E49", "E50", "E51", "E54", "E55", "E56"]
article_list = ["P1", "P2", "P3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12", "E13", "E14", "E15",
                "E16", "E17", "E18", "E19", "E20", "E26", "E29", "E30", "E31", "E49", "E50", "E51", "E54", "E55", "E56"]

languages = {
    "de": "de",
    "en": "en",
}
language = "de"  # default


app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024  # max 1MB upload size
app.config["UPLOAD_EXTENSIONS"] = [".xml"]
app.config["UPLOAD_PATH"] = "src/data/"
app.config["SECRET_KEY"] = os.urandom(24).hex()  # random key


@app.route("/")
def home():
    global language
    language = request.args.get("lang") if request.args.get(
        "lang") != None else language
    return render_template("/index.html", lang=language)


@app.route("/", methods=["POST"])
def update():
    # global language
    # language = request.form.get('lang')
    # print(f"main: language")
    # handler.delete_all_xml()

    return redirect(url_for('lastPeriod') + f"?lang={language}")


@app.route("/1_lastPeriod")
def lastPeriod():
    args = request.args
    language = args.get("lang")
    return render_template("/1_lastPeriod.html", error=False, message=False, lang=language)


@app.route("/1_lastPeriod", methods=["POST"])
def upload_file():
    dataOverwritten = False  # default

    if "file" not in request.files:
        abort(400)
    uploaded_file = request.files["file"]
    filename = secure_filename(uploaded_file.filename)
    full_filename = os.path.join(app.config["UPLOAD_PATH"], filename)

    if filename == "":
        return render_template("/1_lastPeriod.html", error=True, message=False, lang=language)

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
        return render_template("/1_lastPeriod.html", invalid=True, message=False)

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
        return render_template("/1_lastPeriod.html", error=False, message=True, overwrite=True, period=file_period, lang=language)
    return render_template("/1_lastPeriod.html", error=False, message=True, period=file_period, lang=language)


@app.route("/2_salesPrediction")
def salesPrediction():
    args = request.args
    language = args.get("lang")
    # init database
    handler.init_db()
    # Get default values
    sales = handler.get_sales_forecast(period)
    # get inventory
    current_parts = handler.get_parts_inventory(period)
    all_parts = handler.lookupArticles.p_e_k_list

    return render_template(
        "/2_salesPrediction.html", lang=language, period=period, inventory=current_parts, all_parts=all_parts, len=len(all_parts),

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


@app.route("/2_salesPrediction", methods=["POST"])
def upload_prediction():
    args = request.args
    language = args.get("lang")
    global stock_P1
    global stock_P2
    global stock_P3
    stock_P1 = request.form.get('stock_P1_0')
    stock_P2 = request.form.get('stock_P2_0')
    stock_P3 = request.form.get('stock_P3_0')

    # sales predictions
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

    # users strategy for P-parts inventory
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

    # trading data
    tradeData = {}
    tradeData_db = []  # list of dicts for db
    for article in handler.lookupArticles.p_e_k_list:
        if (article not in ["P1", "P2", "P3"]):
            buy = request.form.get('order_amount_' + article)
        else:
            buy = 0
        sell = request.form.get('sell_amount_' + article)
        price = request.form.get('price_' + article)
        if (article in ["P1", "P2", "P3"]):
            buy = 0
            penalty = request.form.get('penalty_' + article)
        else:
            buy = request.form.get('order_amount_' + article)
            penalty = 0

        if (buy != sell):
            tradeData_db.append({
                "Periode": period,
                "Artikel": article,
                "Direktkauf": buy,
                "Direktverkauf": sell,
                "Preis": price
            })

        tradeData[article] = (buy, sell, price, penalty)

    # Daten in die DB schreiben
    handler.write_input_to_db(salesData, "Absatzprognose")
    print("Daten für Absatzprognose wurden in die Datenbank geschrieben")

    handler.write_input_to_db(stockData, "Strategie_Lagerbestand")
    print("Daten für die Lagerbestandstrategie der P-Teile wurden in die Datenbank geschrieben")

    handler.write_input_to_db(tradeData_db, "Handel")
    print("Daten für den Handel wurden in die Datenbank geschrieben")

    # Daten für exportXml speichern
    for el in salesData:
        handler.xml_absatz.append(
            (el['Artikel'], el['Aktuell_0'])
        )

    for el in ['P1', 'P2', 'P3']:
        handler.xml_absatz_direkt.append((
            # article, sell-amount, price, penalty
            el, tradeData[el][1], tradeData[el][2], tradeData[el][3]
        ))

    return redirect(url_for('stock_planer') + f"?lang={language}")


@app.route("/3_stockPlaner")
def stock_planer():
    args = request.args
    language = args.get("lang")
    stock_data = {"P1": stock_P1, "P2": stock_P2, "P3": stock_P3}
    current_parts = handler.get_parts_inventory(period)
    for article in lookupArticles.e_list:
        stock_data[article] = current_parts[article][0]

    prod_data = {"P1": {}, "P2": {}, "P3": {}}
    for article in lookupArticles.e_list:
        prod_data[article] = {"sum": 0}

    print(handler.get_parts_processing(period))

    return render_template("/3_stockPlaner.html",
                           period=period,
                           stock_data=stock_data,
                           prod_data=prod_data,
                           articles=article_list,
                           headers=header_list,
                           len=len(article_list),
                           len_h=len(header_list),
                           processing=handler.get_parts_processing(period),
                           queued=handler.get_parts_in_queue(period),
                           missing=handler.get_missing_parts(period),
                           trade=handler.get_parts_trade(period),
                           lang=language)


@app.route("/3_stockPlaner", methods=["POST"])
def upload_plan():
    args = request.args
    language = args.get("lang")
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
    return render_template("/3_stockPlaner.html",
                           period=period,
                           calculated=True,
                           stock_data=stock_data,
                           prod_data=prod_data,
                           articles=article_list,
                           headers=header_list,
                           len=len(article_list),
                           len_h=len(header_list),
                           processing=handler.get_parts_processing(period),
                           queued=handler.get_parts_in_queue(period),
                           missing=handler.get_missing_parts(period),
                           trade=handler.get_parts_trade(period),
                           lang=language)


@ app.route("/4_productionSequence")
def production_sequence():
    args = request.args
    language = args.get("lang")
    global sequence
    sequence = ["E16", "E7", "E8", "E9", "E13", "E14", "E15", "E18", "E19", "E20", "E4", "E5", "E6", "E10",
                "E11", "E12", "E29", "E49", "E54", "E17", "E30", "E50", "E55", "E26", "E31", "E51", "E56", "P1", "P3", "P2"]
    production = handler.production

    handler.get_capacity()

    return render_template("/4_productionSequence.html",
                           period=period,
                           len=len(sequence),
                           sequence=sequence,
                           production=production,
                           results_list=[],
                           error=False,
                           lang=language)


@app.route("/4_productionSequence", methods=["POST"])
def upload_Sequence():
    args = request.args
    language = args.get("lang")
    production = handler.production
    data = request.form.to_dict(flat=False)

    # check if amount of production orders is greater than 60
    if (len(data)-1 > 60):
        return render_template("/4_productionSequence.html",
                               period=period,
                               len=len(sequence),
                               sequence=sequence,
                               production=production,
                               results_list=[],
                               error="limit",
                               lang=language)

    # check if products are missing
    if (len(data)-1 < len(production)):
        return render_template("/4_productionSequence.html",
                               period=period,
                               len=len(sequence),
                               sequence=sequence,
                               production=production,
                               results_list=[],
                               error="keys",
                               lang=language)
    for article in production:
        if (article not in data.keys()):
            return render_template("/4_productionSequence.html",
                                   period=period, len=len(sequence),
                                   sequence=sequence,
                                   production=production,
                                   results_list=[],
                                   error="keys",
                                   lang=language)

    # check if sum of part orders is equal to calculated order and if amount
    for article, item in data.items():
        if (article == "results_list"):
            continue
        sum = 0
        for amount in item:
            if (amount == "" or int(amount) < 0):
                continue
            sum += int(amount)
        if (production[article]["sum"] != sum):
            print("Error detected!")
            return render_template("/4_productionSequence.html",
                                   period=period,
                                   len=len(sequence),
                                   sequence=sequence,
                                   production=production,
                                   results_list=[],
                                   error="sum",
                                   lang=language)

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

    return redirect(url_for('procurement_planer') + f"?lang={language}")


@app.route("/5_orders_purchase")
def procurement_planer():
    args = request.args
    language = args.get("lang")
    current_parts = handler.get_parts_inventory(period)
    # calculate forecasts and suggestion for orders
    forecasts = handler.get_consumption_forecast()
    orders = handler.get_orders()

    # TODO: ggf. im template die Schriftfarbe ändern, um Probleme hervorzuheben
    # TODO: Warnungen implementieren

    return render_template(
        "/5_orders_purchase.html",
        period=period,
        articles=lookupArticles.k_list,
        len=len(lookupArticles.k_list),
        discounts=lookupProcurement.discount_amount,
        delivery=lookupProcurement.delivery_days,
        inventory=current_parts,
        forecasts=forecasts,
        orders=orders,
        lang=language)


@app.route("/5_orders_purchase", methods=["POST"])
def upload_orders():
    args = request.args
    language = args.get("lang")
    orders = []
    for article in lookupArticles.k_list:
        norm = request.form.get(f"normal_{article}")
        eil = request.form.get(f"express_{article}")
        if norm != '0':
            orders.append((  # tuple
                article,
                norm,
                5
            ))
        if eil != '0':
            orders.append((  # tuple
                article,
                eil,
                4
            ))

    handler.xml_bestellungen = orders

    return redirect(url_for('capacity_planer') + f"?lang={language}")


@app.route("/6_capacity")
def capacity_planer():
    args = request.args
    language = args.get("lang")
    capacity = handler.get_capacity()
    shifts = handler.get_shifts()
    article_list = ["P1", "P2", "P3"]
    article_list.extend(lookupArticles.e_list)

    return render_template(
        "/6_capacity.html",
        period=period,
        lang=language,
        len=len(stations),
        len_a=len(article_list),
        stations=stations,
        shifts=shifts,
        articles=article_list,
        capacity=capacity
    )


@app.route("/6_capacity", methods=["POST"])
def upload_shifts():
    args = request.args
    language = args.get("lang")
    shifts = []
    for station in stations:
        if station == "Station_5":
            continue
        shifts.append((  # tuple
            station.replace("Station_", ''),
            request.form.get(f"shift_{station}"),
            request.form.get(f"extra_minutes_{station}")
        ))

    handler.xml_stationen = shifts
    # TODO: Schichten in die DB einlesen bzw ins XML schreiben; Format: Tupel (Schichten, Extraminuten pro Tag)
    handler.write_to_xml()
    return redirect(url_for('xml_download') + f"?lang={language}")


@app.route("/download")
def xml_download():
    args = request.args
    language = args.get("lang")
    return render_template("/download.html", period=period, lang=language)


@app.route("/download", methods=["POST"])
def create_results():
    # if os.path.exists(f'src/static/xml/input_results.xml'):
    #     os.remove(f'src/static/xml/input_results.xml')

    # TODO: Erfolgsmeldung nach Buttonklick

    return render_template("/download.html", period=period, lang=language, success=True)
