from .dbBase import db
from datetime import datetime


class SRP(db.Model):
    __tablename__ = "SRP"

    id = db.Column(db.Integer, primary_key=True)
    zbor_id = db.Column(db.Integer, db.ForeignKey('Zbory.id'))
    pass_nr = db.Column(db.Integer, nullable=False)
    regnum1 = db.Column(db.String, nullable=False)
    regnum2 = db.Column(db.String, nullable=True)
    regnum3 = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
