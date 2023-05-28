import xml.etree.ElementTree as ET
ET.register_namespace("svg", "http://www.w3.org/2000/svg")


def gen_1(srp, svg_qrcode, zbor):
    tree = ET.parse("parking-pass-id-template-1.svg")
    root = tree.getroot()

    # nr identyfikatora
    elem = root.find(".//*[@id='numerIdentyfikatora']")
    elem.text = str(srp.pass_nr)

    # nazwa zboru
    elem = root.find(".//*[@id='nazwaZboru']")
    elem.text = zbor.name

    # nr rejestracyjny na 3 dni kongresowe
    elem = root.find(".//*[@id='rejnum']")
    elem.text = srp.regnum1

    # qrcode
    elem = root.find(".//*[@id='layer1']")
    qrcode_tree = ET.fromstring(svg_qrcode)
    grp = ET.SubElement(elem, "svg:g")
    grp.set("id", "g1864")
    grp.set("style", "stroke-width:1.35465")
    grp.set("transform", "translate(86.4 15.5) scale(1.02 1.02)")
    grp.append(qrcode_tree)
    elem.append(grp)

    return ET.tostring(root)


def gen_3(srp, svg_qrcode, zbor):
    tree = ET.parse("parking-pass-id-template-3.svg")
    root = tree.getroot()

    # nr identyfikatora
    elem = root.find(".//*[@id='numerIdentyfikatora']")
    elem.text = str(srp.pass_nr)

    # nazwa zboru
    elem = root.find(".//*[@id='nazwaZboru']")
    elem.text = zbor.name

    # numery rejestracyjne
    elem = root.find(".//*[@id='d1rejnum']")
    elem.text = srp.regnum1
    elem = root.find(".//*[@id='d2rejnum']")
    elem.text = srp.regnum2
    elem = root.find(".//*[@id='d3rejnum']")
    elem.text = srp.regnum3

    # qrcode
    elem = root.find(".//*[@id='layer1']")
    qrcode_tree = ET.fromstring(svg_qrcode)
    grp = ET.SubElement(elem, "svg:g")
    grp.set("id", "g1864")
    grp.set("style", "stroke-width:1.35465")
    grp.set("transform", "translate(86.4 15.5) scale(1.02 1.02)")
    grp.append(qrcode_tree)
    elem.append(grp)

    return ET.tostring(root)
