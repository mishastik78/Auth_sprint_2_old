from flask import url_for


def register_user(test_client, email, password):
    return test_client.post(
        url_for('api.auth_register'),
        data=f'email={email}&password={password}',
        content_type='application/x-www-form-urlencoded',
    )
