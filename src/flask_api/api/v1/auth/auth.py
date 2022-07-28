from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, fields, marshal
from flask_restx._http import HTTPStatus

from ..role.models import role_create_model

auth = Namespace('auth', description='Validating access token, authenticate users.')

user_roles_model = auth.model(
    'UserRoles',
    {
        'id': fields.String,
        'roles': fields.List(fields.Nested(role_create_model))
    }
)


@auth.route('', endpoint='auth')
@auth.doc(security='Bearer')
class Auth(Resource):
    @jwt_required(optional=True)
    @auth.response(int(HTTPStatus.OK), 'User authenticated. Access token valid.', model=user_roles_model)
    @auth.response(int(HTTPStatus.UPGRADE_REQUIRED), 'Anonymous User. No access token found.')
    @auth.response(int(HTTPStatus.UNAUTHORIZED), 'Token expired or revoked. Refresh required.')
    def get(self):
        """
        Authenticate user by JWT or return Anonimous user.
        Validate access token if present and return user id and roles.
        """
        if not get_jwt():
            return {'user': 'Anonymous User'}, HTTPStatus.UPGRADE_REQUIRED
        return marshal(get_jwt()['sub'], user_roles_model), 200
