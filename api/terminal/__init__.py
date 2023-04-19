from flask import Blueprint
from cls import terminale

terminal_api = Blueprint('terminal', __name__, url_prefix='/terminal')


@terminal_api.route('/all')
def terminals_list():
    return terminale.root_list()


@terminal_api.route('/<tid>')
def terminal_full_info(tid):
    return terminale.terminal(tid)
