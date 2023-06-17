from flask import current_app
from sql import Terminale


def _terminals_list():
    """
    Zwraca listę wszystkich terminali.
    Bufory też należą do terminali, ale są specjalnego przeznaczenia.
    """
    try:
        res = []
        terminals = Terminale.query.order_by(Terminale.name).all()
        for t in terminals:
            tmp = dict()
            tmp["tid"] = t.id
            tmp["name"] = t.name
            tmp["buffer"] = True if t.is_buffer == 1 else False
            res.append(tmp)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"Get TERMINALS list exception: {e}")
        return f"{e}", 500

