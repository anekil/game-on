from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

from .scripts import get_all_games, get_game, get_game_rating, save_user_rating

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
        "slug": game.slug,
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


class RatingForm(FlaskForm):
    rating = SelectField('Rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')


@views.route('/games/<game_title>', methods=['GET', 'POST'])
@login_required
def game_details(game_title):
    form = RatingForm()
    game = get_game(game_title)
    rating = get_game_rating(current_user, game)

    if form.validate_on_submit():
        rating = form.rating.data
        save_user_rating(current_user, game, rating)
        flash('Rating submitted successfully', category='success')
    return render_template("game.html", user=current_user, form=form, rating=rating, game=serialize_whole_game(game))
