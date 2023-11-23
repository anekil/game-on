from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .scripts import get_all_games, get_game

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


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
        "cover": game.cover,
        "url": game.url,
        "summary": game.summary,
        "total_rating": game.total_rating,
        "hypes": game.hypes,
        "genres": [item.name for item in game.genres],
        "themes":  [item.name for item in game.themes],
        "keywords": [item.name for item in game.keywords],
        "modes": [item.name for item in game.modes],
        "platforms": [item.name for item in game.platforms],
        "screenshots": [item for item in game.screenshots]
    }


@views.route('/games')
@login_required
def browse_games():
    return render_template("games.html", user=current_user, data=[serialize_game(game) for game in get_all_games()])


@views.route('/games/<game_title>')
@login_required
def game_details(game_title):
    return render_template("game.html", user=current_user, game=serialize_whole_game(get_game(game_title)))
