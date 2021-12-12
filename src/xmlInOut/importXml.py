import xml.etree.ElementTree as ET
import pandas as pd
import os

# XML Ergebnis Dateien auslesen

# Auslesen aller XML files in /src/data
def parse_all_xml(path = 'src/data/'):
    """
    Parses all xml files in given directory and returns a list of xml-root objects
    Parameters
    -----------
    `path`: str
        The directory where the xml files reside. 
    """
    # Liste aller XML roots
    root_arr = []
    #path = 'src//data//'
    files_list = os.listdir(path)
    for file in files_list:
        if file.endswith('.xml'):
            # XML file parsen
            tree = ET.parse(path + file)
            # Speichern des root Elements von jedem XML tree
            root = tree.getroot()
            # Sammeln in einer Liste
            root_arr.append(root)

    return root_arr

def get_period_by_file(file: str):
    """
    Parses xml file and returns the period in file. This method is only used for validation in the html upload form.
    Parameters.
    -----------
    `file`: str
        The xml file.
    """
    try: # This is the first point where xml file is parsed
        # TODO Exception-Types aufsplitten, sodass Fehler beim Upload klarer ist
        root = ET.parse(file).getroot()
        return (int(root.get('period')))
    except:
        return -1

# Finde die aktuelle Periode anhand der hochgeladenen XML files
def get_current_period(root_arr: list):
    """
    Iterates through all xml-root objects in given list and returns the highest period incremented by 1 (since uploading the result of period `x` indicates that user wants to simulate period `x+1`).
    Parameters
    -----------
    `root_arr`: list
        List of xml root objects that is retrieved by `parse_all_xml()` method.
    """
    if(len(root_arr) == 0):
        return 1
    periods = []
    for root in root_arr:
        periods.append(int(root.get('period'))+1)
    return max(periods)

# Erstelle Liste der Vertriebswünsche (für Tabelle Absatzprognose)
# Die Ergebnis-XML einer Periode enthält immer den Vertriebswunsch/Absatzprognose der kommenden Periode
def create_vertriebswunsch(root_arr):
    vertriebswunsch_arr = []

    # Erste Periode manuell hinzufügen: 
    vertriebswunsch_arr.append({
        'Periode': 1, 
        'Artikel': 'P1', 
        'Aktuell_0': 150, 
        'Aktuell_1': 150, 
        'Aktuell_2': 150, 
        'Aktuell_3': 150
    })
    vertriebswunsch_arr.append({
        'Periode': 1, 
        'Artikel': 'P2', 
        'Aktuell_0': 150, 
        'Aktuell_1': 100, 
        'Aktuell_2': 100, 
        'Aktuell_3': 50
    })
    vertriebswunsch_arr.append({
        'Periode': 1, 
        'Artikel': 'P3', 
        'Aktuell_0': 150, 
        'Aktuell_1': 100, 
        'Aktuell_2': 50, 
        'Aktuell_3': 50
    })

    for root in root_arr:
        forecast = root.find('forecast')
        vertriebswunsch_arr.append({
            'Periode': int(root.get('period'))+1, # forecast of period i concerns period i+1
            'Artikel': 'P1',
            'Aktuell_0': forecast.get('p1'),
            'Aktuell_1': "0",
            'Aktuell_2': "0",
            'Aktuell_3': "0",
        })
        vertriebswunsch_arr.append({
            'Periode': int(root.get('period'))+1,
            'Artikel': 'P2',
            'Aktuell_0': forecast.get('p2'),
            'Aktuell_1': "0",
            'Aktuell_2': "0",
            'Aktuell_3': "0",
        })
        vertriebswunsch_arr.append({
            'Periode': int(root.get('period'))+1,
            'Artikel': 'P3',
            'Aktuell_0': forecast.get('p3'),
            'Aktuell_1': "0",
            'Aktuell_2': "0",
            'Aktuell_3': "0",
        })

    return vertriebswunsch_arr

# Lagerbestand
def create_lagerbestand(root_arr):
    lagerbestand_arr = []
    for root in root_arr:
        for article in root.iter('article'):

            lagerbestand_arr.append({
                'Periode': int(root.get('period')), 
                'Artikel': article.get('id'), 
                'Anfangsbestand': article.get('startamount'), 
                'Endbestand': article.get('amount'), 
                'Wert': article.get('price')
                })
    
    return lagerbestand_arr

