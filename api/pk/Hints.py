from flask import current_app
from sql import Dzialy


def _pk_hints_all():
    try:
        res = []
        dzialy = Dzialy.query.all()
        for d in dzialy:
            tmp = dict()
            tmp['id'] = d.id
            tmp['lang'] = d.lang
            tmp['name'] = d.name
            tmp['tura'] = d.tura
            res.append(tmp)
        return res, 200

    except Exception as e:
        current_app.logger.error(f"PK: get HINTS list exception: {e}")
        return f"{e}", 500
