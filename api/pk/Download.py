from flask import current_app, send_file
from sql import DzialyPK, Dzialy
from qr import gen_qrcode
from .generate import _gen_1, _gen_3
from svglib.svglib import svg2rlg
from svglib.fonts import register_font
from reportlab.graphics import renderPDF
import io


def _pk_download(pk_id):
    try:
        pk = DzialyPK.query.filter_by(id=pk_id).one()
        is_one_car = True

        qr_src_data = f"pk-{pk.pass_nr}-{pk.regnum1}"
        if pk.regnum2 is not None and len(pk.regnum2) > 0:
            is_one_car = False
            qr_src_data += f"-{pk.regnum2}"
        else:
            qr_src_data += f"-{pk.regnum1}"
        if pk.regnum3 is not None and len(pk.regnum3) > 0:
            is_one_car = False
            qr_src_data += f"-{pk.regnum3}"
        else:
            qr_src_data += f"-{pk.regnum1}"

        qr_code = gen_qrcode(qr_src_data)
        pos = qr_code.find('<svg:svg')
        svg_qrcode = qr_code[pos:]

        department = Dzialy.query.filter_by(id=pk.dzial_id).one()

        if is_one_car:
            svg = _gen_1(pk, svg_qrcode, department)
        else:
            svg = _gen_3(pk, svg_qrcode, department)

        register_font("Roboto", "Roboto-Regular.ttf")
        register_font("Roboto-Bold", "Roboto-Bold.ttf")
        fd_svg = io.BytesIO()
        fd_svg.write(svg)
        fd_svg.seek(0)
        drawing = svg2rlg(fd_svg)
        fd_pdf = io.BytesIO()
        renderPDF.drawToFile(drawing, fd_pdf)
        fd_pdf.seek(0)
        return send_file(fd_pdf, mimetype="application/pdf", as_attachment=True, download_name="identyfikator-parkingowy.pdf")

    except Exception as e:
        current_app.logger.error(f"PK download pass id: exception: {e}")
        return f"{e}", 500

