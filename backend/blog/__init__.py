import os

from flask import Flask
from flask_gzip import Gzip
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


def create_app(config=None, instance_path=None):
    app = Flask(
        __name__,
        instance_path=instance_path,
        instance_relative_config=True,
    )

    Gzip(app)
    CORS(app, resources={"*": {"origins": "*"}})
    JWTManager(app)

    app.config.from_mapping(
        SITE_URL="http://127.0.0.1:3000",
        API_URL="http://127.0.0.1:5000",

        SECRET_KEY="dev",
        DEBUG=True,
        OWNER_DATA="owner:password",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(
            app.instance_path, 'blog-db.sqlite'
        ),
        IMAGES_FOLDER=os.path.join(app.instance_path, 'images'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,

        PROPAGATE_EXCEPTIONS=True,
    )

    if config is None:
        app.config.from_pyfile("config.cfg", silent=True)
    else:
        app.config.from_mapping(config)

    # Create folders
    for path in (app.instance_path, app.config['IMAGES_FOLDER']):
        try:
            os.makedirs(path)
        except OSError:
            pass

    from .resources import api
    api.init_app(app)

    from . import models

    from .database import db
    db.init_app(app)

    Migrate(app, db)

    return app
