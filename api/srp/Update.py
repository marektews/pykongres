from flask import current_app
from sql import db, SRP


def _update_pass_id(json):
    try:
        pass_id = json['passid']
        regnum1 = json['regnum1']
        regnum2 = json['regnum2']
        regnum3 = json['regnum3']

        db.session.begin()

        srp = SRP.query.filter_by(id=pass_id).first()
        srp.regnum1 = regnum1
        srp.regnum2 = regnum2 if len(regnum2) > 0 else None
        srp.regnum3 = regnum3 if len(regnum3) > 0 else None
        db.session.commit()
        current_app.logger.info(f"SRA update pass id finished")
        return "", 200
    except Exception as e:
        current_app.logger.error(f"SRA update pass id: exception: {e}")
        db.session.rollback()
        return f"{e}", 500
