from flask import current_app
from sql import Sektory


def _sector_initialize(sid):
    try:
        sector = Sektory.query.filter_by(id=sid).one()
        res = dict()
        res['id'] = sector.id
        res['name'] = sector.name
        return res, 200
    except Exception as e:
        current_app.logger.error(f"SECTOR: initialize: sector={sid}, exception='{e}'")
        return f"{e}", 500
