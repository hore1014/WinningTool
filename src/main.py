from database import db_mock as db
from production import production as prod
from production import consumption as cons
from capacity import capacity as cap
import json
from functools import reduce

# load all necessary data for production calculation from database
sales_forecast = db.get_sales_forecast(1)
current_parts = db.get_parts_inventory(1)
planned_parts = db.get_parts_inventory_planned(1)
parts_processing = db.get_parts_processing(1)
parts_in_queue = db.get_parts_in_queue(1)
parts_traded = db.get_parts_trade(1)

production = prod.calculate_production(
    sales_forecast,
    current_parts,
    planned_parts,
    parts_processing,
    parts_in_queue,
    parts_traded,
)

consumption = cons.calculate_consumption(production, sales_forecast)

# TODO: calculate tooling factors for each period from average of pervious periods
tooling_factors = {"Station_1": 1.25, "Station_2": 1.25, "Station_3": 1, "Station_4": 1.25, "Station_5": 0, "Station_6": 1, "Station_7": 2,
                   "Station_8": 1.5, "Station_9": 1, "Station_10": 1.25, "Station_11": 1.25, "Station_12": 1, "Station_13": 1, "Station_14": 1, "Station_15": 2, }

capacity = cap.calculate_capacity(production, tooling_factors)

shifts = cap.calculate_shifts(capacity)

# print the results with sums for control purposes
print(f"Produktion:\n{json.dumps(production, indent=4)}")
print(f"Summe: {reduce(lambda x, value: x + value, production.values(), 0)}\n")

print(f"Verbrauch:\n{json.dumps(consumption, indent=4)}")
print(f"Summe: {reduce(lambda x, value: x + value, consumption.values(), 0)}\n")

print(f"Kapazität:\n{json.dumps(capacity, indent=4)}")
print(f"Summe: {reduce(lambda x, value: x + value, capacity.values(), 0)}\n")

print("Schichten:\n{")
for station in shifts:
    print(
        f"\t\"{station}\": ({shifts[station][0]}, {shifts[station][1]/5})")
print("}\n" +
      f"Summe Mehrarbeit: {reduce(lambda x, value: x + value[1], shifts.values(), 0)}\n")
