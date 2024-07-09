from flask import current_app
from sql import db, Arrivals
from datetime import datetime


def _toggle(json):
    try:
        bus_id = json["bus_id"]
        db.session.begin()

        arrival = Arrivals.query.filter_by(bus_id=bus_id).first()
        if arrival is not None:
            arrival.datetime = datetime.utcnow()
            arrival.arrived = not arrival.arrived
        else:
            arrival = Arrivals(bus_id=bus_id, arrived=1)
            db.session.add(arrival)

        db.session.commit()
        return {}, 200

    except Exception as e:
        current_app.logger.error(f"ARRIVALS: toggle exception: {e}")
        db.session.rollback()
        return f"{e}", 500
