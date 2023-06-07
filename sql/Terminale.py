from .dbBase import db


class Terminale(db.Model):
    __tablename__ = "Terminale"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    is_buffer = db.Column(db.Integer, nullable=False)
    assigned_buffer = db.Column(db.Integer, nullable=True)

    def __init__(self, name, is_buffer, assigned_buffer=None):
        self.name = name
        self.is_buffer = is_buffer
        self.assigned_buffer = assigned_buffer
