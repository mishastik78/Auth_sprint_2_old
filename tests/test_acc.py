from http import HTTPStatus
from flask import url_for, json
import pytest


@pytest.mark.parametrize('endpoint, status_code', (
    ('api_v1.signup', HTTPStatus.CREATED),
    ('api_v1.login', HTTPStatus.UNAUTHORIZED)
))
def test_signup_login_new_user(client, db, endpoint, status_code):
    url = url_for(endpoint)
    data = {'email': 'test', 'password': 'test'}
    response = client.post(url, data=json.dumps(data), content_type='application/json',)
    assert response.status_code == status_code


@pytest.mark.parametrize('endpoint, status_code', (
    ('api_v1.signup', HTTPStatus.CONFLICT),
    ('api_v1.login', HTTPStatus.OK)
))
def test_signup_login_existing_user(client, db, user, endpoint, status_code):
    url = url_for(endpoint)
    data = {'email': 'test1', 'password': 'test1'}
    response = client.post(url, data=json.dumps(data), content_type='application/json',)
    assert response.status_code == status_code


@pytest.mark.parametrize('endpoint', ('api_v1.signup', 'api_v1.login'))
@pytest.mark.parametrize('email, password', (('name', 'password'), ('email', 'pasword'), ('name', 'pasword')))
def test_signup_wrong_param(client, db, user, endpoint, email, password):
    url = url_for(endpoint)
    data = {email: 'test1', password: 'test'}
    response = client.post(url, data=json.dumps(data), content_type='application/json',)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_logout(client, auth_user):
    headers = {'Authorization': f'Bearer {auth_user["access_token"]}'}
    response = client.delete(url_for('api_v1.logout'), headers=headers)
    assert response.status_code == HTTPStatus.OK
    response = client.get(url_for('api_v1.auth'), headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
