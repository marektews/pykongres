from flask import current_app
from sql import DzialyPK


def _pk_read(pk_id):
    """
    Odczyt stanu identyfikatora
    :param pk_id: private key w bazie
    :return: {
        "passid": "<private key rekordu>",
        "pass_nr": <numer identyfikatora>,
        "regnum1": "<numer rejestracyjny na piątek lub na wszystkie dni>",
        "regnum2": "<numer rejestracyjny na sobotę>",
        "regnum3": "<numer rejestracyjny na niedzielę>",
    }
    """
    try:
        dpk = DzialyPK.query.filter_by(id=pk_id).first()
        res = dict()
        res["passid"] = dpk.id
        res["pass_nr"] = dpk.pass_nr
        res["regnum1"] = dpk.regnum1
        res["regnum2"] = dpk.regnum2 if dpk.regnum2 is not None else ''
        res["regnum3"] = dpk.regnum3 if dpk.regnum3 is not None else ''
        return res, 200
    except Exception as e:
        current_app.logger.error(f"PK update pass id: exception: {e}")
        return f"{e}", 500
