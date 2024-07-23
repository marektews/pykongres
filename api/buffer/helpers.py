from flask import current_app
from api.getActiveDay import getActiveDay


def arrive_today(rja):
    # active_day = current_app.config['ACTIVE_DAY']
    active_day = getActiveDay()
    if active_day == 'd1' and rja.a1 is None:
        return False
    if active_day == 'd2' and rja.a2 is None:
        return False
    if active_day == 'd3' and rja.a3 is None:
        return False
    return True
