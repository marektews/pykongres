from .dbBase import db
from datetime import datetime


class SOA(db.Model):
    __tablename__ = "SOA"

    id = db.Column(db.Integer, primary_key=True)
    rja_id = db.Column(db.Integer, db.ForeignKey('Rozklad.id'))
    status = db.Column(db.String(45), nullable=False, default='no-bus')
    ts = db.Column(db.DateTime, nullable=False, default=datetime.now)       # w bazie jest TIMESTAMP ze względu na indeksowanie, formatowanie na napis jest identyczne

    def __init__(self, rja_id, status):
        self.rja_id = rja_id
        self.status = status
