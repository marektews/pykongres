from flask import current_app
from sql import Terminale


def _get_terminals():
    try:
        res = []
        terminals = Terminale.query.filter_by(isBuffer=0).all()
        for t in terminals:
            tmp = dict()
            tmp["tid"] = t.id
            tmp["name"] = t.name
            res.append(tmp)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"RJA: get TERMINALS list exception: {e}")
        return f"{e}", 500
