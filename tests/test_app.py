from http import HTTPStatus


def test_read_root_must_return_ok(client):  # TRIPLE A
    # client = TestClient(app)  # Arrange (organizacao)

    response = client.get('/')  # Act (acao)

    assert response.status_code == HTTPStatus.OK  # Assert (afirmacao)
    assert response.json() == {'message': 'Olá Mundo!'}
