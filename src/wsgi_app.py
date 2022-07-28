from gevent import monkey

monkey.patch_all()
from dotenv import load_dotenv

load_dotenv()
from flask_api import app
