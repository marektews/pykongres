from flask import current_app
from sql import db, SRP


def _srp_delete(srp_id):
    try:
        db.session.begin()
        srp = SRP.query.filter_by(id=srp_id).one()
        db.session.delete(srp)
        db.session.commit()
        current_app.logger.info(f"SRP pass id {srp.pass_nr} - {srp.regnum1} deleted")
        return "", 200
    except Exception as e:
        current_app.logger.error(f"SRP deleting pass id: exception: {e}")
        return f"{e}", 500
