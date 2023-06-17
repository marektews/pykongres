from flask import current_app
from sql import DzialyPK


def _pk_load_all():
    try:
        res = []
        all_pk = DzialyPK.query.order_by(DzialyPK.dzial_id, DzialyPK.pass_nr).all()
        for pk in all_pk:
            tmp = dict()
            tmp['id'] = pk.id
            tmp['dep_id'] = pk.dzial_id
            tmp['pass_nr'] = pk.pass_nr
            tmp['regnum1'] = pk.regnum1
            tmp['regnum2'] = pk.regnum2
            tmp['regnum3'] = pk.regnum3
            tmp['registred'] = pk.registered.strftime('%Y-%m-%d %H:%M')
            res.append(tmp)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"PK load all pass ids: exception: {e}")
        return f"{e}", 500
