import xml.etree.ElementTree as ET
#import numpy as np
import pandas as pd
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine

# XML Ergebnis Datei auslesen
tree_period_1 = ET.parse('src\data\ergebnis_periode1.xml')
tree_period_2 = ET.parse('src\data\ergebnis_periode2.xml')
tree_period_3 = ET.parse('src\data\ergebnis_periode3.xml')
tree_period_4 = ET.parse('src\data\ergebnis_periode4.xml')
tree_period_5 = ET.parse('src\data\ergebnis_periode5.xml')
tree_period_6 = ET.parse('src\data\ergebnis_periode6.xml')

# Speichern des root Elements von jedem XML tree
root_period_1 = tree_period_1.getroot()
root_period_2 = tree_period_2.getroot()
root_period_3 = tree_period_3.getroot()
root_period_4 = tree_period_4.getroot()
root_period_5 = tree_period_5.getroot()
root_period_6 = tree_period_6.getroot()

# Sammeln in einer Liste
root_arr = []
root_arr.append(root_period_1)
root_arr.append(root_period_2)
root_arr.append(root_period_3)
root_arr.append(root_period_4)
root_arr.append(root_period_5)
root_arr.append(root_period_6)

# Erstelle Liste der Vertriebswünsche (für Tabelle Absatzprognose)
# Die Ergebnis-XML einer Periode enthält immer den Vertriebswunsch/Absatzprognose der kommenden Periode
def create_vertriebswunsch():
    vertriebswunsch_arr = []
    vertriebswunsch_arr.append({'p1': '150', 'p2': '150', 'p3': '150'})

    for root in root_arr:
        forecast = root.find('forecast')
        vertriebswunsch_arr.append(forecast.attrib)

    return vertriebswunsch_arr

#p1_val = vertriebswunsch_arr[0]['p1']
#print(p1_val)

# Lagerbestand
def create_lagerbestand():
    lagerbestand_arr = []
    for i, root in enumerate(root_arr):
        for article in root.iter('article'):

            lagerbestand_arr.append({
                'Periode': i+1, 
                'Artikel': article.get('id'), 
                'Anfangsbestand': article.get('startamount'), 
                'Endbestand': article.get('amount'), 
                'Wert': article.get('price')
                })
    
    return lagerbestand_arr()

# Wareneingänge
# Die eingetroffenen Waren werden in DB gespeichert
# Wenn diese Waren bereits eingetroffen sind, ist der Ankunftszeitpunkt unerheblich für die Bestellplanung (steht in XML als 'time' in min.)
# Lediglich für noch offene Bestellungen (future-inward-stock-movement) sollte der voraussichtliche Zeitpunkt für die Bestellplanung ausgerechnet werden
def create_wareneingang(): 
    wareneingang_arr = []
    for i, root in enumerate(root_arr):
        for order in root.find('inwardstockmovement').iter('order'):
            wareneingang_arr.append({
                'Periode': i+1,
                'Artikel': order.get('article'),
                'Menge': order.get('amount')
            })
    return wareneingang_arr

# Hole die Werte für die Artikel in Bearbeitung
def create_in_bearbeitung():
    in_bearbeitung_arr = []
    for i, root in enumerate(root_arr):
        for workplace in root.find('ordersinwork').iter('workplace'):
            in_bearbeitung_arr.append({
                'Periode': i+1,
                'Artikel': workplace.get('item'),
                'Menge': workplace.get('amount'),
                'Stationen': workplace.get('id')
            })
    return in_bearbeitung_arr

# Hole die Werte für die Artikel in Warteschlange
def create_warteschlangen():
    warteschlangen_arr = []

    for i, root in enumerate(root_arr):
        for workplace in root.find('waitinglistworkstations').iter('workplace'):
            if int(workplace.get('timeneed')) > 0:
                for waitinglist in workplace.iter('waitinglist'):
                    warteschlangen_arr.append({
                        'Periode': i+1,
                        'Artikel': waitinglist.get('item'),
                        'Menge': waitinglist.get('amount'),
                        'Stationen': workplace.get('id')
                    })
    # Zeilen nach Artikel aggregieren (Mengen gleicher Artikel summieren)
    df = pd.DataFrame(warteschlangen_arr)
    warteschlangen_arr_aggreg = df.groupby(['Periode', 'Artikel', 'Stationen']).agg(sum)
    #TODO Stationen in Listen zusammenfassen

    return warteschlangen_arr_aggreg

# Hole die Werte für die fehlenden Artikel
def create_fehlmaterial():
    fehlmaterial_arr = []
    for i, root in enumerate(root_arr):
        for missingpart in root.find('waitingliststock').iter('missingpart'):
            if(missingpart):
                workplace = missingpart.find('workplace')
                waitinglist = workplace.find('waitinglist')
                fehlmaterial_arr.append({
                    'Periode': i+1,
                    'Artikel': waitinglist.get('item'),
                    'Menge': waitinglist.get('amount'),
                    'Stationen': workplace.get('id'),
                    'Fehlmaterial': missingpart.get('id')
                })
    return fehlmaterial_arr
    # TODO: Was tun mit Liste von Missingparts? Müssen nur solche Missingparts mit Unterelement Waitinglist erfasst werden?
    # TODO: Es scheint immer nur eine Waitinglist/ein Workplace pro Missingpart zu geben. --> Kein Schleife nötig?


