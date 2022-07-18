from http import HTTPStatus

from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource

from .models import auth_model, changing_model, history_model, tokens_model

acc = Namespace("account", description="Account operations", validate=True)
acc.models[auth_model.name] = auth_model
acc.models[tokens_model.name] = tokens_model
acc.models[changing_model.name] = changing_model
acc.models[history_model.name] = history_model


@acc.route('/signup')
class SignUp(Resource):
    @acc.expect(auth_model)
    @acc.response(int(HTTPStatus.CREATED), "New user was successfully created.", tokens_model)
    @acc.response(int(HTTPStatus.CONFLICT), "Email address is already registered.")
    @acc.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        '''Register a new user and return tokens.'''
        pass


@acc.route('/login')
class LogIn(Resource):
    @acc.expect(auth_model)
    @acc.response(int(HTTPStatus.OK), "Login succeeded.", tokens_model)
    @acc.response(int(HTTPStatus.UNAUTHORIZED), "Email and/or password does not match.")
    @acc.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        '''Authenticate an existing user and return tokens.'''
        pass


@acc.route('/logout')
class LogOut(Resource):
    @jwt_required(verify_type=False)
    @acc.doc(security=('AccessJWT', 'RefreshJWT'))
    @acc.response(int(HTTPStatus.OK), "Succeeded, token is no longer valid.")
    @acc.response(int(HTTPStatus.BAD_REQUEST), "Token is invalid or no token.")
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def delete(self):
        '''
        Mark token as invoked, deauthenticating the current user.
        Must be called for Access and Refresh Tokens separately.
        '''
        pass


@acc.route('/refresh')
class TokensRefresh(Resource):
    @jwt_required(refresh=True)
    @acc.doc(security='RefreshJWT')
    @acc.response(int(HTTPStatus.OK), "Refresh succeeded.", tokens_model)
    @acc.response(int(HTTPStatus.UNAUTHORIZED), "Token expired or invoked, Login process required.")
    @acc.response(int(HTTPStatus.BAD_REQUEST), "Token is invalid or no token.")
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        '''Generating new Access and Fefresh tokens.'''
        pass


@acc.route('/changing-cridentials')
class Change(Resource):
    @jwt_required()
    @acc.doc(security='AccessJWT')
    @acc.expect(changing_model)
    @acc.response(int(HTTPStatus.OK), "Refresh succeeded.", tokens_model)
    @acc.response(int(HTTPStatus.UNAUTHORIZED), "Token expired or invoked, Login required.")
    @acc.response(int(HTTPStatus.BAD_REQUEST), "Token is invalid or no token.")
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def patch(self):
        '''
        Canging user's email or/and password
        At least one of the fields is required.
        '''
        pass


@acc.route('/history')
class UserHistory(Resource):
    @jwt_required()
    @acc.doc(security='AccessJWT')
    @acc.marshal_list_with(history_model, )
    @acc.response(int(HTTPStatus.OK), "History provided.", history_model)
    @acc.response(int(HTTPStatus.UNAUTHORIZED), "Token expired or invoked, refresh required.")
    @acc.response(int(HTTPStatus.BAD_REQUEST), "Token is invalid or no token.")
    @acc.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def get(self):
        '''Provides history of user's account actions.'''
        pass
