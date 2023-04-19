from flask import Blueprint, current_app
from cls import autokary, terminale, states

sector_api = Blueprint('sector', __name__, url_prefix='/sector')


@sector_api.route("/<sid>")
def sector_initialize(sid):
    return terminale.sector(sid)


@sector_api.route("/<sid>/state")
def sector_state(sid):
    buses = autokary.all_from_sector(sid)
    res = []
    for bus in buses:
        bus_state = states.find_by_bid(bus["bid"])
        o = dict()
        o["bid"] = bus["bid"]
        o["congregation"] = bus["congregation"]
        o["schedule"] = bus[current_app.config["active_day"]]
        o["real"] = bus_state
        res.append(o)
    return res


@sector_api.route("/<sid>/schedule")
def sector_schedule(sid):
    return autokary.all_from_sector(sid)
