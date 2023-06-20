from flask import current_app
from sql import db, SRP, Zbory


def _create_pass_id(json):
    try:
        congregation = json['congregation']
        regnum1 = json['regnum1']
        regnum2 = json['regnum2']
        regnum3 = json['regnum3']

        db.session.begin()
        zbor = Zbory.query.filter_by(name=congregation).one()

        # poszukiwanie nieużywanego jeszcze numeru identyfikatora
        used_numbers = [n+1 for n in range(zbor.plimit)]
        tmp = SRP.query.filter_by(zbor_id=zbor.id).all()
        for item in tmp:
            used_numbers.remove(item.pass_nr)
            # testowanie czy pojazd nie występuje już na innym identyfikatorze
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
        srp = SRP()
        srp.zbor_id = zbor.id
        srp.pass_nr = used_numbers[0]
        srp.regnum1 = regnum1
        if len(regnum2) > 0:
            srp.regnum2 = regnum2
        if len(regnum3) > 0:
            srp.regnum3 = regnum3

        db.session.add(srp)
        db.session.commit()
        current_app.logger.info(f"SRP generate pass id finished")

        res = dict()
        res["passID"] = srp.id
        return res, 200
    except Exception as e:
        current_app.logger.error(f"SRP generate pass id: exception: {e}")
        db.session.rollback()
        return f"{e}", 500
