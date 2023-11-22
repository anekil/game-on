from typing import Optional, List

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import mapped_column, Mapped, relationship, DeclarativeBase

from . import db
from flask_login import UserMixin


class Base(DeclarativeBase):
    pass


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String, nullable=False)
    ratings: Mapped[List["Rating"]] = relationship(back_populates="user")


class Rating(db.Model):
    __tablename__ = "ratings"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    rating: Mapped[int] = mapped_column(db.Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="ratings")
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"))
    game: Mapped["Game"] = relationship(back_populates="ratings")


game_genres = Table(
    'game_genres',
    Base.metadata,
    Column('game_id', ForeignKey('games.id')),
    Column('genre_id', ForeignKey('genres.id'))
)
game_themes = Table(
    'game_themes',
    Base.metadata,
    Column('game_id', ForeignKey('games.id')),
    Column('theme_id', ForeignKey('themes.id'))
)
game_keywords = Table(
    'game_keywords',
    Base.metadata,
    Column('game_id', ForeignKey('games.id')),
    Column('keyword_id', ForeignKey('keywords.id'))
)


class Genre(db.Model):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    api_id: Mapped[int] = mapped_column(db.Integer, unique=True)
    name: Mapped[str] = mapped_column(db.String)


class Theme(db.Model):
    __tablename__ = "themes"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    api_id: Mapped[int] = mapped_column(db.Integer, unique=True)
    name: Mapped[str] = mapped_column(db.String)


class Keyword(db.Model):
    __tablename__ = "keywords"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    api_id: Mapped[int] = mapped_column(db.Integer, unique=True)
    name: Mapped[str] = mapped_column(db.String)


class Game(db.Model):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    api_id: Mapped[int] = mapped_column(db.Integer, unique=True)
    name: Mapped[str] = mapped_column(db.String)
    url: Mapped[str] = mapped_column(db.String)
    summary: Mapped[Optional[str]] = mapped_column(db.String)
    cover: Mapped[Optional[str]] = mapped_column(db.String)
    total_rating: Mapped[Optional[int]] = mapped_column(db.Integer)
    genres: Mapped[List[Genre]] = relationship(secondary=game_genres)
    themes: Mapped[List[Theme]] = relationship(secondary=game_themes)
    keywords: Mapped[List[Keyword]] = relationship(secondary=game_keywords)
    screenshots: Mapped[Optional[JSON]] = mapped_column(db.JSON)
    ratings: Mapped[List["Rating"]] = relationship(back_populates="game")
