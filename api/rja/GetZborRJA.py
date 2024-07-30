from flask import current_app
from sql import Zbory, Rozklad, SRA
from api.createShortBusID import createShortBusID


def _zbor_get_rja(zbor_id):
    try:
        res = []
        zbor = Zbory.query.filter_by(id=zbor_id).one()
        all_sra = SRA.query.filter_by(zbor_id=zbor.id).all()
        for sra in all_sra:
            rja = Rozklad.query.filter_by(sra_id=sra.id).one()
            item = dict()
            item['sector'] = rja.sektor_id
            item['ident'] = createShortBusID(letter=sra.prefix, sektor=rja.sektor_id, tura=rja.tura, static_identifier=sra.static_identifier)
            item['zbor'] = zbor.name
            item['lp'] = sra.lp
            item['d1'] = rja.d1.strftime("%H:%M") if rja.d1 is not None else ''
            item['d2'] = rja.d2.strftime("%H:%M") if rja.d2 is not None else ''
            item['d3'] = rja.d3.strftime("%H:%M") if rja.d3 is not None else ''
            res.append(item)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"RJA: get congregation rja exception: {e}")
        return f"{e}", 500
