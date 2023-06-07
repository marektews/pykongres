from flask import current_app
from sql import Zbory, SRP


def _find_pass_id(json):
    try:
        congregation = json['congregation']
        regnum = json['regnum']

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
