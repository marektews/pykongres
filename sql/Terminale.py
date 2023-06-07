from .dbBase import db


class Terminale(db.Model):
    __tablename__ = "Terminale"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    isBuffer = db.Column(db.Integer, nullable=False)

    def __init__(self, name, is_buffer):
        self.name = name
        self.isBuffer = is_buffer
