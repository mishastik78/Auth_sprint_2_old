import logging
from flask_api import config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    return app

def register_blueprints(app):
    from flask_api.api.v1 import apiv1
    from flask_api.cli import command
    app.register_blueprint(apiv1, url_prefix='/api/v1')
    app.register_blueprint(command)

app = create_app(config.Config)
register_blueprints(app)
