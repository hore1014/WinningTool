from . import lookupProdDemand as pd

# defining the sequence for the calculation from top to bottom, most complex products first
calculation_sequence = ["P1", "P2", "P3", "E26", "E31", "E51", "E56", "E16", "E17", "E30", "E50", "E55", "E4",
                        "E5", "E6", "E10", "E11", "E12", "E29", "E49", "E54", "E7", "E8", "E9", "E13", "E14", "E15", "E18", "E19", "E20"]


def calculate_production(sales, current, planned, processing, missing, queued, trade):
    results = {"P1": {}, "P2": {}, "P3": {}, "E4": {}, "E5": {}, "E6": {}, "E7": {}, "E8": {}, "E9": {}, "E10": {}, "E11": {}, "E12": {}, "E13": {}, "E14": {}, "E15": {},
               "E16": {}, "E17": {}, "E18": {}, "E19": {}, "E20": {}, "E26": {}, "E29": {}, "E30": {}, "E31": {}, "E49": {}, "E50": {}, "E51": {}, "E54": {}, "E55": {}, "E56": {}}

    for article in calculation_sequence:
        # print(f"\nArtikel {article}:")
        production = 0
        processing_article = processing[article] if article in processing else 0
        queued_article = queued[article] if article in queued else 0
        missing_article = missing[article] if article in missing else 0
        purchase_article = trade[article][0] if article in trade else 0
        sell_article = trade[article][1] if article in trade else 0
        # for every part look up the parts that need this specific part and the amount of it to get assembled
        for key in pd.production_demand[article]:
            results[article][key] = results[key]["sum"] * pd.production_demand[article][key] if key not in results[article] else (
                results[article][key] + results[key]["sum"]) * pd.production_demand[article][key]
            # print(f"Steckt in {key}: {results[key]['sum']} * {pd.production_demand[article][key]} = {results[article][key]}")
            production += results[key]["sum"] * \
                pd.production_demand[article][key]

        # add and substract all the factors to determine the amount that needs to be produced
        if article in ["P1", "P2", "P3"]:
            results[article]["sum"] = \
                sales[article][0] + \
                production + \
                planned[article][0] - \
                current[article][0] - \
                processing_article - \
                queued_article - \
                missing_article - \
                purchase_article + \
                sell_article
            print(f"{sales[article][0]} + {production} + {planned[article][0]} - {current[article][0]} - {processing_article} - {queued_article} - {missing_article} - {purchase_article} + {sell_article} = {results[article]['sum']}")
        else:
            results[article]["sum"] = \
                production + \
                planned[article][0] - \
                current[article][0] - \
                processing_article - \
                queued_article - \
                missing_article - \
                purchase_article + \
                sell_article
            print(
                f"{production} + {planned[article][0]} - {current[article][0]} - {processing_article} - {queued_article} - {missing_article} - {purchase_article} + {sell_article} = {results[article]['sum']}")

    return results


def calculate_production_forecast(sales, planned, period):
    results = {"P1": {}, "P2": {}, "P3": {}, "E4": {}, "E5": {}, "E6": {}, "E7": {}, "E8": {}, "E9": {}, "E10": {}, "E11": {}, "E12": {}, "E13": {}, "E14": {}, "E15": {},
               "E16": {}, "E17": {}, "E18": {}, "E19": {}, "E20": {}, "E26": {}, "E29": {}, "E30": {}, "E31": {}, "E49": {}, "E50": {}, "E51": {}, "E54": {}, "E55": {}, "E56": {}}

    for article in calculation_sequence:
        production = 0
        # for every part look up the parts that need this specific part and the amount of it to get assembled
        for key in pd.production_demand[article]:
            production += results[key]["sum"] * \
                pd.production_demand[article][key]

        # add and substract all the factors to determine the amount that needs to be produced
        if article in ["P1", "P2", "P3"]:
            results[article]["sum"] = sales[article][period] + \
                production + planned[article][period] - \
                planned[article][period-1]
        else:
            results[article]["sum"] = production

    return results
