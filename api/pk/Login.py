from flask import current_app
from sql import Dzialy


def _pk_login(login, passwd):
    try:
        d = Dzialy.query.filter_by(id=login, password=passwd).first()
        if d is not None:
            return "", 200
        else:
            return "", 403
    except Exception as e:
        current_app.logger.error(f"PK: login exception: {e}")
        return f"{e}", 500
