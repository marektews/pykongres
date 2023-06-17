from flask import Blueprint
from flask_login import login_required
from .List import _ia_list
from .Download import _ia_download

ia_api = Blueprint('ia', __name__, url_prefix='/ia')


@login_required
@ia_api.route('/list/<congregation_name>')
def ia_list(congregation_name):
    return _ia_list(congregation_name)


@login_required
@ia_api.route('/download/<sra_id>')
def ia_download(sra_id):
    return _ia_download(sra_id)
