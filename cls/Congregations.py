from flask import current_app
from pathlib import Path
import json
import logging


class Congregations:
    _filename = "dbase/congregations.json"

    def __init__(self):
        self._congregations = []
        try:
            p = Path().absolute()
            p = p.joinpath(self._filename)
            with open(p.absolute(), "r", encoding="utf-8") as f:
                self._congregations = json.load(f)
            logging.info(f"Congregations :: loading complete : {len(self._congregations)}")
        except Exception as e:
            logging.error(f"Congregations :: __init__ exception: {e}")

    def list(self, lang):
        return self._congregations[lang]

    def match(self, pattern: str):
        lower_pattern = pattern.lower()
        res = []
        for congregation in self._congregations['pl']:
            if str(congregation).lower().find(lower_pattern) != -1:
                res.append(congregation)
        for congregation in self._congregations['ua']:
            if str(congregation).lower().find(lower_pattern) != -1:
                res.append(congregation)
        for congregation in self._congregations['ru']:
            if str(congregation).lower().find(lower_pattern) != -1:
                res.append(congregation)
        res.sort()
        return res


congregations = Congregations()
