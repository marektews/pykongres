from flask import current_app
from sql import Arrivals, Bus, Zbory, SRA, Rozklad, Sektory, Terminale


def _arrivals_list():
    """
    Zwraca listę stanów porannych przyjazdów wszystkich autokarów
    """
    try:
        res = []
        buses = Bus.query.all()
        for bus in buses:
            sra = SRA.query.filter_by(bus_id=bus.id).first()
            if not sra.canceled:
                zbor = Zbory.query \
                    .filter_by(id=sra.zbor_id) \
                    .first()

                r = Rozklad.query.filter_by(sra_id=sra.id).first()
                if r is not None:
                    sektor = Sektory.query.filter_by(id=r.sektor_id).first()
                    terminal = Terminale.query.filter_by(id=sektor.tid).first()
                    name = f"{terminal.name[0]}{r.sektor_id}{r.tura} - {zbor.name}"
                else:
                    name = zbor.name

                arrival = Arrivals.query \
                    .filter_by(bus_id=bus.id) \
                    .order_by(Arrivals.datetime.desc()) \
                    .first()

                res.append({
                    "bus_id": bus.id,
                    "name": name,
                    "datetime": arrival.datetime if arrival else None,
                    "arrived": arrival.arrived if arrival else False
                })
        return res, 200
    except Exception as e:
        current_app.logger.error(f"ARRIVALS: get list exception: {e}")
        return f"{e}", 500
