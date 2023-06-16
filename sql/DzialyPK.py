from .dbBase import db
from datetime import datetime


class DzialyPK(db.Model):
    __tablename__ = "DzialyPK"

    id = db.Column(db.Integer, primary_key=True)
    dzial_id = db.Column(db.Integer, db.ForeignKey('Dzialy.id'))
    pass_nr = db.Column(db.Integer, nullable=False)
    regnum1 = db.Column(db.String, nullable=False)
    regnum2 = db.Column(db.String, nullable=True)
    regnum3 = db.Column(db.String, nullable=True)
    registered = db.Column(db.DateTime, nullable=False, default=datetime.now)
    d1 = db.Column(db.DateTime, nullable=True)
    d2 = db.Column(db.DateTime, nullable=True)
    d3 = db.Column(db.DateTime, nullable=True)
