from http import HTTPStatus
from time import sleep

from flask import current_app, url_for


def test_auth_anonimous(client):
    url = url_for('api_v1.auth')
    response = client.get(url)
    assert response.status_code == HTTPStatus.UPGRADE_REQUIRED
    assert 'Anonymous User' in response.json['user']


def test_auth_access_token(client, auth_user):
    url = url_for('api_v1.auth')
    response = client.get(url, headers={'Authorization': f'Bearer {auth_user["access_token"]}'})
    assert response.status_code == HTTPStatus.OK
    assert 'id' in response.json
    assert 'roles' in response.json


def test_auth_access_expired(client, auth_user):
    time = current_app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
    sleep(time + 1)
    url = url_for('api_v1.auth')
    assert client.get(
        url, headers={'Authorization': f'Bearer {auth_user["access_token"]}'}).status_code == HTTPStatus.UNAUTHORIZED


def test_auth_refresh_instead_access(client, auth_user):
    url = url_for('api_v1.auth')
    assert client.get(url, headers={'Authorization': f'Bearer {auth_user["refresh_token"]}'}
                      ).status_code == HTTPStatus.UNPROCESSABLE_ENTITY
