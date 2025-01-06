import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import table_registry, User

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
def session():
    engine = create_engine(
        'sqlite:///:memory:',  # cria o banco de dados em memoria
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)  # cria os metadados

    with Session(engine) as session:  # cria a sessao
        yield session  # vai para test_db.py para testar

    table_registry.metadata.drop_all(engine)  # derruba o db depois de testar


# fixture para testes novos usuarios
@pytest.fixture
def user(session):
    user = User(username='teste', email='teste@test.com', password='teste123')
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user