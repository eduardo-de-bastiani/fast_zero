from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models import TaskState


class Message(BaseModel):
    message: str


class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str


# para atualizacao de usuarios
class UserSchema(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


# schema retornado do usuario (nao queremos retornar senha e ainda nao temos id)
class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TaskSchema(BaseModel):
    title: str
    description: Optional[str] = None
    state: TaskState


# retorna todo o TaskSchema + id
class TaskPublic(TaskSchema):
    id: int


class TaskList(BaseModel):
    tasks: list[TaskPublic]


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TaskState | None = None
