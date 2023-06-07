from flask import current_app
from sql import SRP


def _load_all():
    try:
        res = []
        all_srp = SRP.query.all()
        for srp in all_srp:
            tmp = dict()
            tmp['id'] = srp.id
            tmp['zbor_id'] = srp.zbor_id
            tmp['pass_nr'] = srp.pass_nr
            tmp['regnum1'] = srp.regnum1
            tmp['regnum2'] = srp.regnum2
            tmp['regnum3'] = srp.regnum3
            tmp['ts'] = srp.timestamp.strftime('%Y-%m-%d %H:%M')
            res.append(tmp)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"SRA generate pass id: exception: {e}")
        return f"{e}", 500
