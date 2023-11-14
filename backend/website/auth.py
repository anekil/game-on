from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])


def get_username(email):
    return email.split('@')[0]


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        flash(f"Hello { get_username(form.email.data) }!")
    return render_template("login.html", form=form)


@auth.route('/logout')
def logout():
    return render_template("home.html")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm(request.form)
    if request.method == 'POST':
        flash('Account created successfully!', category="success")
    return render_template("register.html", form=form)

