from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_read_root_must_return_ok(client):  # TRIPLE A
    # client = TestClient(app)  # Arrange (organizacao)

    response = client.get('/')  # Act (acao)

    assert response.status_code == HTTPStatus.OK  # Assert (afirmacao)
    assert response.json() == {'message': 'Olá Mundo!'}


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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'id': 1,
            'username': 'novo_username',
            'email': 'emailteste@teste.com',
            'password': 'senha_teste',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'novo_username',
        'email': 'emailteste@teste.com',
    }


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
