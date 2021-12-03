-- SQL commands for clearing database

--ATTACH DATABASE 'ibsys2.db' As 'IBSYS2';

DROP TABLE IF EXISTS Absatzprognose;
--DROP TABLE IF EXISTS Absatzprognose_Neu;
DROP TABLE IF EXISTS Strategie_Lagerbestand;
DROP TABLE IF EXISTS Produktion;
DROP TABLE IF EXISTS Verbrauch;
DROP TABLE IF EXISTS Lagerbestand;
DROP TABLE IF EXISTS Kapazitaet;
DROP TABLE IF EXISTS Einkauf;
DROP TABLE IF EXISTS Handel;
DROP TABLE IF EXISTS Wareneingaenge;
DROP TABLE IF EXISTS Wareneingaenge_Ausstehend;
DROP TABLE IF EXISTS Warteschlangen;
DROP TABLE IF EXISTS In_Bearbeitung;
DROP TABLE IF EXISTS Fehlmaterial;
