from .dbBase import db


class Sektory(db.Model):
    __tablename__ = "Sektory"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    tid = db.Column(db.Integer, nullable=False)

    def __init__(self, name, tid):
        self.name = name
        self.tid = tid
