from app.utils.validators import validate_name, validate_password
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator


class LoginCredentials(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def validate_password(cls, password: str) -> str | HTTPException:
        return validate_password(password=password)


class Name(BaseModel):
    name: str | None

    @validator("name")
    def validate_name(cls, name: str | None = None) -> str | None | HTTPException:
        return validate_name(name=name)


class Phone(BaseModel):
    phone: str


class Email(BaseModel):
    email: EmailStr


class User(BaseModel):
    email: EmailStr | None
    phone: str | None
    name: str | None


class UpdatePassword(BaseModel):
    password: str
    confirm_password: str

    @validator("confirm_password")
    def validate_password(cls, confirm_password: str) -> str | HTTPException:
        return validate_password(password=confirm_password)
