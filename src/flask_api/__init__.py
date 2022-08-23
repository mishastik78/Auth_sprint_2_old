import logging

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from flask_api import config
from .cache import Cache

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
oauth = OAuth()

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    oauth.init_app(app, cache=Cache())
    return app

def register_blueprints(app):
    from flask_api.api.v1 import apiv1
    app.register_blueprint(apiv1, url_prefix='/api/v1')

app = create_app(config.Config)
register_blueprints(app)
