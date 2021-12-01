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

db_Verbrauch = Table(
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

db_warteschlangen = Table(
    'Warteschlangen', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Menge', Integer),
    Column('Stationen', Integer, primary_key=True)
)

db_in_bearbeitung = Table(
    'In_Bearbeitung', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Menge', Integer),
    Column('Stationen', Integer, primary_key = True)
)

db_fehlmaterial = Table(
    'Fehlmaterial', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Menge', Integer),
    Column('Stationen', Integer, primary_key = True),
    Column('Fehlmaterial', String, primary_key = True) #Fehlende Artikel, die für diesen Artiekl benötigt werden
)

# Initialize (create and populate) database from XML input data
def init_db():

    # Read SQL files
    file = open("src\database\drop_tables.sql", "r")
    drop_cmd = file.read()
    file.close()

    file = open("src\database\create_tables.sql", "r")
    create_cmd = file.read()
    file.close()

    # Create and Connect to SQLite database
    conn = sqlite3.connect("src\database\ibsys2.db")
    #engine = create_engine('sqlite:///src/database/ibsys2.db', echo = True)

    # Drop existing tables
    conn.executescript(drop_cmd)

    # Create Tables
    conn.executescript(create_cmd)

    # Insert statements
    for el in create_lagerbestand(): 
        conn.execute(str(db_lagerbestand.insert()), el)

    for el in create_wareneingang():
        conn.execute(str(db_wareneingaenge.insert()), el)

    for el in create_in_bearbeitung():
        conn.execute(str(db_in_bearbeitung.insert()), el)

    for el in create_warteschlangen():
        conn.execute(str(db_warteschlangen.insert()), el)

    for el in create_fehlmaterial():
        conn.execute(str(db_fehlmaterial.insert()), el)

    for el in create_vertriebswunsch():
        conn.execute(str(db_absatzprognose.insert()), el)

    # for el in create_vertriebswunsch_neu():
    #     conn.execute(str(db_absatzprognose_neu.insert()), el)

    conn.commit()
    conn.close()

    return



# Retrieve data from DB
def get_sales_forecast(period):

    res_dict = {}

    # SQL Query statements
    query = "SELECT * from Absatzprognose WHERE Periode = :p"
    
    # Create and Connect to SQLite database
    conn = sqlite3.connect("src\database\ibsys2.db")

    # Execute SQL command
    result = conn.execute(str(query), str(period)).fetchall()
    for row in result:
        # Add values to dictionary
        res_dict[row[1]] = (row[2], row[3], row[4], row[5])

    # Close connection to database
    conn.close()

    return res_dict

def get_inventory_strategy(period):
    # Create and Connect to SQLite database
    conn = sqlite3.connect("src\database\ibsys2.db")

     # SQL Query statement
    query = "SELECT * from Strategie_Lagerbestand WHERE Periode = :p"

    for art in lookup.p_e_list:
           

    
    return

def get_parts_inventory(period):
    return

def get_inventory_strategy(period):
    return

def get_parts_processing(period):
    return

def get_parts_in_queue(period):
    return

def get_parts_trade(period):
    return
