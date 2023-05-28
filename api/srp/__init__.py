import io
from flask import Blueprint, request, current_app, send_file
from flask_login import login_required
from sql import db, SRP, Zbory
from qr import gen_qrcode
from svglib.svglib import svg2rlg
from svglib.fonts import register_font
from reportlab.graphics import renderPDF
from .generate import gen_1, gen_3

system_rej_poj_api = Blueprint('srp', __name__, url_prefix='/srp')


@login_required
@system_rej_poj_api.route('/isfreepass/<congregation>')
def is_free_pass_id(congregation):
    """
    Sprawdzanie czy jest jeszcze wolny identyfikator do wykorzystania
    :return: HTTP codes: 200 | 404
    """
    try:
        _zbor = Zbory.query.filter_by(name=congregation).first()
        c = SRP.query.filter_by(zbor_id=_zbor.id).count()

        if c < 4:
            return "", 200
        else:
            return "", 404
    except Exception as e:
        current_app.logger.error(f"SRA check free pass id: exception: {e}")
        db.session.rollback()
        return f"{e}", 500


@login_required
@system_rej_poj_api.route('/generate', methods=['POST'])
def generate_pass_id():
    """
    Generowanie przepustki parkingowej

    Struktura danych:
        "congregation": "<nazwa zboru>",
        "regnum1": "<numer rejestracyjny na piątek lub na wszystkie dni>",
        "regnum2": "" | None,
        "regnum3": "" | None,
    """
    try:
        data = request.json
        congregation = data['congregation']
        regnum1 = data['regnum1']
        regnum2 = data['regnum2']
        regnum3 = data['regnum3']

        db.session.begin()

        srp = SRP()

        zbor = Zbory.query.filter_by(name=congregation).first()
        srp.zbor_id = zbor.id
        srp.regnum1 = regnum1
        if len(regnum2) > 0:
            srp.regnum2 = regnum2
        if len(regnum3) > 0:
            srp.regnum3 = regnum3

        db.session.add(srp)
        db.session.flush()
        db.session.commit()
        current_app.logger.info(f"SRA generate pass id finished")

        res = dict()
        res["passID"] = srp.id
        return res, 200
    except Exception as e:
        current_app.logger.error(f"SRA generate pass id: exception: {e}")
        db.session.rollback()
        return f"{e}", 500


@login_required
@system_rej_poj_api.route('/update', methods=['POST'])
def update_pass_id():
    """
    Aktualizacja przepustki parkingowej

    Struktura danych:
        "passid": "<private key rekordu>",
        "regnum1": "<numer rejestracyjny na piątek lub na wszystkie dni>",
        "regnum2": "" | None,
        "regnum3": "" | None,
    """
    try:
        pass_id = request.json['passid']
        regnum1 = request.json['regnum1']
        regnum2 = request.json['regnum2']
        regnum3 = request.json['regnum3']

        db.session.begin()

        srp = SRP.query.filter_by(id=pass_id).first()
        srp.regnum1 = regnum1
        srp.regnum2 = regnum2 if len(regnum2) > 0 else None
        srp.regnum3 = regnum3 if len(regnum3) > 0 else None
        db.session.commit()
        current_app.logger.info(f"SRA update pass id finished")
        return "", 200
    except Exception as e:
        current_app.logger.error(f"SRA update pass id: exception: {e}")
        db.session.rollback()
        return f"{e}", 500


@login_required
@system_rej_poj_api.route('/download/<pass_id>')
def download_pass_id(pass_id):
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


@login_required
@system_rej_poj_api.route('/find', methods=['POST'])
def find_pass_id():
    try:
        congregation = request.json['congregation']
        regnum = request.json['regnum']

        zbor = Zbory.query.filter_by(name=congregation).first()
        srp = SRP.query\
            .filter_by(zbor_id=zbor.id)\
            .filter((SRP.regnum1 == regnum) | (SRP.regnum2 == regnum) | (SRP.regnum3 == regnum))\
            .first()

        if srp is not None:
            res = dict()
            res['pass_id'] = srp.id
            return res, 200
        else:
            return "", 404

    except Exception as e:
        current_app.logger.error(f"SRA find pass id: exception: {e}")
        return f"{e}", 500
