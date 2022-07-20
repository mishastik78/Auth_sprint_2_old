from flask_api.jwt import admin_required
from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, marshal
from flask_restx._http import HTTPStatus

from .business import create_role, get_roles, delete_role, edit_role, assign_role, unassign_role, get_user_roles
from .models import role_model, user_roles

role = Namespace("role", description="Roles accounts operations", validate=True)
role.models[role_model.name] = role_model
role.models[user_roles.name] = user_roles


@role.route('/manage')
@role.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or no token or no admin permissions.')
@role.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class Roles(Resource):
    @jwt_required()
    @admin_required
    @role.expect(role_model)
    @role.marshal_with(role_model, code=HTTPStatus.CREATED)
    @role.response(int(HTTPStatus.CONFLICT), 'Role with given name is exists.')
    @role.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    def post(self):
        '''Create role'''
        return create_role(role.payload)

    @jwt_required()
    @admin_required
    @role.marshal_list_with(role_model, code=HTTPStatus.OK)
    def get(self):
        '''Receive all roles'''
        return get_roles()


@role.route('/manage/<uuid:role_id>')
@role.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or no token or no admin permissions.')
@role.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class RolesParam(Resource):
    @jwt_required()
    @admin_required
    @role.response(int(HTTPStatus.OK), 'Role deleted.')
    @role.response(int(HTTPStatus.NOT_FOUND), 'Role not found.')
    def delete(self, role_id):
        '''Remove role'''
        return delete_role(role_id)

    @jwt_required()
    @admin_required
    @role.expect(role_model)
    @role.marshal_with(role_model, code=HTTPStatus.OK)
    @role.response(int(HTTPStatus.NOT_FOUND), 'Role not found.')
    def patch(self, role_id):
        '''Edit role'''
        return edit_role(role_id, role.payload)


@role.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or no token or no admin permissions.')
@role.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
@role.route('/assign/<uuid:user_id>')
class Assign(Resource):
    @jwt_required()
    @admin_required
    @role.expect(role_model)
    @role.response(int(HTTPStatus.NOT_FOUND), 'User or Role not found.')
    def post(self, user_id):
        '''Assign role to user'''
        data = assign_role(user_id, role.payload)
        return marshal(data, user_roles)

    @jwt_required()
    @admin_required
    @role.expect(role_model)
    @role.response(int(HTTPStatus.NOT_FOUND), 'User or Role not found.')
    def delete(self, user_id):
        '''Remove role from user'''
        data = unassign_role(user_id, role.payload)
        return marshal(data, user_roles)

    @jwt_required()
    @admin_required
    @role.response(int(HTTPStatus.NOT_FOUND), 'User not found.')
    def get(self, user_id):
        '''Get all coount roles'''
        data = get_user_roles(user_id)
        return marshal(data, user_roles)
