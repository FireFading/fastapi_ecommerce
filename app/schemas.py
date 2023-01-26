from datetime import datetime

from pydantic import BaseModel


class LoginCredentials(BaseModel):
    email: str
    password: str


class User(BaseModel):
    email: str
    phone: str
    password: str


class Email(BaseModel):
    email: str


class Phone(BaseModel):
    phone: str


class ResetPassword(BaseModel):
    password: str
    confirm_password: str
