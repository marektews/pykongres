from flask import current_app
from sql import db, DzialyPK


def _pk_update(json):
    try:
        pkid = json['pkid']
        regnum1 = json['regnum1']
        regnum2 = json['regnum2']
        regnum3 = json['regnum3']

        db.session.begin()

        dpk = DzialyPK.query.filter_by(id=pkid).first()
        dpk.regnum1 = regnum1
        dpk.regnum2 = regnum2 if len(regnum2) > 0 else None
        dpk.regnum3 = regnum3 if len(regnum3) > 0 else None
        db.session.commit()
        current_app.logger.info(f"PK update pass id finished")
        return "", 200
    except Exception as e:
        current_app.logger.error(f"PK update pass id: exception: {e}")
        db.session.rollback()
        return f"{e}", 500
