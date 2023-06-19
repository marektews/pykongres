from flask import current_app
from sql import db, DzialyPK
from datetime import datetime


def _pk_check(args):
    """
    Weryfikowanie identyfikatorów na parking księżycowy
    :args: data=pk-<pass nr>-<regnum1>-<regnum2>-<regnum3>
    :return:
        200 - może wjechać,
        400 - brak wymaganego argumentu,
        406 - argument ma niepoprawny format,
        403 - nie może wjechać - identyfikator już użyty
        404 - brak zarejestrowanego identyfikatora na ten numer rejestracyjny pojazdu,
        500 - błąd serwera - spróbuj ponownie
    """
    try:
        # weryfikowanie poprawności przesłanego identyfikatora
        if 'data' not in args:
            return "brak wymaganego argumentu", 400
        sl = args['data'].split('-')
        if len(sl) != 5:
            return "argument ma niepoprawny format", 406

        pk = DzialyPK.query.filter_by(pass_nr=sl[1], regnum1=sl[2]).first()
        if pk is None:
            return "brak zarejestrowanego identyfikatora na ten numer rejestracyjny pojazdu", 404
        if pk.regnum2 is not None and pk.regnum2 != sl[3]:
            return "brak zarejestrowanego identyfikatora na ten numer rejestracyjny pojazdu", 404
        if pk.regnum3 is not None and pk.regnum3 != sl[4]:
            return "brak zarejestrowanego identyfikatora na ten numer rejestracyjny pojazdu", 404
        # weryfikowanie użycia
        active_day = current_app.config['ACTIVE_DAY']
        if active_day == 'd1':
            if pk.d1 is not None:
                return f"identyfikator już użyty: {pk.d1}", 403
            else:
                pk.d1 = datetime.now()
                db.session.commit()
                return "może wjechać", 200

        elif active_day == 'd2':
            if pk.d2 is not None:
                return f"identyfikator już użyty: {pk.d2}", 403
            else:
                pk.d2 = datetime.now()
                db.session.commit()
                return "może wjechać", 200

        elif active_day == 'd3':
            if pk.d3 is not None:
                return f"identyfikator już użyty: {pk.d3}", 403
            else:
                pk.d3 = datetime.now()
                db.session.commit()
                return "może wjechać", 200

        return "???", 500

    except Exception as e:
        current_app.logger.error(f"PK check pass id: exception: {e}")
        return f"{e}", 500
