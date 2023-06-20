from flask import current_app
from sql import Rozklad, Terminale, Sektory, SOA
from .helpers import arrive_today


def _buffer_states(bid):
    """
    Zwraca statusy wszystkich autokarów przypisanych do tego bufora
    """
    try:
        # opis bufora
        select_buffer = Terminale.query.filter_by(id=bid).one()

        # odnajdź terminal współpracujący z buforem
        select_terminal = Terminale.query.filter_by(assigned_buffer=select_buffer.id).one()

        # sektory współpracujące z buforem
        select_sectors = Sektory.query.filter_by(tid=select_terminal.id).all()

        # wszystkie autobusy, które przypisane są do bufora
        lst = [item.id for item in select_sectors]
        all_rja = Rozklad.query.filter(Rozklad.sektor_id.in_(lst)).order_by(Rozklad.tura, Rozklad.sektor_id).all()

        # buffer info
        res = dict()
        res['bid'] = select_buffer.id

        # buses states
        states = dict()
        for rja in all_rja:
            if not arrive_today(rja):
                continue

            soa = SOA.query.filter_by(rja_id=rja.id).order_by(SOA.ts.desc(), SOA.id.desc()).first()
            if soa is not None:
                tmp = dict()
                tmp['status'] = soa.status
                tmp['ts'] = soa.ts.strftime("%x %X")
                states[soa.rja_id] = tmp

        res['states'] = states

        return res, 200
    except Exception as e:
        current_app.logger.error(f"Buffer: status: id={bid}, exception='{e}'")
        return f"{e}", 500
