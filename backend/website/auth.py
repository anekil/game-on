from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms.validators import InputRequired, Length, EqualTo


auth = Blueprint('auth', __name__)


class LoginForm(FlaskForm):
    email = EmailField('Email Address', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)])


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                flash("Logged in", category="success")
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password", category="error")
        else:
            flash("User doesn't exist", category="error")
    return render_template("login.html",  user=current_user, form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm(request.form)
    if request.method == 'POST':
        email = form.email.data
        hash_password = generate_password_hash(form.password.data)
        user = User.query.filter_by(email=email).first()
        if user:
            flash("User already exists", category="error")
        else:
            new_user = User(email=email, password=hash_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created successfully", category="success")
            return redirect(url_for('views.home'))
    return render_template("register.html",  user=current_user, form=form)
