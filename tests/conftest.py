import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


# DRY (don't repeat yourself)
@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')  # cria o banco de dados em memoria
    table_registry.metadata.create_all(engine)  # cria os metadados

    with Session(engine) as session:  # cria a sessao
        yield session  # vai para test_db.py para testar

    table_registry.metadata.drop_all(engine)  # derruba o db depois de testar
