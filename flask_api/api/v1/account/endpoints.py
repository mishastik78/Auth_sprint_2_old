from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource
from flask_restx._http import HTTPStatus

from .business import (changing, create_user, get_history, login_user,
                       logout_user, refresh_tokens, validate_request)
from .models import auth_model, changing_model, history_model, tokens_model

acc = Namespace("account", description="Account operations", validate=True)
acc.models[auth_model.name] = auth_model
acc.models[tokens_model.name] = tokens_model
acc.models[changing_model.name] = changing_model
acc.models[history_model.name] = history_model


@acc.route('/signup', endpoint='signup')
class SignUp(Resource):
    @acc.expect(auth_model)
    @acc.marshal_with(tokens_model, code=HTTPStatus.CREATED)
    @acc.response(int(HTTPStatus.CONFLICT), 'Email address is already registered.')
    @acc.response(int(HTTPStatus.BAD_REQUEST), 'Validation error.')
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        '''Register a new user and return tokens.'''
        email, password = validate_request(acc.payload)
        return create_user(email, password), 201


@acc.route('/login', endpoint='login')
class LogIn(Resource):
    @acc.expect(auth_model)
    @acc.marshal_with(tokens_model, code=HTTPStatus.OK)
    @acc.response(int(HTTPStatus.UNAUTHORIZED), "Email and/or password does not match.")
    @acc.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        '''Authenticate an existing user and return tokens.'''
        email, password = validate_request(acc.payload)
        return login_user(email, password)


@acc.route('/logout', endpoint='logout')
class LogOut(Resource):
    @jwt_required()
    @acc.doc(security='Bearer')
    @acc.response(int(HTTPStatus.OK), "Succeeded, tokens is no longer valid.")
    @acc.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or no token.")
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def delete(self):
        '''
        Mark tokens as invoked, deauthenticating the current user.
        Must be called for Access token only.
        '''
        jwt = get_jwt()
        return logout_user(jwt)


@acc.route('/refresh')
class TokensRefresh(Resource):
    @jwt_required(refresh=True)
    @acc.doc(security='Bearer')
    @acc.marshal_with(tokens_model, code=HTTPStatus.OK)
    @acc.response(int(HTTPStatus.UNAUTHORIZED), "Token expired or invoked, Login process required.")
    @acc.response(int(HTTPStatus.BAD_REQUEST), "Token is invalid or no token.")
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        '''Generating new Access and Fefresh tokens.'''
        jwt = get_jwt()
        return refresh_tokens(jwt)


@acc.route('/changing-cridentials')
class Change(Resource):
    @jwt_required()
    @acc.doc(security='Bearer')
    @acc.expect(changing_model)
    @acc.response(int(HTTPStatus.OK), "Changing succeeded.")
    @acc.response(int(HTTPStatus.CONFLICT), 'Email address is already registered.')
    @acc.response(int(HTTPStatus.UNAUTHORIZED), "Token expired or invoked, Login required.")
    @acc.response(int(HTTPStatus.BAD_REQUEST), "Token is invalid or no token.")
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def patch(self):
        '''
        Canging user's email or/and password
        At least one of the fields is required.
        '''
        jwt = get_jwt()
        api = acc.payload
        return changing(jwt, api)


@acc.route('/history')
class UserHistory(Resource):
    @jwt_required()
    @acc.doc(security='Bearer')
    @acc.marshal_list_with(history_model, )
    @acc.response(int(HTTPStatus.OK), "History provided.", history_model)
    @acc.response(int(HTTPStatus.UNAUTHORIZED), "Token expired or invoked, refresh required.")
    @acc.response(int(HTTPStatus.BAD_REQUEST), "Token is invalid or no token.")
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def get(self):
        '''Provides history of user's account actions.'''
        return get_history(get_jwt())
