from .dbBase import db


class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.Integer, unique=True, nullable=False)
    hash = db.Column(db.String, unique=True, nullable=False)
    fn = db.Column(db.String, unique=False, nullable=False)
    ln = db.Column(db.String, unique=False, nullable=False)
    is_sra = db.Column(db.Integer, nullable=False, default=0)
    is_srp = db.Column(db.Integer, nullable=False, default=0)
    is_pk = db.Column(db.Integer, nullable=False, default=0)
    is_rja = db.Column(db.Integer, nullable=False, default=0)
    is_monitoring = db.Column(db.Integer, nullable=False, default=0)
    is_users = db.Column(db.Integer, nullable=False, default=0)
