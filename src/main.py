import database.db_mock as db
import production.demand as prod

parts_list = ["P1", "P2", "P3", "E4", "E5", "E6", "E7",
              "E8", "E9", "E10", "E11", "E12", "E13", "E14", ]

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

print(demand)
