import xml.etree.ElementTree as ET
ET.register_namespace("svg", "http://www.w3.org/2000/svg")


def gen(sra, zbor):
    tree = ET.parse("autokar-pass-id-template-1.svg")
    root = tree.getroot()

    return ET.tostring(root)
