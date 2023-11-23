from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

import pymysql
pymysql.install_as_MySQLdb()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
DB_NAME = "db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dregyhdehdreh'

    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:root@database:3306/db'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Rating, Game, Genre, Theme, Keyword
    with app.app_context():
        db.drop_all()
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from .scripts import fetch_all_classification_data, fetch_games_data
    with app.app_context():
        fetch_all_classification_data()
        fetch_games_data()

    return app
