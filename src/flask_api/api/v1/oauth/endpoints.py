import os

from authlib.integrations.flask_client import OAuth
from flask import url_for
from flask_jwt_extended import get_jwt, jwt_required
from flask_restx import Namespace, Resource, abort, fields, marshal
from flask_restx._http import HTTPStatus
from ..account.models import tokens_model
from .business import oauth_login_signup

oauth_ns = Namespace('OAuth', 'SignUp and LogIn via OAuth2')
oauth = OAuth()

if g_conf := os.environ.get('GOOGLE_CONF_URL'):
    oauth.register(
        name='google',
        server_metadata_url=g_conf,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )


@oauth_ns.route('/google', endpoint='google_request')
class GoogleOAuthRequest(Resource):
    @jwt_required(optional=True)
    def get(self, name):
        """
        Google OAuth get request
        """
        redirect_uri = url_for('google_auth', _external=True)
        return oauth.google.authorize_redirect(redirect_uri)


@oauth_ns.route('/google/authorize', doc=False, endpoint='google_auth')
class GoogleAuth(Resource):
    def get(self):
        token = oauth.google.authorize_access_token()
        user = token.get('userinfo')
        if (sub := user.get('sub')) and (email := user.get('email')):
            tokens = oauth_login_signup(sub, 'google', email, get_jwt())
            return marshal(tokens, tokens_model)
        abort(HTTPStatus.BAD_REQUEST, 'No required data provided in oauth')
