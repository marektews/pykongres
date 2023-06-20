from flask import current_app
from sql import Terminale


def _buffers_list():
    """
    Zwraca listę wszystkich buforów.
    """
    try:
        res = []
        buffers = Terminale.query.filter_by(is_buffer=1).order_by(Terminale.name).all()
        for b in buffers:
            tmp = dict()
            tmp["tid"] = b.id
            tmp["name"] = b.name
            res.append(tmp)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"BUFFERS: get list exception: {e}")
        return f"{e}", 500

