from flask import Blueprint
from .Terminals import _terminals_list
from .States import _states_repo

monitoring_api = Blueprint('monitoring', __name__, url_prefix='/monitoring')


@monitoring_api.route('/terminals')
def terminals_list():
    return _terminals_list()


@monitoring_api.route('/states')
def states_repo():
    return _states_repo()
