from flask import Blueprint
from flask_restx import Api
from .account import acc
from .role import role

apiv1 = Blueprint('api_v1', __name__,)
authorizations = {'Bearer': {'type': 'apiKey', 'in': 'header', 'name': 'Authorization'},}
api = Api(
    apiv1,
    version='1.0',
    title='Auth REST API with JWT-based session',
    description='Wellcome Auth REST API',
    authorizations=authorizations,
)


api.add_namespace(acc, path='/account')
api.add_namespace(role, path='/roles')
