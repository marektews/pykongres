from pathlib import Path
import json
import logging


class Buffer:
    _filename = "dbase/autokary.json"

    def __init__(self):
        self._buses = []
        try:
            p = Path().absolute()
            p = p.joinpath(self._filename)
            with open(p.absolute(), "r", encoding="utf-8") as f:
                self._buses = json.load(f)
        except Exception as e:
            logging.error(f"Buffer :: __init__ enception: {e}")

    def buffer(self, tid):
        """
        Buffer full info
        :param tid: Identyfikator
        :return: array
        """
        res = []
        for item in self._buses:
            if item["buffer"] == str(tid):
                o = dict()
                o["bid"] = item["bid"]
                o["congregation"] = item["congregation"]
                o["substitution"] = item[current_app.config["ACTIVE_DAY"]]["substitution"]
                res.append(o)
        return res

buffer = Buffer()
