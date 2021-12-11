import xml.etree.ElementTree as ET
from xml.dom import minidom
import os

def prettify(elem):
    """
    Return a pretty-printed XML string for the Element.

    Reference: https://pymotw.com/2/xml/etree/ElementTree/create.html
    """
    #rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(elem)
    return reparsed.toprettyxml(indent="  ")

default_selldirect = [
    ("P1", "0", "0.0", "0.0"),
    ("P2", "0", "0.0", "0.0"),
    ("P3", "0", "0.0", "0.0")
]

def export_xml(absatz: list , absatz_direkt: list, bestellungen: list, produktion: list, stationen: list):
    """
    Generiert die XML Eingabedaten für das Simulationstool
    Parameters
    -----------
    `absatz`: list of tuples
        [(<article>, <quantity>), ...]
    `absatz_direkt`: list of tuples
        [(<article>, <quantity>, <price>, <penalty>), ...]
    `bestellungen`: list of tuples
        [(<article>, <quantity>, <modus>), ...]
    `produktion`: list of tuples
        [(<article>: <quantity>), ...]
    `stationen`: list of tuples
        [(<station>, <shift>, <overtime>), ...]
    """
    # root element
    input = ET.Element('input')

    # qualitycontrol element
    ET.SubElement(input, 'qualitycontrol', {"type": "no", "losequantity":"0", "delay": "0"})

    # sellwish element
    sellwish = ET.SubElement(input, 'sellwish')
    for el in absatz:
        ET.SubElement(sellwish, 'item', {
            "article": el[0][1:], #takes first item in tuple and removes first character 
            "quantity": str(el[1])
        })

    # selldirect element
    selldirect = ET.SubElement(input, 'selldirect')
    if(len(absatz_direkt) == 0):
        absatz_direkt = default_selldirect
    for el in absatz_direkt:
        ET.SubElement(selldirect, 'item', {
            "article": el[0][1:], 
            "quantity": str(el[1]), 
            "price": str(el[2]), 
            "penalty": str(el[3])
        })

    # orderlist element
    orderlist = ET.SubElement(input, 'orderlist')
    for el in bestellungen:
        ET.SubElement(orderlist, 'order', {
            "article" : el[0][1:], 
            "quantity": str(el[1]), 
            "modus": str(el[2])
        })

    # productionlist element
    productionlist = ET.SubElement(input, 'productionlist')
    for el in produktion:
        ET.SubElement(productionlist, 'production', {
            "article": el[0][1:], 
            "quantity": str(el[1])
        })
    
    # workingtimelist element
    workingtimelist = ET.SubElement(input, 'workingtimelist')
    for el in stationen:
        ET.SubElement(workingtimelist, 'workingtime', {
            "station": str(el[0]),
            "shift": str(el[1]),
            "overtime": str(el[2])
        })

    return prettify(ET.tostring(input, encoding='unicode', method='xml'))
