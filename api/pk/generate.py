# from flask import current_app
import xml.etree.ElementTree as ET
ET.register_namespace("svg", "http://www.w3.org/2000/svg")


def _gen_1(pk, svg_qrcode, department):
    tree = ET.parse("parking-torwar-pass-id-template-1.svg")
    root = tree.getroot()

    # nr identyfikatora
    elem = root.find(".//*[@id='numerIdentyfikatora']")
    elem.text = str(pk.pass_nr)

    # nazwa działu
    elem = root.find(".//*[@id='department']")
    elem.text = f"{department.lang} - {department.name}"

    # nr rejestracyjny na 3 dni kongresowe
    elem = root.find(".//*[@id='rejnum']")
    elem.text = pk.regnum1

    # qrcode
    # current_app.logger.info(f"gen_1: qrcode: {svg_qrcode}")
    layer = root.find(".//*[@id='layer1']")
    qrcode_tree = ET.fromstring(svg_qrcode)
    grp = ET.SubElement(layer, "svg:g")
    grp.set("id", "g1864")
    grp.set("style", "stroke-width:1.35465")
    grp.append(qrcode_tree)

    # pozycjonowanie
    margin = 5
    parent_elem = root.find(".//*[@id='qrCode']")
    x = float(parent_elem.get("x")) + margin
    y = float(parent_elem.get("y")) + margin
    pw = float(parent_elem.get("width"))
    ph = float(parent_elem.get("height"))
    width = pw - 2*margin
    height = ph - 2*margin
    s = min((width/pw), (height/ph))
    grp.set("transform", f"translate({x} {y}) scale({s} {s})")
    # current_app.logger.info(f"gen_1: qrcode group: translate({x} {y}) scale({s} {s})")

    return ET.tostring(root)


def _gen_3(pk, svg_qrcode, department):
    tree = ET.parse("parking-torwar-pass-id-template-3.svg")
    root = tree.getroot()

    # nr identyfikatora
    elem = root.find(".//*[@id='numerIdentyfikatora']")
    elem.text = str(pk.pass_nr)

    # nazwa działu
    elem = root.find(".//*[@id='department']")
    elem.text = f"{department.lang} - {department.name}"

    # numery rejestracyjne
    elem = root.find(".//*[@id='d1rejnum']")
    elem.text = pk.regnum1
    elem = root.find(".//*[@id='d2rejnum']")
    elem.text = pk.regnum2
    elem = root.find(".//*[@id='d3rejnum']")
    elem.text = pk.regnum3

    # qrcode
    # current_app.logger.info(f"gen_3: qrcode: {svg_qrcode}")
    elem = root.find(".//*[@id='layer1']")
    qrcode_tree = ET.fromstring(svg_qrcode)
    grp = ET.SubElement(elem, "svg:g")
    grp.set("id", "g1864")
    grp.set("style", "stroke-width:1.35465")
    grp.append(qrcode_tree)

    # pozycjonowanie
    margin = 5
    parent_elem = root.find(".//*[@id='qrCode']")
    x = float(parent_elem.get("x")) + margin
    y = float(parent_elem.get("y")) + margin
    pw = float(parent_elem.get("width"))
    ph = float(parent_elem.get("height"))
    width = pw - 2*margin
    height = ph - 2*margin
    s = min((width/pw), (height/ph))
    grp.set("transform", f"translate({x} {y}) scale({s} {s})")
    # current_app.logger.info(f"gen_3: qrcode group: translate({x} {y}) scale({s} {s})")

    return ET.tostring(root)
