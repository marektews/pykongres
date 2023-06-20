from flask import current_app
from sql import Rozklad, SRA, Zbory, Sektory


def _sector_schedule(sid):
    try:
        res = []
        rja = Rozklad.query.filter_by(sektor_id=sid).order_by(Rozklad.tura).all()
        for item in rja:
            tmp = dict()
            tmp['tura'] = item.tura

            tmp['d1'] = {"arrive": _time_to_str(item.a1), "departure": _time_to_str(item.d1)}
            tmp['d2'] = {"arrive": _time_to_str(item.a2), "departure": _time_to_str(item.d2)}
            tmp['d3'] = {"arrive": _time_to_str(item.a3), "departure": _time_to_str(item.d3)}

            sector = Sektory.query.filter_by(id=item.sektor_id).one()
            sra = SRA.query.filter_by(id=item.sra_id).one()
            bus = dict()
            bus['lp'] = sra.lp
            bus['ident'] = sector.name.replace('x', str(item.tura))
            tmp['bus'] = bus

            zbor = Zbory.query.filter_by(id=sra.zbor_id).one()
            _zbor = dict()
            _zbor['lang'] = zbor.lang
            _zbor['name'] = zbor.name
            tmp['congregation'] = _zbor

            res.append(tmp)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"SECTOR: get schedule: sector={sid}, exception='{e}'")
        return f"{e}", 500


def _time_to_str(time):
    return time.strftime("%H:%M") if time is not None else ''