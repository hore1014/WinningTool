
def calculate_demand(sales, current, planned, processing, queued, trade):
    P1 = sales["P1"] + planned["P1"] - current["P1"] - \
        processing["P1"] - queued["P1"] - trade["P1"]
    P2 = sales["P2"] + planned["P2"] - current["P2"] - \
        processing["P2"] - queued["P2"] - trade["P2"]
    P3 = sales["P3"] + planned["P3"] - current["P3"] - \
        processing["P3"] - queued["P3"] - trade["P3"]

    return {
        "P1": P1,
        "P2": P2,
        "P3": P3,
        "E4": 0,
        "E5": 0,
        "E6": 0,
        "E7": 0,
        "E8": 0,
        "E9": 0,
        "E10": 0,
        "E11": 0,
        "E12": 0,
        "E13": 0,
        "E14": 0,
        "E15": 0,
        "E16": 0,
        "E17": 0,
        "E18": 0,
        "E19": 0,
        "E20": 0,
        "E26": 0,
        "E29": 0,
        "E30": 0,
        "E31": 0,
        "E49": 0,
        "E50": 0,
        "E51": 0,
        "E54": 0,
        "E55": 0,
        "E56": 0,
    }
