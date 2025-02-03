from http import HTTPStatus

from fast_zero.schemas import UserPublic
from tests.factories import UserFactory


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'teste_username',
            'email': 'emailteste@teste.com',
            'password': 'senha_teste',
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    assert response.json() == {
        'id': 1,
        'username': 'teste_username',
        'email': 'emailteste@teste.com',
    }


def test_create_user_same_name(client, session):
    user = UserFactory(username='teste_teste')
    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.post(
        '/users/',
        json={
            'username': 'teste_teste',
            'email': 'emailteste@teste.com',
            'password': 'senha_teste',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_same_email(client, session):
    user = UserFactory(email='emailteste@teste.com')
    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.post(
        '/users/',
        json={
            'username': 'teste_teste',
            'email': 'emailteste@teste.com',
            'password': 'senha_teste',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
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

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': user.id,
        'username': 'novo_username',
        'email': 'emailteste@teste.com',
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',  # certifica que nao eh o usuario permitido
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'novo_username',
            'email': 'emailteste@teste.com',
            'password': 'senha_teste',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',  # certifica que nao eh o usuario permitido
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
