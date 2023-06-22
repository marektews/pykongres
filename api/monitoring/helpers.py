from flask import current_app


def _arrive_by_day(rja):
    active_day = current_app.config['ACTIVE_DAY']
    if active_day == 'd1':
        return rja.a1.strftime("%H:%M") if rja.a1 is not None else ''
    if active_day == 'd2':
        return rja.a2.strftime("%H:%M") if rja.a2 is not None else ''
    if active_day == 'd3':
        return rja.a3.strftime("%H:%M") if rja.a3 is not None else ''
    return rja.a1 if rja.a1 is not None else ''


def _departure_by_day(rja):
    active_day = current_app.config['ACTIVE_DAY']
    if active_day == 'd1':
        return rja.d1.strftime("%H:%M") if rja.d1 is not None else ''
    if active_day == 'd2':
        return rja.d2.strftime("%H:%M") if rja.d2 is not None else ''
    if active_day == 'd3':
        return rja.d3.strftime("%H:%M") if rja.d3 is not None else ''
    return rja.d1 if rja.d1 is not None else ''