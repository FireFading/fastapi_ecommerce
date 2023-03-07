from pydantic import BaseModel


class LoginCredentials(BaseModel):
    email: str
    password: str


class User(BaseModel):
    email: str
    name: str | None
    phone: str | None


class Email(BaseModel):
    email: str


class Phone(BaseModel):
    phone: str


class Name(BaseModel):
    name: str


class UpdatePassword(BaseModel):
    password: str
    confirm_password: str
