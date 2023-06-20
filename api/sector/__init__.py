from flask import Blueprint
from .Initialize import _sector_initialize
from .Schedule import _sector_schedule

sector_api = Blueprint('sector', __name__, url_prefix='/sector')


@sector_api.route("/<bid>")
def sector_initialize(bid):
    return _sector_initialize(bid)


@sector_api.route("/<sid>/state")
def sector_state(sid):
    # buses = autokary.all_from_sector(sid)
    # res = []
    # for bus in buses:
    #     bus_state = states.find_by_bid(bus["bid"])
    #     o = dict()
    #     o["bid"] = bus["bid"]
    #     o["congregation"] = bus["congregation"]
    #     o["schedule"] = bus[current_app.config["ACTIVE_DAY"]]
    #     o["real"] = bus_state
    #     res.append(o)
    # return res
    res = []
    return res


@sector_api.route("/<sid>/schedule")
def sector_schedule(sid):
    return _sector_schedule(sid)
