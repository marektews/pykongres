from flask import current_app
from sql import db, SRA, Pilot, Bus


def _delete_sra(sra_id):
    """
    Kasowanie wpisu
    """
    try:
        db.session.begin()
        sra = SRA.query.filter_by(id=sra_id).one()
        db.session.delete(sra)
        Bus.query.filter_by(id=sra.bus_id).delete()
        Pilot.query.filter_by(id=sra.pilot1_id).delete()
        if sra.pilot2_id is not None:
            Pilot.query.filter_by(id=sra.pilot2_id).delete()
        if sra.pilot3_id is not None:
            Pilot.query.filter_by(id=sra.pilot3_id).delete()
        db.session.commit()
        return "", 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"SRA get table exception: {e}")
        return f"{e}", 500

