from flask import Blueprint
from .List import _terminals_list
from .FullInfo import _terminal_full_info

terminal_api = Blueprint('terminal', __name__, url_prefix='/terminal')


@terminal_api.route('/all', methods=['GET'])
def terminals_list():
    return _terminals_list()


@terminal_api.route('/<tid>', methods=['GET'])
def terminal_full_info(tid):
    return _terminal_full_info(tid)
