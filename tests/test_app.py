from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_must_return_ok():  # TRIPLE A
    client = TestClient(app)  # Arrange (organizacao)

    response = client.get('/')  # Act (acao)

    assert response.status_code == HTTPStatus.OK  # Assert (afirmacao)
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user():
    client = TestClient(app)

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
