from flask import Blueprint
# from cls import buffer

buffer_api = Blueprint('buffer', __name__, url_prefix='/buffer')


@buffer_api.route('/<tid>')
def buffer_full_info(tid):
    return {}
    # return buffer.buffer(tid)
