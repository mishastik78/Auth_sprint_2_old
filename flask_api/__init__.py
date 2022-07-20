from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from .api.v1 import apiv1
app.register_blueprint(apiv1, url_prefix='/api/v1')

from .cli import cli
app.register_blueprint(cli)
