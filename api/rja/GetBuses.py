from flask import current_app
from sql import Bus


def _buses_get_list():
    try:
        buses = Bus.query.all()
        res = []
        for b in buses:
            tmp = dict()
            tmp['id'] = b.id
            tmp['type'] = b.type
            tmp['distance'] = b.distance
            tmp['parking'] = b.parking_mode
            res.append(tmp)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"RJA: get BUSes list exception: {e}")
        return f"{e}", 500
