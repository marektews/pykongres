from .dbBase import db


class Pilot(db.Model):
    __tablename__ = "Pilot"

    id = db.Column(db.Integer, primary_key=True)
    fn = db.Column(db.String, nullable=False)
    ln = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)

    def __init__(self, firstname, lastname, email, phone):
        self.fn = firstname
        self.ln = lastname
        self.email = email
        self.phone = phone
