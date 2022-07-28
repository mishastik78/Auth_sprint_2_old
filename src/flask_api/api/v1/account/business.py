from flask_restx import abort
from flask_restx._http import HTTPStatus

from flask_api.models import User, db
from flask_api.security import (TokensResponse, create_tokens,
                                revoke_access_tokens_by_user,
                                revoke_refresh_tokens_by_user,
                                set_tokens_revoked)


def validate_request(body):
    try:
        email = body['email']
        password = body['password']
    except KeyError:
        abort(HTTPStatus.BAD_REQUEST)
    return email, password


def create_user(body) -> TokensResponse:
    email, password = validate_request(body)
    if User.find_by_email(email):
        abort(HTTPStatus.CONFLICT, f"'{email}' is already registered")
    new_user = User(email=email, password=password)
    new_user.add_history('SignUp')
    db.session.add(new_user)
    db.session.commit()
    return create_tokens(new_user)


def login_user(body) -> TokensResponse:
    email, password = validate_request(body)
    user: User = User.find_by_email(email)
    if not user or not user.verify_password(password):
        if user:
            user.add_history('Wrong password')
        abort(HTTPStatus.UNAUTHORIZED, "email or password does not match")
    user.add_history('LogIn success')
    return create_tokens(user)


def logout_user(payload: dict):
    user = User.find_by_id(payload['sub']['id'])
    if not set_tokens_revoked(payload):
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'Tokens not revoked.')
    user.add_history('LogOut success')
    return {'status': f'success logout {user.email}'}, HTTPStatus.OK


def completely_logout(payload: dict):
    user = User.find_by_id(payload['sub']['id'])
    if not (revoke_access_tokens_by_user(user.id) and revoke_refresh_tokens_by_user(user.id)):
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'Tokens not revoked.')
    user.add_history('LogOut all profiles')
    return create_tokens(user)


def refresh_tokens(payload: dict):
    user = User.find_by_id(payload['sub']['id'])
    if not set_tokens_revoked(payload):
        abort(HTTPStatus.INTERNAL_SERVER_ERROR, 'Token not revoked.')
    return create_tokens(user)


def changing(jwt: dict, api):
    user: User = User.find_by_id(jwt['sub']['id'])
    email = api.get('email')
    if email and email != user.email:
        if User.find_by_email(email):
            abort(HTTPStatus.CONFLICT, "email address is already registered.")
        user.add_history(f'Email changed from {user.email} to {email}')
        user.email = email
    if password := api.get('password'):
        user.password = password
        user.add_history('Password changed')
    db.session.commit()
    revoke_access_tokens_by_user(user.id)
    return {'status': 'success changed'}, HTTPStatus.OK


def get_history(jwt):
    user: User = User.find_by_id(jwt['sub']['id'])
    return user.get_history(10)
