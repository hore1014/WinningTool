import xml.etree.ElementTree as ET
import numpy as np

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
vertriebswunsch_arr = []
vertriebswunsch_arr.append({'p1': '150', 'p2': '150', 'p3': '150'})

for root in root_arr:
    forecast = root.find('forecast')
    vertriebswunsch_arr.append(forecast.attrib)

#p1_val = vertriebswunsch_arr[0]['p1']
#print(p1_val)

# Lagerbestand
lagerbestand_arr = []
for i, root in enumerate(root_arr):
    for article in root.iter('article'):
        id = article.get('id')
        anfangsbestand = article.get('startamount')
        endbestand = article.get('amount')
        wert = article.get('price')

        lagerbestand_arr.append({
            'Periode': i+1, 
            'Artikel': id, 
            'Anfangsbestand': anfangsbestand, 
            'Endbestand': endbestand, 
            'Wert': wert
            })
