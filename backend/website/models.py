from typing import Optional, List

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import mapped_column, Mapped, relationship

from . import db, Base
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)
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
game_modes = Table(
    'game_modes',
    Base.metadata,
    Column('game_id', ForeignKey('games.id')),
    Column('mode_id', ForeignKey('modes.id'))
)
game_platforms = Table(
    'game_platforms',
    Base.metadata,
    Column('game_id', ForeignKey('games.id')),
    Column('platform_id', ForeignKey('platforms.id'))
)


class Genre(db.Model):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(80))


class Theme(db.Model):
    __tablename__ = "themes"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(80))


class Keyword(db.Model):
    __tablename__ = "keywords"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(80))


class Mode(db.Model):
    __tablename__ = "modes"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(40))


class Platform(db.Model):
    __tablename__ = "platforms"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(40))


class Game(db.Model):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(80))
    slug: Mapped[str] = mapped_column(db.String(90))
    url: Mapped[str] = mapped_column(db.String(100))
    summary: Mapped[Optional[str]] = mapped_column(db.String(4000))
    cover: Mapped[Optional[str]] = mapped_column(db.String(100))
    total_rating: Mapped[Optional[int]] = mapped_column(db.Integer)
    hypes: Mapped[Optional[int]] = mapped_column(db.Integer)
    genres: Mapped[List[Genre]] = relationship(secondary=game_genres)
    themes: Mapped[List[Theme]] = relationship(secondary=game_themes)
    keywords: Mapped[List[Keyword]] = relationship(secondary=game_keywords)
    modes: Mapped[List[Mode]] = relationship(secondary=game_modes)
    platforms: Mapped[List[Platform]] = relationship(secondary=game_platforms)
    screenshots: Mapped[Optional[JSON]] = mapped_column(db.JSON)
    ratings: Mapped[List["Rating"]] = relationship(back_populates="game")
