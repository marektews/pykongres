from flask import current_app
from sql import Rozklad, SRA, Zbory


def _get_buses_of_sector(sid, json):
    try:
        tura = json['tura']
        res = []
        rj_sektor = Rozklad.query.filter_by(sektor_id=sid).order_by(Rozklad.sektor_id, Rozklad.tura).all()
        for item in rj_sektor:
            sra = SRA.query.filter_by(id=item.sra_id).one()
            zbor = Zbory.query.filter_by(id=sra.zbor_id, tura=tura).first()
            if zbor is not None:
                tmp = dict()
                tmp['id'] = item.id
                tmp['sra_id'] = item.sra_id
                tmp['sid'] = item.sektor_id
                tmp['tura'] = item.tura
                tmp['d1'] = item.d1.strftime("%H:%M") if item.d1 is not None else ''
                tmp['d2'] = item.d2.strftime("%H:%M") if item.d2 is not None else ''
                tmp['d3'] = item.d3.strftime("%H:%M") if item.d3 is not None else ''
                tmp['a1'] = item.a1.strftime("%H:%M") if item.a1 is not None else ''
                tmp['a2'] = item.a2.strftime("%H:%M") if item.a2 is not None else ''
                tmp['a3'] = item.a3.strftime("%H:%M") if item.a3 is not None else ''
                tmp['canceled'] = False if sra.canceled == 0 else True
                res.append(tmp)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"RJA: get BUSES of sector exception: {e}")
        return f"{e}", 500
