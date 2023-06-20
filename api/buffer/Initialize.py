from flask import current_app
from sql import Rozklad, SRA, Sektory, Terminale, Zbory
from .helpers import arrive_today


def _buffer_initialize(bid):
    """
    Zwraca wszystkie statyczne informacje na temat bufora oraz listę przypisanych do niego autobusów
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
        res['name'] = select_buffer.name

        # buffers' buses
        buses = []
        for rja in all_rja:
            if not arrive_today(rja):
                continue

            tmp = dict()
            tmp['id'] = rja.id
            tmp['tura'] = rja.tura
            tmp['arrive'] = _arrive_by_day(rja)
            tmp['departure'] = _departure_by_day(rja)

            sra = SRA.query.filter_by(id=rja.sra_id).one()
            _sra = dict()
            _sra['id'] = sra.id
            _sra['lp'] = sra.lp
            # _sra['pilot'] = TODO: maybe
            tmp['sra'] = _sra

            zbor = Zbory.query.filter_by(id=sra.zbor_id).one()
            _congregation = dict()
            _congregation['name'] = zbor.name
            _congregation['lang'] = zbor.lang
            tmp['congregation'] = _congregation

            sektor = _find_sector(select_sectors, rja.sektor_id)
            _sector = dict()
            _sector['name'] = sektor.name
            tmp['sector'] = _sector

            buses.append(tmp)
        res['buses'] = buses

        return res, 200
    except Exception as e:
        current_app.logger.error(f"Buffer: initialize: id={bid}, exception='{e}'")
        return f"{e}", 500


def _arrive_by_day(rja):
    active_day = current_app.config['ACTIVE_DAY']
    if active_day == 'd1':
        return rja.a1.strftime("%H:%M") if rja.a1 is not None else ''
    if active_day == 'd2':
        return rja.a2.strftime("%H:%M") if rja.a2 is not None else ''
    if active_day == 'd3':
        return rja.a3.strftime("%H:%M") if rja.a3 is not None else ''
    return rja.a1 if rja.a1 is not None else ''


def _departure_by_day(rja):
    active_day = current_app.config['ACTIVE_DAY']
    if active_day == 'd1':
        return rja.d1.strftime("%H:%M") if rja.d1 is not None else ''
    if active_day == 'd2':
        return rja.d2.strftime("%H:%M") if rja.d2 is not None else ''
    if active_day == 'd3':
        return rja.d3.strftime("%H:%M") if rja.d3 is not None else ''
    return rja.d1 if rja.d1 is not None else ''


def _find_sector(lst, sid):
    for i in lst:
        if i.id == sid:
            return i
    return None
