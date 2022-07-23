from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields, marshal
from flask_restx._http import HTTPStatus

auth = Namespace('auth', description='Validating access token, authenticate users.')

user_roles_model = auth.model(
    'UserRoles',
    {
        'id': fields.String,
        'roles': fields.List(fields.Nested(
            {
                'id': fields.String,
                'name': fields.String,
            }
        ))
    }
)


@auth.route('', endpoint='auth')
@auth.doc(security='Bearer')
class Auth(Resource):
    @jwt_required(optional=True)
    @auth.response(int(HTTPStatus.OK), 'User authenticated. Access token valid.')
    @auth.response(int(HTTPStatus.UPGRADE_REQUIRED), 'Anonymous User. No access token found.')
    @auth.response(int(HTTPStatus.UNAUTHORIZED), 'Token expired or revoked. Refresh required.')
    def get(self):
        if not get_jwt():
            return {'user': 'Anonymous User'}, HTTPStatus.UPGRADE_REQUIRED
        return marshal(get_jwt()['sub'], user_roles_model)
