import re
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

HASHED_PASSWORD_RE = re.compile(r"[A-Za-z\d/+=]{44}")
NAME_RE = re.compile(r"[A-Za-zА-яЁё\d]")

MIN_LENGTH = 8
MAX_LENGTH = 24

ASCII_LOWERCASE = set(ascii_lowercase)
ASCII_UPPERCASE = set(ascii_uppercase)
DIGITS = set(digits)
PUNCTUATION = set(punctuation)
AVAILABLE_CHARS = ASCII_LOWERCASE | ASCII_UPPERCASE | DIGITS | PUNCTUATION


def validate_password(password: str) -> bool:
    if re.search(HASHED_PASSWORD_RE, password):
        return True
    password_chars = set(password)
    return bool(
        (MIN_LENGTH <= len(password) <= MAX_LENGTH)
        and (password_chars & ASCII_LOWERCASE)
        and (password_chars & ASCII_UPPERCASE)
        and (password_chars & DIGITS)
        and (password_chars & PUNCTUATION)
        and not (password_chars - AVAILABLE_CHARS)
    )


def validate_name(name: str) -> bool:
    return bool(re.search(NAME_RE, name))
