from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.models import User, table_registry


def test_create_user():
    engine = create_engine('sqlite:///:memory:')

    table_registry.metadata.create_all(engine)  # cria a tabela do banco enquanto testa

    with Session(engine) as session:
        user = User(username='eduardo', email='eduardo@gmail.com', password='senha1234')

        session.add(user)
        session.commit()
        session.refresh(user)

    assert user.id == 1
