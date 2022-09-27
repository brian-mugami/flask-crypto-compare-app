import datetime
from website import db


class Crypto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    date = db.Column(db.DateTime(), default= datetime.datetime.utcnow())
    crypto_name = db.Column(db.String(80))

    def __init__(self, name, crypto_name):
        self.name = name
        self.crypto_name = crypto_name