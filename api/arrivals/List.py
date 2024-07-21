from flask import current_app
from sql import Arrivals, Bus, Zbory, SRA, Rozklad, Sektory, Terminale
from api.createShortBusID import createShortBusID
from api.whichTura import whichTura


def _arrivals_list():
    """
    Zwraca listę stanów porannych przyjazdów wszystkich autokarów
    """
    try:
        res = []
        tura = whichTura()
        buses = Bus.query.all()
        for bus in buses:
            sra = SRA.query.filter_by(bus_id=bus.id).first()

            if sra is None:
                continue

            if not sra.canceled:
                zbor = Zbory.query \
                    .filter_by(id=sra.zbor_id) \
                    .first()

                if zbor is None or zbor.tura != tura:
                    continue

                if sra.lp is not None:
                    zborName = f"{zbor.name} {sra.lp}"
                else:
                    zborName = zbor.name

                r = Rozklad.query.filter_by(sra_id=sra.id).first()
                if r is not None:
                    sektor = Sektory.query.filter_by(id=r.sektor_id).first()
                    terminal = Terminale.query.filter_by(id=sektor.tid).first()
                    sl = sektor.name.split()
                    shortBusID = createShortBusID(letter=terminal.name[0], sektor=sl[1], tura=r.tura, static_identifier=sra.static_identifier)
                    name = f"{shortBusID} - {zborName}"
                else:
                    name = zborName

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
