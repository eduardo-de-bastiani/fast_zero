from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.settings import Settings

engine = create_engine(Settings().DATABASE_URL)


def get_session():  # pragma: no cover  # fala para o pytest-cov nao cobrir
    with Session(engine) as session:
        yield session
