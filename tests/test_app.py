from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_must_return_ok():  # TRIPLE A
    client = TestClient(app)  # Arrange (organizacao)

    response = client.get('/')  # Act (acao)

    assert response.status_code == HTTPStatus.OK  # Assert (afirmacao)
    assert response.json() == {'message': 'Olá Mundo!'}


def test_read_user_must_return_created():
    client = TestClient(app)

    response = client.post('/users/')

    assert response.status_code == HTTPStatus.CREATED