# Wareneingänge
# Die eingetroffenen Waren werden in DB gespeichert
# Wenn diese Waren bereits eingetroffen sind, ist der Ankunftszeitpunkt unerheblich für die Bestellplanung (steht in XML als 'time' in min.)
# Lediglich für noch offene Bestellungen (future-inward-stock-movement) sollte der voraussichtliche Zeitpunkt für die Bestellplanung ausgerechnet werden
def create_wareneingang(root_arr): 
    wareneingang_arr = []
    for root in root_arr:
        for order in root.find('inwardstockmovement').iter('order'):
            wareneingang_arr.append({
                'Periode': int(root.get('period')), 
                'Artikel': order.get('article'),
                'Menge': int(order.get('amount'))
            })
    # Mengen gleicher Artikel summieren (da ansonsten UNIQUE constraint verletzt ist)
    if not len(root_arr) == 0:
        df = pd.DataFrame(wareneingang_arr)
        wareneingang_arr_aggreg = df.groupby(['Periode', 'Artikel']).agg(sum).reset_index().to_dict('records')

        return wareneingang_arr_aggreg
    return wareneingang_arr

# Noch ausstehende Wareneingänge für Bestellungen, die bereits getätigt wurden
def create_ausstehende_lieferungen(root_arr):
    orders_arr = []
    for root in root_arr:
        for order in root.find('futureinwardstockmovement').iter('order'):
            dict_element = {
                'Bestellperiode': int(order.get('orderperiod')),
                'Artikel': int(order.get('article')),
                'Menge': int(order.get('amount')),
                'Bestellart': int(order.get('mode')) # Normal (4) - oder Eilbestellung (5)
            }
            # Ausstehende Bestellunge können auch in der Folgeperiode noch auf der Warteliste stehen
            # und werden dort daher nochmal aufgeführt.
            # Diese sollen nicht nochmal extrahiert werden, da sonst das UNIQUE constraint der DB verletzt wird!
            if dict_element not in orders_arr:
                orders_arr.append(dict_element)

    return orders_arr


# Hole die Werte für die Artikel in Bearbeitung
def create_in_bearbeitung(root_arr):
    in_bearbeitung_arr = []
    for i, root in enumerate(root_arr):
        for workplace in root.find('ordersinwork').iter('workplace'):
            in_bearbeitung_arr.append({
                'Periode': int(root.get('period'))+1,  # we want to store start values of subsequent period
                'Artikel': workplace.get('item'),
                'Menge': workplace.get('amount'),
                'Station': workplace.get('id')
            })
    return in_bearbeitung_arr

# Hole die Werte für die Artikel in Warteschlange
def create_warteschlangen(root_arr):
    warteschlangen_arr = []

    for root in root_arr:
        for workplace in root.find('waitinglistworkstations').iter('workplace'):
            if int(workplace.get('timeneed')) > 0:
                for waitinglist in workplace.iter('waitinglist'):
                    warteschlangen_arr.append({
                        'Periode': int(root.get('period'))+1, # we want to store start values of subsequent period
                        'Artikel': waitinglist.get('item'),
                        'Menge': int(waitinglist.get('amount')),
                        'Station': workplace.get('id')
                    })
    # Zeilen nach Artikel aggregieren (Mengen gleicher Artikel summieren)
    if not len(root_arr) == 0:
        df = pd.DataFrame(warteschlangen_arr)
        warteschlangen_arr_aggreg = df.groupby(['Periode', 'Artikel', 'Station']).agg(sum).reset_index().to_dict('records')
        #TODO Stationen in Listen zusammenfassen
        return warteschlangen_arr_aggreg
    return warteschlangen_arr

# Hole die Werte für die fehlenden Artikel
def create_fehlmaterial(root_arr):
    fehlmaterial_arr = []
    for root in root_arr:
        for missingpart in root.find('waitingliststock').iter('missingpart'):
            if(missingpart):
                workplace = missingpart.find('workplace')
                waitinglist = workplace.find('waitinglist')
                fehlmaterial_arr.append({
                    'Periode': int(root.get('period'))+1, # we want to store start values of subsequent period
                    'Artikel': waitinglist.get('item'),
                    'Menge': waitinglist.get('amount'),
                    'Station': workplace.get('id'),
                    'Fehlmaterial': missingpart.get('id')
                })
    return fehlmaterial_arr
    # TODO: Was tun mit Liste von Missingparts? Müssen nur solche Missingparts mit Unterelement Waitinglist erfasst werden?
    # TODO: Es scheint immer nur eine Waitinglist/ein Workplace pro Missingpart zu geben. --> Keine Schleife nötig?


