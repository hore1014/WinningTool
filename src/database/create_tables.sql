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

CREATE TABLE IF NOT EXISTS Strategie_Lagerbestand(
   Periode INT,
   Artikel CHAR(10),
   Aktuell_0 INT,
   Aktuell_1 INT,
   Aktuell_2 INT,
   Aktuell_3 INT,
   PRIMARY KEY (Periode, Artikel)
);

CREATE TABLE IF NOT EXISTS  Produktion(
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
   Endbestand INT,
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
   Direktkauf REAL,
   Direktverkauf REAL,
   Preis REAL,
   PRIMARY KEY (Periode, Artikel)
);

CREATE TABLE IF NOT EXISTS Wareneingaenge(
   Periode INT,
   Artikel CHAR(10),
   Menge INT,
   PRIMARY KEY (Periode, Artikel)
);

CREATE TABLE IF NOT EXISTS Warteschlangen(
   Periode INT,
   Artikel CHAR(10),
   Menge_in_Bearbeitung INT,
   Stationen_in_Bearbeitung INT,
   Menge_Warteschlange INT,
   Stationen_Warteschlange INT,
   Menge_Fehlmaterial INT,
   Stationen_Fehlmaterial INT,
   Fehlmaterial CHAR(20),
   PRIMARY KEY (Periode, Artikel)
);
