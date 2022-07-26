from flask_restx import abort
from flask_restx._http import HTTPStatus

from flask_api.models import Role, User, db
from flask_api.security import revoke_access_tokens_by_user


def create_role(body):
    name = body['name']
    if Role.find_by_name(name):
        abort(HTTPStatus.CONFLICT, f'"{name}" is already exists.')
    description = body.get('description')
    new_role = Role(name=name, description=description)
    db.session.add(new_role)
    db.session.commit()
    return new_role


def get_roles():
    return Role.query.all()


def get_role_by_id(id):
    try:
        role = Role.find_by_id(id)
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST, 'Role ID is not valid uuid ver.4.')
    if not role:
        abort(HTTPStatus.BAD_REQUEST, f'Not found role with {id=}.')
    return role


def get_user_by_id(id):
    try:
        user = User.find_by_id(id)
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST, 'User ID is not valid uuid ver.4.')
    if not user:
        abort(HTTPStatus.BAD_REQUEST, f'Not found user with {id=}.')
    return user


def delete_role(body):
    role = get_role_by_id(body['id'])
    db.session.delete(role)
    db.session.commit()
    return {'status': 'success deleted'}, HTTPStatus.OK


def edit_role(body):
    role = get_role_by_id(body['id'])
    new_name = body.get('new_name') or role.name
    if role.name != new_name and Role.find_by_name(new_name):
        abort(HTTPStatus.CONFLICT, f'Role {new_name} is already registered.')
    role.name = new_name
    role.description = body.get('new_description') or role.description
    db.session.commit()
    return role


def assign_role(body):
    user = get_user_by_id(body['user_id'])
    role = get_role_by_id(body['role_id'])
    if role not in user.roles:
        user.roles.append(role)
        db.session.commit()
        revoke_access_tokens_by_user(user.id)
    return {'status': 'success'}


def unassign_role(body):
    user = get_user_by_id(body['user_id'])
    role = get_role_by_id(body['role_id'])
    if role not in user.roles:
        abort(HTTPStatus.NOT_FOUND, "Role doesn't assign to the user.")
    user.roles.remove(role)
    db.session.commit()
    revoke_access_tokens_by_user(user.id)
    return {'status': 'success'}


def check_user_role(body):
    user = get_user_by_id(body['user_id'])
    role = get_role_by_id(body['role_id'])
    if role not in user.roles:
        abort(HTTPStatus.NOT_FOUND, "Role doesn't assign to the user.")
    return {'status': 'success'}
