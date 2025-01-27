from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Task, TaskState, User
from fast_zero.schemas import Message, TaskList, TaskPublic, TaskSchema, TaskUpdate
from fast_zero.security import get_current_user

router = APIRouter(prefix='/tasks', tags=['tasks'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TaskPublic)
def create_task(task: TaskSchema, user: T_CurrentUser, session: T_Session):
    db_task = Task(
        title=task.title,
        description=task.description,
        state=task.state,
        user_id=user.id,
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


# endpoint que filtra tasks por diversos campos


@router.get('/', response_model=TaskList)
def list_tasks(  # noqa: PLR0913, PLR0917   # ruff ignorar mais de 5 parametros
    session: T_Session,
    user: T_CurrentUser,
    title: str | None = None,
    description: str | None = None,
    state: TaskState | None = None,
    offset: int | None = None,
    limit: int | None = None,
):
    # inicialmente filtra dentro da aplicacao pelo proprio usuario
    query = select(Task).where(Task.user_id == user.id)

    if title:
        query = query.filter(Task.title.contains(title))
    if description:
        query = query.filter(Task.description.contains(description))
    if state:
        query = query.filter(Task.state == state)

    # pega as tasks filtradas com offset e limit no banco
    tasks = session.scalars(query.offset(offset).limit(limit)).all()

    return {'tasks': tasks}


@router.delete('/{task_id}', response_model=Message)
def delete_task(task_id: int, session: T_Session, user: T_CurrentUser):
    task = session.scalar(select(Task).where(Task.user_id == user.id, Task.id == task_id))

    if not task:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not found')

    session.delete(task)
    session.commit()

    return {'message': 'Task deleted successfully'}


@router.patch('/{task_id}', response_model=TaskPublic)
def update_task(task_id: int, session: T_Session, user: T_CurrentUser, task: TaskUpdate):
    db_task = session.scalar(
        select(Task).where(Task.id == task_id, Task.user_id == user.id)
    )

    if not db_task:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Task not found')

    # exclui os valores False do TaskUpdate (campos que nao foram marcados)
    for key, value in task.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task
