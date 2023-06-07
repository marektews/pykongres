from flask import current_app
from sql import Sektory


def _get_sectors(tid):
    try:
        res = []
        sectors = Sektory.query.filter_by(tid=tid).all()
        for s in sectors:
            tmp = dict()
            tmp["sid"] = s.id
            tmp["name"] = s.name
            res.append(tmp)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"RJA: get SECTORS list exception: {e}")
        return f"{e}", 500
