from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
