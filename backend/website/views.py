import json

from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from wtforms.validators import DataRequired

from .recommendation.recommendation import recommend_something
from .scripts import get_game, get_game_rating, save_user_rating, delete_rating, serialize_game, \
    serialize_whole_game, get_game_by_id, get_sorted_games

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    recommendations = [serialize_game(game) for game in recommend_something()]
    return render_template("home.html", user=current_user, data=recommendations)


@views.route('/games')
@login_required
def browse_games():
    return render_template("browse.html", user=current_user, data=[serialize_game(game) for game in get_sorted_games(100)])


class RatingForm(FlaskForm):
    rating = RadioField('Rating', choices=[(x, str(x)) for x in range(1, 6).__reversed__()], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')


@views.route('/games/<game_title>', methods=['GET', 'POST'])
@login_required
def game_details(game_title):
    form = RatingForm()
    game = get_game(game_title)
    rating = get_game_rating(current_user.id, game.id)
    similar_games = [serialize_game(get_game_by_id(game)) if get_game_by_id(game) else None for game in game.similar_games]

    if form.validate_on_submit():
        new_rating = form.rating.data
        save_user_rating(current_user.id, game.id, new_rating)
        flash('Rating submitted successfully', category='success')
    return render_template("game.html", user=current_user, form=form, rating=rating,
                           game=serialize_whole_game(game), similars=similar_games)


@views.route('/rating-delete', methods=['POST'])
@login_required
def rating_delete():
    data = json.loads(request.data)
    delete_rating(data['ratingId'], current_user)
    return jsonify({})


@views.route('/recommend')
@login_required
def recommend():
    df = recommend_something()
    #table = df.to_html(classes='table table-striped')
    return render_template('index.html',  user=current_user, data=df)
