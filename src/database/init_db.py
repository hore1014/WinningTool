import sqlite3
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine
from sqlalchemy.sql.sqltypes import DECIMAL, REAL, Float

file = open("src\database\drop_tables.sql", "r")
drop_cmd = file.read()
file.close()

file = open("src\database\create_tables.sql", "r")
create_cmd = file.read()
file.close()

# Create and Connect to SQLite database
conn = sqlite3.connect("src\database\ibsys2.db")
engine = create_engine('sqlite:///src/database/ibsys2.db', echo = True)

# Drop existing tables
conn.executescript(drop_cmd)

# Create Tables
conn.executescript(create_cmd)

meta = MetaData()

db_absatzprognose = Table(
    'Absatzprognose', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Aktuell_0', Integer),
    Column('Aktuell_1', Integer),
    Column('Aktuell_2', Integer),
    Column('Aktuell_3', Integer),
)

db_strategie_Lagerbestand = Table(
    'Strategie_Lagerbestand', meta,
    Column('Periode', Integer, primary_key = True),
    Column('Artikel', String, primary_key = True),
    Column('Aktuell_0', Integer),
    Column('Aktuell_1', Integer),
    Column('Aktuell_2', Integer),
    Column('Aktuell_3', Integer),
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
    Column('Menge_in_Bearbeitung', Integer),
    Column('Stationen_in_Bearbeitung', Integer),
    Column('Menge_Warteschlange', Integer),
    Column('Stationen_Warteschlange', Integer),
    Column('Menge_Fehlmaterial', Integer),
    Column('Stationen_Fehlmaterial', Integer),
    #Column('Fehlmaterial', String) -- Fehlende Artikel, die für diesen Artiekl benötigt werden
)

conn.execute()



conn.close()
