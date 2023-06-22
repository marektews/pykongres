from flask import current_app
from sql import SOA


def _states_repo():
    try:
        res = dict()
        all_soa = SOA.query.order_by(SOA.ts.desc(), SOA.id.desc()).all()
        for soa in all_soa:
            tmp = dict()
            tmp['status'] = soa.status
            tmp['ts'] = soa.ts.strftime("%x %X")
            res[soa.rja_id] = tmp
        return res, 200
    except Exception as e:
        current_app.logger.error(f"Monitoring: loading states exception='{e}'")
        return f"{e}", 500
