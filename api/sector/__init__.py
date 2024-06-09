from flask import Blueprint
from .Initialize import _sector_initialize
from .Schedule import _sector_schedule
from .States import _sector_states
from .Notifications import _sector_notification

sector_api = Blueprint('sector', __name__, url_prefix='/sector')


@sector_api.route("/<sid>")
def sector_initialize(sid):
    return _sector_initialize(sid)


@sector_api.route("/<sid>/states")
def sector_states(sid):
    return _sector_states(sid)


@sector_api.route("/<sid>/schedule")
def sector_schedule(sid):
    return _sector_schedule(sid)


@sector_api.route('/notify/sendtosector/<rja_id>', methods=['GET'])
def sector_notification_sendtosector(rja_id):
    return _sector_notification(rja_id, 'send-to-sector')


@sector_api.route('/notify/readytoleave/<rja_id>', methods=['GET'])
def sector_notification_readytoleave(rja_id):
    return _sector_notification(rja_id, 'ready-to-leave')


@sector_api.route('/notify/onsector/<rja_id>', methods=['GET'])
def sector_notification_onsector(rja_id):
    return _sector_notification(rja_id, 'on-sector')


@sector_api.route('/notify/ontheroad/<rja_id>', methods=['GET'])
def sector_notification_ontheroad(rja_id):
    return _sector_notification(rja_id, 'on-the-road')
