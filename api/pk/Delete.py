from flask import current_app
from sql import db, DzialyPK


def _pk_delete(pk_id):
    try:
        db.session.begin()
        dpk = DzialyPK.query.filter_by(id=pk_id).one()
        db.session.delete(dpk)
        db.session.commit()
        current_app.logger.info(f"PK pass id {dpk.pass_nr} - {dpk.regnum1} deleted")
        return "", 200
    except Exception as e:
        current_app.logger.error(f"PK deleting pass id: exception: {e}")
        return f"{e}", 500
