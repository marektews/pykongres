from .dbBase import db


class Dzialy(db.Model):
    __tablename__ = "Dzialy"

    id = db.Column(db.Integer, primary_key=True)
    lang = db.Column(db.String, unique=False, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
