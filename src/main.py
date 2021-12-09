from typing import Any
from database import db_mock as mock, db
from production import production as prod
from production import consumption as cons
from capacity import capacity as cap
from procurement import procurement as proc
from financial import inventory as inv
import json
from functools import reduce
from xmlInOut import importXml as xml

# TODO Löschen von XML files aus dem Ordner per Button

# global variables for Initialization
root_arr = []
current_period = 1

# global variables for calculations
sales_forecast = {}
current_parts = {}
planned_parts = {}
parts_processing = {}
parts_in_queue = {}
missing_parts = {}
parts_traded = {}
parts_ordered = {}

# global variables for results
production = {}
consumption = {}
orders = {}
capacity = {}
shifts = {}
average_inventory_worth = {}


# Read all xml files
def parse_all_xml():
    print("Parsing XML files")
    global root_arr
    root_arr = xml.parse_all_xml('src//data//')
    return root_arr


def get_current_period():
    print("Setting current Period")
    global current_period
    current_period = xml.get_current_period(root_arr)
    return current_period


# Initialize (create and populate) database from XML input data
def init_db():
    # TODO: Exception Handling! Es werden hässliche Fehlermeldungen
    # auf der Seite angezeigt
    db.init_db(root_arr)
    print("Datenbank wurde initialisiert")

# Write user input into db


def write_input_to_db(data: list, table_name: str):
    db.write_input_to_db(data, table_name)


# get from DB methods
def get_sales_forecast(current_period):
    return db.get_sales_forecast(current_period)


def get_inventory_strategy(current_period):
    return db.get_inventory_strategy(current_period)


def get_parts_inventory(current_period):
    return db.get_parts_inventory(current_period)


def get_parts_processing(current_period):
    return db.get_parts_processing(current_period)


def get_parts_in_queue(current_period):
    return db.get_parts_in_queue(current_period)


def get_missing_parts(current_period):
    return db.get_missing_parts(current_period)


def get_parts_trade(current_period):
    return db.get_parts_trade(current_period)


def get_orders_in_transit(current_period):
    return db.get_orders_in_transit(current_period-1) if current_period > 1 else {}


def get_production(current_period):
    global sales_forecast
    global current_parts
    global planned_parts
    global parts_processing
    global parts_in_queue
    global missing_parts
    global parts_traded

    sales_forecast = db.get_sales_forecast(current_period)
    current_parts = db.get_parts_inventory(current_period)
    planned_parts = mock.get_inventory_strategy(current_period)
    parts_processing = db.get_parts_processing(current_period)
    parts_in_queue = db.get_parts_in_queue(current_period)
    missing_parts = db.get_missing_parts(current_period)
    parts_traded = db.get_parts_trade(current_period)

    global production
    production = prod.calculate_production(
        sales_forecast,
        current_parts,
        planned_parts,
        parts_processing,
        parts_in_queue,
        missing_parts,
        parts_traded,
    )

    print(f"Produktion:\n{json.dumps(production, indent=4)}")
    return production


def get_consumption():
    global consumption
    consumption = cons.calculate_consumption(production, sales_forecast)

    print(f"Verbrauch:\n{json.dumps(consumption, indent=4)}")
    return consumption


def get_capacity():
    # TODO: calculate tooling factors for each period from average of pervious periods
    tooling_factors = {"Station_1": 1.25, "Station_2": 1.25, "Station_3": 1, "Station_4": 1.25, "Station_5": 0, "Station_6": 1, "Station_7": 2,
                       "Station_8": 1.5, "Station_9": 1, "Station_10": 1.25, "Station_11": 1.25, "Station_12": 1, "Station_13": 1, "Station_14": 1, "Station_15": 2, }

    global capacity
    capacity = cap.calculate_capacity(
        production,
        parts_processing,
        parts_in_queue,
        missing_parts,
        tooling_factors
    )

    print(f"Kapazität:\n{json.dumps(capacity, indent=4)}")
    return capacity


def get_shifts():
    global shifts
    shifts = cap.calculate_shifts(capacity)

    print("Schichten:\n{")
    for station in shifts:
        print(
            f"\t\"{station}\": ({shifts[station][0]}, {shifts[station][1]/5})")

    return shifts


def calc_prod_forecast(period):
    return prod.calculate_production_forecast(sales_forecast, planned_parts, period)


def get_orders():
    global parts_ordered

    parts_ordered = db.get_orders_in_transit(
        current_period-1) if current_period > 1 else {}

    production2 = calc_prod_forecast(1)
    production3 = calc_prod_forecast(2)
    production4 = calc_prod_forecast(3)

    consumption1 = cons.calculate_consumption_forecast(production)
    consumption2 = cons.calculate_consumption_forecast(production2)
    consumption3 = cons.calculate_consumption_forecast(production3)
    consumption4 = cons.calculate_consumption_forecast(production4)

    global orders
    orders = proc.calculate_procurement(
        current_parts,
        consumption1,
        consumption2,
        consumption3,
        consumption4,
        parts_ordered,
        current_period)

    print("Bestellungen:\n{")
    for article in orders:
        print(
            f"\t\"{article}\": Normalbestellung: {orders[article][0]},\tEilbestellung: {orders[article][1]},\tReichweite: {orders[article][2]} Tage")
    print("}\n")

    return orders


def get_average_inventory_worth():
    global average_inventory_worth

    get_consumption()

    average_inventory_worth = inv.get_average_inventory_worth(
        current_parts, production, consumption, parts_processing, parts_in_queue, missing_parts, parts_traded)

    print(
        f"Durchschnittlicher Lagerwert:\n{json.dumps(average_inventory_worth, indent=4)}")
    return average_inventory_worth


# Testing
get_production(1)


# print the results with sums for control purposes
def print_all_data():
    print(f"Produktion:\n{json.dumps(production, indent=4)}")
    print(
        f"Summe: {reduce(lambda x, value: x + value, production.values(), 0)}\n")

    print(f"Verbrauch:\n{json.dumps(consumption, indent=4)}")
    print(
        f"Summe: {reduce(lambda x, value: x + value, consumption.values(), 0)}\n")

    print(f"Kapazität:\n{json.dumps(capacity, indent=4)}")
    print(
        f"Summe: {reduce(lambda x, value: x + value, capacity.values(), 0)}\n")

    print("Schichten:\n{")
    for station in shifts:
        print(
            f"\t\"{station}\": ({shifts[station][0]}, {shifts[station][1]/5})")
    print("}\n" +
          f"Summe Mehrarbeit: {reduce(lambda x, value: x + value[1], shifts.values(), 0)}\n")

    print("Bestellungen:\n{")
    for article in orders:
        print(
            f"\t\"{article}\": Normalbestellung: {orders[article][0]},\tEilbestellung: {orders[article][1]},\tReichweite: {orders[article][2]} Tage")
    print("}\n")

    print(
        f"Durchschnittlicher Lagerwert:\n{json.dumps(average_inventory_worth, indent=4)}")
    print(
        f"Summe: {reduce(lambda x, value: x + value, average_inventory_worth.values(), 0)}\n")
