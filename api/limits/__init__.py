from flask import Blueprint, current_app, request
from sql import Zbory, Dzialy, db

limits_api = Blueprint('limits', __name__, url_prefix='/limits')


@limits_api.route('/zbory', methods=['GET'])
def get_limits_zbory():
    try:
        res = []
        all_zbory = Zbory.query.all()
        for zbor in all_zbory:
            tmp = dict()
            tmp['id'] = zbor.id
            tmp['number'] = zbor.number
            tmp['name'] = zbor.name
            tmp['lang'] = zbor.lang
            tmp['plimit'] = zbor.plimit
            tmp['tura'] = zbor.tura
            res.append(tmp)
        return res
    except Exception as e:
        current_app.logger.error(f"LIMITS: zbory: exception: {e}")
        return f"{e}", 500


@limits_api.route('/zbory/setlimit', methods=['POST'])
def set_limit_zbory():
    try:
        zbor_id = request.json['zbor_id']
        plimit = request.json['plimit']
        db.session.begin()
        zbor = Zbory.query.filter_by(id=zbor_id).first()
        if zbor:
            zbor.plimit = plimit
            db.session.commit()
            return {}, 200
        else:
            return {}, 404
    except Exception as e:
        current_app.logger.error(f"LIMITS: zbory set limit: exception: {e}")
        db.session.rollback()
        return f"{e}", 500


@limits_api.route('/dzialy', methods=['GET'])
def get_limits_dzialy():
    try:
        res = []
        all_dzialy = Dzialy.query.all()
        for dzial in all_dzialy:
            tmp = dict()
            tmp['id'] = dzial.id
            tmp['lang'] = dzial.lang
            tmp['name'] = dzial.name
            tmp['plimit'] = dzial.plimit
            tmp['tura'] = dzial.tura
            res.append(tmp)
        return res
    except Exception as e:
        current_app.logger.error(f"LIMITS: dzialy: exception: {e}")
        return f"{e}", 500


@limits_api.route('/dzialy/setlimit', methods=['POST'])
def set_limit_dzialy():
    try:
        dzial_id = request.json['dzial_id']
        plimit = request.json['plimit']
        db.session.begin()
        dzial = Dzialy.query.filter_by(id=dzial_id).first()
        if dzial:
            dzial.plimit = plimit
            db.session.commit()
            return {}, 200
        else:
            return {}, 404
    except Exception as e:
        current_app.logger.error(f"LIMITS: dzialy set limit: exception: {e}")
        db.session.rollback()
        return f"{e}", 500
