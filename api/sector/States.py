from flask import current_app
from sql import Rozklad, SOA
from .helpers import arrive_today


def _sector_states(sid):
    """
    Zwraca statusy wszystkich autokarów przypisanych do tego sektora
    """
    try:
        # wszystkie autobusy, które przypisane są do bufora
        all_rja = Rozklad.query.filter_by(sektor_id=sid).order_by(Rozklad.tura, Rozklad.sektor_id).all()

        # sektor info
        res = dict()
        res['sid'] = sid

        # buses states
        states = dict()
        for rja in all_rja:
            if not arrive_today(rja):
                continue

            soa = SOA.query.filter_by(rja_id=rja.id).order_by(SOA.ts.desc(), SOA.id.desc()).first()
            if soa is not None:
                tmp = dict()
                tmp['status'] = soa.status
                tmp['ts'] = soa.ts.strftime("%x %X")
                states[soa.rja_id] = tmp

        res['states'] = states

        return res, 200
    except Exception as e:
        current_app.logger.error(f"Sector: status: id={sid}, exception='{e}'")
        return f"{e}", 500
