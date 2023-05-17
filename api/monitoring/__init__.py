from flask import Blueprint
from cls import autokary

monitoring_api = Blueprint('monitoring', __name__, url_prefix='/monitoring')


@monitoring_api.route('/buses')
def buses_list():
    return autokary.all_list()
