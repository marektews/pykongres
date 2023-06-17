import io
from flask import current_app, send_file
from sql import SRA, Zbory
from svglib.svglib import svg2rlg
from svglib.fonts import register_font
from reportlab.graphics import renderPDF
from .generate import gen


def _ia_download(sra_id):
    try:
        sra = SRA.query.filter_by(id=sra_id).one()
        zbor = Zbory.query.filter_by(id=sra.zbor_id).first()

        svg = gen(sra, zbor)

        register_font("Roboto", "Roboto-Regular.ttf")
        register_font("Roboto-Bold", "Roboto-Bold.ttf")
        fd_svg = io.BytesIO()
        fd_svg.write(svg)
        fd_svg.seek(0)
        drawing = svg2rlg(fd_svg)
        fd_pdf = io.BytesIO()
        renderPDF.drawToFile(drawing, fd_pdf, autoSize=0)
        fd_pdf.seek(0)
        return send_file(fd_pdf, mimetype="application/pdf", as_attachment=True, download_name="identyfikator-parkingowy.pdf")

    except Exception as e:
        current_app.logger.error(f"SRA download pass id: exception: {e}")
        return f"{e}", 500
