import uuid

from app.utils.validators import validate_name, validate_password
from pydantic import BaseModel, EmailStr, validator


class Email(BaseModel):
    email: EmailStr


class LoginCredentials(Email, BaseModel):
    password: str


class CreateUser(Email, BaseModel):
    password: str

    @validator("password")
    def validate_password(cls, password: str) -> str | ValueError:
        return validate_password(password=password)


class Name(BaseModel):
    name: str

    @validator("name")
    def validate_name(cls, name: str | None = None) -> str | None | ValueError:
        return validate_name(name=name)


class Phone(BaseModel):
    phone: str


class User(BaseModel):
    guid: uuid.UUID
    email: EmailStr | None
    phone: str | None
    name: str | None

    class Config:
        orm_mode = True


class UpdatePassword(BaseModel):
    password: str
    confirm_password: str

    @validator("confirm_password")
    def validate_password(cls, confirm_password: str) -> str | ValueError:
        return validate_password(password=confirm_password)
