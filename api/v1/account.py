from .config import api
from flask_restx import Resource

acc = api.namespace("account", description="Account operations")
api.add_namespace(acc)


@acc.route('signup')
class Signup(Resource):
    def post(self):
        pass
