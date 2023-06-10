from flask import current_app
from pathlib import Path
import json
import logging


class Autokary:
    _filename = "dbase/autokary.json"

    def __init__(self):
        self._buses = []
        try:
            p = Path().absolute()
            p = p.joinpath(self._filename)
            with open(p.absolute(), "r", encoding="utf-8") as f:
                self._buses = json.load(f)
            logging.info(f"Autokary :: loading complete : {len(self._buses)}")
        except Exception as e:
            logging.error(f"Autokary :: __init__ exception: {e}")

    def all_list(self):
        res = []
        active_day = current_app.config["ACTIVE_DAY"]
        for item in self._buses:
            o = dict()
            o['bid'] = item['bid']
            o['congregation'] = item['congregation']
            o['buffer'] = item['buffer']
            o['sector'] = item['sector']
            o['substitution'] = item[active_day]['substitution']
            o['departure'] = item[active_day]['departure']
            res.append(o)
        return res

    def find_by_bid(self, bid):
        for item in self._buses:
            if item["bid"] == str(bid):
                return item
        return None

    def all_from_sector(self, sid):
        res = [item for item in self._buses if item["sector"] == str(sid)]
        return res


autokary = Autokary()
