import os
import secrets
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, 'crypto.db')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.secret_key = secrets.token_urlsafe(16)
    db.init_app(app)

    from .views import views
    app.register_blueprint(views, url_prefix="/")

    from .models import Crypto
    create_database(app)

    return app

def create_database(app):
    if not os.path.join(basedir, 'crypto.db'):
        db.create_all(app=app)
    return "created successfully"