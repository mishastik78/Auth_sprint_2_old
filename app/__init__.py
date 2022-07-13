from flask import Flask
from api.v1 import api_v1

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.register_blueprint(api_v1, url_prefix='api/v1/')