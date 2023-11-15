from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


def get_username(email):
    return email.split('@')[0]


@views.route('/')
@login_required
def home():
    return render_template("home.html", username=get_username(current_user.email))
