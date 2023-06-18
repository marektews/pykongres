import io
from flask import current_app, send_file
from sql import SRA, Zbory, Rozklad, Sektory, Terminale
from svglib.svglib import svg2rlg
from svglib.fonts import register_font
from reportlab.graphics import renderPDF
from .generate import gen


def _ia_download(sra_id):
    try:
        sra = SRA.query.filter_by(id=sra_id).one()
        congregation = Zbory.query.filter_by(id=sra.zbor_id).one()
        rja = Rozklad.query.filter_by(sra_id=sra.id).one()
        sector = Sektory.query.filter_by(id=rja.sektor_id).one()
        terminal = Terminale.query.filter_by(id=sector.tid).one()

        all_departures = Rozklad.query.filter_by(sektor_id=rja.sektor_id).order_by(Rozklad.d1).all()
        order = [item.sra_id for item in all_departures]
        tura = order.index(rja.sra_id) + 1

        svg = gen(congregation, rja, sector, terminal, str(tura))

        register_font("Lato-Bold", "Lato-Bold.ttf")
        fd_svg = io.BytesIO()
        fd_svg.write(svg)
        fd_svg.seek(0)
        drawing = svg2rlg(fd_svg)
        fd_pdf = io.BytesIO()
        renderPDF.drawToFile(drawing, fd_pdf)
        fd_pdf.seek(0)
        return send_file(fd_pdf, mimetype="application/pdf", as_attachment=True, download_name="identyfikator-autokaru.pdf")

    except Exception as e:
        current_app.logger.error(f"IA download pass id: exception: {e}")
        return f"{e}", 500
