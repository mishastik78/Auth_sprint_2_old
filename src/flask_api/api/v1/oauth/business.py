import logging
import secrets
import string

from flask_restx import abort
from flask_restx._http import HTTPStatus

from flask_api.models import OAuthAccount, User, db
from flask_api.security import create_tokens

logger = logging.getLogger()


def oauth_login_signup(sub, issuer, email, current_user):
    oauth_user: User | None = User.find_by_oauth(issuer, sub)
    jwt_user: User | None = None
    if current_user:  # Токен передан, пользователь известен
        logger.debug('JWT present in request.')
        jwt_user = User.find_by_id(current_user['sub']['id'])
        if not jwt_user:
            abort(HTTPStatus.UNAUTHORIZED, 'JWT user not found in db.')
        if oauth_user:  # Найден oauth пользователь и есть токен
            if oauth_user == jwt_user:
                abort(HTTPStatus.BAD_REQUEST, 'OAuth profile already assign to the user.')
            abort(HTTPStatus.BAD_REQUEST, 'OAuth profile assign to another user. LogOut first.')
    if not oauth_user:  # Не найден oauth пользователь в бд
        logger.debug('OAuth user not found in db.')
        if not jwt_user:  # Не передан токен, пользователь не залогинен, создаем нового
            logger.debug('JWT not present in request.')
            if User.find_by_email(email):
                abort(HTTPStatus.BAD_REQUEST, 'User with given email already registered.'
                      'LogIn to assign this OAuth accout or use another one to SignUP here.')
            alphabet = string.ascii_letters + string.digits
            password = ''.join(secrets.choice(alphabet) for i in range(8))
            jwt_user = User(email=email, password=password)
        oauth = OAuthAccount(issuer=issuer, sub=sub, user=jwt_user)  # присоединяем к поль-лю oauth акк
        db.session.add(oauth)
        db.session.commit()
        oauth_user = jwt_user
    else:
        logger.debug('OAuth user (%s) found in db, logging one.', oauth_user.email)
    return create_tokens(oauth_user)  # Найден oauth пользователь в бд, логиним его или нового/текущего с oauth акк
