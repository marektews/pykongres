from flask import current_app
from sql import Rozklad, SRA, Zbory


def _buses_get_used(json):
    try:
        tura = json['tura']
        all_rja = Rozklad.query.all()
        res = []
        for rja in all_rja:
            sra = SRA.query.filter_by(id=rja.sra_id).first()
            if sra:
                zbor = Zbory.query.filter_by(id=sra.zbor_id, tura=tura).first()
                if zbor is not None:
                    res.append(rja.sra_id)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"RJA: get BUSes used exception: {e}")
        return f"{e}", 500
