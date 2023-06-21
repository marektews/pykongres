from flask import current_app
from sql import db, SOA


def _sector_notification(rja_id, status):
    try:
        db.session.begin()
        soa = SOA(rja_id=rja_id, status=status)
        db.session.add(soa)
        db.session.commit()

        ntf = dict()
        ntf['rja_id'] = soa.rja_id
        ntf['status'] = soa.status
        ntf['ts'] = soa.ts.strftime("%x %X")

        return ntf, 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Sector: '{status}' notification: id={rja_id}, exception='{e}'")
        return f"{e}", 500
