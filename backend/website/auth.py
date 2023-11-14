from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo


class LoginForm(FlaskForm):
    email = EmailField('Email Address', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])
    confirm = PasswordField('Confirm password', validators=[InputRequired(), Length(min=6, max=20), EqualTo('password', message='Passwords must match')])


def get_username(email):
    return email.split('@')[0]


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        flash(f"Hello { get_username(form.email.data) }!")
    return render_template("login.html", form=form)


@auth.route('/logout')
def logout():
    return render_template("home.html")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            flash("Account created successfully", category="success")
    return render_template("register.html", form=form)

