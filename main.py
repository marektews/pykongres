import logging
import locale
from flask import Flask
from api import api, login_manager
from sql import db
from mail import mail

app = Flask(__name__)
app.config.from_pyfile("config.py")
app.register_blueprint(api)
mail.init_app(app)
db.init_app(app)
login_manager.init_app(app)

# polskie locale
locale.setlocale(locale.LC_ALL, 'pl_PL')

if __name__ == '__main__':
    """ Start w debuggerze """
    app.logger.info("Start application ...")
    app.run(debug=True)

if __name__ != '__main__':
    """ Start w środowisku produkcyjnym """
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("### Start application ... ###")
