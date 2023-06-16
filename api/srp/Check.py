from flask import current_app
from sql import db, SRP
from datetime import datetime


def _srp_check(args):
    """
    Weryfikowanie identyfikatorów na parking pod trybuną
    :args: data=<pass nr>-<regnum1>-<regnum2>-<regnum3>
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
        if len(sl) != 4:
            return "argument ma niepoprawny format", 406

        srp = SRP.query.filter_by(pass_nr=sl[0], regnum1=sl[1]).first()
        if srp is None:
            return "brak zarejestrowanego identyfikatora na ten numer rejestracyjny pojazdu", 404
        if srp.regnum2 is not None and srp.regnum2 != sl[2]:
            return "brak zarejestrowanego identyfikatora na ten numer rejestracyjny pojazdu", 404
        if srp.regnum3 is not None and srp.regnum3 != sl[3]:
            return "brak zarejestrowanego identyfikatora na ten numer rejestracyjny pojazdu", 404
        # weryfikowanie użycia
        active_day = current_app.config['ACTIVE_DAY']
        if active_day == 'd1':
            if srp.d1 is not None:
                return f"identyfikator już użyty: {srp.d1}", 403
            else:
                srp.d1 = datetime.now()
                db.session.commit()
                return "może wjechać", 200

        elif active_day == 'd2':
            if srp.d2 is not None:
                return f"identyfikator już użyty: {srp.d2}", 403
            else:
                srp.d2 = datetime.now()
                db.session.commit()
                return "może wjechać", 200

        elif active_day == 'd3':
            if srp.d3 is not None:
                return f"identyfikator już użyty: {srp.d3}", 403
            else:
                srp.d3 = datetime.now()
                db.session.commit()
                return "może wjechać", 200

        return "???", 500

    except Exception as e:
        current_app.logger.error(f"SRP check pass id: exception: {e}")
        return f"{e}", 500
