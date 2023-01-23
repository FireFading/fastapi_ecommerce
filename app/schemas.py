from datetime import datetime

from pydantic import BaseModel


class LoginCredentials(BaseModel):
    email: str
    password: str


class User(BaseModel):
    email: str
    phone: str
    password: str


class Token(BaseModel):
    email: str
    exp: datetime
