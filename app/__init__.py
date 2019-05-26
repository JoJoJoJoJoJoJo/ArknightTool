# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import Config

db = SQLAlchemy()
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bootstrap.init_app(app)
    from app.controllers import main as main_bp
    app.register_blueprint(main_bp)
    return app
