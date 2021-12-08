# This file is responsible for handling communication realted to database, i.e. initialization, creation, population of database as well as retrievement of data from database

import os
import sqlite3
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine, insert, select, update, text
from sqlalchemy.sql.expression import column
from sqlalchemy.sql.sqltypes import DECIMAL, REAL, Float
import itertools
import sys
sys.path.append(os.path.abspath(os.curdir))
from src.xmlInOut.importXml import *
from . import lookupArticles as lookup

# The database directory
db_dir = "src\database\ibsys2.db"

# Define ORM for database tables
meta = MetaData()

db_absatzprognose = Table(
        'Absatzprognose', meta,
        Column('Periode', Integer, primary_key = True),
        Column('Artikel', String, primary_key = True),
        Column('Aktuell_0', Integer),
        Column('Aktuell_1', Integer),
        Column('Aktuell_2', Integer),
        Column('Aktuell_3', Integer)
)

# db_absatzprognose_neu = Table(
#     'Absatzprognose_Neu', meta,
#     Column('Periode', Integer, primary_key = True),
#     Column('P1', Integer),
#     Column('P2', Integer),
#     Column('P3', Integer),
# )

db_strategie_Lagerbestand = Table(
    'Strategie_Lagerbestand', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Aktuell_0', Integer),
    Column('Aktuell_1', Integer),
    Column('Aktuell_2', Integer),
    Column('Aktuell_3', Integer)
)

db_produktion = Table(
    'Produktion', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Planlagerbestand', Integer),
    Column('Produktionsmenge', Integer)    
)

db_verbrauch = Table(
    'Verbrauch', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Verbrauch', Integer)
)

db_lagerbestand = Table(
    'Lagerbestand', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Anfangsbestand', Integer),
    Column('Endbestand', Integer),
    Column('Wert', Float)
)

db_kapazitaet = Table(
    'Kapazitaet', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Station', String, primary_key = True),
    Column('Bearbeitungszeit', Integer),
    Column('Ruestzeit', Integer),
    Column('Ruestzeitfaktor', Integer)    
)

db_einkauf = Table(
    'Einkauf', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Menge_Normalbestellung', Integer),
    Column('Menge_Eilbestellung', Integer)
)

db_handel = Table(
    'Handel', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),  
    Column('Direktkauf', Float),
    Column('Direktverkauf', Float),
    Column('Preis', Float)
)

db_wareneingaenge = Table(
    'Wareneingaenge', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Menge', Integer)  
)

db_wareneingaenge_ausstehend = Table(
    'Wareneingaenge_Ausstehend', meta,
    Column('Bestellperiode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Menge', Integer),
    Column('Bestellart', Integer, primary_key = True)  
)

db_warteschlangen = Table(
    'Warteschlangen', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Menge', Integer),
    Column('Station', Integer, primary_key=True)
)

db_in_bearbeitung = Table(
    'In_Bearbeitung', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Menge', Integer),
    Column('Station', Integer, primary_key = True)
)

db_fehlmaterial = Table(
    'Fehlmaterial', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Menge', Integer),
    Column('Station', Integer, primary_key = True),
    Column('Fehlmaterial', String, primary_key = True) #Fehlende Artikel, die für diesen Artiekl benötigt werden
)

tables = {
   "Absatzprognose": db_absatzprognose,
   "Strategie_Lagerbestand": db_strategie_Lagerbestand,
   "Produktion": db_produktion,
   "Verbrauch": db_verbrauch,
   "Lagerbestand": db_lagerbestand,
   "Kapazitaet": db_kapazitaet,
   "Einkauf": db_einkauf,
   "Handel": db_handel,
   "Wareneingaenge": db_wareneingaenge,
   "Wareneingaenge_Ausstehend": db_wareneingaenge_ausstehend,
   "Warteschlangen": db_warteschlangen,
   "In_Bearbeitung": db_in_bearbeitung,
   "Fehlmaterial": db_fehlmaterial
}

# Initialize (create and populate) database from XML input data
def init_db(root_arr: list):

    # Read SQL files
    #TODO Das soll nur explizit vom User ausgeführt werden!
    file = open("src\database\drop_tables.sql", "r")
    drop_cmd = file.read()
    file.close()

    file = open("src\database\create_tables.sql", "r")
    create_cmd = file.read()
    file.close()

    # Create and Connect to SQLite database
    conn = sqlite3.connect(db_dir)
    #engine = create_engine('sqlite:///src/database/ibsys2.db', echo = True)

    # Drop existing tables
    conn.executescript(drop_cmd)

    # Create Tables
    conn.executescript(create_cmd)

    # Insert statements
    for el in create_lagerbestand(root_arr): 
        conn.execute(str(db_lagerbestand.insert()), el)

    for el in create_wareneingang(root_arr):
        conn.execute(str(db_wareneingaenge.insert()), el)

    for el in create_ausstehende_lieferungen(root_arr):
        conn.execute(str(db_wareneingaenge_ausstehend.insert()), el)

    for el in create_in_bearbeitung(root_arr):
        conn.execute(str(db_in_bearbeitung.insert()), el)

    for el in create_warteschlangen(root_arr):
        conn.execute(str(db_warteschlangen.insert()), el)

    for el in create_fehlmaterial(root_arr):
        conn.execute(str(db_fehlmaterial.insert()), el)

    for el in create_vertriebswunsch(root_arr):
        conn.execute(str(db_absatzprognose.insert()), el)

    conn.commit()
    conn.close()

    return


