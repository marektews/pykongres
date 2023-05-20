from .dbBase import db


class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Integer, unique=True, nullable=False)
    hash = db.Column(db.String, unique=True, nullable=False)
    fn = db.Column(db.String, unique=False, nullable=False)
    ln = db.Column(db.String, unique=False, nullable=False)
