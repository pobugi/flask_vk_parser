from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

import config

db = SQLAlchemy()


def create_app(app_settings=config.ProductionConfig):
    app = Flask(__name__)

    app.config.from_object(app_settings)

    db.init_app(app)
    from src.api.parser.views import vk_parser_api

    app.register_blueprint(vk_parser_api)

    app.engine = create_engine(app.config["DATABASE_URL"])
    if not database_exists(app.engine.url):
        create_database(app.engine.url)

    with app.app_context():
        db.create_all()

    return app
