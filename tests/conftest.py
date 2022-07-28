"""Global pytest fixtures."""
import pytest
from flask import json, url_for

from flask_api import create_app
from flask_api import db as database
from flask_api import register_blueprints
from flask_api.models import Role, User

from .config import TestConfig

EMAIL = 'test1@test.test'
PASSWORD = 'test1Test-'


ADMIN_EMAIL = 'admin@test.test'


@pytest.fixture
def app():
    app = create_app(TestConfig)
    register_blueprints(app)
    return app


@pytest.fixture
def db(app, client, request):
    database.drop_all()
    database.create_all()
    database.session.commit()

    def fin():
        database.session.remove()

    request.addfinalizer(fin)
    return database


@pytest.fixture
def user(db):
    user = User(email=EMAIL, password=PASSWORD)
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def auth_user(client, user):
    url = url_for('api_v1.login')
    data = {'email': EMAIL, 'password': PASSWORD}
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    return response.json


@pytest.fixture
def auth_admin_header(client, db):
    user = User(email=ADMIN_EMAIL, password=PASSWORD, is_superuser=True)
    db.session.add(user)
    db.session.commit()
    url = url_for('api_v1.login')
    data = {'email': ADMIN_EMAIL, 'password': PASSWORD}
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    return {'Authorization': f'Bearer {response.json["access_token"]}'}


@pytest.fixture
def role(db):
    role = Role(name='Test Role', description='Some description.')
    db.session.add(role)
    db.session.commit()
    return role
