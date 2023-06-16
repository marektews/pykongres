from flask import current_app, send_file
from sql import DzialyPK, Dzialy
from .generate import gen_1, gen_3
from qr import gen_qrcode
from svglib.svglib import svg2rlg
from svglib.fonts import register_font
from reportlab.graphics import renderPDF
import io


def _pk_download(pass_id):
    try:
        srp = SRP.query.filter_by(id=pass_id).first()
        is_one_car = True

        qr_src_data = f"{srp.pass_nr}-{srp.regnum1}"
        if srp.regnum2 is not None and len(srp.regnum2) > 0:
            is_one_car = False
            qr_src_data += f"-{srp.regnum2}"
        else:
            qr_src_data += f"-{srp.regnum1}"
        if srp.regnum3 is not None and len(srp.regnum3) > 0:
            is_one_car = False
            qr_src_data += f"-{srp.regnum3}"
        else:
            qr_src_data += f"-{srp.regnum1}"

        qr_code = gen_qrcode(qr_src_data)
        pos = qr_code.find('<svg:svg')
        svg_qrcode = qr_code[pos:]

        zbor = Zbory.query.filter_by(id=srp.zbor_id).first()

        if is_one_car:
            svg = gen_1(srp, svg_qrcode, zbor)
        else:
            svg = gen_3(srp, svg_qrcode, zbor)

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
        current_app.logger.error(f"SRA download pass id: exception: {e}")
        return f"{e}", 500
