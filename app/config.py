import re
from string import ascii_lowercase, ascii_uppercase, digits, punctuation

from app.settings import Settings

HASHED_PASSWORD_RE = re.compile(r"[A-Za-z\d/+=]{44}")
NAME_RE = re.compile(r"[A-Za-zА-яЁё\d]")

MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 24

ASCII_LOWERCASE = set(ascii_lowercase)
ASCII_UPPERCASE = set(ascii_uppercase)
DIGITS = set(digits)
PUNCTUATION = set(punctuation)
AVAILABLE_CHARS = ASCII_LOWERCASE | ASCII_UPPERCASE | DIGITS | PUNCTUATION

MAX_NAME_LEN = 100

settings = Settings(_env_file=".env.example")
jwt_settings = Settings(_env_file=".env.example")
