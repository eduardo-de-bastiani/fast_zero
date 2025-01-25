from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import Task, User
from fast_zero.schemas import TaskPublic, TaskSchema, TaskList
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
def list_tasks(
    session: T_Session, 
    user: T_CurrentUser, 
    title: str | None = None,
    description: str | None = None,
    state: str | None = None,
    offset: int | None = None,
    limit: int| None = None,
    ):
    ...