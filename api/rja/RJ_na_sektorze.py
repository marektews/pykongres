from flask import current_app
from sql import Rozklad


def _get_buses_of_sector(sid):
    try:
        res = []
        rj_sektor = Rozklad.query.filter_by(sektor_id=sid).order_by(Rozklad.d1).all()
        for item in rj_sektor:
            tmp = dict()
            tmp['id'] = item.id
            tmp['sra_id'] = item.sra_id
            tmp['sid'] = item.sektor_id
            tmp['bufor_id'] = item.bufor_id
            tmp['d1'] = item.d1.strftime("%H:%M")
            tmp['d2'] = item.d2.strftime("%H:%M")
            tmp['d3'] = item.d3.strftime("%H:%M")
            res.append(tmp)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"RJA: get BUSES of sector exception: {e}")
        return f"{e}", 500
