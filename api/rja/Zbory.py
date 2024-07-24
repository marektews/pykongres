from flask import current_app
from sql import Zbory


def _zbory_get_list(json):
    try:
        tura = json['tura']
        zbory = Zbory.query.order_by(Zbory.lang, Zbory.name).filter_by(tura=tura).all()
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
        current_app.logger.error(f"RJA: get ZBORY list exception: {e}")
        return f"{e}", 500
