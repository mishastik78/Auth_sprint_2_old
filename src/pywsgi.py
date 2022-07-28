from gevent import monkey

monkey.patch_all()

from dotenv import load_dotenv

load_dotenv()
from gevent.pywsgi import WSGIServer

from flask_api import app

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()
