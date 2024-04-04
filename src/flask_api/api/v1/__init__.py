from flask import Blueprint
from flask_restx import Api

from .account import acc
from .auth import auth
from .oauth import oauth_ns
from .role import role

apiv1 = Blueprint('api_v1', __name__,)
authorizations = {'Bearer': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'},}
api = Api(
    apiv1,
    version='1.0',
    title='Flask Auth API with JWT-Based Authentication',
    description='Welcome to the Swagger UI documentation site!',
    authorizations=authorizations,
)

api.add_namespace(oauth_ns, path='/oauth')
api.add_namespace(acc, path='/account')
api.add_namespace(role, path='/roles')
api.add_namespace(auth, path='/auth')
