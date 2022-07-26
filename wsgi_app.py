from gevent import monkey

monkey.patch_all()

from flask_api import app
