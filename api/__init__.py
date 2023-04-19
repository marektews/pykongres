from flask import Blueprint
from .sector import sector_api
from .buffer import buffer_api
from .terminal import terminal_api

api = Blueprint('api', __name__, url_prefix='/api')
api.register_blueprint(sector_api)
api.register_blueprint(buffer_api)
api.register_blueprint(terminal_api)
