from flask import current_app
from sql import SRA, Zbory, Pilot, Bus


def _ia_list(congregation_name):
    try:
        res = []
        zbor = Zbory.query.filter_by(name=congregation_name).one()
        all_sra = SRA.query.filter_by(zbor_id=zbor.id).all()
        for sra in all_sra:
            tmp = dict()
            tmp['id'] = sra.id
            tmp['lp'] = sra.lp

            bus = Bus.query.filter_by(id=sra.bus_id).one()
            tmp['bus'] = {"type": bus.type}

            pilot = Pilot.query.filter_by(id=sra.pilot1_id).one()
            tmp['pilot1'] = {"fn": pilot.fn, "ln": pilot.ln}

            if sra.pilot2_id is not None:
                pilot = Pilot.query.filter_by(id=sra.pilot2_id).one()
                tmp['pilot2'] = {"fn": pilot.fn, "ln": pilot.ln}

            if sra.pilot3_id is not None:
                pilot = Pilot.query.filter_by(id=sra.pilot3_id).one()
                tmp['pilot2'] = {"fn": pilot.fn, "ln": pilot.ln}

            res.append(tmp)
        return res, 200
    except Exception as e:
        current_app.logger.error(f"IA get list exception: {e}")
        return f"{e}", 500
