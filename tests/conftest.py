"""Global pytest fixtures."""
import pytest
from flask_api import db as database, create_app, register_blueprints
from flask_api.models import User
from .config import TestConfig
from flask import url_for, json

EMAIL = 'test1'
PASSWORD = 'test1'


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
    response = client.post(url, data=json.dumps(data), content_type="application/json",)
    return response.json
