from flask import current_app
from sql import db, Dzialy, DzialyPK


def _pk_create(json):
    try:
        dep_id = json['dep_id']
        regnum1 = json['regnum1']
        regnum2 = json['regnum2']
        regnum3 = json['regnum3']

        db.session.begin()
        dzial = Dzialy.query.filter_by(id=dep_id).one()

        # testowanie czy pojazd nie wystepuje już na innym identyfikatorze
        used_numbers = []
        tmp = DzialyPK.query.filter_by(dzial_id=dzial.id).all()
        for item in tmp:
            used_numbers.append(item.pass_nr)
            if regnum1 == item.regnum1 or regnum1 == item.regnum2 or regnum1 == item.regnum3:
                db.session.rollback()
                return "", 400
            if regnum2 is not None and (regnum2 == item.regnum1 or regnum2 == item.regnum2 or regnum2 == item.regnum3):
                db.session.rollback()
                return "", 400
            if regnum3 is not None and (regnum3 == item.regnum1 or regnum3 == item.regnum2 or regnum3 == item.regnum3):
                db.session.rollback()
                return "", 400

        # tworzenie nowego wpisu z nowym identyfikatorem
        dpk = DzialyPK()
        dpk.dzial_id = dzial.id
        dpk.pass_nr = _find_free_pass_nr(used_numbers)
        dpk.regnum1 = regnum1
        if len(regnum2) > 0:
            dpk.regnum2 = regnum2
        if len(regnum3) > 0:
            dpk.regnum3 = regnum3

        db.session.add(dpk)
        db.session.commit()
        current_app.logger.info(f"PK generate pass id finished")

        res = dict()
        res["passID"] = dpk.id
        return res, 200

    except Exception as e:
        current_app.logger.error(f"PK generate pass id: exception: {e}")
        db.session.rollback()
        return f"{e}", 500


def _find_free_pass_nr(used_numbers):
    used_numbers.sort()
    tmp = 0
    for i in used_numbers:
        if tmp + 1 != i:
            return tmp + 1
        tmp = i
    return len(used_numbers) + 1
