from .dbBase import db


class Rozklad(db.Model):
    __tablename__ = "Rozklad"

    id = db.Column(db.Integer, primary_key=True)
    sra_id = db.Column(db.Integer, nullable=False)
    sektor_id = db.Column(db.Integer, nullable=False)
    bufor_id = db.Column(db.Integer, nullable=False)
    d1 = db.Column(db.Time, nullable=True)
    d2 = db.Column(db.Time, nullable=True)
    d3 = db.Column(db.Time, nullable=True)

    def __init__(self, sra_id, sektor_id, bufor_id, d1, d2, d3):
        self.sra_id = sra_id
        self.sektor_id = sektor_id
        self.bufor_id = bufor_id
        self.d1 = d1
        self.d2 = d2
        self.d3 = d3
