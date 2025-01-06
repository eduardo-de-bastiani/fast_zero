from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()


database = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    # injecao de dependencias (executa a funcao e depois passa como argumento)
    db_user = session.scalar(
        select(User).where(or_(User.username == user.username, User.email == user.email))
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Username already exists'
            )

        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Email already exists'
            )

    db_user = User(username=user.username, email=user.email, password=user.password)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)  # nao precisa status code OK (standard)
def read_users(
    limit: int = 10,
    skip: int = 0,
    session: Session = Depends(get_session)
    ):
    users = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, datail='User not foud')

    user_with_id = UserDB(
        id=user_id,
        **user.model_dump(),
    )

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, datail='User not foud')

    del database[user_id - 1]

    return {'message': 'User deleted'}
