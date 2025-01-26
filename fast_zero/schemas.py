from pydantic import BaseModel, ConfigDict, EmailStr

from fast_zero.models import TaskState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


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
    description: str
    state: TaskState


# retorna todo o TaskSchema + id
class TaskPublic(TaskSchema):
    id: int


class TaskList(BaseModel):
    tasks: list[TaskPublic]
