from .dbBase import db
from datetime import datetime


class Arrivals(db.Model):
    __tablename__ = "Arrivals"

    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    arrived = db.Column(db.Boolean, nullable=False)

    def __init__(self, bus_id, arrived):
        self.bus_id = bus_id
        self.datetime = datetime.utcnow()
        self.arrived = arrived
