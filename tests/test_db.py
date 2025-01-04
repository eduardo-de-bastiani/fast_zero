from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='eduardo', email='eduardo@gmail.com', password='senha1234')

    session.add(user)
    session.commit()
    result = session.scalar(select(User).where(User.email == 'eduardo@gmail.com'))

    assert result.username == 'eduardo'
