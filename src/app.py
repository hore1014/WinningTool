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
    return redirect(url_for('stockPlaner'))


@app.route("/3_stockPlaner.html")
def stockPlaner():
    # TODO: hier vielleicht noch eine Funktion, die die Angaben aus der letzten Periode als Startwerte setzt
    return render_template(
        "3_stockPlaner.html", period=period,
        stock_P1=stock_P1, stock_P2=stock_P2, stock_P3=stock_P3,
        stock_E4=100, stock_E5=100, stock_E6=100, stock_E7=100, stock_E8=100,
        stock_E9=100, stock_E10=100, stock_E11=100, stock_E12=100, stock_E13=100,
        stock_E14=100, stock_E15=100, stock_E16=100, stock_E17=100, stock_E18=100,
        stock_E19=100, stock_E20=100, stock_E26=100, stock_E29=100, stock_E30=100,
        stock_E31=100, stock_E49=100, stock_E50=100, stock_E51=100, stock_E54=100,
        stock_E55=100, stock_E56=100
    )


@app.route("/3_stockPlaner.html", methods=["POST"])
def upload_plan():

    stock_data = []
    for article in lookupArticles.e_list:
        stock_data.append({
            'Periode': period,
            'Artikel': article,
            'Aktuell_0': request.form.get(f'stock_{article}'),
            'Aktuell_1': 0,
            'Aktuell_2': 0,
            'Aktuell_3': 0
        })

    # print(stock_data)
    # Daten in die DB schreiben
    main.write_input_to_db(stock_data, "Strategie_Lagerbestand")
    print("Daten für die Lagerbestandstrategie der E-Teile wurden in die Datenbank geschrieben")

    prod_data = main.get_production()

    return render_template(
        "3_stockPlaner.html", period=period,
        stock_P1=stock_P1, stock_P2=stock_P2, stock_P3=stock_P3,
        stock_E4=stock_data[0]["Aktuell_0"], stock_E5=stock_data[1]["Aktuell_0"], stock_E6=stock_data[2]["Aktuell_0"],
        stock_E7=stock_data[3]["Aktuell_0"], stock_E8=stock_data[4]["Aktuell_0"], stock_E9=stock_data[5]["Aktuell_0"],
        stock_E10=stock_data[6]["Aktuell_0"], stock_E11=stock_data[7]["Aktuell_0"], stock_E12=stock_data[8]["Aktuell_0"],
        stock_E13=stock_data[9]["Aktuell_0"], stock_E14=stock_data[10]["Aktuell_0"], stock_E15=stock_data[11]["Aktuell_0"],
        stock_E16=stock_data[12]["Aktuell_0"], stock_E17=stock_data[13]["Aktuell_0"], stock_E18=stock_data[14]["Aktuell_0"],
        stock_E19=stock_data[15]["Aktuell_0"], stock_E20=stock_data[16]["Aktuell_0"], stock_E26=stock_data[17]["Aktuell_0"],
        stock_E29=stock_data[18]["Aktuell_0"], stock_E30=stock_data[19]["Aktuell_0"], stock_E31=stock_data[20]["Aktuell_0"],
        stock_E49=stock_data[21]["Aktuell_0"], stock_E50=stock_data[22]["Aktuell_0"], stock_E51=stock_data[23]["Aktuell_0"],
        stock_E54=stock_data[24]["Aktuell_0"], stock_E55=stock_data[25]["Aktuell_0"], stock_E56=stock_data[26]["Aktuell_0"],
        production_P1=prod_data["P1"]["sum"], production_P2=prod_data["P2"]["sum"], production_P3=prod_data["P3"]["sum"],
        production_E4=prod_data["E4"]["sum"], production_E5=prod_data["E5"]["sum"], production_E6=prod_data["E6"]["sum"],
        production_E7=prod_data["E7"]["sum"], production_E8=prod_data["E8"]["sum"], production_E9=prod_data["E9"]["sum"],
        production_E10=prod_data["E10"]["sum"], production_E11=prod_data["E11"]["sum"], production_E12=prod_data["E12"]["sum"],
        production_E13=prod_data["E13"]["sum"], production_E14=prod_data["E14"]["sum"], production_E15=prod_data["E15"]["sum"],
        production_E16=prod_data["E16"]["sum"], production_E17=prod_data["E17"]["sum"], production_E18=prod_data["E18"]["sum"],
        production_E19=prod_data["E19"]["sum"], production_E20=prod_data["E20"]["sum"], production_E26=prod_data["E26"]["sum"],
        production_E29=prod_data["E29"]["sum"], production_E30=prod_data["E30"]["sum"], production_E31=prod_data["E31"]["sum"],
        production_E49=prod_data["E49"]["sum"], production_E50=prod_data["E50"]["sum"], production_E51=prod_data["E51"]["sum"],
        production_E54=prod_data["E54"]["sum"], production_E55=prod_data["E55"]["sum"], production_E56=prod_data["E56"]["sum"],
    )


@app.route("/4_productionSequence.html")
def productionSequence():
    return render_template("4_productionSequence.html", period=period)


if __name__ == "__main__":
    # "debug" refreshes app every time a change is made
    app.run(debug=True, port=port)
