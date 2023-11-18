from . import db
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import ARRAY


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(300))
    ratings = db.relationship('Rating', lazy=True)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    rating = db.Column(db.Integer)


game_genres = db.Table(
    'game_genres',
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)
game_themes = db.Table(
    'game_themes',
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True),
    db.Column('theme_id', db.Integer, db.ForeignKey('themes.id'), primary_key=True)
)
game_keywords = db.Table(
    'game_keywords',
    db.Column('game_id', db.Integer, db.ForeignKey('games.id'), primary_key=True),
    db.Column('keyword_id', db.Integer, db.ForeignKey('keywords.id'), primary_key=True)
)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(40))
    url = db.Column(db.String(80))
    summary = db.Column(db.String(600), nullable=True)
    cover = db.Column(db.String(80), nullable=True)
    total_rating = db.Column(db.Integer, nullable=True)
    genres = db.relationship('Genre', secondary=game_genres, backref=db.backref('games', lazy='dynamic'))
    themes = db.relationship('Theme', secondary=game_themes, backref=db.backref('games', lazy='dynamic'))
    keywords = db.relationship('Keyword', secondary=game_keywords, backref=db.backref('games', lazy='dynamic'))
    screenshots = db.Column(ARRAY(db.String), nullable=True)


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)


class Theme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)


class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
