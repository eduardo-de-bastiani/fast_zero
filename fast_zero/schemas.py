from pydantic import BaseModel, EmailStr


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
    
# provisorio (herda atributos do userSchema)
class UserDB(UserSchema):
    id: int
