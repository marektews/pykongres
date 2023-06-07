from flask import current_app
from sql import Terminale, Sektory


def _terminal_full_info(tid):
    try:
        res = dict()
        t = Terminale.query.filter_by(id=tid).one()
        res["tid"] = t.id
        res["name"] = t.name

        if t.is_buffer == 0:
            res["buffer"] = False
            res["sectors"] = []
            sectors = Sektory.query.filter_by(tid=tid).all()
            for s in sectors:
                tmp = dict()
                tmp["sid"] = s.id
                tmp["name"] = s.name
                res["sectors"].append(tmp)
        else:
            res["buffer"] = True

        return res, 200
    except Exception as e:
        current_app.logger.error(f"Get TERMINAL full info exception: {e}")
        return f"{e}", 500

