import uuid

from flask_restx import abort
from flask_restx._http import HTTPStatus

from flask_api.security import revoke_access_tokens
from flask_api.models import Role, User, db


def create_role(body):
    name = body['name']
    if Role.find_by_name(name):
        abort(HTTPStatus.CONFLICT, f'"{name}" is already exists', status='fail')
    description = body.get('description')
    new_role = Role(name=name, description=description)
    db.session.add(new_role)
    db.session.commit()
    return new_role


def get_roles():
    return Role.query.all()


def delete_role(id):
    if not (obj := Role.find_by_id(id)):
        abort(HTTPStatus.NOT_FOUND, f'Not found role with {id=}', status='fail')
    obj.delete()
    db.session.commit()
    return {'status': 'success deleted'}, HTTPStatus.OK


def edit_role(id, body):
    if not (obj := Role.find_by_id(id)):
        abort(HTTPStatus.NOT_FOUND, f'Not found role with {id=}', status='fail')
    new_name = body['name']
    if obj.name != new_name and Role.find_by_name(new_name):
        abort(HTTPStatus.CONFLICT, f'Role {body["name"]} is already registered.', status='fail')
    obj.name = new_name
    obj.description = body.get('description')
    db.session.commit()
    return obj


def validate_params(user_id, body) -> tuple[User, Role]:
    user = User.find_by_id(user_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, f'Not found user with {user_id=}', status='fail')
    try:
        id = body.get('id')
        if id:
            id = uuid.UUID(id)
    except ValueError:
        abort(HTTPStatus.BAD_REQUEST, 'id not uuid type', status='fail')
    name = None
    if id:
        role = Role.find_by_id(id)
    elif name := body.get('name'):
        role = Role.find_by_name(name)
    else:
        role = None
    if not role:
        abort(HTTPStatus.NOT_FOUND, f'Not found role with {id=} or {name=}', status='fail')
    return user, role


def assign_role(user_id, body):
    user, role = validate_params(user_id, body)
    user.roles.append(role)
    db.session.commit()
    revoke_access_tokens(user_id)
    return user


def unassign_role(user_id, body):
    user, role = validate_params(user_id, body)
    try:
        user.roles.remove(role)
        db.session.commit()
    except ValueError:
        abort(HTTPStatus.NOT_FOUND, "Role doesn't assign to the user", status='fail')
    revoke_access_tokens(user_id)
    return user


def get_user_roles(user_id):
    user = User.find_by_id(user_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, f'Not found user with {user_id=}', status='fail')
    return user
