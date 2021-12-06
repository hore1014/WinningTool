from procurement import lookupProcurement as pc
from math import floor, ceil


def calculate_procurement(inventory, forecast0, forecast1, forecast2, forecast3, orders, period):
    results = {"K21": (0, 0, 0), "K22": (0, 0, 0), "K23": (0, 0, 0), "K24": (0, 0, 0), "K25": (0, 0, 0), "K27": (0, 0, 0), "K28": (0, 0, 0), "K32": (0, 0, 0), "K33": (0, 0, 0), "K34": (0, 0, 0), "K35": (0, 0, 0), "K36": (0, 0, 0), "K37": (0, 0, 0), "K38": (0, 0, 0), "K39": (
        0, 0, 0), "K40": (0, 0, 0), "K41": (0, 0, 0), "K42": (0, 0, 0), "K43": (0, 0, 0), "K44": (0, 0, 0), "K45": (0, 0, 0), "K46": (0, 0, 0), "K47": (0, 0, 0), "K48": (0, 0, 0), "K52": (0, 0, 0), "K53": (0, 0, 0), "K57": (0, 0, 0), "K58": (0, 0, 0), "K59": (0, 0, 0), }

    # TODO: test this factor in sandbox environment
    order_factor = 1.2

    for article in results:
        inventory_reach = 0
        orders_article = orders[article] if article in orders else []

        average_consumption = (
            forecast0[article] + forecast1[article] + forecast2[article] + forecast3[article])/4
        # factor in a buffer when ordering and round up to next 10
        order = int(ceil(average_consumption * order_factor / 10) * 10)

        # check in which period inventory goes to 0 and then find exact day to calulate inventory reach
        if (inventory[article][0] - forecast0[article] <= 0):
            inventory_reach = floor(
                0 + (inventory[article][0]) / (forecast0[article]/5))

        elif (inventory[article][0] - forecast0[article] - forecast1[article] <= 0):
            inventory_reach = floor(
                5 + (inventory[article][0] - forecast0[article]) / (forecast1[article]/5))

        elif (inventory[article][0] - forecast0[article] - forecast1[article] - forecast2[article] <= 0):
            inventory_reach = floor(
                10 + (inventory[article][0] - forecast0[article] - forecast1[article]) / (forecast2[article]/5))

        elif (inventory[article][0] - forecast0[article] - forecast1[article] - forecast2[article] - forecast3[article] <= 0):
            inventory_reach = floor(
                15 + (inventory[article][0] - forecast0[article] - forecast1[article] - forecast2[article]) / (forecast3[article]/5))

        else:
            inventory_reach = 20

        add_to_reach = 0
        for order_unit in orders_article:
            # check if order is normal (5) or express (4) and get the corresponding delivery time
            order_arrival = pc.delivery_days[article][0] if order_unit[2] == 4 else pc.delivery_days[article][2]
            # calculate how many periods ago the order was issued and subtract 5 days per period
            order_arrival -= (period - order_unit[0])*5

            # check if order arrives before inventory goes to 0 and if yes, add the amount of days gained
            if (inventory_reach >= order_arrival):
                add_to_reach += (order_unit[1] / (average_consumption/5))

        inventory_reach = floor(inventory_reach + add_to_reach)

        # express order if reach is less than normal delayed delivery time
        if (inventory_reach < pc.delivery_days[article][2]):
            # for express orders order double the amount so next period a normal order can be issued
            results[article] = (0, order*2, inventory_reach)

        # normal order if reach is greater than normal delayed delivery time and if inventory has less than 5 days of buffer
        elif (inventory_reach >= pc.delivery_days[article][2] and inventory_reach <= pc.delivery_days[article][2] + 5):
            results[article] = (order, 0, inventory_reach)

        # no order if inventory has at least 5 days of buffer
        else:
            results[article] = (0, 0, inventory_reach)

    return results
