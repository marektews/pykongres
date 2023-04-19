from flask import current_app
from pathlib import Path
import json


class Autokary:
    _filename = "./dbase/autokary.json"

    def __init__(self):
        self._buses = []
        try:
            p = Path().absolute()
            p = p.joinpath(self._filename)
            with open(p.absolute(), "r", encoding="utf-8") as f:
                self._buses = json.load(f)
        except Exception as e:
            current_app.logger.error(f"Autokary :: __init__ exception: {e}")

    def find_by_bid(self, bid):
        for item in self._buses:
            if item["bid"] == str(bid):
                return item
        return None

    def all_from_sector(self, sid):
        res = [item for item in self._buses if item["sector"] == str(sid)]
        return res
