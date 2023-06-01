from flask import Blueprint, request, current_app
from flask_login import login_required
from sql import Zbory, Pilot
from .GetTable import _get_table
from .Write import _write_sra
from .Export import _export_to_xlsx
from .Submit import _submit_sra
from .Delete import _delete_sra

sra_api = Blueprint('sra', __name__, url_prefix='/sra')


@sra_api.route('/search/congregations/<pattern>')
def search_congregations(pattern):
    """
    Wyszukiwanie zborów na podstawie krótkiego ciągu
    :param pattern: Wzorzec wyszukiwania
    :return: [zbor.name, ...]
    """
    zbory = Zbory.query.order_by(Zbory.name).filter(Zbory.name.contains(pattern)).all()
    return [zbor.name for zbor in zbory]


@login_required
@sra_api.route('/check_pilot_duplicate', methods=['POST'])
def is_pilot_duplicate():
    """
    Sprawdzanie czy podane dane pilota nie są już przypisane do innego autokaru
    :return: HTTP codes: 200, 400
    """
    try:
        data = request.json
        _phone = f"{data['phone']['direct']} {data['phone']['number']}"
        p = Pilot.query.filter_by(phone=_phone).first()
        if p is None:
            return "", 200
        else:
            return "", 400
    except Exception as e:
        current_app.logger.error(f"SRA submit exception: {e}")
        return f"{e}", 500


@login_required
@sra_api.route('/submit', methods=['POST'])
def submit_sra_registration():
    """
    Zapis zgłoszenia do bazy danych
    """
    return _submit_sra(request.json)


@login_required
@sra_api.route('/table')
def get_table():
    """
    Budowanie tabeli w trybie administracyjnym
    """
    return _get_table()


@login_required
@sra_api.route('/write', methods=['POST'])
def write_sra_registration():
    """
    Aktualizacja istniejącego zgłoszenia
    """
    return _write_sra(request.json)


@login_required
@sra_api.route('/export/xlsx')
def build_xlsx():
    """
    Export do formatu Excela - *.xlsx
    """
    return _export_to_xlsx()


@login_required
@sra_api.route('/delete/<sra_id>', methods=['GET'])
def delete_sra(sra_id):
    return _delete_sra(sra_id)
