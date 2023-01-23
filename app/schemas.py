from datetime import datetime

from pydantic import BaseModel


class LoginCredentials(BaseModel):
    email: str
    password: str


class User(BaseModel):
    email: str
    phone: str
    password: str


class UpdateEmail(BaseModel):
    email: str


class UpdatePhone(BaseModel):
    phone: str


class Token(BaseModel):
    email: str
    exp: datetime
