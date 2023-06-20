from flask import Blueprint, request
from .List import _buffers_list
from .Initialize import _buffer_initialize
from .States import _buffer_states
from .Notifications import _buffer_notification

buffer_api = Blueprint('buffer', __name__, url_prefix='/buffer')


@buffer_api.route('/all', methods=['GET'])
def buffers_list():
    return _buffers_list()


@buffer_api.route('/<bid>')
def buffer_full_info(bid):
    return _buffer_initialize(bid)


@buffer_api.route('/<bid>/states')
def buffer_states(bid):
    return _buffer_states(bid)


@buffer_api.route('/notify/nobus/<rja_id>', methods=['GET'])
def buffer_notification_nobus(rja_id):
    return _buffer_notification(rja_id, 'no-bus')


@buffer_api.route('/notify/inbuffer/<rja_id>', methods=['GET'])
def buffer_notification_inbuffer(rja_id):
    return _buffer_notification(rja_id, 'in-buffer')


@buffer_api.route('/notify/secondcircle/<rja_id>', methods=['GET'])
def buffer_notification_secondcircle(rja_id):
    return _buffer_notification(rja_id, 'second-circle')


@buffer_api.route('/notify/sendtosector/<rja_id>', methods=['GET'])
def buffer_notification_sendtosector(rja_id):
    return _buffer_notification(rja_id, 'send-to-sector')
