from pathlib import Path
import json
import logging


class Terminale:
    _filename = "dbase/terminale.json"

    def __init__(self):
        self._terminals = []
        try:
            p = Path().absolute()
            p = p.joinpath(self._filename)
            with open(p.absolute(), "r", encoding="utf-8") as f:
                self._terminals = json.load(f)
        except Exception as e:
            logging.error(f"Terminale :: __init__ enception: {e}")

    def root_list(self):
        """
        Budowanie listy terminali; tylko pierwszy poziom
        :return: Lista terminali
        """
        res = []
        for item in self._terminals:
            tmp = dict()
            tmp["tid"] = item["tid"]
            tmp["name"] = item["name"]
            tmp["buffer"] = False if "sectors" in item else True
            res.append(tmp)
        return res

    def terminal(self, tid):
        """
        Terminal full info
        :param tid: Identyfikator
        :return: dict
        """
        for item in self._terminals:
            if item["tid"] == str(tid):
                return item
        return {}

    def sector(self, sid):
        """
        Sector full info
        :param sid: Identyfikator
        :return: dict
        """
        for terminal in self._terminals:
            if 'sectors' not in terminal:
                continue
            for item in terminal['sectors']:
                if item["sid"] == str(sid):
                    return item
        return {}

terminale = Terminale()
