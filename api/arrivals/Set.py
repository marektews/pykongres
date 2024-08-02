from flask import current_app
from sql import db, Arrivals
from datetime import datetime


def _set(json):
    try:
        bus_id = json["bus_id"]
        state = json["state"]
        db.session.begin()

        arrival = Arrivals.query.filter_by(bus_id=bus_id).first()
        if arrival is not None:
            arrival.datetime = datetime.utcnow()
            arrival.arrived = state
        else:
            arrival = Arrivals(bus_id=bus_id, arrived=state)
            db.session.add(arrival)

        db.session.commit()
        return {}, 200

    except Exception as e:
        current_app.logger.error(f"ARRIVALS: set exception: {e}")
        db.session.rollback()
        return f"{e}", 500
