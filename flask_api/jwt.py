from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from typing import Any
from .cache import Cache
from flask_api import app
import logging
from flask import _request_ctx_stack
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_api.models import User
from flask_jwt_extended import (JWTManager, create_access_token, get_current_user,
                                create_refresh_token, decode_token, get_jti, get_jwt)

logger = logging.getLogger(__name__)
jwt = JWTManager(app)
jwt_redis_blocklist = Cache()


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    return {
        'id': user.id,
        'roles': user.roles
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
    if jwt_redis_blocklist.set(jti, '', ex=app.config['JWT_ACCESS_TOKEN_EXPIRES']):
        logger.info('Access token added to blocklist')
    refresh_jti = jwt_payload.get('refresh_jti')
    if refresh_jti and jwt_redis_blocklist.set(refresh_jti, '', ex=app.config['JWT_REFRESH_TOKEN_EXPIRES']):
        logger.info('Refresh token added to blocklist')


@jwt.token_in_blocklist_loader
def check_revoked_token(jwt_header, jwt_payload: dict):
    jti = jwt_payload['jti']
    token_in_redis = jwt_redis_blocklist.get(jti)
    if token_in_redis is not None:
        logger.debug('Token found in blocklist - %s', token_in_redis)
    return token_in_redis is not None


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
