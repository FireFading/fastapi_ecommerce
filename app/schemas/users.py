import re

from app.config import (
    ASCII_LOWERCASE,
    ASCII_UPPERCASE,
    AVAILABLE_CHARS,
    DIGITS,
    HASHED_PASSWORD_RE,
    MAX_NAME_LEN,
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
    NAME_RE,
    PUNCTUATION,
)
from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, validates


class LoginCredentials(BaseModel):
    email: EmailStr
    password: str


class Name(BaseModel):
    name: str | None

    @validates("name")
    def validate_name(self, name: str) -> str:
        if not name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Name field is empty",
            )
        if len(name) > MAX_NAME_LEN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Name field average max symbols :: {MAX_NAME_LEN}",
            )
        if not bool(re.search(NAME_RE, name)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid symbols in name field",
            )
        return name


class Email(BaseModel):
    email: EmailStr | None


class User(Name, Email, BaseModel):
    phone: str | None


class Phone(BaseModel):
    phone: str


class UpdatePassword(BaseModel):
    password: str
    confirm_password: str

    @validates("confirm_password")
    def validate_password(self, confirm_password: str) -> bool:
        if re.search(HASHED_PASSWORD_RE, confirm_password):
            return True
        password_chars = set(confirm_password)
        return bool(
            (MIN_PASSWORD_LENGTH <= len(confirm_password) <= MAX_PASSWORD_LENGTH)
            and (password_chars & ASCII_LOWERCASE)
            and (password_chars & ASCII_UPPERCASE)
            and (password_chars & DIGITS)
            and (password_chars & PUNCTUATION)
            and not (password_chars - AVAILABLE_CHARS)
        )
