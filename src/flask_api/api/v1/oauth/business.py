from flask_restx import abort
from flask_restx._http import HTTPStatus
from flask_api.security import create_tokens
from flask_api.models import User, db, OAuthAccount


def oauth_login_signup(sub, issuer, email, current_user):
    oauth_user: User | None = User.find_by_oauth(issuer, sub)
    jwt_user: User | None = User.find_by_id(current_user['sub']) if current_user else None
    if oauth_user and jwt_user:  # Найден oauth пользователь и есть токен
        if oauth_user == jwt_user:
            abort(HTTPStatus.BAD_REQUEST, 'OAuth profile already assign to the user.')
        abort(HTTPStatus.BAD_REQUEST, 'OAuth profile assign to another user. LogOut first.')
    if not oauth_user:  # Не найден oauth пользователь в бд
        oauth_user = jwt_user or User(email=email, password=sub)  # берем текущего поль-ля из токена или создаем нового
        oauth = OAuthAccount(issuer=issuer, sub=sub, user=oauth_user)  # присоединяем к поль-лю oauth акк
        db.session.add(oauth)
        db.session.commit()
    return create_tokens(oauth_user)  # Найден oauth пользователь в бд, логиним его или нового/текущего с oauth акк
