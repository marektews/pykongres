from flask import current_app
from sql import Arrivals, Bus, Zbory, SRA


def _arrivals_list():
    """
    Zwraca listę stanów porannych przyjazdów wszystkich autokarów
    """
    try:
        res = []
        buses = Bus.query.all()
        for bus in buses:
            sra = SRA.query.filter_by(bus_id=bus.id).one()
            if not sra.canceled:
                zbor = Zbory.query.filter_by(id=sra.zbor_id).one()
                arrival = Arrivals.query.filter_by().last() ???
                res.append({
                    "busId": arrival.bus_id,
                    "datetime": arrival.datetime,
                    "arrived": arrival.arrived
                })
        return res, 200
    except Exception as e:
        current_app.logger.error(f"ARRIVALS: get list exception: {e}")
        return f"{e}", 500
