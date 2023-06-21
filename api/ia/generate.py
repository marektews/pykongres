import xml.etree.ElementTree as ET
ET.register_namespace("svg", "http://www.w3.org/2000/svg")


def gen(sra, congregation, rja, sector, terminal, tura):
    tree = ET.parse("identyfikator-autokaru-template.svg")
    root = tree.getroot()

    # terminal: Łazienkowska (D) | Torwar (T)
    elem = root.find(".//*[@id='terminal']")
    elem.text = terminal.name

    # numer sektora
    elem = root.find(".//*[@id='sektor']")
    elem.text = _sector_number(sector.name)

    # sektor + tura
    elem = root.find(".//*[@id='identyfikator']")
    elem.text = sector.name.replace('x', tura)

    # nazwa zboru
    elem = root.find(".//*[@id='congregation']")
    if sra.lp is not None:
        elem.text = f"{congregation.name} {sra.lp}"
    else:
        elem.text = congregation.name

    # podstawienia
    elem = root.find(".//*[@id='arrive1']")
    elem.text = rja.a1.strftime("%H:%M") if rja.a1 is not None else ""
    elem = root.find(".//*[@id='arrive2']")
    elem.text = rja.a2.strftime("%H:%M") if rja.a2 is not None else ""
    elem = root.find(".//*[@id='arrive3']")
    elem.text = rja.a3.strftime("%H:%M") if rja.a3 is not None else ""

    # odjazdy
    elem = root.find(".//*[@id='departure1']")
    elem.text = rja.d1.strftime("%H:%M") if rja.d1 is not None else ""
    elem = root.find(".//*[@id='departure2']")
    elem.text = rja.d2.strftime("%H:%M") if rja.d2 is not None else ""
    elem = root.find(".//*[@id='departure3']")
    elem.text = rja.d3.strftime("%H:%M") if rja.d3 is not None else ""

    return ET.tostring(root)


def _sector_number(name):
    i = name.index('x')
    return name[i+1:]
