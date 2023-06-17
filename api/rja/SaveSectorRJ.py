from flask import current_app
from sql import db, Rozklad


def _save_buses_of_sector(json):
    try:
        db.session.begin()
        # kasowanie poprzedniej listy
        Rozklad.query.filter_by(sektor_id=json['sid']).delete()
        # wstawienie nowej listy
        for item in json['rja']:
            rja = Rozklad(sra_id=item['sra_id'], sektor_id=item['sid'],
                          d1=item['d1'], d2=item['d2'], d3=item['d3'],
                          a1=item['a1'], a2=item['a2'], a3=item['a3'])
            db.session.add(rja)
        db.session.commit()
        return "", 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"RJA: save exception: {e}")
        return f"{e}", 500
