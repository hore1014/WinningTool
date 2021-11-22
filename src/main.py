from database import db_mock as db
from production import demand as prod
from production import consumption as cons
import json
from functools import reduce

# load all necessary data for production calculation from database
sales_forecast = db.get_sales_forecast(1)
current_parts = db.get_parts_inventory(1)
planned_parts = db.get_parts_inventory_planned(1)
parts_processing = db.get_parts_processing(1)
parts_in_queue = db.get_parts_in_queue(1)
parts_traded = db.get_parts_trade(1)

demand = prod.calculate_demand(
    sales_forecast,
    current_parts,
    planned_parts,
    parts_processing,
    parts_in_queue,
    parts_traded,
)

consumption = cons.calculate_consumption(demand, sales_forecast)

# print the results with sums for control purposes
print(f"Produktion:\n{json.dumps(demand, indent=4)}")
print(f"Summe: {reduce(lambda x, value: x + value, demand.values(), 0)}\n")

print(f"Verbrauch:\n{json.dumps(consumption, indent=4)}")
print(f"Summe: {reduce(lambda x, value: x + value, consumption.values(), 0)}\n")
