from flask import current_app
from sql import SRA, Zbory


def _sra_get_list(json):
    try:
        tura = json['tura']
        sra = SRA.query.all()
        res = []
        for s in sra:
            zbor = Zbory.query.filter_by(id=s.zbor_id, tura=tura)
            if zbor is not None:
                tmp = dict()
                tmp['id'] = s.id
                tmp['zbor_id'] = s.zbor_id
                tmp['bus_id'] = s.bus_id
                tmp['lp'] = s.lp
                tmp['canceled'] = False if s.canceled == 0 else True
                tmp['prefix'] = s.prefix
                tmp['static_identifier'] = s.static_identifier
                res.append(tmp)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"RJA: get SRA list exception: {e}")
        return f"{e}", 500
