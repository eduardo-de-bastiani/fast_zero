from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema
from fast_zero.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(
    prefix='/users',  # adiciona prefixo de rota compartilhada
    tags=['users'],
)

# com Annotated, definimos o tipo e atribuimos o valor
# antes tinhamos ->  session: Session = Depends(get_session)
T_Session = Annotated[Session, Depends(get_session)]  # Tipo Session (padronizacao)

T_CurrentUser = Annotated[User, Depends(get_current_user)]  # Tipo Current_User


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
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

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', response_model=UserList)  # nao precisa status code OK (standard)
def read_users(
    session: T_Session,
    limit: int | None = None,
    skip: int | None = None,
):
    users = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(HTTPStatus.FORBIDDEN, detail='Not enough permissions')

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    session: T_Session,
    user_id: int,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(HTTPStatus.FORBIDDEN, detail='Not enough permissions')

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
