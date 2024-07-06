from flask import Blueprint

arrivals_api = Blueprint('arrivals', __name__, url_prefix='/arrivals')


@arrivals_api.route('/all', methods=['GET'])
def arrivals_list():
    return _arrivals_list()
