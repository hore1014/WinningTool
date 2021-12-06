
def get_average_inventory_worth(current, production, consumption, processing, queued, missing, trade):
    results = {"P1": 0, "P2": 0, "P3": 0, "E4": 0, "E5": 0, "E6": 0, "E7": 0, "E8": 0, "E9": 0, "E10": 0, "E11": 0, "E12": 0, "E13": 0, "E14": 0, "E15": 0,
               "E16": 0, "E17": 0, "E18": 0, "E19": 0, "E20": 0, "K21": 0, "K22": 0, "K23": 0, "K24": 0, "K25": 0, "E26": 0, "K27": 0, "K28": 0, "E29": 0, "E30": 0,
               "E31": 0, "K32": 0, "K33": 0, "K34": 0, "K35": 0, "K36": 0, "K37": 0, "K38": 0, "K39": 0, "K40": 0, "K41": 0, "K42": 0, "K43": 0, "K44": 0, "K45": 0,
               "K46": 0, "K47": 0, "K48": 0, "E49": 0, "E50": 0, "E51": 0, "K52": 0, "K53": 0, "E54": 0, "E55": 0, "E56": 0, "K57": 0, "K58": 0, "K59": 0, }

    for key in results:
        production_article = production[key] if key in production else 0
        processing_article = processing[key] if key in processing else 0
        queued_article = queued[key] if key in queued else 0
        missing_article = missing[key] if key in missing else 0
        trade_article = trade[key] if key in trade else (0, 0, 0)

        period_end = current[key][0] + production_article - consumption[key] + \
            processing_article + queued_article + \
            missing_article + trade_article[0] - trade_article[1]
        current_worth = current[key][0] * current[key][1]
        period_end_worth = period_end * current[key][1]
        results[key] = round((current_worth + period_end_worth) * 0.5, 2)
        # results are the average inventory worths for every article

    return results
