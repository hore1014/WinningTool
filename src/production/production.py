from production import lookupProdDemand as pd

# defining the sequence for the calculation from top to bottom, most complex products first
calculation_sequence = ["P1", "P2", "P3", "E26", "E31", "E51", "E56", "E16", "E17", "E30", "E50", "E55", "E4",
                        "E5", "E6", "E10", "E11", "E12", "E29", "E49", "E54", "E7", "E8", "E9", "E13", "E14", "E15", "E18", "E19", "E20"]


def calculate_production(sales, current, planned, processing, queued, trade):
    results = {"P1": 0, "P2": 0, "P3": 0, "E4": 0, "E5": 0, "E6": 0, "E7": 0, "E8": 0, "E9": 0, "E10": 0, "E11": 0, "E12": 0, "E13": 0, "E14": 0, "E15": 0,
               "E16": 0, "E17": 0, "E18": 0, "E19": 0, "E20": 0, "E26": 0, "E29": 0, "E30": 0, "E31": 0, "E49": 0, "E50": 0, "E51": 0, "E54": 0, "E55": 0, "E56": 0}

    for article in calculation_sequence:
        production = 0
        # for every part look up the parts that need this specific part and the amount of it to get assembled
        for key in pd.production_demand[article]:
            production += results[key] * pd.production_demand[article][key]

        # add and substract all the factors to determine the amount that needs to be produced
        results[article] = sales[article][0] + production + planned[article] - \
            current[article] - processing[article] - \
            queued[article] - trade[article]

    return results
