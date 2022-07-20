from flask_api.models import db, Role, User
from flask_restx import abort
from flask_restx._http import HTTPStatus


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
    role = Role.find_by_name(body['name'])
    if not role:
        abort(HTTPStatus.NOT_FOUND, f'Not found role with name={body["name"]}', status='fail')
    return user, role


def assign_role(user_id, body):
    user, role = validate_params(user_id, body)
    user.roles.append(role)
    db.session.commit()
    return user


def unassign_role(user_id, body):
    user, role = validate_params(user_id, body)
    try:
        user.roles.remove(role)
        db.session.commit()
    except ValueError:
        abort(HTTPStatus.NOT_FOUND, "Role doesn't assign to the user", status='fail')
    return user


def get_user_roles(user_id):
    user = User.find_by_id(user_id)
    if not user:
        abort(HTTPStatus.NOT_FOUND, f'Not found user with {user_id=}', status='fail')
    return user
