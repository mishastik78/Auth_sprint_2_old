from flask_restx import abort
from flask_restx._http import HTTPStatus

from flask_api.security import TokensResponse, create_tokens, set_tokens_revoked, revoke_access_tokens
from flask_api.models import User, db
import re

re_email = re.compile(r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$')
re_password = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W)[A-Za-z\d\W]{8,20}$')


def validate_request(payload):
    try:
        email = payload['email']
        password = payload['password']
    except KeyError:
        abort(HTTPStatus.BAD_REQUEST)
    return email, password


def validate_email(email):
    if not re.search(re_email, email):
        abort(HTTPStatus.BAD_REQUEST, f"'{email}' is not valid email address")
    return email


def validate_password(password):
    if not re.search(re_password, password):
        abort(HTTPStatus.BAD_REQUEST, f"'{password}' is not valid password (8-20chars, A-Za-z\\d\\W")
    return password


def create_user(email: str, password: str) -> TokensResponse:
    email = validate_email(email)
    password = validate_password(password)
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
    email = api.get('email')
    if email and email != user.email and validate_email(email):
        if User.find_by_email(email):
            abort(HTTPStatus.CONFLICT, "email address is already registered.")
        user.add_history(f'Email changed from {user.email} to {email}')
        user.email = email
    if password := api.get('password'):
        user.password = validate_password(password)
        user.add_history('Password changed')
    db.session.commit()
    revoke_access_tokens(user.id)
    return {'status': f'success change to {user.email}'}, HTTPStatus.OK


def get_history(jwt):
    user: User = User.find_by_id(jwt['sub']['id'])
    return user.get_history(10)
