from .dbBase import db
from datetime import datetime


class Czw(db.Model):
    __tablename__ = "Czw"

    id = db.Column(db.Integer, primary_key=True)
    driver = db.Column(db.String, nullable=False)
    nr_rej = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    nr_ident = db.Column(db.Integer, nullable=False)
    zbor_id = db.Column(db.Integer, nullable=False)
    issuing = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    cancellation = db.Column(db.DateTime, nullable=True)
