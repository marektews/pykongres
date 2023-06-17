from .dbBase import db


class Rozklad(db.Model):
    __tablename__ = "Rozklad"

    id = db.Column(db.Integer, primary_key=True)
    sra_id = db.Column(db.Integer, nullable=False)
    sektor_id = db.Column(db.Integer, nullable=False)
    a1 = db.Column(db.Time, nullable=True)
    a2 = db.Column(db.Time, nullable=True)
    a3 = db.Column(db.Time, nullable=True)
    d1 = db.Column(db.Time, nullable=True)
    d2 = db.Column(db.Time, nullable=True)
    d3 = db.Column(db.Time, nullable=True)

    def __init__(self, sra_id, sektor_id, d1, d2, d3, a1, a2, a3):
        self.sra_id = sra_id
        self.sektor_id = sektor_id
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
