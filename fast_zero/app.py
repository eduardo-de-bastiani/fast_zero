from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fast_zero.routers import auth, tasks, users  # importando os routers
from fast_zero.schemas import Message

app = FastAPI()

origins = [
    'http://localhost:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

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
