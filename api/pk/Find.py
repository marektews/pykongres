from flask import current_app
from sql import DzialyPK


def _pk_find(json):
    try:
        dep_id = json['dep_id']
        regnum = json['regnum']

        dpk = DzialyPK.query \
            .filter_by(dzial_id=dep_id) \
            .filter((DzialyPK.regnum1 == regnum) | (DzialyPK.regnum2 == regnum) | (DzialyPK.regnum3 == regnum)) \
            .first()

        if dpk is not None:
            res = dict()
            res['pk_id'] = dpk.id
            return res, 200
        else:
            return "", 404

    except Exception as e:
        current_app.logger.error(f"PK find pass id: exception: {e}")
        return f"{e}", 500
