from flask import Blueprint
from flask import request
from flask_login import login_required
from .GetTerminals import _get_terminals
from .GetSectors import _get_sectors
from .GetSectorRJ import _get_buses_of_sector
from .Zbory import _zbory_get_list
from .GetBuses import _buses_get_list
from .GetSRA import _sra_get_list
from .SaveSectorRJ import _save_buses_of_sector
from .GetUsedBuses import _buses_get_used
from .GetZborRJA import _zbor_get_rja

rja_api = Blueprint('rja', __name__, url_prefix='/rja')


@login_required
@rja_api.route('/zbory', methods=['POST'])
def zbory():
    return _zbory_get_list(request.json)


@login_required
@rja_api.route('/zbor/<zbor_id>', methods=['GET'])
def zbor_rja(zbor_id):
    return _zbor_get_rja(zbor_id)


@login_required
@rja_api.route('/buses', methods=['GET'])
def buses():
    return _buses_get_list()


@login_required
@rja_api.route('/sra', methods=['POST'])
def sra():
    return _sra_get_list(request.json)


@login_required
@rja_api.route('/terminals', methods=['GET'])
def terminals():
    return _get_terminals()


@login_required
@rja_api.route('/sectors/<tid>', methods=['GET'])
def sectors(tid):
    return _get_sectors(tid)


@login_required
@rja_api.route('/buses/<sid>', methods=['POST'])
def get_buses_of_sector(sid):
    return _get_buses_of_sector(sid, request.json)


@login_required
@rja_api.route('/buses/save', methods=['POST'])
def save_buses_of_sector():
    return _save_buses_of_sector(request.json)


@login_required
@rja_api.route('/buses/used', methods=['POST'])
def buses_get_used():
    return _buses_get_used(request.json)
