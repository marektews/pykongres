from .dbBase import db


class Bus(db.Model):
    __tablename__ = "Bus"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    distance = db.Column(db.String, nullable=False)
    parking_mode = db.Column(db.String, nullable=False)

    def __init__(self, typ, distance, parking_mode):
        self.type = typ
        self.distance = distance
        self.parking_mode = parking_mode
