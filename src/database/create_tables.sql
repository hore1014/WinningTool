-- SQL commands for creating all tables in database

--ATTACH DATABASE 'ibsys2.db' As 'IBSYS2';

CREATE TABLE IF NOT EXISTS Absatzprognose(
   Periode INT,
   Artikel CHAR(10),
   Aktuell_0 INT,
   Aktuell_1 INT,
   Aktuell_2 INT,
   Aktuell_3 INT,
   PRIMARY KEY (Periode, Artikel)
);

--CREATE TABLE IF NOT EXISTS Absatzprognose_Neu(
--   Periode INT,
--   P1 INT,
--   P2 INT,
--   P3 INT,
--   PRIMARY KEY (Periode)
--);

CREATE TABLE IF NOT EXISTS Strategie_Lagerbestand(
   Periode INT,
   Artikel CHAR(10),
   Aktuell_0 INT,
   Aktuell_1 INT,
   Aktuell_2 INT,
   Aktuell_3 INT,
   PRIMARY KEY (Periode, Artikel)
);

CREATE TABLE IF NOT EXISTS Produktion(
   Periode INT,
   Artikel CHAR(10),
   Planlagerbestand INT,
   Produktionsmenge INT,
   PRIMARY KEY (Periode, Artikel)
);

CREATE TABLE IF NOT EXISTS Verbrauch(
   Periode INT,
   Artikel CHAR(10),
   Verbrauch INT,
   PRIMARY KEY (Periode, Artikel)
);

CREATE TABLE IF NOT EXISTS Lagerbestand(
   Periode INT,
   Artikel CHAR(10),
   Anfangsbestand INT,
   Wert REAL,
   PRIMARY KEY (Periode, Artikel)
);

CREATE TABLE IF NOT EXISTS Kapazitaet(
   Periode INT,
   Station INT,
   Bearbeitungszeit INT,
   Ruestzeit INT,
   Ruestzeitfaktor REAL,
   PRIMARY KEY (Periode, Station)
);

CREATE TABLE IF NOT EXISTS Einkauf(
   Periode INT,
   Artikel CHAR(10),
   Menge_Normalbestellung INT,
   Menge_Eilbestellung INT,
   PRIMARY KEY (Periode, Artikel)
);

CREATE TABLE IF NOT EXISTS Handel(
   Periode INT,
   Artikel CHAR(10),
   Direktkauf INT,
   Direktverkauf INT,
   Preis REAL,
   PRIMARY KEY (Periode, Artikel)
);

CREATE TABLE IF NOT EXISTS Wareneingaenge(
   Periode INT,
   Artikel CHAR(10),
   Menge INT,
   PRIMARY KEY (Periode, Artikel)
);

CREATE TABLE IF NOT EXISTS Wareneingaenge_Ausstehend(
   Bestellperiode INT,
   Artikel CHAR(10),
   Menge INT,
   Bestellart INT,
   PRIMARY KEY (Bestellperiode, Artikel, Bestellart)
);

CREATE TABLE IF NOT EXISTS Warteschlangen(
   Periode INT,
   Artikel CHAR(10),
   Menge INT, 
   Station INT,
   PRIMARY KEY (Periode, Artikel, Station)
);

CREATE TABLE IF NOT EXISTS In_Bearbeitung(
   Periode INT,
   Artikel CHAR(10),
   Menge INT, -- default: 10
   Station INT,
   PRIMARY KEY (Periode, Artikel, Station)
);

CREATE TABLE IF NOT EXISTS Fehlmaterial(
   Periode INT,
   Artikel CHAR(10),
   Menge INT,
   Station INT,
   Fehlmaterial CHAR(20), -- Fehlende Artikel die für diesen Artikel benötigt werden
   PRIMARY KEY (Periode, Artikel, Station, Fehlmaterial)
);
