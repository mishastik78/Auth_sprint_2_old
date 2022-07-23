from flask_restx import abort
from flask_restx._http import HTTPStatus

from flask_api.security import TokensResponse, create_tokens, set_tokens_revoked
from flask_api.models import User, db


def validate_request(payload):
    try:
        email = payload['email']
        password = payload['password']
    except KeyError:
        abort(HTTPStatus.BAD_REQUEST)
    return email, password


def create_user(email: str, password: str) -> TokensResponse:
    if User.find_by_email(email):
        abort(HTTPStatus.CONFLICT, f"'{email}' is already registered")
    new_user = User(email=email, password=password)
    new_user.add_history('SignUp')
    db.session.add(new_user)
    db.session.commit()
    return create_tokens(new_user)


def login_user(email: str, password: str) -> TokensResponse:
    user: User = User.find_by_email(email)
    if not user or not user.verify_password(password):
        if user:
            user.add_history('Wrong password')
        abort(HTTPStatus.UNAUTHORIZED, "email or password does not match")
    user.add_history('LogIn success')
    return create_tokens(user)


def logout_user(payload: dict):
    user = User.find_by_id(payload['sub']['id'])
    set_tokens_revoked(payload)
    user.add_history('LogOut success')
    return {'status': f'success logout {user.email}'}, HTTPStatus.OK


def refresh_tokens(payload: dict):
    user = User.find_by_id(payload['sub']['id'])
    set_tokens_revoked(payload)
    return create_tokens(user)


def changing(jwt: dict, api):
    user: User = User.find_by_id(jwt['sub']['id'])
    if email := api.get('email'):
        if User.find_by_email(email):
            abort(HTTPStatus.CONFLICT, "email address is already registered.")
        user.add_history(f'Email changed from {user.email} to {email}')
        user.email = email
    if password := api.get('password'):
        user.password = password
        user.add_history('Password changed')
    db.session.commit()
    return {'status': f'success change to {user.email}'}, HTTPStatus.OK


def get_history(jwt):
    user: User = User.find_by_id(jwt['sub']['id'])
    return user.get_history(10)
