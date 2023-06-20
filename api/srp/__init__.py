from flask import Blueprint, request, current_app
from flask_login import login_required
from sql import SRP, Zbory
from .Create import _create_pass_id
from .Update import _update_pass_id
from .Download import _download_pass_id
from .Find import _find_pass_id
from .LoadAll import _load_all
from .GetZbory import _zbory_all
from .Delete import _srp_delete
from .Check import _srp_check

srp_api = Blueprint('srp', __name__, url_prefix='/srp')


@login_required
@srp_api.route('/isfreepass/<congregation>')
def is_free_pass_id(congregation):
    """
    Sprawdzanie czy jest jeszcze wolny identyfikator do wykorzystania
    :return: HTTP codes: 200 | 404
    """
    try:
        _zbor = Zbory.query.filter_by(name=congregation).first()
        c = SRP.query.filter_by(zbor_id=_zbor.id).count()
        if c < _zbor.plimit:
            return "", 200
        else:
            return "", 404
    except Exception as e:
        current_app.logger.error(f"SRA check free pass id: exception: {e}")
        return f"{e}", 500


@login_required
@srp_api.route('/create', methods=['POST'])
def create_pass_id():
    """
    Generowanie przepustki parkingowej

    Struktura danych:
        "congregation": "<nazwa zboru>",
        "regnum1": "<numer rejestracyjny na piątek lub na wszystkie dni>",
        "regnum2": "" | None,
        "regnum3": "" | None,

    :return 200, 400, 500
    """
    return _create_pass_id(request.json)


@login_required
@srp_api.route('/read/<pass_id>')
def read_pass_id(pass_id):
    """
    Odczyt stanu identyfikatora
    :param pass_id: private key w bazie
    :return: {
        "passid": "<private key rekordu>",
        "pass_nr": <numer identyfikatora>,
        "regnum1": "<numer rejestracyjny na piątek lub na wszystkie dni>",
        "regnum2": "<numer rejestracyjny na sobotę>",
        "regnum3": "<numer rejestracyjny na niedzielę>",
    }
    """
    try:
        srp = SRP.query.filter_by(id=pass_id).first()
        res = dict()
        res["passid"] = srp.id
        res["pass_nr"] = srp.pass_nr
        res["regnum1"] = srp.regnum1
        res["regnum2"] = srp.regnum2 if srp.regnum2 is not None else ''
        res["regnum3"] = srp.regnum3 if srp.regnum3 is not None else ''
        return res, 200
    except Exception as e:
        current_app.logger.error(f"SRA update pass id: exception: {e}")
        return f"{e}", 500


@login_required
@srp_api.route('/update', methods=['POST'])
def update_pass_id():
    """
    Aktualizacja przepustki parkingowej

    Struktura danych:
        "passid": "<private key rekordu>",
        "regnum1": "<numer rejestracyjny na piątek lub na wszystkie dni>",
        "regnum2": "<numer rejestracyjny na sobotę>" | None,
        "regnum3": "<numer rejestracyjny na niedzielę>" | None,
    """
    return _update_pass_id(request.json)


@login_required
@srp_api.route('/download/<pass_id>')
def download_pass_id(pass_id):
    return _download_pass_id(pass_id)


@login_required
@srp_api.route('/find', methods=['POST'])
def find_pass_id():
    return _find_pass_id(request.json)


@login_required
@srp_api.route('/all', methods=['GET'])
def load_all():
    return _load_all()


@login_required
@srp_api.route('/zbory', methods=['GET'])
def zbory_all():
    return _zbory_all()


@login_required
@srp_api.route('/delete/<srp_id>', methods=['GET'])
def srp_delete(srp_id):
    return _srp_delete(srp_id)


@srp_api.route('/check', methods=['GET'])
def srp_check():
    return _srp_check(request.args)
