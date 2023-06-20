from flask import Blueprint
from .List import _buffers_list
from .Initialize import _buffer_initialize

buffer_api = Blueprint('buffer', __name__, url_prefix='/buffer')


@buffer_api.route('/all', methods=['GET'])
def buffers_list():
    return _buffers_list()


@buffer_api.route('/<tid>')
def buffer_full_info(tid):
    return _buffer_initialize(tid)
