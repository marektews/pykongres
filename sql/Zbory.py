from .dbBase import db


class Zbory(db.Model):
    __tablename__ = "Zbory"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    lang = db.Column(db.String, unique=False, nullable=False)
