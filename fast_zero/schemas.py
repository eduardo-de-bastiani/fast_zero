from pydantic import BaseModel, ConfigDict, EmailStr


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


# provisorio (herda atributos do userSchema)
class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]
