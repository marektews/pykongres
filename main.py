import logging
import locale
from flask import Flask
from api import api, login_manager
from sql import db
from mail import mail

# logging.basicConfig(
#     filename='/var/log/pykongres.log',
#     level=logging.DEBUG,
#     format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
# )
app = Flask(__name__)
app.config.from_pyfile("config.py")
app.register_blueprint(api)
mail.init_app(app)
db.init_app(app)
login_manager.init_app(app)

locale.setlocale(locale.LC_ALL, 'pl_PL')

if __name__ == '__main__':
    app.logger.info("Start application ...")
    app.run(debug=True)

# We check if we are running directly or not
if __name__ != '__main__':
    # if we are not running directly, we set the loggers
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("### Start application ... ###")
