from http import HTTPStatus

from flask import json, url_for

from flask_api.models import Role


def test_create_role(client, auth_admin_header):
    data = {'name': 'New Role', 'description': 'Some description.'}
    response = client.post(url_for('api_v1.manage'), data=json.dumps(
        data), content_type='application/json', headers=auth_admin_header)
    assert response.status_code == HTTPStatus.CREATED
    assert 'New Role' == response.json['name']
    assert 'Some description.' == response.json['description']
    assert 'id' in response.json
    assert Role.find_by_name('New Role')


def test_create_errors(client, role, auth_user, auth_admin_header):
    # Пытаемся создать клон
    data = {'name': 'Test Role', 'description': 'Some description.'}
    response = client.post(url_for('api_v1.manage'), data=json.dumps(
        data), content_type='application/json', headers=auth_admin_header)
    assert response.status_code == HTTPStatus.CONFLICT
    # Посылаем запрос без админских прав
    response = client.post(url_for('api_v1.manage'), data=json.dumps(
        data), content_type='application/json', headers={'Authorization': f'Bearer {auth_user["access_token"]}'})
    assert response.status_code != HTTPStatus.OK


def test_get_roles(client, role, auth_admin_header):
    response = client.get(url_for('api_v1.manage'), headers=auth_admin_header)
    assert response.status_code == HTTPStatus.OK
    assert next((item for item in response.json if item['name'] == 'Test Role'), False)
    data = {'name': 'New Role', 'description': 'Some description.'}
    response = client.post(url_for('api_v1.manage'), data=json.dumps(
        data), content_type='application/json', headers=auth_admin_header)
    response = client.get(url_for('api_v1.manage'), headers=auth_admin_header)
    names = [item['name'] for item in response.json]
    assert 'New Role' in names
    assert 'Test Role' in names
    assert len(names) == 2


def test_get_errors(client, auth_user):
    # Посылаем запрос без админских прав
    response = client.get(url_for('api_v1.manage'), headers={
                          'Authorization': f'Bearer {auth_user["access_token"]}'})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_role(client, role, auth_admin_header):
    response = client.get(url_for('api_v1.manage'), headers=auth_admin_header)
    assert len(response.json) == 1
    response = client.delete(url_for('api_v1.manage'), data=json.dumps(
        {'id': role.id}), headers=auth_admin_header, content_type='application/json')
    assert response.status_code == HTTPStatus.OK
    response = client.get(url_for('api_v1.manage'), headers=auth_admin_header)
    assert len(response.json) == 0


