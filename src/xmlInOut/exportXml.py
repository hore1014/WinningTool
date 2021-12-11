import xml.etree.ElementTree as ET
import os

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
        {'article': <quantity>}
    `stationen`: list
        {'station': (<shift>, <overtime>)}
    """
    input = ET.Element('input')

    qualitycontrol = ET.SubElement(input, 'qualitycontrol')
    sellwish = ET.SubElement(input, 'sellwish')
    selldirect = ET.SubElement(input, 'selldirect')
    orderlist = ET.SubElement(input, 'orderlist')
    productionlist = ET.SubElement(input, 'productionlist')
    workingtimelist = ET.SubElement(input, 'workingtimelist')

    print(ET.dump(input))



export_xml()