from .dbBase import db
from datetime import datetime


class SRA(db.Model):
    __tablename__ = "SRA"

    id = db.Column(db.Integer, primary_key=True)
    zbor_id = db.Column(db.Integer, db.ForeignKey('Zbory.id'))
    bus_id = db.Column(db.Integer, db.ForeignKey('Bus.id'))
    lp = db.Column(db.Integer, nullable=True)                   # liczba porządkowa w ramach zboru
    pilot1_id = db.Column(db.Integer, db.ForeignKey('Pilot.id'))
    pilot2_id = db.Column(db.Integer, db.ForeignKey('Pilot.id'), nullable=True)
    pilot3_id = db.Column(db.Integer, db.ForeignKey('Pilot.id'), nullable=True)
    info = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now)
