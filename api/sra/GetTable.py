from flask import current_app
from sql import SRA, Zbory, Pilot, Bus


def _get_table():
    try:
        res = []
        all_sra = SRA.query.order_by(SRA.timestamp.desc()).all()
        for sra in all_sra:
            item = dict()
            item["id"] = sra.id
            item["info"] = sra.info
            item["timestamp"] = sra.timestamp.strftime("%a, %x %X")

            zbor = Zbory.query.filter_by(id=sra.zbor_id).one()
            z = dict()
            z["name"] = zbor.name
            z["number"] = zbor.number
            z["lang"] = zbor.lang
            item["zbor"] = z

            bus = Bus.query.filter_by(id=sra.bus_id).one()
            b = dict()
            b["type"] = bus.type
            b["distance"] = bus.distance
            b["parking_mode"] = bus.parking_mode
            item["bus"] = b

            ids = [sra.pilot1_id, sra.pilot2_id, sra.pilot3_id]
            for i in range(3):
                _id = ids[i]
                if _id is not None:
                    pilot = Pilot.query.filter_by(id=_id).one()
                    p = dict()
                    p["fn"] = pilot.fn
                    p["ln"] = pilot.ln
                    p["email"] = pilot.email
                    p["phone"] = pilot.phone
                    item[f"pilot{i+1}"] = p

            res.append(item)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"SRA get table exception: {e}")
        return f"{e}", 500
