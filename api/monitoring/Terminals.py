from flask import current_app
from sql import Terminale, Sektory, SRA, Rozklad, Zbory
from .helpers import _arrive_today, _arrive_by_day, _departure_by_day
from api.createShortBusID import createShortBusID


def _terminals_list():
    try:
        res = []
        terminals = Terminale.query.filter_by(is_buffer=0).order_by(Terminale.name).all()
        for t in terminals:
            tmp = dict()
            tmp["name"] = t.name

            _sektory = []
            sectors = Sektory.query.filter_by(tid=t.id).order_by(Sektory.id).all()
            for s in sectors:
                _tmp = dict()
                _tmp["name"] = s.name
                _sektory.append(_tmp)

                sl = s.name.split()
                sid = sl[1]

                _rja = []
                all_rja = Rozklad.query.filter_by(sektor_id=s.id).order_by(Rozklad.tura).all()
                for rja in all_rja:
                    if not _arrive_today(rja):
                        continue

                    sra = SRA.query.filter_by(id=rja.sra_id).first()
                    zbor = Zbory.query.filter_by(id=sra.zbor_id).first()

                    _tmp2 = dict()
                    _tmp2['id'] = rja.id
                    _tmp2['ident'] = createShortBusID(letter=t.name[0], sektor=sid, tura=str(rja.tura))
                    _tmp2['name'] = zbor.name
                    _tmp2['lp'] = sra.lp
                    _tmp2['tura'] = rja.tura
                    _tmp2['arrive'] = _arrive_by_day(rja)
                    _tmp2['departure'] = _departure_by_day(rja)
                    _rja.append(_tmp2)
                _tmp['rja'] = _rja

            tmp['sectors'] = _sektory

            res.append(tmp)

        return res, 200
    except Exception as e:
        current_app.logger.error(f"Monitoring: terminals static info exception='{e}'")
        return f"{e}", 500