# Retrieve data from DB

# Helper function for specific get-methods
def get_all_from_db(period: int, table: str, period_column_name = "Periode"):
    # Create and Connect to SQLite database
    conn = sqlite3.connect(db_dir)

    # SQL Query statement
    query = f"SELECT * from {table} WHERE {period_column_name} = :p"

    # Execute SQL command
    result = conn.execute(str(query), str(period)).fetchall()

    # Close connection to database
    conn.close()

    return result

# Helper function for specific get-methods
def get_agg_from_db(period: int, table: str):
    # Create and Connect to SQLite database
    conn = sqlite3.connect(db_dir)

    # SQL Query statement
    query = f"SELECT Artikel, SUM(Menge) from {table} WHERE Periode = :p GROUP BY Artikel"

    # Execute SQL command
    result = conn.execute(str(query), str(period)).fetchall()

    # Close connection to database
    conn.close()

    return result


def get_sales_forecast(period: int):
    res_dict = {}
    result = get_all_from_db(period, "Absatzprognose")

    for row in result:
        # Add values to dictionary
        # (Periode, Artikel, Aktuell_0, Aktuell_1, Aktuell_2, Aktuell_3)
        res_dict[row[1]] = (row[2], row[3], row[4], row[5])

    return res_dict

def get_inventory_strategy(period: int):
    res_dict = {}
    result = get_all_from_db(period, "Strategie_Lagerbestand")
    
    for row in result:
        # Add values to dictionary
        # (Periode, Artikel, Aktuell_0, Aktuell_1, Aktuell_2, Aktuell_3)
        res_dict[row[1]] = (row[2], row[3], row[4], row[5])        
    
    return res_dict

def get_parts_inventory(period: int):
    res_dict = {}
    result = get_all_from_db(period, "Lagerbestand")

    for row in result:
        # (Periode, Artikel, Anfangsbestand, Endbestand, Wert)
        # Convert number to official notation
        art = lookup.p_e_k_list[int(row[1]) - 1]
        # Add values to dictionary
        res_dict[art] = (row[2], row[4])
        
    return res_dict

def get_parts_processing(period: int):
    res_dict = {}
    # Parts might be proecessed simultaneously at different stations - so it needs to be aggregated
    result = get_agg_from_db(period, "In_Bearbeitung")

    for row in result:
        # (Artikel, Menge)
        # Convert number to official notation
        art = lookup.p_e_k_list[int(row[0]) - 1]
        # Add values to dictionary
        res_dict[art] = row[1]
        
    return res_dict

def get_parts_in_queue(period: int):
    res_dict = {}
    # Parts might be proecessed simultaneously at different stations - so it needs to be aggregated
    result = get_agg_from_db(period, "Warteschlangen")

    for row in result:
        # (Artikel, Menge)
        # Convert number to official notation
        art = lookup.p_e_k_list[int(row[0]) - 1]
        # Add values to dictionary
        res_dict[art] = row[1]

    return res_dict

def get_missing_parts(period: int):
    res_dict = {}
    # Parts might be proecessed simultaneously at different stations - so it needs to be aggregated 
    result = get_agg_from_db(period, "Fehlmaterial")

    for row in result:
        # (Artikel, Menge)
        # Convert number to official notation
        art = lookup.p_e_k_list[int(row[0]) - 1]
        # Add values to dictionary
        res_dict[art] = row[1]

    return res_dict

def get_parts_trade(period: int):
    res_dict = {}

    result = get_all_from_db(period, "Handel")

    # (Periode, Artikel, Direktkauf, Direktverkauf, Preis)
    for row in result:
        #TODO: User needs to input trade values with preceeding letter! (P, E or K)
        res_dict[row[1]] = (row[2], row[3], row[4])

    return res_dict

def get_orders_in_transit(period: int):
    res_dict = {}
    result = get_all_from_db(period, "Wareneingaenge_Ausstehend", "Bestellperiode")

    for row in result:
        # (Bestellperiode, Artikel, Menge, Bestellart)
        art = lookup.p_e_k_list[int(row[1]) - 1]
        val = (row[0], row[2], row[3]) #tuple
        if art in res_dict:
            # Gleiche Artikel zusammenfassen:
            res_dict[art].append(val)
        else:
            res_dict[art] = [val, ] #list of tuples
    print(res_dict)
    return res_dict

# Write data from user input
# TODO How to overwrite rows?
def write_input_to_db(data: list, table_name: str):
     # Connect to SQLite database
    conn = sqlite3.connect(db_dir)

    # Insert statements
    for el in data: 
        conn.execute(str(tables[table_name].insert()), el)

    conn.commit()
    conn.close()

    return