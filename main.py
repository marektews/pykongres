from flask import Flask
# from flask_restful import Api
from Buffer import Buffer
from Terminale import Terminale
from Autokary import Autokary
from States import States

app = Flask(__name__)
app.config["active_day"] = "d1"     # d1 | d2| d3
states = States()


@app.route('/api/terminals')
def terminals_list():
    t = Terminale()
    return t.root_list()


@app.route('/api/buffer/<tid>')
def buffer_full_info(tid):
    b = Buffer()
    return b.buffer(tid)


@app.route('/api/terminal/<tid>')
def terminal_full_info(tid):
    t = Terminale()
    return t.terminal(tid)


@app.route("/api/sector/<sid>")
def sector_initialize(sid):
    t = Terminale()
    return t.sector(sid)


@app.route("/api/sector/<sid>/state")
def sector_state(sid):
    a = Autokary()
    buses = a.all_from_sector(sid)
    res = []
    for bus in buses:
        bus_state = states.find_by_bid(bus["bid"])
        o = dict()
        o["bid"] = bus["bid"]
        o["congregation"] = bus["congregation"]
        o["schedule"] = bus[app.config["active_day"]]
        o["real"] = bus_state
        res.append(o)
    return res


@app.route("/api/sector/<sid>/schedule")
def sector_schedule(sid):
    a = Autokary()
    return a.all_from_sector(sid)


if __name__ == '__main__':
    app.run(debug=True)
