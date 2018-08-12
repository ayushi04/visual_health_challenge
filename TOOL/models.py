from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.Integer, nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, name="", phone="", password="", email=""):
        self.email = email
        self.phone = phone
        self.name = name
        self.password = password

    def __repr__(self):
        return "<User %s %s>" % (self.id, self.name)
