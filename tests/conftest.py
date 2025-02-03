from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import table_registry
from fast_zero.security import get_password_hash
from tests.factories import UserFactory


# cria uma unica conexao com o banco (mas sem interdependencia entre os testes)
@pytest.fixture(scope='session')  # roda a fixture por 'sessao' de teste (apenas 1 vez)
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


# DRY (don't repeat yourself)


# fixture para trocar as sessoes quando testar
@pytest.fixture
def client(session):
    def get_test_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_test_session

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


# fixture para teste de usuario
@pytest.fixture
def user(session):
    pwd = 'senhateste'

    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # Monkey Patch

    return user


# fixture para testes novos usuarios
@pytest.fixture
def other_user(session):
    user = UserFactory()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token', data={'username': user.email, 'password': user.clean_password}
    )
    return response.json()['access_token']
