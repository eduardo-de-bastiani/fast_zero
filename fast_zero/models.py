from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


# enum dos estados das tasks
class TaskState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


@table_registry.mapped_as_dataclass
class User:  # registro escalar
    __tablename__ = 'users'  # nome da tabela dentro do banco de dados

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


@table_registry.mapped_as_dataclass
class Task:
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    state: Mapped[TaskState]
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())


    # relacionamento entre a task e o usuario
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
