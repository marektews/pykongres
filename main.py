import logging
import locale
import threading
from flask import Flask
from api import api, login_manager
from sql import db
# from mail import mail
from qr import qrc
# from mqtt import init_mqtt

app = Flask(__name__)
app.config.from_pyfile("config.py")
app.register_blueprint(api)
# mail.init_app(app)
db.init_app(app)
login_manager.init_app(app)
qrc.init_app(app)

# polskie locale
locale.setlocale(locale.LC_ALL, 'pl_PL')

if __name__ == '__main__':
    """ Start w debuggerze """
    app.logger.info("Start application ...")
    # th = threading.current_thread()
    # print(f"{th.name} - {th.ident} - {th.native_id}")
    # init_mqtt(app, False)
    app.run(debug=True, port=8000)

if __name__ != '__main__':
    """ Start w środowisku produkcyjnym """
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info("### Start application ... ###")
    # init_mqtt(app, True)
