from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import TaskPublic, TaskSchema
from fast_zero.security import get_current_user

router = APIRouter(prefix='/tasks', tags=['tasks'])

T_Session = Annotated[Session, Depends(get_session)]
T_User = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=TaskPublic)
def create_task(task: TaskSchema, user: T_User, session: T_Session): ...
