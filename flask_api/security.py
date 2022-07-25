import logging
from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from typing import Any

from flask import current_app
from flask_jwt_extended import (create_access_token,
                                create_refresh_token, decode_token, get_jti,
                                get_jwt)
from flask_jwt_extended.exceptions import NoAuthorizationError

from flask_api import jwt
from flask_api.models import User

from .cache import Cache
from .utils import utc_now

logger = logging.getLogger(__name__)
app = current_app

jwt_tokens_blocklist = Cache()
jwt_user_access_blocklist = Cache()
jwt_user_refresh_blocklist = Cache()


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return {
        'id': user.id,
        'roles': [{'id': role.id, 'name': role.name} for role in user.roles]
    }


@dataclass
class TokensResponse:
    access_token: str
    access_token_expired_utc: datetime
    refresh_token: str
    refresh_token_expired_utc: datetime


def create_tokens(user: User) -> TokensResponse:
    refresh_token = create_refresh_token(identity=user)
    access_token = create_access_token(identity=user, additional_claims={'refresh_jti': get_jti(refresh_token)})
    return TokensResponse(
        access_token,
        datetime.fromtimestamp(decode_token(access_token)['exp']),
        refresh_token,
        datetime.fromtimestamp(decode_token(refresh_token)['exp']),
    )


def set_tokens_revoked(jwt_payload: dict):
    jti = jwt_payload['jti']
    if jwt_tokens_blocklist.set(jti, '', ex=app.config['JWT_ACCESS_TOKEN_EXPIRES']):
        logger.info('Access token added to blocklist')
    refresh_jti = jwt_payload.get('refresh_jti')
    if refresh_jti and jwt_tokens_blocklist.set(refresh_jti, '', ex=app.config['JWT_REFRESH_TOKEN_EXPIRES']):
        logger.info('Refresh token added to blocklist')


def revoke_access_tokens(user_id):
    jwt_user_access_blocklist.set(str(user_id), datetime.timestamp(utc_now()),
                                  ex=app.config['JWT_ACCESS_TOKEN_EXPIRES'])


@jwt.token_in_blocklist_loader
def check_revoked_token(jwt_header, jwt_payload: dict):
    jti = jwt_payload['jti']
    revoked_token = jwt_tokens_blocklist.get(jti)
    if revoked_token is not None:
        logger.debug('Token found in blocklist - %s', revoked_token)
        return True
    type = jwt_payload['type']
    user_id = jwt_payload['sub']['id']
    if type == 'access' and (revoked_token := jwt_user_access_blocklist.get(user_id)):
        iat = datetime.fromtimestamp(jwt_payload['iat'])
        block_time = datetime.fromtimestamp(float(revoked_token))
        if block_time > iat:
            logger.debug('User found in access blocklist with time (%s) later than iat (%s)', block_time, iat)
            return True
    return False


def admin_required(fn) -> Any:
    '''
    A decorator to protect an admin only endpoints.
    Should be used after jwt_requred decorator.
    '''
    @wraps(fn)
    def decorator(*args, **kwargs):
        user_id = get_jwt()['sub']['id']
        user: User = User.find_by_id(user_id)
        if not user.is_superuser:
            raise NoAuthorizationError('Admin permissions required')
        return fn(*args, **kwargs)
    return decorator
