from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.routers import auth, tasks, users  # importando os routers
from fast_zero.schemas import Message

app = FastAPI()

# incluindo os endpoints
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(tasks.router)


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
    responses={'200': {'model': Message}, '404': {'model': Message}},
)
def read_root():
    return {'message': 'Olá Mundo!'}
