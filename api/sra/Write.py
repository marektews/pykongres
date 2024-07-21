from flask import current_app
from sql import db, Pilot, Bus, SRA
from .helpers import _build_pilot_phone


def _write_sra(data):
    try:
        db.session.begin()
        sra = SRA.query.filter_by(id=data['id']).one()
        sra.lp = data['bus']['lp']
        sra.prefix = data['bus']['prefix'].upper()
        if len(data['info']) > 0:
            sra.info = data['info']
        else:
            sra.info = None

        # aktualizacja danych autokaru
        bus = Bus.query.filter_by(id=sra.bus_id).one()
        bus.type = data['bus']['type']
        bus.distance = data['bus']['distance']
        bus.parking_mode = data['bus']['parking_mode']
        db.session.flush()

        # pilot 1
        dp1 = data['pilot1']
        pilot = Pilot.query.filter_by(id=sra.pilot1_id).one()
        pilot.fn = dp1['fn']
        pilot.ln = dp1['ln']
        pilot.email = dp1['email']
        pilot.phone = _build_pilot_phone(dp1['prefix'], dp1['number'])
        db.session.flush()

        # pilot 2 - update, insert, remove
        if 'pilot2' in data:
            sra.pilot2_id = _update_pilot(db, sra.pilot2_id, data['pilot2'])
        else:
            sra.pilot2_id = _remove_pilot(db, sra.pilot2_id)

        # pilot 3 - update, insert, remove
        if 'pilot3' in data:
            sra.pilot3_id = _update_pilot(db, sra.pilot3_id, data['pilot3'])
        else:
            sra.pilot3_id = _remove_pilot(db, sra.pilot3_id)

        db.session.commit()
        return '', 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"SRA write exception: {e}")
        return f"{e}", 500


def _update_pilot(_db, pilot_id, pilot_data):
    if pilot_id is not None:
        # update
        pilot = Pilot.query.filter_by(id=pilot_id).one()
        pilot.fn = pilot_data['fn']
        pilot.ln = pilot_data['ln']
        pilot.email = pilot_data['email']
        pilot.phone = _build_pilot_phone(pilot_data['prefix'], pilot_data['number'])
        _db.session.flush()
        return pilot.id
    else:
        # insert
        pilot = Pilot(firstname=pilot_data['fn'], lastname=pilot_data['ln'],
                      email=pilot_data['email'], phone=_build_pilot_phone(pilot_data['prefix'], pilot_data['number']))
        _db.session.add(pilot)
        _db.session.flush()
        return pilot.id


def _remove_pilot(_db, pilot_id) -> [None, int]:
    if pilot_id is not None:
        pilot = Pilot.query.filter_by(id=pilot_id).one()
        _db.session.delete(pilot)
        return None
    else:
        return pilot_id
