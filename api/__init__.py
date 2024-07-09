from flask import Blueprint
from .test import test_api
from .login import login_api, login_manager
from .sector import sector_api
from .buffer import buffer_api
from .terminal import terminal_api
from .monitoring import monitoring_api
from .sra import sra_api
from .srp import srp_api
from .rja import rja_api
from .pk import pk_api
from .ia import ia_api
from .czw import czw_api
from .arrivals import arrivals_api

api = Blueprint('api', __name__, url_prefix='/api')

api.register_blueprint(test_api)
api.register_blueprint(login_api)
api.register_blueprint(sector_api)
api.register_blueprint(buffer_api)
api.register_blueprint(terminal_api)
api.register_blueprint(monitoring_api)
api.register_blueprint(sra_api)
api.register_blueprint(srp_api)
api.register_blueprint(rja_api)
api.register_blueprint(pk_api)
api.register_blueprint(ia_api)
api.register_blueprint(czw_api)
api.register_blueprint(arrivals_api)
