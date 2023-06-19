from flask import current_app
from sql import db, Rozklad


def _save_buses_of_sector(json):
    try:
        db.session.begin()
        # kasowanie poprzedniej listy
        Rozklad.query.filter_by(sektor_id=json['sid']).delete()
        # wstawienie nowej listy
        tura = 0
        for item in json['rja']:
            tura += 1
            rja = Rozklad(sra_id=item['sra_id'],
                          sektor_id=item['sid'],
                          tura=tura,
                          d1=item['d1'] if len(item['d1']) > 0 else None,
                          d2=item['d2'] if len(item['d2']) > 0 else None,
                          d3=item['d3'] if len(item['d3']) > 0 else None,
                          a1=item['a1'] if len(item['a1']) > 0 else None,
                          a2=item['a2'] if len(item['a2']) > 0 else None,
                          a3=item['a3'] if len(item['a3']) > 0 else None)
            db.session.add(rja)
        db.session.commit()
        return "", 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"RJA: save exception: {e}")
        return f"{e}", 500
