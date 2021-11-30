from procurement import lookupProcurement as pc
from math import floor


def calculate_procurement(inventory, forecast0, forecast1, forecast2, forecast3):
    results = {"K21": (0, 0), "K22": (0, 0), "K23": (0, 0), "K24": (0, 0), "K25": (0, 0), "K27": (0, 0), "K28": (0, 0), "K32": (0, 0), "K33": (0, 0), "K34": (0, 0), "K35": (0, 0), "K36": (0, 0), "K37": (0, 0), "K38": (0, 0), "K39": (
        0, 0), "K40": (0, 0), "K41": (0, 0), "K42": (0, 0), "K43": (0, 0), "K44": (0, 0), "K45": (0, 0), "K46": (0, 0), "K47": (0, 0), "K48": (0, 0), "K52": (0, 0), "K53": (0, 0), "K57": (0, 0), "K58": (0, 0), "K59": (0, 0), }

    for article in results:
        inventory_reach = 0
        average_consumption = (
            forecast0[article] + forecast1[article] + forecast2[article] + forecast3[article])/4
        order = average_consumption * 1, 2

        if (inventory[article] - forecast0[article] <= 0):
            inventory_reach = floor(
                0 + (inventory[article]) / (forecast0[article]/5))

        elif (inventory[article] - forecast0[article] - forecast1[article] <= 0):
            inventory_reach = floor(
                5 + (inventory[article] - forecast0[article]) / (forecast1[article]/5))

        elif (inventory[article] - forecast0[article] - forecast1[article] - forecast2[article] <= 0):
            inventory_reach = floor(
                10 + (inventory[article] - forecast0[article] - forecast1[article]) / (forecast2[article]/5))

        elif (inventory[article] - forecast0[article] - forecast1[article] - forecast2[article] - forecast3[article] <= 0):
            inventory_reach = floor(
                15 + (inventory[article] - forecast0[article] - forecast1[article] - forecast2[article]) / (forecast3[article]/5))

        elif ():
            print(f"Reichweite Lagerbestand {article}: >20 Tage")

        if (inventory_reach >= pc.delivery_days[article][2]):
            results[article] = (order, 0)
        else:
            results[article] = (0, order)

    return results
