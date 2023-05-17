from flask import Flask
from api import api, login_manager
from sql import db
from mail import mail
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
)
app = Flask(__name__)
app.config["SECRET_KEY"] = "grzegorzbrzeczyszczykiewicz"
app.config["active_day"] = "d1"     # d1 | d2| d3

app.config['MAIL_SERVER'] = 'poczta.interia.pl'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'qasim@poczta.fm'
app.config['MAIL_PASSWORD'] = 'matrixewa'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail.init_app(app)

# mysql://username:password@host:port/database_name
# Production
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://api:matuzalem@127.0.0.1:33060/kw23"
# Debug
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://marek:_T1r2x3!@146.59.126.172:3306/kw23"
db.init_app(app)

app.register_blueprint(api)
login_manager.init_app(app)

if __name__ == '__main__':
    app.logger.info("Start application ...")
    logging.info("Start application ...")
    app.run(debug=True)
