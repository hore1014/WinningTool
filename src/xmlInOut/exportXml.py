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

def export_xml(absatz: list, absatz_direkt: list, bestellungen: list, produktion: list, stationen: list):
    """
    Generiert die XML Eingabedaten für das Simulationstool
    Parameters
    -----------
    `absatz`: list
        {'article': <quantity>, ...}
    `absatz_direkt`: list
        {'article': (<quantity>, <price>, <penalty>), ...}
    `bestellungen`: list
        {'article': (<quantity>, <modus>), ...}
    `produktion`: list
        [('article': <quantity>), ...]
    `stationen`: list
        {'station': (<shift>, <overtime>)}
    """
    input = ET.Element('input')

    qualitycontrol = ET.SubElement(input, 'qualitycontrol')
    sellwish = ET.SubElement(input, 'sellwish')
    selldirect = ET.SubElement(input, 'selldirect')
    orderlist = ET.SubElement(input, 'orderlist')
    productionlist = ET.SubElement(input, 'productionlist')
    for el in produktion:
            article = el[0][1:] # takes first item in tuple and removes first character
            quantity = str(el[1])
            ET.SubElement(productionlist, 'production', {"article": article, "quantity": quantity})
    workingtimelist = ET.SubElement(input, 'workingtimelist')

    return prettify(ET.tostring(input, encoding='unicode', method='xml'))
