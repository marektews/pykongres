from flask import Blueprint
from cls import congregations

system_rej_poj_api = Blueprint('srp', __name__, url_prefix='/srp')

@system_rej_poj_api.route('/congregations/search/<pattern>')
def match_congregations(pattern):
    return congregations.match(pattern)

@system_rej_poj_api.route('/congregations/<lang>')
def congregations_list(lang):
    return congregations.list(lang)
