from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .api.v1 import apiv1

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(apiv1, url_prefix='/api/v1/')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
