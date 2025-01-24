from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):
    response = client.post(
        '/auth/token', data={'username': user.email, 'password': user.clean_password}
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert token['access_token']


def test_token_expired_after_time(client, user):
    with freeze_time('2025-01-5 12:00:00'):
        # gera o token (12:00)
        response = client.post(
            '/auth/token', data={'username': user.email, 'password': user.clean_password}
        )

        assert response.status_code == HTTPStatus.OK

        token = response.json()['access_token']

    with freeze_time('2025-01-5 12:31:00'):
        # Usa o token (12:31)   # expirado!

        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'id': user.id,
                'username': 'novo_username',
                'email': 'emailteste@teste.com',
                'password': 'senha_teste',
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_wrong_password(client, user):
    response = client.post(
        'auth/token', data={'username': user.email, 'password': 'wrong_password'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_wrong_email(client, user):
    response = client.post(
        'auth/token',
        data={'username': 'email_errado@teste.com', 'password': user.clean_password},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(client, token):
    response = client.post(
        'auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'Bearer'


def test_token_expired_dont_refresh(client, user, token):
    with freeze_time('2025-01-5 12:00:00'):
        # gera o token (12:00)
        response = client.post(
            '/auth/token', data={'username': user.email, 'password': user.clean_password}
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2025-01-5 12:31:00'):
        # Usa o token (12:31)   # expirado!

        response = client.post(
            '/auth/refresh_token', data={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Not authenticated'}
