from requests import request
from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/games')
@login_required
def games():
    url = "https://api.igdb.com/v4/games"
    payload = "fields name, cover.url, total_rating; limit 50; where total_rating > 50 & category = 0; sort total_rating_count desc; "
    headers = {
        'Authorization': 'Bearer 7uasv2bw3iyqjavppma1c5yntc1geo',
        'Client-ID': 't6vglpbbejgf6vm4ptt5q5lsrlros2',
    }
    response = request("POST", url, headers=headers, data=payload)
    data = response.json()
    return render_template("games.html", user=current_user, data=data)
