from sqlalchemy import update

from . import db
from .models import Game, Rating


def get_all_games():
    return db.session.query(Game).all()


def get_sorted_games(limit):
    return (db.session.query(Game)
            .filter(Game.total_rating_count.isnot(None))
            .order_by(Game.total_rating_count.desc())
            .limit(limit).all())


def get_game(slug):
    return db.session.execute(db.select(Game).where(Game.slug.in_([slug]))).scalars().first()


def get_game_by_id(id):
    return Game.query.get(id)


def get_games(ids):
    return Game.query.filter(Game.id.in_(ids)).all()


def get_liked_games(user_id):
    return get_games_by_rating(user_id, 1)


def get_disliked_games(user_id):
    return get_games_by_rating(user_id, 0)


def get_games_by_rating(user_id, rating):
    ratings = Rating.query.filter_by(user_id=user_id)
    liked_games = [r.game for r in ratings if r.rating == rating]
    return liked_games


def get_game_rating(user_id, game_id):
    return Rating.query.filter_by(user_id=user_id, game_id=game_id).first()


def save_user_rating(user_id, game_id, new_rating):
    rating = db.session.execute(db.select(Rating).where(Rating.game_id == game_id, Rating.user_id == user_id)).scalar()
    if rating is None:
        rating = Rating(
            rating=new_rating,
            user_id=user_id,
            game_id=game_id
        )
        db.session.add(rating)
    else:
        db.session.execute(update(Rating).where(Rating.id == rating.id).values(rating=new_rating))
    db.session.commit()


def delete_rating(rating_id, user):
    rating = Rating.query.get(rating_id)
    if rating:
        if rating.user_id == user.id:
            db.session.delete(rating)
            db.session.commit()


def serialize_game(game):
    return {
        "id": game.id,
        "name": game.name,
        "slug": game.slug,
        "cover": game.cover,
        "genres": [item.name for item in game.genres],
        "themes":  [item.name for item in game.themes],
    }


def serialize_whole_game(game):
    return {
        "id": game.id,
        "name": game.name,
        "slug": game.slug,
        "cover": game.cover,
        "url": game.url,
        "summary": game.summary,
        "storyline": game.storyline,
        "total_rating": game.total_rating,
        "hypes": game.hypes,
        "genres": [item.name for item in game.genres],
        "themes":  [item.name for item in game.themes],
        "keywords": [item.name for item in game.keywords],
        "modes": [item.name for item in game.modes],
        "platforms": [item.name for item in game.platforms],
        "screenshots": [item for item in game.screenshots],
        "similar_games": [item for item in game.similar_games]
    }
