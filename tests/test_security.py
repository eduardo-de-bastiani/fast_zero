from http import HTTPStatus

import pytest
from fastapi.exceptions import HTTPException
from jwt import decode

from fast_zero.security import (
    create_access_token,
    get_current_user,
    settings,
)


def test_jwt():
    data = {'sub': 'teste@teste.com '}

    token = create_access_token(data)

    result = decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)

    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_must_return_jwt_error():
    with pytest.raises(HTTPException):
        get_current_user({})


def test_get_current_user_must_return_credentials_exception():
    with pytest.raises(HTTPException):
        get_current_user({'sub': 'Jefferson@gmail.com'})


def test_get_current_user_without_sub():
    token = create_access_token(data={})

    with pytest.raises(HTTPException):
        get_current_user(token=token)


def test_jwt_valid_token_with_user_not_exists(client, token):
    # remove o proprio usuario
    client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    # tenta remover novamente
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
