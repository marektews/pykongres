from flask import current_app
from sql import SOA, Rozklad
from .helpers import _arrive_today


def _states_repo():
    try:
        res = dict()
        all_rja = Rozklad.query.all()
        for rja in all_rja:
            if not _arrive_today(rja):
                continue

            soa = SOA.query.filter_by(rja_id=rja.id).order_by(SOA.ts.desc(), SOA.id.desc()).first()
            if soa is not None:
                tmp = dict()
                tmp['status'] = soa.status
                tmp['ts'] = soa.ts.strftime("%x %X")
                res[soa.rja_id] = tmp
        return res, 200
    except Exception as e:
        current_app.logger.error(f"Monitoring: loading states exception='{e}'")
        return f"{e}", 500
