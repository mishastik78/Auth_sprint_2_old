from flask import Blueprint
from flask_restx import Api
from .account import acc

apiv1 = Blueprint('api_v1', __name__,)
authorizations = {'AccessJWT': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'},
                  'RefreshJWT': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'}}
api = Api(
    apiv1,
    version='1.0',
    title='Auth REST API',
    description='Auth REST API',
    authorizations=authorizations,
)


api.add_namespace(acc, path='/account')
