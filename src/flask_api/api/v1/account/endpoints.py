from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource
from flask_restx._http import HTTPStatus

from .business import (changing, completely_logout, create_user, get_history,
                       login_user, logout_user, refresh_tokens)
from .models import (changing_model, create_model, history_model, login_model,
                     tokens_model)

acc = Namespace('account', description='Account operations', validate=True)
acc.models[create_model.name] = create_model
acc.models[login_model.name] = login_model
acc.models[tokens_model.name] = tokens_model
acc.models[changing_model.name] = changing_model
acc.models[history_model.name] = history_model


@acc.route('/signup', endpoint='signup')
class SignUp(Resource):
    @acc.expect(create_model)
    @acc.marshal_with(tokens_model, code=HTTPStatus.CREATED)
    @acc.response(int(HTTPStatus.CONFLICT), 'Email address is already registered.')
    @acc.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.')
    def post(self):
        """Register a new user and return tokens."""
        return create_user(acc.payload), HTTPStatus.CREATED


@acc.route('/login', endpoint='login')
class LogIn(Resource):
    @acc.expect(login_model)
    @acc.marshal_with(tokens_model, code=HTTPStatus.OK)
    @acc.response(int(HTTPStatus.UNAUTHORIZED), 'Email and/or password does not match.')
    @acc.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.')
    def post(self):
        """Authenticate an existing user and return tokens."""
        return login_user(acc.payload)


@acc.route('/logout', endpoint='logout')
class LogOut(Resource):
    @jwt_required()
    @acc.doc(security='Bearer')
    @acc.response(int(HTTPStatus.OK), 'Succeeded, tokens is no longer valid.')
    @acc.response(int(HTTPStatus.UNAUTHORIZED), 'Token is expired or revoked. Refresh process required. '
                                                'Attention! Refresh token can still be valid.')
    @acc.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Token is invalid or no token.')
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.')
    def delete(self):
        """
        Mark tokens as invoked, deauthenticating the current user.
        Must be called for Access token only.
        """
        jwt = get_jwt()
        return logout_user(jwt)


@acc.route('/logout-all-sessions', endpoint='completely_logout')
class LogOutComplete(Resource):
    @jwt_required()
    @acc.doc(security='Bearer')
    @acc.marshal_with(tokens_model, code=HTTPStatus.OK, description='Succeeded, all user tokens is no longer valid. '
                      'New tokens issued.')
    @acc.response(int(HTTPStatus.UNAUTHORIZED), 'Token is expired or revoked. Refresh process required.')
    @acc.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Token is invalid or no token.')
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.')
    def delete(self):
        """
        Mark tokens as invoked, deauthenticating the current user on all devices.
        Must be called for Access token only. Only new tokens will be valid. New tokens issued.
        """
        jwt = get_jwt()
        return completely_logout(jwt)


@acc.route('/refresh', endpoint='refresh')
class TokensRefresh(Resource):
    @jwt_required(refresh=True)
    @acc.doc(security='Bearer')
    @acc.marshal_with(tokens_model, code=HTTPStatus.OK)
    @acc.response(int(HTTPStatus.UNAUTHORIZED), 'Token expired or invoked, Login process required.')
    @acc.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Token is invalid or no token.')
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.')
    def post(self):
        """
        Generating new Access and Fefresh tokens.
        Refresh token requried.
        """
        jwt = get_jwt()
        return refresh_tokens(jwt)


@acc.route('/changing-cridentials', endpoint='changing')
class Change(Resource):
    @jwt_required()
    @acc.doc(security='Bearer')
    @acc.expect(changing_model)
    @acc.response(int(HTTPStatus.OK), 'Changing succeeded.')
    @acc.response(int(HTTPStatus.CONFLICT), 'Email address is already registered.')
    @acc.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Token is invalid or no token.')
    @acc.response(int(HTTPStatus.UNAUTHORIZED), 'Token expired or invoked, refresh required.')
    @acc.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.')
    def patch(self):
        """
        Canging user's email or/and password
        At least one of the fields is required.
        Access token requried.
        """
        return changing(get_jwt(), acc.payload)


@acc.route('/history', endpoint='history')
class UserHistory(Resource):
    @jwt_required()
    @acc.doc(security='Bearer')
    @acc.marshal_list_with(history_model, code=HTTPStatus.OK)
    @acc.response(int(HTTPStatus.UNAUTHORIZED), 'Token expired or invoked, refresh required.')
    @acc.response(int(HTTPStatus.BAD_REQUEST), 'Token is invalid or no token.')
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), 'Internal server error.')
    def get(self):
        """
        Provides history of user's account actions.
        Access token requried.
        """
        return get_history(get_jwt())
