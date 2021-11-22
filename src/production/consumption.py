from production import lookupProdDemand as pd


def calculate_consumption(demand, sales):
    results = {"P1": 0, "P2": 0, "P3": 0, "E4": 0, "E5": 0, "E6": 0, "E7": 0, "E8": 0, "E9": 0, "E10": 0, "E11": 0, "E12": 0, "E13": 0, "E14": 0, "E15": 0,
               "E16": 0, "E17": 0, "E18": 0, "E19": 0, "E20": 0, "K21": 0, "K22": 0, "K23": 0, "K24": 0, "K25": 0, "E26": 0, "K27": 0, "K28": 0, "E29": 0, "E30": 0,
               "E31": 0, "K32": 0, "K33": 0, "K34": 0, "K35": 0, "K36": 0, "K37": 0, "K38": 0, "K39": 0, "K40": 0, "K41": 0, "K42": 0, "K43": 0, "K44": 0, "K45": 0,
               "K46": 0, "K47": 0, "K48": 0, "E49": 0, "E50": 0, "E51": 0, "K52": 0, "K53": 0, "E54": 0, "E55": 0, "E56": 0, "K57": 0, "K58": 0, "K59": 0, }

    for article in results:
        consumption = 0
        for key in pd.production_demand[article]:
            consumption += demand[key] * pd.production_demand[article][key]
        results[article] = consumption + sales[article]

    return results