def test_delete_errors(client, user, auth_user, auth_admin_header):
    # Пытаемся передать не верный id
    response = client.delete(url_for('api_v1.manage'), data=json.dumps(
        {'id': 'hvbsuveuvow'}), headers=auth_admin_header, content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    # Пытаемся передать валидный uuid, но которого нет в базе ролей
    response = client.delete(url_for('api_v1.manage'), data=json.dumps(
        {'id': user.id}), headers=auth_admin_header, content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    # Пытаемся передать не id
    response = client.delete(url_for('api_v1.manage'), data=json.dumps(
        {'role_id': user.id}), headers=auth_admin_header, content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    # Посылаем запрос без админских прав
    response = client.delete(
        url_for('api_v1.manage'),
        data=json.dumps({'id': user.id}),
        content_type='application/json',
        headers={'Authorization': f'Bearer {auth_user["access_token"]}'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_patch_role(client, role, auth_admin_header):
    assert role.name == 'Test Role'
    assert role.description == 'Some description.'
    data = {'id': role.id, 'new_name': 'New Role'}
    response = client.patch(url_for('api_v1.manage'), data=json.dumps(
        data), headers=auth_admin_header, content_type='application/json')
    assert response.status_code == HTTPStatus.OK
    assert role.name == 'New Role'
    assert role.description == 'Some description.'
    data = {'id': role.id, 'new_description': 'Test description.'}
    response = client.patch(url_for('api_v1.manage'), data=json.dumps(
        data), headers=auth_admin_header, content_type='application/json')
    assert response.status_code == HTTPStatus.OK
    assert role.name == 'New Role'
    assert role.description == 'Test description.'


def test_patch_errors(client, role, user, auth_user, auth_admin_header):
    # Пытаемся переименовать на имеющееся имя
    data = {'name': 'New Role', 'description': 'Some description.'}
    response = client.post(url_for('api_v1.manage'), data=json.dumps(
        data), content_type='application/json', headers=auth_admin_header)
    data = {'id': role.id, 'new_name': 'New Role'}
    response = client.patch(url_for('api_v1.manage'), data=json.dumps(
        data), headers=auth_admin_header, content_type='application/json')
    assert response.status_code == HTTPStatus.CONFLICT
    # Передаем неверные ключи
    data = {'id': user.id, 'name': 'New Role'}
    response = client.patch(url_for('api_v1.manage'), data=json.dumps(
        data), headers=auth_admin_header, content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    # Передаем uuid несуществующей роли
    data = {'id': user.id, 'new_name': 'New Role'}
    response = client.patch(url_for('api_v1.manage'), data=json.dumps(
        data), headers=auth_admin_header, content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    # Посылаем запрос без админских прав
    response = client.patch(url_for('api_v1.manage'), data=json.dumps(
        data), content_type='application/json', headers={'Authorization': f'Bearer {auth_user["access_token"]}'})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_assign_role(client, user, role, auth_user, auth_admin_header):
    data = {'user_id': user.id, 'role_id': role.id}
    response = client.post(url_for('api_v1.assign'), data=json.dumps(
        data), headers=auth_admin_header, content_type='application/json')
    assert response.status_code == HTTPStatus.OK
    assert role in user.roles
    # Проверяем что токен отозван
    response = client.get(url_for('api_v1.auth'), headers={'Authorization': f'Bearer {auth_user["access_token"]}'})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_assign_errors(client, user, role, auth_user, auth_admin_header):
    # Меняем местами параметры
    data = {'user_id': role.id, 'role_id': user.id}
    response = client.post(url_for('api_v1.assign'), data=json.dumps(
        data), headers=auth_admin_header, content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    # Посылаем запрос без админских прав
    response = client.post(url_for('api_v1.assign'), data=json.dumps(
        data), content_type='application/json', headers={'Authorization': f'Bearer {auth_user["access_token"]}'})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_unassign_role(client, db, user, role, auth_user, auth_admin_header):
    user.roles.append(role)
    db.session.commit()
    data = {'user_id': user.id, 'role_id': role.id}
    response = client.delete(url_for('api_v1.assign'), data=json.dumps(
        data), headers=auth_admin_header, content_type='application/json')
    assert response.status_code == HTTPStatus.OK
    assert role not in user.roles
    # Проверяем что токен отозван
    response = client.get(url_for('api_v1.auth'), headers={'Authorization': f'Bearer {auth_user["access_token"]}'})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_unassign_errors(client, user, role, auth_user, auth_admin_header):
    # Меняем местами параметры
    data = {'user_id': role.id, 'role_id': user.id}
    response = client.delete(url_for('api_v1.assign'), data=json.dumps(
        data), headers=auth_admin_header, content_type='application/json')
    assert response.status_code == HTTPStatus.BAD_REQUEST
    # Посылаем запрос без админских прав
    response = client.delete(url_for('api_v1.assign'), data=json.dumps(
        data), content_type='application/json', headers={'Authorization': f'Bearer {auth_user["access_token"]}'})
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_check_roles(client, db, user, role, auth_admin_header):
    user.roles.append(role)
    db.session.commit()
    data = {'user_id': user.id, 'role_id': role.id}
    assert client.get(url_for('api_v1.assign'), data=json.dumps(
        data), content_type='application/json', headers=auth_admin_header).status_code == HTTPStatus.OK


def test_check_errors(client, user, auth_user, role, auth_admin_header):
    # Посылаем неверный id
    data = {'user_id': 'gvyicih vkuftccg', 'role_id': 'gvyicih vkuftccg'}
    assert client.get(url_for('api_v1.assign'), headers=auth_admin_header, data=json.dumps(
        data), content_type='application/json').status_code == HTTPStatus.BAD_REQUEST
    # Посылаем uuid несуществующего пользователя
    data = {'user_id': role.id, 'role_id': user.id}
    assert client.get(url_for('api_v1.assign'), headers=auth_admin_header, data=json.dumps(
        data), content_type='application/json').status_code == HTTPStatus.BAD_REQUEST
    # Посылаем запрос без админских прав
    data = {'user_id': user.id, 'role_id': role.id}
    assert client.get(url_for('api_v1.assign'), data=json.dumps(
        data), content_type='application/json', headers={
        'Authorization': f'Bearer {auth_user["access_token"]}'}).status_code == HTTPStatus.UNAUTHORIZED
