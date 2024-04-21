from flask import Blueprint
from datetime import datetime

test_api = Blueprint('test', __name__, url_prefix='/test')


@test_api.route('/', methods=['GET'])
def test():
    return {"datetime": datetime.now()}
