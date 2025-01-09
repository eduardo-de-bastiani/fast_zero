from pwdlib import PasswordHash
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


from jwt import encode

pwd_context = PasswordHash.recommended()



def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    pwd_context.verify(plain_password, hashed_password)


def create_access_toke(data: dict):
    