import logging
import os

from flask import make_response, request, url_for
from flask_jwt_extended import get_jwt, jwt_required, set_access_cookies
from flask_restx import Namespace, Resource, abort
from flask_restx._http import HTTPStatus

from flask_api import oauth
from flask_api.config import Config

from ..account.models import tokens_model
from .business import oauth_login_signup

logger = logging.getLogger()

oauth_ns = Namespace('OAuth', 'SignUp and LogIn via OAuth2')

if os.environ.get('GOOGLE_CLIENT_ID'):
    oauth.register(
        name='google',
        server_metadata_url=Config.GOOGLE_CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


@oauth_ns.route('/login/<name>', endpoint='oauth_request')
class OAuthRequest(Resource):
    @jwt_required(optional=True)
    @oauth_ns.param('name', 'OAuth provider name.', _in='path')
    @oauth_ns.doc(security='Bearer')
    @oauth_ns.produces(['text/html'])
    @oauth_ns.response(int(HTTPStatus.FOUND),
                       'Redirect to OAuth page, then redirect to authorize endpoint.')
    @oauth_ns.response(int(HTTPStatus.UNPROCESSABLE_ENTITY), 'Token is invalid.')
    def get(self, name):
        """
        OAuth get request
        """
        client = oauth.create_client(name)
        if not client:
            abort(HTTPStatus.NOT_FOUND, 'Given OAuth povider name not registered.')
        redirect_uri = url_for('api_v1.oauth_auth', name=name, _external=True)
        response = client.authorize_redirect(redirect_uri)
        header = request.headers.get('Authorization')
        if header:
            bearer = header.split(' ')[-1]
            response = make_response(response)
            logger.debug('set authorization cookies')
            set_access_cookies(response, bearer)
        return response


@oauth_ns.route('/authorize/<name>', endpoint='oauth_auth')
class GoogleAuth(Resource):
    @jwt_required(optional=True, locations='cookies')
    @oauth_ns.marshal_with(tokens_model, code=HTTPStatus.OK)
    @oauth_ns.response(HTTPStatus.BAD_REQUEST, 'OAuth account already assigned.')
    @oauth_ns.response(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal server error.')
    def get(self, name):
        """Redirect to this endpoint after provider's OAuth pass."""
        client = oauth.create_client(name)
        if not client:
            abort(HTTPStatus.NOT_FOUND, 'Given OAuth povider name not registered.')
        token = client.authorize_access_token()
        user = token.get('userinfo') or client.userinfo()
        if (sub := user.get('sub')) and (email := user.get('email')):
            tokens = oauth_login_signup(sub, 'google', email, get_jwt())
            return tokens
        abort(HTTPStatus.BAD_REQUEST, 'No required data provided in oauth.')
