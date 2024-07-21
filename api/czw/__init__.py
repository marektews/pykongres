from flask import Blueprint, current_app, request
from sql import Zbory, Czw, db
from api.whichTura import whichTura

czw_api = Blueprint('czw', __name__, url_prefix='/czw')


@czw_api.route('/init', methods=['GET'])
def initialize():
    try:
        tura = whichTura()
        zbory = Zbory.query.filter_by(tura=tura).all()
        res = []
        for z in zbory:
            tmp = dict()
            tmp['id'] = z.id
            tmp['number'] = z.number
            tmp['name'] = z.name
            tmp['lang'] = z.lang
            tmp['tura'] = z.tura
            res.append(tmp)
        return res, 200

    except Exception as e:
        current_app.logger.error(f"CZW: get ZBORY list exception: {e}")
        return f"{e}", 500


@czw_api.route('/issuing', methods=['POST'])
def issuing():
    try:
        db.session.begin()

        czw = Czw.query \
            .filter_by(nr_ident=request.json['nr_ident'], cancellation=None) \
            .first()

        if czw is not None:
            return {"error": "in used"}, 423

        zbor_name = request.json['zbor']
        zbor = Zbory.query.filter_by(name=zbor_name).one()
        if zbor is None:
            current_app.logger.error(f"CZW: zbor {zbor_name} not found")
            return {"error": f"zbor {zbor_name} not found"}, 404

        czw = Czw()
        czw.nr_rej = request.json['nr_rej']
        czw.phone = request.json['phone']
        czw.nr_ident = request.json['nr_ident']
        czw.zbor_id = zbor.id

        db.session.add(czw)
        db.session.commit()
        return {}, 200

    except Exception as e:
        current_app.logger.error(f"CZW: issuing exception: {e}")
        db.session.rollback()
        return f"{e}", 500


@czw_api.route('/search', methods=['POST'])
def search():
    try:
        if "nr_ident" in request.json:
            czw = Czw.query \
                .filter_by(nr_ident=request.json['nr_ident'], cancellation=None) \
                .first()
        else:
            czw = Czw.query \
                .filter_by(nr_rej=request.json['nr_rej'], cancellation=None) \
                .first()

        if czw is None:
            return request.json, 404

        if czw.cancellation is not None:
            return request.json, 205

        return {
            "phone": czw.phone,
            "nr_rej": czw.nr_rej,
            "nr_ident": czw.nr_ident,
            "issued": czw.issuing,
            "cancellation": czw.cancellation
        }, 200

    except Exception as e:
        current_app.logger.error(f"CZW: search exception: {e}")
        return f"{e}", 500


@czw_api.route('/cancellation', methods=['POST'])
def cancellation():
    try:
        status = 200
        db.session.begin()

        czw = Czw.query \
            .filter_by(nr_ident=request.json["nr_ident"], cancellation=None) \
            .first()
        if czw is not None:
            czw.cancellation = datetime.utcnow()
            db.session.commit()
        else:
            status = 404

        return {}, status

    except Exception as e:
        current_app.logger.error(f"CZW: search exception: {e}")
        db.session.rollback()
        return f"{e}", 500
