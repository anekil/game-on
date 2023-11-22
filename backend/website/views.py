from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Game

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


def serialize_game(game):
    return {
        "id": game.id,
        "name": game.name,
        "url": game.url,
        "summary": game.summary,
        "cover": game.cover,
        "total_rating": game.total_rating,
        "genres": [item.name for item in game.genres],
        "themes":  [item.name for item in game.themes],
        "keywords":  [item.name for item in game.keywords],
        "screenshots": game.screenshots
    }


@views.route('/games')
@login_required
def games():
    game = Game.query.get(1)
    return render_template("games.html", user=current_user, data=serialize_game(game))
