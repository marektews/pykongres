from flask import current_app
from sql import db, Rozklad, SRA, Zbory


def _save_buses_of_sector(json):
    try:
        tura = json['tura']
        db.session.begin()

        # kasowanie poprzedniej listy
        lst_delete = []
        filter_rja = Rozklad.query.filter_by(sektor_id=json['sid']).all()
        for rja in filter_rja:
            sra = SRA.query.filter_by(id=rja.sra_id).first()
            if sra is not None:
                zbor = Zbory.query.filter_by(id=sra.zbor_id, tura=tura).first()
                if zbor is not None:
                    lst_delete.append(rja.id)

        for rja_id in lst_delete:
            Rozklad.query.filter_by(id=rja_id).delete()

        # wstawienie nowej listy
        sektor_tura = 0
        for item in json['rja']:
            sektor_tura += 1
            rja = Rozklad(sra_id=item['sra_id'],
                          sektor_id=item['sid'],
                          tura=sektor_tura,
                          d1=item['d1'] if len(item['d1']) > 0 else None,
                          d2=item['d2'] if len(item['d2']) > 0 else None,
                          d3=item['d3'] if len(item['d3']) > 0 else None,
                          a1=item['a1'] if len(item['a1']) > 0 else None,
                          a2=item['a2'] if len(item['a2']) > 0 else None,
                          a3=item['a3'] if len(item['a3']) > 0 else None)
            db.session.add(rja)

            # aktualizacja flagi anulowania autokaru
            sra = SRA.query.filter_by(id=rja.sra_id).one()
            sra.canceled = 1 if item['canceled'] else 0

        db.session.commit()
        return "", 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"RJA: save exception: {e}")
        return f"{e}", 500
