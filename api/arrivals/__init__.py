from flask import Blueprint, request
from .List import _arrivals_list
from .Toggle import _toggle

arrivals_api = Blueprint('arrivals', __name__, url_prefix='/arrivals')


@arrivals_api.route('/all', methods=['GET'])
def arrivals_list():
    return _arrivals_list()


@arrivals_api.route('/toggle', methods=['POST'])
def toggle():
    return _toggle(request.json)
