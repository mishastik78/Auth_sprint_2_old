from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, marshal
from flask_restx._http import HTTPStatus

from flask_api.security import admin_required

from .business import (assign_role, create_role, delete_role, edit_role,
                       get_roles, get_user_roles, unassign_role)
from .models import role_assign_model, role_create_model, user_roles, role_patch_model, role_delete_model

role = Namespace("role", description="Roles accounts operations", validate=True)
role.models[role_create_model.name] = role_create_model
role.models[user_roles.name] = user_roles
role.models[role_assign_model.name] = role_assign_model
role.models[role_patch_model.name] = role_patch_model
role.models[role_delete_model.name] = role_delete_model


@role.route('/manage', endpoint='manage')
@role.doc(security='Bearer')
@role.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or no token or no admin permissions.')
@role.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class Roles(Resource):
    @jwt_required()
    @admin_required
    @role.expect(role_create_model)
    @role.marshal_with(role_create_model, code=HTTPStatus.CREATED)
    @role.response(int(HTTPStatus.CONFLICT), 'Role with given name exists.')
    @role.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    def post(self):
        '''Create role'''
        return create_role(role.payload), HTTPStatus.CREATED

    @jwt_required()
    @admin_required
    @role.marshal_list_with(role_create_model, code=HTTPStatus.OK)
    def get(self):
        '''Receive all roles'''
        return get_roles()

    @jwt_required()
    @admin_required
    @role.expect(role_patch_model)
    @role.marshal_with(role_create_model, code=HTTPStatus.OK)
    @role.response(int(HTTPStatus.CONFLICT), 'Role with given name exists.')
    @role.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @role.response(int(HTTPStatus.NOT_FOUND), 'Role not found.')
    def patch(self):
        '''Edit role'''
        return edit_role(role.payload)

    @jwt_required()
    @admin_required
    @role.expect(role_delete_model)
    @role.response(int(HTTPStatus.OK), 'Role deleted.')
    @role.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @role.response(int(HTTPStatus.NOT_FOUND), 'Role not found.')
    def delete(self):
        '''Delete role'''
        return delete_role(role.payload)


@role.route('/assign', endpoint='assign')
@role.doc(security='Bearer')
@role.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or no token or no admin permissions.')
@role.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class Assign(Resource):
    @jwt_required()
    @admin_required
    @role.expect(role_assign_model)
    @role.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @role.response(int(HTTPStatus.NOT_FOUND), 'User or Role not found.')
    def post(self):
        '''Assign role to user'''
        data = assign_role(role.payload)
        return marshal(data, user_roles)

    @jwt_required()
    @admin_required
    @role.expect(role_assign_model)
    @role.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @role.response(int(HTTPStatus.NOT_FOUND), 'User or Role not found.')
    def delete(self):
        '''Remove role from user'''
        data = unassign_role(role.payload)
        return marshal(data, user_roles)


@role.route('/view-user-roles/<uuid:user_id>', endpoint='view')
@role.doc(security='Bearer')
@role.response(int(HTTPStatus.UNAUTHORIZED), 'Token is invalid or no token or no admin permissions.')
@role.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
class ViewRoles(Resource):
    @jwt_required()
    @admin_required
    @role.response(int(HTTPStatus.NOT_FOUND), 'User not found.')
    def get(self, user_id):
        '''Get all user's roles'''
        data = get_user_roles(user_id)
        return marshal(data, user_roles)
