from pathlib import Path
import json
import logging


class States:
    """
    Przechowuje aktualne stany oraz rzeczywiste czasy podstawienia i odjazdu.
    Rzeczywiste dane mogą się różnić od zaplanowanych w rozkładzie jazdy.

    Struktura danych i pliku 'states.json'
    {
        "<bid>": {
            "substitution": "12:34",
            "departure": "12:36"
        },
        ...
    }
    """
    _filename = "states/states.json"

    def __init__(self):
        self._states = {}
        try:
            p = Path().absolute()
            p = p.joinpath(self._filename)
            with open(p.absolute(), "r", encoding="utf-8") as f:
                self._states = json.load(f)
        except Exception as e:
            logging.error(f"States :: __init__ exception: {e}")

    def save(self):
        try:
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump(self._states, f)
        except Exception as e:
            logging.error(f"States :: save to file exception: {e}")

    def find_by_bid(self, bid):
        if bid not in self._states:
            return {
                "substitution": "",
                "departure": ""
            }
        else:
            return self._states[bid]

    def set_state(self, bid, state):
        self._states[bid] = state
        self.save()

states = States()
