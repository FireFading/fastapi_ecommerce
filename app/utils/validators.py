import re
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

from fastapi import HTTPException, status

PASSWORD_RE = re.compile(r"[A-Za-z\d/+=]{44}")
NAME_RE = re.compile(r"[A-Za-zА-яЁё\d]")

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 24

ASCII_LOWERCASE = set(ascii_lowercase)
ASCII_UPPERCASE = set(ascii_uppercase)
DIGITS = set(digits)
PUNCTUATION = set(punctuation)
AVAILABLE_CHARS = ASCII_LOWERCASE | ASCII_UPPERCASE | DIGITS | PUNCTUATION

MAX_NAME_LEN = 100


def validate_password(password: str) -> str | HTTPException:
    if re.search(PASSWORD_RE, password):
        return True
    password_chars = set(password)
    if not (
        (MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH)
        and (password_chars & ASCII_LOWERCASE)
        and (password_chars & ASCII_UPPERCASE)
        and (password_chars & DIGITS)
        and (password_chars & PUNCTUATION)
        and not (password_chars - AVAILABLE_CHARS)
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid validate password",
        )
    return password


def validate_name(name: str | None = None) -> str | None | HTTPException:
    if not name:
        return None
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
