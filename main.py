from flask import Flask
from api import api
import logging

logging.basicConfig(
    filename='c:/app.log',
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
)
app = Flask(__name__)
app.config["active_day"] = "d1"     # d1 | d2| d3
app.register_blueprint(api)

if __name__ == '__main__':
    app.logger.info("Start application ...")
    logging.info("Start application ...")
    app.run(debug=True)
